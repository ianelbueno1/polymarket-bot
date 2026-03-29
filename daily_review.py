"""
Daily Review — Polymarket Auto-Research Evaluation Script
=========================================================
Calcula metricas de performance del bot basado en trades reales.
Este script es el equivalente al prepare.py de Karpathy:
el agente NO PUEDE modificar este archivo.

Uso:
    python daily_review.py              # Generar reporte del dia
    python daily_review.py --json       # Output JSON para el agente
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
TRADES_FILE = DATA_DIR / "trades.json"
BOT_STATE_FILE = DATA_DIR / "bot_state.json"
PORTFOLIO_FILE = DATA_DIR / "portfolio.json"
REPORT_FILE = DATA_DIR / "daily_report.json"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"

INITIAL_BALANCE = 1000.0


def load_json(filepath, default):
    if filepath.exists():
        with open(filepath, "r") as f:
            return json.load(f)
    return default


def get_trades():
    return load_json(TRADES_FILE, [])


def get_sells(trades):
    return [t for t in trades if t["type"] == "SELL"]


def get_buys(trades):
    return [t for t in trades if t["type"] == "BUY"]


def trades_in_window(trades, days):
    """Filtrar trades de los ultimos N dias."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    return [t for t in trades if t.get("timestamp", "") >= cutoff]


def calc_metrics(sells):
    """Calcular metricas core de una lista de sells."""
    if not sells:
        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "avg_pnl": 0,
            "avg_win": 0,
            "avg_loss": 0,
            "win_loss_ratio": 0,
            "best_trade": 0,
            "worst_trade": 0,
        }

    pnls = [t.get("pnl", 0) for t in sells]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]

    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = abs(sum(losses) / len(losses)) if losses else 0

    return {
        "total_trades": len(sells),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": round(len(wins) / len(sells) * 100, 1) if sells else 0,
        "total_pnl": round(sum(pnls), 2),
        "avg_pnl": round(sum(pnls) / len(pnls), 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "win_loss_ratio": round(avg_win / avg_loss, 2) if avg_loss > 0 else 0,
        "best_trade": round(max(pnls), 2) if pnls else 0,
        "worst_trade": round(min(pnls), 2) if pnls else 0,
    }


def calc_sizing_adherence(buys):
    """Verificar si los trades respetan las reglas de sizing de STRATEGY.md."""
    if not buys:
        return {"total_buys": 0, "within_limits": 0, "oversized": 0, "adherence_pct": 100}

    within = 0
    over = 0
    for t in buys:
        amount = t.get("amount", 0)
        if amount <= 10:  # Max $10 por trade segun STRATEGY.md
            within += 1
        else:
            over += 1

    return {
        "total_buys": len(buys),
        "within_limits": within,
        "oversized": over,
        "adherence_pct": round(within / len(buys) * 100, 1),
    }


def generate_report():
    """Generar reporte completo de metricas."""
    trades = get_trades()
    all_sells = get_sells(trades)
    all_buys = get_buys(trades)

    portfolio = load_json(PORTFOLIO_FILE, {"balance": INITIAL_BALANCE, "positions": {}})
    bot_state = load_json(BOT_STATE_FILE, {})

    # Metricas por ventana temporal
    sells_7d = get_sells(trades_in_window(trades, 7))
    sells_30d = get_sells(trades_in_window(trades, 30))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "portfolio": {
            "balance": portfolio.get("balance", INITIAL_BALANCE),
            "open_positions": len(portfolio.get("positions", {})),
            "total_value_approx": portfolio.get("balance", INITIAL_BALANCE),
            "return_pct": round(
                (portfolio.get("balance", INITIAL_BALANCE) - INITIAL_BALANCE)
                / INITIAL_BALANCE
                * 100,
                1,
            ),
        },
        "all_time": calc_metrics(all_sells),
        "last_7_days": calc_metrics(sells_7d),
        "last_30_days": calc_metrics(sells_30d),
        "sizing_adherence": calc_sizing_adherence(all_buys),
        "bot_state": {
            "total_pnl": bot_state.get("total_pnl", 0),
            "daily_pnl": bot_state.get("daily_pnl", 0),
            "signals_generated": bot_state.get("signals_generated", 0),
            "trades_executed": bot_state.get("trades_executed", 0),
        },
    }

    return report


def save_report(report):
    """Guardar reporte como JSON."""
    REPORT_FILE.parent.mkdir(exist_ok=True)
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)


def save_snapshot(report):
    """Guardar snapshot diario para el agente remoto."""
    SNAPSHOTS_DIR.mkdir(exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    snapshot_file = SNAPSHOTS_DIR / f"snapshot_{date_str}.json"

    # Incluir trades recientes en el snapshot para que el agente los vea
    trades = get_trades()
    recent_trades = trades_in_window(trades, 7)

    snapshot = {
        **report,
        "recent_trades": recent_trades,
    }

    with open(snapshot_file, "w") as f:
        json.dump(snapshot, f, indent=2)

    return snapshot_file


def print_report(report):
    """Mostrar reporte en consola."""
    print(f"\n{'='*60}")
    print(f"  DAILY REVIEW — {report['generated_at'][:10]}")
    print(f"{'='*60}")

    p = report["portfolio"]
    print(f"\n  Portfolio:")
    print(f"    Balance: ${p['balance']:.2f}")
    print(f"    Posiciones abiertas: {p['open_positions']}")
    print(f"    Retorno: {p['return_pct']}%")

    for label, key in [
        ("All Time", "all_time"),
        ("Last 7 Days", "last_7_days"),
        ("Last 30 Days", "last_30_days"),
    ]:
        m = report[key]
        print(f"\n  {label}:")
        print(f"    Trades: {m['total_trades']} (W:{m['wins']} L:{m['losses']})")
        print(f"    Win rate: {m['win_rate']}%")
        print(f"    P&L: ${m['total_pnl']}")
        print(f"    Avg P&L: ${m['avg_pnl']}")
        print(f"    Avg Win/Loss: ${m['avg_win']} / ${m['avg_loss']}")
        print(f"    W/L Ratio: {m['win_loss_ratio']}")

    s = report["sizing_adherence"]
    print(f"\n  Sizing Adherence:")
    print(f"    {s['adherence_pct']}% dentro de limites ({s['oversized']} oversized)")

    print(f"\n{'='*60}")


if __name__ == "__main__":
    report = generate_report()

    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)

    save_report(report)
    snapshot_path = save_snapshot(report)
    print(f"\n  Snapshot guardado: {snapshot_path}")

"""
Polymarket Auto Trader — Risk Management Only
===============================================
El bot SOLO gestiona riesgo de posiciones existentes:
- Take profit (+30%)
- Stop loss (-50%)
- Stop loss diario ($50)
- Detecta mercados resueltos

Los trades los mete Ian + Claude en sesiones diarias.

Uso:
    python auto_trader.py              # Correr monitor en loop
    python auto_trader.py --once       # Un solo chequeo
    python auto_trader.py --stats      # Ver estadísticas
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import paper_trader as pt

# ============================================================
# CONFIG
# ============================================================
SCAN_INTERVAL = 300         # Segundos entre scans (5 min)
TAKE_PROFIT = 999           # No auto-cerrar por ganancia — hold hasta resolución
STOP_LOSS_PCT = -999        # No auto-cerrar por pérdida — hold hasta resolución
MAX_DAILY_LOSS = 50.0       # Stop loss diario

DATA_DIR = Path(__file__).parent / "data"
BOT_STATE_FILE = DATA_DIR / "bot_state.json"
BOT_LOG_FILE = DATA_DIR / "bot_log.json"

# ============================================================
# BOT STATE
# ============================================================

def load_bot_state():
    default = {
        "total_trades": 0,
        "wins": 0,
        "losses": 0,
        "total_pnl": 0,
        "daily_trades": 0,
        "daily_pnl": 0,
        "daily_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "last_scan": None,
        "signals_generated": 0,
        "trades_executed": 0,
    }
    return pt.load_json(BOT_STATE_FILE, default)

def save_bot_state(state):
    pt.save_json(BOT_STATE_FILE, state)

def reset_daily_if_needed(state):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if state["daily_date"] != today:
        state["daily_trades"] = 0
        state["daily_pnl"] = 0
        state["daily_date"] = today
    return state

def log_bot_action(action, details):
    logs = pt.load_json(BOT_LOG_FILE, [])
    logs.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        **details
    })
    if len(logs) > 500:
        logs = logs[-500:]
    pt.save_json(BOT_LOG_FILE, logs)

# ============================================================
# RISK MANAGEMENT
# ============================================================

def check_and_manage_exits():
    """Check all positions for TP/SL and auto-exit if triggered."""
    state = load_bot_state()
    state = reset_daily_if_needed(state)

    portfolio = pt.load_portfolio()
    n_positions = len(portfolio.get("positions", {}))

    now = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"\n{'='*60}")
    print(f"  RISK CHECK @ {now} | Balance: ${portfolio['balance']:.2f} | Pos: {n_positions}")
    print(f"{'='*60}")

    # Fetch all markets once
    print(f"  Fetching markets...")
    markets = pt.fetch_markets(limit=200)
    print(f"  Got {len(markets)} markets")

    # Build lookup
    market_lookup = {}
    for m in markets:
        cid = m.get("conditionId", "")
        market_lookup[cid[:10]] = m

    exits_done = 0

    for key, pos in list(portfolio.get("positions", {}).items()):
        cid = pos.get("condition_id", "")
        market = market_lookup.get(cid[:10])

        if not market:
            print(f"  {pos['question'][:40]} — no encontrado en mercados activos (puede haber cerrado)")
            continue

        prices = market.get("outcomePrices")
        if isinstance(prices, str):
            prices = json.loads(prices)

        side_idx = 0 if pos["side"] == "YES" else 1
        current_price = float(prices[side_idx])
        current_value = pos["shares"] * current_price
        pnl = current_value - pos["total_cost"]
        pnl_pct = (pnl / pos["total_cost"]) if pos["total_cost"] > 0 else 0

        should_exit = False
        reason = ""

        # Take profit
        if pnl_pct >= TAKE_PROFIT:
            should_exit = True
            reason = f"TAKE PROFIT +{pnl_pct*100:.1f}%"

        # Stop loss
        elif pnl_pct <= STOP_LOSS_PCT:
            should_exit = True
            reason = f"STOP LOSS {pnl_pct*100:.1f}%"

        # Market resolved
        elif current_price <= 0.01 or current_price >= 0.99:
            should_exit = True
            won = (current_price >= 0.99)
            reason = f"RESOLVED — {'WIN' if won else 'LOSS'}"

        # Daily stop loss
        if state["daily_pnl"] <= -MAX_DAILY_LOSS:
            if pnl < 0:
                should_exit = True
                reason = f"DAILY STOP LOSS (${state['daily_pnl']:.2f})"

        sign = "+" if pnl >= 0 else ""
        status = f"${current_price:.3f} ({sign}{pnl_pct*100:.1f}%)"

        if should_exit:
            # Execute exit
            proceeds = pos["shares"] * current_price
            portfolio = pt.load_portfolio()  # reload
            portfolio["balance"] += proceeds
            del portfolio["positions"][key]
            pt.save_portfolio(portfolio)

            trade = {
                "type": "SELL",
                "condition_id": pos["condition_id"],
                "question": pos["question"],
                "side": pos["side"],
                "price": current_price,
                "proceeds": proceeds,
                "shares": pos["shares"],
                "pnl": round(pnl, 2),
                "pnl_pct": round(pnl_pct * 100, 1),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            pt.save_trade(trade)

            state["total_trades"] += 1
            if pnl >= 0:
                state["wins"] += 1
            else:
                state["losses"] += 1
            state["total_pnl"] += pnl
            state["daily_pnl"] += pnl

            log_bot_action("AUTO_EXIT", {
                "question": pos["question"],
                "side": pos["side"],
                "pnl": round(pnl, 2),
                "reason": reason
            })

            print(f"  EXIT: {reason} | {sign}${pnl:.2f} | {pos['question'][:40]}")
            exits_done += 1
        else:
            print(f"  HOLD: {status} | {pos['question'][:45]}")

    if exits_done == 0:
        print(f"\n  Sin exits este scan. Todo en hold.")
    else:
        print(f"\n  {exits_done} posiciones cerradas.")

    state["last_scan"] = datetime.now(timezone.utc).isoformat()
    save_bot_state(state)

# ============================================================
# STATS
# ============================================================

def show_stats():
    state = load_bot_state()
    portfolio = pt.load_portfolio()
    trades = pt.load_trades()

    total = state["wins"] + state["losses"]
    win_rate = (state["wins"] / total * 100) if total > 0 else 0

    buys = [t for t in trades if t["type"] == "BUY"]
    sells = [t for t in trades if t["type"] == "SELL"]

    print(f"\n{'='*60}")
    print(f"  POLYMARKET PAPER TRADER — STATS")
    print(f"{'='*60}")
    print(f"  Trades cerrados: {total} (Wins: {state['wins']} | Losses: {state['losses']})")
    print(f"  Win rate: {win_rate:.1f}%")
    print(f"  P&L total: ${state['total_pnl']:.2f}")
    print(f"  P&L hoy: ${state['daily_pnl']:.2f}")
    print(f"  Balance: ${portfolio['balance']:.2f}")
    print(f"  Posiciones abiertas: {len(portfolio.get('positions', {}))}")
    print(f"  Total BUYs: {len(buys)} | Total SELLs: {len(sells)}")

    if sells:
        pnls = [t.get("pnl", 0) for t in sells]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]
        if wins:
            print(f"  Avg win: +${sum(wins)/len(wins):.2f}")
        if losses:
            print(f"  Avg loss: ${sum(losses)/len(losses):.2f}")

    print(f"{'='*60}")

# ============================================================
# MAIN
# ============================================================

def run_monitor():
    print(f"\n  Polymarket Risk Monitor")
    print(f"  TP: +{TAKE_PROFIT*100:.0f}% | SL: {STOP_LOSS_PCT*100:.0f}% | Daily SL: ${MAX_DAILY_LOSS}")
    print(f"  Scan interval: {SCAN_INTERVAL}s")
    print(f"  Press Ctrl+C to stop\n")

    try:
        while True:
            try:
                check_and_manage_exits()
            except Exception as e:
                print(f"\n  ERROR: {e}")
                log_bot_action("ERROR", {"message": str(e)})

            print(f"\n  Next check in {SCAN_INTERVAL}s...")
            time.sleep(SCAN_INTERVAL)
    except KeyboardInterrupt:
        print(f"\n\n  Monitor detenido.")
        show_stats()

if __name__ == "__main__":
    if "--stats" in sys.argv:
        show_stats()
    elif "--once" in sys.argv:
        check_and_manage_exits()
    else:
        run_monitor()

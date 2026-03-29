"""
Polymarket Paper Trading Bot
=============================
Sistema de paper trading para testear estrategias en Polymarket sin riesgo.

Estrategias:
1. Contrarian + Trend Following (comprar miedo en tendencia alcista)
2. Copy Trading (seguir wallets top)

Uso:
    python paper_trader.py markets          # Ver mercados activos
    python paper_trader.py markets crypto   # Filtrar por categoría
    python paper_trader.py buy <market_id> <amount>   # Paper buy YES
    python paper_trader.py sell <market_id> <amount>   # Paper sell (cerrar posición)
    python paper_trader.py portfolio        # Ver portfolio y P&L
    python paper_trader.py history          # Ver historial de trades
    python paper_trader.py watch            # Monitorear mercados en loop
"""

import json
import os
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ============================================================
# CUSTOM DNS RESOLVER (bypass local DNS issues)
# Pre-resolved IPs for Polymarket (ISP blocks DNS for these)
# ============================================================
_dns_cache = {
    "gamma-api.polymarket.com": "104.18.34.205",
    "clob.polymarket.com": "104.18.34.205",
}
_original_getaddrinfo = socket.getaddrinfo

def _custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    """Override DNS for Polymarket domains using hardcoded IPs."""
    if isinstance(host, str) and host in _dns_cache:
        ip = _dns_cache[host]
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (ip, port))]
    return _original_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = _custom_getaddrinfo

SESSION = requests.Session()

# ============================================================
# CONFIG
# ============================================================
GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"
DATA_DIR = Path(__file__).parent / "data"
PORTFOLIO_FILE = DATA_DIR / "portfolio.json"
TRADES_FILE = DATA_DIR / "trades.json"
INITIAL_BALANCE = 1000.0  # USDC simulados para arrancar

# ============================================================
# DATA PERSISTENCE
# ============================================================

def ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)

def load_json(filepath, default):
    if filepath.exists():
        with open(filepath, "r") as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    ensure_data_dir()
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)

def load_portfolio():
    default = {
        "balance": INITIAL_BALANCE,
        "positions": {},
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    return load_json(PORTFOLIO_FILE, default)

def save_portfolio(portfolio):
    save_json(PORTFOLIO_FILE, portfolio)

def load_trades():
    return load_json(TRADES_FILE, [])

def save_trade(trade):
    trades = load_trades()
    trades.append(trade)
    save_json(TRADES_FILE, trades)

# ============================================================
# POLYMARKET API
# ============================================================

def fetch_markets(category=None, limit=50):
    """Fetch active markets from Gamma API."""
    params = {
        "active": "true",
        "closed": "false",
        "archived": "false",
        "limit": limit,
        "order": "volume24hr",
        "ascending": "false"
    }

    try:
        resp = SESSION.get(f"{GAMMA_API}/markets", params=params, timeout=15)
        resp.raise_for_status()
        markets = resp.json()
    except Exception as e:
        print(f"Error fetching markets: {e}")
        return []

    if category:
        category = category.lower()
        filtered = []
        for m in markets:
            question = m.get("question", "").lower()
            group_slug = m.get("groupItemTitle", "").lower() if m.get("groupItemTitle") else ""
            tags = " ".join([t.get("label", "") for t in (m.get("tags") or [])]).lower()
            searchable = f"{question} {group_slug} {tags}"
            if category in searchable:
                filtered.append(m)
        markets = filtered

    return markets

def fetch_market_by_id(condition_id):
    """Fetch a specific market by conditionId (full or partial)."""
    short_id = condition_id[:10] if len(condition_id) > 10 else condition_id
    # Search in active markets list (most reliable)
    try:
        resp = SESSION.get(f"{GAMMA_API}/markets", params={
            "limit": 200, "active": "true", "closed": "false"
        }, timeout=15)
        resp.raise_for_status()
        for m in resp.json():
            cid = m.get("conditionId", "")
            if cid == condition_id or cid.startswith(short_id):
                return m
    except Exception:
        pass
    return None

def get_price(token_id):
    """Get current midpoint price from CLOB."""
    try:
        resp = SESSION.get(f"{CLOB_API}/midpoint", params={"token_id": token_id}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return float(data.get("mid", 0))
    except Exception:
        return None

def fetch_events(category=None, limit=50):
    """Fetch active events from Gamma API."""
    params = {
        "active": "true",
        "closed": "false",
        "limit": limit,
        "order": "volume24hr",
        "ascending": "false"
    }
    try:
        resp = SESSION.get(f"{GAMMA_API}/events", params=params, timeout=15)
        resp.raise_for_status()
        events = resp.json()
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []

    if category:
        category = category.lower()
        events = [e for e in events if
                  category in e.get("title", "").lower() or
                  any(category in t.get("label", "").lower() for t in (e.get("tags") or []))]

    return events

# ============================================================
# DISPLAY
# ============================================================

def display_markets(markets):
    """Show markets in a readable table."""
    if not markets:
        print("No se encontraron mercados.")
        return

    print(f"\n{'='*90}")
    print(f"{'ID':<12} {'YES':>6} {'NO':>6} {'Vol 24h':>12} {'Question'}")
    print(f"{'='*90}")

    for m in markets[:30]:
        condition_id = m.get("conditionId", "?")[:10]
        question = m.get("question", "?")[:50]

        prices = m.get("outcomePrices")
        if prices:
            if isinstance(prices, str):
                prices = json.loads(prices)
            yes_price = f"${float(prices[0]):.2f}" if len(prices) > 0 else "?"
            no_price = f"${float(prices[1]):.2f}" if len(prices) > 1 else "?"
        else:
            yes_price = "?"
            no_price = "?"

        vol24 = m.get("volume24hr", 0)
        if vol24:
            vol24 = f"${float(vol24):,.0f}"
        else:
            vol24 = "$0"

        print(f"{condition_id:<12} {yes_price:>6} {no_price:>6} {vol24:>12} {question}")

    print(f"\nTotal: {len(markets)} mercados encontrados (mostrando max 30)")

# ============================================================
# PAPER TRADING
# ============================================================

def paper_buy(condition_id, amount, side="YES"):
    """Simulate buying shares in a market."""
    portfolio = load_portfolio()
    amount = float(amount)

    if amount > portfolio["balance"]:
        print(f"Balance insuficiente. Tenés ${portfolio['balance']:.2f} USDC")
        return

    # Fetch market data
    market = fetch_market_by_id(condition_id)
    if not market:
        # Try searching by partial ID
        markets = fetch_markets(limit=100)
        market = next((m for m in markets if m.get("conditionId", "").startswith(condition_id)), None)
        if not market:
            print(f"Mercado no encontrado: {condition_id}")
            return

    prices = market.get("outcomePrices")
    if isinstance(prices, str):
        prices = json.loads(prices)

    side_idx = 0 if side.upper() == "YES" else 1
    price = float(prices[side_idx])

    if price <= 0 or price >= 1:
        print(f"Precio inválido: {price}")
        return

    shares = amount / price

    # Update portfolio
    portfolio["balance"] -= amount
    pos_key = f"{condition_id}_{side.upper()}"

    if pos_key not in portfolio["positions"]:
        portfolio["positions"][pos_key] = {
            "condition_id": market.get("conditionId"),
            "question": market.get("question", "?"),
            "side": side.upper(),
            "shares": 0,
            "avg_price": 0,
            "total_cost": 0
        }

    pos = portfolio["positions"][pos_key]
    total_cost = pos["total_cost"] + amount
    total_shares = pos["shares"] + shares
    pos["avg_price"] = total_cost / total_shares if total_shares > 0 else 0
    pos["shares"] = total_shares
    pos["total_cost"] = total_cost

    save_portfolio(portfolio)

    # Log trade
    trade = {
        "type": "BUY",
        "condition_id": market.get("conditionId"),
        "question": market.get("question", "?"),
        "side": side.upper(),
        "price": price,
        "amount": amount,
        "shares": shares,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    save_trade(trade)

    print(f"\n  PAPER BUY")
    print(f"  Mercado: {market.get('question', '?')[:60]}")
    print(f"  Side: {side.upper()} @ ${price:.3f}")
    print(f"  Invertido: ${amount:.2f} USDC")
    print(f"  Shares: {shares:.2f}")
    print(f"  Balance restante: ${portfolio['balance']:.2f} USDC")

def paper_sell(condition_id, side="YES"):
    """Close a paper position."""
    portfolio = load_portfolio()
    pos_key = f"{condition_id}_{side.upper()}"

    # Try partial match
    if pos_key not in portfolio["positions"]:
        matches = [k for k in portfolio["positions"] if k.startswith(condition_id)]
        if len(matches) == 1:
            pos_key = matches[0]
        elif len(matches) > 1:
            print(f"Múltiples posiciones matchean. Sé más específico:")
            for m in matches:
                print(f"  - {m}")
            return
        else:
            print(f"No tenés posición en {condition_id}")
            return

    pos = portfolio["positions"][pos_key]

    # Get current price
    market = fetch_market_by_id(pos["condition_id"])
    if not market:
        print("No se pudo obtener precio actual.")
        return

    prices = market.get("outcomePrices")
    if isinstance(prices, str):
        prices = json.loads(prices)

    side_idx = 0 if pos["side"] == "YES" else 1
    current_price = float(prices[side_idx])

    proceeds = pos["shares"] * current_price
    pnl = proceeds - pos["total_cost"]
    pnl_pct = (pnl / pos["total_cost"]) * 100 if pos["total_cost"] > 0 else 0

    portfolio["balance"] += proceeds
    del portfolio["positions"][pos_key]
    save_portfolio(portfolio)

    # Log trade
    trade = {
        "type": "SELL",
        "condition_id": pos["condition_id"],
        "question": pos["question"],
        "side": pos["side"],
        "price": current_price,
        "proceeds": proceeds,
        "shares": pos["shares"],
        "pnl": pnl,
        "pnl_pct": pnl_pct,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    save_trade(trade)

    emoji = "+" if pnl >= 0 else ""
    print(f"\n  PAPER SELL")
    print(f"  Mercado: {pos['question'][:60]}")
    print(f"  Side: {pos['side']} @ ${current_price:.3f}")
    print(f"  Proceeds: ${proceeds:.2f} USDC")
    print(f"  P&L: {emoji}${pnl:.2f} ({emoji}{pnl_pct:.1f}%)")
    print(f"  Balance: ${portfolio['balance']:.2f} USDC")

def show_portfolio():
    """Show current paper portfolio with live P&L."""
    portfolio = load_portfolio()

    print(f"\n{'='*80}")
    print(f"  PAPER TRADING PORTFOLIO")
    print(f"{'='*80}")
    print(f"  Balance disponible: ${portfolio['balance']:.2f} USDC")

    if not portfolio["positions"]:
        print(f"  Sin posiciones abiertas.")
        total_value = portfolio["balance"]
    else:
        print(f"\n  {'Mercado':<40} {'Side':<5} {'Entry':>7} {'Now':>7} {'P&L':>10} {'P&L%':>7}")
        print(f"  {'-'*76}")

        total_unrealized = 0
        total_invested = 0

        for key, pos in portfolio["positions"].items():
            market = fetch_market_by_id(pos["condition_id"])
            if market:
                prices = market.get("outcomePrices")
                if isinstance(prices, str):
                    prices = json.loads(prices)
                side_idx = 0 if pos["side"] == "YES" else 1
                current_price = float(prices[side_idx])
            else:
                current_price = pos["avg_price"]

            current_value = pos["shares"] * current_price
            pnl = current_value - pos["total_cost"]
            pnl_pct = (pnl / pos["total_cost"]) * 100 if pos["total_cost"] > 0 else 0

            total_unrealized += pnl
            total_invested += pos["total_cost"]

            sign = "+" if pnl >= 0 else ""
            question = pos["question"][:38]
            print(f"  {question:<40} {pos['side']:<5} ${pos['avg_price']:>.3f} ${current_price:>.3f} {sign}${pnl:>7.2f} {sign}{pnl_pct:>5.1f}%")

        total_value = portfolio["balance"] + total_invested + total_unrealized
        sign = "+" if total_unrealized >= 0 else ""
        print(f"\n  Invertido: ${total_invested:.2f}")
        print(f"  P&L no realizado: {sign}${total_unrealized:.2f}")

    print(f"  Valor total: ${total_value:.2f} USDC")
    print(f"  Inicio: ${INITIAL_BALANCE:.2f} USDC")
    total_pnl = total_value - INITIAL_BALANCE
    sign = "+" if total_pnl >= 0 else ""
    print(f"  Retorno total: {sign}${total_pnl:.2f} ({sign}{(total_pnl/INITIAL_BALANCE)*100:.1f}%)")
    print(f"{'='*80}")

def show_history():
    """Show trade history."""
    trades = load_trades()
    if not trades:
        print("Sin trades registrados.")
        return

    print(f"\n{'='*90}")
    print(f"  HISTORIAL DE TRADES")
    print(f"{'='*90}")

    for t in trades:
        ts = t["timestamp"][:19].replace("T", " ")
        if t["type"] == "BUY":
            print(f"  [{ts}] BUY  {t['side']} @ ${t['price']:.3f} | ${t['amount']:.2f} | {t['question'][:45]}")
        else:
            sign = "+" if t.get("pnl", 0) >= 0 else ""
            print(f"  [{ts}] SELL {t['side']} @ ${t['price']:.3f} | {sign}${t.get('pnl',0):.2f} ({sign}{t.get('pnl_pct',0):.1f}%) | {t['question'][:35]}")

    print(f"\n  Total trades: {len(trades)}")

def watch_markets(category=None, interval=60):
    """Monitor markets in a loop."""
    print(f"Monitoreando mercados cada {interval}s... (Ctrl+C para parar)")
    try:
        while True:
            markets = fetch_markets(category=category, limit=20)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"  [LIVE] {datetime.now().strftime('%H:%M:%S')} | Categoría: {category or 'ALL'}")
            display_markets(markets)

            portfolio = load_portfolio()
            if portfolio["positions"]:
                print(f"\n  Posiciones abiertas: {len(portfolio['positions'])} | Balance: ${portfolio['balance']:.2f}")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoreo detenido.")

# ============================================================
# CLI
# ============================================================

def print_usage():
    print("""
  Polymarket Paper Trader
  =======================

  Comandos:
    python paper_trader.py markets [categoria]     Ver mercados (crypto, politics, sports...)
    python paper_trader.py events [categoria]      Ver eventos agrupados
    python paper_trader.py buy <id> <monto> [YES/NO]   Comprar (paper)
    python paper_trader.py sell <id> [YES/NO]      Vender posición (paper)
    python paper_trader.py portfolio               Ver portfolio y P&L
    python paper_trader.py history                 Historial de trades
    python paper_trader.py watch [categoria]       Monitor en tiempo real
    python paper_trader.py reset                   Resetear portfolio a $1000
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    cmd = sys.argv[1].lower()

    if cmd == "markets":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        markets = fetch_markets(category=category)
        display_markets(markets)

    elif cmd == "events":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        events = fetch_events(category=category)
        print(f"\n{'='*80}")
        for e in events[:20]:
            title = e.get("title", "?")[:60]
            vol = f"${float(e.get('volume', 0)):,.0f}" if e.get('volume') else "$0"
            n_markets = len(e.get("markets", []))
            print(f"  {title:<60} Vol: {vol:>12} ({n_markets} markets)")
        print(f"{'='*80}")

    elif cmd == "buy":
        if len(sys.argv) < 4:
            print("Uso: python paper_trader.py buy <condition_id> <monto> [YES/NO]")
            return
        cid = sys.argv[2]
        amount = sys.argv[3]
        side = sys.argv[4] if len(sys.argv) > 4 else "YES"
        paper_buy(cid, amount, side)

    elif cmd == "sell":
        if len(sys.argv) < 3:
            print("Uso: python paper_trader.py sell <condition_id> [YES/NO]")
            return
        cid = sys.argv[2]
        side = sys.argv[3] if len(sys.argv) > 3 else "YES"
        paper_sell(cid, side)

    elif cmd == "portfolio":
        show_portfolio()

    elif cmd == "history":
        show_history()

    elif cmd == "watch":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        watch_markets(category=category)

    elif cmd == "reset":
        confirm = input("Resetear portfolio a $1000? (s/n): ")
        if confirm.lower() == "s":
            save_portfolio({
                "balance": INITIAL_BALANCE,
                "positions": {},
                "created_at": datetime.now(timezone.utc).isoformat()
            })
            save_json(TRADES_FILE, [])
            print("Portfolio reseteado.")

    else:
        print_usage()

if __name__ == "__main__":
    main()

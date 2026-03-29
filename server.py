"""
Polymarket Paper Trading — Web Server API
Sirve data del paper trader al frontend.
"""

import json
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Reutilizar funciones del paper trader
import paper_trader as pt

app = Flask(__name__, static_folder="frontend")
CORS(app)

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/api/portfolio")
def api_portfolio():
    portfolio = pt.load_portfolio()
    positions = []
    total_invested = 0
    total_unrealized = 0

    for key, pos in portfolio.get("positions", {}).items():
        market = pt.fetch_market_by_id(pos["condition_id"])
        current_price = pos["avg_price"]  # fallback
        if market:
            prices = market.get("outcomePrices")
            if isinstance(prices, str):
                prices = json.loads(prices)
            side_idx = 0 if pos["side"] == "YES" else 1
            if prices and len(prices) > side_idx:
                current_price = float(prices[side_idx])

        current_value = pos["shares"] * current_price
        pnl = current_value - pos["total_cost"]
        pnl_pct = (pnl / pos["total_cost"]) * 100 if pos["total_cost"] > 0 else 0

        total_invested += pos["total_cost"]
        total_unrealized += pnl

        positions.append({
            "key": key,
            "question": pos["question"],
            "side": pos["side"],
            "shares": round(pos["shares"], 2),
            "avg_price": round(pos["avg_price"], 4),
            "current_price": round(current_price, 4),
            "cost": round(pos["total_cost"], 2),
            "value": round(current_value, 2),
            "pnl": round(pnl, 2),
            "pnl_pct": round(pnl_pct, 1),
        })

    total_value = portfolio["balance"] + total_invested + total_unrealized
    total_pnl = total_value - pt.INITIAL_BALANCE

    return jsonify({
        "balance": round(portfolio["balance"], 2),
        "positions": positions,
        "total_invested": round(total_invested, 2),
        "total_unrealized": round(total_unrealized, 2),
        "total_value": round(total_value, 2),
        "total_pnl": round(total_pnl, 2),
        "total_pnl_pct": round((total_pnl / pt.INITIAL_BALANCE) * 100, 1),
        "initial_balance": pt.INITIAL_BALANCE,
    })

@app.route("/api/trades")
def api_trades():
    trades = pt.load_trades()
    return jsonify(trades[::-1])  # newest first

@app.route("/api/markets")
def api_markets():
    category = request.args.get("category", None)
    limit = int(request.args.get("limit", 30))
    markets = pt.fetch_markets(category=category, limit=limit)
    result = []
    for m in markets[:30]:
        prices = m.get("outcomePrices")
        if isinstance(prices, str):
            prices = json.loads(prices)
        yes_price = float(prices[0]) if prices and len(prices) > 0 else 0
        no_price = float(prices[1]) if prices and len(prices) > 1 else 0
        result.append({
            "id": m.get("conditionId", "")[:10],
            "condition_id": m.get("conditionId", ""),
            "question": m.get("question", "?"),
            "yes_price": round(yes_price, 3),
            "no_price": round(no_price, 3),
            "volume24hr": float(m.get("volume24hr", 0) or 0),
            "volume": float(m.get("volume", 0) or 0),
            "liquidity": float(m.get("liquidity", 0) or 0),
        })
    return jsonify(result)

@app.route("/api/buy", methods=["POST"])
def api_buy():
    data = request.json
    cid = data.get("condition_id", "")
    amount = float(data.get("amount", 0))
    side = data.get("side", "YES")

    if amount <= 0:
        return jsonify({"error": "Monto debe ser > 0"}), 400

    portfolio = pt.load_portfolio()
    if amount > portfolio["balance"]:
        return jsonify({"error": f"Balance insuficiente: ${portfolio['balance']:.2f}"}), 400

    market = pt.fetch_market_by_id(cid)
    if not market:
        markets = pt.fetch_markets(limit=100)
        market = next((m for m in markets if m.get("conditionId", "").startswith(cid)), None)
    if not market:
        return jsonify({"error": "Mercado no encontrado"}), 404

    prices = market.get("outcomePrices")
    if isinstance(prices, str):
        prices = json.loads(prices)

    side_idx = 0 if side.upper() == "YES" else 1
    price = float(prices[side_idx])

    if price <= 0 or price >= 1:
        return jsonify({"error": f"Precio inválido: {price}"}), 400

    shares = amount / price
    portfolio["balance"] -= amount
    pos_key = f"{cid[:10]}_{side.upper()}"

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
    pt.save_portfolio(portfolio)

    trade = {
        "type": "BUY",
        "condition_id": market.get("conditionId"),
        "question": market.get("question", "?"),
        "side": side.upper(),
        "price": price,
        "amount": amount,
        "shares": shares,
        "timestamp": pt.datetime.now(pt.timezone.utc).isoformat()
    }
    pt.save_trade(trade)

    return jsonify({"ok": True, "trade": trade})

@app.route("/api/sell", methods=["POST"])
def api_sell():
    data = request.json
    pos_key = data.get("key", "")

    portfolio = pt.load_portfolio()
    if pos_key not in portfolio["positions"]:
        return jsonify({"error": "Posición no encontrada"}), 404

    pos = portfolio["positions"][pos_key]
    market = pt.fetch_market_by_id(pos["condition_id"])
    current_price = pos["avg_price"]
    if market:
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
        "pnl_pct": round(pnl_pct, 1),
        "timestamp": pt.datetime.now(pt.timezone.utc).isoformat()
    }
    pt.save_trade(trade)

    return jsonify({"ok": True, "trade": trade})

@app.route("/api/bot-stats")
def api_bot_stats():
    bot_state_file = Path(__file__).parent / "data" / "bot_state.json"
    bot_log_file = Path(__file__).parent / "data" / "bot_log.json"

    state = pt.load_json(bot_state_file, {
        "total_trades": 0, "wins": 0, "losses": 0,
        "total_pnl": 0, "daily_trades": 0, "daily_pnl": 0,
        "daily_date": "", "last_scan": None,
        "signals_generated": 0, "trades_executed": 0
    })

    total = state["wins"] + state["losses"]
    win_rate = (state["wins"] / total * 100) if total > 0 else 0

    logs = pt.load_json(bot_log_file, [])
    recent_logs = logs[-20:][::-1]

    return jsonify({
        **state,
        "win_rate": round(win_rate, 1),
        "total_closed": total,
        "recent_logs": recent_logs,
    })

if __name__ == "__main__":
    print("\n  Polymarket Paper Trader — Dashboard")
    print("  http://localhost:5555\n")
    app.run(host="0.0.0.0", port=5555, debug=False)

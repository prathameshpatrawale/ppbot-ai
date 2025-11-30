import json
import os
import time

class PnLTracker:
    def __init__(self, filename="pnl_log.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({"trades": [], "pnl": 0}, f)

    def log_trade(self, market_id, outcome, amount, result):
        with open(self.filename, "r") as f:
            data = json.load(f)

        trade = {
            "time": time.time(),
            "market": market_id,
            "outcome": outcome,
            "amount": amount,
            "result": result,
        }

        data["trades"].append(trade)

        # Update P&L if API returns profit field
        profit = result.get("profit", 0)
        data["pnl"] += profit

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)

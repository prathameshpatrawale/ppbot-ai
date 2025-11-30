import json
import matplotlib.pyplot as plt
import os
import datetime

def plot_pnl(log_file="pnl_log.json", output="pnl_plot.png"):
    if not os.path.exists(log_file):
        print("No PnL log file found:", log_file)
        return

    with open(log_file, "r") as f:
        data = json.load(f)

    trades = data.get("trades", [])

    if not trades:
        print("No trades found in log.")
        return

    times = []
    pnl_values = []

    cumulative_pnl = 0

    for trade in trades:
        t = datetime.datetime.fromtimestamp(trade["time"])
        times.append(t)

        profit = trade["result"].get("profit", 0)
        cumulative_pnl += profit
        pnl_values.append(cumulative_pnl)

    plt.figure(figsize=(10, 5))
    plt.plot(times, pnl_values, marker='o')
    plt.title("PPBot P&L Over Time")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Profit (Mana)")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output)
    print(f"Saved PnL graph → {output}")

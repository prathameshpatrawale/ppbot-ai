# scripts/backtest.py
import json
import argparse
import random
# Use the HybridStrategy for consistency with the bot
from ppbot.strategy import HybridStrategy 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="market history JSON")
    args = parser.parse_args()

    with open(args.data, "r") as f:
        data = json.load(f)

    # Use HybridStrategy for backtesting
    strategy = HybridStrategy() 
    balance = 1000.0 # Start balance
    pnl = 0.0

    print("--- Starting Backtest ---")
    
    for m in data:
        decision = strategy.decide(m)
        if decision["action"] == "buy":
            amount = decision["amount"]
            
            # Simple P&L Simulation for Backtesting (50% win rate)
            if random.random() < 0.5:
                # Simulate a win (profit = amount * 1x return)
                profit = amount 
            else:
                # Simulate a loss
                profit = -amount

            # Update balance and cumulative P&L
            balance += profit 
            pnl += profit
            
    print("--- Backtest Finished ---")
    print("Final Cumulative P&L:", round(pnl, 2))
    print("Final Balance:", round(balance, 2))


if __name__ == "__main__":
    main()
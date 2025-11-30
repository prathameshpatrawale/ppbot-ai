# scripts/backtest.py
import json
import argparse
from ppbot.strategy import SimpleStrategy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="market history JSON")
    args = parser.parse_args()

    with open(args.data, "r") as f:
        data = json.load(f)

    strategy = SimpleStrategy()
    balance = 1000

    for m in data:
        decision = strategy.decide(m)
        if decision["action"] == "buy":
            balance -= decision["amount"]
        # (No simulation of P&L here yet)

    print("Balance after backtest:", balance)


if __name__ == "__main__":
    main()

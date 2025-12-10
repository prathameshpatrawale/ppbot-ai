# run.py - entrypoint for PPbot
import os
import sys
import argparse
from ppbot.bot import PPBot
from dotenv import load_dotenv
# Correct import path for PnLTracker, assuming pnl.py is now inside ppbot/
from ppbot.pnl import PnLTracker 

load_dotenv()

def detect_api_key():
    # Check multiple env var names for convenience
    return os.environ.get("MIKHAILTHAL_API_KEY") or os.environ.get("API_KEY")

def main():
    parser = argparse.ArgumentParser(description="PPbot runner")
    parser.add_argument("--mode", choices=["auto","simulation","real"], default="auto", help="auto/simulation/real")
    parser.add_argument("--dry", action="store_true", help="dry run (no side-effects)")
    args = parser.parse_args()

    api_key = detect_api_key()
    mode = args.mode
    if mode == "auto":
        mode = "real" if api_key else "simulation"

    print(f"Selected mode: {mode}")
    
    # 1. Instantiate the PnLTracker here
    pnl_tracker = PnLTracker() 
    
    # 2. Pass the PnLTracker instance to the PPBot constructor
    bot = PPBot(mode=mode, api_key=api_key, dry=args.dry, pnl_tracker=pnl_tracker)
    bot.run()

if __name__ == '__main__':
    main()
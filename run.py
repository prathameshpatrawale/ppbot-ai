# run.py - entrypoint for PPbot
import os
import sys
import argparse
from ppbot.bot import PPBot
from dotenv import load_dotenv

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
    bot = PPBot(mode=mode, api_key=api_key, dry=args.dry)
    bot.run()

if __name__ == '__main__':
    main()

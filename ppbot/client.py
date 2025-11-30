import requests
import logging
import random

log = logging.getLogger(__name__)

API_BASE = "https://api.manifold.markets/v0"

class ManifoldClient:
    def __init__(self, api_key=None, dry=False):
        self.api_key = api_key
        self.dry = dry

        if self.api_key:
            self.headers = {"Authorization": f"Key {self.api_key}"}
            log.info("Real ManifoldClient initialized.")
        else:
            self.headers = {}
            log.info("Simulation (no API key).")

    
    # FETCH MARKETS by "MikhailTal"
    def fetch_mikhail_markets(self):
        """Fetch ONLY markets created by MikhailTal (contest requirement)."""
        try:
            url = f"{API_BASE}/markets?creator=MikhailTal&limit=50"
            res = requests.get(url)
            res.raise_for_status()
            markets = res.json()

            # Filter out resolved (closed) markets
            markets = [m for m in markets if m.get("isResolved") is False]

            log.info(f"Fetched {len(markets)} markets from MikhailTal")
            return markets

        except Exception as e:
            log.error("Failed to fetch markets: %s", e)
            return []

    
    # PLACE REAL BET
    def place_bet(self, market_id, outcome, amount):
        """Places a REAL bet if API key, else simulates."""
        if self.dry:
            log.info("[DRY RUN] Skipping real API bet.")
            return {
                "status": "dry",
                "market": market_id,
                "outcome": outcome,
                "amount": amount
            }

        if not self.api_key:
            log.info("[SIM] Fake bet (no API key).")
            return {
                "status": "simulated",
                "market": market_id,
                "outcome": outcome,
                "amount": amount
            }

        try:
            url = f"{API_BASE}/bet"
            payload = {
                "contractId": market_id,
                "outcome": outcome,
                "amount": amount
            }

            r = requests.post(url, json=payload, headers=self.headers)
            r.raise_for_status()
            return r.json()

        except Exception as e:
            log.error("Bet failed: %s", e)
            return {"error": str(e)}

    
    # GET USER BALANCE
    def get_balance(self):
        if not self.api_key:
            return {"balance": 1000, "simulated": True}

        try:
            url = f"{API_BASE}/me"
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
            return r.json()

        except Exception as e:
            log.error("Failed to fetch user balance: %s", e)
            return {"error": str(e)}

    # GET POSITIONS (open positions)
    def get_positions(self):
        if not self.api_key:
            return []

        try:
            url = f"{API_BASE}/bets"
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
            return r.json()

        except Exception as e:
            log.error("Failed to fetch positions: %s", e)
            return {"error": str(e)}

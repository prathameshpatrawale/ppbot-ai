# ppbot/simulation.py
import random
import logging

log = logging.getLogger("ppbot.sim")

class SimulationClient:
    """
    A fake market simulator for testing the bot logic
    without using real Manifold API calls.
    """

    def __init__(self, pnl_tracker): 
        self._tick = 0
        self.pnl_tracker = pnl_tracker
        self.market_data = {}

    
    def fetch_mikhail_markets(self, limit=50):
        """Returns a list of 3 fake markets with full data."""
        markets = []
        for i in range(3):
            self._tick += 1
            prob = random.uniform(0.1, 0.9)
            
            markets.append({
                "id": f"sim-{self._tick}",
                "question": f"Simulated market #{self._tick}",
                "probability": prob,
                "creatorUsername": "MikhailTal",
                # Added trend and volume data for strategy.py to work
                "trend": random.uniform(-0.2, 0.2), 
                "volume24Hours": random.uniform(50, 500) 
            })
            self.market_data[f"sim-{self._tick}"] = markets[-1]
            
        log.info("Simulation: generated %d fake markets", len(markets))
        return markets

    
    def place_bet(self, market_id, outcome, amount):
        log.info("[SIM] Placed fake bet %s mana on %s in %s",
                      amount, outcome, market_id)

        # SIMULATE THE PROFIT/LOSS (50% chance of success or failure)
        if random.random() < 0.5:
            # Simulate a win (profit = amount * payout multiplier)
            simulated_profit = amount * random.uniform(0.5, 1.5) 
        else:
            # Simulate a loss (profit = negative amount bet)
            simulated_profit = -amount 

        result = {
            "status": "ok",
            "simulated": True,
            "market": market_id,
            "outcome": outcome,
            "amount": amount,
            # CRITICAL FIX: Include the 'profit' key
            "profit": simulated_profit 
        }

        # REMOVED: Redundant internal call to self.pnl_tracker.log_trade(). 
        # Logging is now handled externally by the PPBot class.

        return result
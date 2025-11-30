# ppbot/simulation.py
import random
import logging

log = logging.getLogger("ppbot.sim")

class SimulationClient:
    """
    A fake market simulator for testing the bot logic
    without using real Manifold API calls.
    """

    def __init__(self):
        self._tick = 0

    
    # Fake version of fetch_mikhail_markets
    def fetch_mikhail_markets(self, limit=50):
        """
        Returns a list of 3 fake markets with random probabilities.
        This keeps the bot loop running during simulation mode.
        """

        markets = []

        for i in range(3):
            self._tick += 1
            prob = random.uniform(0.1, 0.9)

            markets.append({
                "id": f"sim-{self._tick}",
                "question": f"Simulated market #{self._tick}",
                "probability": prob,
                "creatorUsername": "MikhailTal"  # so strategy is happy
            })

        log.info("Simulation: generated %d fake markets", len(markets))
        return markets

    
    # Fake bet
    def place_bet(self, market_id, outcome, amount):
        log.info("[SIM] Placed fake bet %s mana on %s in %s",
                 amount, outcome, market_id)

        return {
            "status": "ok",
            "simulated": True,
            "market": market_id,
            "outcome": outcome,
            "amount": amount,
        }

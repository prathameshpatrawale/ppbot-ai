import logging
import random

log = logging.getLogger(__name__)

class HybridStrategy:
    """
    Combines:
    - Mean reversion (bet against extreme prices)
    - Momentum (bet with strong trend)
    - Minimum liquidity filter
    """
    def decide(self, market):
        prob = market.get("probability", 0.5)
        trend = market.get("trend", 0)
        volume = market.get("volume24Hours", 0)

        # Skip low liquidity markets
        if volume < 50:
            if random.random() < 0.3:
                return {"action": "buy", "outcome": "YES", "amount": 5}

            return {"action": "hold"}

        # Mean reversion edge
        if prob > 0.85:
            return {"action": "buy", "outcome": "NO", "amount": 5}
        if prob < 0.15:
            return {"action": "buy", "outcome": "YES", "amount": 5}

        # Momentum edge
        if trend > 0.1:
            return {"action": "buy", "outcome": "YES", "amount": 5}

        if trend < -0.1:
            return {"action": "buy", "outcome": "NO", "amount": 5}

        if random.random() < 0.3:
            return {"action": "buy", "outcome": "YES", "amount": 5}

        return {"action": "hold"}


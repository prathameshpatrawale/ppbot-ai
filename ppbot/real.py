# ppbot/real.py
import logging
logger = logging.getLogger("ppbot.real")

class RealClient:
    def __init__(self, api_key=None, dry=False):
        if not api_key:
            raise ValueError("API key required for real mode")
        self.api_key = api_key
        self.dry = dry
        logger.info("RealClient initialized (dry=%s)", dry)
        # TODO: initialize real API clients here (Manifold / exchange)

    def fetch_market_snapshot(self):
        # TODO: implement real market snapshot fetch using the API
        logger.info("Fetching real market snapshot (stubbed)")
        # Return a simple stub so the rest of the bot can run in dry mode
        return {"price": 42.0, "timestamp": None}

    def place_order(self, order):
        # In dry mode we don't send real orders
        if self.dry:
            logger.info("Dry run: would place order: %s", order)
            return {"status": "dry", "order_id": None}
        # TODO: place order via real API
        logger.info("Placing real order (stubbed): %s", order)
        return {"status": "ok", "order_id": "real-12345"}
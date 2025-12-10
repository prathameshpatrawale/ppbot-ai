# ppbot/bot.py
import time
import logging

from .client import ManifoldClient
from .simulation import SimulationClient
from .strategy import HybridStrategy


log = logging.getLogger("ppbot.bot")
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s"
)

class PPBot:
    """
    PPBot orchestrates:
    - Real client or simulation client (auto based on API key)
    - Fetching markets created ONLY by user 'MikhailTal'
    - Applying strategy
    - Placing trades (dry / real)
    """

    # FIX 1: Add pnl_tracker to the constructor signature to resolve TypeError
    def __init__(self, mode="simulation", api_key=None, dry=False, sleep=5, pnl_tracker=None):
        self.mode = mode
        self.api_key = api_key
        self.dry = dry
        self.sleep = sleep
        
        # FIX 2: Store the pnl_tracker instance passed from run.py
        self.pnl = pnl_tracker 

        # ---- Select client ----
        if self.mode == "real":
            log.info("Initializing REAL mode client")
            # ManifoldClient can be updated to accept the tracker later if needed
            self.client = ManifoldClient(api_key=api_key, dry=dry)
        else:
            log.info("Initializing SIMULATION mode client")
            # FIX 3: Pass the tracker instance to the SimulationClient
            self.client = SimulationClient(pnl_tracker=self.pnl)

        # ---- Strategy ----
        self.strategy = HybridStrategy()

    # Main loop
    def run(self):
        log.info("Starting PPBot — Mode: %s | Dry: %s", self.mode, self.dry)

        max_loops = 20  # run only 20 cycles

        for loop in range(max_loops):
            log.info("---- Loop %d / %d ----", loop + 1, max_loops)

            try:
                # 1) Fetch markets created by "MikhailTal"
                markets = self.client.fetch_mikhail_markets()
                if not markets:
                    log.info("No markets found for user 'MikhailTal'")
                    time.sleep(self.sleep)
                    continue

                # 2) Evaluate markets
                for market in markets:
                    market_id = market["id"]
                    question = market.get("question", "")

                    log.info("Evaluating market: %s | %s", market_id, question)

                    # 3) Strategy decision
                    decision = self.strategy.decide(market)
                    log.info("Decision: %s", decision)

                    # 4) Execute decision
                    if decision["action"] == "buy":
                        outcome = decision["outcome"]
                        amount = decision["amount"]

                        log.info("Placing bet: %s mana on %s", amount, outcome)
                        result = self.client.place_bet(
                            market_id=market_id,
                            outcome=outcome,
                            amount=amount
                        )
                        log.info("Bet result: %s", result)

                        # Log PnL trade (This is the central call, using the 'profit' 
                        # key returned by the SimulationClient)
                        self.pnl.log_trade(market_id, outcome, amount, result)

                    else:
                        log.info("Holding (no trade)")


                # 5) Sleep between cycles
                time.sleep(self.sleep)

            except KeyboardInterrupt:
                log.info("Bot stopped by user.")
                break

            except Exception as e:
                log.error("Error during loop: %s", e)
                time.sleep(3)

        log.info("Finished %d loops. Exiting bot.", max_loops)
# PPbotAI — Manifold Prediction Market Trading Bot
***Contest Submission for Manifold Featured Challenge***

**Bot Username:** PPbotAI

PPbotAI is an automated trading bot designed specifically for the Manifold Markets Featured Contest.  
It trades only in markets created by the user "MikhailTal" as required by contest rules.  
The bot supports real API trading, simulation mode, a custom hybrid strategy, and PnL logging.

<img width="3564" height="1768" alt="stylish_pnl_plot" src="https://github.com/user-attachments/assets/8fd31c12-a7ad-4a8d-8506-d6d5d652660a" />

------------------------------------------------------------
## Project Features
------------------------------------------------------------

1. Market Filtering  
   - Trades strictly in markets created by "MikhailTal".  
   - Fetches markets through the Manifold public API.

2. Real and Simulation Mode  
   - If MANIFOLD_API_KEY is present in the .env file, the bot runs in real mode.  
   - If no API key is provided, the bot switches automatically to simulation mode.

3. Hybrid Trading Strategy  
   - Combines mean reversion, momentum, and liquidity filtering.  
   - Mean reversion: Buy against extreme probabilities.  
   - Momentum: Buy in direction of trend.  
   - Liquidity filter: Ignores low-volume markets.

4. PnL Logging  
   - All buy trades are logged to pnl_log.json.  
   - Provides a record of timestamp, market, outcome, amount, and result.

5. PnL Graph Generation  
   - plot_pnl.py generates a cumulative profit graph from pnl_log.json.  
   - Output is saved as pnl_plot.png.

6. Clean and Modular Architecture  
   - Separate modules for strategy, client, simulation, and PnL tracking.  
   - Well-organized codebase suitable for contest evaluation.

------------------------------------------------------------
## Project Structure
------------------------------------------------------------

PPbotAI  
│  
├── README.md  
├── requirements.txt  
├── LICENSE  
├── run.py  
├── .env.example  
│  
├── ppbot  
│   ├── __init__.py  
│   ├── bot.py  
│   ├── client.py  
│   ├── strategy.py  
│   ├── simulation.py  
│   ├── pnl.py  
│   └── plot_pnl.py  
│  
├── pnl_log.json (generated automatically)  
└── plot_pnl.py (top-level runner)

------------------------------------------------------------
## Installation
------------------------------------------------------------

1. Install dependencies:

pip install -r requirements.txt

2. Create a .env file based on .env.example:

MANIFOLD_API_KEY=your_api_key_here

Leave empty to run in simulation mode.

------------------------------------------------------------
## Usage
------------------------------------------------------------

**Run in simulation mode:**

```bash
python run.py --dry
```
**Run in real mode:**
```bash
python run.py
```

***Limit loops for testing:***
```bash
python run.py --dry --loops 20
```

***Generate PnL graph:***

```bash
python plot_pnl.py
```

------------------------------------------------------------
## Strategy Summary
------------------------------------------------------------

1. Mean Reversion  
   - If probability > 0.85: buy NO  
   - If probability < 0.15: buy YES  

2. Momentum  
   - If trend > 0.1: buy YES  
   - If trend < -0.1: buy NO  

3. Liquidity Filter  
   - Skip markets with volume24Hours < 50.

------------------------------------------------------------
## Technical Overview
------------------------------------------------------------

bot.py  
- Main trading loop, strategy application, trade execution, and PnL logging.

client.py  
- Manifold API wrapper for real trading.

simulation.py  
- Fake market generator for testing without an API key.

strategy.py  
- Hybrid trading strategy implementation.

pnl.py  
- Handles trade logging and PnL calculation.

plot_pnl.py  
- Generates cumulative PnL graph.

run.py  
- Command-line entry point and mode switching logic.

------------------------------------------------------------
## Bot Identity
------------------------------------------------------------

***Bot Username: PPbotAI***

------------------------------------------------------------
## License
------------------------------------------------------------

This project is licensed under the MIT License.

import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

# --- Configuration ---
# Set the plot style (try 'seaborn-v0_8', 'dark_background', or 'bmh' for alternatives)
plt.style.use('ggplot')

# Define file paths
LOG_FILE_PATH = 'pnl_log.json'
OUTPUT_FOLDER = 'plots'
OUTPUT_FILENAME = 'stylish_pnl_plot.png'

def plot_pnl():
    """
    Loads trade data from pnl_log.json, calculates cumulative P&L,
    and generates a stylized plot saved to the 'plots' folder.
    """
    if not os.path.exists(LOG_FILE_PATH):
        print(f"Error: P&L log file not found at {LOG_FILE_PATH}")
        print("Please run the bot (python run.py --dry) first to generate trade data.")
        return

    # 1. Load Data
    try:
        with open(LOG_FILE_PATH, 'r') as f:
            data = json.load(f)
        
        trades = data.get('trades', [])
        if not trades:
            print("No trades found in the log file. Plotting skipped.")
            return

    except json.JSONDecodeError:
        print(f"Error decoding JSON from {LOG_FILE_PATH}. File might be corrupted.")
        return
    
    # 2. Extract and Process Data
    times = []
    profits = []
    for trade in trades:
        # Convert UNIX timestamp to a readable datetime object
        times.append(datetime.fromtimestamp(trade['time']))
        # Extract the profit/loss from the trade result
        profits.append(trade['result']['profit'])

    # Calculate cumulative P&L
    cumulative_pnl = [sum(profits[:i+1]) for i in range(len(profits))]

    # 3. Create the Plot
    
    # Initialize a clean figure
    plt.figure(figsize=(12, 6))

    # Plot with enhanced styling
    plt.plot(
        times, 
        cumulative_pnl, 
        color='#3498db',         # A clean blue color
        linewidth=2.5,            # Medium-thick line
        linestyle='-',            # Solid line (you can use '--' for dashed)
        marker='o',               # Circular markers
        markersize=6,             # Marker size
        markeredgecolor='black',  # Black outline for markers
        markerfacecolor='#2ecc71', # Green fill for markers
        label='Cumulative P&L'
    )
    
    # Add labels and title
    plt.title(
        f'PPBot P&L Over Time (Total P&L: {cumulative_pnl[-1]:.2f} Mana)', 
        fontsize=16, 
        fontweight='bold', 
        pad=20
    )
    plt.xlabel('Time of Trade', fontsize=12)
    plt.ylabel('Cumulative Profit (Mana)', fontsize=12)
    
    # Improve readability
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() # Adjusts plot to prevent labels from being cut off

    # 4. Save the Plot
    
    # Ensure the output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
    
    # Save with high resolution (dpi=300) and tight bounding box
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    print(f"\n Plot successfully saved to: {output_path}")

# Main execution block
if __name__ == '__main__':
    plot_pnl()
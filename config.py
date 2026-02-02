import os

# --- SEARCH SETTINGS ---
SEARCH_QUERY = "Ferreteria in Mexico City"

# --- SCROLLING SETTINGS ---
# Time to wait (in seconds) for new results to load after scrolling
SCROLL_PAUSE_TIME = 2.0
# Randomness factor (e.g., wait between 2.0 and 4.0 seconds)
SCROLL_RANDOMNESS = 2.0

# --- LIMITS ---
# Stop scrolling after finding this many businesses (prevents getting stuck forever)
MAX_RESULTS = 100

# --- OUTPUT SETTINGS ---
OUTPUT_FOLDER = "output"
# Dynamic filename based on search query (e.g., "leads_Ferreteria_in_Mexico_City.csv")
filename_safe = SEARCH_QUERY.replace(" ", "_").replace(",", "").lower()
OUTPUT_FILE = f"leads_{filename_safe}.csv"

# --- SYSTEM PATHS ---
# Automatically create the full path for the output file
OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
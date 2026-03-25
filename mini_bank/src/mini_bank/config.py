import logging
from pathlib import Path
import json
Bank_NAME = "Mini Bank"
currency = "USD"
DATA_DIR = Path(__file__).parent / "logs"
DATA_DIR.mkdir(exist_ok=True)

log_file=DATA_DIR / "bank.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger=logging.getLogger(__name__)
logger.info(f"{Bank_NAME} started with currency: {currency}")

DATA_FILE = Path(__file__).parent / "data.json"

def load_data():
    """Load bank data from JSON file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"accounts": {}}

def save_data(data):
    """Save bank data to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


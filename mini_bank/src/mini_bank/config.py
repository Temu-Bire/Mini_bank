import logging
from pathlib import Path

Bank_NAME = "Mini Bank"
currency = "ETB"
DATA_DIR = Path(__file__).parent / "logs"
DATA_DIR.mkdir(exist_ok=True)

log_file=DATA_DIR / "bank.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger=logging.getLogger(__name__)
logger.info(f"{Bank_NAME} started with currency: {currency}")


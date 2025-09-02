from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / 'data'

# =============================================================================
# This Is Where You Store Your StanCan Archives:
# =============================================================================
DATA_EXTERNAL_PATH = DATA_DIR / 'external'

PAGE_URL = 'https://www150.statcan.gc.ca/n1/en/type/data'

from pathlib import Path

from pytonapi.utils import amount_to_nano

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOGS_DIR = BASE_DIR / 'logs'

CLAIM_COMPILED_JSON_PATH = BASE_DIR / 'src/claim/build/Claim.compiled.json'

USER_COMPILED_JSON_PATH = BASE_DIR / 'src/claim/build/User.compiled.json'

ADMIN_HIGHLOAD_MNEMO_PATH = BASE_DIR / 'secret/admin_highload_mnemo.json'

ADMIN_MNEMO_PATH = BASE_DIR / 'secret/admin_mnemo.json'

FIRST_CLAIM_AMOUNT = amount_to_nano(1)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOGS_DIR = BASE_DIR / 'logs'

CLAIM_COMPILED_JSON_PATH = BASE_DIR / 'src/claim/build/Claim.compiled.json'

USER_COMPILED_JSON_PATH = BASE_DIR / 'src/claim/build/User.compiled.json'

HIGHLOAD_MNEMO_PATH = BASE_DIR / 'secret/highload_mnemo.json'

MAIN_MNEMO_PATH = BASE_DIR / 'secret/main_mnemo.json'

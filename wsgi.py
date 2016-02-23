from bern_db import create_app

try:
    import config_local as config
except ImportError:
    config=None

app = create_app(config=config)

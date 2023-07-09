import contextlib
import json
import os

import psycopg2
from psycopg2.extras import RealDictCursor

config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path, "rt") as fin:
    config = json.load(fin)


@contextlib.contextmanager
def connection():
    connection = psycopg2.connect(
        host=config["host"],
        user=config["user"],
        password=config["pass"],
        database="watchtower",
        cursor_factory=RealDictCursor,
    )
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    except:
        connection.commit()
    finally:
        connection.close()

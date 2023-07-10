from datetime import datetime

from chalicelib.account import get_account, get_ad_units, get_apps
from chalicelib.auth import authenticate, authorize
from chalicelib.db import connection
from chalicelib.network import network_ecpm
from chalicelib.realtime import realtime_query
from chalicelib.service import backfill_account, sync_dataset, fetch_app_json
from chalicelib.utils import get_account_id

with connection() as conn:
    # print(get_apps(conn, 6))
    # print(get_ad_units(conn, 6))
    # print(network_ecpm(conn, 6, breakdowns=["format", "platform"]))
    # sync_dataset(conn)
    print(
        fetch_app_json(
            conn,
        )
    )
    # print(realtime_by_ad_unit(conn, 6, datetime(year=2023, month=7, day=1), datetime(year=2023, month=7, day=7)))

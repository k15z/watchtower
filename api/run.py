from datetime import datetime

from chalicelib.account import get_account, get_ad_units, get_apps
from chalicelib.auth import authenticate, authorize
from chalicelib.db import connection
from chalicelib.network import network_ecpm
from chalicelib.realtime import realtime_query
from chalicelib.service import backfill_account, sync_dataset
from chalicelib.utils import get_account_id

# with connection() as conn:
#    backfill_account(conn, 1)

from chalicelib.cards import handle_card

print(
    handle_card(
        name="ReportByAppV1", options={"date_filter": {"interval": "week"}}, user_id=8
    ).dict()
)

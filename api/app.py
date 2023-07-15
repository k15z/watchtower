import datetime
from zoneinfo import ZoneInfo

import boto3
from chalice import Chalice
from dateutil.parser import parse

from chalicelib.account import (delete_account, get_account, get_ad_units,
                                get_apps, insert_message)
from chalicelib.auth import (authenticate, authorize, delete_api_keys,
                             generate_api_key)
from chalicelib.db import connection
from chalicelib.network import network_ecpm
from chalicelib.realtime import realtime_by_app, realtime_query
from chalicelib.service import backfill_account, sync_dataset
from chalicelib.utils import get_account_id

app = Chalice(app_name="watchtower-api")
app.api.cors = True

sqs = boto3.client("sqs")


@app.route("/hello")
def _index():
    return {"hello": "world"}


@app.route("/authorize", methods=["POST"])
def _post_authorize():
    body = app.current_request.json_body
    auth_code = body["auth_code"]
    with connection() as conn:
        account_id, token, needs_backfill = authorize(conn, auth_code)
        if needs_backfill:
            sqs.send_message(
                QueueUrl="https://sqs.us-east-1.amazonaws.com/082395104119/WatchtowerNewUserAuth",
                MessageBody=str(account_id),
            )
        return {
            "id": account_id,
            "token": token,
        }


@app.route("/authenticate", methods=["POST"])
def _post_authenticate():
    body = app.current_request.json_body
    google_token = body["google_token"]
    with connection() as conn:
        return authenticate(conn, google_token)


@app.route("/account")
def _get_account():
    auth = app.current_request.headers.get("Authorization", None)
    token = auth.split()[1]
    with connection() as conn:
        id = get_account_id(conn, token)
        return get_account(conn, id)


@app.route("/account", methods=["DELETE"])
def _delete_account():
    auth = app.current_request.headers.get("Authorization", None)
    token = auth.split()[1]
    with connection() as conn:
        id = get_account_id(conn, token)
        return delete_account(conn, id)


@app.route("/account/apps")
def _get_account_apps():
    auth = app.current_request.headers.get("Authorization", None)
    token = auth.split()[1]
    with connection() as conn:
        id = get_account_id(conn, token)
        return get_apps(conn, id)


@app.route("/account/ad_units")
def _get_account_ad_units():
    auth = app.current_request.headers.get("Authorization", None)
    token = auth.split()[1]
    with connection() as conn:
        id = get_account_id(conn, token)
        return get_ad_units(conn, id)


@app.route("/account/api_keys")
def _generate_account_api_keys():
    auth = app.current_request.headers.get("Authorization", None)
    token = auth.split()[1]
    with connection() as conn:
        id = get_account_id(conn, token)
        return generate_api_key(conn, id)


@app.route("/account/api_keys", methods=["DELETE"])
def _delete_account_api_keys():
    auth = app.current_request.headers.get("Authorization", None)
    token = auth.split()[1]
    with connection() as conn:
        id = get_account_id(conn, token)
        return delete_api_keys(conn, id)


@app.route("/account/message", methods=["POST"])
def _post_account_message():
    auth = app.current_request.headers.get("Authorization", None)
    token = auth.split()[1]
    with connection() as conn:
        try:
            id = get_account_id(conn, token)
        except:
            id = None
        body = app.current_request.json_body
        body["email"], body["message"]
        return insert_message(conn, id, body["email"], body["message"])


@app.route("/network/ecpm")
def _get_network_ecpm():
    auth = app.current_request.headers.get("Authorization", None)
    token = auth.split()[1]
    with connection() as conn:
        id = get_account_id(conn, token)
        breakdowns = app.current_request.query_params.get("breakdowns", "").split(",")
        return network_ecpm(conn, id, breakdowns)


def _get_timedelta(period):
    match period:
        case "1-day":
            return datetime.timedelta(days=1)
        case "7-day":
            return datetime.timedelta(days=7)
        case "28-day":
            return datetime.timedelta(days=28)
        case _:
            raise ValueError("Unknown period: {period}.")


def _parse_start_end(query_params):
    if "period" in query_params:
        period = query_params.get("period")
        end = datetime.datetime.now(ZoneInfo("US/Pacific")) + datetime.timedelta(days=1)
        if query_params.get("previous"):
            end = end - _get_timedelta(period)
        start = end - _get_timedelta(period)
    else:
        start = parse(query_params.get("start", ""))
        end = parse(query_params.get("end", ""))
    return start, end


@app.route("/realtime/by_app")
def _get_realtime_by_app():
    auth = app.current_request.headers.get("Authorization", None)
    token = auth.split()[1]
    with connection() as conn:
        id = get_account_id(conn, token)
        start, end = _parse_start_end(app.current_request.query_params)
        return realtime_by_app(conn, id, start, end)


@app.route("/realtime/query")
def _realtime_query():
    auth = app.current_request.headers.get("Authorization", None)
    token = auth.split()[1]
    with connection() as conn:
        id = get_account_id(conn, token)
        start, end = _parse_start_end(app.current_request.query_params)
        breakdowns = app.current_request.query_params.get("breakdowns", "").split(",")
        return realtime_query(conn, id, start, end, breakdowns)


@app.on_sqs_message(queue="WatchtowerNewUserAuth")
def _backfill_account(event):
    with connection() as conn:
        for record in event:
            backfill_account(conn, int(record.body))


@app.schedule("rate(1 day)")
def _sync_dataset(event):
    with connection() as conn:
        sync_dataset(conn)

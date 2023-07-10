import datetime
import json
import requests
from zoneinfo import ZoneInfo
from google_play_scraper import app


from .utils import build_admob_service


def backfill_account(conn, id):
    service = build_admob_service(conn, id)
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE account SET status = 'STARTED_BACKFILL' WHERE id = %s", (id,)
        )
    conn.commit()

    try:
        _fetch_apps_and_ad_units(conn, service)
        date = datetime.datetime.now(ZoneInfo("US/Pacific")) - datetime.timedelta(
            days=1
        )
        while date > datetime.datetime.now(ZoneInfo("US/Pacific")) - datetime.timedelta(
            days=180
        ):
            _fetch_admob_data(conn, service, date)
            date = date - datetime.timedelta(days=1)
    except Exception as e:
        print(e)
        with conn.cursor() as cursor:
            cursor.execute("UPDATE account SET status = 'ERROR' WHERE id = %s", (id,))
        conn.commit()

    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE account SET status = 'FINISHED_BACKFILL' WHERE id = %s", (id,)
        )
    conn.commit()


def sync_dataset(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM account")
        account_ids = [row["id"] for row in cursor.fetchall()]
    date = datetime.datetime.now(ZoneInfo("US/Pacific")) - datetime.timedelta(days=1)
    for account_id in account_ids:
        try:
            service = build_admob_service(conn, account_id)
            _fetch_admob_data(conn, service, date)
        except Exception as e:
            print("Error updating", account_id, e)
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE account SET status = 'ERROR' WHERE id = %s", (account_id,)
                )
            conn.commit()


def _fetch_apps_and_ad_units(conn, service):
    response = service.accounts().list(pageSize=1).execute()

    apps = {}
    ad_units = {}

    account_list = response["account"]
    for account in account_list:
        # Fetch the apps
        next_page_token = ""
        while True:
            # Execute the request.
            response = (
                service.accounts()
                .apps()
                .list(
                    pageSize=1000,
                    pageToken=next_page_token,
                    parent="accounts/{}".format(account["publisherId"]),
                )
                .execute()
            )

            # Check if the response is empty.
            if not response:
                break

            # Insert the result
            for app in response["apps"]:
                app["publisherId"] = account["publisherId"]
                apps[app["appId"]] = app

            if "nextPageToken" not in response:
                break

            # Update the next page token.
            next_page_token = response["nextPageToken"]

        # Fetch the ad units
        next_page_token = ""
        while True:
            # Execute the request.
            response = (
                service.accounts()
                .adUnits()
                .list(
                    pageSize=1000,
                    pageToken=next_page_token,
                    parent="accounts/{}".format(account["publisherId"]),
                )
                .execute()
            )

            # Check if the response is empty.
            if not response:
                break

            # Insert the result
            for ad_unit in response["adUnits"]:
                ad_units[ad_unit["adUnitId"]] = ad_unit

            if "nextPageToken" not in response:
                break
            # Update the next page token.
            next_page_token = response["nextPageToken"]

    with conn.cursor() as cursor:
        for app in apps.values():
            cursor.execute(
                "INSERT INTO app (admob_publisher_id, admob_app_id, platform, app_store_id, display_name) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (
                    app["publisherId"],
                    app["appId"],
                    app["platform"],
                    app["linkedAppInfo"]["appStoreId"],
                    app["linkedAppInfo"]["displayName"],
                ),
            )
        for ad_unit in ad_units.values():
            cursor.execute(
                "INSERT INTO ad_unit (admob_ad_unit_id, admob_app_id, display_name, format, ad_types) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (
                    ad_unit["adUnitId"],
                    ad_unit["appId"],
                    ad_unit["displayName"],
                    ad_unit["adFormat"],
                    json.dumps(ad_unit["adTypes"]),
                ),
            )
    conn.commit()


def _fetch_admob_data(conn, service, date):
    response = service.accounts().list(pageSize=10).execute()
    for account in response["account"]:
        print("Handling:", account["publisherId"], date)

        year, month, day = date.year, date.month, date.day
        date_range = {
            "start_date": {"year": year, "month": month, "day": day},
            "end_date": {"year": year, "month": month, "day": day},
        }
        dimensions = [
            "APP",
            "DATE",
            "PLATFORM",
            "AD_UNIT",
            "COUNTRY",
            "FORMAT",
            "APP_VERSION_NAME",
            "MOBILE_OS_VERSION",
            "GMA_SDK_VERSION",
            "SERVING_RESTRICTION",
        ]
        metrics = [
            "ESTIMATED_EARNINGS",
            "MATCHED_REQUESTS",
            "AD_REQUESTS",
            "CLICKS",
            "IMPRESSIONS",
        ]
        report_spec = {
            "date_range": date_range,
            "dimensions": dimensions,
            "metrics": metrics,
            "sort_conditions": [],
            "dimension_filters": [],
            "localizationSettings": {
                "currencyCode": "USD",
                "languageCode": "en-US",
            },
        }
        request = {"report_spec": report_spec}

        # Execute network report request.
        response = (
            service.accounts()
            .networkReport()
            .generate(parent="accounts/{}".format(account["publisherId"]), body=request)
            .execute()
        )

        # Display responses.
        with conn.cursor() as cursor:
            rows = []
            for report_line in response[1:-1]:
                row = report_line["row"]
                rows.append(
                    (
                        row["dimensionValues"]["DATE"].get("value"),
                        row["dimensionValues"]["AD_UNIT"].get("value"),
                        row["dimensionValues"]["APP_VERSION_NAME"].get("value"),
                        row["dimensionValues"]["COUNTRY"].get("value"),
                        row["dimensionValues"]["MOBILE_OS_VERSION"].get("value"),
                        row["dimensionValues"]["GMA_SDK_VERSION"].get("value"),
                        row["dimensionValues"]["SERVING_RESTRICTION"].get("value"),
                        row["metricValues"]["ESTIMATED_EARNINGS"].get("microsValue"),
                        row["metricValues"]["CLICKS"].get("integerValue"),
                        row["metricValues"]["IMPRESSIONS"].get("integerValue"),
                        row["metricValues"]["AD_REQUESTS"].get("integerValue"),
                        row["metricValues"]["MATCHED_REQUESTS"].get("integerValue"),
                        row["metricValues"]["ESTIMATED_EARNINGS"].get("microsValue"),
                        row["metricValues"]["CLICKS"].get("integerValue"),
                        row["metricValues"]["IMPRESSIONS"].get("integerValue"),
                        row["metricValues"]["AD_REQUESTS"].get("integerValue"),
                        row["metricValues"]["MATCHED_REQUESTS"].get("integerValue"),
                    )
                )
            cursor.executemany(
                """
                INSERT INTO record (
                    date, admob_ad_unit_id, app_version, country, mobile_os_version, gma_sdk_version, serving_restriction,
                    earnings, clicks, impressions, requests, matched_requests) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT ON CONSTRAINT record_partition
                    DO UPDATE SET 
                        earnings = %s,
                        clicks = %s,
                        impressions = %s,
                        requests = %s,
                        matched_requests = %s;
                """,
                rows,
            )
        conn.commit()

def fetch_app_json(conn):
    """For each app, populate the app_external table with its metadata."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, platform, app_store_id FROM app WHERE id NOT IN (SELECT app_id FROM app_external)")
        results = cursor.fetchall()

    rows = []
    for row in results:
        if row["platform"] == "ANDROID":
            metadata = app(
                row['app_store_id'],
                lang='en', # defaults to 'en'
                country='us' # defaults to 'us'
            )
        elif row["platform"] == "IOS":
            url = f"https://itunes.apple.com/lookup?id={row['app_store_id']}&country=US&entity=software"
            metadata = requests.get(url).json()["results"][0]
        else:
            print("Unknown platform", row)
        genre = metadata.get("genre", metadata.get('primaryGenreName'))
        rows.append((
            row["id"],
            genre,
            json.dumps(metadata, indent=2)
        ))

    with conn.cursor() as cursor:
        cursor.executemany("INSERT INTO app_external (app_id, genre, metadata) VALUES (%s, %s, %s)", rows)
    conn.commit()

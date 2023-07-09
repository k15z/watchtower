"""
GET /api/realtime/by_app?start=...&end=...
GET /api/realtime/by_ad_unit?start=...&end=...
"""
import datetime
from zoneinfo import ZoneInfo

from .utils import build_admob_service


def _query_admob(conn, id, start_date, end_date, by):
    service = build_admob_service(conn, id)
    response = service.accounts().list(pageSize=10).execute()
    result = []
    for account in response["account"]:
        date_range = {
            "start_date": {
                "year": start_date.year,
                "month": start_date.month,
                "day": start_date.day,
            },
            "end_date": {
                "year": end_date.year,
                "month": end_date.month,
                "day": end_date.day,
            },
        }

        if by == "app":
            dimensions = ["APP", "PLATFORM"]
        else:
            dimensions = ["AD_UNIT"]
        metrics = [
            "ESTIMATED_EARNINGS",
            "AD_REQUESTS",
            "MATCHED_REQUESTS",
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

        # Create network report request.
        request = {"report_spec": report_spec}

        # Execute network report request.
        response = (
            service.accounts()
            .networkReport()
            .generate(parent="accounts/{}".format(account["publisherId"]), body=request)
            .execute()
        )

        # Display responses.
        for report_line in response[1:-1]:
            row = report_line["row"]
            result.append(row)
    return result


def realtime_by_app(conn, id, start_date, end_date):
    return _query_admob(conn, id, start_date, end_date, by="app")


def realtime_by_ad_unit(conn, id, start_date, end_date):
    return _query_admob(conn, id, start_date, end_date, by="ad_unit")

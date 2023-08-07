import math
from enum import Enum
from typing import TypeVar, List, Union, Optional
from zoneinfo import ZoneInfo
from pydantic import BaseModel, validate_arguments
from datetime import datetime, timedelta
from chalicelib.utils import build_admob_service
from chalicelib.db import connection

T = TypeVar("T")


class BaseCard(BaseModel):
    pass


class StartEndDateFilter(BaseModel):
    start: datetime
    end: datetime


class RecentInterval(str, Enum):
    Day = "day"
    Week = "week"
    Month = "month"


class RecentIntervalDateFilter(BaseModel):
    interval: RecentInterval


DateFilter = Union[StartEndDateFilter, RecentIntervalDateFilter]


class IntCurrentAndPrevious(BaseModel):
    # TODO: revisit using generics, but seems to behave very badly with JSON serialization
    current: int
    previous: int


class FloatCurrentAndPrevious(BaseModel):
    current: float
    previous: float


def _get_time_delta(interval: str):
    match interval:
        case "day":
            return timedelta(days=1 - 1)
        case "week":
            return timedelta(days=7 - 1)
        case "month":
            return timedelta(days=28 - 1)


def _date_filter_to_start_end(
    date_filter: DateFilter, zoneinfo: str
) -> (datetime, datetime):
    if isinstance(date_filter, RecentIntervalDateFilter):
        end = datetime.now(ZoneInfo(zoneinfo))
        if date_filter.interval != "day":
            # For week and month modes, start from yesterday.
            end = end - timedelta(days=1)
        start = end - _get_time_delta(date_filter.interval)
        return start, end
    return date_filter.start, date_filter.end


# ---


def _get_basics(service, start, end, publisher_id, dimensions=[]):
    date_range = {
        "start_date": {
            "year": start.year,
            "month": start.month,
            "day": start.day,
        },
        "end_date": {
            "year": end.year,
            "month": end.month,
            "day": end.day,
        },
    }

    metrics = [
        "ESTIMATED_EARNINGS",
        "AD_REQUESTS",
        "IMPRESSIONS",
    ]
    report_spec = {
        "date_range": date_range,
        "dimensions": dimensions,
        "metrics": metrics,
        "sort_conditions": [],
        "dimension_filters": [],
        "localizationSettings": {
            "languageCode": "en-US",
        },
    }

    # Create network report request.
    request = {"report_spec": report_spec}

    # Execute network report request.
    response = (
        service.accounts()
        .networkReport()
        .generate(parent="accounts/{}".format(publisher_id), body=request)
        .execute()
    )

    # Display responses.
    currency_code = response[0]["header"]["localizationSettings"].get(
        "currencyCode", "USD"
    )
    return currency_code, [row["row"] for row in response[1:-1]]


class ReportCardV1Options(BaseModel):
    user_id: int
    date_filter: RecentIntervalDateFilter


class ReportCardV1(BaseCard):
    time_zone: str
    currency_code: str
    estimated_earnings: FloatCurrentAndPrevious
    impressions: IntCurrentAndPrevious
    ad_requests: IntCurrentAndPrevious
    ecpm: FloatCurrentAndPrevious

    @classmethod
    @validate_arguments
    def build(self, options: ReportCardV1Options):
        with connection() as conn:
            service = build_admob_service(conn, options.user_id)

        result = {}
        response = service.accounts().list(pageSize=10).execute()
        for account in response["account"]:
            result["time_zone"] = account["reportingTimeZone"]

            start, end = _date_filter_to_start_end(
                options.date_filter, account["reportingTimeZone"]
            )
            result["currency_code"], current = _get_basics(
                service, start, end, account["publisherId"]
            )
            result["currency_code"], previous = _get_basics(
                service,
                start
                - (_get_time_delta(options.date_filter.interval) + timedelta(days=1)),
                end
                - (_get_time_delta(options.date_filter.interval) + timedelta(days=1)),
                account["publisherId"],
            )
            if not current:
                current = [
                    {
                        "metricValues": {
                            "ESTIMATED_EARNINGS": {"microsValue": 0},
                            "IMPRESSIONS": {"integerValue": 0},
                            "AD_REQUESTS": {"integerValue": 0},
                        }
                    }
                ]
            if not previous:
                previous = [
                    {
                        "metricValues": {
                            "ESTIMATED_EARNINGS": {"microsValue": 0},
                            "IMPRESSIONS": {"integerValue": 0},
                            "AD_REQUESTS": {"integerValue": 0},
                        }
                    }
                ]

            result["estimated_earnings"] = FloatCurrentAndPrevious(
                current=int(
                    current[0]["metricValues"]["ESTIMATED_EARNINGS"]["microsValue"]
                )
                / (1000.0 * 1000.0),
                previous=int(
                    previous[0]["metricValues"]["ESTIMATED_EARNINGS"]["microsValue"]
                )
                / (1000.0 * 1000.0),
            )
            result["impressions"] = IntCurrentAndPrevious(
                current=int(current[0]["metricValues"]["IMPRESSIONS"]["integerValue"]),
                previous=int(
                    previous[0]["metricValues"]["IMPRESSIONS"]["integerValue"]
                ),
            )
            result["ad_requests"] = IntCurrentAndPrevious(
                current=int(current[0]["metricValues"]["AD_REQUESTS"]["integerValue"]),
                previous=int(
                    previous[0]["metricValues"]["AD_REQUESTS"]["integerValue"]
                ),
            )
            result["ecpm"] = FloatCurrentAndPrevious(
                current=result["estimated_earnings"].current
                / (
                    result["impressions"].current
                    if result["impressions"].current
                    else float("nan")
                )
                * 1000.0,
                previous=result["estimated_earnings"].previous
                / (
                    result["impressions"].previous
                    if result["impressions"].previous
                    else float("nan")
                )
                * 1000.0,
            )
            if math.isnan(result["ecpm"].current):
                result["ecpm"].current = 0.0
            if math.isnan(result["ecpm"].previous):
                result["ecpm"].previous = 0.0
        return ReportCardV1(**result)


# ---


class PlatformECPMV1Options(BaseModel):
    date_filter: DateFilter


class PlatformECPMV1Row(BaseModel):
    ad_format: str
    ios_ecpm: Optional[float]
    android_ecpm: Optional[float]


class PlatformECPMV1(BaseCard):
    rows: List[PlatformECPMV1Row]

    @classmethod
    @validate_arguments
    def build(self, options: PlatformECPMV1Options):
        format_to_row = {}
        with connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        format,
                        platform,
                        (SUM(earnings) / SUM(impressions)) / 1000.0 as ecpm
                    FROM (
                        SELECT * FROM record
                        LEFT JOIN ad_unit ON record.admob_ad_unit_id = ad_unit.admob_ad_unit_id
                        LEFT JOIN app ON ad_unit.admob_app_id = app.admob_app_id
                        WHERE impressions > 0
                    ) dataset
                    GROUP BY format, platform
                    ORDER BY format, platform
                    """
                )
                for row in cursor.fetchall():
                    if row["format"] not in format_to_row:
                        format_to_row[row["format"]] = PlatformECPMV1Row(
                            ad_format=row["format"],
                            ios_ecpm=None,
                            android_ecpm=None,
                        )
                    if row["platform"] == "IOS":
                        format_to_row[row["format"]].ios_ecpm = float(row["ecpm"])
                    elif row["platform"] == "ANDROID":
                        format_to_row[row["format"]].android_ecpm = float(row["ecpm"])
        return PlatformECPMV1(rows=list(format_to_row.values()))


# ---


def format_date(yyyymmdd):
    return "{}-{}-{}".format(yyyymmdd[:4], yyyymmdd[4:6], yyyymmdd[6:])


class TimeSeriesPlotV1Options(BaseModel):
    user_id: int
    date_filter: DateFilter


class TimeSeriesPlotV1Row(BaseModel):
    date: str
    estimated_earnings: float
    impressions: int
    ad_requests: int


class TimeSeriesPlotV1(BaseCard):
    currency_code: str
    rows: List[TimeSeriesPlotV1Row]

    @classmethod
    @validate_arguments
    def build(self, options: TimeSeriesPlotV1Options):
        with connection() as conn:
            service = build_admob_service(conn, options.user_id)

        result = {"rows": []}
        response = service.accounts().list(pageSize=10).execute()
        for account in response["account"]:
            result["time_zone"] = account["reportingTimeZone"]

            start, end = _date_filter_to_start_end(
                options.date_filter, account["reportingTimeZone"]
            )

            result["currency_code"], rows = _get_basics(
                service, start, end, account["publisherId"], dimensions=["DATE"]
            )
            for row in rows:
                result["rows"].append(
                    {
                        "date": format_date(row["dimensionValues"]["DATE"]["value"]),
                        "estimated_earnings": int(
                            row["metricValues"]["ESTIMATED_EARNINGS"]["microsValue"]
                        )
                        / (1000.0 * 1000.0),
                        "impressions": int(
                            row["metricValues"]["IMPRESSIONS"]["integerValue"]
                        ),
                        "ad_requests": int(
                            row["metricValues"]["AD_REQUESTS"]["integerValue"]
                        ),
                    }
                )
        return TimeSeriesPlotV1(**result)


# ---


class EarningsByDayOfWeekV1Row(BaseModel):
    day_of_week: str
    min: float
    p25: float
    p50: float
    p75: float
    max: float


class EarningsByDayOfWeekOptions(BaseModel):
    user_id: int


class EarningsByDayOfWeekV1(BaseCard):
    rows: List[EarningsByDayOfWeekV1Row]

    @classmethod
    @validate_arguments
    def build(self, options: EarningsByDayOfWeekOptions):
        rows = []
        with connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                    to_char(date, 'Day') as day_of_week,
                        MIN(earnings) as min,
                        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY earnings) as P25,
                        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY earnings) as P50,
                        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY earnings) as P75,
                        ( -- max = 1.5*IQR + Q3
                            (PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY earnings)) + 
                            1.5 * ((PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY earnings)) - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY earnings))
                        ) as max
                    FROM (
                    SELECT
                        date,
                        SUM(earnings) as earnings
                    FROM record
                    LEFT JOIN ad_unit ON record.admob_ad_unit_id = ad_unit.admob_ad_unit_id
                    LEFT JOIN app ON ad_unit.admob_app_id = app.admob_app_id
                    LEFT JOIN publisher ON app.admob_publisher_id = publisher.admob_publisher_id
                    LEFT JOIN account ON publisher.account_id = account.id
                    WHERE account.id = %s
                    GROUP BY date
                    ) x
                    GROUP BY day_of_week
                    """,
                    (options.user_id,),
                )
                for row in cursor.fetchall():
                    rows.append(
                        EarningsByDayOfWeekV1Row(
                            day_of_week=row["day_of_week"].strip(),
                            min=float(row["min"]) / (1000.0 * 1000.0),
                            p25=float(row["p25"]) / (1000.0 * 1000.0),
                            p50=float(row["p50"]) / (1000.0 * 1000.0),
                            p75=float(row["p75"]) / (1000.0 * 1000.0),
                            max=float(row["max"]) / (1000.0 * 1000.0),
                        )
                    )
        rows = sorted(
            rows,
            key=lambda row: [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ].index(row.day_of_week),
        )
        return EarningsByDayOfWeekV1(rows=rows)


# ---


class ECPMByGenreV1Row(BaseModel):
    app_genre: str
    ecpm: float


class ECPMByGenreV1Options(BaseModel):
    ad_format: str


class ECPMByGenreV1(BaseCard):
    rows: List[ECPMByGenreV1Row]

    @classmethod
    @validate_arguments
    def build(self, options: ECPMByGenreV1Options):
        rows = []
        with connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        genre,
                        (SUM(earnings) / SUM(impressions)) / 1000.0 as ecpm
                    FROM (
                        SELECT cast(date_trunc('week', date) as date) as week, * FROM record
                        LEFT JOIN ad_unit ON record.admob_ad_unit_id = ad_unit.admob_ad_unit_id
                        LEFT JOIN app ON ad_unit.admob_app_id = app.admob_app_id
                        LEFT JOIN app_external ON app.id = app_external.app_id
                        LEFT JOIN publisher ON app.admob_publisher_id = publisher.admob_publisher_id
                        LEFT JOIN account ON publisher.account_id = account.id
                        WHERE impressions > 0 AND format = %s
                    ) dataset
                    GROUP BY genre
                    ORDER BY genre
                    """, (options.ad_format,)
                )
                for row in cursor.fetchall():
                    rows.append(
                        ECPMByGenreV1Row(
                            app_genre=row["genre"].strip(),
                            ecpm=float(row["ecpm"]),
                        )
                    )
        return ECPMByGenreV1(rows=rows)


# ---

card_name_to_class = {card.__name__: card for card in BaseCard.__subclasses__()}

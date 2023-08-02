import sys
sys.path.append("./")

from datetime import datetime, timedelta

import country_converter as coco
import pandas as pd
from dateutil import parser

from api.chalicelib.db import connection


class WeeklySummaryWriter:
    """Summarize the week-over-week eCPM across various breakdowns."""

    OUTLIER_THRESHOLD = 10.0
    MIN_IMPRESSION_COUNT = 1000

    def __init__(self, end_date=None):
        if not end_date:
            self.end_date = datetime.now()
        elif not isinstance(end_date, datetime):
            self.end_date = parser.parse(end_date)
        else:
            self.end_date = end_date
        self._fetch_data()
        self._build_strings()

    def summarize(self):
        result = ""
        for key, value in self._strings.items():
            if value:
                result += value + "\n\n"
        return result

    def _build_strings(self):
        num_impressions = self.df["impressions"].sum()
        overall_pct_change = self._ecpm_overall()
        if not overall_pct_change:
            self._strings = {
                "": "We are unable to generate a report for this week."
            }
        else:
            self._strings = {
                "overall_str": self._describe_ecpm_overall(
                    num_impressions, overall_pct_change
                ),
                "region_str": self._ecpm_outliers("region", overall_pct_change),
                "platform_str": self._ecpm_outliers("platform", overall_pct_change),
                "serving_restriction_str": self._ecpm_outliers(
                    "serving_restriction", overall_pct_change
                ),
                "genre_str": self._ecpm_outliers("genre", overall_pct_change),
            }

    def _fetch_data(self):
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT is_current, country, platform, SUM(impressions) as impressions, SUM(earnings) as earnings, serving_restriction, platform, genre FROM (
                        SELECT date >= %s as is_current, * FROM record
                        LEFT JOIN ad_unit ON record.admob_ad_unit_id = ad_unit.admob_ad_unit_id
                        LEFT JOIN app ON ad_unit.admob_app_id = app.admob_app_id
                        LEFT JOIN app_external ON app.id = app_external.app_id
                        LEFT JOIN publisher ON app.admob_publisher_id = publisher.admob_publisher_id
                        LEFT JOIN account ON publisher.account_id = account.id
                        WHERE date >= %s AND date < %s
                    ) dataset GROUP BY is_current, country, platform, serving_restriction, genre
                """,
                    (
                        self.end_date - timedelta(days=7),
                        self.end_date - timedelta(days=14),
                        self.end_date,
                    ),
                )
                rows = cur.fetchall()
        self.df = pd.DataFrame(rows)
        cc = coco.CountryConverter()
        self.df["region"] = cc.convert(
            names=self.df["country"], to="continent", not_found=None
        )

    def _describe_ecpm_overall(self, num_impressions, overall_pct_change):
        result = f"Based on an anonymized dataset with approximately {num_impressions:,} impressions, the average eCPM has "
        if overall_pct_change < 0:
            result += f"decreased around {-overall_pct_change:.0f}% compared to the previous week."
        else:
            result += f"increased around {overall_pct_change:.0f}% compared to the previous week."
        return result

    def _delta_string(self, pct_change):
        if pct_change < 0:
            return f"decreased by {-pct_change:.0f}%"
        else:
            return f"increased by {pct_change:.0f}%"

    def _key_to_human_string(self, key):
        match key:
            case "serving_restriction":
                return "privacy/personalization settings"
            case "genre":
                return "app genre/category"
        return key

    def _value_to_human_string(self, key):
        match key:
            case "Non-personalized ads":
                return '"non-personalized ads"'
            case "Personalization disabled":
                return '"personalization disabled"'
        return key

    def _ecpm_overall(self):
        current = self.df[self.df["is_current"]]
        previous = self.df[~self.df["is_current"]]
        if self.df["impressions"].sum() > self.MIN_IMPRESSION_COUNT:
            current_ecpm = current["earnings"].sum() / (
                current["impressions"].sum() * 1000.0
            )
            previous_ecpm = previous["earnings"].sum() / (
                previous["impressions"].sum() * 1000.0
            )
            return 100.0 * (current_ecpm - previous_ecpm) / previous_ecpm

    def _ecpm_outliers(self, breakdown, overall_pct_change):
        # Find the breakdown values that are most different from the overall percent change.
        breakdown_to_pct_change = {}
        for key, df in self.df.groupby(breakdown):
            current = df[df["is_current"]]
            previous = df[~df["is_current"]]
            if (
                current["impressions"].sum() > self.MIN_IMPRESSION_COUNT
                and previous["impressions"].sum() > self.MIN_IMPRESSION_COUNT
            ):
                current_ecpm = current["earnings"].sum() / (
                    current["impressions"].sum() * 1000.0
                )
                previous_ecpm = previous["earnings"].sum() / (
                    previous["impressions"].sum() * 1000.0
                )
                pct_change = 100.0 * (current_ecpm - previous_ecpm) / previous_ecpm
                breakdown_to_pct_change[key] = pct_change
        outliers = {}
        for key, value in breakdown_to_pct_change.items():
            if (value - overall_pct_change) > self.OUTLIER_THRESHOLD:
                outliers[key] = value
        if not outliers:
            return f"Looking at {self._key_to_human_string(breakdown)}, there are no clear trends in eCPM."
        if len(outliers) == 1:
            return (
                f"Looking at {self._key_to_human_string(breakdown)}, it appears that {self._value_to_human_string(list(outliers.keys())[0])} is an outlier where the eCPM actually "
                + self._delta_string(list(outliers.values())[0])
                + "."
            )


if __name__ == "__main__":
    wsw = WeeklySummaryWriter()
    print(wsw.summarize())

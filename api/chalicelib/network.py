"""
GET /api/network/ecpm?breakdowns=date,platform,format
"""
import pandas as pd

VALID_BREAKDOWNS = set(
    [
        "week",
        "genre",
        "country",
        "format",
        "platform",
        "mobile_os_version",
        "serving_restriction",
        "gma_sdk_version",
    ]
)


def network_ecpm(conn, id, breakdowns):
    assert set(breakdowns).issubset(VALID_BREAKDOWNS)
    with conn.cursor() as cursor:
        cursor.execute(
            f"""
        SELECT
            {",".join(breakdowns)},
            (SUM(earnings) / SUM(impressions)) / 1000.0 as ecpm,
            (
                SUM(CASE WHEN account_id = %s THEN earnings ELSE 0 END) / 
                NULLIF(SUM(CASE WHEN account_id = %s THEN impressions ELSE 0 END), 0)
            ) / 1000.0 as your_ecpm
        FROM (
            SELECT cast(date_trunc('week', date) as date) as week, * FROM record
            LEFT JOIN ad_unit ON record.admob_ad_unit_id = ad_unit.admob_ad_unit_id
            LEFT JOIN app ON ad_unit.admob_app_id = app.admob_app_id
            LEFT JOIN app_external ON app.id = app_external.app_id
            LEFT JOIN publisher ON app.admob_publisher_id = publisher.admob_publisher_id
            LEFT JOIN account ON publisher.account_id = account.id
            WHERE impressions > 0
        ) dataset
        GROUP BY {",".join(breakdowns)}
        ORDER BY {",".join(breakdowns)}
        """,
            (id, id),
        )
        rows = cursor.fetchall()
        if "week" not in breakdowns:
            return rows

        # Special handling for time series breakdowns
        df = pd.DataFrame(rows)
        df["week"] = df["week"].map(lambda x: x.strftime("%Y-%m-%d"))
        breakdowns_no_date = [x for x in breakdowns if x != "week"]
        if not breakdowns_no_date:
            raise ValueError("Expected additional breakdowns with week!")
        df = df.pivot(index="week", columns=breakdowns_no_date, values="ecpm")
        df = df.where((pd.notnull(df)), None)

        series = []
        for column_name in df.columns:
            series.append(
                {
                    "breakdown": column_name,
                    "data": df[column_name].values.tolist(),
                }
            )
        return {"week": df.index.values.tolist(), "series": series}

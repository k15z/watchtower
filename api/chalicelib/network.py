"""
GET /api/network/ecpm?breakdowns=date,platform,format
"""

VALID_BREAKDOWNS = set(
    [
        "date",
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
            SELECT * FROM record
            JOIN ad_unit ON record.admob_ad_unit_id = ad_unit.admob_ad_unit_id
            JOIN app ON ad_unit.admob_app_id = app.admob_app_id
            JOIN publisher ON app.admob_publisher_id = publisher.admob_publisher_id
            JOIN account ON publisher.account_id = account.id
            WHERE impressions > 0
        ) dataset
        GROUP BY {",".join(breakdowns)}
        ORDER BY {",".join(breakdowns)}
        """,
            (id, id),
        )
        return cursor.fetchall()

def get_account(conn, id: int):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT email, picture_url, first_name, last_name, status FROM account WHERE id = %s",
            (id,),
        )
        row = cursor.fetchone()
        if not row:
            raise ValueError("Account doesn't exist.")
    return row


def delete_account(conn, id):
    with conn.cursor() as cursor:
        cursor.execute("UPDATE account SET status = 'DELETED' WHERE id = %s", (id,))
        return cursor.rowcount


def get_apps(conn, id):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT admob_publisher_id, admob_app_id, platform, app_store_id, display_name FROM app WHERE admob_publisher_id IN (SELECT admob_publisher_id FROM publisher WHERE account_id = %s)",
            (id,),
        )
        return cursor.fetchall()


def get_ad_units(conn, id):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT admob_ad_unit_id, admob_app_id, display_name, format, ad_types FROM ad_unit WHERE admob_app_id IN (SELECT admob_app_id FROM app WHERE admob_publisher_id IN (SELECT admob_publisher_id FROM publisher WHERE account_id = %s))",
            (id,),
        )
        return cursor.fetchall()

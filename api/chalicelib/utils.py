import base64
import pickle

from googleapiclient.discovery import build


def get_account_id(conn, token: str) -> int:
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT account_id FROM token WHERE token = %s AND expires_at > NOW()",
            (token,),
        )
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Unknown token: {token}")
    return row["account_id"]


def build_admob_service(conn, id: int):
    with conn.cursor() as cursor:
        cursor.execute("SELECT credentials FROM account WHERE id = %s", (id,))
        credentials = pickle.loads(base64.b64decode(cursor.fetchone()["credentials"]))
    return build("admob", "v1", credentials=credentials)

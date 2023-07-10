import base64
import os
import pickle
import uuid

from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
CLIENT_ID = "758313252344-959jdouposo1nd3mq7c01b6rbv0mf8hf.apps.googleusercontent.com"


def _generate_auth_token(conn, account_id: int) -> str:
    auth_token = str(uuid.uuid4())
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO token (account_id, token) VALUES (%s, %s)",
            (account_id, auth_token),
        )
    conn.commit()
    return auth_token


def authenticate(conn, google_token: str) -> str:
    idinfo = id_token.verify_oauth2_token(google_token, Request(), CLIENT_ID)
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM account WHERE email = %s", (idinfo["email"],))
        row = cursor.fetchone()
        if not row:
            raise ValueError("User doesn't exist.")
    return _generate_auth_token(conn, row["id"])


def authorize(conn, auth_code: str) -> str:
    client_secrets = os.path.join(os.path.dirname(__file__), "secrets.json")
    flow = Flow.from_client_secrets_file(
        client_secrets, scopes=["https://www.googleapis.com/auth/admob.readonly"]
    )
    flow.redirect_uri = "postmessage"
    flow.fetch_token(code=auth_code, include_client_id=True)

    idinfo = id_token.verify_oauth2_token(
        flow.credentials.id_token, Request(), CLIENT_ID
    )
    response = (
        build("admob", "v1", credentials=flow.credentials)
        .accounts()
        .list(pageSize=10)
        .execute()
    )
    publisher_ids = [account["publisherId"] for account in response["account"]]

    with conn.cursor() as cursor:
        # Insert account profile
        cursor.execute("SELECT id FROM account WHERE email = %s", (idinfo["email"],))
        row = cursor.fetchone()
        if row:
            account_id = row["id"]
            cursor.execute(
                "UPDATE account SET credentials = %s WHERE id = %s",
                (
                    base64.b64encode(pickle.dumps(flow.credentials)),
                    account_id,
                ),
            )
        else:
            cursor.execute(
                "INSERT INTO account (email, picture_url, first_name, last_name, credentials) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (
                    idinfo["email"],
                    idinfo["picture"],
                    idinfo["given_name"],
                    idinfo["family_name"],
                    base64.b64encode(pickle.dumps(flow.credentials)),
                ),
            )
            account_id = cursor.fetchone()["id"]

        # Insert publisher IDs
        cursor.executemany(
            "INSERT INTO publisher (account_id, admob_publisher_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            [(account_id, publisher_id) for publisher_id in publisher_ids],
        )
    conn.commit()

    return account_id, _generate_auth_token(conn, account_id)


def generate_api_key(conn, account_id):
    auth_token = str(uuid.uuid4())
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO token (account_id, token, type) VALUES (%s, %s, %s)",
            (account_id, auth_token, "API_KEY"),
        )
    conn.commit()
    return auth_token


def delete_api_keys(conn, account_id):
    with conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM token WHERE account_id = %s AND type = %s",
            (account_id, "API_KEY"),
        )
    conn.commit()

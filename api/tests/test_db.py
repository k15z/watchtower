from chalicelib.db import connection

def test_connect():
    with connection() as conn:
        assert not conn.closed
    assert conn.closed

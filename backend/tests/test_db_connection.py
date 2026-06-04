from app.db.connection import get_connection


def test_db_connection_can_execute_simple_query() -> None:
    conn = get_connection()
    cur = conn.execute('SELECT 1')
    result = cur.fetchone()

    assert result is not None
    assert result[0] == 1
    
    conn.close()
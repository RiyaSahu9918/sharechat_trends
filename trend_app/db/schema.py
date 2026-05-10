from trend_app.db.connection import get_connection
from trend_app.db.queries import (
    CREATE_TREND_POSTS_TABLE,
    CREATE_TREND_RUNS_TABLE,
    CREATE_TREND_TAGS_TABLE,
)


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(CREATE_TREND_RUNS_TABLE)
    cur.execute(CREATE_TREND_TAGS_TABLE)
    cur.execute(CREATE_TREND_POSTS_TABLE)
    conn.commit()
    conn.close()

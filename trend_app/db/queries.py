CREATE_TREND_RUNS_TABLE = """
CREATE TABLE IF NOT EXISTS trend_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date TEXT NOT NULL UNIQUE,
    generation_mode TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL
);
"""

CREATE_TREND_TAGS_TABLE = """
CREATE TABLE IF NOT EXISTS trend_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    title_hi TEXT NOT NULL,
    description_hi TEXT NOT NULL,
    category TEXT NOT NULL,
    heat_score REAL NOT NULL,
    rank INTEGER NOT NULL,
    signal_source TEXT NOT NULL,
    signal_volume REAL NOT NULL,
    spike_factor REAL NOT NULL,
    recency_score REAL NOT NULL,
    diversity_adjustment REAL NOT NULL,
    region TEXT NOT NULL,
    language TEXT NOT NULL,
    trend_date TEXT NOT NULL,
    created_at TEXT NOT NULL,
    daily_active_users_clicks INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    searches_in_last_30mins INTEGER DEFAULT 0,
    users_from_multiple_sources REAL DEFAULT 0.0,
    trends_in_other_platforms REAL DEFAULT 0.0,
    new_vs_old_users REAL DEFAULT 0.0,
    mobile_os_type TEXT DEFAULT '',
    app_vs_web REAL DEFAULT 0.0,
    session_time_in_category INTEGER DEFAULT 0,
    creators_in_category_recently INTEGER DEFAULT 0,
    nearby_location_trends REAL DEFAULT 0.0,
    gender TEXT DEFAULT '',
    seasonal_event INTEGER DEFAULT 0,
    occasion TEXT DEFAULT '',
    FOREIGN KEY(run_id) REFERENCES trend_runs(id)
);
"""

CREATE_TREND_POSTS_TABLE = """
CREATE TABLE IF NOT EXISTS trend_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trend_tag_id INTEGER NOT NULL,
    author_name TEXT NOT NULL,
    content_text TEXT NOT NULL,
    media_type TEXT NOT NULL,
    media_url TEXT,
    likes INTEGER NOT NULL,
    comments INTEGER NOT NULL,
    shares INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(trend_tag_id) REFERENCES trend_tags(id)
);
"""

SELECT_RUN_BY_DATE = "SELECT id FROM trend_runs WHERE run_date = ?"
INSERT_TREND_RUN = (
    "INSERT INTO trend_runs(run_date, generation_mode, notes, created_at) VALUES (?, ?, ?, ?)"
)

INSERT_TREND_TAG = """
INSERT INTO trend_tags(
    run_id, tag, title_hi, description_hi, category, heat_score, rank, signal_source,
    signal_volume, spike_factor, recency_score, diversity_adjustment, region, language,
    trend_date, created_at, daily_active_users_clicks, views, searches_in_last_30mins,
    users_from_multiple_sources, trends_in_other_platforms, new_vs_old_users,
    mobile_os_type, app_vs_web, session_time_in_category, creators_in_category_recently,
    nearby_location_trends, gender, seasonal_event, occasion
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

INSERT_TREND_POST = """
INSERT INTO trend_posts(
    trend_tag_id, author_name, content_text, media_type, media_url, likes, comments, shares, created_at
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SELECT_LATEST_TRENDS = """
SELECT *
FROM trend_tags
WHERE run_id = (
    SELECT id
    FROM trend_runs
    ORDER BY run_date DESC
    LIMIT 1
)
ORDER BY rank ASC
LIMIT ?
"""

SELECT_TREND_BY_ID = "SELECT * FROM trend_tags WHERE id = ?"
SELECT_POSTS_BY_TREND_ID = (
    "SELECT * FROM trend_posts WHERE trend_tag_id = ? ORDER BY likes DESC"
)

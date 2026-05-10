JSON_CONTENT_TYPE = "application/json; charset=utf-8"
HTML_CONTENT_TYPE = "text/html; charset=utf-8"

ROOT_PATH = "/"
TRENDS_PATH = "/api/trends"
TREND_GENERATE_PATH = "/api/trends/generate"
TREND_DETAIL_PREFIX = "/api/trends/"

DEFAULT_LIMIT = 10
TOP_K_PER_CATEGORY = 3
MAX_FINAL_TRENDS = 10

REGION_INDIA = "IN"
LANGUAGE_HINDI = "hi"

WEIGHT_ENGAGEMENT = 0.4
WEIGHT_SPIKE = 0.3
WEIGHT_RECENCY = 0.2
WEIGHT_DIVERSITY = 0.1

SOURCE_WEIGHTS = {
    "google_trends": 0.28,
    "twitter": 0.22,
    "youtube": 0.18,
    "news": 0.17,
    "social": 0.15,
}

import json
from urllib.parse import parse_qs, urlparse

from trend_app.constants import (
    DEFAULT_LIMIT,
    HTML_CONTENT_TYPE,
    JSON_CONTENT_TYPE,
    ROOT_PATH,
    TREND_DETAIL_PREFIX,
    TREND_GENERATE_PATH,
    TRENDS_PATH,
)
from trend_app.api.schemas import (
    validate_generate_response_payload,
    validate_trend_detail_payload,
    validate_trends_list_payload,
)
from trend_app.services.trends_service import (
    generate_for_today,
    latest_trends,
    trend_detail,
)
from trend_app.web.templates import INDEX_HTML


def _json_response(payload, status_code: int = 200):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return status_code, JSON_CONTENT_TYPE, body


def _html_response(html: str, status_code: int = 200):
    return status_code, HTML_CONTENT_TYPE, html.encode("utf-8")


def _parse_limit(query_string: str) -> int:
    params = parse_qs(query_string)
    raw_limit = params.get("limit", [str(DEFAULT_LIMIT)])[0]
    try:
        parsed = int(raw_limit)
        if parsed < 1:
            raise ValueError("Limit should be positive")
        return parsed
    except ValueError:
        return DEFAULT_LIMIT


def _handle_trends_list(query_string: str):
    payload = latest_trends(limit=_parse_limit(query_string))
    return _json_response(validate_trends_list_payload(payload))


def _handle_trend_detail(path: str):
    raw_id = path.split("/")[-1]
    try:
        trend_id = int(raw_id)
    except ValueError:
        return _json_response({"error": "invalid id"}, status_code=400)

    payload = trend_detail(trend_id)
    if payload is None:
        return _json_response({"error": "not found"}, status_code=404)
    return _json_response(validate_trend_detail_payload(payload))


def handle_get(path: str):
    try:
        parsed = urlparse(path)
        exact_routes = {
            ROOT_PATH: lambda: _html_response(INDEX_HTML),
            TRENDS_PATH: lambda: _handle_trends_list(parsed.query),
        }

        route_handler = exact_routes.get(parsed.path)
        if route_handler:
            return route_handler()
        if parsed.path.startswith(TREND_DETAIL_PREFIX):
            return _handle_trend_detail(parsed.path)
        return _json_response({"error": "not found"}, status_code=404)
    except ValueError as error:
        return _json_response({"error": str(error)}, status_code=400)


def handle_post(path: str):
    try:
        post_routes = {
            TREND_GENERATE_PATH: lambda: _json_response(
                validate_generate_response_payload(generate_for_today(mode="simulated"))
            ),
        }
        route_handler = post_routes.get(path)
        if route_handler:
            return route_handler()
        return _json_response({"error": "not found"}, status_code=404)
    except ValueError as error:
        return _json_response({"error": str(error)}, status_code=400)

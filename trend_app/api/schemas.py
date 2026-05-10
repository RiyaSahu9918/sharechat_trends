from typing import Any, TypedDict


class TrendPostPayload(TypedDict):
    id: int
    trend_tag_id: int
    author_name: str
    content_text: str
    media_type: str
    media_url: str | None
    likes: int
    comments: int
    shares: int
    created_at: str


class TrendListItemPayload(TypedDict):
    id: int
    run_id: int
    tag: str
    title_hi: str
    description_hi: str
    category: str
    heat_score: float
    rank: int
    signal_source: str
    signal_volume: float
    spike_factor: float
    recency_score: float
    diversity_adjustment: float
    region: str
    language: str
    trend_date: str
    created_at: str


class TrendDetailPayload(TrendListItemPayload):
    posts: list[TrendPostPayload]
    summary_hi: str


class GenerateResponsePayload(TypedDict):
    message: str
    run_date: str


def _require_keys(payload: dict[str, Any], required: dict[str, type | tuple[type, ...]]) -> None:
    for key, expected_type in required.items():
        if key not in payload:
            raise ValueError(f"Missing key in payload: {key}")
        if not isinstance(payload[key], expected_type):
            raise ValueError(f"Invalid type for key '{key}'")


def validate_trends_list_payload(payload: Any) -> list[TrendListItemPayload]:
    if not isinstance(payload, list):
        raise ValueError("Trends payload should be a list")
    required = {
        "id": int,
        "tag": str,
        "title_hi": str,
        "description_hi": str,
        "category": str,
        "heat_score": (int, float),
        "rank": int,
        "signal_source": str,
    }
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("Trend item should be an object")
        _require_keys(item, required)
    return payload


def validate_trend_detail_payload(payload: Any) -> TrendDetailPayload:
    if not isinstance(payload, dict):
        raise ValueError("Trend detail payload should be an object")
    required = {
        "id": int,
        "tag": str,
        "title_hi": str,
        "description_hi": str,
        "category": str,
        "heat_score": (int, float),
        "posts": list,
        "summary_hi": str,
    }
    _require_keys(payload, required)
    for post in payload["posts"]:
        if not isinstance(post, dict):
            raise ValueError("Post should be an object")
        _require_keys(
            post,
            {
                "id": int,
                "author_name": str,
                "content_text": str,
                "likes": int,
                "comments": int,
                "shares": int,
            },
        )
    return payload


def validate_generate_response_payload(payload: Any) -> GenerateResponsePayload:
    if not isinstance(payload, dict):
        raise ValueError("Generate response should be an object")
    _require_keys(payload, {"message": str, "run_date": str})
    return payload

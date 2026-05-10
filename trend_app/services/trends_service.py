import random
import re
from datetime import date, datetime, timezone

from trend_app.constants import (
    LANGUAGE_HINDI,
    MAX_FINAL_TRENDS,
    REGION_INDIA,
    SOURCE_WEIGHTS,
    TOP_K_PER_CATEGORY,
    WEIGHT_DIVERSITY,
    WEIGHT_ENGAGEMENT,
    WEIGHT_RECENCY,
    WEIGHT_SPIKE,
)
from trend_app.data.seeds import POST_TEMPLATES, TOPIC_POOL
from trend_app.db.connection import get_connection
from trend_app.db.queries import (
    INSERT_TREND_POST,
    INSERT_TREND_RUN,
    INSERT_TREND_TAG,
    SELECT_LATEST_TRENDS,
    SELECT_POSTS_BY_TREND_ID,
    SELECT_TREND_BY_ID,
)


def _dedupe_key(tag: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\u0900-\u097F]+", "", tag.lower())


def _source_scores(rng: random.Random) -> dict[str, float]:
    return {
        "google_trends": rng.uniform(45, 100),
        "twitter": rng.uniform(35, 100),
        "youtube": rng.uniform(30, 98),
        "news": rng.uniform(30, 95),
        "social": rng.uniform(40, 99),
    }


def _weighted_source_score(scores: dict[str, float]) -> float:
    return sum(scores[source] * weight for source, weight in SOURCE_WEIGHTS.items())


def _dominant_sources(scores: dict[str, float]) -> str:
    top = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:3]
    return "+".join(source for source, _ in top)


def generate_for_today(mode: str = "simulated") -> dict:
    trend_date = date.today().isoformat()
    run_date = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    conn = get_connection()
    cur = conn.cursor()

    seed = int(datetime.now(timezone.utc).timestamp() * 1_000_000)
    rng = random.Random(seed)
    run_created = datetime.now(timezone.utc).isoformat()
    cur.execute(
        INSERT_TREND_RUN,
        (
            run_date,
            mode,
            "Refresh-based multi-source run with rich data.",
            run_created,
        ),
    )
    run_id = cur.lastrowid

    scored_candidates = []
    category_occurrence = {}
    
    # Shuffle to ensure varied subset if TOPIC_POOL is larger than what we process
    pool = list(TOPIC_POOL)
    rng.shuffle(pool)
    
    for item in pool:
        category = item["category"]
        category_occurrence[category] = category_occurrence.get(category, 0) + 1

        source_scores = _source_scores(rng)
        base_engagement = _weighted_source_score(source_scores)
        
        # New Rich Data Fields
        daily_active_users_clicks = rng.randint(1000, 150000)
        views = daily_active_users_clicks * rng.randint(2, 10)
        searches_in_last_30mins = rng.randint(50, 10000)
        users_from_multiple_sources = round(rng.uniform(0.1, 0.8), 2)
        trends_in_other_platforms = round(rng.uniform(10, 100), 2)
        new_vs_old_users = round(rng.uniform(0.1, 0.9), 2)
        mobile_os_type = rng.choice(["Android: 80%, iOS: 20%", "Android: 90%, iOS: 10%", "Android: 70%, iOS: 30%"])
        app_vs_web = round(rng.uniform(0.6, 0.99), 2)
        session_time_in_category = rng.randint(120, 1200)
        creators_in_category_recently = rng.randint(10, 800)
        nearby_location_trends = round(rng.uniform(0.0, 100.0), 2)
        gender = rng.choice(["Male: 60%, Female: 40%", "Male: 50%, Female: 50%", "Male: 70%, Female: 30%"])
        seasonal_event = 1 if category == "festivals" else 0
        occasion = "Festival" if seasonal_event else ""

        # Complex Heat Score Calculation incorporating new metrics
        spike = source_scores["twitter"]
        recency = rng.uniform(65, 100)
        diversity = max(0, 100 - (category_occurrence[category] - 1) * 15)
        
        # Normalize some metrics for scoring
        click_score = min(daily_active_users_clicks / 1500, 100)
        view_score = min(views / 15000, 100)
        search_score = min(searches_in_last_30mins / 100, 100)
        
        # New formula
        heat = round(
            0.20 * base_engagement +
            0.15 * spike +
            0.10 * recency +
            0.05 * diversity +
            0.15 * click_score +
            0.15 * view_score +
            0.10 * search_score +
            0.10 * trends_in_other_platforms,
            2,
        )

        scored_candidates.append(
            {
                **item,
                "engagement": base_engagement,
                "spike": spike,
                "recency": recency,
                "diversity": diversity,
                "heat": heat,
                "source_scores": source_scores,
                "daily_active_users_clicks": daily_active_users_clicks,
                "views": views,
                "searches_in_last_30mins": searches_in_last_30mins,
                "users_from_multiple_sources": users_from_multiple_sources,
                "trends_in_other_platforms": trends_in_other_platforms,
                "new_vs_old_users": new_vs_old_users,
                "mobile_os_type": mobile_os_type,
                "app_vs_web": app_vs_web,
                "session_time_in_category": session_time_in_category,
                "creators_in_category_recently": creators_in_category_recently,
                "nearby_location_trends": nearby_location_trends,
                "gender": gender,
                "seasonal_event": seasonal_event,
                "occasion": occasion
            }
        )

    deduped: dict[str, dict] = {}
    for row in sorted(scored_candidates, key=lambda x: x["heat"], reverse=True):
        key = _dedupe_key(row["tag"])
        if key not in deduped:
            deduped[key] = row

    guarded = []
    per_category_count: dict[str, int] = {}
    for row in sorted(deduped.values(), key=lambda x: x["heat"], reverse=True):
        category = row["category"]
        if per_category_count.get(category, 0) >= TOP_K_PER_CATEGORY:
            continue
        per_category_count[category] = per_category_count.get(category, 0) + 1
        guarded.append(row)

    ranked = sorted(guarded, key=lambda x: x["heat"], reverse=True)[:MAX_FINAL_TRENDS]
    now = datetime.now(timezone.utc).isoformat()

    for idx, row in enumerate(ranked, start=1):
        cur.execute(
            INSERT_TREND_TAG,
            (
                run_id,
                row["tag"],
                row["title_hi"],
                row["description_hi"],
                row["category"],
                row["heat"],
                idx,
                _dominant_sources(row["source_scores"]),
                round(row["engagement"], 2),
                round(row["spike"], 2),
                round(row["recency"], 2),
                round(row["diversity"], 2),
                REGION_INDIA,
                LANGUAGE_HINDI,
                trend_date,
                now,
                row["daily_active_users_clicks"],
                row["views"],
                row["searches_in_last_30mins"],
                row["users_from_multiple_sources"],
                row["trends_in_other_platforms"],
                row["new_vs_old_users"],
                row["mobile_os_type"],
                row["app_vs_web"],
                row["session_time_in_category"],
                row["creators_in_category_recently"],
                row["nearby_location_trends"],
                row["gender"],
                row["seasonal_event"],
                row["occasion"]
            ),
        )
        trend_tag_id = cur.lastrowid
        for i, template in enumerate(POST_TEMPLATES[:3]):  # Just generate 3 posts per trend
            cur.execute(
                INSERT_TREND_POST,
                (
                    trend_tag_id,
                    f"user_{idx}_{i + 1}",
                    template.format(title=row["title_hi"]),
                    "text",
                    None,
                    rng.randint(100, 5000),
                    rng.randint(20, 1500),
                    rng.randint(10, 1000),
                    now,
                ),
            )

    conn.commit()
    conn.close()
    return {"message": "generated", "run_date": run_date}


def latest_trends(limit: int = 10):
    conn = get_connection()
    rows = conn.execute(SELECT_LATEST_TRENDS, (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def trend_detail(trend_id: int):
    conn = get_connection()
    trend = conn.execute(SELECT_TREND_BY_ID, (trend_id,)).fetchone()
    if not trend:
        conn.close()
        return None
    posts = conn.execute(SELECT_POSTS_BY_TREND_ID, (trend_id,)).fetchall()
    conn.close()

    payload = dict(trend)
    payload["posts"] = [dict(post) for post in posts]
    
    # Enhanced summary block for the detail view
    payload["summary_hi"] = (
        f"{payload['title_hi']} इस समय टॉप ट्रेंड्स में से एक है। पिछले 30 मिनट में इसे {payload['searches_in_last_30mins']} बार सर्च किया गया "
        f"और {payload['views']} व्यूज मिले हैं। मुख्य रूप से {payload['mobile_os_type']} यूजर्स इसे देख रहे हैं। "
        f"इसका हीट स्कोर {payload['heat_score']} है!"
    )
    return payload


def ensure_seed_data() -> None:
    if not latest_trends(limit=1):
        generate_for_today()

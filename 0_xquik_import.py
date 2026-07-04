"""
Convert Xquik tweet exports into the Power BI sentiment pipeline dataset.

Usage:
    python 0_xquik_import.py xquik-export.json
    python 0_xquik_import.py xquik-export.csv --output data/labeled_tweets.csv
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)
analyzer = SentimentIntensityAnalyzer()

TOPIC_KEYWORDS = {
    "AI": ["chatgpt", "openai", "llm", "artificial intelligence", "machine learning"],
    "Climate": ["climate change", "global warming", "carbon", "renewable"],
    "Sports": ["champions league", "nba", "nfl", "transfer", "goal"],
    "Politics": ["election", "senate", "policy", "government", "vote"],
    "Crypto": ["bitcoin", "ethereum", "defi", "crypto", "blockchain"],
}


def load_xquik_export(path: Path) -> pd.DataFrame:
    """Load Xquik JSON, JSONL, or CSV exports into the Power BI row shape."""
    if path.suffix.lower() == ".csv":
        records = pd.read_csv(path).to_dict(orient="records")
    else:
        records = _load_json_records(path)

    rows = [_normalize_record(record) for record in records if isinstance(record, dict)]
    rows = [row for row in rows if row["text"]]
    return pd.DataFrame(rows)


def _load_json_records(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
        return _extract_records(payload)
    except json.JSONDecodeError:
        records = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            records.extend(_extract_records(json.loads(line)))
        return records


def _extract_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []

    for key in ("tweets", "results", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]

    data = payload.get("data")
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        return _extract_records(data)

    return []


def _normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    metrics = _nested(record, "public_metrics") or _nested(record, "metrics") or {}
    text = _first(record, ("text", "full_text", "content", "body")) or ""
    created_at = pd.to_datetime(
        _first(record, ("created_at", "createdAt", "timestamp", "time")),
        errors="coerce",
        utc=True,
    )
    if pd.isna(created_at):
        created_at = pd.Timestamp.utcnow()

    score = analyzer.polarity_scores(text)["compound"]
    sentiment = _sentiment_label(score)
    topic = _first(record, ("topic", "query", "keyword")) or _detect_topic(text)

    return {
        "tweet_id": _first(record, ("id", "tweet_id", "tweetId")) or "",
        "topic": topic,
        "text": text,
        "sentiment": sentiment,
        "vader_compound": score,
        "confidence": abs(score),
        "retweet_count": _first(metrics, ("retweet_count", "retweets", "reposts")) or 0,
        "like_count": _first(metrics, ("like_count", "likes", "favorites")) or 0,
        "word_count": len(text.split()),
        "created_at": created_at,
        "date": created_at.date(),
        "hour_of_day": created_at.hour,
        "day_of_week": created_at.strftime("%A"),
        "week": created_at.strftime("%Y-W%U"),
        "month": created_at.strftime("%Y-%m"),
    }


def _detect_topic(text: str) -> str:
    text_lower = text.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            return topic
    return "General"


def _sentiment_label(score: float) -> str:
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def _nested(source: dict[str, Any], key: str) -> dict[str, Any] | None:
    value = source.get(key)
    return value if isinstance(value, dict) else None


def _first(source: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        value = source.get(key)
        if value not in (None, ""):
            return value
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Xquik exports for Power BI.")
    parser.add_argument("input", type=Path, help="Xquik JSON, JSONL, or CSV export")
    parser.add_argument("--output", default="data/labeled_tweets.csv")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    df = load_xquik_export(args.input)
    if args.limit > 0:
        df = df.head(args.limit)

    os.makedirs(Path(args.output).parent, exist_ok=True)
    df.to_csv(args.output, index=False)
    log.info("Saved %s rows to %s", len(df), args.output)


if __name__ == "__main__":
    main()

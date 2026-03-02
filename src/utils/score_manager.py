import json
import os
import unicodedata
from datetime import datetime
from typing import List

_DEFAULT_SCORES = [
    ("REM", 520),
    ("RPK", 460),
    ("SEB", 390),
    ("JDG", 320),
    ("ADO", 260),
    ("EDO", 210),
    ("ENZ", 170),
    ("JUL", 130),
    ("IRI", 90),
    ("LIS", 60),
]


def _scores_path() -> str:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(root, "scores.json")


def _highscore_path() -> str:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(root, "highscore")


def _ensure_file() -> None:
    path = _scores_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            scores = data.get("scores", []) if isinstance(data, dict) else []
        except Exception:
            scores = []
        if isinstance(scores, list):
            _export_highscore(scores)
        return
    data = {
        "scores": [
            {"name": name, "score": score, "timestamp": "default"} for name, score in _DEFAULT_SCORES
        ]
    }
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    _export_highscore(data["scores"])


def load_scores() -> List[dict]:
    _ensure_file()
    path = _scores_path()
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        data = {"scores": []}
    scores = data.get("scores", [])
    if not isinstance(scores, list):
        return []
    cleaned = []
    for entry in scores:
        if not isinstance(entry, dict) or "score" not in entry:
            continue
        if "name" not in entry or not str(entry.get("name", "")).strip():
            entry["name"] = "Player"
        cleaned.append(entry)
    return cleaned


def save_scores(entries: List[dict]) -> None:
    path = _scores_path()
    data = {"scores": entries}
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    _export_highscore(entries)


def _normalize_arcade_name(name: str) -> str:
    normalized = unicodedata.normalize("NFD", str(name).strip().upper())
    ascii_only = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    filtered = "".join(ch for ch in ascii_only if ch.isalnum())
    return (filtered[:3] or "UNK")


def _export_highscore(entries: List[dict], limit: int = 10) -> None:
    path = _highscore_path()
    lines = []
    for entry in entries[:limit]:
        name = _normalize_arcade_name(entry.get("name", "UNK"))
        score = int(entry.get("score", 0))
        lines.append(f"{name}-{score}")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def add_score(score: int, name: str) -> None:
    entries = load_scores()
    trimmed_name = _normalize_arcade_name(name)
    entries.append({
        "name": trimmed_name,
        "score": int(score),
        "timestamp": datetime.now().isoformat(),
    })
    entries = sorted(entries, key=lambda item: int(item.get("score", 0)), reverse=True)
    save_scores(entries[:50])


def get_score_lines(limit: int = 10) -> List[str]:
    entries = load_scores()
    if not entries:
        return []
    lines = []
    for index, entry in enumerate(entries[:limit], start=1):
        name = str(entry.get("name", "Player"))
        score = int(entry.get("score", 0))
        lines.append(f"{index}. {name} - {score}")
    return lines

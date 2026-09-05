import argparse
import json
import os
import re
import statistics
import tempfile
from typing import Any, Dict, List, Optional

from yt_dlp import YoutubeDL
from content_analysis import analyze_transcript, analyze_visuals_from_url
from recommendations import generate_recommendations

YOUTUBE_ID_REGEX = re.compile(
    r"(?:(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtube\.com/shorts/|youtu\.be/))([A-Za-z0-9_-]{11})"
)


def is_youtube_url(url: str) -> bool:
    return bool(YOUTUBE_ID_REGEX.search(url))


def get_video_id(url: str) -> Optional[str]:
    match = YOUTUBE_ID_REGEX.search(url)
    return match.group(1) if match else None


def load_video_info(url: str) -> Dict[str, Any]:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "ignoreerrors": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    if not info:
        raise ValueError(f"Could not extract metadata for {url}")
    return info


def download_transcript(url: str, lang: str = "en") -> Optional[str]:
    with tempfile.TemporaryDirectory() as tempdir:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitlesformat": "json3",
            "subtitleslangs": [lang],
            "outtmpl": os.path.join(tempdir, "%(id)s"),
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
        video_id = info.get("id")
        if not video_id:
            return None
        found_files = [
            os.path.join(tempdir, name)
            for name in os.listdir(tempdir)
            if name.startswith(video_id) and name.endswith(".json3")
        ]
        if not found_files:
            return None
        transcript_path = found_files[0]
        with open(transcript_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        lines = []
        for event in data.get("events", []):
            pieces = event.get("segs") or []
            line = "".join(piece.get("utf8", "") for piece in pieces).strip()
            if line:
                lines.append(line)
        return "\n".join(lines).strip()


def summarize_text(text: str) -> Dict[str, Any]:
    words = re.findall(r"\w+", text)
    word_count = len(words)
    sentence_count = max(len(re.findall(r"[.!?]+", text)), 1)
    avg_words = word_count / sentence_count if sentence_count else word_count
    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "average_words_per_sentence": round(avg_words, 1),
    }


def safe_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def bool_to_yesno(value: Any) -> str:
    return "Yes" if value else "No"


def compute_insights(info: Dict[str, Any], transcript: Optional[str]) -> Dict[str, Any]:
    duration = safe_int(info.get("duration"))
    view_count = safe_int(info.get("view_count"))
    like_count = safe_int(info.get("like_count"))
    tags = info.get("tags") or []
    chap = info.get("chapters") or []
    transcript_summary = summarize_text(transcript) if transcript else None
    words_per_minute = None
    if transcript_summary and duration:
        words_per_minute = round((transcript_summary["word_count"] / duration) * 60, 1)
    engagement_ratio = None
    if like_count is not None and view_count:
        engagement_ratio = round(like_count / view_count, 4)
    style_notes: List[str] = []
    if duration:
        style_notes.append(
            "This video is longform." if duration >= 900 else "This video is short-form friendly."
        )
    if info.get("is_live"):
        style_notes.append("Live or event-style format detected.")
    if tags:
        style_notes.append(f"This video uses {len(tags)} tag(s), which can help reach niche searches.")
    if chap:
        style_notes.append("This video includes chapters, which is useful for tutorial/navigation.")
    if transcript_summary:
        if transcript_summary["average_words_per_sentence"] > 20:
            style_notes.append("The spoken-word text suggests a dense, informational delivery.")
        if words_per_minute and words_per_minute > 180:
            style_notes.append("The speech pacing is fast; consider shorter clips or slower delivery.")
    return {
        "duration_seconds": duration,
        "view_count": view_count,
        "like_count": like_count,
        "engagement_ratio": engagement_ratio,
        "has_chapters": bool(chap),
        "chapter_count": len(chap),
        "tag_count": len(tags),
        "transcript_metrics": transcript_summary,
        "words_per_minute": words_per_minute,
        "style_notes": style_notes,
    }


def build_report(
    info: Dict[str, Any],
    transcript: Optional[str],
    content_analysis: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    metadata = {
        "id": info.get("id"),
        "title": info.get("title"),
        "uploader": info.get("uploader"),
        "upload_date": info.get("upload_date"),
        "duration_seconds": safe_int(info.get("duration")),
        "view_count": safe_int(info.get("view_count")),
        "like_count": safe_int(info.get("like_count")),
        "average_rating": info.get("average_rating"),
        "description": info.get("description"),
        "thumbnail": info.get("thumbnail"),
        "tags": info.get("tags"),
        "categories": info.get("categories"),
        "is_live": bool(info.get("is_live")),
    }
    insights = compute_insights(info, transcript)
    report = {
        "source_url": info.get("webpage_url"),
        "metadata": metadata,
        "insights": insights,
        "content_analysis": content_analysis or {},
        "transcript_excerpt": transcript[:2000] if transcript else None,
    }
    report["recommendations"] = generate_recommendations(report)
    return report


def analyze_youtube(url: str, caption_lang: str = "en") -> Dict[str, Any]:
    if not is_youtube_url(url):
        raise ValueError("Please enter a valid YouTube video URL.")
    print(f"Extracting video metadata for {url}...")
    info = load_video_info(url)
    transcript = None
    try:
        transcript = download_transcript(url, lang=caption_lang)
    except Exception:
        transcript = None
    content_analysis = {
        "transcript": analyze_transcript(transcript, safe_int(info.get("duration"))),
        "visuals": analyze_visuals_from_url(url, thumbnail_url=info.get("thumbnail")),
    }
    report = build_report(info, transcript, content_analysis=content_analysis)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a YouTube video and produce a JSON report.")
    parser.add_argument("--url", required=True, help="YouTube video URL to analyze.")
    parser.add_argument("--caption-lang", default="en", help="Spoken language code to request when fetching transcript text.")
    parser.add_argument("--output", help="Optional output JSON file.")
    args = parser.parse_args()
    report = analyze_youtube(args.url, caption_lang=args.caption_lang)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as outfile:
            json.dump(report, outfile, indent=2, ensure_ascii=False)
        print(f"Saved report to {args.output}")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

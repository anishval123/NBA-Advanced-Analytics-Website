import re
from typing import Any, Dict, List, Optional


POWER_WORDS = {
    "best",
    "worst",
    "mistakes",
    "secret",
    "proven",
    "simple",
    "easy",
    "fast",
    "ultimate",
    "complete",
    "beginner",
    "guide",
    "review",
    "ranking",
    "truth",
    "why",
    "how",
}

CTA_WORDS = {
    "subscribe",
    "comment",
    "like",
    "share",
    "watch next",
    "check out",
    "link below",
    "download",
    "join",
    "follow",
}


def _words(text: Optional[str]) -> List[str]:
    if not text:
        return []
    return re.findall(r"[A-Za-z0-9']+", text.lower())


def _score_from_penalties(start: int, penalties: List[int]) -> int:
    return max(0, min(100, start - sum(penalties)))


def _title_score(title: str) -> Dict[str, Any]:
    title_words = _words(title)
    penalties = []
    positives = []
    fixes = []

    if len(title) < 35:
        penalties.append(15)
        fixes.append("Make the title more specific. Name the viewer, outcome, or tension.")
    elif len(title) > 80:
        penalties.append(15)
        fixes.append("Shorten the title so the main promise is visible in search and suggested videos.")
    else:
        positives.append("Title length is in a strong range for readability.")

    if not any(word in POWER_WORDS for word in title_words):
        penalties.append(10)
        fixes.append("Add a clearer curiosity or outcome word, such as 'why', 'how', 'best', or 'mistakes'.")
    else:
        positives.append("Title has at least one useful curiosity or outcome cue.")

    if len(set(title_words)) < max(4, len(title_words) * 0.65):
        penalties.append(8)
        fixes.append("Remove repeated words from the title.")

    return {
        "name": "Title",
        "score": _score_from_penalties(100, penalties),
        "positives": positives,
        "fixes": fixes,
    }


def _description_score(description: str) -> Dict[str, Any]:
    words = _words(description)
    penalties = []
    positives = []
    fixes = []

    if len(words) < 50:
        penalties.append(25)
        fixes.append("Expand the description with a short summary, key topics, and links to the next action.")
    else:
        positives.append("Description has enough text for context and search relevance.")

    if "http://" not in description and "https://" not in description:
        penalties.append(10)
        fixes.append("Add one useful link, such as a related video, newsletter, product, or resource.")

    if not any(word in CTA_WORDS for word in description.lower().split()):
        penalties.append(10)
        fixes.append("Add a clear call to action in the description.")

    return {
        "name": "Description",
        "score": _score_from_penalties(100, penalties),
        "positives": positives,
        "fixes": fixes,
    }


def _structure_score(report: Dict[str, Any]) -> Dict[str, Any]:
    insights = report.get("insights", {})
    duration = insights.get("duration_seconds") or 0
    has_chapters = insights.get("has_chapters")
    tag_count = insights.get("tag_count") or 0
    transcript = report.get("transcript_excerpt") or ""
    transcript_words = _words(transcript)
    first_words = " ".join(transcript_words[:80])
    penalties = []
    positives = []
    fixes = []

    if duration >= 600 and not has_chapters:
        penalties.append(20)
        fixes.append("Add chapters because the video is long enough that viewers need navigation.")
    elif has_chapters:
        positives.append("Chapters are present, which helps viewers jump to the right section.")

    if tag_count == 0:
        penalties.append(12)
        fixes.append("Add a focused set of tags for names, topics, and niche search terms.")
    elif tag_count < 5:
        penalties.append(6)
        fixes.append("Add a few more targeted tags around the main topic.")
    else:
        positives.append("Tags are present.")

    if transcript:
        if not any(word in first_words for word in ("today", "why", "how", "here", "learn", "show", "mistake", "problem")):
            penalties.append(14)
            fixes.append("Strengthen the first 30 seconds with a clearer promise, problem, or payoff.")
        else:
            positives.append("The opening words appear to introduce a topic or promise.")
    else:
        penalties.append(8)
        fixes.append("The app could not access the spoken words, so hook and pacing advice is limited.")

    return {
        "name": "Structure",
        "score": _score_from_penalties(100, penalties),
        "positives": positives,
        "fixes": fixes,
    }


def _pacing_score(report: Dict[str, Any]) -> Dict[str, Any]:
    insights = report.get("insights", {})
    wpm = insights.get("words_per_minute")
    transcript_metrics = insights.get("transcript_metrics") or {}
    avg_sentence = transcript_metrics.get("average_words_per_sentence")
    penalties = []
    positives = []
    fixes = []

    if wpm is None:
        penalties.append(15)
        fixes.append("Spoken pacing could not be measured because the video's words were unavailable.")
    elif wpm < 115:
        penalties.append(15)
        fixes.append("The spoken pace seems slow. Tighten pauses or add more visual changes in slower sections.")
    elif wpm > 185:
        penalties.append(12)
        fixes.append("The spoken pace seems fast. Use on-screen emphasis, pattern breaks, and clearer section breaks.")
    else:
        positives.append("Speech pace is in a comfortable range.")

    if avg_sentence and avg_sentence > 22:
        penalties.append(10)
        fixes.append("Break long ideas into shorter sentences so the video feels easier to follow.")
    elif avg_sentence:
        positives.append("Sentence length looks readable.")

    return {
        "name": "Pacing",
        "score": _score_from_penalties(100, penalties),
        "positives": positives,
        "fixes": fixes,
    }


def _engagement_score(report: Dict[str, Any]) -> Dict[str, Any]:
    insights = report.get("insights", {})
    metadata = report.get("metadata", {})
    engagement_ratio = insights.get("engagement_ratio")
    transcript = (report.get("transcript_excerpt") or "").lower()
    penalties = []
    positives = []
    fixes = []

    if engagement_ratio is None:
        penalties.append(8)
        fixes.append("Like or view data was unavailable, so compare this video against your channel average manually.")
    elif engagement_ratio < 0.015:
        penalties.append(18)
        fixes.append("Engagement looks low. Ask a more specific question and give viewers a reason to comment.")
    elif engagement_ratio >= 0.04:
        positives.append("Like-to-view ratio looks strong.")
    else:
        positives.append("Engagement is usable, but there is room to create more audience response.")

    searchable_text = " ".join(
        [
            metadata.get("title") or "",
            metadata.get("description") or "",
            transcript,
        ]
    ).lower()
    if not any(phrase in searchable_text for phrase in CTA_WORDS):
        penalties.append(12)
        fixes.append("Add one clear call to action in the video or description.")
    else:
        positives.append("A call-to-action phrase appears in the video text or description.")

    return {
        "name": "Engagement",
        "score": _score_from_penalties(100, penalties),
        "positives": positives,
        "fixes": fixes,
    }


def _hook_score(report: Dict[str, Any]) -> Dict[str, Any]:
    transcript = (report.get("content_analysis", {}).get("transcript") or {})
    if not transcript.get("available"):
        return {
            "name": "Hook",
            "score": 70,
            "positives": [],
            "fixes": transcript.get("fixes") or ["Spoken-word access was unavailable, so hook analysis is limited."],
        }

    fixes = []
    positives = list(transcript.get("signals") or [])
    for fix in transcript.get("fixes") or []:
        if "opening" in fix.lower() or "intro" in fix.lower() or "first 15" in fix.lower():
            fixes.append(fix)

    if not fixes:
        positives.append("The opening words have enough signal to understand what the video is about.")

    return {
        "name": "Hook",
        "score": transcript.get("hook_score") or 0,
        "positives": positives,
        "fixes": fixes,
    }


def _script_score(report: Dict[str, Any]) -> Dict[str, Any]:
    transcript = (report.get("content_analysis", {}).get("transcript") or {})
    if not transcript.get("available"):
        return {
            "name": "Script",
            "score": 70,
            "positives": [],
            "fixes": transcript.get("fixes") or ["Spoken-word access was unavailable, so script analysis is limited."],
        }

    fixes = []
    positives = list(transcript.get("signals") or [])
    for fix in transcript.get("fixes") or []:
        if not ("opening" in fix.lower() or "intro" in fix.lower() or "first 15" in fix.lower()):
            fixes.append(fix)

    if not fixes:
        positives.append("The spoken-word text does not show major pacing or repetition problems.")

    return {
        "name": "Script",
        "score": transcript.get("script_score") or 0,
        "positives": positives,
        "fixes": fixes,
    }


def _visual_score(report: Dict[str, Any]) -> Dict[str, Any]:
    visuals = (report.get("content_analysis", {}).get("visuals") or {})
    if not visuals.get("available"):
        return {
            "name": "Visuals",
            "score": 70,
            "positives": [],
            "fixes": visuals.get("fixes") or ["Visual analysis was unavailable."],
        }

    positives = list(visuals.get("signals") or [])
    fixes = list(visuals.get("fixes") or [])
    if not fixes:
        positives.append("Sampled frames do not show major brightness, contrast, or visual-variety issues.")

    # Enhanced visual recommendations
    color_palette = visuals.get("color_palette")
    if color_palette:
        if color_palette[0].get("saturation") == "vibrant":
            positives.append("Color palette is vibrant and eye-catching.")
        else:
            fixes.append("Consider using more vibrant colors to increase visual appeal.")
        
        if color_palette[0].get("lightness") == "dark":
            fixes.append("The overall palette is dark. Consider adding brighter elements for better visibility.")

    composition = visuals.get("composition")
    if composition:
        if composition.get("rule_of_thirds_score", 0) > 60:
            positives.append("Composition follows the rule of thirds well.")
        elif composition.get("rule_of_thirds_score", 0) < 40:
            fixes.append("Consider using the rule of thirds for more dynamic composition.")
        
        if composition.get("text_overlay_frequency", 0) < 10:
            fixes.append("Consider adding text overlays or graphics to emphasize key points.")
        elif composition.get("text_overlay_frequency", 0) > 50:
            positives.append("Good use of text overlays for emphasis.")

    scene_analysis = visuals.get("scene_analysis")
    if scene_analysis:
        scene_types = scene_analysis.get("scene_types", {})
        if len(scene_types) <= 2:
            fixes.append("Scene variety is limited. Mix different shot types and angles.")
        elif len(scene_types) >= 4:
            positives.append("Good scene variety keeps viewers engaged.")

    return {
        "name": "Visuals",
        "score": visuals.get("visual_score") or 0,
        "positives": positives,
        "fixes": fixes,
    }


def _priority(scorecard: List[Dict[str, Any]]) -> List[str]:
    actions = []
    for section in sorted(scorecard, key=lambda item: item["score"]):
        actions.extend(section["fixes"])
    return actions[:5]


def generate_recommendations(report: Dict[str, Any]) -> Dict[str, Any]:
    metadata = report.get("metadata", {})
    title = metadata.get("title") or ""
    description = metadata.get("description") or ""

    scorecard = [
        _title_score(title),
        _description_score(description),
        _hook_score(report),
        _script_score(report),
        _visual_score(report),
        _structure_score(report),
        _pacing_score(report),
        _engagement_score(report),
    ]
    overall = round(sum(section["score"] for section in scorecard) / len(scorecard))

    return {
        "overall_score": overall,
        "grade": _grade(overall),
        "top_actions": _priority(scorecard),
        "scorecard": scorecard,
    }


def _grade(score: int) -> str:
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Strong"
    if score >= 60:
        return "Needs work"
    return "High priority"

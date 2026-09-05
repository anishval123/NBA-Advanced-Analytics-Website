import colorsys
import math
import os
import re
import tempfile
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import requests
from PIL import Image
from moviepy.editor import VideoFileClip
from yt_dlp import YoutubeDL


HOOK_WORDS = {
    "why",
    "how",
    "today",
    "here",
    "problem",
    "mistake",
    "secret",
    "best",
    "worst",
    "learn",
    "show",
    "because",
    "actually",
}

FILLER_WORDS = {
    "um",
    "uh",
    "like",
    "basically",
    "literally",
    "actually",
    "kind of",
    "sort of",
    "you know",
}


def _words(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9']+", text.lower())


def _sentences(text: str) -> List[str]:
    return [part.strip() for part in re.split(r"[.!?]+", text) if part.strip()]


def analyze_transcript(transcript: Optional[str], duration_seconds: Optional[int]) -> Dict[str, Any]:
    if not transcript:
        return {
            "available": False,
            "hook_score": None,
            "script_score": None,
            "source": None,
            "signals": [],
            "fixes": ["Spoken-word analysis is unavailable because the app could not access what was said. Audio transcription is the right next upgrade for videos without public transcript text."],
        }

    words = _words(transcript)
    first_80_words = words[:80]
    first_30_text = " ".join(first_80_words)
    word_count = len(words)
    sentences = _sentences(transcript)
    unique_ratio = round(len(set(words)) / word_count, 2) if word_count else 0
    filler_count = _count_fillers(transcript)
    filler_rate = round((filler_count / word_count) * 100, 2) if word_count else 0
    words_per_minute = None
    if duration_seconds:
        words_per_minute = round((word_count / duration_seconds) * 60, 1)

    hook_penalties = []
    script_penalties = []
    signals = []
    fixes = []

    if not any(word in HOOK_WORDS for word in first_80_words):
        hook_penalties.append(25)
        fixes.append("The opening does not clearly signal a promise, problem, or payoff. Put the main reason to watch in the first 15 seconds.")
    else:
        signals.append("Opening language contains a promise, topic, or curiosity cue.")

    if len(first_80_words) < 45:
        hook_penalties.append(10)
        fixes.append("The intro appears light on spoken setup. Add one crisp sentence that tells viewers what they will get.")

    if words_per_minute is not None:
        if words_per_minute < 115:
            script_penalties.append(15)
            fixes.append("Speech pacing looks slow. Tighten pauses or add stronger visual pattern breaks.")
        elif words_per_minute > 185:
            script_penalties.append(12)
            fixes.append("Speech pacing looks fast. Add on-screen emphasis, section breaks, or simpler phrasing.")
        else:
            signals.append("Speech pacing is in a comfortable range.")

    if sentences:
        avg_sentence_words = round(word_count / len(sentences), 1)
        if avg_sentence_words > 22:
            script_penalties.append(12)
            fixes.append("Sentences run long. Break dense explanations into shorter beats.")
        else:
            signals.append("Sentence length is easy to follow.")
    else:
        avg_sentence_words = None

    if filler_rate > 3:
        script_penalties.append(10)
        fixes.append("Filler language is noticeable. Cut hesitant phrases and repeated setup.")

    if unique_ratio < 0.34 and word_count > 250:
        script_penalties.append(8)
        fixes.append("The spoken-word text looks repetitive. Trim repeated points or turn them into faster examples.")

    return {
        "available": True,
        "source": "youtube_transcript",
        "hook_score": max(0, 100 - sum(hook_penalties)),
        "script_score": max(0, 100 - sum(script_penalties)),
        "word_count": word_count,
        "words_per_minute": words_per_minute,
        "average_sentence_words": avg_sentence_words,
        "filler_count": filler_count,
        "filler_rate_percent": filler_rate,
        "unique_word_ratio": unique_ratio,
        "opening_excerpt": " ".join(transcript.split()[:90]),
        "signals": signals,
        "fixes": fixes,
    }


def _count_fillers(text: str) -> int:
    lowered = text.lower()
    total = 0
    for filler in FILLER_WORDS:
        if " " in filler:
            total += len(re.findall(rf"\b{re.escape(filler)}\b", lowered))
        else:
            total += len(re.findall(rf"\b{re.escape(filler)}\b", lowered))
    return total


def download_preview_video(url: str, tempdir: str) -> Optional[str]:
    output_template = os.path.join(tempdir, "%(id)s.%(ext)s")
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best[height<=360][ext=mp4][vcodec!=none]/worst[ext=mp4][vcodec!=none]/worst[vcodec!=none]",
        "outtmpl": output_template,
        "noplaylist": True,
        "merge_output_format": "mp4",
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    video_id = info.get("id")
    if not video_id:
        return None
    for name in os.listdir(tempdir):
        if name.startswith(video_id):
            return os.path.join(tempdir, name)
    return None


def analyze_visuals_from_url(url: str, thumbnail_url: Optional[str] = None, max_samples: int = 24) -> Dict[str, Any]:
    video_error = None
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            video_path = download_preview_video(url, tempdir)
            if not video_path:
                video_error = "Could not download a preview video for visual analysis."
            else:
                # Try enhanced analysis first, fall back to basic
                try:
                    return analyze_visuals_enhanced(video_path, max_samples=max_samples)
                except Exception as enhanced_exc:
                    video_error = f"Enhanced analysis failed: {enhanced_exc}"
                    return analyze_visuals(video_path, max_samples=max_samples)
    except Exception as exc:
        video_error = f"Video frame sampling failed: {exc}"

    if thumbnail_url:
        thumbnail_result = analyze_thumbnail(thumbnail_url)
        if thumbnail_result.get("available"):
            thumbnail_result["fixes"].insert(
                0,
                "Full video frame sampling failed, so visual analysis used the thumbnail as a fallback.",
            )
            thumbnail_result["fallback_reason"] = video_error
            return thumbnail_result

    return _visual_unavailable(video_error or "Visual analysis failed.")


def analyze_thumbnail(thumbnail_url: str) -> Dict[str, Any]:
    temp_path = None
    try:
        response = requests.get(thumbnail_url, timeout=12)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as handle:
            handle.write(response.content)
            temp_path = handle.name
        return analyze_image(temp_path)
    except Exception as exc:
        return _visual_unavailable(f"Thumbnail fallback failed: {exc}")
    finally:
        if temp_path:
            try:
                os.remove(temp_path)
            except OSError:
                pass


def analyze_image(image_path: str) -> Dict[str, Any]:
    image = Image.open(image_path).convert("RGB")
    frame = np.array(image)
    small = frame[:: max(1, frame.shape[0] // 180), :: max(1, frame.shape[1] // 320), :3]
    gray = (
        0.299 * small[:, :, 0]
        + 0.587 * small[:, :, 1]
        + 0.114 * small[:, :, 2]
    )
    avg_brightness = round(float(np.mean(gray)), 1)
    avg_contrast = round(float(np.std(gray)), 1)
    penalties = []
    fixes = []
    signals = []

    if avg_brightness < 55:
        penalties.append(15)
        fixes.append("The thumbnail/frame sample is dark. Increase exposure or use a brighter image.")
    elif avg_brightness > 215:
        penalties.append(10)
        fixes.append("The thumbnail/frame sample is very bright. Check exposure so detail is not washed out.")
    else:
        signals.append("Thumbnail brightness looks usable.")

    if avg_contrast < 35:
        penalties.append(15)
        fixes.append("Thumbnail contrast is low. Use stronger separation between subject, text, and background.")
    else:
        signals.append("Thumbnail contrast looks readable.")

    return {
        "available": True,
        "source": "thumbnail",
        "visual_score": max(0, 100 - sum(penalties)),
        "sample_count": 1,
        "average_brightness": avg_brightness,
        "average_contrast": avg_contrast,
        "average_frame_change": None,
        "visual_change_rate": None,
        "sampled_frames": [{"time": None, "brightness": avg_brightness, "contrast": avg_contrast}],
        "signals": signals,
        "fixes": fixes,
    }


def analyze_visuals(video_path: str, max_samples: int = 24) -> Dict[str, Any]:
    with VideoFileClip(video_path) as clip:
        duration = clip.duration or 0
        if duration <= 0:
            return _visual_unavailable("Video duration was unavailable.")

        sample_count = min(max_samples, max(4, math.ceil(duration / 8)))
        times = np.linspace(0.5, max(0.5, duration - 0.5), sample_count)
        stats = []
        previous_small = None
        frame_changes = []

        for timestamp in times:
            frame = clip.get_frame(float(timestamp))
            small = frame[:: max(1, frame.shape[0] // 90), :: max(1, frame.shape[1] // 160), :3]
            gray = (
                0.299 * small[:, :, 0]
                + 0.587 * small[:, :, 1]
                + 0.114 * small[:, :, 2]
            )
            brightness = float(np.mean(gray))
            contrast = float(np.std(gray))
            stats.append({"time": round(float(timestamp), 1), "brightness": round(brightness, 1), "contrast": round(contrast, 1)})
            if previous_small is not None:
                diff = float(np.mean(np.abs(small.astype(float) - previous_small.astype(float))))
                frame_changes.append(diff)
            previous_small = small

    avg_brightness = round(float(np.mean([item["brightness"] for item in stats])), 1)
    avg_contrast = round(float(np.mean([item["contrast"] for item in stats])), 1)
    avg_frame_change = round(float(np.mean(frame_changes)), 1) if frame_changes else None
    high_change_count = sum(1 for value in frame_changes if value >= 28)
    change_rate = round(high_change_count / len(frame_changes), 2) if frame_changes else None

    penalties = []
    fixes = []
    signals = []

    if avg_brightness < 55:
        penalties.append(15)
        fixes.append("The sampled frames are dark. Increase exposure or use brighter footage for clearer viewing.")
    elif avg_brightness > 215:
        penalties.append(10)
        fixes.append("The sampled frames are very bright. Check exposure so detail is not washed out.")
    else:
        signals.append("Average brightness looks usable.")

    if avg_contrast < 35:
        penalties.append(15)
        fixes.append("Visual contrast is low. Add better lighting, sharper graphics, or higher-contrast edits.")
    else:
        signals.append("Average contrast looks readable.")

    if change_rate is not None:
        if change_rate < 0.18:
            penalties.append(20)
            fixes.append("Visual variety looks low. Add cuts, zooms, B-roll, graphics, or screen changes every few seconds.")
        elif change_rate > 0.75:
            penalties.append(8)
            fixes.append("The video changes visuals very often. Make sure the cuts do not distract from the point.")
        else:
            signals.append("Visual change rate looks healthy.")

    return {
        "available": True,
        "source": "video_frames",
        "visual_score": max(0, 100 - sum(penalties)),
        "sample_count": len(stats),
        "average_brightness": avg_brightness,
        "average_contrast": avg_contrast,
        "average_frame_change": avg_frame_change,
        "visual_change_rate": change_rate,
        "sampled_frames": stats,
        "signals": signals,
        "fixes": fixes,
    }


def _visual_unavailable(reason: str) -> Dict[str, Any]:
    return {
        "available": False,
        "source": None,
        "visual_score": None,
        "visual_change_rate": None,
        "signals": [],
        "fixes": [reason],
    }


def _extract_color_palette(frame: np.ndarray, n_colors: int = 5) -> List[Dict[str, Any]]:
    """Extract dominant colors from a frame using simple quantization."""
    small = frame[:: max(1, frame.shape[0] // 60), :: max(1, frame.shape[1] // 80), :3]
    pixels = small.reshape(-1, 3)
    
    # Simple color quantization using k-means-like approach
    from sklearn.cluster import KMeans
    try:
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_
        counts = np.bincount(labels)
        
        palette = []
        for i, (color, count) in enumerate(sorted(zip(colors, counts), key=lambda x: x[1], reverse=True)):
            r, g, b = color
            h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
            palette.append({
                "rgb": f"rgb({r}, {g}, {b})",
                "hex": f"#{r:02x}{g:02x}{b:02x}",
                "percentage": round(count / len(pixels) * 100, 1),
                "hue": "warm" if h < 0.15 or h > 0.85 else ("cool" if 0.5 < h < 0.75 else "neutral"),
                "saturation": "vibrant" if s > 0.5 else "muted",
                "lightness": "light" if l > 0.6 else ("dark" if l < 0.4 else "medium"),
            })
        return palette
    except ImportError:
        # Fallback if sklearn not available
        return _simple_color_quantization(pixels, n_colors)


def _simple_color_quantization(pixels: np.ndarray, n_colors: int) -> List[Dict[str, Any]]:
    """Fallback color quantization without sklearn."""
    # Reduce to basic color buckets
    buckets = {}
    for pixel in pixels:
        r, g, b = pixel
        # Quantize to 32 levels
        r_bucket = (r // 32) * 32
        g_bucket = (g // 32) * 32
        b_bucket = (b // 32) * 32
        key = (r_bucket, g_bucket, b_bucket)
        buckets[key] = buckets.get(key, 0) + 1
    
    # Get top colors
    top_colors = sorted(buckets.items(), key=lambda x: x[1], reverse=True)[:n_colors]
    palette = []
    total = sum(buckets.values())
    
    for (r, g, b), count in top_colors:
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        palette.append({
            "rgb": f"rgb({r}, {g}, {b})",
            "hex": f"#{r:02x}{g:02x}{b:02x}",
            "percentage": round(count / total * 100, 1),
            "hue": "warm" if h < 0.15 or h > 0.85 else ("cool" if 0.5 < h < 0.75 else "neutral"),
            "saturation": "vibrant" if s > 0.5 else "muted",
            "lightness": "light" if l > 0.6 else ("dark" if l < 0.4 else "medium"),
        })
    return palette


def _detect_text_overlay(frame: np.ndarray) -> Dict[str, Any]:
    """Detect potential text overlays using edge detection and contrast analysis."""
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) if len(frame.shape) == 3 else frame
    
    # Apply adaptive thresholding to find text-like regions
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Find contours that might be text
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    text_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h) if h > 0 else 0
        area = w * h
        frame_area = frame.shape[0] * frame.shape[1]
        
        # Text typically has specific aspect ratios and sizes
        if 0.1 < aspect_ratio < 15 and 0.001 < area / frame_area < 0.3:
            text_regions.append({
                "position": "top" if y < frame.shape[0] * 0.3 else ("bottom" if y > frame.shape[0] * 0.7 else "middle"),
                "size": "large" if area / frame_area > 0.05 else "small",
                "aspect_ratio": round(aspect_ratio, 2),
            })
    
    has_text = len(text_regions) > 0
    return {
        "has_text_overlay": has_text,
        "text_regions": text_regions[:5],  # Limit to top 5
        "text_density": round(len(text_regions) / 10, 2),  # Normalized density
    }


def _analyze_composition(frame: np.ndarray) -> Dict[str, Any]:
    """Analyze basic composition rules (rule of thirds, symmetry)."""
    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) if len(frame.shape) == 3 else frame
    
    # Divide frame into 3x3 grid (rule of thirds)
    third_h, third_w = h // 3, w // 3
    
    # Calculate edge strength in each region
    edges = cv2.Canny(gray, 100, 200)
    grid_strength = []
    
    for i in range(3):
        for j in range(3):
            region = edges[i*third_h:(i+1)*third_h, j*third_w:(j+1)*third_w]
            strength = np.mean(region) / 255.0
            grid_strength.append(strength)
    
    # Check if strong elements align with rule of thirds
    corner_strength = (grid_strength[0] + grid_strength[2] + grid_strength[6] + grid_strength[8]) / 4
    center_strength = grid_strength[4]
    rule_of_thirds_score = round(corner_strength / (center_strength + 0.1) * 50, 1)
    
    # Check symmetry
    left_half = gray[:, :w//2]
    right_half = np.fliplr(gray[:, w//2:])
    symmetry_score = round(np.mean(np.abs(left_half.astype(float) - right_half.astype(float))) / 255 * 100, 1)
    
    return {
        "rule_of_thirds_score": min(100, rule_of_thirds_score),
        "symmetry_score": round(100 - symmetry_score, 1),  # Higher = more symmetric
        "composition_type": "balanced" if rule_of_thirds_score > 60 else "centered" if symmetry_score > 70 else "dynamic",
    }


def _detect_scene_type(frame: np.ndarray) -> str:
    """Detect basic scene type from frame characteristics."""
    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) if len(frame.shape) == 3 else frame
    
    # Calculate features
    brightness = np.mean(gray)
    contrast = np.std(gray)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.mean(edges) / 255
    
    # Simple scene classification
    if edge_density > 0.3 and contrast > 50:
        return "action"  # High motion/complexity
    elif brightness > 180 and contrast < 40:
        return "flat"  # Bright, low contrast (talking head, screen recording)
    elif brightness < 80:
        return "dark"  # Dark scene
    elif edge_density < 0.1:
        return "static"  # Low motion
    else:
        return "standard"


def analyze_visuals_enhanced(video_path: str, max_samples: int = 24) -> Dict[str, Any]:
    """Enhanced visual analysis with color, text, and composition detection."""
    try:
        import cv2
    except ImportError:
        return {
            "available": False,
            "error": "OpenCV not installed. Install with: pip install opencv-python",
            "visual_score": None,
            "signals": [],
            "fixes": ["Enhanced visual analysis requires OpenCV."],
        }
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return _visual_unavailable("Could not open video file.")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    if duration <= 0:
        cap.release()
        return _visual_unavailable("Video duration was unavailable.")
    
    # Sample frames
    sample_count = min(max_samples, max(4, math.ceil(duration / 8)))
    frame_indices = np.linspace(0, total_frames - 1, sample_count, dtype=int)
    
    all_palettes = []
    all_compositions = []
    all_text_detections = []
    scene_types = []
    frame_stats = []
    previous_frame = None
    frame_changes = []
    
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        
        timestamp = idx / fps if fps > 0 else 0
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Basic stats
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = round(float(np.mean(gray)), 1)
        contrast = round(float(np.std(gray)), 1)
        
        frame_stats.append({
            "time": round(timestamp, 1),
            "brightness": brightness,
            "contrast": contrast,
        })
        
        # Enhanced analysis
        palette = _extract_color_palette(rgb_frame)
        all_palettes.append(palette)
        
        composition = _analyze_composition(rgb_frame)
        all_compositions.append(composition)
        
        text_detection = _detect_text_overlay(frame)
        all_text_detections.append(text_detection)
        
        scene_type = _detect_scene_type(rgb_frame)
        scene_types.append(scene_type)
        
        # Frame change detection
        if previous_frame is not None:
            diff = np.mean(np.abs(rgb_frame.astype(float) - previous_frame.astype(float)))
            frame_changes.append(float(diff))
        previous_frame = rgb_frame
    
    cap.release()
    
    # Aggregate results
    avg_brightness = round(float(np.mean([s["brightness"] for s in frame_stats])), 1)
    avg_contrast = round(float(np.mean([s["contrast"] for s in frame_stats])), 1)
    avg_frame_change = round(float(np.mean(frame_changes)), 1) if frame_changes else None
    high_change_count = sum(1 for v in frame_changes if v >= 28)
    change_rate = round(high_change_count / len(frame_changes), 2) if frame_changes else None
    
    # Aggregate color palette
    combined_palette = _combine_palettes(all_palettes)
    
    # Aggregate composition scores
    avg_rule_of_thirds = round(float(np.mean([c["rule_of_thirds_score"] for c in all_compositions])), 1)
    avg_symmetry = round(float(np.mean([c["symmetry_score"] for c in all_compositions])), 1)
    
    # Text overlay frequency
    text_frequency = round(sum(1 for t in all_text_detections if t["has_text_overlay"]) / len(all_text_detections) * 100, 1) if all_text_detections else 0
    
    # Scene type distribution
    scene_distribution = {st: scene_types.count(st) for st in set(scene_types)}
    
    # Calculate penalties and signals
    penalties = []
    fixes = []
    signals = []
    
    if avg_brightness < 55:
        penalties.append(15)
        fixes.append("The sampled frames are dark. Increase exposure or use brighter footage.")
    elif avg_brightness > 215:
        penalties.append(10)
        fixes.append("The sampled frames are very bright. Check exposure so detail is not washed out.")
    else:
        signals.append("Average brightness looks usable.")
    
    if avg_contrast < 35:
        penalties.append(15)
        fixes.append("Visual contrast is low. Add better lighting, sharper graphics, or higher-contrast edits.")
    else:
        signals.append("Average contrast looks readable.")
    
    if change_rate is not None:
        if change_rate < 0.18:
            penalties.append(20)
            fixes.append("Visual variety looks low. Add cuts, zooms, B-roll, graphics, or screen changes every few seconds.")
        elif change_rate > 0.75:
            penalties.append(8)
            fixes.append("The video changes visuals very often. Make sure cuts don't distract from the point.")
        else:
            signals.append("Visual change rate looks healthy.")
    
    # Enhanced signals and fixes
    if combined_palette:
        dominant_hue = combined_palette[0]["hue"]
        signals.append(f"Dominant color palette is {dominant_hue}.")
        
        if combined_palette[0]["saturation"] == "vibrant":
            signals.append("Color palette is vibrant and eye-catching.")
        else:
            fixes.append("Consider using more vibrant colors to increase visual appeal.")
    
    if text_frequency > 50:
        signals.append(f"Text overlays appear in {text_frequency}% of frames - good for emphasis.")
    elif text_frequency < 10:
        fixes.append("Consider adding text overlays or graphics to emphasize key points.")
    
    if avg_rule_of_thirds > 60:
        signals.append("Composition follows the rule of thirds well.")
    elif avg_rule_of_thirds < 40:
        fixes.append("Consider using the rule of thirds for more dynamic composition.")
    
    # Scene variety
    if len(scene_distribution) <= 2 and duration > 60:
        fixes.append("Scene variety is limited. Mix different shot types and angles.")
    elif len(scene_distribution) >= 4:
        signals.append("Good scene variety keeps viewers engaged.")
    
    visual_score = max(0, 100 - sum(penalties))
    
    return {
        "available": True,
        "source": "video_frames",
        "visual_score": visual_score,
        "sample_count": len(frame_stats),
        "average_brightness": avg_brightness,
        "average_contrast": avg_contrast,
        "average_frame_change": avg_frame_change,
        "visual_change_rate": change_rate,
        "sampled_frames": frame_stats,
        "signals": signals,
        "fixes": fixes,
        # Enhanced data
        "color_palette": combined_palette,
        "composition": {
            "rule_of_thirds_score": avg_rule_of_thirds,
            "symmetry_score": avg_symmetry,
            "text_overlay_frequency": text_frequency,
        },
        "scene_analysis": {
            "scene_types": scene_distribution,
            "primary_scene": max(scene_distribution, key=scene_distribution.get) if scene_distribution else "unknown",
        },
    }


def _combine_palettes(palettes: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Combine multiple frame palettes into an overall video palette."""
    if not palettes:
        return []
    
    # Aggregate color data
    color_data = {}
    for palette in palettes:
        for color in palette:
            hex_key = color["hex"]
            if hex_key not in color_data:
                color_data[hex_key] = {
                    "rgb": color["rgb"],
                    "hex": hex_key,
                    "total_percentage": 0,
                    "count": 0,
                    "hue": color["hue"],
                    "saturation": color["saturation"],
                    "lightness": color["lightness"],
                }
            color_data[hex_key]["total_percentage"] += color["percentage"]
            color_data[hex_key]["count"] += 1
    
    # Sort by average percentage and return top colors
    sorted_colors = sorted(
        color_data.values(),
        key=lambda x: x["total_percentage"] / x["count"],
        reverse=True
    )[:8]
    
    for color in sorted_colors:
        color["percentage"] = round(color["total_percentage"] / color["count"], 1)
    
    return sorted_colors

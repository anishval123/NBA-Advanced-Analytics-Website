import argparse
import json
import statistics
from pathlib import Path

from moviepy.editor import VideoFileClip

VALID_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi"}

try:
    from scenedetect import detect, AdaptiveDetector
    HAS_SCENEDETECT = True
except ImportError:
    HAS_SCENEDETECT = False


def get_shot_durations(video_path):
    with VideoFileClip(str(video_path)) as video:
        duration = video.duration

    if HAS_SCENEDETECT:
        try:
            scenes = detect(str(video_path), AdaptiveDetector(luma_only=True))
            durations = [scene[1].get_seconds() - scene[0].get_seconds() for scene in scenes if scene[1].get_seconds() - scene[0].get_seconds() > 0.1]
            if durations:
                return durations
            print("  No scenes found, falling back to equal-duration segments")
        except Exception as e:
            print(f"  Warning: scene detection failed ({e}), using equal-duration segments")

    segments = max(3, int(duration / 5))
    return [duration / segments for _ in range(segments)]


def summarize_durations(durations):
    if not durations:
        return {}
    return {
        "count": len(durations),
        "average": statistics.mean(durations),
        "median": statistics.median(durations),
        "min": min(durations),
        "max": max(durations),
        "stdev": statistics.stdev(durations) if len(durations) > 1 else 0.0,
        "shot_lengths": durations,
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze example videos to estimate shot-length style.")
    parser.add_argument("--examples", required=True, help="Folder containing example edited videos.")
    parser.add_argument("--output", default="style_profile.json", help="Output JSON file.")
    args = parser.parse_args()

    example_dir = Path(args.examples)
    if not example_dir.exists() or not example_dir.is_dir():
        raise SystemExit(f"Example folder not found: {example_dir}")

    all_durations = []
    example_files = []
    for video_path in sorted(example_dir.iterdir()):
        if video_path.suffix.lower() not in VALID_EXTENSIONS:
            continue
        print(f"Analyzing: {video_path.name}")
        durations = get_shot_durations(video_path)
        all_durations.extend(durations)
        example_files.append(video_path.name)
        print(f"  segments: {len(durations)}, avg segment: {statistics.mean(durations):.2f}s")

    if not all_durations:
        raise SystemExit("No valid videos found in the example folder.")

    overall = summarize_durations(all_durations)
    style_profile = {
        "example_files": example_files,
        "average_shot_length": round(overall["average"], 2),
        "median_shot_length": round(overall["median"], 2),
        "min_shot_length": round(overall["min"], 2),
        "max_shot_length": round(overall["max"], 2),
        "shot_count": overall["count"],
        "target_shot_length": round(overall["average"], 2),
        "style_notes": {
            "description": "Estimated pacing from example videos. Uses equal-duration fallback if scene detection is unavailable.",
            "cutter": "hard_cut"
        },
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(style_profile, f, indent=2)

    print(f"Saved style profile to {args.output}")


if __name__ == "__main__":
    main()

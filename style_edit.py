import argparse
import json
import statistics
from pathlib import Path

from moviepy.editor import VideoFileClip, concatenate_videoclips

VALID_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi"}


def estimate_shot_length(video_path: Path) -> float:
    with VideoFileClip(str(video_path)) as video:
        duration = video.duration

    if duration <= 0:
        return 5.0

    segments = max(3, int(duration / 5))
    return duration / segments


def estimate_style(examples_dir: Path):
    durations = []
    example_files = []

    for video_path in sorted(examples_dir.iterdir()):
        if video_path.suffix.lower() not in VALID_EXTENSIONS:
            continue
        example_files.append(video_path.name)
        print(f"Analyzing example: {video_path.name}")
        durations.append(estimate_shot_length(video_path))

    if not durations:
        raise SystemExit("No valid example videos found in the examples folder.")

    average_length = statistics.mean(durations)
    return {
        "example_files": example_files,
        "average_shot_length": round(average_length, 2),
        "example_shot_lengths": [round(value, 2) for value in durations],
        "style_notes": {
            "description": "Estimated pacing from example videos using equal-duration segment approximation.",
            "cutter": "hard_cut"
        },
    }


def build_segments(duration: float, shot_length: float, max_segments: int):
    segments = []
    start = 0.0
    while start + 0.2 < duration and len(segments) < max_segments:
        end = min(duration, start + shot_length)
        if end - start >= 0.2:
            segments.append((start, end))
        start = end

    if segments and segments[-1][1] < duration:
        segments[-1] = (segments[-1][0], duration)
    elif not segments and duration > 0:
        segments.append((0.0, duration))

    return segments


def main():
    parser = argparse.ArgumentParser(description="Analyze style examples and edit raw footage in one step.")
    parser.add_argument("--examples", required=True, help="Folder containing edited example videos.")
    parser.add_argument("--input", required=True, help="Raw input video file.")
    parser.add_argument("--output", default="output.mp4", help="Output styled video file.")
    parser.add_argument("--style-output", help="Optional JSON file to save the estimated style profile.")
    parser.add_argument("--max-segments", type=int, default=50, help="Maximum number of output segments.")
    parser.add_argument("--duration", type=float, help="Optional maximum duration (seconds) of raw footage to use for the test.")
    parser.add_argument("--test-mode", action="store_true", help="If set, create a visible jump-cut test output.")
    args = parser.parse_args()

    examples_dir = Path(args.examples)
    if not examples_dir.exists() or not examples_dir.is_dir():
        raise SystemExit(f"Examples folder not found: {examples_dir}")

    raw_video = Path(args.input)
    if not raw_video.exists():
        raise SystemExit(f"Raw video not found: {raw_video}")

    style_profile = estimate_style(examples_dir)
    shot_length = style_profile["average_shot_length"]

    if args.style_output:
        with open(args.style_output, "w", encoding="utf-8") as f:
            json.dump(style_profile, f, indent=2)
        print(f"Saved style profile to {args.style_output}")

    with VideoFileClip(str(raw_video)) as video:
        raw_duration = video.duration
        max_duration = min(raw_duration, args.duration) if args.duration and args.duration > 0 else raw_duration
        print(f"Raw duration: {raw_duration:.2f}s")
        if args.duration and args.duration > 0:
            print(f"Limiting output to first {max_duration:.2f}s")
        print(f"Using target shot length: {shot_length:.2f}s")

        segments = build_segments(max_duration, shot_length, args.max_segments)
        print(f"Creating {len(segments)} segments")

        if args.test_mode:
            segments = [seg for i, seg in enumerate(segments) if i % 2 == 0]
            print(f"Test mode: keeping {len(segments)} of the original segments")

        clips = [video.subclip(start, end).without_audio() for start, end in segments]
        if not clips:
            raise SystemExit("No clips were created for the output video.")

        final = concatenate_videoclips(clips, method="compose")
        if video.audio is not None:
            audio_clip = video.audio.subclip(0, max_duration)
            final = final.set_audio(audio_clip)
            print("Preserving raw audio voice track in the output.")
        else:
            print("No audio track found in the raw input; output will be silent.")

        print(f"Writing styled output to {args.output}...")
        final.write_videofile(str(args.output), codec="libx264", audio_codec="aac", verbose=False, logger=None)

    print(f"Saved styled edit to {args.output}")


if __name__ == "__main__":
    main()

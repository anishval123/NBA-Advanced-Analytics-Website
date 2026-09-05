import argparse
import json
from pathlib import Path

from moviepy.editor import VideoFileClip, concatenate_videoclips


def build_segments(duration, shot_length, max_segments):
    if duration <= 0 or shot_length <= 0:
        return [(0.0, duration)] if duration > 0 else []

    segments = []
    start = 0.0
    while start + 0.2 < duration and len(segments) < max_segments:
        end = min(duration, start + shot_length)
        segments.append((start, end))
        start = end

    if segments and segments[-1][1] < duration:
        segments[-1] = (segments[-1][0], duration)
    elif not segments and duration > 0:
        segments.append((0.0, duration))

    return segments


def main():
    parser = argparse.ArgumentParser(description="Apply a shot-length style profile to raw footage.")
    parser.add_argument("--input", required=True, help="Raw input video file.")
    parser.add_argument("--style", default="style_profile.json", help="Style profile JSON file.")
    parser.add_argument("--output", default="output.mp4", help="Output rendered file.")
    parser.add_argument("--max_segments", type=int, default=50, help="Maximum number of output segments.")
    args = parser.parse_args()

    raw_video = Path(args.input)
    if not raw_video.exists():
        raise SystemExit(f"Raw video not found: {raw_video}")

    style_profile = json.loads(Path(args.style).read_text(encoding="utf-8"))
    shot_length = style_profile.get("target_shot_length") or style_profile.get("average_shot_length")
    if not shot_length:
        raise SystemExit("Style profile does not contain a target shot length.")

    with VideoFileClip(str(raw_video)) as video:
        raw_duration = video.duration
        print(f"Raw duration: {raw_duration:.2f}s")
        segments = build_segments(raw_duration, shot_length, args.max_segments)
        print(f"Creating {len(segments)} segments at ~{shot_length:.2f}s each")

        clips = [video.subclip(start, end) for start, end in segments if end - start >= 0.2]
        if not clips:
            raise SystemExit("No output clips were created.")

        final = concatenate_videoclips(clips, method="compose")
        print(f"Writing output to {args.output}...")
        final.write_videofile(str(args.output), codec="libx264", audio_codec="aac", verbose=False, logger=None)

    print(f"Saved styled edit to {args.output}")


if __name__ == "__main__":
    main()

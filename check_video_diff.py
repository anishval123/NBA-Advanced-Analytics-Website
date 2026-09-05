from pathlib import Path
from moviepy.editor import VideoFileClip

for file_name in ["raw_inputs/allen.mp4", "allen_styled.mp4"]:
    path = Path(file_name)
    if not path.exists():
        print(f"{file_name} MISSING")
        continue
    with VideoFileClip(str(path)) as clip:
        print(f"{file_name}: {path.stat().st_size} bytes, {clip.duration:.2f} seconds")


import cv2
import os
import json

def analyze_video(video_path):
    if not os.path.isfile(video_path):
        print("Error: Video file not found!")
        return

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Error: Unable to open video!")
        return

    # Extract video metadata
    filename = os.path.basename(video_path)
    file_size = os.path.getsize(video_path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = frame_count / fps if fps > 0 else 0

    metadata = {
        "Filename": filename,
        "File Extension": os.path.splitext(filename)[1],
        "File Size (MB)": round(file_size / (1024 * 1024), 2),
        "Resolution": f"{width} x {height}",
        "Width": width,
        "Height": height,
        "Frame Rate (FPS)": round(fps, 2),
        "Total Frames": frame_count,
        "Duration (Seconds)": round(duration, 2)
    }

    video.release()

    print("\n===== VIDEO METADATA =====")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # Save metadata to a JSON file
    output_file = os.path.splitext(video_path)[0] + "_metadata.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)

    print(f"\nMetadata saved to: {output_file}")


if __name__ == "__main__":
    path = input("Enter the full path of the video: ").strip().strip('"')
    analyze_video(path)

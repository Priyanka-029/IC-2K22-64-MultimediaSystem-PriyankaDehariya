
import os
import csv
import soundfile as sf
from mutagen import File

def analyze_audio(file_path):
    if not os.path.isfile(file_path):
        print("Error: File not found!")
        return

    try:
        # Read audio properties
        info = sf.info(file_path)
        audio = File(file_path)

        metadata = {
            "File Name": os.path.basename(file_path),
            "File Format": info.format,
            "Audio Subtype": info.subtype,
            "Duration (seconds)": round(info.duration, 2),
            "Sample Rate (Hz)": info.samplerate,
            "Channels": info.channels,
            "Total Frames": info.frames,
            "File Size (MB)": round(
                os.path.getsize(file_path) / (1024 * 1024), 2
            ),
            "Bitrate (kbps)": (
                round(audio.info.bitrate / 1000, 2)
                if audio and audio.info and hasattr(audio.info, "bitrate")
                else "Not available"
            )
        }

        # Display metadata
        print("\n===== AUDIO ANALYSIS REPORT =====")
        for key, value in metadata.items():
            print(f"{key}: {value}")

        # Export to CSV
        output_file = os.path.splitext(file_path)[0] + "_report.csv"

        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Property", "Value"])
            for key, value in metadata.items():
                writer.writerow([key, value])

        print(f"\nReport saved to: {output_file}")

    except Exception as error:
        print("Could not analyze this audio file:", error)
        print("Try a WAV or FLAC file if the format is unsupported.")


if __name__ == "__main__":
    file_path = input("Enter the audio file path: ").strip().strip('"')
    analyze_audio(file_path)

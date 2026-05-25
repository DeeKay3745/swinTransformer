import os
import re
import argparse
import subprocess
import pandas as pd


def safe_filename(text, max_len=80):
    text = str(text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)

    if len(text) > max_len:
        text = text[:max_len]

    return text if text else "clip"


def timestamp_to_seconds(ts):
    """
    Convert HH:MM:ss.000 timestamp into seconds.

    Example:
    00:01:23.450 -> 83.45 seconds
    """

    if pd.isna(ts):
        raise ValueError("Empty timestamp")

    # If Excel reads timestamp as datetime/time object
    if hasattr(ts, "hour") and hasattr(ts, "minute") and hasattr(ts, "second"):
        return (
            ts.hour * 3600
            + ts.minute * 60
            + ts.second
            + ts.microsecond / 1_000_000
        )

    # If Excel reads it as number
    if isinstance(ts, (int, float)):
        return float(ts)

    ts = str(ts).strip().replace(",", ".")
    parts = ts.split(":")

    if len(parts) == 3:
        hh = float(parts[0])
        mm = float(parts[1])
        ss = float(parts[2])
        return hh * 3600 + mm * 60 + ss

    elif len(parts) == 2:
        mm = float(parts[0])
        ss = float(parts[1])
        return mm * 60 + ss

    elif len(parts) == 1:
        return float(parts[0])

    else:
        raise ValueError(f"Unsupported timestamp format: {ts}")


def detect_level_from_id(clip_id):
    """
    Detect type from id.

    A-Z       -> character
    s1, s2    -> sentence
    p1, p2    -> paragraph
    otherwise -> word
    """

    raw_id = str(clip_id).strip()
    lower_id = raw_id.lower()

    if re.fullmatch(r"s\d+", lower_id):
        return "sentences", "sentence"

    if re.fullmatch(r"p\d+", lower_id):
        return "paragraphs", "paragraph"

    if re.fullmatch(r"[a-zA-Z]", raw_id):
        return "characters", "character"

    return "words", "word"


def trim_video_clip(video_path, output_path, start_sec, end_sec):
    """
    Trim video clip using ffmpeg and save as MP4.
    Keeps both video and audio.
    """

    duration = end_sec - start_sec

    if duration <= 0:
        raise ValueError(
            f"Invalid timestamps: start={start_sec}, end={end_sec}"
        )

    command = [
        "ffmpeg",
        "-y",
        "-ss", str(start_sec),
        "-i", video_path,
        "-t", str(duration),

        # Re-encode for accurate trimming
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",

        # Audio settings
        "-c:a", "aac",
        "-b:a", "128k",

        output_path
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )


def main():
    parser = argparse.ArgumentParser(
        description="Trim video clips from video using Excel timestamps"
    )

    parser.add_argument(
        "--video",
        required=True,
        help="Path to input video file"
    )

    parser.add_argument(
        "--excel",
        required=True,
        help="Path to Excel file with id, start_time, end_time"
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        help="Folder where trimmed video clips will be saved"
    )

    parser.add_argument(
        "--language",
        default="english",
        help="Language name, example: english"
    )

    parser.add_argument(
        "--speaker",
        default="speaker01",
        help="Speaker name or speaker ID"
    )

    args = parser.parse_args()

    video_path = args.video
    excel_path = args.excel
    output_dir = args.output_dir
    language = safe_filename(args.language)
    speaker = safe_filename(args.speaker)

    df = pd.read_excel(excel_path)

    required_columns = ["Content", "Start Time (HH:MM:SS.000)", "End Time (HH:MM:SS.000)"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"Missing column: {col}\n"
                f"Your Excel columns are: {list(df.columns)}\n"
                f"Required columns are: id, start_time, end_time"
            )

    os.makedirs(output_dir, exist_ok=True)

    success_count = 0
    failed_count = 0

    for idx, row in df.iterrows():
        try:
            clip_id = str(row["id"]).strip()

            start_sec = timestamp_to_seconds(row["start_time"])
            end_sec = timestamp_to_seconds(row["end_time"])

            folder_name, unit_name = detect_level_from_id(clip_id)

            save_folder = os.path.join(output_dir, folder_name)
            os.makedirs(save_folder, exist_ok=True)

            clean_id = safe_filename(clip_id)

            output_filename = (
                f"{speaker}_{language}_{unit_name}_{clean_id}.mp4"
            )

            output_path = os.path.join(save_folder, output_filename)

            trim_video_clip(
                video_path=video_path,
                output_path=output_path,
                start_sec=start_sec,
                end_sec=end_sec
            )

            print(f"[OK] Saved: {output_path}")
            success_count += 1

        except Exception as e:
            print(f"[FAILED] Excel row {idx + 2}: {e}")
            failed_count += 1

    print("\n==============================")
    print("Video trimming completed")
    print("==============================")
    print(f"Successfully saved clips: {success_count}")
    print(f"Failed rows: {failed_count}")
    print(f"Output folder: {output_dir}")


if __name__ == "__main__":
    main()
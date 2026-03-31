"""
WAV Cropper — Trims a WAV file into segments based on an Excel sheet.
Excel format: Column A = Title, Column B = Start time, Column C = End time
Time format: HH:MM:SS.microseconds (e.g., 00:00:16.436000)

Usage:
    pip install pandas openpyxl pydub
    python crop_wav.py <wav_file> <excel_file> [output_folder]

Example:
    python crop_wav.py recording.wav marathi.xlsx output_clips
"""

import sys
import os
import re
import pandas as pd
from pydub import AudioSegment


def parse_time_to_ms(time_val):
    """Convert HH:MM:SS.ffffff or HH:MM:SS.fff string to milliseconds."""
    if pd.isna(time_val):
        return None

    time_str = str(time_val).strip()

    # Handle Timedelta objects (pandas may auto-parse)
    if hasattr(time_val, 'total_seconds'):
        return int(time_val.total_seconds() * 1000)

    # Parse string format HH:MM:SS.ffffff
    match = re.match(r'(\d+):(\d+):(\d+)\.?(\d*)', time_str)
    if not match:
        print(f"  WARNING: Could not parse time '{time_str}', skipping.")
        return None

    h, m, s, frac = match.groups()
    frac = frac.ljust(6, '0')[:6]  # Pad/truncate to microseconds
    total_ms = (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(frac) // 1000
    return total_ms


def sanitize_filename(name):
    """Remove/replace characters that are invalid in filenames."""
    name = str(name).strip()
    name = re.sub(r'[\\/*?:"<>|]', '_', name)
    name = name.replace('\n', ' ').replace('\r', '')
    return name[:100]  # Limit length


def main():
    if len(sys.argv) < 3:
        print("Usage: python crop_wav.py <wav_file> <excel_file> [output_folder] [sheet_number] [prefix]")
        print("  sheet_number: 1 = first sheet (default), 2 = second sheet, etc.")
        print("  prefix: e.g. hemmant_phase7_marathi_ or sahil_phase7_hindi_")
        sys.exit(1)

    wav_path = sys.argv[1]
    excel_path = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "cropped_output"
    sheet_num = int(sys.argv[4]) - 1 if len(sys.argv) > 4 else 0  # 1-based to 0-based
    prefix = sys.argv[5] if len(sys.argv) > 5 else "hemmant_phase7_marathi_"

    os.makedirs(output_dir, exist_ok=True)

    # Read specified sheet (no header row, columns: A=title, B=start, C=end)
    print(f"Reading Excel: {excel_path} (sheet {sheet_num + 1})")
    df = pd.read_excel(excel_path, header=None, sheet_name=sheet_num)

    # Skip the first row if it's a header (Start/End)
    if str(df.iloc[0, 1]).strip().lower() == 'start':
        df = df.iloc[1:].reset_index(drop=True)

    # Load WAV file
    print(f"Loading WAV: {wav_path} (this may take a moment for large files)...")
    audio = AudioSegment.from_wav(wav_path)
    print(f"  Duration: {len(audio) / 1000:.2f} seconds")

    success_count = 0
    skip_count = 0

    for idx, row in df.iterrows():
        title = row.iloc[0]
        start_raw = row.iloc[1]
        end_raw = row.iloc[2]

        # Skip rows with no title or no timestamps
        if pd.isna(title) or (pd.isna(start_raw) and pd.isna(end_raw)):
            skip_count += 1
            continue

        start_ms = parse_time_to_ms(start_raw)
        end_ms = parse_time_to_ms(end_raw)

        if start_ms is None or end_ms is None:
            print(f"  Skipping '{title}': missing start or end time.")
            skip_count += 1
            continue

        if end_ms <= start_ms:
            print(f"  Skipping '{title}': end time <= start time.")
            skip_count += 1
            continue

        # Crop the audio segment
        segment = audio[start_ms:end_ms]

        # Save with prefix + sanitized title
        safe_name = sanitize_filename(title)
        full_name = f"{prefix}{safe_name}"
        out_path = os.path.join(output_dir, f"{full_name}.wav")

        # Handle duplicate filenames
        counter = 1
        while os.path.exists(out_path):
            out_path = os.path.join(output_dir, f"{full_name}_{counter}.wav")
            counter += 1

        segment.export(out_path, format="wav")
        duration_ms = end_ms - start_ms
        print(f"  ✓ '{full_name}.wav' | {start_ms}ms → {end_ms}ms | duration: {duration_ms}ms")
        success_count += 1

    print(f"\nDone! {success_count} clips saved to '{output_dir}/', {skip_count} rows skipped.")


if __name__ == "__main__":
    main()
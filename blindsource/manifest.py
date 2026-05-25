import argparse
from pathlib import Path
import pandas as pd
import soundfile as sf


AUDIO_EXTENSIONS = {
    ".wav", ".mp3", ".flac", ".m4a", ".aac", ".ogg"
}


def get_audio_info(audio_path):
    try:
        info = sf.info(str(audio_path))
        duration_sec = round(info.frames / info.samplerate, 3)
        sample_rate = info.samplerate
        num_channels = info.channels
        return duration_sec, sample_rate, num_channels
    except Exception as e:
        print(f"[WARN] Could not read audio info: {audio_path} | {e}")
        return "", "", ""


def create_manifest(root_dir):
    root_dir = Path(root_dir).expanduser().resolve()

    if not root_dir.exists():
        raise FileNotFoundError(f"Folder not found: {root_dir}")

    output_csv = root_dir / "dau_kdah_audio_manifest.csv"

    rows = []

    audio_files = [
        p for p in root_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS
    ]

    print(f"[INFO] Root folder: {root_dir}")
    print(f"[INFO] Found {len(audio_files)} audio files")

    for audio_path in sorted(audio_files):
        relative_parts = audio_path.relative_to(root_dir).parts

        phase = ""
        severity = ""

        for part in relative_parts:
            part_lower = part.lower()

            if part_lower.startswith("phase"):
                phase = part

            if part_lower in ["high", "medium", "low"]:
                severity = part

        duration_sec, sample_rate, num_channels = get_audio_info(audio_path)

        rows.append({
            "sample_id": audio_path.stem,
            "audio_path": str(audio_path),
            "relative_path": str(audio_path.relative_to(root_dir)),
            "phase": phase,
            "severity": severity,
            "filename": audio_path.name,
            "extension": audio_path.suffix.lower(),
            "duration_sec": duration_sec,
            "sample_rate": sample_rate,
            "num_channels": num_channels
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")

    print("\n[DONE] Manifest created successfully")
    print(f"[SAVED AT] {output_csv}")
    print("\nPreview:")
    print(df.head())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create DAU-KDAH audio manifest inside the same folder"
    )

    parser.add_argument(
        "--root_dir",
        required=True,
        help="Path to your Audios folder"
    )

    args = parser.parse_args()
    create_manifest(args.root_dir)
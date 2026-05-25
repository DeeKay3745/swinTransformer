import pandas as pd

manifest_path = "/Volumes/DEEKAY/Audios/dau_kdah_audio_manifest.csv"

df = pd.read_csv(manifest_path)

print(df.head())
print("\nTotal files:", len(df))
print("\nPhases:")
print(df["phase"].value_counts())

print("\nSeverity:")
print(df["severity"].value_counts())

print("\nSample rates:")
print(df["sample_rate"].value_counts())
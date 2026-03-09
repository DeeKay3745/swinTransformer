from pydub import AudioSegment
import pandas as pd
import os

# Load audio
audio_file = "sitaram_phase7_sev_marathi.wav"
audio = AudioSegment.from_wav(audio_file)

# Detailed mapping based on Abhishek_Marathi.docx
segments = [
    # --- Vowels (अ to अः)  ---
    (1100, 2500, "अ"), (2500, 3600, "आ"), (4500, 5600, "इ"), 
    (5600, 6800, "ई"), (7500, 8500, "उ"), (8500, 9600, "ऊ"), 
    (10200, 11400, "ऋ"), (12800, 14000, "ए"), (14000, 15500, "ऐ"), 
    (15500, 17200, "ओ"), (17200, 18500, "औ"), (18500, 19800, "अं"), 
    (19800, 21500, "अः"),

    # --- Individual Words  ---
    (79500, 81000, "आई"), (81000, 82500, "वडील"), (82500, 84000, "शाळा"),
    (84000, 85500, "आंबा"), (85500, 87000, "घर"), (93500, 96000, "बालपण"),
    (96000, 97500, "भाऊ"), (97500, 99500, "नवरा"), (99500, 101000, "बहीण"),
    (101000, 103500, "गणपती"), (104500, 106500, "पुस्तक"), (106500, 108500, "शिक्षक"),
    (108500, 111500, "टिपणवही"), (111500, 113500, "डोळे"), (113500, 116000, "गुडघा"),

    # --- Sentences (s1 to s5)  ---
    (243500, 249500, "Sentence_1"),
    (250000, 257500, "Sentence_2"),
    (258500, 271500, "Sentence_3"),
    (272500, 285500, "Sentence_4"),
    (286500, 300500, "Sentence_5")
]

# Output setup
output_dir = "marathi_trimmed_files"
if not os.path.exists(output_dir): os.makedirs(output_dir)

metadata = []

print("Trimming in progress...")

for start, end, label in segments:
    chunk = audio[start:end]
    filename = f"{label}.wav"
    chunk.export(os.path.join(output_dir, filename), format="wav")
    
    metadata.append({
        "Marathi Text": label,
        "Start (ms)": start,
        "End (ms)": end,
        "Duration (ms)": end - start,
        "File Name": filename
    })

# Save timestamps to Excel
df = pd.DataFrame(metadata)
df.to_excel("marathi_audio_metadata.xlsx", index=False)

print(f"Task Complete! check the '{output_dir}' folder.")
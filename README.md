# 🧠 SwinLip: Visual Speech Recognition for Dysarthric Patients

## 📌 Overview

**SwinLip** is a research project focused on building a **Visual Speech Recognition (VSR)** system tailored for **dysarthric patients**. Dysarthria affects speech clarity due to neuromuscular impairments, making conventional ASR systems unreliable.

This project leverages **lip-reading from video input** using modern deep learning architectures such as **Swin Transformer**, **BiGRU**, and **CTC/Seq2Seq decoders** to generate accurate predicted text.

---

## 🎯 Objective

- Develop a robust lip-reading model for dysarthric speech
- Explore Swin Transformer for spatio-temporal feature extraction
- Compare BiGRU vs Transformer for temporal modeling
- Evaluate CTC vs Seq2Seq decoding strategies
- Contribute toward assistive communication AI systems

---

## 🏗️ Proposed Pipeline
Video Input
↓
Face Detection
↓
Lip Region Cropping
↓
Spatio-Temporal Feature Extraction (3D CNN / Swin Transformer)
↓
Temporal Modeling (BiGRU / Transformer)
↓
CTC / Seq2Seq Decoder
↓
Predicted Text


---

## 🔬 Architecture Description

### 1️⃣ Video Input
Raw video frames containing a speaking subject.

### 2️⃣ Face Detection
Detect face bounding boxes from each frame.

### 3️⃣ Lip Region Cropping
Extract mouth Region of Interest (ROI) using facial landmarks.

### 4️⃣ Spatio-Temporal Feature Extraction
- 3D CNN (baseline)
- **Swin Transformer** (primary backbone)

Captures spatial lip patterns and motion dynamics across frames.

### 5️⃣ Temporal Modeling
- BiGRU (efficient sequence modeling)
- Transformer (long-range dependency modeling)

### 6️⃣ Decoder
- CTC (Connectionist Temporal Classification)
- Seq2Seq (attention-based decoding)

### 7️⃣ Output
Predicted text transcription.

---

## 📍 Current Development Status

| Stage | Current Status |
|-------|----------------|
| Video Input | ✔ Dataset collection in progress |
| Face Detection | ⏳ Planned |
| Lip Region Cropping | 🚧 Installing & configuring MediaPipe |
| Spatio-Temporal Feature Extraction | ⏳ Not started |
| Temporal Modeling | ⏳ Not started |
| Decoder | ⏳ Not started |
| Training & Evaluation | ⏳ Not started |

---

## 🔧 Current Focus

Currently working on:

- Installing and configuring **MediaPipe**
- Extracting lip landmarks from video
- Cropping accurate lip ROI for downstream modeling

This preprocessing stage is critical for improving final recognition accuracy.

---

## 🛠️ Tech Stack (Planned)

- Python
- PyTorch
- OpenCV
- MediaPipe
- Swin Transformer
- BiGRU / Transformer
- CTC Loss

---

## 📊 Future Work

- Complete lip region extraction pipeline
- Integrate Swin Transformer backbone
- Implement temporal modeling module
- Train using CTC loss
- Evaluate on dysarthric datasets
- Speaker-specific fine-tuning

---

## 🤝 Research Contribution

This project contributes to:

- Visual Speech Recognition (VSR)
- Transformer-based vision modeling
- Assistive AI for speech impairment
- Multimodal speech understanding

---



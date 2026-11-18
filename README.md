# 🛣️ RoadVision AI: Road Damage Detection & Infrastructure Intelligence

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/Ultralytics-YOLOv8-00FFFF?logo=yolo&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/Framework-PyTorch-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An end-to-end Computer Vision system that automatically detects, localizes, and classifies 7 types of road surface distress from images and dashcam footage using fine-tuned YOLOv8 models and an interactive high-tech inspection dashboard.

---

## 📌 Table of Contents
- [Overview](#-overview)
- [Target Road Damage Classes](#-target-road-damage-classes)
- [Model Training & Comparative Analysis](#-model-training--comparative-analysis)
- [Deployment App (RoadVision AI)](#-deployment-app-roadvision-ai)
- [Project Directory Structure](#-project-directory-structure)
- [Getting Started](#-getting-started)
- [Results & Plots](#-results--plots)
- [License](#-license)

---

## 🌟 Overview
Automated road condition assessment is vital for transportation safety, municipal budget planning, and predictive infrastructure maintenance. This project trains, benchmarks, and deploys multiple state-of-the-art **YOLOv8** object detection models (`yolov8n`, `yolov8s`, `yolov8m`) to detect road deterioration in real time.

---

## 🏷️ Target Road Damage Classes
The models are trained to classify and localize 7 distinct damage categories:

| Color Code | Class Name | Description & Visual Characteristics |
| :---: | :--- | :--- |
| <span style="color:#EF4444">🔴</span> | **Pothole** | Structural surface cavity / crater posing severe vehicle hazards. |
| <span style="color:#A855F7">🟣</span> | **Alligator Crack** | Interconnected fatigue cracking resembling crocodile skin. |
| <span style="color:#F59E0B">🟠</span> | **Longitudinal Crack** | Linear cracks running parallel to the direction of travel. |
| <span style="color:#EAB308">🟡</span> | **Transverse Crack** | Cracks perpendicular to the road centerline caused by thermal expansion. |
| <span style="color:#06B6D4">🔵</span> | **Block Crack** | Large rectangular cracked blocks forming an interconnected web. |
| <span style="color:#3B82F6">🔷</span> | **Edge Crack** | Deterioration along the outer pavement edges. |
| <span style="color:#10B981">🟢</span> | **General Crack** | Unclassified fissures and early-stage pavement stress lines. |

---

## 📊 Model Training & Comparative Analysis

All models were fine-tuned for **60 Epochs** using identical hyperparameter baselines (`imgsz=640`, `batch=16`, `lr0=0.01`, `optimizer="auto"`, `seed=42`).

### 📈 Benchmark Comparison Table

| Model | Parameters / Size | mAP@50 | mAP@50-95 | Precision | Recall | Latency (ms) | Inference FPS | Best For |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **YOLOv8n** (Nano) | **6.2 MB** | 0.4169 | 0.2457 | **0.6020** | 0.3987 | **10.5 ms** | **95.2 FPS** | Edge / Mobile / Dashcam |
| **YOLOv8s** (Small) 🏆 | 21.5 MB | **0.4301** | **0.2473** | 0.4679 | 0.4272 | 15.6 ms | 64.0 FPS | **Balanced Production** |
| **YOLOv8m** (Medium) | 49.6 MB | 0.4249 | 0.2428 | 0.4736 | **0.4395** | 27.1 ms | 36.9 FPS | High-Capacity Workstations |

### 🔍 Results Discussion:
1. **Best Overall Performer (`YOLOv8s`):**
   * Achieved the highest detection accuracy with **`mAP@50 = 43.01%`** and **`mAP@50-95 = 24.73%`**.
   * Delivers **64.0 FPS**, making it perfectly capable of real-time 60 FPS video processing.
2. **Edge Deployment Champion (`YOLOv8n`):**
   * Retains **97% of the accuracy** of YOLOv8s while being **3.5x smaller (6.2 MB)** and running at **95.2 FPS**.
   * Ideal for deployment on resource-constrained embedded devices (e.g. Raspberry Pi 5, Jetson Nano).
3. **Observation on `YOLOv8m`:**
   * Increasing capacity to Medium did not improve mAP (42.49% vs 43.01%), while latency nearly doubled to 27.1 ms. This indicates slight overfitting and shows that for this dataset size, the Small architecture is the optimal sweet spot.

---

## 💻 Deployment App (RoadVision AI)

The deployment app is built with **Streamlit** using a custom dark-mode design system directly mirrored from our **Figma** UI prototype.

### Key Features:
* 📁 **Flexible Input:** Upload any road footage/image or choose from pre-loaded field samples.
* ⚙️ **Real-Time Thresholds:** Interactive sliders for Confidence score and IoU / NMS suppression.
* 🎛️ **Damage Class Filtering:** Multi-select damage categories with custom color tokens.
* 🔄 **Split Comparison:** Compare raw road photos side-by-side with AI annotated overlays.
* 📊 **Automated KPI Assessment:**
  * **Total Damages Count**
  * **Road Condition Index** (0 - 100 Health Score)
  * **Inference Latency & FPS**
  * **Hazard Level** (Low / Moderate / High)
* 📋 **Inspection Log:** Detailed coordinate tracking `(x, y, w, h)` with one-click **CSV Report Export**.
* 🍩 **Distribution Donut Chart:** Interactive Plotly breakdown of damage types.

---

## 📁 Project Directory Structure

```text
Road Damage Project/
├── app.py                      # Main Streamlit Web Application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
│
├── weights/                    # Fine-tuned best model weights
│   ├── yolov8n_best.pt         # YOLOv8 Nano weights (6.2 MB)
│   ├── yolov8s_best.pt         # YOLOv8 Small weights (21.5 MB) [Default]
│   └── yolov8m_best.pt         # YOLOv8 Medium weights (49.6 MB)
│
├── notebooks/                  # Jupyter / Kaggle training notebooks
│   └── road-damage-object-detection.ipynb
│
├── sample_images/              # Preloaded road inspection samples
│   ├── road_section_01.jpg
│   ├── road_section_02.jpg
│   └── road_section_08.jpg
│
├── outputs/                    # Evaluation artifacts & plots
│   ├── results.json            # Parsed metrics for all trained models
│   ├── plots/                  # Comparison bar charts (mAP, FPS, size, etc.)
│   └── predictions/            # Prediction grid against ground truth
│
└── Figma Design/               # UI/UX design export & Tailwind prototypes
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/road-damage-detection.git
cd road-damage-detection
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Web Application
```bash
streamlit run app.py
```
Then open **`http://localhost:8501`** in your browser.

---

## 📈 Results & Plots
The evaluation curves and comparison plots are stored in `outputs/plots/`:
* `map50.png` & `map50_95.png`: Mean Average Precision comparison.
* `fps.png`: Inference throughput benchmark.
* `model_size.png`: Checkpoint footprint analysis.
* `precision.png` & `recall.png`: Detection trade-offs.

---

## 📜 License
This project is licensed under the MIT License - feel free to use and adapt it for academic and commercial applications.

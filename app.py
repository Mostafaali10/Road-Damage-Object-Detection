import os
import time
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import plotly.graph_objects as go
from ultralytics import YOLO

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="RoadVision AI - Infrastructure Intelligence",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Custom Styling (Figma Design Pixel-Perfect Match)
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

:root {
    --bg-main: #0B0F17;
    --card-bg: rgba(20, 29, 44, 0.75);
    --border-color: #23334D;
    --blue: #2563EB;
    --emerald: #10B981;
    --amber: #F59E0B;
    --red: #EF4444;
    --purple: #A855F7;
    --cyan: #06B6D4;
    --yellow: #EAB308;
}

/* App Background & Global Fonts */
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 78% 0%, rgba(37, 99, 235, 0.08), transparent 30%), #0B0F17 !important;
    font-family: 'Inter', sans-serif !important;
    color: #E7EEF9 !important;
}

[data-testid="stHeader"] {
    display: none !important;
}

/* Hide default streamlit decorations */
#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(17, 24, 37, 0.95), rgba(11, 15, 23, 0.98)) !important;
    border-right: 1px solid rgba(35, 51, 77, 0.8) !important;
    padding-top: 1rem;
}

/* Topbar Header */
.topbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 24px;
    background: rgba(11, 15, 23, 0.92);
    border: 1px solid rgba(35, 51, 77, 0.85);
    border-radius: 12px;
    margin-bottom: 20px;
    backdrop-filter: blur(16px);
}

.brand-section {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: linear-gradient(145deg, #3B82F6, #1D4ED8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 0 20px rgba(37, 99, 235, 0.35);
}

.brand-title {
    font-size: 19px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #FFFFFF;
    line-height: 1.2;
}

.brand-title span {
    color: #60A5FA;
}

.brand-sub {
    font-size: 8px;
    letter-spacing: 1.5px;
    color: #64748B;
    font-weight: 700;
    text-transform: uppercase;
}

.model-badge {
    padding: 4px 10px;
    border: 1px solid #263B5B;
    background: #111A29;
    border-radius: 6px;
    font: 600 9px 'JetBrains Mono', monospace;
    color: #94A3B8;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.dot-pulse {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #3B82F6;
    box-shadow: 0 0 8px #3B82F6;
}

.top-pills {
    display: flex;
    align-items: center;
    gap: 10px;
}

.status-pill {
    background: rgba(20, 29, 44, 0.8);
    border: 1px solid #1F2C41;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 11px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: #E2E8F0;
}

.status-pill strong {
    font-family: 'JetBrains Mono', monospace;
}

.live-green-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 8px #10B981;
}

.profile-chip {
    display: flex;
    align-items: center;
    gap: 10px;
}

.profile-avatar {
    width: 36px;
    height: 36px;
    border-radius: 9px;
    background: linear-gradient(145deg, #264063, #18253A);
    border: 1px solid #354965;
    color: #93C5FD;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 11px;
}

/* Sidebar Section Headers */
.side-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 18px;
    margin-bottom: 10px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.2px;
    color: #8796AD;
}

.side-header .badge-num {
    font: 700 8px 'JetBrains Mono', monospace;
    color: #3B82F6;
    background: rgba(37, 99, 235, 0.15);
    border: 1px solid rgba(37, 99, 235, 0.3);
    padding: 2px 5px;
    border-radius: 4px;
    margin-right: 6px;
}

/* Upload file box */
.file-loaded-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #141E2F;
    border: 1px solid #283A53;
    border-radius: 8px;
    padding: 8px 12px;
    margin-top: 8px;
    margin-bottom: 12px;
}

.file-loaded-title {
    font-size: 11px;
    font-weight: 600;
    color: #E2E8F0;
}

.file-loaded-sub {
    font-size: 9px;
    color: #64748B;
    font-family: 'JetBrains Mono', monospace;
}

/* Metric KPI Cards */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 20px;
}

.kpi-card {
    background: rgba(18, 26, 40, 0.7);
    border: 1px solid #213047;
    border-radius: 10px;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
}

.kpi-card.blue::before { background: #3B82F6; }
.kpi-card.green::before { background: #10B981; }
.kpi-card.cyan::before { background: #06B6D4; }
.kpi-card.amber::before { background: #F59E0B; }
.kpi-card.red::before { background: #EF4444; }

.kpi-info span {
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #7D8DA8;
    font-weight: 600;
    display: block;
    margin-bottom: 4px;
}

.kpi-info strong {
    font-size: 22px;
    font-weight: 700;
    color: #FFFFFF;
    font-family: 'JetBrains Mono', monospace;
}

.kpi-info small {
    font-size: 10px;
    color: #94A3B8;
    margin-left: 4px;
}

.kpi-meta {
    font-size: 9px;
    margin-top: 3px;
    color: #64748B;
}

.kpi-icon {
    width: 38px;
    height: 38px;
    border-radius: 8px;
    background: #142033;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}

/* Inspection Viewport Container */
.viewport-card {
    background: rgba(16, 23, 36, 0.8);
    border: 1px solid #23334D;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 20px;
}

.viewport-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.eyebrow {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.2px;
    color: #38BDF8;
    display: flex;
    align-items: center;
    gap: 6px;
}

.viewport-title {
    font-size: 18px;
    font-weight: 700;
    color: #F8FAFC;
    margin: 0;
}

.viewport-title span {
    color: #3B82F6;
}

/* Bottom Grid Panel */
.bottom-panel {
    background: rgba(16, 23, 36, 0.8);
    border: 1px solid #23334D;
    border-radius: 12px;
    padding: 16px 20px;
    height: 100%;
}

.panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}

.panel-header h3 {
    margin: 0;
    font-size: 15px;
    font-weight: 700;
    color: #F8FAFC;
}

/* Custom Table */
.custom-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
}

.custom-table th {
    text-align: left;
    padding: 10px 8px;
    color: #7D8DA8;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    border-bottom: 1px solid #23334D;
}

.custom-table td {
    padding: 9px 8px;
    border-bottom: 1px solid #1C293F;
    color: #E2E8F0;
    font-family: 'JetBrains Mono', monospace;
}

.class-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
    font-size: 11px;
}

.class-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

/* Progress bar inside table */
.conf-bar-bg {
    width: 60px;
    height: 5px;
    background: #1C2739;
    border-radius: 4px;
    display: inline-block;
    margin-right: 8px;
    vertical-align: middle;
    overflow: hidden;
}

.conf-bar-fill {
    height: 100%;
    border-radius: 4px;
}

/* Run Button Styling */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: #FFFFFF !important;
    border: 1px solid #3B82F6 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    box-shadow: 0 0 18px rgba(37, 99, 235, 0.4) !important;
    transition: all 0.2s ease !important;
}

div.stButton > button:first-child:hover {
    box-shadow: 0 0 25px rgba(37, 99, 235, 0.7) !important;
    transform: translateY(-1px) !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Damage Classes & Palette Setup
# ---------------------------------------------------------
CLASS_METADATA = {
    "alligator": {"name": "Alligator Crack", "color": "#A855F7", "rgb": (168, 85, 247), "severity": 3},
    "block": {"name": "Block Crack", "color": "#06B6D4", "rgb": (6, 182, 212), "severity": 2},
    "crack": {"name": "General Crack", "color": "#10B981", "rgb": (16, 185, 129), "severity": 1},
    "edge": {"name": "Edge Crack", "color": "#3B82F6", "rgb": (59, 130, 246), "severity": 2},
    "longitudinal": {"name": "Longitudinal Crack", "color": "#F59E0B", "rgb": (245, 158, 11), "severity": 2},
    "pothole": {"name": "Pothole", "color": "#EF4444", "rgb": (239, 68, 68), "severity": 4},
    "transverse": {"name": "Transverse Crack", "color": "#EAB308", "rgb": (234, 179, 8), "severity": 2},
}

MODEL_PATHS = {
    "YOLOv8s · Balanced (Best Accuracy)": "weights/yolov8s_best.pt",
    "YOLOv8n · Edge Fast (Lightweight)": "weights/yolov8n_best.pt",
    "YOLOv8m · Heavy (High Capacity)": "weights/yolov8m_best.pt",
}

# ---------------------------------------------------------
# Model Loader with Caching
# ---------------------------------------------------------
@st.cache_resource
def load_yolo_model(model_path: str):
    if os.path.exists(model_path):
        return YOLO(model_path)
    # Fallback paths
    fallback_map = {
        "weights/yolov8s_best.pt": "experiments/yolov8s_20261110_161614/weights/best.pt",
        "weights/yolov8n_best.pt": "experiments/yolov8n_20261110_150819/weights/best.pt",
        "weights/yolov8m_best.pt": "experiments/yolov8m_20261110_172624/weights/best.pt",
    }
    fb = fallback_map.get(model_path)
    if fb and os.path.exists(fb):
        return YOLO(fb)
    return YOLO("yolov8s.pt")

# ---------------------------------------------------------
# Annotation Function (PIL with Translucent Bounding Boxes)
# ---------------------------------------------------------
def annotate_image(image: Image.Image, detections: list) -> Image.Image:
    base = image.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Try loading Windows standard font
    font = None
    for font_name in ["segoeui.ttf", "arial.ttf", "calibri.ttf"]:
        p = os.path.join(r"C:\Windows\Fonts", font_name)
        if os.path.exists(p):
            try:
                font = ImageFont.truetype(p, 13)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()

    for det in detections:
        box = det["box"]
        x1, y1, x2, y2 = box
        cls_key = det["class_name"].lower()
        meta = CLASS_METADATA.get(cls_key, {"name": cls_key, "color": "#3B82F6", "rgb": (59, 130, 246)})
        rgb = meta["rgb"]
        
        # 1. Translucent filled box
        draw.rectangle([x1, y1, x2, y2], fill=(*rgb, 40), outline=(*rgb, 240), width=2)
        
        # 2. Pill Tag at top left
        label_text = f"{meta['name']} {int(det['confidence'] * 100)}%"
        bbox = draw.textbbox((0, 0), label_text, font=font)
        tw = bbox[2] - bbox[0] + 12
        th = bbox[3] - bbox[1] + 8
        
        tag_y1 = max(0, y1 - th - 3)
        tag_y2 = tag_y1 + th
        tag_x2 = x1 + tw
        
        draw.rounded_rectangle([x1, tag_y1, tag_x2, tag_y2], radius=4, fill=(*rgb, 235))
        draw.text((x1 + 6, tag_y1 + 3), label_text, fill=(255, 255, 255, 255), font=font)

    return Image.alpha_composite(base, overlay).convert("RGB")

# ---------------------------------------------------------
# Top Navigation Bar
# ---------------------------------------------------------
st.markdown(
    """
    <div class="topbar-container">
        <div class="brand-section">
            <div class="brand-icon">🛣️</div>
            <div>
                <div class="brand-title">RoadVision <span>AI</span></div>
                <div class="brand-sub">Infrastructure Intelligence</div>
            </div>
            <div class="model-badge">
                <span class="dot-pulse"></span> YOLOv8 Powered
            </div>
        </div>
        <div class="top-pills">
            <div class="status-pill">
                <span style="color:#64748B;">Active Model</span>
                <strong>YOLOv8s</strong>
            </div>
            <div class="status-pill">
                <span class="live-green-dot"></span>
                <strong>Engine Active</strong>
                <small style="color:#64748B; border-left:1px solid #334155; padding-left:6px;">CPU / GPU</small>
            </div>
            <div class="status-pill" style="color:#34D399;">
                ⚡ <strong>15.6 ms</strong>
                <small style="color:#64748B;">64 FPS</small>
            </div>
        </div>
        <div class="profile-chip">
            <div class="profile-avatar">AK</div>
            <div>
                <div style="font-size:11px; font-weight:700; color:#F1F5F9;">Alex Kim</div>
                <div style="font-size:8px; color:#64748B;">Lead Inspector</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="side-header">
            <div><span class="badge-num">01</span> INPUT SOURCE</div>
            <span style="color:#38BDF8; font-size:7px;">READY</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Sample selection or upload
    sample_options = {
        "Default Inspection (road_section_08.jpg)": "sample_images/road_section_08.jpg",
        "Multi-Damage Zone 1 (road_section_01.jpg)": "sample_images/road_section_01.jpg",
        "Critical Potholes Zone 2 (road_section_02.jpg)": "sample_images/road_section_02.jpg",
    }
    
    selected_sample = st.selectbox(
        "Choose Preloaded Road Footage",
        options=list(sample_options.keys()),
        index=0,
    )
    
    uploaded_file = st.file_uploader(
        "Or Upload Road Image / Footage",
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload asphalt road images or dashcam frames",
    )
    
    # Load source image
    current_filename = "road_section_08.jpg"
    if uploaded_file is not None:
        source_image = Image.open(uploaded_file)
        current_filename = uploaded_file.name
    else:
        sample_path = sample_options[selected_sample]
        source_image = Image.open(sample_path)
        current_filename = os.path.basename(sample_path)

    img_w, img_h = source_image.size
    st.markdown(
        f"""
        <div class="file-loaded-box">
            <div>
                <div class="file-loaded-title">📁 {current_filename}</div>
                <div class="file-loaded-sub">{img_w} × {img_h} px · RGB</div>
            </div>
            <div style="color:#10B981; font-size:14px;">✔</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="side-header">
            <div><span class="badge-num">02</span> MODEL CONFIG</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    selected_model_label = st.selectbox(
        "Detection Model",
        options=list(MODEL_PATHS.keys()),
        index=0,
    )
    
    conf_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.10,
        max_value=0.95,
        value=0.35,
        step=0.05,
        help="Minimum confidence score for damage detection",
    )
    
    iou_threshold = st.slider(
        "IoU / NMS Threshold",
        min_value=0.10,
        max_value=0.90,
        value=0.45,
        step=0.05,
        help="Non-Maximum Suppression threshold to filter overlapping boxes",
    )

    st.markdown(
        """
        <div class="side-header">
            <div><span class="badge-num">03</span> CLASS FILTERS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    active_classes = []
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.checkbox("🔴 Pothole", value=True): active_classes.append("pothole")
        if st.checkbox("🟣 Alligator", value=True): active_classes.append("alligator")
        if st.checkbox("🟠 Longitudinal", value=True): active_classes.append("longitudinal")
        if st.checkbox("🟢 General Crack", value=True): active_classes.append("crack")
    with col_c2:
        if st.checkbox("🟡 Transverse", value=True): active_classes.append("transverse")
        if st.checkbox("🔵 Block", value=True): active_classes.append("block")
        if st.checkbox("🔷 Edge", value=True): active_classes.append("edge")

    run_inference_btn = st.button("⚡ Run AI Inspection", use_container_width=True)
    st.markdown(
        """
        <div style="text-align:center; margin-top:8px; font-size:9px; color:#64748B;">
            <span class="live-green-dot"></span> Ready · Est. speed <b>~15ms</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# Inference Engine Execution
# ---------------------------------------------------------
model_path = MODEL_PATHS[selected_model_label]
model = load_yolo_model(model_path)

t_start = time.time()
yolo_results = model.predict(
    source_image,
    conf=conf_threshold,
    iou=iou_threshold,
    verbose=False,
)[0]
inference_duration_ms = (time.time() - t_start) * 1000
fps_val = 1000.0 / max(1.0, inference_duration_ms)

# Parse detections
all_detections = []
boxes_data = yolo_results.boxes
if boxes_data is not None and len(boxes_data) > 0:
    for i, (box, cls_id, conf) in enumerate(
        zip(boxes_data.xyxy.tolist(), boxes_data.cls.tolist(), boxes_data.conf.tolist())
    ):
        raw_name = model.names[int(cls_id)].lower()
        if raw_name in active_classes:
            all_detections.append({
                "id": f"#RV-{i+101:03d}",
                "class_name": raw_name,
                "confidence": conf,
                "box": [round(b, 1) for b in box],
                "box_wh": [
                    round(box[0], 1),
                    round(box[1], 1),
                    round(box[2] - box[0], 1),
                    round(box[3] - box[1], 1),
                ],
            })

# Calculate Road Condition Index (0-100)
total_damages = len(all_detections)
severity_sum = sum(CLASS_METADATA.get(d["class_name"], {}).get("severity", 2) for d in all_detections)
road_condition_score = max(15, 100 - (severity_sum * 11 + total_damages * 4))

if road_condition_score >= 80:
    condition_label = "Good Condition"
    hazard_level = "Low Risk"
    hazard_color = "green"
elif road_condition_score >= 50:
    condition_label = "Fair Condition"
    hazard_level = "Moderate Alert"
    hazard_color = "amber"
else:
    condition_label = "Critical Damage"
    hazard_level = "High Hazard"
    hazard_color = "red"

# ---------------------------------------------------------
# Viewport Card (Inspection Viewer)
# ---------------------------------------------------------
st.markdown(
    """
    <div class="viewport-card">
        <div class="viewport-header">
            <div>
                <div class="eyebrow"><span class="live-green-dot"></span> INSPECTION VIEWPORT</div>
                <div class="viewport-title">Road section <span>/</span> CH-104 · KM 18.4</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Image Viewer Mode Toggle
view_mode = st.radio(
    "Viewer Mode",
    options=["Annotated View (AI Detection)", "Split Comparison (Original vs Annotated)"],
    index=0,
    horizontal=True,
    label_visibility="collapsed",
)

annotated_img = annotate_image(source_image, all_detections)

if "Split" in view_mode:
    col_orig, col_annot = st.columns(2)
    with col_orig:
        st.markdown("<div style='font-size:11px; font-weight:700; color:#94A3B8; margin-bottom:4px;'>📷 ORIGINAL ROAD FOOTAGE</div>", unsafe_allow_html=True)
        st.image(source_image, use_container_width=True)
    with col_annot:
        st.markdown("<div style='font-size:11px; font-weight:700; color:#38BDF8; margin-bottom:4px;'>🤖 AI DETECTIONS OVERLAY</div>", unsafe_allow_html=True)
        st.image(annotated_img, use_container_width=True)
else:
    st.image(annotated_img, use_container_width=True)

# HUD Overlay footer
st.markdown(
    f"""
    <div style="display:flex; justify-content:space-between; align-items:center; background:#101726; border:1px solid #1F2C41; border-radius:8px; padding:6px 14px; margin-top:-10px; margin-bottom:20px; font-size:10px; font-family:'JetBrains Mono', monospace; color:#94A3B8;">
        <div>🛰️ <b>GPS LOCKED:</b> 40.7128° N, 74.0060° W &nbsp;|&nbsp; <b>Frame:</b> 01 / 01</div>
        <div><b>Model:</b> {selected_model_label.split('·')[0].strip()} &nbsp;|&nbsp; <b>Confidence:</b> ≥ {int(conf_threshold*100)}%</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# KPI Metric Cards
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="kpi-container">
        <div class="kpi-card blue">
            <div class="kpi-info">
                <span>Total Damages Found</span>
                <strong>{total_damages}</strong><small>Issues</small>
                <div class="kpi-meta">+2 from previous scan</div>
            </div>
            <div class="kpi-icon" style="color:#60A5FA;">🔍</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-info">
                <span>Road Condition Index</span>
                <strong>{road_condition_score}</strong><small>/ 100</small>
                <div class="kpi-meta">{condition_label}</div>
            </div>
            <div class="kpi-icon" style="color:#34D399;">⏱️</div>
        </div>
        <div class="kpi-card cyan">
            <div class="kpi-info">
                <span>Inference Speed</span>
                <strong>{inference_duration_ms:.1f}</strong><small>ms</small>
                <div class="kpi-meta">{fps_val:.1f} FPS · Real-time</div>
            </div>
            <div class="kpi-icon" style="color:#38BDF8;">⚡</div>
        </div>
        <div class="kpi-card {hazard_color}">
            <div class="kpi-info">
                <span>Hazard Level</span>
                <strong>{hazard_level.split()[0]}</strong>
                <div class="kpi-meta">{hazard_level}</div>
            </div>
            <div class="kpi-icon" style="color:#F87171;">⚠️</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Bottom Section: Inspection Log & Distribution
# ---------------------------------------------------------
col_log, col_dist = st.columns([1.6, 1.0])

with col_log:
    st.markdown(
        f"""
        <div class="bottom-panel">
            <div class="panel-header">
                <div>
                    <div class="eyebrow">LIVE DETECTIONS</div>
                    <h3>Inspection Log</h3>
                </div>
                <div style="font-size:10px; font-family:'JetBrains Mono'; color:#64748B;">
                    {total_damages} records logged
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    
    if all_detections:
        table_rows_html = ""
        for det in all_detections:
            cls_key = det["class_name"].lower()
            meta = CLASS_METADATA.get(cls_key, {"name": cls_key, "color": "#3B82F6"})
            conf_pct = int(det["confidence"] * 100)
            coords_str = f"{det['box_wh'][0]}, {det['box_wh'][1]}, {det['box_wh'][2]}, {det['box_wh'][3]}"
            
            table_rows_html += f"""
            <tr>
                <td style="color:#94A3B8;">{det['id']}</td>
                <td>
                    <div class="class-tag">
                        <span class="class-dot" style="background:{meta['color']};"></span>
                        <span style="color:#F1F5F9;">{meta['name']}</span>
                    </div>
                </td>
                <td>
                    <div class="conf-bar-bg">
                        <div class="conf-bar-fill" style="width:{conf_pct}%; background:{meta['color']};"></div>
                    </div>
                    <b>{det['confidence']*100:.1f}%</b>
                </td>
                <td style="color:#64748B;">{coords_str}</td>
            </tr>
            """
            
        st.markdown(
            f"""
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Damage Type</th>
                        <th>Confidence</th>
                        <th>Coordinates (x, y, w, h)</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )
        
        # Download Report CSV
        df_export = pd.DataFrame([
            {
                "ID": d["id"],
                "Damage_Type": d["class_name"],
                "Confidence": f"{d['confidence']*100:.2f}%",
                "X1": d["box"][0],
                "Y1": d["box"][1],
                "X2": d["box"][2],
                "Y2": d["box"][3],
            }
            for d in all_detections
        ])
        csv_data = df_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Inspection CSV",
            data=csv_data,
            file_name="road_damage_inspection_report.csv",
            mime="text/csv",
        )
    else:
        st.markdown("<div style='color:#64748B; font-size:12px; padding:20px 0;'>No damages detected with current thresholds. Adjust confidence slider in sidebar.</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

with col_dist:
    st.markdown(
        """
        <div class="bottom-panel">
            <div class="panel-header">
                <div>
                    <div class="eyebrow">ISSUE BREAKDOWN</div>
                    <h3>Damage Distribution</h3>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    
    if all_detections:
        counts = {}
        for d in all_detections:
            c = d["class_name"]
            counts[c] = counts.get(c, 0) + 1
            
        labels = [CLASS_METADATA.get(k, {}).get("name", k) for k in counts.keys()]
        values = list(counts.values())
        colors = [CLASS_METADATA.get(k, {}).get("color", "#3B82F6") for k in counts.keys()]
        
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.68,
                    marker=dict(colors=colors, line=dict(color="#0B0F17", width=2)),
                    textinfo="value",
                    textfont=dict(family="JetBrains Mono", size=12, color="#FFFFFF"),
                    hoverinfo="label+percent",
                )
            ]
        )
        
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(family="Inter", size=9, color="#94A3B8"),
            ),
            annotations=[
                dict(
                    text=f"<b>{total_damages}</b><br><span style='font-size:9px; color:#64748B;'>TOTAL</span>",
                    x=0.5,
                    y=0.5,
                    font=dict(size=18, family="JetBrains Mono", color="#FFFFFF"),
                    showarrow=False,
                )
            ],
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=240,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown("<div style='color:#64748B; font-size:12px; padding:20px 0;'>No data to visualize.</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

import { useRef, useState } from "react";

type IconName =
  | "road"
  | "upload"
  | "file"
  | "chevron"
  | "spark"
  | "download"
  | "zoomIn"
  | "zoomOut"
  | "move"
  | "box"
  | "search"
  | "clock"
  | "gauge"
  | "alert"
  | "activity"
  | "check";

const paths: Record<IconName, React.ReactNode> = {
  road: (
    <>
      <path d="M8 3 5 21M16 3l3 18M12 4v3m0 4v3m0 4v2" />
      <path d="M3.5 21h17" />
    </>
  ),
  upload: (
    <>
      <path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5" />
      <path d="M5 14v5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-5" />
    </>
  ),
  file: (
    <>
      <path d="M7 3h7l4 4v14H7z" />
      <path d="M14 3v5h4M10 13h5m-5 4h5" />
    </>
  ),
  chevron: <path d="m8 10 4 4 4-4" />,
  spark: (
    <>
      <path d="m12 3 1.2 3.8L17 8l-3.8 1.2L12 13l-1.2-3.8L7 8l3.8-1.2z" />
      <path d="m18.5 14 .7 2.3 2.3.7-2.3.7-.7 2.3-.7-2.3-2.3-.7 2.3-.7zM5 14l.8 2.5 2.5.8-2.5.8L5 20.5l-.8-2.4-2.5-.8 2.5-.8z" />
    </>
  ),
  download: (
    <>
      <path d="M12 3v12m0 0 4-4m-4 4-4-4" />
      <path d="M5 19h14" />
    </>
  ),
  zoomIn: (
    <>
      <circle cx="10.5" cy="10.5" r="6.5" />
      <path d="m15.5 15.5 5 5M10.5 7.5v6m-3-3h6" />
    </>
  ),
  zoomOut: (
    <>
      <circle cx="10.5" cy="10.5" r="6.5" />
      <path d="m15.5 15.5 5 5m-13-10h6" />
    </>
  ),
  move: (
    <>
      <path d="M12 2v20m0-20-3 3m3-3 3 3m-3 17-3-3m3 3 3-3M2 12h20M2 12l3-3m-3 3 3 3m17-3-3-3m3 3-3 3" />
    </>
  ),
  box: (
    <>
      <rect x="4" y="5" width="16" height="14" rx="2" />
      <path d="M8 9h8v6H8z" />
    </>
  ),
  search: (
    <>
      <circle cx="11" cy="11" r="7" />
      <path d="m16 16 5 5" />
    </>
  ),
  clock: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 7v5l3 2" />
    </>
  ),
  gauge: (
    <>
      <path d="M4.2 18a9 9 0 1 1 15.6 0" />
      <path d="m12 14 4-5" />
      <path d="M7 18h10" />
    </>
  ),
  alert: (
    <>
      <path d="M12 3 2.8 20h18.4z" />
      <path d="M12 9v4m0 3h.01" />
    </>
  ),
  activity: <path d="M3 12h4l2.2-6 4.2 12 2.1-6H21" />,
  check: <path d="m5 12 4 4L19 6" />,
};

function Icon({
  name,
  size = 18,
  className = "",
}: {
  name: IconName;
  size?: number;
  className?: string;
}) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {paths[name]}
    </svg>
  );
}

const filterItems = [
  ["Pothole", 3, "red"],
  ["Alligator", 1, "amber"],
  ["Longitudinal", 0, "purple"],
  ["Transverse", 2, "amber"],
  ["Block", 0, "cyan"],
  ["Edge", 0, "blue"],
  ["Crack", 1, "green"],
] as const;

const logData = [
  ["#RV-001", "Pothole", "91.3%", "412, 298, 186, 124", "red"],
  ["#RV-002", "Transverse crack", "84.7%", "702, 374, 244, 68", "amber"],
  ["#RV-003", "Pothole", "78.9%", "215, 446, 112, 92", "red"],
  ["#RV-004", "Alligator crack", "76.2%", "531, 208, 164, 116", "purple"],
  ["#RV-005", "Transverse crack", "71.8%", "864, 274, 128, 54", "amber"],
];

export default function App() {
  const [confidence, setConfidence] = useState(62);
  const [iou, setIou] = useState(45);
  const [mode, setMode] = useState<"split" | "annotated">("annotated");
  const [showBoxes, setShowBoxes] = useState(true);
  const [zoom, setZoom] = useState(100);
  const [isRunning, setIsRunning] = useState(false);
  const [fileName, setFileName] = useState("road_section_06.jpg");
  const [activeFilters, setActiveFilters] = useState(filterItems.map((f) => f[0]));
  const inputRef = useRef<HTMLInputElement>(null);

  const runInspection = () => {
    setIsRunning(true);
    window.setTimeout(() => setIsRunning(false), 1400);
  };

  const toggleFilter = (name: string) => {
    setActiveFilters((prev) =>
      prev.includes(name) ? prev.filter((item) => item !== name) : [...prev, name],
    );
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-area">
          <div className="brand-mark">
            <Icon name="road" size={22} />
          </div>
          <div>
            <div className="brand-name">
              RoadVision <span>AI</span>
            </div>
            <div className="brand-sub">INFRASTRUCTURE INTELLIGENCE</div>
          </div>
          <div className="powered-badge">
            <span className="badge-dot" /> YOLOv8 Powered
          </div>
        </div>

        <div className="top-statuses">
          <div className="status-pill">
            <span>Model</span>
            <strong>YOLOv8s</strong>
          </div>
          <div className="status-pill">
            <span className="live-dot" />
            <strong>GPU Active</strong>
            <small>CUDA</small>
          </div>
          <div className="latency-pill">
            <Icon name="activity" size={15} />
            <div>
              <strong>
                15.6 <small>ms</small>
              </strong>
              <span>64 FPS</span>
            </div>
          </div>
        </div>

        <div className="top-actions">
          <button
            className="export-button"
            onClick={() => alert("Inspection report queued for export.")}
          >
            <Icon name="download" size={16} /> Export report <span>PDF / CSV</span>
          </button>
          <div className="profile">
            <div className="avatar">AK</div>
            <div>
              <strong>Alex Kim</strong>
              <span>Lead Inspector</span>
            </div>
            <Icon name="chevron" size={15} />
          </div>
        </div>
      </header>

      <div className="dashboard">
        <aside className="sidebar">
          <div className="section-heading">
            <div>
              <span>01</span> INPUT SOURCE
            </div>
            <span className="optional">REQUIRED</span>
          </div>
          <input
            ref={inputRef}
            type="file"
            accept="image/*,video/*"
            hidden
            onChange={(e) => e.target.files?.[0] && setFileName(e.target.files[0].name)}
          />
          <button className="upload-zone" onClick={() => inputRef.current?.click()}>
            <div className="upload-icon">
              <Icon name="upload" size={22} />
            </div>
            <strong>Drop road footage here</strong>
            <span>
              or <b>browse files</b> from device
            </span>
            <small>JPG, PNG, MP4 · Max 500 MB</small>
          </button>
          <div className="loaded-file">
            <div className="file-icon">
              <Icon name="file" size={16} />
            </div>
            <div>
              <strong>{fileName}</strong>
              <span>8.4 MB · 4096 × 2731</span>
            </div>
            <span className="file-check">
              <Icon name="check" size={12} />
            </span>
          </div>

          <div className="divider" />
          <div className="section-heading">
            <div>
              <span>02</span> MODEL CONFIG
            </div>
          </div>
          <label className="field-label">Detection model</label>
          <div className="select-wrap">
            <select defaultValue="YOLOv8s">
              <option value="YOLOv8s">YOLOv8s · Balanced</option>
              <option value="YOLOv8n">YOLOv8n · Edge Fast</option>
              <option value="YOLOv8m">YOLOv8m · Heavy</option>
            </select>
            <Icon name="chevron" size={16} />
          </div>

          <Slider label="Confidence threshold" value={confidence} setValue={setConfidence} />
          <Slider label="IoU / NMS threshold" value={iou} setValue={setIou} />

          <div className="divider" />
          <div className="section-heading filter-heading">
            <div>
              <span>03</span> CLASS FILTERS
            </div>
            <button
              onClick={() =>
                setActiveFilters(
                  activeFilters.length === filterItems.length ? [] : filterItems.map((f) => f[0]),
                )
              }
            >
              {activeFilters.length === filterItems.length ? "Clear" : "All"}
            </button>
          </div>
          <div className="filter-list">
            {filterItems.map(([name, count, color]) => (
              <button
                key={name}
                className={`filter-row ${activeFilters.includes(name) ? "active" : ""}`}
                onClick={() => toggleFilter(name)}
              >
                <span className={`check-box ${color}`}>
                  <Icon name="check" size={11} />
                </span>
                <span className={`class-dot ${color}`} /> <span>{name}</span>
                <small>{count}</small>
              </button>
            ))}
          </div>
          <button className={`run-button ${isRunning ? "running" : ""}`} onClick={runInspection}>
            <Icon name={isRunning ? "activity" : "spark"} size={18} />
            {isRunning ? "Analyzing road surface..." : "Run AI inspection"}
          </button>
          <div className="estimate">
            <span className="live-dot" /> Ready · Est. processing time <b>1.2s</b>
          </div>
        </aside>

        <main className="main-content">
          <section className="viewer-card">
            <div className="viewer-header">
              <div>
                <div className="eyebrow">
                  <span className="live-dot" /> INSPECTION VIEWPORT
                </div>
                <h1>
                  Road section <span>/</span> CH-104 · KM 18.4
                </h1>
              </div>
              <div className="view-toggle">
                <button
                  className={mode === "split" ? "active" : ""}
                  onClick={() => setMode("split")}
                >
                  Split comparison
                </button>
                <button
                  className={mode === "annotated" ? "active" : ""}
                  onClick={() => setMode("annotated")}
                >
                  Annotated view
                </button>
              </div>
            </div>

            <div className={`image-viewport ${mode}`}>
              {mode === "split" && <div className="split-label original">ORIGINAL</div>}
              <div className="road-image" style={{ transform: `scale(${zoom / 100})` }}>
                <img
                  src="https://images.unsplash.com/photo-1741996950906-5faf36413669?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&q=88&w=1600&h=850"
                  alt="Cracked asphalt road surface under AI inspection"
                />
                <div className="image-shade" />
                {showBoxes && (
                  <>
                    <Detection className="detect-one" label="Pothole" score="91%" color="red" />
                    <Detection
                      className="detect-two"
                      label="Transverse crack"
                      score="84%"
                      color="amber"
                    />
                    <Detection className="detect-three" label="Pothole" score="79%" color="red" />
                    <Detection
                      className="detect-four"
                      label="Alligator"
                      score="76%"
                      color="purple"
                    />
                  </>
                )}
              </div>
              {mode === "split" && (
                <>
                  <div className="split-divider">
                    <span />
                  </div>
                  <div className="split-label analyzed">AI ANALYSIS</div>
                </>
              )}
              <div className="image-meta">
                <span>
                  <i /> GPS LOCKED
                </span>
                <b>40.7128° N, 74.0060° W</b>
                <span>Frame 01 / 01</span>
              </div>
              <div className="viewer-tools">
                <button onClick={() => setZoom(Math.max(80, zoom - 10))} aria-label="Zoom out">
                  <Icon name="zoomOut" size={17} />
                </button>
                <span>{zoom}%</span>
                <button onClick={() => setZoom(Math.min(140, zoom + 10))} aria-label="Zoom in">
                  <Icon name="zoomIn" size={17} />
                </button>
                <i />
                <button title="Pan image">
                  <Icon name="move" size={17} />
                </button>
                <button
                  className={showBoxes ? "active" : ""}
                  onClick={() => setShowBoxes(!showBoxes)}
                  title="Toggle bounding boxes"
                >
                  <Icon name="box" size={17} />
                </button>
              </div>
            </div>
          </section>

          <section className="metrics-grid">
            <Metric
              icon="search"
              tone="blue"
              label="Total damages found"
              value="7"
              suffix="Issues"
              meta="+2 from last scan"
            />
            <Metric
              icon="gauge"
              tone="green"
              label="Road condition index"
              value="68"
              suffix="/ 100"
              meta="Fair condition"
            />
            <Metric
              icon="clock"
              tone="cyan"
              label="Inference speed"
              value="15.6"
              suffix="ms"
              meta="64 FPS · Real-time"
            />
            <Metric
              icon="alert"
              tone="amber"
              label="Hazard level"
              value="Moderate"
              suffix=""
              meta="Attention recommended"
            />
          </section>

          <section className="bottom-grid">
            <div className="panel log-panel">
              <div className="panel-header">
                <div>
                  <span className="eyebrow">LIVE DETECTIONS</span>
                  <h2>Inspection log</h2>
                </div>
                <div className="panel-actions">
                  <span>7 records</span>
                  <button>
                    <Icon name="download" size={15} />
                  </button>
                </div>
              </div>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Damage type</th>
                      <th>Confidence</th>
                      <th>
                        Coordinates <span>(x, y, w, h)</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {logData.map(([id, type, score, coords, color]) => (
                      <tr key={id}>
                        <td>{id}</td>
                        <td>
                          <span className={`type-mark ${color}`} />
                          {type}
                        </td>
                        <td>
                          <div className="confidence">
                            <span style={{ width: score }} className={color} />
                          </div>
                          <b>{score}</b>
                        </td>
                        <td>{coords}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="panel distribution-panel">
              <div className="panel-header">
                <div>
                  <span className="eyebrow">ISSUE BREAKDOWN</span>
                  <h2>Damage distribution</h2>
                </div>
                <button className="more">•••</button>
              </div>
              <div className="distribution-content">
                <div className="donut">
                  <div>
                    <strong>7</strong>
                    <span>TOTAL</span>
                  </div>
                </div>
                <div className="legend">
                  <Legend color="red" label="Potholes" value="3" percent="43%" />
                  <Legend color="amber" label="Transverse" value="2" percent="29%" />
                  <Legend color="purple" label="Alligator" value="1" percent="14%" />
                  <Legend color="green" label="Cracks" value="1" percent="14%" />
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}

function Slider({
  label,
  value,
  setValue,
}: {
  label: string;
  value: number;
  setValue: (v: number) => void;
}) {
  return (
    <div className="slider-field">
      <div className="slider-label">
        <label>{label}</label>
        <output>{(value / 100).toFixed(2)}</output>
      </div>
      <input
        type="range"
        min="0"
        max="100"
        value={value}
        onChange={(e) => setValue(Number(e.target.value))}
        style={{ "--value": `${value}%` } as React.CSSProperties}
      />
      <div className="range-ends">
        <span>0.0</span>
        <span>1.0</span>
      </div>
    </div>
  );
}

function Detection({
  label,
  score,
  color,
  className,
}: {
  label: string;
  score: string;
  color: string;
  className: string;
}) {
  return (
    <div className={`detection ${color} ${className}`}>
      <div className="detection-label">
        <span>{label}</span>
        <b>{score}</b>
      </div>
      <i className="corner c1" />
      <i className="corner c2" />
      <i className="corner c3" />
      <i className="corner c4" />
    </div>
  );
}

function Metric({
  icon,
  tone,
  label,
  value,
  suffix,
  meta,
}: {
  icon: IconName;
  tone: string;
  label: string;
  value: string;
  suffix: string;
  meta: string;
}) {
  return (
    <div className={`metric-card ${tone}`}>
      <div className="metric-icon">
        <Icon name={icon} size={20} />
      </div>
      <div className="metric-copy">
        <span>{label}</span>
        <div>
          <strong>{value}</strong>
          {suffix && <b>{suffix}</b>}
        </div>
        <small>{meta}</small>
      </div>
      <div className="metric-spark">
        {[24, 42, 31, 55, 48, 68, 62, 78, 72, 88].map((h, i) => (
          <i key={i} style={{ height: `${h}%` }} />
        ))}
      </div>
    </div>
  );
}

function Legend({
  color,
  label,
  value,
  percent,
}: {
  color: string;
  label: string;
  value: string;
  percent: string;
}) {
  return (
    <div className="legend-row">
      <span className={`legend-dot ${color}`} />
      <span>{label}</span>
      <b>{value}</b>
      <small>{percent}</small>
    </div>
  );
}

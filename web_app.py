import json
from flask import Flask, render_template_string, request

from analyze_url import analyze_youtube

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>YouTube Analyzer</title>
    <style>
      :root {
        --bg: #f7f8fa;
        --panel: #ffffff;
        --ink: #17202a;
        --muted: #667085;
        --line: #d9dee7;
        --accent: #0f766e;
        --accent-dark: #115e59;
        --warn: #b45309;
        --soft: #eef6f5;
      }

      * { box-sizing: border-box; }

      body {
        margin: 0;
        background: var(--bg);
        color: var(--ink);
        font-family: Arial, Helvetica, sans-serif;
        line-height: 1.5;
      }

      main {
        width: min(1120px, calc(100% - 32px));
        margin: 0 auto;
        padding: 28px 0 48px;
      }

      header {
        display: grid;
        gap: 10px;
        margin-bottom: 22px;
      }

      h1, h2, h3, p { margin-top: 0; }
      h1 { margin-bottom: 0; font-size: 34px; }
      h2 { margin-bottom: 14px; font-size: 22px; }
      h3 { margin-bottom: 8px; font-size: 17px; }
      p { color: var(--muted); }

      form {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 110px 124px;
        gap: 10px;
        align-items: end;
        margin-bottom: 18px;
      }

      label {
        display: block;
        margin-bottom: 6px;
        color: #344054;
        font-size: 14px;
        font-weight: 700;
      }

      input[type=text] {
        width: 100%;
        min-height: 44px;
        border: 1px solid var(--line);
        border-radius: 6px;
        padding: 10px 12px;
        color: var(--ink);
        background: white;
      }

      button {
        min-height: 44px;
        border: 0;
        border-radius: 6px;
        padding: 10px 16px;
        background: var(--accent);
        color: white;
        font-weight: 700;
        cursor: pointer;
      }

      button:hover { background: var(--accent-dark); }

      .notice {
        margin: 16px 0;
        padding: 12px 14px;
        border-left: 4px solid var(--warn);
        background: #fff7ed;
        color: #7c2d12;
      }

      .panel {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
        padding: 18px;
        margin-bottom: 16px;
      }

      .report-head {
        display: grid;
        grid-template-columns: 180px minmax(0, 1fr);
        gap: 18px;
        align-items: center;
      }

      .score {
        display: grid;
        place-items: center;
        width: 160px;
        aspect-ratio: 1;
        border-radius: 50%;
        border: 12px solid var(--accent);
        background: var(--soft);
      }

      .score strong {
        display: block;
        font-size: 42px;
        line-height: 1;
      }

      .score span {
        color: var(--muted);
        font-weight: 700;
      }

      .metrics {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 10px;
      }

      .metric {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: #fbfcfd;
        padding: 12px;
        min-height: 78px;
      }

      .metric span {
        display: block;
        color: var(--muted);
        font-size: 13px;
      }

      .metric strong {
        display: block;
        margin-top: 4px;
        font-size: 18px;
        overflow-wrap: anywhere;
      }

      .actions {
        display: grid;
        gap: 10px;
        margin: 0;
        padding: 0;
        list-style: none;
      }

      .actions li {
        border-left: 4px solid var(--accent);
        background: var(--soft);
        padding: 10px 12px;
      }

      .scorecard {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
      }

      .section-card {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: white;
        padding: 14px;
      }

      .section-top {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: center;
        margin-bottom: 10px;
      }

      .pill {
        border-radius: 999px;
        background: #e5f3f1;
        color: #0f5f58;
        padding: 5px 9px;
        font-weight: 700;
        white-space: nowrap;
      }

      ul.compact {
        margin: 0;
        padding-left: 18px;
        color: #344054;
      }

      .muted { color: var(--muted); }

      .color-palette {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 10px;
      }

      .color-swatch {
        width: 48px;
        height: 48px;
        border-radius: 6px;
        border: 2px solid var(--line);
        position: relative;
        cursor: pointer;
        transition: transform 0.2s;
      }

      .color-swatch:hover {
        transform: scale(1.1);
      }

      .color-swatch::after {
        content: attr(data-hex);
        position: absolute;
        bottom: -20px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 10px;
        color: var(--muted);
        white-space: nowrap;
      }

      .scene-tags {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
        margin-top: 8px;
      }

      .scene-tag {
        background: #f0f4ff;
        color: #1e40af;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 600;
      }

      .composition-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 10px;
      }

      .composition-item {
        background: #fbfcfd;
        border: 1px solid var(--line);
        border-radius: 6px;
        padding: 10px;
        text-align: center;
      }

      .composition-item strong {
        display: block;
        font-size: 20px;
        color: var(--accent);
      }

      .composition-item span {
        font-size: 12px;
        color: var(--muted);
      }

      .status-list {
        display: grid;
        gap: 8px;
        margin-top: 14px;
      }

      .status-line {
        border-left: 4px solid var(--line);
        background: #fbfcfd;
        padding: 10px 12px;
        color: #344054;
      }

      details {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: white;
        padding: 14px;
      }

      summary {
        cursor: pointer;
        font-weight: 700;
      }

      pre {
        margin-bottom: 0;
        padding: 14px;
        overflow-x: auto;
        background: #101828;
        color: #f2f4f7;
        border-radius: 6px;
      }

      @media (max-width: 760px) {
        main { width: min(100% - 24px, 1120px); padding-top: 18px; }
        h1 { font-size: 28px; }
        form, .report-head, .metrics, .scorecard {
          grid-template-columns: 1fr;
        }
        .score {
          width: 140px;
        }
      }
    </style>
  </head>
  <body>
    <main>
      <header>
        <h1>YouTube Analyzer</h1>
        <p>Paste a public video URL to get a practical improvement checklist for metadata, spoken words, hook strength, pacing, and visual variety.</p>
      </header>

      <form method="post">
        <div>
          <label for="url">YouTube video URL</label>
          <input type="text" id="url" name="url" value="{{ submitted_url or '' }}" placeholder="https://youtube.com/watch?v=..." required>
        </div>
        <div>
          <label for="lang">Spoken language</label>
          <input type="text" id="lang" name="lang" value="{{ submitted_lang or 'en' }}" placeholder="en">
        </div>
        <button type="submit">Analyze</button>
      </form>

      {% if error %}
        <div class="notice"><strong>Error:</strong> {{ error }}</div>
      {% endif %}

      {% if report %}
        {% set rec = report.recommendations %}
        {% set meta = report.metadata %}
        {% set insights = report.insights %}
        {% set content = report.content_analysis %}
        {% set transcript = content.transcript or {} %}
        {% set visuals = content.visuals or {} %}

        <section class="panel report-head">
          <div class="score">
            <div>
              <strong>{{ rec.overall_score }}</strong>
              <span>{{ rec.grade }}</span>
            </div>
          </div>
          <div>
            <h2>{{ meta.title }}</h2>
            <p>{{ meta.uploader or "Unknown channel" }}</p>
            <div class="metrics">
              <div class="metric"><span>Duration</span><strong>{{ fmt_duration(insights.duration_seconds) }}</strong></div>
              <div class="metric"><span>Views</span><strong>{{ fmt_number(insights.view_count) }}</strong></div>
              <div class="metric"><span>Likes</span><strong>{{ fmt_number(insights.like_count) }}</strong></div>
              <div class="metric"><span>Words/min</span><strong>{{ insights.words_per_minute or "Unknown" }}</strong></div>
            </div>
          </div>
        </section>

        <section class="panel">
          <h2>Top Fixes</h2>
          {% if rec.top_actions %}
            <ol class="actions">
              {% for action in rec.top_actions %}
                <li>{{ action }}</li>
              {% endfor %}
            </ol>
          {% else %}
            <p class="muted">No major fixes detected from the available metadata.</p>
          {% endif %}
        </section>

        <section class="panel">
          <h2>Content Signals</h2>
          <div class="metrics">
            <div class="metric"><span>Hook score</span><strong>{{ transcript.get("hook_score") or "Unknown" }}</strong></div>
            <div class="metric"><span>Script score</span><strong>{{ transcript.get("script_score") or "Unknown" }}</strong></div>
            <div class="metric"><span>Visual score</span><strong>{{ visuals.get("visual_score") or "Unknown" }}</strong></div>
            <div class="metric"><span>Visual change</span><strong>{{ pct(visuals.get("visual_change_rate")) }}</strong></div>
          </div>
          <div class="status-list">
            {% if not transcript.get("available") %}
              <div class="status-line">{{ first_item(transcript.get("fixes")) }}</div>
            {% endif %}
            {% if transcript.get("source") %}
              <div class="status-line">Words source: {{ label_source(transcript.get("source")) }}</div>
            {% endif %}
            {% if visuals.get("source") %}
              <div class="status-line">Visual source: {{ label_source(visuals.get("source")) }}</div>
            {% endif %}
            {% if visuals.get("fallback_reason") %}
              <div class="status-line">{{ visuals.get("fallback_reason") }}</div>
            {% endif %}
            {% if not visuals.get("available") %}
              <div class="status-line">{{ first_item(visuals.get("fixes")) }}</div>
            {% endif %}
          </div>
          {% if transcript.get("opening_excerpt") %}
            <p class="muted" style="margin-top: 14px;"><strong>Opening excerpt:</strong> {{ transcript.get("opening_excerpt") }}</p>
          {% endif %}
        </section>

        {% if visuals.get("color_palette") %}
        <section class="panel">
          <h2>Color Palette</h2>
          <div class="color-palette">
            {% for color in visuals.color_palette %}
              <div class="color-swatch" style="background: {{ color.hex }};" data-hex="{{ color.hex }}" title="{{ color.hue }}, {{ color.saturation }}, {{ color.lightness }} - {{ color.percentage }}%"></div>
            {% endfor %}
          </div>
          <p class="muted" style="margin-top: 28px;">
            Dominant: <strong>{{ visuals.color_palette[0].hue }}</strong> | 
            Saturation: <strong>{{ visuals.color_palette[0].saturation }}</strong> | 
            Lightness: <strong>{{ visuals.color_palette[0].lightness }}</strong>
          </p>
        </section>
        {% endif %}

        {% if visuals.get("composition") %}
        <section class="panel">
          <h2>Composition Analysis</h2>
          <div class="composition-grid">
            <div class="composition-item">
              <strong>{{ visuals.composition.rule_of_thirds_score }}</strong>
              <span>Rule of Thirds</span>
            </div>
            <div class="composition-item">
              <strong>{{ visuals.composition.symmetry_score }}</strong>
              <span>Symmetry</span>
            </div>
            <div class="composition-item">
              <strong>{{ visuals.composition.text_overlay_frequency }}%</strong>
              <span>Text Overlays</span>
            </div>
          </div>
        </section>
        {% endif %}

        {% if visuals.get("scene_analysis") %}
        <section class="panel">
          <h2>Scene Analysis</h2>
          <div class="scene-tags">
            <span class="scene-tag">Primary: {{ visuals.scene_analysis.primary_scene }}</span>
            {% for scene, count in visuals.scene_analysis.scene_types.items() %}
              <span class="scene-tag">{{ scene }} ({{ count }})</span>
            {% endfor %}
          </div>
        </section>
        {% endif %}

        <section class="scorecard">
          {% for section in rec.scorecard %}
            <article class="section-card">
              <div class="section-top">
                <h3>{{ section.name }}</h3>
                <span class="pill">{{ section.score }}/100</span>
              </div>
              {% if section.fixes %}
                <ul class="compact">
                  {% for fix in section.fixes %}
                    <li>{{ fix }}</li>
                  {% endfor %}
                </ul>
              {% elif section.positives %}
                <ul class="compact">
                  {% for positive in section.positives %}
                    <li>{{ positive }}</li>
                  {% endfor %}
                </ul>
              {% else %}
                <p class="muted">No issues found.</p>
              {% endif %}
            </article>
          {% endfor %}
        </section>

        <details>
          <summary>Raw report data</summary>
          <pre>{{ report_json }}</pre>
        </details>
      {% endif %}
    </main>
  </body>
</html>
"""


def fmt_number(value):
    if value is None:
        return "Unknown"
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def fmt_duration(seconds):
    if not seconds:
        return "Unknown"
    minutes, secs = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m {secs}s"


def pct(value):
    if value is None:
        return "Unknown"
    try:
        return f"{round(float(value) * 100)}%"
    except (TypeError, ValueError):
        return str(value)


def first_item(value):
    if isinstance(value, list) and value:
        return value[0]
    return value or ""


def label_source(value):
    labels = {
        "video_frames": "sampled video frames",
        "thumbnail": "thumbnail fallback",
        "youtube_transcript": "YouTube spoken-word text",
    }
    return labels.get(value, value or "unknown")


app.jinja_env.globals.update(
    fmt_number=fmt_number,
    fmt_duration=fmt_duration,
    pct=pct,
    first_item=first_item,
    label_source=label_source,
)


@app.route("/", methods=["GET", "POST"])
def index():
    report = None
    report_json = None
    error = None
    submitted_url = ""
    submitted_lang = "en"
    if request.method == "POST":
        submitted_url = request.form.get("url", "").strip()
        submitted_lang = request.form.get("lang", "en").strip() or "en"
        try:
            report = analyze_youtube(submitted_url, caption_lang=submitted_lang)
            report_json = json.dumps(report, indent=2, ensure_ascii=False)
        except Exception as exc:
            error = str(exc)
    return render_template_string(
        HTML_TEMPLATE,
        report=report,
        report_json=report_json,
        error=error,
        submitted_url=submitted_url,
        submitted_lang=submitted_lang,
    )


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

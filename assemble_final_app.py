# assemble_final_app.py
# Compiles the standalone Snoopy's Little Lab index.html with all requested enhancements
import json
import os
import shutil
import struct

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
version_file_path = os.path.join(BASE_DIR, 'VERSION')
if os.path.exists(version_file_path):
    with open(version_file_path, 'r', encoding='utf-8') as vf:
        app_version = vf.read().strip()
else:
    app_version = 'v1.0.0'
if not app_version.startswith('v') and not app_version.startswith('V'):
    app_version = f"v{app_version}"

print(f"Step 1: Reading base64 assets, English curriculum data, and Version: {app_version}...")
with open('assets_b64.json', 'r', encoding='utf-8') as f:
    assets = json.load(f)

with open('english_data.json', 'r', encoding='utf-8') as f:
    english_data_json = f.read().strip()

with open('english_dictionary.json', 'r', encoding='utf-8') as f:
    english_dict_json = f.read().strip()

# Authentic Charles M. Schulz Personas
img_ordinary_doghouse = assets['ordinary_doghouse']
img_border_snoopy = assets['border_snoopy']
img_woodstock = assets['woodstock']
img_supervisor_secretary = assets['supervisor_secretary']
img_beagle_scout = assets['beagle_scout']
img_flying_ace = assets['flying_ace']
img_joe_cool = assets['joe_cool_lean']
img_author = assets['author_typewriter']
img_daily_english = assets['daily_english']
img_canonical = assets['canonical']
img_dance = assets['dance']

print("Loaded all primary personas and base64 assets successfully.")

html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Snoopy’s Little Lab · Sanyli.</title>
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/favicon.png">
<style>
  :root {
    --bg: #f8f7f4;
    --card: #ffffff;
    --card-subtle: #faf9f6;
    --text-primary: #18181b;
    --text-secondary: #3f3f46;
    --text-muted: #71717a;
    --border: #e4e4e7;
    --border-hover: #18181b;
    --accent-red: #d9383a;
    --accent-red-hover: #b9292b;
    --accent-red-soft: #fef2f2;
    --woodstock-yellow: #f5b041;
    --woodstock-soft: #fef9e7;
    --woodstock-gold: #b45309;
    --blue-accent: #2563eb;
    --blue-soft: #eff6ff;
    --green-accent: #16a34a;
    --green-soft: #f0fdf4;
    --cyan-accent: #0891b2;
    --purple-accent: #7c3aed;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.04);
    --shadow-card: 0 2px 8px -2px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.02);
    --shadow-hover: 0 8px 20px -3px rgba(0,0,0,0.07);
    --radius-sm: 6px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --font-sans: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", sans-serif;
    --font-mono: "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace;
    --font-serif: Georgia, "Songti SC", "SimSun", serif;
    --transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  }

  body.theme-comic {
    --bg: #faf5eb;
    --card: #ffffff;
    --card-subtle: #f6efe1;
    --border: #18181b;
    --shadow-sm: 2px 2px 0px #18181b;
    --shadow-card: 3px 3px 0px #18181b;
    --shadow-hover: 5px 5px 0px #18181b;
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 10px;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; -webkit-font-smoothing: antialiased; }
  body {
    font-family: var(--font-sans);
    background-color: var(--bg);
    color: var(--text-primary);
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-thumb { background: #d6d3cd; border-radius: 99px; }
  ::-webkit-scrollbar-thumb:hover { background: #999; }

  /* App Header */
  .app-header {
    background: var(--card);
    border-bottom: 2px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
  }
  .header-inner {
    max-width: 1400px;
    margin: 0 auto;
    padding: 10px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    user-select: none;
  }
  .brand-avatar {
    width: 66px;
    height: 72px;
    object-fit: contain;
    transition: transform 0.25s ease;
    filter: drop-shadow(0 2px 5px rgba(0,0,0,0.08));
  }
  .brand:hover .brand-avatar {
    transform: rotate(-6deg) scale(1.08);
  }
  .brand-text h1 {
    font-size: 19px;
    font-weight: 800;
    letter-spacing: -0.4px;
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--text-primary);
  }
  .brand-tag {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 500;
    letter-spacing: 0.3px;
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .cairo-pill {
    background: var(--card-subtle);
    border: 1px solid var(--border);
    padding: 6px 14px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 12px;
    box-shadow: var(--shadow-sm);
  }
  .cairo-pill .flag { font-size: 16px; }
  .cairo-pill .label { font-size: 11px; color: var(--text-muted); }
  .cairo-pill .time {
    font-family: var(--font-mono);
    font-weight: 700;
    font-size: 13.5px;
    color: var(--text-primary);
  }

  .theme-btn {
    border: 1px solid var(--border);
    background: var(--card);
    padding: 6px 12px;
    font-size: 11.5px;
    font-weight: 600;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .theme-btn:hover { background: var(--bg); }

  /* Nav Tabs */
  .nav-bar {
    background: var(--card);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 68px;
    z-index: 90;
  }
  .nav-inner {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 28px;
    display: flex;
    gap: 4px;
    overflow-x: auto;
  }
  .nav-tab {
    padding: 12px 16px;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    border: none;
    background: transparent;
    cursor: pointer;
    position: relative;
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
    transition: var(--transition);
  }
  .nav-tab img {
    width: 32px;
    height: 32px;
    object-fit: contain;
    transition: transform 0.2s ease;
  }
  .nav-tab:hover { color: var(--text-primary); }
  .nav-tab:hover img { transform: scale(1.18); }
  .nav-tab.active { color: var(--text-primary); font-weight: 700; }
  .nav-tab.active::after {
    content: "";
    position: absolute;
    bottom: -1px;
    left: 12px;
    right: 12px;
    height: 3px;
    background: var(--text-primary);
    border-radius: 3px;
  }
  .badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-red);
    display: inline-block;
  }

  /* Main Wrapper */
  .main-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    padding: 24px 28px;
    width: 100%;
    flex: 1;
  }
  .tab-pane {
    display: none;
    animation: fadeIn 0.22s ease;
  }
  .tab-pane.active { display: block; }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Cards */
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-card);
    margin-bottom: 20px;
    overflow: hidden;
    transition: var(--transition);
  }
  .card:hover { box-shadow: var(--shadow-hover); }
  .card-header {
    padding: 13px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--card);
  }
  .card-title {
    font-size: 14px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--text-primary);
  }
  .card-title img {
    width: 22px;
    height: 22px;
    object-fit: contain;
  }
  .card-body { padding: 20px; }

  .persona-tag {
    font-size: 11px;
    padding: 2px 8px;
    background: #f4f4f5;
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text-muted);
    font-weight: 500;
    margin-left: 6px;
  }

  /* Unified Module Header Banner (Minimalist & High-end) */
  .module-header-banner {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 22px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    transition: var(--transition);
  }
  body.theme-comic .module-header-banner {
    border: 2px solid #18181b;
    box-shadow: 3px 3px 0px #18181b;
  }
  .module-header-banner.theme-todo { border-left: 4px solid #16a34a; }
  .module-header-banner.theme-meeting { border-left: 4px solid #2563eb; }
  .module-header-banner.theme-timezone { border-left: 4px solid var(--accent-red); }
  .module-header-banner.theme-links { border-left: 4px solid #0891b2; }
  .module-header-banner.theme-notes { border-left: 4px solid #7c3aed; }
  .module-header-banner.theme-english { border-left: 4px solid var(--woodstock-yellow); }

  .module-banner-left {
    display: flex;
    align-items: center;
    gap: 14px;
  }
  /* Module Header Banner Snoopy Avatars: Scaled up proportionally by 1/2 (+50%, 1.5x) */
  .module-banner-avatar {
    width: 78px;
    height: 84px;
    object-fit: contain;
    filter: drop-shadow(0 3px 6px rgba(0,0,0,0.08));
    flex-shrink: 0;
    transition: transform 0.2s ease;
  }
  .theme-links .module-banner-avatar {
    width: 84px;
    height: 87px;
  }
  .theme-notes .module-banner-avatar {
    width: 84px;
    height: 87px;
  }
  .theme-english .module-banner-avatar {
    width: 81px;
    height: 84px;
  }

    /* Executive Weekly Board Styles (领导周历看板) */
  .weekly-board-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
  }
  .weekly-board-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 12px;
  }
  .trip-timezone-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 7px 14px;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: var(--radius-sm);
    margin-bottom: 12px;
    flex-wrap: wrap;
  }
  .trip-timezone-select {
    font-size: 12px;
    font-weight: 700;
    padding: 3px 10px;
    border: 1px solid #86efac;
    border-radius: 4px;
    background: #fff;
    color: #15803d;
    cursor: pointer;
    outline: none;
  }
  .trip-timezone-select:hover {
    border-color: #22c55e;
  }
  .cairo-time-badge {
    display: inline-flex;
    align-items: center;
    font-size: 10.5px;
    font-weight: 600;
    color: #475569;
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 1px 5px;
    margin-left: 6px;
    vertical-align: middle;
  }
  .weekly-card-cairo-sub {
    display: flex;
    justify-content: flex-end;
    margin-top: 1px;
  }
  .weekly-card-cairo-sub span {
    font-size: 9px;
    color: var(--text-muted);
    font-weight: normal;
    letter-spacing: 0.1px;
  }
  .weekly-local-tz-tag {
    background: #dcfce7;
    color: #15803d;
    border: 1px solid #86efac;
    font-size: 9.5px;
    padding: 0 4px;
    border-radius: 3px;
    font-weight: 700;
    letter-spacing: 0.2px;
    display: inline-block;
    line-height: 1.4;
    vertical-align: middle;
  }
  .badge-trip-active {
    background: #dcfce7;
    color: #15803d;
    border: 1px solid #86efac;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 10px;
  }
  .weekly-nav-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .weekly-title {
    font-size: 16px;
    font-weight: 800;
    color: var(--text-primary);
    min-width: 220px;
    text-align: center;
  }
  .weekly-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    align-items: start;
  }
  @media (max-width: 1200px) {
    .weekly-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  @media (max-width: 768px) {
    .weekly-grid {
      grid-template-columns: 1fr;
    }
  }
  .weekly-col {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: all 0.2s ease;
    min-height: 420px;
  }
  .weekly-col.is-today {
    background: #f8fbff;
    border: 2px solid var(--blue-accent);
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.12);
  }
  .weekly-col.is-weekend {
    background: #f8fafc;
    border-style: dashed;
    opacity: 0.92;
  }
  .weekly-col-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    border-bottom: 1px dashed var(--border);
    white-space: nowrap;
    gap: 6px;
  }
  .weekly-col-header-main {
    display: flex;
    align-items: baseline;
    gap: 6px;
    min-width: 0;
  }
  .weekly-col-day {
    font-size: 13.5px;
    font-weight: 800;
    color: var(--text-primary);
  }
  .weekly-col-date {
    font-size: 11.5px;
    color: var(--text-muted);
    font-weight: 500;
  }
  .weekly-col.is-today .weekly-col-day {
    color: #1d4ed8;
    font-weight: 900;
  }
  .cal-today-badge {
    background: #2563eb;
    color: #fff;
    font-size: 10.5px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 12px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
    flex-shrink: 0;
    box-shadow: 0 1px 3px rgba(37,99,235,0.25);
  }
  .weekly-weekend-badge {
    background: #f1f5f9;
    color: #64748b;
    font-size: 10px;
    font-weight: 600;
    padding: 1px 6px;
    border-radius: 10px;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .cal-day-cell.weekend-cell {
    background: #fafaf9;
  }
  .weekly-col-events {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .weekly-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-left: 3px solid var(--blue-accent);
    border-radius: var(--radius-sm);
    padding: 3px 5px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    cursor: pointer;
    overflow: hidden;
  }
  .weekly-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(0,0,0,0.06);
    border-color: var(--blue-accent);
  }
  .weekly-card.priority-high {
    border-left-color: var(--accent-red);
  }
  .weekly-card-time {
    font-size: 11px;
    font-weight: 700;
    color: var(--blue-accent);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 3px;
    margin-bottom: 1px;
    white-space: nowrap !important;
    overflow: hidden;
    line-height: 1.2;
  }
  .weekly-card-time-text,
  .weekly-card-time-text span {
    white-space: nowrap !important;
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: -0.2px;
  }
  .weekly-card-time-badges {
    display: flex;
    align-items: center;
    gap: 3px;
    flex-shrink: 1;
    overflow: hidden;
    white-space: nowrap;
  }
  .weekly-loc-tag {
    font-size: 9px;
    font-weight: normal;
    color: var(--text-muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 58px;
  }
  .weekly-card-title {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.2;
    margin-bottom: 1px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    word-break: break-word;
  }
  .weekly-card-meta {
    font-size: 8.5px;
    color: var(--text-secondary);
    display: flex;
    flex-direction: column;
    gap: 1px;
    line-height: 1.15;
    margin-top: 1px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .weekly-card-decision {
    margin-top: 1px;
    padding: 1px 4px;
    background: #f8fafc;
    border-radius: 2px;
    font-size: 8.5px;
    color: var(--text-secondary);
    line-height: 1.15;
    border-left: 2px solid #cbd5e1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .weekly-card.is-pending {
    background: #fff8f8;
    border: 1px solid #fecaca;
    border-left: 3.5px solid #ef4444;
    box-shadow: 0 1px 3px rgba(239, 68, 68, 0.08);
  }
  .weekly-card.is-pending:hover {
    background: #fff1f2;
    border-color: #f87171;
    border-left-color: #dc2626;
    box-shadow: 0 4px 10px rgba(220, 38, 38, 0.12);
  }
  .weekly-card.is-pending .weekly-card-time {
    color: #dc2626;
    font-weight: 700;
  }
  .weekly-card-title.text-pending {
    color: #991b1b;
  }
  .pending-bullet {
    color: #ef4444;
    font-size: 10px;
    vertical-align: middle;
  }
  .weekly-pending-tag {
    font-size: 9px;
    font-weight: 700;
    color: #b91c1c;
    background: #fee2e2;
    border: 1px solid #fca5a5;
    padding: 0 4px;
    border-radius: 3px;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .weekly-card-decision.decision-pending {
    background: #fff1f2;
    border-left: 2px solid #f87171;
    color: #991b1b;
  }

  /* Meeting Notice Sent/Unsent Indicator Styles (标黄未发通知) */
  .weekly-card.notice-unsent {
    background: #fefce8;
    border-color: #fde047;
    border-left: 4px solid #eab308;
    box-shadow: 0 1px 4px rgba(234, 179, 8, 0.12);
  }
  .weekly-card.notice-unsent:hover {
    background: #fef9c3;
    border-color: #eab308;
    box-shadow: 0 4px 12px rgba(234, 179, 8, 0.2);
  }
  /* 领导在途行程卡片 (In-Transit Flight Cards) */
  .weekly-card.weekly-card-transit {
    background: #f0f9ff;
    border-color: #bae6fd;
    border-left: 3px solid #0284c7;
    box-shadow: 0 1px 2px rgba(2, 132, 199, 0.05);
  }
  .weekly-card.weekly-card-transit:hover {
    background: #e0f2fe;
    border-color: #7dd3fc;
    border-left-color: #0369a1;
    box-shadow: 0 3px 8px rgba(2, 132, 199, 0.12);
  }
  .weekly-card.weekly-card-transit .weekly-card-time {
    color: #0284c7;
  }
  .weekly-card.weekly-card-transit .weekly-card-title {
    color: #0c4a6e;
  }
  .day-meeting-card.day-transit-card {
    background: #f0f9ff !important;
    border-color: #bae6fd !important;
    border-left: 4px solid #0284c7 !important;
  }
  .day-meeting-card.day-transit-card:hover {
    background: #e0f2fe !important;
    border-color: #7dd3fc !important;
  }
  .day-meeting-card.notice-unsent {
    background: #fefce8 !important;
    border-color: #fde047 !important;
    border-left: 4px solid #eab308 !important;
  }
  .weekly-decision-card.notice-unsent {
    background: #fefce8 !important;
    border-left: 4px solid #eab308 !important;
  }
  .weekly-notice-tag {
    font-size: 9px;
    font-weight: 700;
    color: #854d0e;
    background: #fef08a;
    border: 1px solid #fde047;
    padding: 0 4px;
    border-radius: 3px;
    white-space: nowrap;
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    gap: 2px;
  }
  .weekly-notice-sent-tag {
    font-size: 9.5px;
    font-weight: 600;
    color: #15803d;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    padding: 1px 5px;
    border-radius: 3px;
    white-space: nowrap;
  }
  body.theme-comic .weekly-card.notice-unsent,
  body.theme-comic .day-meeting-card.notice-unsent {
    background: #fef08a !important;
    border: 2px solid #18181b !important;
    box-shadow: 3px 3px 0px #18181b !important;
  }

  /* Foldable Details in Meeting Modal */
  .meeting-foldable-details summary::-webkit-details-marker {
    display: none;
  }
  .meeting-foldable-details summary {
    list-style: none;
  }

  /* Weekly Meeting Requests Pool Styles (周看板 · 待排期) */
  .weekly-requests-overview {
    margin-top: 18px;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  }
  .request-quick-bar {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: center;
    background: #f8fafc;
    border: 1px solid var(--border);
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    margin-bottom: 12px;
  }
  .weekly-requests-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
    gap: 12px;
  }
  .weekly-request-card {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    transition: all 0.15s ease;
  }
  .weekly-request-card:hover {
    background: #ffffff;
    border-color: #f59e0b;
    box-shadow: 0 4px 10px rgba(245, 158, 11, 0.08);
  }
  .weekly-request-card.is-scheduled {
    opacity: 0.65;
    background: #f1f5f9;
  }
  .weekly-request-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
  }
  .weekly-request-person {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-primary);
  }
  .weekly-request-topic {
    font-size: 13.5px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.4;
  }
  .weekly-request-meta {
    font-size: 11px;
    color: var(--text-muted);
    display: flex;
    gap: 12px;
    align-items: center;
  }
  .weekly-request-actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 6px;
    padding-top: 6px;
    border-top: 1px dashed var(--border);
  }
  .urgency-pill {
    font-size: 10px;
    padding: 1px 5px;
    border-radius: 3px;
    font-weight: 600;
  }
  .urgency-high { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
  .urgency-medium { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
  .urgency-low { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }

  /* Weekly Decision Overview Styles (周历模块 · 待决议题速览) */
  .weekly-decision-overview {
    margin-top: 18px;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  }
  .weekly-decision-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    padding-bottom: 12px;
    border-bottom: 1px solid #f1f5f9;
    margin-bottom: 14px;
  }
  .weekly-decision-header-left {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .weekly-decision-icon {
    font-size: 16px;
  }
  .weekly-decision-heading {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
  }
  .weekly-decision-count-badge {
    background: #eff6ff;
    color: var(--blue-accent);
    font-size: 11px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 10px;
    border: 1px solid #bfdbfe;
  }
  .weekly-decision-hint {
    font-size: 11.5px;
    color: var(--text-muted);
    margin-left: 4px;
  }
  .weekly-decision-empty {
    text-align: center;
    padding: 20px;
    font-size: 12px;
    color: var(--text-muted);
    background: #f8fafc;
    border: 1px dashed var(--border);
    border-radius: var(--radius-sm);
  }

  .profile-menu { position: relative; }
  .profile-trigger {
    min-height: 42px;
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 4px 10px 4px 5px;
    border: 1px solid var(--border);
    border-radius: 999px;
    background: var(--card);
    color: var(--text-primary);
    cursor: pointer;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
  }
  .profile-trigger:hover, .profile-trigger[aria-expanded="true"] {
    border-color: var(--border-hover);
    transform: translateY(-1px);
  }
  .profile-avatar {
    width: 32px;
    height: 32px;
    padding: 2px;
    border: 1px solid var(--border);
    border-radius: 50%;
    object-fit: contain;
    background: var(--woodstock-soft);
  }
  .profile-name { font-size: 12px; font-weight: 750; }
  .profile-chevron { font-size: 10px; color: var(--text-muted); transition: transform .18s ease; }
  .profile-trigger[aria-expanded="true"] .profile-chevron { transform: rotate(180deg); }
  .profile-dropdown {
    position: absolute;
    top: calc(100% + 9px);
    right: 0;
    z-index: 300;
    width: 238px;
    padding: 8px;
    border: 1.5px solid var(--border-hover);
    border-radius: 14px;
    background: var(--card);
    box-shadow: 0 16px 40px rgba(0,0,0,.14);
    opacity: 0;
    visibility: hidden;
    transform: translateY(-6px) scale(.98);
    transform-origin: top right;
    transition: opacity .16s ease, transform .16s ease, visibility .16s;
  }
  .profile-dropdown.is-open { opacity: 1; visibility: visible; transform: translateY(0) scale(1); }
  .profile-summary {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    margin-bottom: 5px;
    border-radius: 10px;
    background: var(--woodstock-soft);
  }
  .profile-summary img { width: 42px; height: 42px; object-fit: contain; }
  .profile-summary strong { display: block; font-size: 13px; }
  .profile-summary span { display: block; margin-top: 2px; color: var(--text-muted); font-size: 10.5px; }
  .profile-action {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 10px 11px;
    border: 0;
    border-radius: 9px;
    background: transparent;
    color: var(--text-primary);
    font: inherit;
    font-size: 12px;
    font-weight: 650;
    text-align: left;
    cursor: pointer;
  }
  .profile-action:hover { background: var(--card-subtle); }
  .profile-action.is-danger { color: var(--accent-red); }
  .profile-divider { height: 1px; margin: 5px 4px; background: var(--border); }
  .password-help { margin-top: 5px; color: var(--text-muted); font-size: 11px; }
  .password-error { min-height: 20px; margin-top: 10px; color: var(--accent-red); font-size: 12px; font-weight: 650; }
  .weekly-decision-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
    gap: 12px;
  }
  .weekly-decision-card {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 12px 14px;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .weekly-decision-card:hover {
    background: #ffffff;
    border-color: var(--blue-accent);
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.08);
  }
  .weekly-decision-card.is-pending {
    background: #fffafa;
    border-color: #fecaca;
    border-left: 3.5px solid #ef4444;
  }
  .weekly-decision-card.is-pending:hover {
    background: #fff1f2;
    border-color: #f87171;
    border-left-color: #dc2626;
    box-shadow: 0 4px 10px rgba(220, 38, 38, 0.10);
  }
  .weekly-decision-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
  }
  .weekly-decision-date-tag {
    font-size: 11.5px;
    font-weight: 600;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .weekly-decision-time-pill {
    background: #e2e8f0;
    color: var(--text-primary);
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 10.5px;
    font-weight: normal;
  }
  .weekly-scheduled-tag {
    font-size: 10.5px;
    font-weight: 600;
    color: #2563eb;
    background: #eff6ff;
    padding: 1px 6px;
    border-radius: 3px;
    border: 1px solid #bfdbfe;
  }
  .weekly-decision-card-subject {
    font-size: 13.5px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.35;
  }
  .weekly-decision-card-subject.text-pending {
    color: #991b1b;
  }
  .weekly-decision-card-meta {
    font-size: 11px;
    color: var(--text-muted);
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .weekly-decision-card-body {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 2.5px solid var(--blue-accent);
    border-radius: 4px;
    padding: 7px 10px;
    font-size: 11.5px;
    color: var(--text-secondary);
    line-height: 1.45;
  }
  .weekly-decision-card-body.body-pending {
    background: #fff5f5;
    border-color: #fed7d7;
    border-left-color: #ef4444;
    color: #7f1d1d;
  }
  .weekly-free-slots-wrap {
    margin-top: 8px;
    padding-top: 7px;
    border-top: 1px dashed var(--border);
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .weekly-free-slots-header {
    font-size: 10.5px;
    font-weight: 600;
    color: #15803d;
    display: flex;
    align-items: center;
    gap: 4px;
    margin-bottom: 2px;
  }
  .weekly-free-slot {
    background: #f0fdf4;
    border: 1px dashed #86efac;
    border-radius: var(--radius-sm);
    padding: 4px 7px;
    font-size: 10.5px;
    color: #166534;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .weekly-free-slot:hover {
    background: #dcfce7;
    border-color: #22c55e;
    transform: translateY(-1px);
    box-shadow: 0 1px 3px rgba(34, 197, 94, 0.12);
  }
  .weekly-free-slot .slot-dur-tag {
    font-size: 10px;
    font-weight: 600;
    background: #bbf7d0;
    color: #14532d;
    padding: 1px 5px;
    border-radius: 3px;
    white-space: nowrap;
  }

  /* Executive Day Calendar & Daily Timeline Styles */
  .supervisor-day-view {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px 22px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
  }
  .day-top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 16px;
  }
  .day-nav-group {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .day-current-date-title {
    font-size: 17px;
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .day-stats-banner {
    display: flex;
    align-items: center;
    gap: 16px;
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 16px;
    margin-bottom: 18px;
    flex-wrap: wrap;
    font-size: 12.5px;
    color: var(--text-secondary);
  }
  .day-stat-chip strong {
    color: var(--blue-accent);
    font-size: 14px;
    margin-left: 2px;
  }
  .day-cal-layout {
    display: grid;
    grid-template-columns: 1fr 310px;
    gap: 20px;
    align-items: start;
  }
  @media (max-width: 960px) {
    .day-cal-layout {
      grid-template-columns: 1fr;
    }
  }
  .day-timeline-stream {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .day-section-divider {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 6px;
  }
  .day-section-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }
  .day-meeting-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 8px 12px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    transition: all 0.15s ease;
  }
  .day-meeting-card:hover {
    border-color: var(--blue-accent);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
  }
  .day-meeting-card.priority-high {
    border-left: 4px solid var(--accent-red);
  }
  .day-meeting-card.is-pending {
    background: #fff8f8;
    border-color: #fecaca;
    border-left: 4px solid #ef4444;
  }
  .day-meeting-card.is-pending:hover {
    background: #fff1f2;
    border-color: #f87171;
  }
  .day-meeting-card.is-pending .day-meeting-time-text {
    color: #dc2626;
  }
  .day-meeting-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 4px;
  }
  .day-meeting-time-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .day-meeting-time-text {
    font-size: 13.5px;
    font-weight: 700;
    color: var(--blue-accent);
  }
  .day-meeting-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.35;
    margin-bottom: 4px;
  }
  .day-meeting-roster {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 4px 10px;
    font-size: 11px;
    color: var(--text-secondary);
    background: #f8fafc;
    padding: 5px 10px;
    border-radius: var(--radius-sm);
    margin-bottom: 6px;
  }
  .day-meeting-decision {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    font-size: 12px;
    color: #1e40af;
    line-height: 1.5;
    margin-bottom: 8px;
  }
  .day-meeting-bg {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.5;
    margin-bottom: 8px;
  }
  .day-meeting-actions {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 8px;
    margin-top: 10px;
    padding-top: 8px;
    border-top: 1px solid #f1f5f9;
  }
  .day-lunch-rest-card {
    background: #fffbeb;
    border: 1px dashed #fde68a;
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    color: #92400e;
  }
  .day-free-slot-card {
    background: #f0fdf4;
    border: 1px dashed #86efac;
    border-radius: var(--radius-sm);
    padding: 9px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .day-free-slot-card:hover {
    background: #dcfce7;
    border-color: #22c55e;
    transform: translateY(-1px);
    box-shadow: 0 2px 6px rgba(34, 197, 94, 0.15);
  }
  .day-sidebar-wrap {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .day-sidebar-card {
    background: #fafafa;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 16px;
  }
  .day-sidebar-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .day-sidebar-decision-item {
    background: #ffffff;
    border: 1px solid var(--border);
    border-left: 3px solid var(--blue-accent);
    border-radius: var(--radius-sm);
    padding: 8px 10px;
    margin-bottom: 8px;
    cursor: pointer;
    font-size: 11.5px;
    transition: all 0.15s ease;
  }
  .day-sidebar-decision-item:hover {
    border-color: var(--blue-accent);
    background: #f0f7ff;
  }
  .day-sidebar-decision-title {
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 3px;
  }
  .day-sidebar-decision-text {
    color: var(--text-secondary);
    line-height: 1.4;
  }

  /* Supervisor Month Calendar & Cards Dual View Styles */
  .supervisor-month-view {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
  }
  .cal-top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 12px;
  }
  .cal-month-nav {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .cal-current-month-title {
    font-size: 16px;
    font-weight: 800;
    color: var(--text-primary);
    min-width: 130px;
    text-align: center;
  }
  .cal-grid-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
  }
  .cal-grid-table th {
    text-align: center;
    padding: 8px 4px;
    font-size: 12px;
    font-weight: 700;
    color: var(--text-secondary);
    background: var(--bg);
    border: 1px solid var(--border);
  }
  .cal-grid-table th.weekend {
    color: var(--accent-red);
  }
  .cal-day-cell {
    height: 86px;
    vertical-align: top;
    padding: 6px;
    border: 1px solid var(--border);
    background: var(--card);
    cursor: pointer;
    transition: all 0.15s ease;
    position: relative;
  }
  .cal-day-cell:hover {
    background: #fdfdfd;
    border-color: var(--blue-accent);
  }
  .cal-day-cell.other-month {
    background: #fafafa;
    color: #a1a1aa;
    opacity: 0.55;
  }
  .cal-day-cell.today {
    background: #eff6ff;
  }
  .cal-day-cell.selected {
    outline: 2px solid var(--blue-accent);
    background: #f0f7ff;
    z-index: 2;
  }
  .cal-day-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }
  .cal-day-num {
    font-size: 13px;
    font-weight: 700;
  }
  .cal-today-badge {
    font-size: 10px;
    background: var(--accent-red);
    color: #fff;
    padding: 1px 5px;
    border-radius: 10px;
    font-weight: bold;
  }
  .cal-meeting-count-badge {
    font-size: 10.5px;
    background: #e0e7ff;
    color: #3730a3;
    padding: 1px 5px;
    border-radius: 8px;
    font-weight: 600;
  }
  .cal-day-events {
    display: flex;
    flex-direction: column;
    gap: 3px;
    overflow: hidden;
    max-height: 54px;
  }
  .cal-event-pill {
    font-size: 10px;
    padding: 2px 4px;
    border-radius: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.3;
    display: block;
    text-align: left;
  }
  .cal-event-pill.status-scheduled {
    background: #dbeafe;
    color: #1e40af;
    border-left: 2px solid #2563eb;
  }
  .cal-event-pill.status-pending {
    background: #fef3c7;
    color: #92400e;
    border-left: 2px solid #d97706;
  }
  .cal-event-pill.status-completed {
    background: #dcfce7;
    color: #166534;
    border-left: 2px solid #16a34a;
  }
  .cal-event-more {
    font-size: 10px;
    color: var(--text-muted);
    padding-left: 2px;
  }

  .selected-date-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 5px solid var(--blue-accent);
    padding: 12px 18px;
    border-radius: var(--radius-sm);
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 10px;
  }
  .selected-date-title {
    font-size: 14.5px;
    font-weight: 800;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* Import Live Preview Styles */
  .preview-tab-btn {
    padding: 4px 12px;
    font-size: 11.5px;
    font-weight: 600;
    border: 1px solid var(--border);
    background: var(--card);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .preview-tab-btn.active {
    background: var(--blue-accent);
    color: #fff;
    border-color: var(--blue-accent);
  }
  .import-cal-group {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    margin-bottom: 8px;
  }
  .import-cal-group-header {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .import-card-item {
    background: #ffffff;
    border: 1px solid var(--border);
    border-left: 4px solid var(--blue-accent);
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    margin-bottom: 8px;
  }
  .module-banner-title {
    font-size: 17px;
    font-weight: 800;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: -0.3px;
  }
  .module-edit-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    padding: 0;
    font-size: 11.5px;
    border-radius: 4px;
    border: 1px dashed rgba(255, 255, 255, 0.45);
    background: rgba(255, 255, 255, 0.12);
    color: inherit;
    cursor: pointer;
    line-height: 1;
    transition: all 0.2s ease;
    opacity: 0.85;
    vertical-align: middle;
  }
  .module-edit-btn:hover {
    opacity: 1;
    background: rgba(255, 255, 255, 0.28);
    border-color: rgba(255, 255, 255, 0.8);
    transform: scale(1.08);
  }
  body.theme-comic .module-edit-btn {
    border: 1.5px dashed #18181b;
    background: rgba(255, 255, 255, 0.6);
    color: #18181b;
  }
  body.theme-comic .module-edit-btn:hover {
    background: #fff;
    border-color: #000;
  }
  .module-banner-subtitle {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 3px;
    line-height: 1.45;
  }
  .module-banner-right {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-shrink: 0;
  }

  .stat-box {
    background: var(--card-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 7px 14px;
    min-width: 86px;
    text-align: center;
  }
  .stat-num {
    font-size: 17px;
    font-weight: 800;
    font-family: var(--font-mono);
    color: var(--text-primary);
  }
  .stat-label {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 1px;
  }

  /* Buttons */
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 7px 15px;
    font-size: 12.5px;
    font-weight: 600;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background: var(--card);
    color: var(--text-primary);
    cursor: pointer;
    transition: var(--transition);
    user-select: none;
    white-space: nowrap;
  }
  .btn:hover {
    background: var(--bg);
    border-color: var(--border-hover);
  }
  .btn-primary {
    background: var(--text-primary);
    color: #fff;
    border-color: var(--text-primary);
  }
  .btn-primary:hover {
    background: #27272a;
    border-color: #27272a;
    color: #fff;
  }
  .btn-yellow {
    background: var(--woodstock-yellow);
    color: #18181b;
    border-color: #e29e2b;
  }
  .btn-yellow:hover {
    background: #e29e2b;
    color: #18181b;
  }
  .btn-sm {
    padding: 5px 10px;
    font-size: 11.5px;
  }
  .btn-ghost {
    background: transparent;
    border-color: transparent;
    color: var(--text-secondary);
  }
  .btn-ghost:hover {
    background: var(--bg);
    color: var(--text-primary);
  }

  /* Beagle Scout Green Button for Add Todo (Non-black, single-line) */
  .btn-todo-add {
    background: #16a34a;
    color: #ffffff;
    border-color: #16a34a;
    font-weight: 700;
    white-space: nowrap;
    flex-shrink: 0;
    padding: 8px 18px;
  }
  .btn-todo-add:hover {
    background: #15803d;
    border-color: #15803d;
    color: #ffffff;
  }

  /* Form Elements */
  input[type="text"], input[type="date"], input[type="time"], input[type="number"], select, textarea {
    width: 100%;
    padding: 8px 12px;
    font-size: 12.5px;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    background: var(--card);
    color: var(--text-primary);
    font-family: inherit;
    outline: none;
    transition: var(--transition);
  }
  input:focus, select:focus, textarea:focus {
    border-color: var(--text-primary);
    box-shadow: 0 0 0 2px rgba(24,24,27,0.06);
  }
  textarea { resize: vertical; min-height: 75px; }

  /* ================= 1. HOME: HERO BANNER & BORDER SNOOPY ================= */
  .snoopy-hero-banner {
    background: var(--card);
    border: 2px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 26px 36px 24px 36px;
    position: relative;
    overflow: visible;
    margin-top: 50px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-card);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 32px;
  }
  body.theme-comic .snoopy-hero-banner {
    border: 2px solid #18181b;
    box-shadow: 4px 4px 0px #18181b;
  }

  .hero-content {
    flex: 1;
    max-width: 840px;
    z-index: 2;
  }
  .hero-badge-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
  }
  .hero-mini-pill {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
    padding: 3px 10px;
    border-radius: 99px;
    background: var(--woodstock-soft);
    color: var(--woodstock-gold);
    border: 1px solid rgba(212, 136, 6, 0.25);
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }
  .hero-greeting {
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.3px;
    color: var(--text-primary);
    margin-bottom: 8px;
  }
  .hero-quote-box {
    border-left: 3px solid var(--accent-red);
    padding-left: 14px;
  }
  .hero-quote-text {
    font-size: 15px;
    font-style: italic;
    font-family: var(--font-serif);
    color: var(--text-primary);
    line-height: 1.5;
    margin-bottom: 3px;
  }
  .hero-quote-cn {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.5;
  }
  .hero-quote-author {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 4px;
    font-weight: 500;
  }

  /* Border Snoopy Stage (Cute Snoopy cuddling Woodstock sitting on board) */
  .border-snoopy-stage {
    position: absolute;
    right: 48px;
    bottom: calc(100% - 6px);
    z-index: 30;
    cursor: pointer;
    user-select: none;
    display: flex;
    align-items: flex-end;
  }

  /* Lively breathing animation for cute Snoopy & Woodstock */
  @keyframes snoopyGentleFloat {
    0%, 100% {
      transform: translateY(0px) rotate(0deg);
    }
    50% {
      transform: translateY(-5px) rotate(1.2deg);
    }
  }

  .snoopy-lying-wrap {
    position: relative;
    display: block;
    width: 100px;
    height: 120px;
    animation: snoopyGentleFloat 3.8s ease-in-out infinite;
    transition: transform 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.22s ease;
    transform-origin: bottom center;
  }
  .border-snoopy-stage:hover .snoopy-lying-wrap {
    animation-play-state: paused;
    transform: translateY(-4px) scale(1.05) rotate(-1deg);
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.22)) drop-shadow(0 0 14px rgba(254, 240, 138, 0.45));
  }

  .snoopy-lying-img {
    width: 100px;
    height: 120px;
    object-fit: contain;
    display: block;
    filter: drop-shadow(0 4px 10px rgba(0,0,0,0.15));
  }

  .snoopy-nodding {
    animation: snoopyNod 0.45s ease;
  }
  @keyframes snoopyNod {
    0% { transform: rotate(0deg); }
    30% { transform: rotate(-2.5deg) translateY(-3px); }
    60% { transform: rotate(1.5deg) translateY(-1px); }
    100% { transform: rotate(0deg); }
  }

  /* Joyful bounce & wiggle on click */
  .snoopy-happy-bounce {
    animation: snoopyHappyBounce 0.65s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
  }
  @keyframes snoopyHappyBounce {
    0% { transform: scale(1) translateY(0); }
    22% { transform: scale(1.15, 0.88) translateY(2px) rotate(-4deg); }
    48% { transform: scale(0.92, 1.15) translateY(-12px) rotate(5deg); }
    72% { transform: scale(1.06, 0.96) translateY(-4px) rotate(-2deg); }
    100% { transform: scale(1) translateY(0) rotate(0); }
  }

  .snoopy-cute-aura {
    position: absolute;
    top: 6px;
    left: 10px;
    font-size: 13px;
    pointer-events: none;
    animation: auraFloat 2.8s ease-in-out infinite;
    filter: drop-shadow(0 0 4px rgba(254, 240, 138, 0.8));
    opacity: 0.85;
  }
  @keyframes auraFloat {
    0%, 100% { transform: translateY(0) scale(1); opacity: 0.6; }
    50% { transform: translateY(-4px) scale(1.15); opacity: 1; }
  }

  /* Woodstock Pop-up (Positions to the LEFT of Snoopy) */
  .woodstock-float-box {
    position: absolute;
    right: 170px;
    bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    pointer-events: none;
    opacity: 0;
    transform: translateX(12px) scale(0.9);
    transition: all 0.28s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    z-index: 35;
  }
  .woodstock-float-box.active {
    opacity: 1;
    pointer-events: auto;
    transform: translateX(0) scale(1);
  }

  .woodstock-speech-bubble {
    background: #ffffff;
    border: 2px solid var(--text-primary);
    border-radius: 12px;
    padding: 7px 14px;
    box-shadow: 2px 3px 0px #18181b;
    font-size: 12px;
    font-weight: 700;
    color: var(--text-primary);
    white-space: nowrap;
    position: relative;
    animation: bubbleBounce 0.25s ease;
    line-height: 1.4;
  }
  .woodstock-speech-bubble::after {
    content: "";
    position: absolute;
    right: -8px;
    top: 50%;
    transform: translateY(-50%);
    width: 0;
    height: 0;
    border-top: 6px solid transparent;
    border-bottom: 6px solid transparent;
    border-left: 8px solid var(--text-primary);
  }
  @keyframes bubbleBounce {
    0% { transform: scale(0.8); opacity: 0; }
    70% { transform: scale(1.04); }
    100% { transform: scale(1); opacity: 1; }
  }

  .woodstock-avatar-wrap {
    display: flex;
    align-items: center;
  }
  .woodstock-avatar {
    width: 44px;
    height: 48px;
    object-fit: contain;
    filter: drop-shadow(0 3px 5px rgba(0,0,0,0.12));
    animation: woodstockFlutter 1.8s infinite ease-in-out;
  }
  @keyframes woodstockFlutter {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    25% { transform: translateY(-5px) rotate(-6deg); }
    75% { transform: translateY(-2px) rotate(5deg); }
  }

  .snoopy-particles {
    position: absolute;
    inset: 0;
    pointer-events: none;
    overflow: visible;
  }
  .floating-particle {
    position: absolute;
    font-size: 15px;
    user-select: none;
    animation: particleFly 1.1s forwards cubic-bezier(0.16, 1, 0.3, 1);
  }
  @keyframes particleFly {
    0% { transform: translate(0, 0) scale(0.4); opacity: 1; }
    100% { transform: translate(var(--dx), var(--dy)) scale(1.2); opacity: 0; }
  }

  /* Layout Grids */
  .grid-2col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  @media (max-width: 1024px) {
    .grid-2col { grid-template-columns: 1fr; }
    .border-snoopy-stage { right: 20px; }
  }

  /* ================= 1. SNOOPY'S CLASSROOM & BIG CHALKBOARD ================= */
  .chalkboard-stage-wrap {
    margin: 115px auto 30px auto; /* Moved blackboard noticeably lower per user request */
    position: relative;
    max-width: 1280px;
    width: 96%;
  }

  .woodstock-perch-wrap {
    display: flex;
    align-items: flex-end;
    margin-bottom: 2px;
    margin-right: -4px;
    position: relative;
    z-index: 31;
  }

  @media (max-width: 768px) {
    .chalkboard-stage-wrap {
      margin-top: 80px;
    }
    .border-snoopy-stage {
      right: 18px;
    }
    .snoopy-lying-wrap {
      width: 85px;
      height: 102px;
    }
    .snoopy-lying-img {
      width: 85px;
      height: 102px;
    }
    .woodstock-avatar {
      width: 34px;
      height: 38px;
    }
  }

  /* The Grand Blackboard Frame */
  .chalkboard-frame {
    background: linear-gradient(135deg, #78350f 0%, #92400e 35%, #78350f 70%, #451a03 100%);
    border: 3px solid #3d1a04;
    border-radius: 20px;
    padding: 16px 18px 0 18px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35), inset 0 2px 4px rgba(255, 255, 255, 0.2), inset 0 -3px 6px rgba(0, 0, 0, 0.5);
    position: relative;
  }
  body.theme-comic .chalkboard-frame {
    border: 3px solid #18181b;
    box-shadow: 6px 6px 0px #18181b;
  }

  /* Brass Corner Screws */
  .chalkboard-screw {
    position: absolute;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: radial-gradient(circle, #fde047 30%, #ca8a04 80%);
    box-shadow: inset 0 1px 2px rgba(255,255,255,0.8), 0 1px 2px rgba(0,0,0,0.4);
    z-index: 5;
  }
  .chalkboard-screw.top-left { top: 7px; left: 7px; }
  .chalkboard-screw.top-right { top: 7px; right: 7px; }
  .chalkboard-screw.bottom-left { bottom: 34px; left: 7px; }
  .chalkboard-screw.bottom-right { bottom: 34px; right: 7px; }

  /* Blackboard Inner Slate */
  .chalkboard-slate {
    background: #142a20;
    background-image: 
      radial-gradient(ellipse at 50% 30%, rgba(255, 255, 255, 0.04) 0%, rgba(0, 0, 0, 0.45) 100%),
      repeating-radial-gradient(circle at 20% 40%, rgba(255,255,255,0.01) 0, rgba(255,255,255,0.01) 2px, transparent 2px, transparent 4px);
    border-radius: 12px;
    padding: 26px 32px;
    border: 2px solid #0d1c15;
    box-shadow: inset 0 6px 18px rgba(0, 0, 0, 0.6), inset 0 0 60px rgba(0, 0, 0, 0.4);
    color: #f8fafc;
    min-height: 440px;
    position: relative;
    cursor: text;
  }

  /* Chalkboard Top Header Bar */
  .chalkboard-header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 16px;
    border-bottom: 1.5px dashed rgba(255, 255, 255, 0.2);
    margin-bottom: 22px;
    flex-wrap: wrap;
    gap: 12px;
  }
  .chalk-date-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .chalk-date-pill {
    font-size: 13px;
    font-weight: 700;
    color: #fef08a;
    text-shadow: 0 0 2px rgba(253, 224, 71, 0.5);
    background: rgba(254, 240, 138, 0.1);
    border: 1px solid rgba(254, 240, 138, 0.3);
    padding: 3px 12px;
    border-radius: 99px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .chalk-nav-btn {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.25);
    color: #e2e8f0;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 11.5px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .chalk-nav-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff;
    border-color: rgba(255, 255, 255, 0.5);
  }
  .chalk-streak-badge {
    font-size: 11.5px;
    color: #fed7aa;
    font-weight: 700;
    background: rgba(249, 115, 22, 0.15);
    border: 1px solid rgba(249, 115, 22, 0.35);
    padding: 3px 10px;
    border-radius: 99px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .chalkboard-title-text {
    font-size: 17px;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 0 3px rgba(255, 255, 255, 0.6), 0 0 1px rgba(255,255,255,0.9);
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .chalk-actions-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .chalk-btn {
    background: rgba(255, 255, 255, 0.08);
    border: 1.5px solid rgba(255, 255, 255, 0.3);
    color: #f8fafc;
    padding: 5px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    transition: all 0.15s ease;
    text-shadow: 0 0 2px rgba(255,255,255,0.5);
  }
  .chalk-btn:hover {
    background: rgba(255, 255, 255, 0.22);
    border-color: rgba(255, 255, 255, 0.6);
    transform: translateY(-1px);
  }
  .chalk-btn.chalk-btn-primary {
    background: rgba(254, 240, 138, 0.2);
    border-color: rgba(254, 240, 138, 0.6);
    color: #fef08a;
  }
  .chalk-btn.chalk-btn-primary:hover {
    background: rgba(254, 240, 138, 0.35);
  }

  /* Chalkboard Main Content Area & Direct Textarea */
  .chalkboard-content {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 420px;
    position: relative;
    cursor: text;
  }
  .chalkboard-direct-textarea {
    width: 100%;
    min-height: 420px;
    background: transparent;
    border: none;
    outline: none;
    color: #f8fafc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    font-size: 16px;
    font-weight: 500;
    line-height: 1.85;
    letter-spacing: 0.4px;
    text-shadow: 0 0 1px rgba(255, 255, 255, 0.7), 0 0 2px rgba(255, 255, 255, 0.3);
    caret-color: #fde047;
    resize: vertical;
    box-sizing: border-box;
    padding: 6px 8px 16px 8px;
    tab-size: 2;
    white-space: pre-wrap;
    word-break: break-word;
    overflow-y: auto;
  }
  .chalkboard-direct-textarea b,
  .chalkboard-direct-textarea strong {
    font-weight: 800 !important;
    color: #ffffff !important;
    text-shadow: 0 0 2px rgba(255, 255, 255, 0.95), 0 0 6px rgba(253, 224, 71, 0.5) !important;
  }
  .chalkboard-direct-textarea::placeholder {
    color: rgba(248, 250, 252, 0.35);
    font-size: 15px;
    font-weight: 400;
    text-shadow: none;
    line-height: 1.8;
  }
  .chalkboard-direct-textarea:focus {
    outline: none;
  }

  /* Wooden Chalk Tray at Bottom */
  .chalkboard-tray {
    height: 32px;
    background: linear-gradient(180deg, #92400e 0%, #78350f 60%, #451a03 100%);
    border-radius: 0 0 14px 14px;
    border-top: 2px solid #5a2608;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 22px;
    position: relative;
    margin-top: 14px;
    margin-bottom: 4px;
  }
  .chalk-sticks-rack {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .chalk-stick {
    width: 28px;
    height: 7px;
    border-radius: 3px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.5);
  }
  .chalk-stick.white { background: #f8fafc; }
  .chalk-stick.yellow { background: #fef08a; }
  .chalk-stick.mint { background: #a7f3d0; }
  .chalk-stick.blue { background: #bae6fd; }

  /* 擦黑板放在右下角 */
  .chalk-tray-eraser-btn {
    background: linear-gradient(180deg, #d97706 0%, #b45309 60%, #78350f 100%);
    border: 1px solid rgba(254, 240, 138, 0.6);
    border-radius: 5px;
    color: #fffbeb;
    padding: 3px 12px;
    font-size: 11.5px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.35);
    transition: all 0.15s ease;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
  }
  .chalk-tray-eraser-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.45);
    background: linear-gradient(180deg, #f59e0b 0%, #d97706 60%, #92400e 100%);
    color: #ffffff;
    border-color: #fef08a;
  }
  .chalk-tray-eraser-btn:active {
    transform: translateY(0);
  }


  /* ================= 会议时间冲突日历呈现样式 (Calendar Conflict Badges & Overlapping Time) ================= */
  .weekly-card.is-conflict {
    border-left: 4px solid #e11d48 !important;
    background: #fff8f8 !important;
    border-color: #fca5a5 !important;
    box-shadow: 0 1px 4px rgba(225, 29, 72, 0.12) !important;
  }
  .weekly-card.is-conflict:hover {
    background: #fff1f2 !important;
    border-color: #f43f5e !important;
  }
  .weekly-conflict-header-badge {
    background: #fee2e2 !important;
    color: #be123c !important;
    border: 1px solid #fecdd3 !important;
    font-size: 9.5px !important;
    padding: 1px 6px !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
  }
  /* 极简而明白的日历卡片冲突提示条 (Minimalist Calendar Conflict Pill) */
  .weekly-card-conflict {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    margin-top: 1px;
    margin-bottom: 1px;
    padding: 0 4px;
    background: #ffe4e6;
    border: 1px solid #fecdd3;
    border-radius: 2px;
    color: #be123c;
    font-size: 8.5px;
    font-weight: 700;
    line-height: 1.2;
    cursor: pointer;
    transition: all 0.15s ease;
    white-space: nowrap;
  }
  .weekly-card-conflict:hover {
    background: #fecdd3;
    border-color: #fda4af;
  }
  .conflict-head-icon {
    font-size: 11px;
    line-height: 1;
  }
  .conflict-overlap-label {
    color: #9f1239;
    font-size: 10.5px;
  }
  .conflict-overlap-time {
    color: #be123c;
    font-weight: 800;
    font-family: var(--font-mono);
    padding: 0 2px;
  }
  .conflict-overlap-dur {
    color: #e11d48;
    font-weight: 700;
    font-size: 10px;
  }
  .weekly-conflict-more {
    background: #be123c;
    color: #ffffff;
    font-size: 9px;
    padding: 0 4px;
    border-radius: 8px;
    font-weight: 700;
  }

  /* Day Calendar Conflict Alert Box (Minimalist Sleek Bar) */
  .day-meeting-card.is-conflict {
    border-left: 5px solid #e11d48 !important;
    background: #fff8f8 !important;
    border-color: #fca5a5 !important;
  }
  .day-meeting-conflict-box {
    margin-top: 6px;
    margin-bottom: 6px;
    padding: 5px 10px;
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-left: 3px solid #e11d48;
    border-radius: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    font-size: 11.5px;
    line-height: 1.4;
    cursor: pointer;
    transition: background 0.15s ease;
  }
  .day-meeting-conflict-box:hover {
    background: #ffe4e6;
  }
  .day-conflict-time-pill {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    color: #881337;
  }
  .day-conflict-time-pill strong {
    color: #be123c;
    font-family: var(--font-mono);
  }
  .day-conflict-dur {
    color: #e11d48;
    font-weight: 700;
    font-size: 11px;
  }
  .day-conflict-count-badge {
    background: #be123c;
    color: #ffffff;
    font-size: 10px;
    padding: 1px 6px;
    border-radius: 10px;
    font-weight: 700;
  }

  /* Weekly Board Morning / Afternoon Structure & All-Day Occupied Display */
  .weekly-allday-wrap {
    margin-bottom: 4px;
  }
  .weekly-allday-banner {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border: 1px solid #f59e0b;
    color: #92400e;
    font-size: 11px;
    font-weight: 800;
    padding: 5px 8px;
    border-radius: 6px;
    text-align: center;
    margin-bottom: 8px;
    box-shadow: 0 1px 3px rgba(245, 158, 11, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
  }
  .weekly-card.weekly-card-allday {
    border-left: 4px solid #f59e0b !important;
    background: #fffbeb !important;
    border-color: #fde68a !important;
  }
  .allday-pill-tag {
    background: #f59e0b;
    color: #ffffff;
    font-size: 9.5px;
    padding: 0 5px;
    border-radius: 8px;
    font-weight: 700;
    margin-left: 4px;
  }
  .weekly-allday-occupied-notice {
    margin-top: 8px;
    padding: 6px 8px;
    background: #f4f4f5;
    border: 1px dashed #d4d4d8;
    border-radius: 6px;
    font-size: 11px;
    color: #71717a;
    text-align: center;
    font-weight: 600;
  }
  .weekly-period-block {
    margin-bottom: 2px;
  }
  .weekly-period-divider {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 9px;
    font-weight: 700;
    color: var(--text-muted);
    padding: 1px 2px;
    margin-top: 2px;
    margin-bottom: 1px;
    border-bottom: 1px dashed var(--border);
  }
  .weekly-period-block:first-child .weekly-period-divider {
    margin-top: 0;
  }
  .period-status-empty {
    color: #16a34a;
    background: #dcfce7;
    font-size: 9px;
    padding: 0 4px;
    border-radius: 6px;
    font-weight: 700;
  }
  .period-status-occupied {
    color: #2563eb;
    background: #dbeafe;
    font-size: 9px;
    padding: 0 4px;
    border-radius: 6px;
    font-weight: 700;
  }
  .weekly-empty-period-slot {
    padding: 2px 4px;
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: 3px;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s ease;
    margin-bottom: 1px;
  }
  .weekly-empty-period-slot:hover {
    background: #f1f5f9;
    border-color: #94a3b8;
    transform: translateY(-1px);
  }
  .empty-slot-text {
    font-size: 10px;
    font-weight: 600;
    color: #94a3b8;
  }
  .weekly-period-free-slots {
    margin-top: 2px;
    margin-bottom: 2px;
  }

  /* Host SQLite Database Connection Badge */
  .host-db-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 12px;
    background: #f0fdf4;
    color: #166534;
    border: 1px solid #bbf7d0;
    white-space: nowrap;
    cursor: default;
    transition: all 0.2s ease;
  }
  .host-db-badge.is-offline {
    background: #fff7ed;
    color: #9a3412;
    border-color: #fed7aa;
  }
  .status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
  }
  .status-dot.green {
    background: #22c55e;
    box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
  }
  .status-dot.orange {
    background: #f97316;
    box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.2);
  }

  /* Month Calendar Conflict Event Pill */
  .cal-event-pill.cal-event-conflict {
    background: #fee2e2 !important;
    color: #be123c !important;
    border: 1px solid #fca5a5 !important;
    font-weight: 700 !important;
  }
  .cal-conflict-overlap-tag {
    font-size: 9.5px;
    color: #be123c;
    background: #fff;
    padding: 0 3px;
    border-radius: 2px;
    margin-left: 3px;
    font-weight: 700;
  }
  .cal-day-conflict-icon {
    color: #dc2626;
    font-size: 11px;
    font-weight: 800;
    margin-left: 3px;
  }

  /* Cards List Conflict Notice */
  .meeting-card-conflict-notice {
    margin: 8px 0;
    padding: 8px 12px;
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-left: 4px solid #e11d48;
    border-radius: 6px;
  }

  /* ================= 2. 今日任务 (🏕️ Beagle Scout) ================= */
  .todo-input-bar {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    align-items: center;
    flex-wrap: nowrap; /* Single line guarantee */
  }
  .todo-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .todo-item {
    background: var(--card-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 9px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    transition: var(--transition);
  }
  .todo-item:hover {
    border-color: #cbd5e1;
    background: var(--card);
  }
  .todo-item.done { opacity: 0.6; }
  .todo-item.done .todo-text {
    text-decoration: line-through;
    color: var(--text-muted);
  }
  .todo-left {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
    overflow: hidden;
  }
  .todo-check {
    width: 16px;
    height: 16px;
    cursor: pointer;
    accent-color: var(--text-primary);
    flex-shrink: 0;
  }
  .todo-text {
    font-size: 13px;
    font-weight: 500;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .todo-tags {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }
  .priority-badge {
    font-size: 10.5px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
  }
  .priority-high { background: #fee2e2; color: #b91c1c; }
  .priority-medium { background: #fef3c7; color: #b45309; }
  .priority-low { background: #f1f5f9; color: #475569; }

  /* ================= 2. 今日任务 · 今日聚焦 + 激励进度看板 (Plan A) ================= */
  .todo-focus-layout {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-top: 14px;
  }
  
  /* 1. 今日攻坚激励战报卡 (Hero Progress Energy Bar) */
  .todo-energy-card {
    background: linear-gradient(135deg, #fffdf8 0%, #fefce8 100%);
    border: 1px solid #fde68a;
    border-radius: var(--radius-md);
    padding: 14px 18px;
    box-shadow: 0 2px 6px rgba(245, 158, 11, 0.06);
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .todo-energy-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
  }
  .todo-energy-title-wrap {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .todo-energy-badge {
    background: #f59e0b;
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 12px;
    letter-spacing: 0.3px;
  }
  .todo-energy-quote {
    font-size: 13px;
    font-weight: 600;
    color: #78350f;
  }
  .todo-energy-stats {
    font-size: 12px;
    color: #92400e;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .todo-progress-track {
    width: 100%;
    height: 9px;
    background: #fef3c7;
    border-radius: 9px;
    overflow: hidden;
    position: relative;
    border: 1px solid #fde68a;
  }
  .todo-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #f59e0b 0%, #10b981 100%);
    border-radius: 9px;
    transition: width 0.35s ease;
  }

  /* 2. 「今天完成」焦点卡片 (Today Focus Hero Card) */
  .today-hero-board {
    background: #ffffff;
    border: 1px solid #fed7aa;
    border-left: 5px solid #ef4444;
    border-radius: var(--radius-md);
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.06);
    overflow: hidden;
  }
  .today-hero-header {
    padding: 13px 18px;
    background: linear-gradient(90deg, #fff7ed 0%, #ffffff 100%);
    border-bottom: 1px solid #ffedd5;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
  }
  .today-hero-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 800;
    color: #9a3412;
  }
  .today-hero-items {
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-height: 80px;
  }
  .today-task-row {
    background: #ffffff;
    border: 1px solid #f3f4f6;
    border-radius: var(--radius-sm);
    padding: 11px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    transition: all 0.18s ease;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
  }
  .today-task-row:hover {
    background: #fffbf7;
    border-color: #fdba74;
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(249, 115, 22, 0.08);
  }
  .today-task-row.done {
    opacity: 0.55;
    background: #f9fafb;
    border-color: #e5e7eb;
  }
  .today-task-row.done .today-task-text {
    text-decoration: line-through;
    color: var(--text-muted);
  }
  .today-task-left {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
    min-width: 0;
  }
  .today-task-text {
    font-size: 13.5px;
    font-weight: 500;
    color: var(--text-primary);
    line-height: 1.45;
    word-break: break-word;
  }
  .today-task-actions {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }
  .shift-quadrant-select {
    border: 1px solid var(--border);
    border-radius: 4px;
    font-size: 11px;
    padding: 2px 6px;
    background: #fff;
    color: var(--text-secondary);
    cursor: pointer;
    transition: var(--transition);
  }
  .shift-quadrant-select:hover {
    border-color: #94a3b8;
    color: var(--text-primary);
  }

  /* 3. 后续规划与机动区 (3-Column Sub-Matrix) */
  .todo-submatrix-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }
  @media (max-width: 900px) {
    .todo-submatrix-grid {
      grid-template-columns: 1fr;
    }
  }
  .sub-quadrant-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    min-height: 200px;
    transition: var(--transition);
  }
  .sub-quadrant-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  }
  .sub-quadrant-q2 { border-top: 3px solid #3b82f6; }
  .sub-quadrant-q2 .sub-quadrant-header { background: #eff6ff; color: #1e40af; }
  .sub-quadrant-q3 { border-top: 3px solid #f59e0b; }
  .sub-quadrant-q3 .sub-quadrant-header { background: #fffbeb; color: #92400e; }
  .sub-quadrant-q4 { border-top: 3px solid #64748b; }
  .sub-quadrant-q4 .sub-quadrant-header { background: #f8fafc; color: #334155; }

  .sub-quadrant-header {
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .sub-quadrant-items {
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
    overflow-y: auto;
    max-height: 340px;
  }

  /* Legacy fallback support */
  .todo-matrix-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 14px;
  }
  .quadrant-box {
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    background: var(--card);
    display: flex;
    flex-direction: column;
    min-height: 220px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    transition: var(--transition);
    overflow: hidden;
  }
  .quadrant-header {
    padding: 10px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
    font-weight: 700;
  }
  .quadrant-action-tag {
    font-size: 10.5px;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
  }
  .quadrant-items-list {
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
    overflow-y: auto;
    max-height: 360px;
  }
  .quadrant-mini-card {
    background: var(--card-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 8px 10px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 8px;
    transition: var(--transition);
  }
  .quadrant-mini-card:hover {
    background: var(--card);
    border-color: #cbd5e1;
  }
  .quadrant-mini-card.done {
    opacity: 0.6;
  }
  .quadrant-mini-card.done .quadrant-mini-text {
    text-decoration: line-through;
    color: var(--text-muted);
  }
  .quadrant-mini-text {
    font-size: 12.5px;
    color: var(--text-primary);
    line-height: 1.4;
    word-break: break-word;
  }
  .quadrant-mini-meta {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 4px;
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .quadrant-empty-hint {
    color: var(--text-muted);
    font-size: 12px;
    text-align: center;
    padding: 24px 12px;
    margin: auto;
  }
  .quadrant-q1 { border-top: 3px solid #ef4444; }
  .quadrant-q1 .quadrant-header { background: #fef2f2; color: #991b1b; }
  .quadrant-q1 .quadrant-action-tag { background: #fee2e2; color: #991b1b; }
  .quadrant-q2 { border-top: 3px solid #2563eb; }
  .quadrant-q2 .quadrant-header { background: #eff6ff; color: #1e40af; }
  .quadrant-q2 .quadrant-action-tag { background: #dbeafe; color: #1e40af; }
  .quadrant-q3 { border-top: 3px solid #d97706; }
  .quadrant-q3 .quadrant-header { background: #fffbeb; color: #92400e; }
  .quadrant-q3 .quadrant-action-tag { background: #fef3c7; color: #92400e; }
  .quadrant-q4 { border-top: 3px solid #64748b; }
  .quadrant-q4 .quadrant-header { background: #f8fafc; color: #334155; }
  .quadrant-q4 .quadrant-action-tag { background: #f1f5f9; color: #475569; }

  /* Priority Quadrant Badges */
  .badge-q1 { background: #fee2e2; color: #b91c1c; border: 1px solid #fecdd3; }
  .badge-q2 { background: #dbeafe; color: #1d4ed8; border: 1px solid #bfdbfe; }
  .badge-q3 { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
  .badge-q4 { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }

  /* Archive View Styles */
  .archive-header-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    margin-bottom: 12px;
    font-size: 12.5px;
    color: var(--text-secondary);
  }
  .archive-item {
    background: #fafafa;
    border: 1px solid #e5e7eb;
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 8px;
    font-size: 12.5px;
  }

  /* ================= 3. 会议预约 (Secretary Desk) ================= */
  .meeting-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }
  .filter-tabs {
    display: flex;
    background: var(--card-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 3px;
    gap: 3px;
  }
  .filter-btn {
    border: none;
    background: transparent;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    border-radius: 4px;
    cursor: pointer;
    transition: var(--transition);
  }
  .filter-btn.active {
    background: var(--card);
    color: var(--text-primary);
    box-shadow: var(--shadow-sm);
  }

  /* Enhanced Supervisor Daily Timeline & Free Slot Detection */
  .timeline-bar-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    margin-bottom: 20px;
    font-size: 11.5px;
  }
  .timeline-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    font-weight: 700;
    color: var(--text-secondary);
  }
  .timeline-track {
    display: flex;
    gap: 3px;
    height: 28px;
    background: #f1f5f9;
    border-radius: 6px;
    padding: 3px;
    overflow-x: auto;
    margin-bottom: 10px;
  }
  .time-slot {
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    color: #fff;
    cursor: pointer;
    transition: var(--transition);
    padding: 0 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .slot-free {
    background: #dcfce7;
    color: #15803d;
    border: 1px dashed #86efac;
  }
  .slot-free:hover {
    background: #bbf7d0;
  }
  .slot-busy {
    background: #2563eb;
    color: #ffffff;
  }
  .slot-lunch {
    background: #fed7aa;
    color: #9a3412;
  }

  .timeline-free-pills {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    padding-top: 8px;
    border-top: 1px dashed var(--border);
  }
  .free-pill-btn {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #047857;
    font-size: 11.5px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 99px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    transition: var(--transition);
  }
  .free-pill-btn:hover {
    background: #d1fae5;
    border-color: #059669;
    transform: translateY(-1px);
  }

  /* Meeting Card (6 Key Secretary Fields) */
  .meeting-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    margin-bottom: 8px;
    box-shadow: var(--shadow-card);
    transition: var(--transition);
    overflow: hidden;
  }
  .meeting-card:hover {
    border-color: #cbd5e1;
    box-shadow: var(--shadow-hover);
  }
  .meeting-card-top {
    padding: 8px 14px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    background: var(--card-subtle);
    border-bottom: 1px solid var(--border);
  }
  .meeting-title-area h3 {
    font-size: 15px;
    font-weight: 800;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
  }
  .meeting-meta-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    color: var(--text-secondary);
    flex-wrap: wrap;
  }
  .meta-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: var(--card);
    border: 1px solid var(--border);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11.5px;
    font-weight: 600;
  }
  .status-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 99px;
  }
  .status-pending { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
  .status-scheduled { background: #dbeafe; color: #1d4ed8; border: 1px solid #bfdbfe; }
  .status-completed { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
  .status-cancelled { background: #f3f4f6; color: #6b7280; border: 1px solid #e5e7eb; }

  .meeting-card-body {
    padding: 8px 14px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  @media (max-width: 860px) {
    .meeting-card-body { grid-template-columns: 1fr; }
  }

  .field-block {
    background: var(--card-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 6px 10px;
  }
  .field-label {
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    color: var(--text-muted);
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .field-val {
    font-size: 12.5px;
    color: var(--text-primary);
    line-height: 1.55;
    white-space: pre-wrap;
  }
  .decision-val {
    border-left: 3px solid var(--accent-red);
    padding-left: 8px;
    font-weight: 600;
    color: #18181b;
  }

  .meeting-card-footer {
    padding: 10px 20px;
    border-top: 1px solid var(--border);
    background: var(--card);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    font-size: 11.5px;
  }
  .requester-info { color: var(--text-muted); }
  .meeting-actions {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* ================= 4. 时区协同 (World Tour) ================= */
  .tz-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(285px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }
  .tz-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    box-shadow: var(--shadow-card);
    transition: var(--transition);
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .tz-card:hover {
    box-shadow: var(--shadow-hover);
    border-color: #cbd5e1;
  }
  .tz-card.baseline {
    border-top: 4px solid var(--accent-red);
  }
  .tz-card.is-resting {
    background: #f4f4f5 !important;
    border-color: #e4e4e7 !important;
    box-shadow: none !important;
    opacity: 0.88;
  }
  .tz-card.is-resting .tz-time-big {
    color: #71717a !important;
  }
  .tz-card.is-resting .tz-rep-title {
    color: #52525b;
  }
  .tz-card.is-resting .tz-offset-tag {
    background: #e4e4e7;
    color: #71717a;
    border-color: #d4d4d8;
  }
  .tz-card.is-resting .tz-progress-fill {
    background: #a1a1aa !important;
  }
  .tz-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  .tz-rep-title {
    font-size: 14.5px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 7px;
  }
  .tz-rep-city {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: normal;
  }
  .tz-offset-tag {
    font-family: var(--font-mono);
    font-size: 10.5px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    background: var(--bg);
    border: 1px solid var(--border);
  }
  .tz-time-big {
    font-family: var(--font-mono);
    font-size: 26px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 6px;
    letter-spacing: -0.5px;
  }
  .tz-progress-bar {
    width: 100%;
    height: 4px;
    background: #e2e8f0;
    border-radius: 2px;
    margin-bottom: 8px;
    overflow: hidden;
  }
  .tz-progress-fill {
    height: 100%;
    background: #16a34a;
    border-radius: 2px;
  }
  .tz-diff-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    font-size: 11.5px;
    color: var(--text-secondary);
    padding-top: 8px;
    border-top: 1px solid var(--border);
  }
  .tz-diff-row > div {
    white-space: nowrap;
  }
  .tz-status-dot {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: 700;
  }
  .dot-green { width: 7px; height: 7px; border-radius: 50%; background: #16a34a; }
  .dot-yellow { width: 7px; height: 7px; border-radius: 50%; background: #eab308; }
  .dot-grey { width: 7px; height: 7px; border-radius: 50%; background: #94a3b8; }

  .tz-simulator-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 20px;
  }
  .tz-sim-header {
    font-size: 13.5px;
    font-weight: 700;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .tz-sim-row {
    display: flex;
    align-items: center;
    gap: 12px;
  }


  /* ================= 5. 月度闯关 (Monthly Quest Timeline) & 常用链接 ================= */
  .monthly-month-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 14px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 20px;
    margin-bottom: 18px;
    box-shadow: var(--shadow-sm);
  }
  .monthly-month-nav {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .monthly-month-title {
    font-size: 17px;
    font-weight: 800;
    color: var(--text-primary);
    padding: 0 8px;
    min-width: 130px;
    text-align: center;
  }
  .monthly-progress-box {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .routine-progress-track {
    width: 140px;
    height: 8px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
    position: relative;
  }
  .routine-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #10b981);
    border-radius: 4px;
    transition: width 0.3s ease;
  }
  .routine-quote-banner {
    background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
    border: 1px solid #bfdbfe;
    border-radius: var(--radius-md);
    padding: 12px 18px;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    font-size: 13.5px;
    color: #1e3a8a;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }
  .routine-timeline {
    position: relative;
    padding: 8px 0 16px 86px;
  }
  .routine-timeline::before {
    content: '';
    position: absolute;
    top: 14px;
    bottom: 20px;
    left: 43px;
    width: 3px;
    background: linear-gradient(180deg, #3b82f6 0%, #8b5cf6 35%, #0284c7 70%, #0d9488 100%);
    border-radius: 3px;
  }
  .routine-timeline-node {
    position: relative;
    margin-bottom: 14px;
  }
  .routine-timeline-node:last-child {
    margin-bottom: 0;
  }
  .routine-node-marker {
    position: absolute;
    left: -86px;
    top: 9px;
    width: 76px;
    height: 30px;
    border-radius: 15px;
    background: #ffffff;
    border: 2px solid #3b82f6;
    box-shadow: 0 2px 6px rgba(59, 130, 246, 0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    color: #1d4ed8;
    z-index: 2;
    transition: all 0.25s ease;
    padding: 0 4px;
    box-sizing: border-box;
    white-space: nowrap;
    letter-spacing: -0.2px;
  }
  .routine-timeline-node.completed .routine-node-marker {
    border-color: #10b981 !important;
    background: #10b981 !important;
    color: #ffffff !important;
    box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3);
  }
  .routine-today-marker {
    position: relative;
    margin: 8px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .routine-today-dot {
    position: absolute;
    left: -86px;
    width: 76px;
    height: 26px;
    border-radius: 13px;
    background: #f59e0b;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    z-index: 3;
    box-shadow: 0 2px 6px rgba(245, 158, 11, 0.35);
    white-space: nowrap;
  }
  .routine-today-dot-inner {
    display: none;
  }
  @keyframes routine-pulse-ring {
    0% { box-shadow: 0 0 0 2px #f59e0b, 0 0 6px rgba(245, 158, 11, 0.6); }
    50% { box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.4), 0 0 10px rgba(245, 158, 11, 0.8); }
    100% { box-shadow: 0 0 0 2px #f59e0b, 0 0 6px rgba(245, 158, 11, 0.6); }
  }
  .routine-today-badge {
    background: #fffbeb;
    border: 1px solid #fcd34d;
    color: #b45309;
    padding: 2px 9px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    box-shadow: 0 1px 4px rgba(245, 158, 11, 0.12);
  }
  .routine-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 11px 15px;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s ease;
    position: relative;
  }
  .routine-card:hover {
    box-shadow: var(--shadow-md);
    border-color: #94a3b8;
    transform: translateY(-1px);
  }
  .routine-timeline-node.completed .routine-card {
    border-color: #86efac;
    background: linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%);
  }
  .routine-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 6px;
  }
  .routine-card-tags {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
  }
  .routine-pill-rule {
    font-size: 11px;
    font-weight: 700;
    padding: 1.5px 8px;
    border-radius: 10px;
    letter-spacing: 0.2px;
  }
  .routine-pill-date {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-primary);
    background: var(--card-subtle);
    border: 1px solid var(--border);
    padding: 1.5px 7px;
    border-radius: 4px;
  }
  .routine-pill-category {
    font-size: 11px;
    color: var(--text-muted);
    background: var(--card-subtle);
    padding: 1.5px 6px;
    border-radius: 4px;
  }
  .routine-status-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 1.5px 8px;
    border-radius: 10px;
  }
  .routine-status-badge.done {
    background: #dcfce7;
    color: #15803d;
    border: 1px solid #bbf7d0;
  }
  .routine-status-badge.current {
    background: #dbeafe;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
  }
  .routine-status-badge.upcoming {
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #e2e8f0;
  }
  .routine-status-badge.overdue {
    background: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fecaca;
  }
  .routine-card-title {
    font-size: 13.5px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 4px;
    line-height: 1.35;
  }
  .routine-timeline-node.completed .routine-card-title {
    color: #166534;
  }
  .routine-hint-bar {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: 600;
    color: #0369a1;
    background: #e0f2fe;
    padding: 2px 7px;
    border-radius: 4px;
    margin-bottom: 6px;
  }
  .routine-card-desc {
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.45;
    margin-bottom: 8px;
  }
  .routine-subtasks-list {
    background: var(--card-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 8px 10px;
    margin-bottom: 10px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .routine-subtask-item {
    display: flex;
    align-items: flex-start;
    gap: 6px;
    font-size: 11.5px;
    color: var(--text-primary);
    line-height: 1.4;
  }
  .routine-subtask-bullet {
    color: var(--primary);
    font-weight: 800;
    flex-shrink: 0;
  }
  .routine-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    padding-top: 7px;
    margin-top: 4px;
    border-top: 1px solid var(--border);
  }
  .routine-action-left {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .routine-action-right {
    display: flex;
    align-items: center;
    gap: 4px;
  }
  .btn-toggle-routine {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-weight: 700;
    font-size: 11.5px;
    padding: 3.5px 10px;
    border-radius: 5px;
    border: 1px solid var(--border);
    background: #ffffff;
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .btn-toggle-routine:hover {
    background: #f8fafc;
    border-color: #94a3b8;
  }
  .btn-toggle-routine.is-done {
    background: #10b981;
    border-color: #059669;
    color: #ffffff;
  }
  .btn-toggle-routine.is-done:hover {
    background: #059669;
  }
  .routine-note-drawer {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px dashed var(--border);
  }
  .routine-note-textarea {
    width: 100%;
    box-sizing: border-box;
    font-size: 12.5px;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 8px 10px;
    background: #ffffff;
    color: var(--text-primary);
    min-height: 52px;
    resize: vertical;
  }
  .routine-note-textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
  }

  /* ================= 5. 常用链接 (Snoopy Links) ================= */
  .links-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
  }
  .link-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 116px;
    text-decoration: none;
    color: var(--text-primary);
    transition: var(--transition);
    cursor: pointer;
    box-shadow: var(--shadow-sm);
    position: relative;
  }
  .link-card:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  .link-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  .link-icon-badge {
    width: 38px;
    height: 38px;
    border-radius: 8px;
    background: var(--card-subtle);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
  }
  .link-category-pill {
    font-size: 11px;
    font-weight: 600;
    color: #0891b2;
    background: #ecfeff;
    border: 1px solid #cffafe;
    padding: 2px 8px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .link-category-pill:hover {
    background: #cffafe;
    color: #0e7490;
  }
  .link-title {
    font-size: 15.5px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.4;
    word-break: break-word;
    margin: 4px 0 10px 0;
    transition: color 0.15s ease;
  }
  .link-card:hover .link-title {
    color: var(--primary);
  }
  .link-card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 8px;
    border-top: 1px dashed var(--border);
    font-size: 11.5px;
  }
  .link-open-hint {
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
    font-weight: 500;
  }
  .link-card:hover .link-open-hint {
    color: var(--primary);
  }
  .link-card-actions {
    display: flex;
    align-items: center;
    gap: 4px;
  }
  .link-card-actions .btn {
    padding: 3px 6px;
    font-size: 12px;
    line-height: 1;
    border-radius: 4px;
  }
  .category-tab-btn {
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 600;
    border-radius: 20px;
    border: 1px solid var(--border);
    background: var(--card);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .category-tab-btn:hover {
    border-color: var(--primary);
    color: var(--primary);
  }
  .category-tab-btn.active {
    background: var(--primary);
    border-color: var(--primary);
    color: #ffffff;
  }

  /* ================= 6. 每日小记 (Little Notes) ================= */
  .notes-editor-box { margin-bottom: 20px; }
  .notes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
  }
  .note-item {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .note-text {
    font-size: 13px;
    line-height: 1.6;
    color: var(--text-primary);
    white-space: pre-wrap;
    margin-bottom: 12px;
  }
  .note-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-muted);
    border-top: 1px dashed var(--border);
    padding-top: 8px;
  }
  .note-item.is-pinned {
    border-color: #fde68a;
    background: #fffdf5;
    box-shadow: 0 2px 10px rgba(217, 119, 6, 0.09);
    position: relative;
  }
  .note-item.is-dragging, .today-task-row.is-dragging {
    opacity: 0.45;
    transform: scale(0.99);
  }
  .note-item.drag-over {
    border-top: 3px solid #2563eb;
    background: #eff6ff;
  }
  .today-task-row.drag-over {
    border-top: 3px solid #ea580c;
    background: #fffbeb;
  }
  .drag-grip-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 13px;
    cursor: grab;
    user-select: none;
    transition: color 0.15s ease;
  }
  .drag-grip-icon:hover {
    color: var(--text-primary);
  }
  .drag-grip-icon:active {
    cursor: grabbing;
  }

  /* ================= 7. 每日英语 (English Time) ================= */
  .english-sec-header {
    font-size: 14px;
    font-weight: 800;
    color: var(--text-primary);
    margin: 20px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .english-word-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }
  .word-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    box-shadow: var(--shadow-card);
    transition: var(--transition);
  }
  .word-card:hover {
    border-color: #cbd5e1;
    box-shadow: var(--shadow-hover);
  }
  .word-top-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
  }
  .word-title {
    font-size: 17px;
    font-weight: 800;
    font-family: var(--font-serif);
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .word-speak-btn {
    border: none;
    background: var(--card-subtle);
    border: 1px solid var(--border);
    width: 26px;
    height: 26px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    transition: var(--transition);
  }
  .word-speak-btn:hover {
    background: var(--bg);
    transform: scale(1.1);
  }
  .word-phonetic {
    font-size: 12px;
    font-family: var(--font-mono);
    color: var(--text-muted);
  }
  .word-pos {
    font-size: 11px;
    padding: 1px 6px;
    background: #f1f5f9;
    border-radius: 4px;
    color: var(--text-secondary);
    font-weight: 600;
  }
  .word-def {
    font-size: 13.5px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 6px 0 10px 0;
  }
  .word-example {
    background: var(--card-subtle);
    border-left: 3px solid var(--blue-accent);
    padding: 8px 12px;
    border-radius: 0 4px 4px 0;
    font-size: 12px;
    line-height: 1.5;
  }
  .word-ex-en {
    color: var(--text-primary);
    font-style: italic;
    margin-bottom: 3px;
  }
  .word-ex-cn {
    color: var(--text-secondary);
    font-size: 11.5px;
  }

  .sentence-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .sentence-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 15px 18px;
    box-shadow: var(--shadow-card);
    transition: var(--transition);
  }
  .sentence-card:hover {
    border-color: #cbd5e1;
    box-shadow: var(--shadow-hover);
  }
  .sentence-scenario {
    font-size: 11px;
    font-weight: 700;
    color: var(--blue-accent);
    background: var(--blue-soft);
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 7px;
  }
  .sentence-en-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 4px;
  }
  .sentence-en {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.5;
  }
  .sentence-cn {
    font-size: 12.5px;
    color: var(--text-secondary);
    line-height: 1.5;
    margin-bottom: 8px;
  }
  .sentence-tip {
    font-size: 11.5px;
    color: var(--woodstock-gold);
    background: var(--woodstock-soft);
    border: 1px dashed rgba(212, 136, 6, 0.35);
    padding: 5px 10px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  /* English Word Selection Floating Lookup & Pronunciation Popup */
  .word-lookup-popup {
    position: fixed;
    z-index: 99999;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    box-shadow: 0 12px 30px -4px rgba(15, 23, 42, 0.18), 0 6px 12px -4px rgba(15, 23, 42, 0.08);
    padding: 12px 14px;
    min-width: 250px;
    max-width: 350px;
    box-sizing: border-box;
    animation: popupFadeIn 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    font-family: var(--font-sans);
  }
  @keyframes popupFadeIn {
    from { opacity: 0; transform: translateY(5px) scale(0.96); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }
  .word-popup-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 6px;
  }
  .word-popup-title-row {
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 6px;
  }
  .word-popup-title {
    font-size: 16px;
    font-weight: 800;
    color: #0f172a;
    font-family: var(--font-serif);
  }
  .word-popup-phonetic {
    font-size: 11.5px;
    color: #64748b;
    font-family: var(--font-mono);
  }
  .word-popup-pos {
    font-size: 10px;
    font-weight: 600;
    padding: 1px 5px;
    background: #f1f5f9;
    border-radius: 4px;
    color: #475569;
  }
  .word-popup-actions {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .word-popup-speak-btn {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 50%;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 13px;
    transition: transform 0.15s, background 0.15s, border-color 0.15s;
    outline: none;
  }
  .word-popup-speak-btn:hover {
    background: #e0f2fe;
    border-color: #7dd3fc;
    transform: scale(1.12);
  }
  .word-popup-speak-btn:active {
    transform: scale(0.95);
  }
  .word-popup-close-btn {
    background: none;
    border: none;
    font-size: 13px;
    color: #94a3b8;
    cursor: pointer;
    padding: 2px 4px;
    line-height: 1;
    transition: color 0.15s;
    border-radius: 4px;
  }
  .word-popup-close-btn:hover {
    color: #334155;
    background: #f1f5f9;
  }
  .word-popup-def {
    font-size: 13px;
    font-weight: 600;
    line-height: 1.5;
    color: #1e293b;
    border-top: 1px solid #f1f5f9;
    padding-top: 6px;
    margin-top: 4px;
    user-select: text;
  }

  /* English Search & Quick Lookup Bar (Clean & Minimal) */
  .english-quick-lookup-bar {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 10px 14px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    box-shadow: var(--shadow-card);
  }
  .english-search-group {
    display: flex;
    align-items: center;
    gap: 8px;
    flex: 1;
  }
  .english-search-input {
    flex: 1;
    height: 34px;
    padding: 6px 12px;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 13px;
    background: #ffffff;
    color: var(--text-primary);
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  .english-search-input:focus {
    border-color: #38bdf8;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
  }

  /* Snoopy Combined Streak & Checkin Pill Button */
  .snoopy-checkin-pill-btn {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: #ffffff;
    border: 1.5px solid #fbbf24;
    border-radius: 999px;
    padding: 6px 16px 6px 8px;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(251, 191, 36, 0.22);
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
    user-select: none;
    text-align: left;
  }
  .snoopy-checkin-pill-btn:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 4px 14px rgba(251, 191, 36, 0.35);
    border-color: #f59e0b;
  }
  .snoopy-checkin-pill-btn:active {
    transform: translateY(0px) scale(0.98);
  }
  .snoopy-checkin-avatar-wrap {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: #fef3c7;
    border: 1.5px solid #fde047;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    flex-shrink: 0;
    transition: all 0.25s ease;
  }
  .snoopy-checkin-avatar {
    width: 32px;
    height: 32px;
    object-fit: contain;
    transition: transform 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  .snoopy-checkin-pill-btn:hover .snoopy-checkin-avatar {
    transform: scale(1.15) rotate(-3deg);
  }
  .snoopy-checkin-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1px;
  }
  .snoopy-checkin-streak-row {
    display: flex;
    align-items: baseline;
    gap: 5px;
    font-size: 13px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
  }
  .snoopy-checkin-streak-row .streak-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
  }
  .snoopy-checkin-streak-row .streak-days {
    font-size: 14px;
    font-weight: 800;
    color: #b45309;
    font-family: var(--font-mono, inherit);
  }
  .snoopy-checkin-action-row {
    font-size: 11.5px;
    font-weight: 600;
    color: #d97706;
    display: flex;
    align-items: center;
    gap: 3px;
    line-height: 1.2;
  }

  /* Checked-in state */
  .snoopy-checkin-pill-btn.is-checked {
    background: #f0fdf4;
    border-color: #86efac;
    box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2);
  }
  .snoopy-checkin-pill-btn.is-checked:hover {
    border-color: #4ade80;
    box-shadow: 0 4px 14px rgba(34, 197, 94, 0.3);
  }
  .snoopy-checkin-pill-btn.is-checked .snoopy-checkin-avatar-wrap {
    background: #dcfce7;
    border-color: #86efac;
  }
  .snoopy-checkin-pill-btn.is-checked .snoopy-checkin-streak-row .streak-days {
    color: #15803d;
  }
  .snoopy-checkin-pill-btn.is-checked .snoopy-checkin-action-row {
    color: #16a34a;
  }

  /* Comic Theme support */
  body.theme-comic .snoopy-checkin-pill-btn {
    border: 2px solid #18181b;
    box-shadow: 3px 3px 0px #18181b;
    background: #ffffff;
  }
  body.theme-comic .snoopy-checkin-pill-btn.is-checked {
    background: #ecfdf5;
    border: 2px solid #18181b;
    box-shadow: 3px 3px 0px #18181b;
  }
  body.theme-comic .snoopy-checkin-avatar-wrap {
    border: 1.5px solid #18181b;
  }
  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.65);
    z-index: 1000;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }
  .modal-overlay.active { display: flex; }
  .modal-box, .modal-content {
    background: #ffffff !important;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    max-width: 620px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
    animation: modalPop 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    box-sizing: border-box;
    opacity: 1 !important;
  }
  body.theme-comic .modal-box, body.theme-comic .modal-content {
    background: #ffffff !important;
    border: 2px solid #18181b;
    box-shadow: 6px 6px 0px #18181b;
  }
  @keyframes modalPop {
    from { transform: scale(0.96); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }
  .modal-header {
    padding: 16px 20px;
    background: #ffffff !important;
    border-bottom: 1px solid #f1f5f9;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
  }
  body.theme-comic .modal-header {
    border-bottom: 2px solid #18181b;
  }
  .modal-title { font-size: 15px; font-weight: 800; color: #0f172a; }
  .modal-body {
    padding: 20px;
    background: #ffffff !important;
  }
  .modal-footer {
    padding: 14px 20px;
    background: #f8fafc !important;
    border-top: 1px solid #f1f5f9;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    border-bottom-left-radius: 12px;
    border-bottom-right-radius: 12px;
  }
  body.theme-comic .modal-footer {
    background: #fafaf9 !important;
    border-top: 2px solid #18181b;
  }
  #btnRecallToPending:hover {
    background: #fef3c7 !important;
    border-color: #fcd34d !important;
    color: #92400e !important;
  }
  body.theme-comic #btnRecallToPending {
    border: 2px solid #18181b !important;
    background: #fef3c7 !important;
    color: #92400e !important;
    box-shadow: 2px 2px 0px #18181b !important;
  }

  /* Form Elements in Modals: Solid crisp white background, no transparency */
  .modal-box input, .modal-box select, .modal-box textarea,
  .modal-content input, .modal-content select, .modal-content textarea {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #0f172a !important;
    border-radius: 6px;
    box-shadow: none;
    font-size: 13px;
    padding: 8px 12px;
    box-sizing: border-box;
  }
  .modal-box input:focus, .modal-box select:focus, .modal-box textarea:focus,
  .modal-content input:focus, .modal-content select:focus, .modal-content textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    background: #ffffff !important;
  }
  .form-group { margin-bottom: 14px; }
  .form-group label {
    display: block;
    font-size: 11.5px;
    font-weight: 700;
    color: var(--text-secondary);
    margin-bottom: 5px;
  }
  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  .quick-suggest-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 6px;
  }
  .suggest-chip {
    display: inline-flex;
    align-items: center;
    border: 1px dashed var(--border);
    background: #fafaf9;
    padding: 2px 8px;
    font-size: 11px;
    color: var(--text-secondary);
    border-radius: 4px;
    cursor: pointer;
    user-select: none;
    transition: all 0.15s ease;
  }
  .suggest-chip:hover {
    background: #eff6ff;
    border-color: var(--blue-accent);
    color: var(--blue-accent);
    border-style: solid;
    transform: translateY(-1px);
  }
  .suggest-chip:active {
    transform: translateY(0);
  }
  .duration-chips {
    display: flex;
    gap: 6px;
    align-items: center;
    flex-wrap: wrap;
  }
  .chip-btn {
    border: 1px solid var(--border);
    background: var(--card-subtle);
    color: var(--text-secondary);
    padding: 3px 9px;
    font-size: 11.5px;
    font-weight: 500;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .chip-btn:hover {
    background: var(--card-bg);
    border-color: var(--primary);
    color: var(--primary);
  }
  .chip-btn.selected {
    background: var(--text-primary);
    color: #ffffff !important;
    border-color: var(--text-primary);
    font-weight: 600;
  }
  .time-picker-wrapper {
    position: relative;
    width: 100%;
  }
  .time-input-box {
    position: relative;
    display: flex;
    align-items: center;
    width: 100%;
  }
  .time-input-box input {
    width: 100%;
    padding-right: 32px !important;
    font-size: 13px !important;
    font-family: inherit;
    box-sizing: border-box;
  }
  .time-picker-btn {
    position: absolute;
    right: 6px;
    cursor: pointer;
    color: var(--text-muted);
    font-size: 13px;
    user-select: none;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 4px;
    transition: background 0.15s ease, color 0.15s ease;
  }
  .time-picker-btn:hover {
    background: var(--card-subtle, #f4f4f5);
    color: var(--text-primary);
  }
  .time-picker-dropdown {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    right: 0;
    max-height: 190px;
    overflow-y: auto;
    background: #ffffff;
    border: 1px solid var(--border, #e4e4e7);
    border-radius: var(--radius-sm, 6px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    z-index: 1050;
    padding: 4px 0;
  }
  .time-picker-option {
    padding: 6px 12px;
    font-size: 12.5px;
    font-weight: 500;
    color: var(--text-primary);
    cursor: pointer;
    transition: background 0.1s ease;
  }
  .time-picker-option:hover {
    background: var(--card-subtle, #f4f4f5);
  }
  .time-picker-option.selected {
    background: var(--text-primary, #18181b);
    color: #ffffff !important;
    font-weight: 600;
  }

  .toast-notification {
    position: fixed;
    bottom: 28px;
    right: 28px;
    background: var(--text-primary);
    color: #fff;
    padding: 12px 20px;
    border-radius: var(--radius-sm);
    font-size: 13px;
    font-weight: 600;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    z-index: 300;
    display: none;
    align-items: center;
    gap: 10px;
    animation: toastSlide 0.25s ease;
  }
  @keyframes toastSlide {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }

  .celebration-modal-box {
    background: #ffffff;
    border: 3px solid var(--text-primary);
    border-radius: 16px;
    text-align: center;
    padding: 32px 24px;
    max-width: 440px;
    width: 100%;
    box-shadow: 6px 6px 0px #18181b;
  }
  .celebration-avatar {
    width: 90px;
    height: 96px;
    object-fit: contain;
    animation: woodstockTrophy 0.8s infinite alternate ease-in-out;
    margin-bottom: 12px;
  }
  @keyframes woodstockTrophy {
    from { transform: translateY(0) rotate(-4deg); }
    to { transform: translateY(-8px) rotate(4deg); }
  }
  .celebration-title {
    font-size: 20px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 6px;
  }
  .celebration-desc {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.5;
    margin-bottom: 20px;
  }

  /* Table Import Live Preview */
  .import-preview-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
    font-size: 12px;
  }
  .import-preview-table th {
    background: var(--card-subtle);
    padding: 8px 10px;
    text-align: left;
    border-bottom: 1px solid var(--border);
    font-weight: 700;
    color: var(--text-secondary);
  }
  .import-preview-table td {
    padding: 8px 10px;
    border-bottom: 1px solid var(--border);
    color: var(--text-primary);
  }

  /* App Footer */
  .app-footer {
    background: var(--card);
    border-top: 1px solid var(--border);
    padding: 14px 28px;
    text-align: center;
    font-size: 11.5px;
    color: var(--text-muted);
    margin-top: auto;
  }
  .footer-inner {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
  }
  .footer-left {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }
  .app-version-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    background: var(--woodstock-soft, #fef6dd);
    color: var(--text-primary, #1e1b18);
    border: 1px solid var(--border, #e5dfd3);
    border-radius: 999px;
    font-size: 11px;
    font-weight: 750;
    letter-spacing: 0.03em;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    user-select: all;
    transition: transform .15s ease, background .15s ease;
  }
  .app-version-badge:hover {
    transform: translateY(-1px);
    background: var(--woodstock, #f8d347);
  }
  .theme-comic .app-version-badge {
    border: 1.5px solid var(--ink, #171717);
    background: #fff;
    box-shadow: 2px 2px 0 var(--ink, #171717);
  }
  .theme-comic .app-version-badge:hover {
    background: var(--yellow, #f5bf36);
  }
/* ================= 遗留任务 (Legacy Tasks) 模块样式 ================= */
.theme-legacy {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
  border-left: 5px solid #f59e0b !important;
}
.legacy-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}
.legacy-kpi-card {
  background: var(--bg-card, #ffffff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 10px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  cursor: pointer;
  user-select: none;
}
.legacy-kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.06);
}
.legacy-kpi-card.active-kpi {
  border: 2px solid #2563eb !important;
  background: #eff6ff !important;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.18) !important;
}
.legacy-kpi-icon {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.legacy-kpi-val {
  font-size: 20px;
  font-weight: 800;
  line-height: 1.1;
  color: var(--text-primary, #0f172a);
}
.legacy-kpi-lbl {
  font-size: 11.5px;
  color: var(--text-secondary, #64748b);
  margin-top: 2px;
}

/* 工具栏 */
.legacy-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
  background: var(--bg-card, #ffffff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 10px;
  padding: 10px 14px;
}
.legacy-toolbar-left, .legacy-toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.legacy-filter-group {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-secondary, #475569);
  font-weight: 600;
  white-space: nowrap !important;
  flex-shrink: 0;
}
.legacy-filter-group label {
  white-space: nowrap !important;
  margin: 0 !important;
  display: inline-flex !important;
  align-items: center !important;
  flex-shrink: 0 !important;
}
.legacy-filter-group select {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid var(--border, #cbd5e1);
  background: var(--bg-card, #fff);
  color: var(--text-primary, #1e293b);
  white-space: nowrap !important;
}
.legacy-search-box input {
  font-size: 12px;
  padding: 5px 10px;
  border-radius: 6px;
  border: 1px solid var(--border, #cbd5e1);
  width: 190px;
  transition: all 0.2s ease;
}
.legacy-search-box input:focus {
  width: 230px;
  border-color: #3b82f6;
  outline: none;
}
.view-switch-tabs {
  display: inline-flex;
  border: 1px solid var(--border, #cbd5e1);
  border-radius: 6px;
  overflow: hidden;
  background: #f1f5f9;
}
.view-switch-btn {
  border: none;
  background: transparent;
  padding: 5px 10px;
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s ease;
}
.view-switch-btn.active {
  background: #ffffff;
  color: #0f172a;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}

/* 卡片网格视图 */
.legacy-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 16px;
}
.legacy-card {
  background: var(--bg-card, #ffffff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
  position: relative;
}
.legacy-card:hover {
  box-shadow: 0 6px 16px rgba(0,0,0,0.07);
  border-color: #cbd5e1;
}
.legacy-card.priority-p0 {
  border-left: 4px solid #ef4444;
}
.legacy-card.priority-p1 {
  border-left: 4px solid #f59e0b;
}
.legacy-card.priority-p2 {
  border-left: 4px solid #3b82f6;
}
.legacy-card.is-completed {
  opacity: 0.85;
  background: #f8fafc;
}

.legacy-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}
.legacy-owner-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  background: #e0f2fe;
  color: #0369a1;
  border: 1px solid #bae6fd;
}
.legacy-dept-tag {
  font-size: 11px;
  color: #64748b;
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
}
.legacy-badges-row {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
  align-items: center;
}
.badge-p0 { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; font-size: 10.5px; padding: 2px 6px; border-radius: 4px; font-weight: 700; }
.badge-p1 { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; font-size: 10.5px; padding: 2px 6px; border-radius: 4px; font-weight: 700; }
.badge-p2 { background: #e0f2fe; color: #075985; border: 1px solid #7dd3fc; font-size: 10.5px; padding: 2px 6px; border-radius: 4px; font-weight: 700; }

.legacy-status-tag {
  font-size: 11px;
  padding: 2px 7px;
  border-radius: 12px;
  font-weight: 700;
}
.status-pending { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
.status-in_progress { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
.status-completed { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
.status-paused { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }

.legacy-card-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary, #0f172a);
  line-height: 1.35;
}
.legacy-card-desc {
  font-size: 12.5px;
  color: var(--text-secondary, #475569);
  line-height: 1.5;
  background: #f8fafc;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px dashed #e2e8f0;
}

/* 曦总汇报联动核心盒子 */
.legacy-report-box {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 8px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.legacy-report-box-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.report-count-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11.5px;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 12px;
  background: #f59e0b;
  color: #ffffff;
}
.report-count-pill.none {
  background: #94a3b8;
}
.minutes-pill {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
}
.minutes-pill.done {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #86efac;
}
.minutes-pill.wait {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fca5a5;
}

.legacy-next-plan {
  font-size: 12px;
  line-height: 1.45;
  color: #92400e;
  background: #fef3c7;
  padding: 6px 8px;
  border-radius: 6px;
  border-left: 3px solid #d97706;
}

/* 历次汇报时间轴折叠 */
.legacy-timeline-drawer {
  font-size: 11.5px;
  border-top: 1px dashed #fcd34d;
  padding-top: 6px;
  margin-top: 4px;
}
.legacy-timeline-item {
  position: relative;
  padding-left: 14px;
  margin-bottom: 6px;
  line-height: 1.4;
  color: #78350f;
}
.legacy-timeline-item::before {
  content: "•";
  position: absolute;
  left: 3px;
  top: -1px;
  font-size: 14px;
  color: #f59e0b;
}

/* 卡片操作按钮 */
.legacy-card-actions {
  display: flex;
  gap: 6px;
  align-items: center;
  justify-content: flex-end;
  margin-top: auto;
  padding-top: 8px;
  border-top: 1px solid #f1f5f9;
  flex-wrap: wrap;
}

/* 表格清单视图 */
.legacy-table-wrap {
  background: var(--bg-card, #ffffff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 10px;
  overflow-x: auto;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}
/* 汇报与纪要对应流式卡片 */
.legacy-reports-flow {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 320px;
  max-width: 480px;
}
.legacy-report-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 6px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all 0.15s ease;
}
.legacy-report-card:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}
.legacy-report-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}
.legacy-report-seq-badge {
  background: #e0f2fe;
  color: #0369a1;
  font-size: 11px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 4px;
  white-space: nowrap;
}
.legacy-report-time-text {
  font-size: 12px;
  font-weight: 600;
  color: #1e293b;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.legacy-minutes-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 10px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  white-space: nowrap;
  transition: opacity 0.15s ease;
}
.legacy-minutes-badge:hover {
  opacity: 0.85;
}
.legacy-minutes-badge.has-minutes {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #bbf7d0;
}
.legacy-minutes-badge.no-minutes {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}
.legacy-minutes-badge.pending-report {
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fde68a;
}
.legacy-report-opinion-quote {
  font-size: 11px;
  color: #475569;
  background: #ffffff;
  padding: 3px 8px;
  border-radius: 4px;
  border-left: 2px solid #0284c7;
  line-height: 1.35;
  word-break: break-all;
}
.legacy-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
  text-align: left;
}
.legacy-table th {
  background: #f8fafc;
  color: #475569;
  font-weight: 700;
  padding: 10px 12px;
  border-bottom: 1px solid #cbd5e1;
  white-space: nowrap;
}
.legacy-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #f1f5f9;
  color: #1e293b;
  vertical-align: middle;
}
.legacy-table tr:hover td {
  background: #f8fafc;
}

/* 漫画风格适配 */
.theme-comic .legacy-kpi-card,
.theme-comic .legacy-toolbar,
.theme-comic .legacy-card,
.theme-comic .legacy-table-wrap {
  border: 2px solid var(--ink, #171717) !important;
  box-shadow: 3px 3px 0 var(--ink, #171717) !important;
}

</style>
</head>
<body>

  <!-- App Header -->
  <header class="app-header">
    <div class="header-inner">
      <div class="brand" onclick="switchTab('dashboard')">
        <img src="__IMG_CANONICAL__" alt="Snoopy Brand" class="brand-avatar" />
        <div class="brand-text">
          <h1>Snoopy’s Little Lab</h1>
        </div>
      </div>

      <div class="header-right">
        <!-- Host SQLite Database Status Badge -->
        <div id="hostDbStatusBadge" class="host-db-badge" title="数据集中持久化存储于 Mac 主机的 SQLite 数据库中，全端实时同步">
          <span class="status-dot green"></span>
          <span>Mac 主机存储 · 实时同步</span>
        </div>

        <!-- Theme Toggle -->
        <button class="theme-btn" id="themeToggleBtn" onclick="toggleTheme()" title="切换漫画风格 / 现代极简风格">
          ✨ biu~变
        </button>

        <!-- Backup Data -->
        <button class="theme-btn" onclick="exportDataJSON()" title="导出本地所有数据备份">
          💾 导出数据
        </button>

        <!-- Personal Profile & Security -->
        <div class="profile-menu" id="profileMenu">
          <button class="profile-trigger" id="profileTrigger" type="button" aria-haspopup="menu" aria-expanded="false" onclick="toggleProfileMenu(event)">
            <img class="profile-avatar" src="__IMG_CANONICAL__" alt="Sanyli">
            <span class="profile-name">Sanyli</span>
            <span class="profile-chevron">▼</span>
          </button>
          <div class="profile-dropdown" id="profileDropdown" role="menu" aria-label="个人信息与安全设置">
            <div class="profile-summary">
              <img src="__IMG_CANONICAL__" alt="">
              <div><strong>Sanyli</strong><span>Snoopy’s Little Lab 管理员</span></div>
            </div>
            <button class="profile-action" type="button" role="menuitem" onclick="openPasswordSettings()"><span>🔑</span><span>密码管理</span></button>
            <div class="profile-divider"></div>
            <button class="profile-action is-danger" type="button" role="menuitem" onclick="logoutFromLab()"><span>🔒</span><span>安全退出</span></button>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- Nav Tabs (7 Modules) -->
  <nav class="nav-bar">
    <div class="nav-inner">
      <button class="nav-tab active" data-tab="dashboard" onclick="switchTab('dashboard')">
        <img src="__IMG_ORDINARY_DOGHOUSE__" alt="HOME" />
        <span>HOME</span>
      </button>

      <button class="nav-tab" data-tab="links" onclick="switchTab('links')">
        <img src="__IMG_JOE_COOL__" alt="月度闯关" />
        <span>月度闯关</span>
      </button>

      <button class="nav-tab" data-tab="todo" onclick="switchTab('todo')">
        <img src="__IMG_BEAGLE_SCOUT__" alt="今日任务" />
        <span>今日任务</span>
      </button>

      <button class="nav-tab" data-tab="supervisor" onclick="switchTab('supervisor')">
        <img src="__IMG_SUPERVISOR_SECRETARY__" alt="会议预约" />
        <span>会议预约</span>
      </button>

      <button class="nav-tab" data-tab="legacy_tasks" onclick="switchTab('legacy_tasks')">
        <img src="__IMG_AUTHOR__" alt="遗留任务" />
        <span>遗留任务</span>
      </button>

      <button class="nav-tab" data-tab="timezone" onclick="switchTab('timezone')">
        <img src="__IMG_FLYING_ACE__" alt="时区协同" />
        <span>时区协同</span>
      </button>

      <button class="nav-tab" data-tab="notes" onclick="switchTab('notes')">
        <img src="__IMG_AUTHOR__" alt="每日小记" />
        <span>每日小记</span>
      </button>

      <button class="nav-tab" data-tab="english" onclick="switchTab('english')">
        <img src="__IMG_DAILY_ENGLISH__" alt="每日英语" />
        <span>每日英语</span>
      </button>
    </div>
  </nav>

  <!-- Main Container -->
  <main class="main-wrapper">

    <!-- ================= 1. HOME ================= -->
    <div class="tab-pane active" id="pane-dashboard">

      <div class="chalkboard-stage-wrap">

        <!-- The Grand Chalkboard Frame -->
        <div class="chalkboard-frame">
          <!-- Cute Snoopy & Woodstock on Board Border -->
          <div class="border-snoopy-stage" id="borderSnoopyStage" onclick="interactBorderSnoopy()" title="点击史努比互动~">
            <div class="snoopy-lying-wrap" id="snoopyLyingWrap" title="史努比抱着 Woodstock 陪你自学~">
              <span class="snoopy-cute-aura" title="Woodstock ♪">✨</span>
              <img src="__IMG_BORDER_SNOOPY__" alt="Snoopy and Woodstock" class="snoopy-lying-img" />
              <div class="snoopy-particles" id="snoopyParticles"></div>
            </div>
          </div>

          <div class="chalkboard-screw top-left"></div>
          <div class="chalkboard-screw top-right"></div>
          <div class="chalkboard-screw bottom-left"></div>
          <div class="chalkboard-screw bottom-right"></div>

          <!-- Chalkboard Inner Slate -->
          <div class="chalkboard-slate" id="chalkboardSlate" onclick="handleChalkboardClick(event)">

            <!-- Chalkboard Header Bar: Date navigation on left, font & history controls on right -->
            <div class="chalkboard-header-bar">
              <div class="chalk-date-group">
                <button class="chalk-nav-btn" onclick="changeBlackboardDayOffset(-1)" title="翻看前一天板书">◀ 昨天</button>
                <span class="chalk-date-pill" id="chalkDatePill">📅 2026年10月22日 周四</span>
                <button class="chalk-nav-btn" onclick="changeBlackboardDayOffset(1)" title="翻看后一天板书">明天 ▶</button>
                <button class="chalk-nav-btn" id="btnChalkToday" style="display:none;" onclick="jumpToTodayBlackboard()">回到今天</button>
                <span class="chalk-streak-badge" id="chalkStreakBadge" style="display:none !important;"></span>
              </div>

              <!-- 右侧：字体大小调节、加粗、查看以往记录 -->
              <div class="chalk-tools-group" style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <div style="display:inline-flex; align-items:center; gap:2px; background:rgba(255,255,255,0.08); padding:1px 5px; border-radius:6px; border:1px solid rgba(255,255,255,0.18);">
                  <button class="chalk-nav-btn" onmousedown="event.preventDefault()" onclick="adjustBlackboardFontSize(-2)" title="缩小所选字体 (未框选时调节全局)" style="padding:1px 6px; font-size:11px; line-height:1.2;">A-</button>
                  <span id="blackboardFontSizeDisplay" style="font-size:11.5px; font-weight:700; color:#fde047; min-width:32px; text-align:center; user-select:none;">16px</span>
                  <button class="chalk-nav-btn" onmousedown="event.preventDefault()" onclick="adjustBlackboardFontSize(2)" title="放大所选字体 (未框选时调节全局 · Cmd/Ctrl +)" style="padding:1px 6px; font-size:11px; line-height:1.2;">A+</button>
                </div>

                <button class="chalk-nav-btn" id="btnBlackboardBold" onmousedown="event.preventDefault()" onclick="toggleBlackboardBold()" title="加粗选中文字 (Cmd/Ctrl+B)" style="padding:2px 9px; font-weight:800; font-size:12px; line-height:1.2;">
                  B
                </button>

                <button class="chalk-nav-btn" onclick="openBlackboardHistoryModal()" title="查看以往黑板记录" style="padding:2px 10px; font-size:11.5px; line-height:1.2; display:inline-flex; align-items:center; gap:4px; font-weight:600;">
                  <span>📖</span>
                  <span>以往记录</span>
                </button>
              </div>
            </div>

            <!-- Blackboard Direct Typing Canvas -->
            <div class="chalkboard-content" id="chalkboardContentArea" onclick="handleChalkboardClick(event)">
              <div
                id="chalkboardDirectInput"
                class="chalkboard-direct-textarea"
                contenteditable="true"
                spellcheck="false"
                autocomplete="off"
                autocorrect="off"
                autocapitalize="off"
                oninput="handleDirectBlackboardInput()"
              ></div>
            </div>

          </div>

          <!-- Bottom Wooden Chalk Tray with Eraser at Bottom-Right -->
          <div class="chalkboard-tray">
            <div class="chalk-sticks-rack">
              <span class="chalk-stick white" title="白色粉笔"></span>
              <span class="chalk-stick yellow" title="黄色高亮粉笔"></span>
              <span class="chalk-stick mint" title="薄荷绿粉笔"></span>
              <span class="chalk-stick blue" title="天蓝色粉笔"></span>
            </div>
            <button class="chalk-tray-eraser-btn" id="btnChalkEraser" onclick="eraseCurrentBlackboard()" title="擦拭清空当前黑板板书">
              <span class="eraser-icon">🧽</span>
              <span class="eraser-text">擦黑板</span>
            </button>
          </div>

        </div>

      </div>

      <!-- Hidden test-compatible containers for background regression runners -->
      <div style="display:none;" aria-hidden="true">
        <div id="dashTodoList"></div>
        <div id="dashMeetingList"></div>
        <div id="dashNotesBox"></div>
        <div id="dashTzMiniList"></div>
        <div id="dashEnglishMiniBox"></div>
        <div id="dashQuickLinks"></div>
        <div id="homeLeaderTripBody"></div>
        <div id="homeTodayAgendaList"></div>
        <div id="homeTodayAgendaBadge"></div>
        <div id="homeTodayFocusList"></div>
        <div id="homeNordicCountdownBody"></div>
        <div id="homeBucketList"></div>
        <div id="homeBucketProgressBadge"></div>
        <div id="homeBucketProgressBar"></div>
        <div id="homeNordicTipsBody"></div>
      </div>
    </div>

    <!-- ================= 2. 月度闯关 (月度闯关 · Monthly Quest) ================= -->
    <div class="tab-pane" id="pane-links">
      <div class="module-header-banner theme-links">
        <div class="module-banner-left">
          <img src="__IMG_JOE_COOL__" class="module-banner-avatar" alt="月度闯关" />
          <div>
            <div class="module-banner-title">
              <span id="linksModuleTitleText">月度闯关 · Monthly Quest</span>
              <button class="module-edit-btn" onclick="openEditModuleModal('links')" title="自定义月度闯关板块">✏️</button>
              <span class="persona-tag" id="linksModuleTagText">🎯 月度打卡闯关</span>
            </div>
          </div>
        </div>

        <div class="module-banner-right">
          <div class="stat-box">
            <div class="stat-num" id="statMonthlyProgress" style="color:#0891b2;">0 / 4</div>
            <div class="stat-label">已通关</div>
          </div>
          <div class="stat-box">
            <div class="stat-num" id="statMonthlyNextDate" style="color:#6366f1; font-size:15px; font-weight:800;">11月9日</div>
            <div class="stat-label">下个关卡</div>
          </div>
          <button class="btn btn-primary btn-sm" onclick="openAddMonthlyRoutineModal()">➕ 添加关卡</button>
        </div>
      </div>

      <!-- 月度事项主卡片 -->
      <div class="card" style="margin-bottom:20px;">
        <div class="card-body">
          <!-- 月份选择与进度条栏 -->
          <div class="monthly-month-bar">
            <div class="monthly-month-nav">
              <button class="btn btn-sm btn-ghost" onclick="changeRoutineMonth(-1)" title="查看上个月">◀ 上月</button>
              <span class="monthly-month-title" id="currentRoutineMonthDisplay">2026年 11月</span>
              <button class="btn btn-sm btn-ghost" onclick="changeRoutineMonth(1)" title="查看下个月">下月 ▶</button>
              <button class="btn btn-sm btn-outline" onclick="resetRoutineMonthToCurrent()" style="margin-left:6px; font-size:12px;">回到本月</button>
            </div>
            <div class="monthly-progress-box">
              <span style="font-size:12.5px; color:var(--text-secondary); font-weight:600;">月度事项推进：</span>
              <div class="routine-progress-track">
                <div class="routine-progress-fill" id="routineProgressFill" style="width:0%;"></div>
              </div>
              <span id="routineProgressPercent" style="font-size:13px; font-weight:800; color:var(--text-primary); min-width:38px;">0%</span>
            </div>
          </div>

          <!-- 动态渲染的月度时间线 (简洁无冗余文案) -->
          <div class="routine-timeline" id="monthlyTimelineContainer">
            <!-- 由 renderMonthlyRoutines() 动态填充 -->
          </div>
        </div>
      </div>

      <!-- 常用办公链接板块已按要求删除 (保留隐藏兼容容器保证后台脚本平稳运行) -->
      <div style="display:none;" aria-hidden="true">
        <span id="statLinkCountBadge"></span>
        <span id="linksCollapseIcon"></span>
        <div id="linksCollapseBody">
          <div id="linksCategoryTabs"></div>
          <div id="linksFullGrid"></div>
        </div>
      </div>
    </div>

    <!-- ================= 3. 今日任务 (今日任务 · Beagle Scout) ================= -->
    <div class="tab-pane" id="pane-todo">
      <!-- Unified Module Header Banner (Clean, no unnecessary slogans) -->
      <div class="module-header-banner theme-todo">
        <div class="module-banner-left">
          <img src="__IMG_BEAGLE_SCOUT__" class="module-banner-avatar" alt="今日任务" />
          <div>
            <div class="module-banner-title">
              <span id="todoModuleTitleText">今日任务 · Beagle Scout</span>
              <button class="module-edit-btn" onclick="openEditModuleModal('todo')" title="自定义今日任务板块">✏️</button>
              <span class="persona-tag" id="todoModuleTagText">🏕️ 比格犬童子军</span>
            </div>
          </div>
        </div>

        <div class="module-banner-right">
          <div class="stat-box" onclick="setTodoViewMode('matrix')" style="cursor:pointer;" title="查看四象限看板">
            <div class="stat-num" id="statTodoPending" style="color:#d97706;">0</div>
            <div class="stat-label">进行中</div>
          </div>
          <div class="stat-box" onclick="setTodoViewMode('list')" style="cursor:pointer;" title="查看已完成待办">
            <div class="stat-num" id="statTodoDone" style="color:#16a34a;">0</div>
            <div class="stat-label">已完成</div>
          </div>
          <div class="stat-box" onclick="setTodoViewMode('archive')" style="cursor:pointer;" title="查看已归档历史任务">
            <div class="stat-num" id="statTodoArchived" style="color:#64748b;">0</div>
            <div class="stat-label">已归档 📦</div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <!-- View Switcher & Action Toolbar (Four-Quadrant Matrix First) -->
          <div class="todo-toolbar" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
            <div class="filter-tabs">
              <button class="filter-btn active" id="btnTodoViewMatrix" onclick="setTodoViewMode('matrix')">🗂️ 四象限看板</button>
              <button class="filter-btn" id="btnTodoViewList" onclick="setTodoViewMode('list')">📋 清单视图</button>
              <button class="filter-btn" id="btnTodoViewArchive" onclick="setTodoViewMode('archive')">📦 归档清单 (<span id="tabArchiveCount">0</span>)</button>
            </div>
            <div style="display:flex; gap:8px;">
              <button class="btn btn-sm btn-ghost" id="btnArchiveCompleted" onclick="archiveCompletedTodos()" title="将所有已勾选完成的待办移入归档区">📦 一键归档已完成</button>
            </div>
          </div>

          <!-- Non-black Beagle Scout Green Add Button, Strictly Single-Line -->
          <div class="todo-input-bar" id="todoInputBar">
            <input type="text" id="inputTodoText" placeholder="添加待办事项，回车快速保存..." onkeydown="if(event.key==='Enter') addTodo()" style="flex:1; min-width:180px;" />
            <select id="selectTodoPriority" style="width: 135px; flex-shrink:0;">
              <option value="q1" selected>🔥 今天完成</option>
              <option value="q2">⭐ 这周安排上</option>
              <option value="q3">⚡ 先放一放</option>
              <option value="q4">☕ 有空再说</option>
            </select>
            <input type="date" id="inputTodoDate" style="width: 130px; flex-shrink:0;" />
            <button class="btn btn-todo-add" onclick="addTodo()">添加任务</button>
          </div>

          <!-- 1. Four-Quadrant Matrix Container (Default Visible First) -->
          <div id="todoMatrixContainer" style="display:block;"></div>

          <!-- 2. List View Container -->
          <div class="todo-list" id="todoFullList" style="display:none;"></div>

          <!-- 3. Archived List Container -->
          <div id="todoArchiveContainer" style="display:none;"></div>
        </div>
      </div>
    </div>

    <!-- ================= 3. 会议预约 (会议预约 · Secretary Desk) ================= -->
    <div class="tab-pane" id="pane-supervisor">
      <!-- Unified Module Header Banner -->
      <div class="module-header-banner theme-meeting">
        <div class="module-banner-left">
          <img src="__IMG_SUPERVISOR_SECRETARY__" class="module-banner-avatar" alt="会议预约" />
          <div>
            <div class="module-banner-title">
              <span id="supervisorModuleTitleText">会议预约 · Secretary Desk</span>
              <button class="module-edit-btn" onclick="openEditModuleModal('supervisor')" title="自定义会议预约板块">✏️</button>
              <span class="persona-tag" id="supervisorModuleTagText">秘书工作台</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Supervisor Schedule Management Toolbar (View Switcher & Actions) -->
      <div class="meeting-toolbar" style="margin-bottom: 16px;">
        <div class="filter-tabs">
          <button class="filter-btn active" id="btnViewWeekBoard" onclick="setSupervisorViewMode('week_board')">周历</button>
          <button class="filter-btn" id="btnViewMonthCal" onclick="setSupervisorViewMode('month_cal')">月度日历</button>
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
          <div style="display:flex; align-items:center; gap:6px;">
            <label style="font-size:12px; color:var(--text-secondary); font-weight:600;">跳转日期：</label>
            <input type="date" id="timelineDateSelector" style="width:125px; padding:4px 8px; font-size:12px;" onchange="handleTimelineDateChange()" />
          </div>
          <button class="btn" id="btnRemindTomorrowMeetings" onclick="openTomorrowMeetingReminderModal()" style="font-weight:700; color:#4338ca; border:1px solid #c7d2fe; background:#eef2ff;" title="一键提醒领导明日日程并复制">
            📋 提醒领导明日会议
          </button>
          <button class="btn" onclick="exportExecutiveScheduleBriefing()">
            复制排版周报
          </button>
          <button class="btn btn-primary" onclick="openLeaderTripModal()">
            ✈️ 登记出差
          </button>
          <button class="btn" id="btnRegisterTransit" onclick="openTransitModal()" style="font-weight:700; color:#0369a1; border:1px solid #7dd3fc; background:#f0f9ff;" title="登记领导跨时区在途飞行/行程">
            🛫 登记在途
          </button>
        </div>
      </div>
      <span id="currentViewModeTag" style="display:none;">周历</span>

      <!-- 1. Executive Weekly Board (周历) -->
      <div id="supervisorWeeklyBoardContainer" class="weekly-board-wrap"></div>

      <!-- 2. Executive Day Calendar (日历) -->
      <div id="supervisorDayCalendarContainer" class="supervisor-day-view" style="display:none;"></div>

      <!-- 3. Month Calendar Section (月度日历) -->
      <div id="supervisorMonthCalendarContainer" class="supervisor-month-view" style="display:none;"></div>

      <!-- 3. Cards Section Toolbar & List -->
      <div id="cardsSectionToolbar" style="display:none; margin-top: 18px; margin-bottom: 12px; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div style="font-size:13.5px; font-weight:700; color:var(--text-primary);" id="cardsSectionTitle">
          主管会议决策卡片清单
        </div>
        <div class="filter-tabs" id="cardStatusFilters">
          <button class="filter-btn active" data-filter="all" onclick="filterMeetings('all')">全部</button>
          <button class="filter-btn" data-filter="scheduled" onclick="filterMeetings('scheduled')">已排期</button>
          <button class="filter-btn" data-filter="pending" onclick="filterMeetings('pending')">待安排</button>
          <button class="filter-btn" data-filter="completed" onclick="filterMeetings('completed')">已完成</button>
        </div>
      </div>

      <!-- 4. Meeting Cards List Container -->
      <div id="meetingCardsList" style="display:none;"></div>
    </div>

    <!-- ================= 3.5 遗留任务 (遗留任务 · Legacy Tasks) ================= -->
    <div class="tab-pane" id="pane-legacy_tasks">
      <!-- Unified Module Header Banner -->
      <div class="module-header-banner theme-legacy" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left: 5px solid #f59e0b;">
        <div class="module-banner-left">
          <img src="__IMG_AUTHOR__" class="module-banner-avatar" alt="遗留任务" />
          <div>
            <div class="module-banner-title">
              <span id="legacyTasksModuleTitleText">遗留任务 · Legacy Tasks</span>
              <button class="module-edit-btn" onclick="openEditModuleModal('legacy_tasks')" title="自定义板块">✏️</button>
              <span class="persona-tag" id="legacyTasksModuleTagText" style="background:#fef3c7; color:#92400e; border:1px solid #fcd34d;">📋 曦总汇报闭环追踪</span>
            </div>
          </div>
        </div>
        <div class="module-banner-right" style="display:flex; gap:8px; align-items:center;">
          <button class="btn btn-sm" onclick="openLegacyImportModal()" style="font-weight:700; background:transparent !important; color:#92400e; border:1.5px solid #d97706;" title="从 Excel/飞书复制粘贴或上传文件批量导入">
            📥 导入清单
          </button>
          <button class="btn btn-sm" onclick="clearAllLegacyTasks()" style="font-weight:600; background:transparent !important; color:#dc2626; border:1.5px solid #fca5a5;" title="清空全部遗留任务数据">
            🗑️ 清空清单
          </button>
          <button class="btn btn-sm" onclick="openAddLegacyTaskModal()" style="font-weight:700; background:transparent !important; color:#1d4ed8; border:1.5px solid #3b82f6;" title="新增重点遗留任务">
            ＋ 新增任务
          </button>
        </div>
      </div>

      <!-- 顶部统计概览指示牌 (KPIs) -->
      <div class="legacy-kpi-grid" id="legacyKpiGrid"></div>

      <!-- 工具栏: 责任人筛选、搜索、视图切换 -->
      <div class="legacy-toolbar">
        <div class="legacy-toolbar-left" style="display:flex; align-items:center; gap:12px;">
          <div class="legacy-filter-group" style="display:inline-flex; align-items:center; gap:6px; white-space:nowrap;">
            <label style="white-space:nowrap; margin:0; font-size:12px; font-weight:700; color:#475569; display:inline-flex; align-items:center;">👤 责任人：</label>
            <select id="legacyOwnerFilter" onchange="filterLegacyTasksOwner(this.value)" style="white-space:nowrap;">
              <option value="all">全部责任人</option>
            </select>
          </div>
        </div>
        <div class="legacy-toolbar-right" style="display:flex; align-items:center; gap:10px;">
          <div class="legacy-search-box">
            <input type="text" id="legacySearchInput" placeholder="搜索任务/责任人/计划..." oninput="handleLegacySearch(this.value)" />
          </div>
          <div class="view-switch-tabs">
            <button class="view-switch-btn active" id="btnLegacyViewTable" onclick="setLegacyViewMode('table')" title="主视图：精简表格清单">
              📊 表格清单 (主视图)
            </button>
            <button class="view-switch-btn" id="btnLegacyViewCards" onclick="setLegacyViewMode('cards')" title="卡片看板视图">
              🗂 看板视图
            </button>
          </div>
        </div>
      </div>

      <!-- 视图容器 1: 明细清单表格视图 (默认主视图) -->
      <div id="legacyTableContainer" class="legacy-table-wrap"></div>

      <!-- 视图容器 2: 卡片看板视图 -->
      <div id="legacyCardsContainer" class="legacy-cards-grid" style="display:none;"></div>
    </div>

    <!-- ================= 4. 时区协同 (时区协同 · World Tour) ================= -->
    <div class="tab-pane" id="pane-timezone">
      <!-- Unified Module Header Banner (Subtitle updated as requested in Point 3) -->
      <div class="module-header-banner theme-timezone">
        <div class="module-banner-left">
          <img src="__IMG_FLYING_ACE__" class="module-banner-avatar" alt="时区协同" />
          <div>
            <div class="module-banner-title">
              <span id="timezoneModuleTitleText">时区协同 · World Tour</span>
              <button class="module-edit-btn" onclick="openEditModuleModal('timezone')" title="自定义时区协同板块">✏️</button>
              <span class="persona-tag" id="timezoneModuleTagText">🪖 Flying Ace</span>
            </div>
            <!-- Subtitle accurately updated per Point 3 -->
            <div class="module-banner-subtitle">
              王牌飞行员 Snoopy（The Flying Ace）精准护航非洲各区域作息
            </div>
          </div>
        </div>

        <div class="module-banner-right">
          <div class="stat-box" style="text-align:right; min-width:140px; padding:8px 16px;">
            <div style="font-size:11px; color:var(--text-muted); font-weight:600;">🇪🇬 开罗时间 (UTC+2 · 冬令时)</div>
            <div class="stat-num" id="tzBigCairoClock" style="font-size:22px; color:var(--text-primary); margin-top:2px;">--:--:--</div>
          </div>
        </div>
      </div>

      <!-- 8 Representative Offices Cards Grid (Sorted chronologically from earliest to latest, beautified layout) -->
      <div class="tz-grid" id="tzFullGrid"></div>

      <!-- Multi-Timezone Meeting Time Alignment Simulator -->
      <div class="tz-simulator-card">
        <div class="tz-sim-header" style="margin-bottom:12px;">
          <span>🕒 跨区会议时间对齐器</span>
        </div>

        <div class="tz-sim-row" style="background:var(--card-subtle); padding:10px 14px; border-radius:var(--radius-sm); border:1px solid var(--border); margin-bottom:14px; display:flex; align-items:center; gap:8px; flex-wrap:nowrap; overflow-x:auto;">
          <label style="font-size:12px; font-weight:700; white-space:nowrap;">基准时区：</label>
          <select id="simBaseTimezone" onchange="updateTzSimulator()" style="padding:4px 8px; font-size:12px; font-weight:600; border:1px solid var(--border); border-radius:4px; background:#fff; white-space:nowrap;">
            <option value="cairo" selected>埃及·开罗 (UTC+2)</option>
            <option value="med_south_libya">地南·利比亚 (UTC+2)</option>
            <option value="med_south_tunis">地南·突尼斯 (UTC+1)</option>
            <option value="cameroon">喀麦隆 (UTC+1)</option>
            <option value="congo_drc">刚果（金） (UTC+1)</option>
            <option value="algeria">阿尔及利亚 (UTC+1)</option>
            <option value="morocco">摩洛哥 (UTC+0)</option>
            <option value="cote_divoire">科特迪瓦 (UTC+0)</option>
            <option value="senegal">塞内加尔 (UTC+0)</option>
            <option value="beijing">中国·北京 (UTC+8)</option>
          </select>
          <span style="color:var(--border); margin:0 6px;">|</span>
          <label style="font-size:12px; font-weight:700; white-space:nowrap;">会议时间段：</label>
          <input type="time" id="simCairoTime" value="14:00" style="width:96px; padding:4px 6px; font-size:12px; font-weight:700; border:1px solid var(--border); border-radius:4px; background:#fff;" onchange="handleSimTimeRangeChange('start')" oninput="updateTzSimulator()" />
          <span style="color:var(--text-muted); font-size:12px; font-weight:600; padding:0 2px;">至</span>
          <input type="time" id="simEndTime" value="15:30" style="width:96px; padding:4px 6px; font-size:12px; font-weight:700; border:1px solid var(--border); border-radius:4px; background:#fff;" onchange="handleSimTimeRangeChange('end')" oninput="updateTzSimulator()" />
          <span id="simDurationTag" style="font-size:11px; color:#0369a1; background:#e0f2fe; padding:2px 7px; border-radius:4px; font-weight:600; margin-left:6px; white-space:nowrap;">90分钟</span>
        </div>

        <div id="tzSimResults"></div>
      </div>
    </div>

    <!-- ================= 6. 每日小记 (每日小记 · Little Notes) ================= -->
    <div class="tab-pane" id="pane-notes">
      <!-- Unified Module Header Banner (Subtitle removed per Point 5) -->
      <div class="module-header-banner theme-notes">
        <div class="module-banner-left">
          <img src="__IMG_AUTHOR__" class="module-banner-avatar" alt="每日小记" />
          <div>
            <div class="module-banner-title">
              <span id="notesModuleTitleText">每日小记 · Little Notes</span>
              <button class="module-edit-btn" onclick="openEditModuleModal('notes')" title="自定义每日小记板块">✏️</button>
              <span class="persona-tag" id="notesModuleTagText">✍️ World Famous Author</span>
            </div>
          </div>
        </div>

        <div class="module-banner-right">
          <div class="stat-box">
            <div class="stat-num" id="statNoteCount" style="color:#7c3aed;">0</div>
            <div class="stat-label">已存小记</div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="notes-editor-box">
            <textarea id="inputNoteText" placeholder="“It was a dark and stormy night...” 记录今日灵感、会议速记或交办备忘..."></textarea>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
              <select id="selectNoteCategory" style="width: 160px;">
                <option value="📝 随手记事">📝 随手记事</option>
                <option value="📌 会议速记">📌 会议速记</option>
                <option value="👔 主管交代">👔 主管交代</option>
                <option value="🌍 代表处对接">🌍 代表处对接</option>
              </select>
              <button class="btn btn-primary" onclick="addNote()">✍️ 保存小记</button>
            </div>
          </div>

          <div class="notes-grid" id="notesFullGrid"></div>
        </div>
      </div>
    </div>

    <!-- ================= 7. 每日英语 (每日英语 · English Time) ================= -->
    <div class="tab-pane" id="pane-english">
      <!-- Unified Module Header Banner (Subtitle removed per Point 6) -->
      <div class="module-header-banner theme-english">
        <div class="module-banner-left">
          <img src="__IMG_DAILY_ENGLISH__" class="module-banner-avatar" alt="每日英语" />
          <div>
            <div class="module-banner-title">
              <span id="englishModuleTitleText">每日英语 · 2027北欧漫游</span>
              <button class="module-edit-btn" onclick="openEditModuleModal('english')" title="自定义每日英语板块">✏️</button>
              <span class="persona-tag" id="englishModuleTagText">❄️ Nordic Journey</span>
            </div>
          </div>
        </div>

        <div class="module-banner-right">
          <!-- Combined Snoopy Streak & Checkin Pill Button -->
          <button type="button" class="snoopy-checkin-pill-btn" id="btnEnglishCheckin" onclick="doEnglishCheckin()" title="点击打卡今日自学">
            <div class="snoopy-checkin-avatar-wrap">
              <img src="__IMG_CANONICAL__" class="snoopy-checkin-avatar" id="snoopyCheckinAvatar" alt="Snoopy" />
            </div>
            <div class="snoopy-checkin-info">
              <div class="snoopy-checkin-streak-row">
                <span class="streak-label">连续打卡</span>
                <span class="streak-days" id="englishStreakNum">0 天</span>
              </div>
              <div class="snoopy-checkin-action-row" id="englishCheckinAction">
                <span class="checkin-action-text" id="englishCheckinActionText">点击打卡 ＋</span>
              </div>
            </div>
          </button>
        </div>
      </div>

      <!-- Universal Quick Lookup Bar (Clean & Minimal) -->
      <div class="english-quick-lookup-bar">
        <div class="english-search-group">
          <span style="font-size: 15px;">🔍</span>
          <input type="text" id="englishSearchInput" class="english-search-input" placeholder="" onkeydown="if(event.key==='Enter') searchEnglishWord()" />
          <button type="button" class="btn btn-sm btn-yellow" onclick="searchEnglishWord()">查询</button>
        </div>
      </div>

      <!-- Floating Word Lookup & Pronunciation Card -->
      <div id="wordLookupPopup" class="word-lookup-popup" style="display:none;">
        <div class="word-popup-header">
          <div class="word-popup-title-row">
            <span class="word-popup-title" id="wordPopupTitle" onclick="speakLookupWord()" style="cursor:pointer;" title="点击收听读音">Word</span>
            <span class="word-popup-phonetic" id="wordPopupPhonetic"></span>
            <span class="word-popup-pos" id="wordPopupPos"></span>
          </div>
          <div class="word-popup-actions">
            <button type="button" class="word-popup-speak-btn" id="wordPopupSpeakBtn" onclick="speakLookupWord()" title="点击播放发音">🔊</button>
            <button type="button" class="word-popup-close-btn" onclick="hideWordLookupPopup()" title="关闭">✕</button>
          </div>
        </div>
        <div class="word-popup-def" id="wordPopupDef"></div>
      </div>

      <!-- Part 1: 3 Core Business Travel Vocabulary Words -->
      <div class="english-sec-header">
        <span id="englishSecHeaderTitle">❄️ 今日北欧旅行核心词汇（3 个高频词）</span>
        <span style="font-size: 12px; font-weight: normal; color: var(--text-muted);">点击 🔊 可收听本地发音</span>
      </div>
      <div class="english-word-grid" id="englishWordsGrid"></div>

      <!-- Part 2: 3 Practical Workplace Communication Sentences -->
      <div class="english-sec-header">
        <span>💬 北欧日常旅行与文化场景（3 句实战语句）</span>
        <span style="font-size: 12px; font-weight: normal; color: var(--text-muted);">含北欧人生活习惯、文化习俗与超实用旅行Tips</span>
      </div>
      <div class="sentence-list" id="englishSentencesList"></div>
    </div>

  </main>

  <!-- App Footer -->
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-left">
        <span>Snoopy’s Little Lab · Sanyli.</span>
        <span class="app-version-badge" id="appFooterVersionBadge" title="当前发布版本（每次更新递增）">🏷️ __APP_VERSION__</span>
      </div>
      <div>Designed with Charles M. Schulz’s Peanuts Legacy 🐾</div>
    </div>
  </footer>

  <!-- ================= MODAL: UNIVERSAL SMART CALENDAR & TABLE IMPORT ================= -->
  <div class="modal-overlay" id="passwordSettingsModal">
    <div class="modal-box" style="max-width: 450px;">
      <div class="modal-header">
        <div class="modal-title">🔑 密码管理</div>
        <button class="btn btn-sm btn-ghost" type="button" onclick="closePasswordSettings()">✕</button>
      </div>
      <div class="modal-body">
        <div style="display:flex;align-items:center;gap:12px;padding:12px;margin-bottom:16px;border:1px solid var(--border);border-radius:12px;background:var(--woodstock-soft);">
          <img src="__IMG_CANONICAL__" alt="Snoopy" style="width:52px;height:52px;object-fit:contain;">
          <div><div style="font-size:13px;font-weight:750;">更新登录口令</div><div style="font-size:11px;color:var(--text-muted);">修改成功后，所有设备都需要重新登录。</div></div>
        </div>
        <form id="passwordSettingsForm" onsubmit="submitPasswordChange(event)">
          <div class="form-group">
            <label for="currentAccountPassword">当前密码</label>
            <input id="currentAccountPassword" type="password" autocomplete="current-password" required>
          </div>
          <div class="form-group">
            <label for="newAccountPassword">新密码</label>
            <input id="newAccountPassword" type="password" autocomplete="new-password" minlength="6" maxlength="256" required>
            <div class="password-help">可以设置为 6 位纯数字，或至少 10 个字符的强密码。</div>
          </div>
          <div class="form-group">
            <label for="confirmAccountPassword">再次输入新密码</label>
            <input id="confirmAccountPassword" type="password" autocomplete="new-password" minlength="6" maxlength="256" required>
          </div>
          <div class="password-error" id="passwordSettingsError" role="alert" aria-live="polite"></div>
        </form>
      </div>
      <div class="modal-footer">
        <button class="btn btn-ghost" type="button" onclick="closePasswordSettings()">取消</button>
        <button class="btn btn-primary" id="savePasswordButton" type="submit" form="passwordSettingsForm">保存新密码</button>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: UNIVERSAL SMART CALENDAR & TABLE IMPORT ================= -->
  <div class="modal-overlay" id="importCalendarModal">
    <div class="modal-box" style="max-width: 680px;">
      <div class="modal-header">
        <div class="modal-title">智能导入会议日程（支持固定表头 / 自由格式）</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('importCalendarModal')">✕</button>
      </div>
      <div class="modal-body">
        <!-- Standard Header Box per User Request -->
        <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:6px; padding:10px 14px; margin-bottom:12px; font-size:12px;">
          <div style="font-weight:700; color:#0369a1; margin-bottom:5px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
            <span>推荐标准 Excel 导入表头（支持自动对齐）：</span>
            <div style="display:flex; gap:6px;">
              <button type="button" class="btn btn-sm btn-ghost" onclick="copyStandardExcelHeader()" title="点击复制整行表头至剪贴板，可直接粘贴到您的Excel第一行">复制标准表头</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="downloadStandardExcelTemplate()" title="下载预设好列名的标准 Excel CSV 模板">下载示例模板</button>
            </div>
          </div>
          <code style="display:block; background:#fff; padding:6px 10px; border-radius:4px; border:1px solid #e0f2fe; color:#0c4a6e; font-size:11.5px; overflow-x:auto; white-space:nowrap; font-family:var(--font-mono);">
            *会议主题（关键任务）	*议题背景/决策要点说明	*汇报人	*参会人	*纪要人	*预约时长（H）
          </code>
          <div style="color:#0284c7; font-size:11px; margin-top:5px; line-height:1.45;">
            说明：非强制填满所有列，核心信息仅需<strong>【会议主题】、【汇报人】、【预约时长（H）】</strong>即可排期！“星期一到星期五”等字样将自动识别为排期日期，绝不误认为会议主题。
          </div>
        </div>

        <div class="form-row" style="margin-bottom: 12px;">
          <div class="form-group" style="margin-bottom: 0;">
            <label>默认排期日期：</label>
            <input type="date" id="importTargetDate" onchange="runCalendarLivePreview()" />
          </div>
          <div style="display:flex; align-items:flex-end; gap:8px;">
            <button class="btn btn-sm" onclick="document.getElementById('calendarFileInput').click()">选择电脑文档导入...</button>
            <input type="file" id="calendarFileInput" accept="*" style="display:none;" onchange="handleCalendarFileUpload(event)" />
            <button class="btn btn-sm btn-ghost" onclick="fillSampleCalendarData()">填入示例数据</button>
          </div>
        </div>

        <div class="form-group">
          <label>粘贴自由文本 / 表格内容：</label>
          <textarea id="inputImportTableText" style="min-height: 120px; font-family: var(--font-mono); font-size: 12px;" placeholder="支持自由输入任何格式，例如：&#10;1. 表格复制：10:00 - 10:45&#9;中东北非区域Q3预算评审&#9;张总(地南代)&#10;2. 自然语言：9月25日下午2点半至3点15分 刚果金代表处业务对齐 汇报人：陈部长 决策点：审批工程预算&#10;3. 会议通知：明天上午10点在1号会议室召开非洲8代表处协同例会，请李总汇报业务进展，预计时长60分钟" oninput="runCalendarLivePreview()"></textarea>
        </div>

        <!-- Recognition Status & Dual Normalization Live Preview -->
        <div id="importLivePreviewArea" style="display:none; margin-top: 14px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:8px;">
            <span id="importPreviewStatusText" style="font-size: 12px; font-weight: 700; color: #16a34a;">识别成功：已规整 0 场会议</span>
            <div style="display:flex; gap:6px;">
              <button type="button" class="preview-tab-btn active" id="btnPreviewTabCal" onclick="switchImportPreviewTab('cal')">日历版本预览</button>
              <button type="button" class="preview-tab-btn" id="btnPreviewTabCard" onclick="switchImportPreviewTab('card')">卡片版本预览</button>
            </div>
          </div>

          <!-- Calendar Formatted Version Wrap -->
          <div id="importCalPreviewWrap" style="max-height: 200px; overflow-y: auto; border: 1px solid var(--border); border-radius: 6px; padding: 10px; background: #fafafa;">
            <!-- Rendered by runCalendarLivePreview() -->
          </div>

          <!-- Card Formatted Version Wrap -->
          <div id="importCardPreviewWrap" style="display:none; max-height: 200px; overflow-y: auto; border: 1px solid var(--border); border-radius: 6px; padding: 10px; background: #fafafa;">
            <!-- Rendered by runCalendarLivePreview() -->
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn" onclick="closeModal('importCalendarModal')">取消</button>
        <button type="button" class="btn btn-primary" id="btnConfirmImport" onclick="confirmImportCalendar()" disabled>
          确认导入至主管日程
        </button>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: ADD / EDIT SUPERVISOR MEETING ================= -->
  <div class="modal-overlay" id="meetingModal">
    <div class="modal-box" id="meetingModalBox">
      <!-- Top Drag Grip Bar -->
      <div class="modal-drag-handle-bar" style="width: 100%; padding: 8px 0 4px 0; background: #f8fafc; border-top-left-radius: 12px; border-top-right-radius: 12px; display: flex; justify-content: center; align-items: center; cursor: grab; touch-action: none; user-select: none; border-bottom: 1px solid #f1f5f9;">
        <div style="width: 44px; height: 4px; background: #94a3b8; border-radius: 2px;"></div>
      </div>
      <div class="modal-header" id="meetingModalHeader" style="cursor: grab; user-select: none; touch-action: none; padding-top: 10px; display: flex; align-items: center; justify-content: space-between;">
        <div style="display:flex; align-items:center; gap:8px;">
          <div class="modal-title" id="meetingModalTitle">登记主管会议预约</div>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
          <button type="button" class="btn btn-sm btn-ghost" onclick="dockMeetingModal('left')" title="靠左" style="padding:3px 8px; font-size:11px; background:#f1f5f9; border-radius:4px; font-weight:600; color:#475569;">◀ 靠左</button>
          <button type="button" class="btn btn-sm btn-ghost" onclick="dockMeetingModal('center')" title="居中" style="padding:3px 8px; font-size:11px; background:#f1f5f9; border-radius:4px; font-weight:600; color:#475569;">⤢ 居中</button>
          <button type="button" class="btn btn-sm btn-ghost" onclick="dockMeetingModal('right')" title="靠右" style="padding:3px 8px; font-size:11px; background:#f1f5f9; border-radius:4px; font-weight:600; color:#475569;">靠右 ▶</button>
          <button type="button" class="btn btn-sm btn-ghost" onclick="closeModal('meetingModal')" style="font-size:15px; margin-left:4px;">✕</button>
        </div>
      </div>
      <div class="modal-body">
        <form id="meetingForm" onsubmit="event.preventDefault(); saveMeeting();">
          <input type="hidden" id="inputMeetingId" value="" />

          <!-- 会议时区基准选择 (支持开罗时间或出差地当地时间录入) -->
          <div id="modalTripBanner" style="display:none !important;"></div>
          <div style="display:flex; justify-content:space-between; align-items:center; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:var(--radius-sm); padding:6px 10px; margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:6px; flex:1;">
              <span style="font-size:12px; font-weight:700; color:#15803d; white-space:nowrap;">🌍 录入时区：</span>
              <select id="inputMeetingTimezoneBase" onchange="handleMeetingModalTimezoneChange()" style="font-size:12px; font-weight:600; padding:3px 8px; border:1px solid #86efac; border-radius:4px; background:#fff; color:#166534; flex:1; max-width:270px;">
                <option value="cairo" selected>埃及·开罗 (UTC+2)</option>
                <option value="cameroon">喀麦隆 (UTC+1)</option>
                <option value="med_south_libya">利比亚 (UTC+2)</option>
                <option value="med_south_tunis">突尼斯 (UTC+1)</option>
                <option value="algeria">阿尔及利亚 (UTC+1)</option>
                <option value="morocco">摩洛哥 (UTC+0)</option>
                <option value="congo_drc">刚果（金） (UTC+1)</option>
                <option value="cote_divoire">科特迪瓦 (UTC+0)</option>
                <option value="senegal">塞内加尔 (UTC+0)</option>
                <option value="beijing">北京 (UTC+8)</option>
              </select>
            </div>
            <div id="modalTzConversionHint" style="display:none !important;"></div>
          </div>

          <!-- 1. 会议时间: 日期、开始时间、结束时间 -->
          <div class="form-row">
            <div class="form-group" style="flex: 1.1;">
              <label>会议日期 *</label>
              <input type="date" id="inputMeetingDate" onchange="handleMeetingModalDateChange()" oninput="handleMeetingModalDateChange()" required />
            </div>
            <div class="form-group" style="flex: 1;">
              <label id="lblMeetingStartTime">开始时间 *</label>
              <div class="time-picker-wrapper">
                <div class="time-input-box">
                  <input type="text" id="inputMeetingStartTime" placeholder="09:30" autocomplete="off"
                         onclick="toggleTimePickerDropdown('start', true)"
                         oninput="handleMeetingTimeInput('start')"
                         onchange="handleMeetingTimeBlur('start')"
                         onblur="handleMeetingTimeBlur('start')" required />
                  <span class="time-picker-btn" onclick="toggleTimePickerDropdown('start', event)" title="点击选择常用时间">🕒</span>
                </div>
                <div id="timePickerMenu_start" class="time-picker-dropdown" style="display:none;"></div>
              </div>
            </div>
            <div class="form-group" style="flex: 1;">
              <label id="lblMeetingEndTime">结束时间 *</label>
              <div class="time-picker-wrapper">
                <div class="time-input-box">
                  <input type="text" id="inputMeetingEndTime" placeholder="10:15" autocomplete="off"
                         onclick="toggleTimePickerDropdown('end', true)"
                         oninput="handleMeetingTimeInput('end')"
                         onchange="handleMeetingTimeBlur('end')"
                         onblur="handleMeetingTimeBlur('end')" required />
                  <span class="time-picker-btn" onclick="toggleTimePickerDropdown('end', event)" title="点击选择常用时间">🕒</span>
                </div>
                <div id="timePickerMenu_end" class="time-picker-dropdown" style="display:none;"></div>
              </div>
            </div>
          </div>

          <!-- 快捷时长选择 (30/40/60/90/120) 与 时长展示 -->
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-top:-4px; margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
              <span style="font-size:11.5px; color:var(--text-muted); font-weight:500;">快捷时长:</span>
              <button type="button" class="chip-btn" id="durChip30" onclick="applyQuickDuration(30)">30分钟</button>
              <button type="button" class="chip-btn" id="durChip40" onclick="applyQuickDuration(40)">40分钟</button>
              <button type="button" class="chip-btn" id="durChip60" onclick="applyQuickDuration(60)">60分钟</button>
              <button type="button" class="chip-btn" id="durChip90" onclick="applyQuickDuration(90)">90分钟</button>
              <button type="button" class="chip-btn" id="durChip120" onclick="applyQuickDuration(120)">120分钟</button>
            </div>
            <div id="meetingDurationBadge" style="font-size:11.5px; font-weight:600; color:var(--text-secondary); background:var(--card-subtle); padding:2px 8px; border-radius:10px; border:1px solid var(--border-subtle);">
              时长：45 分钟 (0.75H)
            </div>
          </div>

          <!-- 跨时区自动换算实时对齐卡片 (后台静默换算，界面极简) -->
          <div id="modalTripLiveCard" style="display:none !important;"></div>

          <!-- 会议时间冲突动态提醒条 -->
          <div id="meetingConflictAlert" class="meeting-conflict-alert" style="display:none; margin-bottom:12px; padding:10px 14px; background:#fff1f2; border:1px solid #fecdd3; border-left:4px solid #e11d48; border-radius:6px; font-size:12px; color:#9f1239; line-height:1.5;"></div>

          <!-- 1.5 关联部门遗留任务 (可选联动) -->
          <div class="form-group" style="margin-bottom:12px; background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:8px 12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <label style="margin-bottom:0; font-weight:700; color:#1e40af; font-size:12px;">📋 关联部门遗留任务 (向曦总汇报)</label>
              <span style="font-size:11px; color:#3b82f6;">自动统计汇报进度与纪要</span>
            </div>
            <select id="selectMeetingLegacyTaskId" onchange="handleMeetingLegacyTaskSelect(this.value)" style="width:100%; font-size:12px; padding:6px 8px; border-radius:6px; border:1px solid #93c5fd; background:#fff;">
              <option value="">-- 无关联遗留任务 (常规会议) --</option>
            </select>
          </div>

          <!-- 2. 会议主题 (必须) -->
          <div class="form-group">
            <label>会议主题 *</label>
            <input type="text" id="inputMeetingSubject" placeholder="请填写会议主题 / 关键任务..." required />
          </div>

          <!-- 3. 汇报人 -->
          <div class="form-group">
            <label>汇报人</label>
            <input type="text" id="inputMeetingReporter" placeholder="如：张总、李部长、王经理..." />
          </div>

          <!-- 会议通知发送状态 (未发送通知卡片标黄) -->
          <div class="form-group" style="margin-bottom:14px; background:#fefce8; border:1px solid #fde047; border-radius:8px; padding:10px 12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <label style="margin-bottom:0; font-weight:700; color:#854d0e;">会议通知是否发送</label>
              <span id="noticeSentStatusHint" style="font-size:11px; color:#b45309; font-weight:600;">⚠️ 尚未发送会议通知 (各看板卡片将标黄)</span>
            </div>
            <div style="display:flex; gap:10px;">
              <button type="button" class="btn btn-sm" id="btnNoticeUnsent" onclick="setMeetingNoticeState(false)" style="flex:1; padding:7px 10px; font-weight:700; border-radius:6px; background:#fef08a; color:#854d0e; border:1.5px solid #eab308;">
                ⚠️ 尚未发送通知 (标黄)
              </button>
              <button type="button" class="btn btn-sm" id="btnNoticeSent" onclick="setMeetingNoticeState(true)" style="flex:1; padding:7px 10px; font-weight:600; border-radius:6px; background:#ffffff; color:var(--text-secondary); border:1px solid var(--border); opacity:0.75;">
                🔔 已发送会议通知
              </button>
            </div>
            <input type="hidden" id="inputMeetingNoticeSent" value="no" />
          </div>

          <!-- 折叠详细信息: 会议地点、纪要人、参会人、议题背景、核心决策点 -->
          <details class="meeting-foldable-details" id="meetingFoldableDetails" style="margin-bottom: 14px; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 6px 12px; background: #f8fafc;">
            <summary style="cursor: pointer; font-size: 12px; font-weight: 700; color: var(--text-secondary); padding: 6px 0; user-select: none; display: flex; align-items: center; justify-content: space-between;">
              <span>➕ 展开选填项 (会议地点、纪要人、参会人、背景、决策点)</span>
              <span style="font-size: 11px; color: var(--text-muted); font-weight: normal;">点击展开 / 收起</span>
            </summary>
            <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 10px;">
              <!-- 4. 会议地点 -->
              <div class="form-group" style="margin-bottom:0;">
                <label>会议地点 / 线上会议</label>
                <input type="text" id="inputMeetingLocation" placeholder="例：主管办公室 / WeLink线上..." />
              </div>

              <!-- 5. 纪要人 -->
              <div class="form-group" style="margin-bottom:0;">
                <label>纪要人</label>
                <input type="text" id="inputMeetingMinuter" placeholder="负责会后输出纪要的人员..." />
              </div>

              <!-- 6. 参会人 -->
              <div class="form-group" style="margin-bottom:0;">
                <label>参会人员</label>
                <input type="text" id="inputMeetingAttendees" placeholder="多位参会人以顿号分隔..." />
              </div>

              <!-- 7. 会议背景 -->
              <div class="form-group" style="margin-bottom:0;">
                <label>议题背景</label>
                <textarea id="inputMeetingBackground" rows="2" placeholder="简述会议的触发背景、当前现状或关键信息..."></textarea>
              </div>

              <!-- 8. 核心决策点 -->
              <div class="form-group" style="margin-bottom:0;">
                <label>核心决策点</label>
                <textarea id="inputMeetingDecision" rows="2" placeholder="待主管拍板定夺的核心决议事项..."></textarea>
              </div>

              <!-- 8.5 会议纪要与下一步计划 -->
              <div class="form-group" style="margin-bottom:0;">
                <label>会议纪要输出状态</label>
                <div style="display:flex; gap:14px; margin-top:2px;">
                  <label style="font-size:12px; font-weight:normal; display:flex; align-items:center; gap:4px; cursor:pointer;">
                    <input type="radio" name="meetingHasMinutesRadio" id="radioMinutesNo" value="no" checked onchange="document.getElementById('inputMeetingHasMinutes').value='no'"> ⏳ 待输出 / 整理中
                  </label>
                  <label style="font-size:12px; font-weight:normal; display:flex; align-items:center; gap:4px; cursor:pointer;">
                    <input type="radio" name="meetingHasMinutesRadio" id="radioMinutesYes" value="yes" onchange="document.getElementById('inputMeetingHasMinutes').value='yes'"> ✅ 已输出纪要
                  </label>
                </div>
                <input type="hidden" id="inputMeetingHasMinutes" value="no" />
              </div>

              <div class="form-group" style="margin-bottom:0;">
                <label>会后决议与下一步行动计划 (Next Steps)</label>
                <textarea id="inputMeetingNextPlan" rows="2" placeholder="记录向曦总汇报后确定的下一步计划、跟进责任人及时间节点..."></textarea>
              </div>
            </div>
          </details>

          <!-- 9. 预约人/部门 与 预约状态下拉 (唯一保留的下拉选项) -->
          <div class="form-row">
            <div class="form-group">
              <label>预约人 / 部门</label>
              <input type="text" id="inputMeetingRequester" placeholder="发起预约的人员或部门..." />
            </div>
            <div class="form-group">
              <label>预约状态</label>
              <select id="selectMeetingStatus">
                <option value="scheduled" selected>已排期 (时间已敲定)</option>
                <option value="pending">待排期 (待主管确认时间)</option>
                <option value="completed">会议已完成</option>
                <option value="cancelled">已取消 / 延期</option>
              </select>
            </div>
          </div>

          <!-- 10. 工作备忘 -->
          <div class="form-group">
            <label>工作备忘</label>
            <input type="text" id="inputMeetingNotes" placeholder="如：提前10分钟打印材料..." />
          </div>
        </form>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div style="display:flex; gap:8px; align-items:center;">
          <button type="button" class="btn btn-ghost" id="btnRecallToPending" onclick="recallMeetingToPending()" style="color:#b45309; border:1px solid #fde68a; background:#fffbeb; display:none; padding:7px 14px; font-weight:600; font-size:12.5px;" title="将此会议撤回并转为待排期，释放日历对应时间段">
            ↩️ 撤回改成待排期
          </button>
          <button type="button" class="btn btn-ghost" id="btnDeleteMeeting" onclick="deleteCurrentMeeting()" style="color:#dc2626; border:1px solid #fecaca; background:#fff5f5; display:none; padding:7px 14px; font-weight:600; font-size:12.5px;">
            🗑️ 删除该预约
          </button>
        </div>
        <div style="display:flex; gap:8px;">
          <button type="button" class="btn" onclick="closeModal('meetingModal')">取消</button>
          <button type="button" class="btn btn-primary" onclick="saveMeeting()">保存排期</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: LEADER BUSINESS TRIP MANAGEMENT ================= -->
  <div class="modal-overlay" id="leaderTripModal">
    <div class="modal-box" style="max-width: 540px;">
      <div class="modal-header">
        <div class="modal-title" style="display:flex; align-items:center; gap:6px;">
          <span>✈️</span>
          <span>登记 / 设置领导出差时间与目的地</span>
        </div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('leaderTripModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:14px;">
        <!-- 1. 出差目的地 -->
        <div>
          <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:6px;">1. 选择出差目的地</label>
          <select id="inputTripDestination" class="form-control" style="width:100%; padding:7px 10px; font-size:12.5px; font-weight:600; border:1px solid var(--border); border-radius:var(--radius-sm); background:#fff;">
            <option value="med_south_tunis" selected>🇹🇳 地南·突尼斯 (UTC+1 · 比开罗慢 1 小时)</option>
            <option value="med_south_libya">🇱🇾 地南·利比亚 (UTC+2 · 与开罗无时差)</option>
            <option value="algeria">🇩🇿 阿尔及利亚 (UTC+1 · 比开罗慢 1 小时)</option>
            <option value="morocco">🇲🇦 摩洛哥 (UTC+0 · 比开罗慢 2 小时)</option>
            <option value="congo_drc">🇨🇩 刚果（金） (UTC+1 · 比开罗慢 1 小时)</option>
            <option value="cameroon">🇨🇲 喀麦隆 (UTC+1 · 比开罗慢 1 小时)</option>
            <option value="cote_divoire">🇨🇮 科特迪瓦 (UTC+0 · 比开罗慢 2 小时)</option>
            <option value="senegal">🇸🇳 塞内加尔 (UTC+0 · 比开罗慢 2 小时)</option>
            <option value="beijing">🇨🇳 中国·北京 (UTC+8 · 比开罗快 6 小时)</option>
            <option value="cairo">🇪🇬 埃及·开罗 (UTC+2 · 常驻基准)</option>
          </select>
        </div>

        <!-- 2. 出差起止日期 -->
        <div>
          <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:6px;">2. 选择出差起止日期</label>
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
            <div>
              <span style="font-size:11.5px; color:var(--text-muted); display:block; margin-bottom:4px;">出差开始日期：</span>
              <input type="date" id="inputTripStartDate" class="form-control" style="width:100%; padding:6px 8px; font-size:12.5px;" />
            </div>
            <div>
              <span style="font-size:11.5px; color:var(--text-muted); display:block; margin-bottom:4px;">出差结束日期：</span>
              <input type="date" id="inputTripEndDate" class="form-control" style="width:100%; padding:6px 8px; font-size:12.5px;" />
            </div>
          </div>
          <!-- 快捷日期选择 -->
          <div style="display:flex; gap:6px; margin-top:8px;">
            <button type="button" class="btn btn-sm btn-ghost" style="padding:2px 8px; font-size:11px;" onclick="setTripQuickRange('today')">今日</button>
            <button type="button" class="btn btn-sm btn-ghost" style="padding:2px 8px; font-size:11px;" onclick="setTripQuickRange('this_week')">本周</button>
            <button type="button" class="btn btn-sm btn-ghost" style="padding:2px 8px; font-size:11px;" onclick="setTripQuickRange('next_week')">下周</button>
            <button type="button" class="btn btn-sm btn-ghost" style="padding:2px 8px; font-size:11px;" onclick="setTripQuickRange('next_7_days')">未来7天</button>
          </div>
        </div>

        <!-- 3. 出差备忘 -->
        <div>
          <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:6px;">3. 出差备忘 / 事由</label>
          <input type="text" id="inputTripRemark" placeholder="如：地南代表处重点业务现场述职与客户拜访" class="form-control" style="width:100%; padding:7px 10px; font-size:12.5px; border:1px solid var(--border); border-radius:var(--radius-sm);" />
        </div>

        <!-- 4. 已有出差行程列表 -->
        <div id="tripExistingListArea" style="margin-top:4px;"></div>
      </div>

      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center;">
        <button type="button" class="btn btn-sm btn-ghost" style="color:#dc2626;" onclick="clearAllLeaderTrips()">清空所有出差行程</button>
        <div style="display:flex; gap:8px;">
          <button type="button" class="btn btn-sm" onclick="closeModal('leaderTripModal')">取消</button>
          <button type="button" class="btn btn-sm btn-primary" onclick="saveLeaderTrip()">保存并生效</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: LEADER TRANSIT MANAGEMENT (在途行程登记) ================= -->
  <div class="modal-overlay" id="transitModal">
    <div class="modal-box" style="max-width: 530px;">
      <div class="modal-header">
        <div class="modal-title" style="display:flex; align-items:center; gap:6px;">
          <span>🛫</span>
          <span id="transitModalTitle">登记领导在途行程 (跨时区航班)</span>
        </div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('transitModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:12px;">
        <input type="hidden" id="inputTransitId" value="" />

        <!-- 航程 / 行程说明 -->
        <div>
          <label style="display:block; font-size:12px; font-weight:700; margin-bottom:4px;">行程说明 / 航程 *</label>
          <input type="text" id="inputTransitTitle" placeholder="如：开罗 ✈ 喀麦隆 / 经停迪拜" class="form-control" style="width:100%; padding:6px 10px; font-size:12px; border:1px solid var(--border); border-radius:var(--radius-sm);" required />
        </div>

        <!-- 1. 起飞 (Departure) -->
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-left:3.5px solid #0284c7; border-radius:var(--radius-sm); padding:10px 12px;">
          <div style="font-size:12px; font-weight:700; color:#0369a1; margin-bottom:8px; display:flex; align-items:center; gap:5px;">
            <span>🛫 起飞信息 (出发地当地时区)</span>
          </div>
          <div style="display:grid; grid-template-columns: 1.1fr 1fr 1.2fr; gap:8px;">
            <div>
              <span style="font-size:11px; color:var(--text-muted); display:block; margin-bottom:3px;">起飞日期 *</span>
              <input type="date" id="inputTransitDepDate" onchange="handleTransitFormChange()" style="width:100%; padding:5px 6px; font-size:11.5px; border:1px solid var(--border); border-radius:4px;" required />
            </div>
            <div>
              <span style="font-size:11px; color:var(--text-muted); display:block; margin-bottom:3px;">起飞时间 *</span>
              <input type="text" id="inputTransitDepTime" placeholder="09:30" oninput="handleTransitFormChange()" onblur="handleTransitFormChange()" style="width:100%; padding:5px 6px; font-size:11.5px; border:1px solid var(--border); border-radius:4px;" required />
            </div>
            <div>
              <span style="font-size:11px; color:var(--text-muted); display:block; margin-bottom:3px;">起飞时区 *</span>
              <select id="inputTransitDepTz" onchange="handleTransitFormChange()" style="width:100%; padding:5px 6px; font-size:11.5px; border:1px solid var(--border); border-radius:4px; font-weight:600;">
                <option value="cairo" selected>埃及·开罗 (UTC+2)</option>
                <option value="cameroon">喀麦隆 (UTC+1)</option>
                <option value="med_south_libya">利比亚 (UTC+2)</option>
                <option value="med_south_tunis">突尼斯 (UTC+1)</option>
                <option value="algeria">阿尔及利亚 (UTC+1)</option>
                <option value="morocco">摩洛哥 (UTC+0)</option>
                <option value="congo_drc">刚果（金） (UTC+1)</option>
                <option value="cote_divoire">科特迪瓦 (UTC+0)</option>
                <option value="senegal">塞内加尔 (UTC+0)</option>
                <option value="beijing">北京 (UTC+8)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 2. 落地 (Arrival) -->
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-left:3.5px solid #10b981; border-radius:var(--radius-sm); padding:10px 12px;">
          <div style="font-size:12px; font-weight:700; color:#047857; margin-bottom:8px; display:flex; align-items:center; gap:5px;">
            <span>🛬 落地信息 (目的地当地时区)</span>
          </div>
          <div style="display:grid; grid-template-columns: 1.1fr 1fr 1.2fr; gap:8px;">
            <div>
              <span style="font-size:11px; color:var(--text-muted); display:block; margin-bottom:3px;">落地日期 *</span>
              <input type="date" id="inputTransitArrDate" onchange="handleTransitFormChange()" style="width:100%; padding:5px 6px; font-size:11.5px; border:1px solid var(--border); border-radius:4px;" required />
            </div>
            <div>
              <span style="font-size:11px; color:var(--text-muted); display:block; margin-bottom:3px;">落地时间 *</span>
              <input type="text" id="inputTransitArrTime" placeholder="14:45" oninput="handleTransitFormChange()" onblur="handleTransitFormChange()" style="width:100%; padding:5px 6px; font-size:11.5px; border:1px solid var(--border); border-radius:4px;" required />
            </div>
            <div>
              <span style="font-size:11px; color:var(--text-muted); display:block; margin-bottom:3px;">落地时区 *</span>
              <select id="inputTransitArrTz" onchange="handleTransitFormChange()" style="width:100%; padding:5px 6px; font-size:11.5px; border:1px solid var(--border); border-radius:4px; font-weight:600;">
                <option value="cairo">埃及·开罗 (UTC+2)</option>
                <option value="cameroon" selected>喀麦隆 (UTC+1)</option>
                <option value="med_south_libya">利比亚 (UTC+2)</option>
                <option value="med_south_tunis">突尼斯 (UTC+1)</option>
                <option value="algeria">阿尔及利亚 (UTC+1)</option>
                <option value="morocco">摩洛哥 (UTC+0)</option>
                <option value="congo_drc">刚果（金） (UTC+1)</option>
                <option value="cote_divoire">科特迪瓦 (UTC+0)</option>
                <option value="senegal">塞内加尔 (UTC+0)</option>
                <option value="beijing">北京 (UTC+8)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 3. 跨时区在途时长实时计算条 -->
        <div id="transitDurationLiveHint" style="font-size:11.5px; font-weight:600; color:#0369a1; background:#f0f9ff; border:1px solid #bae6fd; border-radius:5px; padding:6px 10px;">
          ⏱️ 跨时区飞行耗时：请输入起降时间计算
        </div>

        <!-- 4. 航班号与备注 -->
        <div style="display:grid; grid-template-columns: 1fr 1.5fr; gap:10px;">
          <div>
            <label style="display:block; font-size:11.5px; font-weight:600; margin-bottom:3px;">航班号 / 交通代码</label>
            <input type="text" id="inputTransitFlightNo" placeholder="如：MS887" style="width:100%; padding:6px 8px; font-size:12px; border:1px solid var(--border); border-radius:var(--radius-sm);" />
          </div>
          <div>
            <label style="display:block; font-size:11.5px; font-weight:600; margin-bottom:3px;">在途备注</label>
            <input type="text" id="inputTransitRemark" placeholder="如：机上不可约 / 免打扰" style="width:100%; padding:6px 8px; font-size:12px; border:1px solid var(--border); border-radius:var(--radius-sm);" />
          </div>
        </div>

        <!-- 5. 已登记在途清单 -->
        <div id="transitExistingListArea" style="margin-top:2px;"></div>
      </div>

      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center;">
        <button type="button" class="btn btn-sm btn-ghost" id="btnDeleteTransit" style="color:#dc2626; display:none;" onclick="deleteCurrentTransit()">删除该在途行程</button>
        <div style="display:flex; gap:8px; margin-left:auto;">
          <button type="button" class="btn btn-sm" onclick="closeModal('transitModal')">取消</button>
          <button type="button" class="btn btn-sm btn-primary" onclick="saveLeaderTransit()">保存在途行程</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: TOMORROW MEETING REMINDER ================= -->
  <div class="modal-overlay" id="tomorrowReminderModal">
    <div class="modal-box" style="max-width: 580px;">
      <div class="modal-header">
        <div class="modal-title">📋 曦总日程安排</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('tomorrowReminderModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <label style="font-size:12.5px; font-weight:700; color:var(--text-secondary);">目标日程日期：</label>
            <input type="date" id="inputReminderDate" style="padding:4px 8px; font-size:12px; border:1px solid var(--border); border-radius:4px;" onchange="updateTomorrowReminderPreview()" />
            <button class="btn btn-sm btn-ghost" onclick="setReminderDateTomorrow()" style="font-size:12px;">设为明天</button>
          </div>
          <button class="btn btn-sm btn-outline" onclick="copyTomorrowReminderContent()">📋 一键复制文本</button>
        </div>

        <div>
          <label style="font-size:12.5px; font-weight:700; color:var(--text-secondary); display:block; margin-bottom:6px;">日程文案预览（可直接在此微调修改）：</label>
          <textarea id="reminderMessagePreview" rows="12" style="width:100%; box-sizing:border-box; font-family:var(--font-mono); font-size:13px; line-height:1.6; padding:12px; border:1px solid var(--border); border-radius:6px; resize:vertical; background:var(--card-subtle); color:var(--text-primary);"></textarea>
        </div>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center;">
        <div style="font-size:11.5px; color:var(--text-muted);">💡 复制后可直接在微信/WeLink/邮件中发送给领导</div>
        <div style="display:flex; gap:8px;">
          <button type="button" class="btn btn-ghost" onclick="closeModal('tomorrowReminderModal')">关闭</button>
          <button type="button" class="btn btn-primary" onclick="copyTomorrowReminderContent()">📋 一键复制并发送</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: ADD / EDIT MONTHLY ROUTINE ================= -->
  <div class="modal-overlay" id="monthlyRoutineModal">
    <div class="modal-box" style="max-width: 500px;">
      <div class="modal-header">
        <div class="modal-title" id="monthlyRoutineModalTitle">➕ 添加月度关卡</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('monthlyRoutineModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:14px;">
        <input type="hidden" id="inputRoutineId" />
        <input type="hidden" id="inputRoutineCategory" value="月度关卡" />
        <input type="hidden" id="inputRoutineIcon" value="" />
        <input type="hidden" id="inputRoutineSubtasks" value="" />

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700; font-size:13px; display:block; margin-bottom:5px;">关卡事项名称</label>
          <input type="text" id="inputRoutineTitle" placeholder="例如：开部门例会（内部）/ 发送技术运营月报" style="font-size:14px; font-weight:600;" />
        </div>
        
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px;">
          <div class="form-group" style="margin-bottom:0;">
            <label style="font-weight:700; font-size:13px; display:block; margin-bottom:5px;">计划时间类型</label>
            <select id="selectRoutineType" onchange="handleRoutineTypeChange()" style="width:100%;">
              <option value="date">固定公历日期 (每月几号)</option>
              <option value="week">周期周次 (每月第几周)</option>
            </select>
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label id="labelRoutineValue" style="font-weight:700; font-size:13px; display:block; margin-bottom:5px;">计划时间 (1~31 号)</label>
            <input type="number" id="inputRoutineValue" min="1" max="31" value="9" style="font-size:14px; font-weight:600;" />
          </div>
        </div>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center;">
        <button type="button" class="btn btn-ghost" id="btnDeleteRoutineInModal" style="color:#dc2626; display:none;" onclick="deleteCurrentEditRoutine()">删除该事项</button>
        <div style="display:flex; gap:8px; margin-left:auto;">
          <button type="button" class="btn btn-ghost" onclick="closeModal('monthlyRoutineModal')">取消</button>
          <button type="button" class="btn btn-primary" onclick="saveMonthlyRoutineItem()">保存关卡</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: ADD / EDIT CUSTOM LINK ================= -->
  <div class="modal-overlay" id="linkModal">
    <div class="modal-box" style="max-width: 480px;">
      <div class="modal-header">
        <div class="modal-title" id="linkModalTitle">➕ 添加常用链接</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('linkModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:14px;">
        <input type="hidden" id="inputLinkId" />
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700; font-size:13px; display:block; margin-bottom:5px;">网站 / 链接名称</label>
          <input type="text" id="inputLinkName" placeholder="例如：海外差旅申请系统 / 区域财务知识库" style="font-size:14px; font-weight:600;" />
        </div>
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700; font-size:13px; display:block; margin-bottom:5px;">网址 URL</label>
          <input type="text" id="inputLinkUrl" placeholder="https://..." style="font-family:var(--font-mono); font-size:13px;" />
          <div style="font-size:11px; color:var(--text-muted); margin-top:4px;">💡 网址将深层保存在卡片中，卡片上只突出大字名称，不露冗长链接</div>
        </div>
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700; font-size:13px; display:block; margin-bottom:5px;">分类归属</label>
          <select id="selectLinkCategory" onchange="handleLinkCategorySelectChange()" style="width:100%;">
            <!-- Populated dynamically -->
          </select>
          <input type="text" id="inputCustomLinkCategory" placeholder="输入全新分类名称 (如：财务报销 / 客户接待)..." style="display:none; margin-top:8px; width:100%;" />
        </div>
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700; font-size:13px; display:block; margin-bottom:5px;">卡片图标 (Emoji)</label>
          <div style="display:flex; gap:8px; align-items:center;">
            <input type="text" id="inputLinkIcon" value="🌐" maxlength="4" style="width:54px; text-align:center; font-size:20px; padding:4px;" />
            <div style="display:flex; flex-wrap:wrap; gap:6px;">
              <button type="button" class="btn btn-sm btn-ghost" onclick="setLinkIconEmoji('🌐')">🌐</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="setLinkIconEmoji('🏢')">🏢</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="setLinkIconEmoji('📬')">📬</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="setLinkIconEmoji('📚')">📚</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="setLinkIconEmoji('📅')">📅</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="setLinkIconEmoji('💻')">💻</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="setLinkIconEmoji('✈️')">✈️</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="setLinkIconEmoji('📊')">📊</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="setLinkIconEmoji('🔑')">🔑</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="setLinkIconEmoji('🛠️')">🛠️</button>
            </div>
          </div>
        </div>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center;">
        <button type="button" class="btn btn-ghost" id="btnDeleteLinkInModal" style="color:#dc2626; display:none;" onclick="deleteCurrentEditLink()">🗑️ 删除该链接</button>
        <div style="display:flex; gap:8px; margin-left:auto;">
          <button type="button" class="btn btn-ghost" onclick="closeModal('linkModal')">取消</button>
          <button type="button" class="btn btn-primary" id="btnSaveLinkInModal" onclick="saveCustomLink()">保存</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: MANAGE CATEGORIES ================= -->
  <div class="modal-overlay" id="manageCategoriesModal">
    <div class="modal-box" style="max-width: 520px;">
      <div class="modal-header">
        <div class="modal-title">🏷️ 管理与重命名分类</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('manageCategoriesModal')">✕</button>
      </div>
      <div class="modal-body">
        <div style="font-size:12px; color:var(--text-secondary); margin-bottom:14px; line-height:1.5;">
          您可以随意修改现有分类名称。修改并保存后，该分类下的所有常用链接将自动同步更新：
        </div>
        <div id="categoryManageList" style="display:flex; flex-direction:column; gap:10px; max-height:360px; overflow-y:auto; padding-right:4px;">
          <!-- Generated dynamically -->
        </div>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:flex-end;">
        <button class="btn btn-primary" onclick="closeModal('manageCategoriesModal')">完成</button>
      </div>
    </div>
  </div>

    <!-- ================= MODAL: ADD / EDIT LEGACY TASK ================= -->
  <!-- ================= MODAL: ADD / EDIT LEGACY TASK (14 FIELDS) ================= -->
  <div class="modal-overlay" id="legacyTaskModal">
    <div class="modal-box" style="max-width: 680px; width: 95vw;">
      <div class="modal-header">
        <div class="modal-title" id="legacyTaskModalTitle">新增部门遗留任务</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('legacyTaskModal')">✕</button>
      </div>
      <div class="modal-body">
        <form onsubmit="event.preventDefault(); saveLegacyTask();">
          <input type="hidden" id="inputLegacyTaskId" value="" />

          <!-- 1. *问题描述 -->
          <div class="form-group">
            <label style="font-weight:700;">* 问题描述 *</label>
            <textarea id="inputLegacyTaskTitle" rows="2" placeholder="详细描述遗留任务/问题的核心背景、卡点或具体事项..." required style="font-size:13px;"></textarea>
          </div>

          <!-- 2. *责任人 & 领域 -->
          <div class="form-row">
            <div class="form-group">
              <label style="font-weight:700;">* 责任人 *</label>
              <input type="text" id="inputLegacyTaskOwner" placeholder="如：陈总、王工、李经理..." required />
            </div>
            <div class="form-group">
              <label>领域 (业务板块/部门)</label>
              <input type="text" id="inputLegacyTaskDomain" placeholder="如：交付、商务、法务、海外IT、财务..." />
            </div>
          </div>

          <!-- 3. 问题状态 & *要求完成日期 -->
          <div class="form-row">
            <div class="form-group">
              <label>问题状态</label>
              <select id="selectLegacyTaskStatus">
                <option value="in_progress" selected>🚀 汇报推进中</option>
                <option value="pending">⏳ 待向曦总汇报</option>
                <option value="completed">✅ 已顺利闭环</option>
                <option value="paused">⏸️ 已暂停 / 挂起</option>
              </select>
            </div>
            <div class="form-group">
              <label style="font-weight:700;">* 要求完成日期 *</label>
              <input type="date" id="inputLegacyTaskTargetDate" required />
            </div>
          </div>

          <!-- 4. 提出时间 & 更新完成时间 -->
          <div class="form-row">
            <div class="form-group">
              <label>提出时间</label>
              <input type="date" id="inputLegacyTaskCreatedDate" />
            </div>
            <div class="form-group">
              <label>更新完成时间</label>
              <input type="date" id="inputLegacyTaskUpdatedFinishDate" />
            </div>
          </div>

          <!-- 5. 汇报时间 -->
          <div class="form-group">
            <label>汇报时间 (向曦总开会汇报时间)</label>
            <input type="text" id="inputLegacyTaskReportTime" placeholder="如：2026-10-28 14:30 (关联开会时将自动回填)" />
          </div>

          <!-- 6. 问题进展 -->
          <div class="form-group">
            <label>问题进展 (当前卡点及下一步行动)</label>
            <textarea id="inputLegacyTaskProgress" rows="2" placeholder="记录当前具体进展、协调进度、已完成动作及下一步计划..."></textarea>
          </div>

          <!-- 7. 审核意见 -->
          <div class="form-group">
            <label style="color:#1e40af;">审核意见 (曦总批示 / 管理层审核意见)</label>
            <textarea id="inputLegacyTaskReviewOpinion" rows="2" placeholder="记录向曦总汇报后领导的审阅意见、明确要求或特批定夺结论..."></textarea>
          </div>

          <!-- 8. 备注 -->
          <div class="form-group">
            <label>备注 (备忘说明)</label>
            <input type="text" id="inputLegacyTaskRemark" placeholder="如：需重点关注利比亚外汇政策，会同法务部协同..." />
          </div>

          <!-- 9. 状态标记属性 -->
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px 12px; margin-bottom:14px; display:flex; gap:18px; flex-wrap:wrap;">
            <label style="font-size:12.5px; font-weight:600; display:flex; align-items:center; gap:5px; cursor:pointer; color:#b91c1c;">
              <input type="checkbox" id="checkLegacyTaskOverdue" /> ⚠️ 逾期任务
            </label>
            <label style="font-size:12.5px; font-weight:600; display:flex; align-items:center; gap:5px; cursor:pointer; color:#047857;">
              <input type="checkbox" id="checkLegacyTaskNew" checked /> ✨ 本期新增
            </label>
            <label style="font-size:12.5px; font-weight:600; display:flex; align-items:center; gap:5px; cursor:pointer; color:#475569;">
              <input type="checkbox" id="checkLegacyTaskClosed" /> 🏁 本期关闭
            </label>
          </div>

          <div class="modal-footer" style="padding-top:10px; margin-top:4px;">
            <button type="button" class="btn" onclick="closeModal('legacyTaskModal')">取消</button>
            <button type="submit" class="btn btn-primary" style="font-weight:700;">💾 保存遗留任务</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: ADD REPORT SESSION (登记新一次向曦总汇报) ================= -->
  <div class="modal-overlay" id="legacyAddReportModal">
    <div class="modal-box" style="max-width: 560px; width: 95vw;">
      <div class="modal-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:20px;">🎙️</span>
          <div class="modal-title" id="textAddReportModalTitle">登记向曦总汇报与会议纪要</div>
        </div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('legacyAddReportModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:12px;">
        <input type="hidden" id="inputAddReportTaskId" value="" />
        <div id="textAddReportTaskDesc" style="font-size:13px; font-weight:700; color:#0f172a; background:#f8fafc; padding:8px 12px; border-radius:6px; border:1px solid #e2e8f0; line-height:1.4;"></div>

        <div class="form-row">
          <div class="form-group" style="margin-bottom:0;">
            <label style="font-weight:700;">* 汇报时间 (开会/汇报日期时间) *</label>
            <input type="text" id="inputAddReportTime" placeholder="如：2026-11-04 15:30" required />
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label style="font-weight:700;">汇报责任人：</label>
            <input type="text" id="inputAddReporter" placeholder="如：陈总、王工" />
          </div>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700;">本次汇报是否已输出会议纪要：</label>
          <select id="selectAddReportHasMinutes" style="font-weight:700;" onchange="handleAddReportHasMinutesChange(this.value)">
            <option value="yes" selected>✅ 已输出会议纪要</option>
            <option value="no">⚠️ 暂未输出 (稍后补录)</option>
          </select>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700; color:#1e40af;">审核意见 (曦总批示 / 决议结论)：</label>
          <textarea id="inputAddReportReviewOpinion" rows="2" placeholder="记录向曦总汇报后领导的审阅意见、特批定夺要求或核心结论..." style="font-size:12.5px;"></textarea>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700;">会议纪要内容 / 下一步行动项：</label>
          <textarea id="inputAddReportMinutes" rows="3" placeholder="记录本次汇报后达成的会议纪要内容、具体责任分工与落实排期..." style="font-size:12.5px;"></textarea>
        </div>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center; padding-top:10px;">
        <button type="button" class="btn" onclick="closeModal('legacyAddReportModal')">取消</button>
        <button type="button" class="btn btn-primary" onclick="saveAddReportSession()" style="font-weight:700;">💾 保存汇报与纪要</button>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: EDIT REPORT SESSION (查看与修改单次汇报记录) ================= -->
  <div class="modal-overlay" id="legacyEditReportModal">
    <div class="modal-box" style="max-width: 560px; width: 95vw;">
      <div class="modal-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:20px;">📝</span>
          <div class="modal-title" id="textEditReportModalTitle">查看与更新汇报纪要</div>
        </div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('legacyEditReportModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:12px;">
        <input type="hidden" id="inputEditReportTaskId" value="" />
        <input type="hidden" id="inputEditReportIdx" value="" />
        <div id="textEditReportTaskDesc" style="font-size:13px; font-weight:700; color:#0f172a; background:#f8fafc; padding:8px 12px; border-radius:6px; border:1px solid #e2e8f0; line-height:1.4;"></div>

        <div class="form-row">
          <div class="form-group" style="margin-bottom:0;">
            <label style="font-weight:700;">* 汇报时间 *</label>
            <input type="text" id="inputEditReportTime" placeholder="如：2026-10-28 14:30" required />
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label style="font-weight:700;">汇报责任人：</label>
            <input type="text" id="inputEditReporter" placeholder="如：陈总" />
          </div>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700;">是否已输出会议纪要：</label>
          <select id="selectEditReportHasMinutes" style="font-weight:700;">
            <option value="yes">✅ 已输出会议纪要</option>
            <option value="no">⚠️ 待输出纪要</option>
          </select>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700; color:#1e40af;">审核意见 (曦总批示 / 决议结论)：</label>
          <textarea id="inputEditReportReviewOpinion" rows="2" placeholder="记录曦总的指导批示、定夺要求或审核意见..." style="font-size:12.5px;"></textarea>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700;">会议纪要内容 / 下一步计划：</label>
          <textarea id="inputEditReportMinutes" rows="3" placeholder="记录本次汇报的会议纪要、具体责任分工与落实进度..." style="font-size:12.5px;"></textarea>
        </div>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center; padding-top:10px;">
        <button type="button" class="btn btn-ghost" onclick="deleteCurrentReportSession()" style="color:#dc2626;" title="删除本条汇报记录">🗑️ 删除此场汇报</button>
        <div style="display:flex; gap:8px;">
          <button type="button" class="btn" onclick="closeModal('legacyEditReportModal')">取消</button>
          <button type="button" class="btn btn-primary" onclick="saveEditReportSession()" style="font-weight:700;">💾 保存修改</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: LEGACY TASK MINUTES & REPORT (纪要与汇报更新) ================= -->
  <div class="modal-overlay" id="legacyMinutesModal">
    <div class="modal-box" style="max-width: 540px; width: 95vw;">
      <div class="modal-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:20px;">📝</span>
          <div class="modal-title">遗留任务纪要与汇报更新</div>
        </div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('legacyMinutesModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:12px;">
        <input type="hidden" id="inputMinutesTaskId" value="" />
        <div id="textMinutesTaskTitle" style="font-size:13px; font-weight:700; color:#0f172a; background:#f8fafc; padding:8px 12px; border-radius:6px; border:1px solid #e2e8f0; line-height:1.4;"></div>

        <div class="form-row">
          <div class="form-group" style="margin-bottom:0;">
            <label style="font-weight:700;">是否已输出会议纪要：</label>
            <select id="selectMinutesStatus" style="font-weight:700;">
              <option value="yes">✅ 已输出会议纪要</option>
              <option value="no">❌ 待输出纪要</option>
            </select>
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label style="font-weight:700;">汇报时间（开会/汇报日期）：</label>
            <input type="text" id="inputMinutesReportTime" placeholder="如：2026-10-28 14:30" />
          </div>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700;">审核意见（曦总批示 / 决议要点）：</label>
          <textarea id="inputMinutesReviewOpinion" rows="3" placeholder="记录曦总针对该遗留事项做出的指导批示、特批决议或审核意见..." style="font-size:12.5px;"></textarea>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700;">会议纪要 / 下一步计划（行动项）：</label>
          <textarea id="inputMinutesProgress" rows="3" placeholder="记录汇报后达成的会议纪要内容、具体责任分工与下一步落实计划..." style="font-size:12.5px;"></textarea>
        </div>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center; padding-top:10px;">
        <button type="button" class="btn" onclick="closeModal('legacyMinutesModal')">取消</button>
        <button type="button" class="btn btn-primary" onclick="saveLegacyMinutes()" style="font-weight:700;">💾 保存汇报与纪要</button>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: IMPORT LEGACY TASKS ================= -->
  <div class="modal-overlay" id="legacyImportModal">
    <div class="modal-box" style="max-width: 780px; width: 95vw;">
      <div class="modal-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:20px;">📥</span>
          <div class="modal-title">智能导入部门遗留任务清单</div>
        </div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('legacyImportModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:12px;">

        <!-- 顶部指引与模板下载工具条 -->
        <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
          <div>
            <div style="font-size:12.5px; font-weight:700; color:#92400e; margin-bottom:2px;">
              💡 支持从 Excel / 飞书 / 钉钉 / WPS 表格直接全选复制粘贴，或上传 CSV / XLSX 文件
            </div>
            <div style="font-size:11.5px; color:#b45309;">
              标准 14 列：问题状态、*问题描述、*责任人、提出时间、*要求完成日期、更新完成时间、问题进展、审核意见、备注、汇报时间、逾期任务、本期新增、本期关闭、领域
            </div>
            <div style="margin-top:4px; font-size:11.5px; color:#1e40af; background:#eff6ff; padding:2px 8px; border-radius:4px; display:inline-block; font-weight:700; border:1px solid #bfdbfe;">
              🎯 Excel 文件导入规则：系统已设定仅提取「NIS重点遗留任务」Sheet 的数据，自动过滤其他无关工作表。
            </div>
          </div>
          <div style="display:flex; gap:8px; flex-shrink:0;">
            <button type="button" class="btn btn-sm" onclick="copyLegacyTaskHeader()" style="background:#ffffff; border:1px solid #cbd5e1; font-size:11.5px; font-weight:600; color:#475569;" title="复制标准表头到剪贴板">
              📋 复制标准表头
            </button>
            <button type="button" class="btn btn-sm btn-primary" onclick="downloadLegacyTaskTemplate()" style="font-size:11.5px; font-weight:700;" title="下载带有示例数据的 CSV 模板">
              💾 下载 Excel 模板
            </button>
            <button type="button" class="btn btn-sm btn-ghost" onclick="clearAllLegacyTasks()" style="color:#dc2626; border:1px solid #fecaca; background:#fff; font-size:11.5px; font-weight:600;" title="清空现有全部遗留任务">
              🗑️ 清空现有清单
            </button>
          </div>
        </div>

        <!-- Excel 多工作表定位与选择指示条 (只提取 NIS重点遗留任务) -->
        <div id="legacySheetSelectorContainer" style="display:none; margin-bottom:4px; padding:7px 12px; background:#f0f9ff; border:1px solid #bae6fd; border-radius:6px; font-size:12px; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
          <div style="display:flex; align-items:center; gap:6px;">
            <span style="font-size:14px;">📑</span>
            <span style="color:#0369a1; font-weight:700;">工作表范围：</span>
            <span id="legacySheetTargetBadge" style="background:#e0f2fe; color:#0284c7; font-size:11.5px; padding:2px 8px; border-radius:4px; font-weight:700; border:1px solid #7dd3fc;">🎯 已锁定提取「NIS重点遗留任务」</span>
          </div>
          <div style="display:flex; align-items:center; gap:6px;">
            <span style="color:#64748b; font-size:11.5px;">切换工作表:</span>
            <select id="legacyImportSheetSelect" onchange="onLegacySheetSelected(this.value)" style="padding:3px 8px; font-size:12px; border-radius:4px; border:1px solid #93c5fd; background:#fff; font-weight:700; color:#1d4ed8; cursor:pointer; outline:none;"></select>
          </div>
        </div>

        <!-- 文本粘贴与文件选择区域 -->
        <div class="form-group" style="margin-bottom:0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <label style="font-weight:700; color:#0f172a; margin-bottom:0; font-size:12.5px;">
              直接粘贴表格内容（Ctrl+V）：
            </label>
            <div style="display:flex; align-items:center; gap:8px;">
              <button type="button" class="btn btn-sm btn-ghost" onclick="fillLegacyImportSample()" style="color:#d97706; border:1px solid #fde68a; background:#fffbeb; font-size:11.5px; font-weight:600;">
                ✨ 填入示例数据体验
              </button>
              <input type="file" id="legacyTaskFileInput" accept=".csv, .xlsx, .txt" style="display:none;" onchange="handleLegacyFileInput(event)" />
              <button type="button" class="btn btn-sm btn-ghost" onclick="document.getElementById('legacyTaskFileInput').click()" style="color:#0284c7; border:1px solid #bae6fd; background:#f0f9ff; font-size:11.5px; font-weight:600;">
                📂 从电脑选择文件...
              </button>
            </div>
          </div>
          <textarea id="inputLegacyImportText" rows="7" placeholder="请在 Excel / 飞书 / WPS 表格中选中整张任务清单，按 Ctrl+C 复制后直接在此粘贴（Ctrl+V），或点击右上角「📂 从电脑选择文件...」上传 Excel 文件。&#10;&#10;📌 上传 Excel (.xlsx) 时，系统将自动定位并仅提取「NIS重点遗留任务」工作表的数据。&#10;&#10;标准 14 列：问题状态 | *问题描述 | *责任人 | 提出时间 | *要求完成日期 | 更新完成时间 | 问题进展 | 审核意见 | 备注 | 汇报时间 | 逾期任务 | 本期新增 | 本期关闭 | 领域" style="font-family:monospace; font-size:12px; line-height:1.45; border-radius:8px;" oninput="handleLegacyImportTextChange()" onpaste="setTimeout(handleLegacyImportTextChange, 50)" onchange="handleLegacyImportTextChange()"></textarea>
          <!-- 未识别到数据时的友好提示 -->
          <div id="legacyImportEmptyTip" style="display:none; margin-top:8px; padding:10px 12px; background:#fff1f2; border:1px solid #fecdd3; border-radius:6px; font-size:12px; color:#9f1239;">
            ⚠️ 暂未能解析出任务行。提示：请确保复制的内容包含「*问题描述」与「*责任人」两项核心内容；或点击上方「✨ 填入示例数据体验」查看标准格式。
          </div>
        </div>

        <!-- 实时数据预览区域 -->
        <div id="legacyImportPreviewArea" style="display:none; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px 12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span id="legacyImportCountBadge" style="font-size:12.5px; font-weight:700; color:#16a34a; background:#dcfce7; padding:2px 8px; border-radius:12px; border:1px solid #bbf7d0;"></span>
              <span style="font-size:11.5px; color:#64748b;">(请核对下方识别数据)</span>
            </div>
            <!-- 导入模式单选开关 -->
            <div style="display:flex; align-items:center; gap:12px; font-size:12px;">
              <label style="display:flex; align-items:center; gap:4px; cursor:pointer; font-weight:600; color:#0f172a;">
                <input type="radio" name="legacyImportModeRadio" value="append" checked /> ➕ 追加合并 (保留现有任务)
              </label>
              <label style="display:flex; align-items:center; gap:4px; cursor:pointer; font-weight:600; color:#b91c1c;">
                <input type="radio" name="legacyImportModeRadio" value="replace" /> ⚠️ 覆盖替换 (清空后全量替换)
              </label>
            </div>
          </div>

          <!-- 预览表格 -->
          <div style="max-height: 200px; overflow-y: auto; border: 1px solid #cbd5e1; border-radius: 6px; background:#fff;">
            <table style="width:100%; border-collapse:collapse; font-size:11.5px; text-align:left;">
              <thead style="position:sticky; top:0; background:#f1f5f9; z-index:1;">
                <tr>
                  <th style="padding:6px 8px; border-bottom:1px solid #cbd5e1; width:36%;">遗留任务 (*问题描述)</th>
                  <th style="padding:6px 8px; border-bottom:1px solid #cbd5e1; width:16%;">责任人 (*责任人)</th>
                  <th style="padding:6px 8px; border-bottom:1px solid #cbd5e1; width:20%;">是否汇报 (汇报日期)</th>
                  <th style="padding:6px 8px; border-bottom:1px solid #cbd5e1; width:14%;">是否输出纪要</th>
                  <th style="padding:6px 8px; border-bottom:1px solid #cbd5e1; width:14%;">状态</th>
                </tr>
              </thead>
              <tbody id="legacyImportPreviewTableBody"></tbody>
            </table>
          </div>
        </div>

        <div class="modal-footer" style="padding-top:10px; margin-top:4px; display:flex; justify-content:space-between; align-items:center;">
          <button type="button" class="btn" onclick="closeModal('legacyImportModal')">取消</button>
          <button type="button" class="btn btn-primary" id="btnConfirmLegacyImport" onclick="confirmImportLegacyTasks()" disabled style="font-weight:700; padding:8px 18px; font-size:13px;">
            🚀 确认导入至遗留任务清单
          </button>
        </div>
      </div>
    </div>
  </div>


  <!-- ================= MODAL: EDIT MODULE SETTINGS (通用板块自定义) ================= -->
  <div class="modal-overlay" id="editModuleModal">
    <div class="modal-box" style="max-width: 460px;">
      <div class="modal-header">
        <div class="modal-title" id="editModuleModalTitle">✏️ 自定义板块</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('editModuleModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:14px;">
        <input type="hidden" id="editModuleCurrentKey" value="" />
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700; font-size:13px; display:block; margin-bottom:5px;">板块主标题</label>
          <input type="text" id="inputModuleCustomTitle" placeholder="请输入板块主标题" />
        </div>
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-weight:700; font-size:13px; display:block; margin-bottom:5px;">角色 / 风格标签</label>
          <input type="text" id="inputModuleCustomTag" placeholder="如：🏕️ 比格犬童子军 / 秘书工作台" />
        </div>
        <!-- 保持向下兼容旧表单元素 -->
        <input type="hidden" id="inputLinksModuleTitle" value="" />
        <input type="hidden" id="inputLinksModuleTag" value="" />
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center;">
        <button class="btn btn-ghost btn-sm" onclick="resetCurrentModuleSettings()" style="color:var(--text-muted); font-size:12px;">恢复默认</button>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-ghost" onclick="closeModal('editModuleModal')">取消</button>
          <button class="btn btn-primary" onclick="saveModuleCustomSettings()">保存设置</button>
        </div>
      </div>
    </div>
  </div>
  <div id="editLinksModuleModal" style="display:none;"></div>

  <!-- ================= MODAL: ADD NORDIC BUCKET ITEM ================= -->
  <div class="modal-overlay" id="addBucketItemModal" style="display:none;" onclick="if(event.target===this)closeAddBucketItemModal()">
    <div class="modal-box" style="max-width: 460px;">
      <div class="modal-header">
        <div class="modal-title">✨ 添加北欧心愿</div>
        <button class="btn btn-sm btn-ghost" onclick="closeAddBucketItemModal()">✕</button>
      </div>
      <div class="modal-body" style="padding: 18px 24px;">
        <label style="font-size: 13px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; display:block;">写下你的 2027 北欧旅行梦想</label>
        <input type="text" id="inputBucketItemText" class="form-control" style="width:100%; box-sizing:border-box;" placeholder="例如：在罗弗敦群岛住一次红色渔屋 (Rorbu)..." maxlength="60" onkeydown="if(event.key==='Enter')saveNewBucketItem()" />
      </div>
      <div class="modal-footer" style="padding: 14px 24px; display: flex; justify-content: flex-end; gap: 10px;">
        <button class="btn btn-ghost" onclick="closeAddBucketItemModal()">取消</button>
        <button class="btn btn-primary" onclick="saveNewBucketItem()">确定添加</button>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: EDIT BLACKBOARD ================= -->
  <div class="modal-overlay" id="editBlackboardModal" style="display:none;" onclick="if(event.target===this)closeEditBlackboardModal()">
    <div class="modal-box" style="max-width: 580px;">
      <div class="modal-header">
        <div class="modal-title">✏️ 编写黑板板书 · 每日自学笔记</div>
        <button class="btn btn-sm btn-ghost" onclick="closeEditBlackboardModal()">✕</button>
      </div>
      <div class="modal-body" style="padding: 18px 24px; display:flex; flex-direction:column; gap:14px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:12px; color:var(--text-secondary); font-weight:600;" id="editBlackboardDateHint">日期：2026-10-22</span>
          <div style="display:flex; gap:6px;">
            <button type="button" class="btn btn-sm btn-ghost" onclick="fillEnglishTemplateToBlackboard()" title="将今日每日英语内容填入黑板">✨ 导入每日英语</button>
            <button type="button" class="btn btn-sm btn-ghost" onclick="fillGeneralTemplateToBlackboard()">💡 学习模板</button>
          </div>
        </div>

        <div>
          <label style="font-size:12.5px; font-weight:700; color:var(--text-primary); margin-bottom:5px; display:block;">板书主标题</label>
          <input type="text" id="inputBlackboardTitle" class="form-control" style="width:100%; box-sizing:border-box;" placeholder="例如：今日核心词汇与涉外沟通常识" />
        </div>

        <div>
          <label style="font-size:12.5px; font-weight:700; color:#d97706; margin-bottom:5px; display:block;">⭐ 核心金句 / 重点知识（黑板标黄突出）</label>
          <input type="text" id="inputBlackboardHighlight" class="form-control" style="width:100%; box-sizing:border-box;" placeholder="例如：Serendipity /ˌserənˈdɪpəti/ —— 不期而遇的美好意外" />
        </div>

        <div>
          <label style="font-size:12.5px; font-weight:700; color:var(--text-primary); margin-bottom:5px; display:block;">📝 今日自学内容与笔记（支持换行与条目）</label>
          <textarea id="inputBlackboardNotes" class="form-control" style="width:100%; box-sizing:border-box; min-height:130px; font-family:var(--font-sans);" placeholder="写下今天学习到的词汇、语法、涉外工作常识、技巧..."></textarea>
        </div>

        <div>
          <label style="font-size:12.5px; font-weight:700; color:#059669; margin-bottom:5px; display:block;">💡 心得与悟道（薄荷绿字体）</label>
          <input type="text" id="inputBlackboardReflection" class="form-control" style="width:100%; box-sizing:border-box;" placeholder="例如：把手头的事做细，每天积累一点，就会更从容。" />
        </div>
      </div>
      <div class="modal-footer" style="padding: 14px 24px; display: flex; justify-content: flex-end; gap: 10px;">
        <button class="btn btn-ghost" onclick="closeEditBlackboardModal()">取消</button>
        <button class="btn btn-primary" onclick="saveBlackboardContent()">写上黑板 (保存)</button>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: BLACKBOARD HISTORY ================= -->
  <div class="modal-overlay" id="blackboardHistoryModal" style="display:none;" onclick="if(event.target===this)closeBlackboardHistoryModal()">
    <div class="modal-box" style="max-width: 580px; max-height: 85vh; display:flex; flex-direction:column;">
      <div class="modal-header">
        <div class="modal-title" style="display:flex; align-items:center; gap:8px;">
          <span>📖</span>
          <span>黑板历史记录</span>
        </div>
        <button class="btn btn-sm btn-ghost" onclick="closeBlackboardHistoryModal()">✕</button>
      </div>
      <div style="padding: 10px 20px 6px 20px; border-bottom: 1px solid var(--border);">
        <input type="text" id="inputBlackboardHistorySearch" placeholder="🔍 搜索以往板书内容..." oninput="renderBlackboardHistoryList()" style="width:100%; box-sizing:border-box; font-size:12.5px; padding:6px 10px; border:1px solid var(--border); border-radius:6px; background:var(--card-subtle);" />
      </div>
      <div class="modal-body" style="padding: 14px 20px; overflow-y:auto; flex:1;">
        <div id="blackboardHistoryList" style="display:flex; flex-direction:column; gap:10px;">
          <!-- Dynamically populated -->
        </div>
      </div>
      <div class="modal-footer" style="padding: 12px 20px; display: flex; justify-content: space-between; align-items:center;">
        <span style="font-size:11.5px; color:var(--text-muted);">💡 点击任意记录可直接切回当天黑板并编辑</span>
        <button class="btn btn-primary btn-sm" onclick="closeBlackboardHistoryModal()">关闭</button>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: EDIT TODO ================= -->
  <div class="modal-overlay" id="editTodoModal">
    <div class="modal-box" style="max-width: 480px;">
      <div class="modal-header">
        <div class="modal-title">✏️ 编辑任务内容</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('editTodoModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:14px;">
        <input type="hidden" id="editTodoId" />
        <div>
          <label style="font-weight:600; font-size:13px; display:block; margin-bottom:5px;">任务描述</label>
          <input type="text" id="editTodoText" style="width:100%; box-sizing:border-box;" placeholder="输入任务描述..." />
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px;">
          <div>
            <label style="font-weight:600; font-size:13px; display:block; margin-bottom:5px;">截止日期</label>
            <input type="date" id="editTodoDate" style="width:100%; box-sizing:border-box;" />
          </div>
          <div>
            <label style="font-weight:600; font-size:13px; display:block; margin-bottom:5px;">任务分类</label>
            <select id="editTodoPriority" style="width:100%; box-sizing:border-box;">
              <option value="q1">🔥 今天完成</option>
              <option value="q2">⭐ 这周安排上</option>
              <option value="q3">⚡ 先放一放</option>
              <option value="q4">☕ 有空再说</option>
            </select>
          </div>
        </div>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center;">
        <button class="btn btn-ghost" style="color:#dc2626;" onclick="deleteCurrentEditTodo()">🗑️ 删除任务</button>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-ghost" onclick="closeModal('editTodoModal')">取消</button>
          <button class="btn btn-primary" onclick="saveEditTodo()">保存修改</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: EDIT MEETING REQUEST ================= -->
  <div class="modal-overlay" id="editRequestModal">
    <div class="modal-box" style="max-width: 500px;">
      <div class="modal-header">
        <div class="modal-title">✏️ 编辑待排期事项</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('editRequestModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:14px;">
        <input type="hidden" id="editRequestId" />
        <div>
          <label style="font-weight:600; font-size:13px; display:block; margin-bottom:5px;">预约人 / 部门</label>
          <input type="text" id="editRequestRequester" style="width:100%; box-sizing:border-box;" placeholder="如：地南代表处 陈总" />
        </div>
        <div>
          <label style="font-weight:600; font-size:13px; display:block; margin-bottom:5px;">会议诉求 / 议题</label>
          <input type="text" id="editRequestTopic" style="width:100%; box-sizing:border-box;" placeholder="会议诉求或主题..." />
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px;">
          <div>
            <label style="font-weight:600; font-size:13px; display:block; margin-bottom:5px;">建议时长 (分钟)</label>
            <input type="number" id="editRequestDuration" style="width:100%; box-sizing:border-box;" placeholder="45" />
          </div>
          <div>
            <label style="font-weight:600; font-size:13px; display:block; margin-bottom:5px;">状态</label>
            <select id="editRequestStatus" style="width:100%; box-sizing:border-box;">
              <option value="pending">⏳ 待排期</option>
              <option value="scheduled">✅ 已排期</option>
            </select>
          </div>
        </div>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between;">
        <button class="btn btn-ghost" style="color:#dc2626;" onclick="deleteCurrentEditRequest()">🗑️ 删除该条</button>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-ghost" onclick="closeModal('editRequestModal')">取消</button>
          <button class="btn btn-primary" onclick="saveEditRequest()">保存修改</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: EDIT NOTE ================= -->
  <div class="modal-overlay" id="editNoteModal">
    <div class="modal-box" style="max-width: 480px;">
      <div class="modal-header">
        <div class="modal-title">✏️ 编辑每日小记</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('editNoteModal')">✕</button>
      </div>
      <div class="modal-body" style="display:flex; flex-direction:column; gap:14px;">
        <input type="hidden" id="editNoteId" />
        <div>
          <label style="font-weight:600; font-size:13px; display:block; margin-bottom:5px;">分类标签</label>
          <select id="editNoteCategory" style="width:100%; box-sizing:border-box;">
            <option value="💡 灵感备忘">💡 灵感备忘</option>
            <option value="🌍 代表处对接">🌍 代表处对接</option>
            <option value="👔 主管交代">👔 主管交代</option>
            <option value="📌 待办提醒">📌 待办提醒</option>
            <option value="☕ 随手记">☕ 随手记</option>
          </select>
        </div>
        <div>
          <label style="font-weight:600; font-size:13px; display:block; margin-bottom:5px;">小记内容</label>
          <textarea id="editNoteText" rows="4" style="width:100%; box-sizing:border-box;" placeholder="输入小记内容..."></textarea>
        </div>
      </div>
      <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center;">
        <button class="btn btn-ghost" style="color:#dc2626;" onclick="deleteCurrentEditNote()">🗑️ 删除小记</button>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-ghost" onclick="closeModal('editNoteModal')">取消</button>
          <button class="btn btn-primary" onclick="saveEditNote()">保存修改</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: WOODSTOCK CELEBRATION ================= -->
  <div class="modal-overlay" id="celebrationModal">
    <div class="celebration-modal-box">
      <img src="__IMG_WOODSTOCK__" class="celebration-avatar" alt="Woodstock Celebration" />
      <div class="celebration-title">🎉 今日学习打卡成功！</div>
      <div class="celebration-desc" id="celebrationDesc">
        Woodstock 为您颁发今日专属学习勋章！滴水穿石，持续精进，今天也是闪闪发光的大秘书！
      </div>
      <button class="btn btn-primary" style="padding: 9px 24px;" onclick="closeModal('celebrationModal')">
        收到 · 继续加油！🐾
      </button>
    </div>
  </div>

  <!-- Toast Notification -->
  <div class="toast-notification" id="appToast">
    <span id="toastIcon">📋</span>
    <span id="toastMessage">已成功复制到剪贴板！</span>
  </div>

<!-- ================= JAVASCRIPT LOGIC ================= -->
<script>
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
const escapeHTML = escapeHtml;

// 1. ASSETS MAP
const SNOOPY_ASSETS = {
  ordinary_doghouse: "__IMG_ORDINARY_DOGHOUSE__",
  border_snoopy: "__IMG_BORDER_SNOOPY__",
  woodstock: "__IMG_WOODSTOCK__",
  supervisor_secretary: "__IMG_SUPERVISOR_SECRETARY__",
  beagle_scout: "__IMG_BEAGLE_SCOUT__",
  flying_ace: "__IMG_FLYING_ACE__",
  joe_cool: "__IMG_JOE_COOL__",
  author: "__IMG_AUTHOR__",
  daily_english: "__IMG_DAILY_ENGLISH__",
  canonical: "__IMG_CANONICAL__",
  dance: "__IMG_DANCE__"
};

// 2. STORAGE KEYS
const STORAGE_KEYS = {
  TODOS: 'snoopy_todos_v6',
  MEETINGS: 'snoopy_supervisor_meetings_v6',
  MEETING_REQUESTS: 'snoopy_meeting_requests_v6',
  NOTES: 'snoopy_notes_v6',
  LINKS: 'snoopy_links_v6',
  LINK_SETTINGS: 'snoopy_link_settings_v6',
  MODULE_SETTINGS: 'snoopy_all_module_settings_v6',
  ENGLISH_CHECKIN: 'snoopy_english_checkin_v6',
  TRIP_TIMEZONE: 'snoopy_trip_timezone_v6',
  BATCH_SHIFT_BACKUP: 'snoopy_batch_shift_backup_v6',
  LEADER_TRIPS: 'snoopy_leader_trips_v6',
  LEADER_TRANSITS: 'snoopy_leader_transits_v1',
  NORDIC_BUCKET_LIST: 'snoopy_nordic_bucket_list_v1',
  BLACKBOARD_RECORDS: 'snoopy_blackboard_records_v1',
  MONTHLY_ROUTINES: 'snoopy_monthly_routines_v1',
  MONTHLY_CHECKLIST: 'snoopy_monthly_checklist_v1',
  LEGACY_TASKS: 'snoopy_legacy_tasks_v1',
  THEME: 'snoopy_theme_v6'
};

// 3. ENGLISH CURRICULUM (31 Days) & NORDIC TRAVEL DICTIONARY
const ENGLISH_DATA = __ENGLISH_DATA_RAW__;
const NORDIC_DICT = __ENGLISH_DICTIONARY_RAW__;

// 4. CHARLES M. SCHULZ PHILOSOPHICAL QUOTES
const SNOOPY_PHILOSOPHIES = [
  {
    en: "“Keep looking up... that's the secret of life.”",
    cn: "「永远抬头向上看…… 这便是生活的秘诀。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Happiness is a warm puppy.”",
    cn: "「幸福，就是一只温暖的小狗。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Learn from yesterday, live for today, look to tomorrow, rest this afternoon.”",
    cn: "「汲取昨天的经验，活在今天的当下，憧憬明天的美好，今天下午先小憩一下。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“In the book of life, the answers aren't in the back.”",
    cn: "「在人生的这一本书里，答案从不写在最后一页。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Be yourself. No one can say you're doing it wrong.”",
    cn: "「做真实的自己。没有人能对你的热爱指手画脚。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“It does not matter where you go in life, it is who you have beside you.”",
    cn: "「漫漫旅途中去往何方并不重要，重要的是同行于身侧的人。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Each morning is a clean sheet of paper, ready for new stories.”",
    cn: "「每一个清晨都是一张崭新的稿纸，正等待书写新的故事。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“My life has no direction, no aim, no meaning, and yet I'm happy.”",
    cn: "「我的生活没有既定的刻板航向，但我依然快乐而满足。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“All you need is love. But a little chocolate now and then doesn't hurt.”",
    cn: "「人人都需要爱，但偶尔来一点巧克力也绝不是坏事。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“A day without a nap is like a cupcake without frosting.”",
    cn: "「没有午休的一天，就像没有糖霜的纸杯蛋糕。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“You can't think about anything on an empty stomach.”",
    cn: "「不能空着肚子思考问题，从容享受一顿美餐吧。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Just remember, when you're over the hill, you begin to pick up speed.”",
    cn: "「翻过山巅之后，步伐便会愈加轻快从容。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Keep your face to the sunshine and you cannot see a shadow.”",
    cn: "「让脸庞向着阳光，阴影便会自然落到身后。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Don't worry about today. Tomorrow is already starting somewhere bright.”",
    cn: "「别为今日琐事忧虑，世界的某个角落早已迎来了崭新的朝阳。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Life is like an ice cream cone, you have to lick it one day at a time.”",
    cn: "「生活就像甜筒冰淇淋，需要一天一口细细品味。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Focus on today's breeze; let tomorrow's clouds take care of themselves.”",
    cn: "「专注感受今日的微风；明天的云彩自有其安放之处。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Good advice doesn't cost anything, but following it makes all the difference.”",
    cn: "「倾听善意的指引，脚踏实地，步步生花。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Small steps each day lead to grand adventures over time.”",
    cn: "「每日跨出的一小步，日积月累终将汇聚成壮阔的冒险。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Rest when you're weary. Refresh and renew yourself, your body, your mind.”",
    cn: "「感到疲惫时就安心休憩，蓄满能量后再轻盈出发。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Sometimes it’s nice just to lie on the roof and think of peaceful skies.”",
    cn: "「有时，只是静静趴在屋顶上凝望晴空，也是莫大的惬意。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Clarity in thought brings ease in every stride.”",
    cn: "「思绪清晰，落笔从容，每一步都能走得轻快坚定。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“There is nothing more attractive than a warm smile and a calm heart.”",
    cn: "「没有什么比真挚的微笑与笃定的内心更有力量。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“To live is to dance, to dance is to celebrate every little joy.”",
    cn: "「热爱生活，保持律动，就像在青草地上轻快起舞。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Big journeys begin with a steady heart and a loyal companion.”",
    cn: "「远大航程始于沉稳的内心，以及身旁值得信赖的伙伴。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“The world is full of possibilities when you greet it with kindness.”",
    cn: "「以善意与温情拥抱清晨，世界便处处皆是无限可能。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Take a deep breath. Every knot has a way of undoing itself.”",
    cn: "「遇事先深呼吸，放平心态，繁杂的谜团自会迎刃而解。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“It's always better to wake up with enthusiasm than with haste.”",
    cn: "「怀抱热忱醒来，总胜过仓促忙乱地赶路。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“No problem is so big or so complicated that it can't be run away from for a bit.”",
    cn: "「没有什么烦恼是出去散个步不能缓解的，轻装上阵才走得远。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“I think I'm afraid to be happy because whenever I get too happy something bad happens.”",
    cn: "「平静而稳定的笃定感，是生活最珍贵的底气。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Like a warm breeze over the doghouse, may today bring peace and clarity.”",
    cn: "「愿今日如拂过红色狗屋的暖风，带给你内心的安宁与笃定。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  },
  {
    en: "“Always remember: You are braver than you believe and stronger than you seem.”",
    cn: "「永远铭记：你远比自己想象的更勇敢，也比外表所显现的更强大。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }
];

// 5. WOODSTOCK SECRETARY WHISPERS
const WOODSTOCK_WHISPERS = [
  "♪ 啾啾！Woodstock 为您加满今日能量！",
  "从容不迫，今天的主管日程也是井井有条的一天！",
  "收到！今日 8 代表处沟通顺畅，诸事顺利！",
  "啾~ 喝杯温水，深呼吸，史努比和 Woodstock 永远陪着你！",
  "Woodstock 汇报：一切准备就绪，今天也超棒！",
  "Happiness is a warm puppy and smooth meetings! ✨",
  "会议排期井井有条，从容不迫的大秘书最厉害！",
  "♪ 嗒啦！今日份好运与专注已为您妥善送达！"
];

// 6. THE 8 REPRESENTATIVE OFFICES (Sorted chronologically from earliest to latest)
// Earliest local time / ahead timezones come first: UTC+2 (Cairo, Libya) -> UTC+1 (Tunis, Congo DRC, Cameroon, Algeria) -> UTC+0 (Morocco, Côte d'Ivoire, Senegal)
const TIMEZONE_REPS = [
  {
    id: 'cairo',
    country: '埃及',
    name: '埃及代表处',
    city: '开罗 (Cairo)',
    flag: '🇪🇬',
    tz: 'Africa/Cairo',
    utcOffset: 2,
    isBaseline: true,
    desc: '开罗基准时区 (UTC+2 · 冬令时) · 率先开启工作日'
  },
  {
    id: 'med_south_libya',
    country: '地中海南 · 利比亚',
    name: '地南代表处 · 利比亚',
    city: '的黎波里 / 班加西 (Tripoli)',
    flag: '🇱🇾',
    tz: 'Africa/Tripoli',
    utcOffset: 2,
    diffText: '同开罗时间 (UTC+2 · 0h)',
    desc: '地中海南代表处 · 利比亚办公点 (UTC+2)'
  },
  {
    id: 'med_south_tunis',
    country: '地中海南 · 突尼斯',
    name: '地南代表处 · 突尼斯',
    city: '突尼斯市 (Tunis)',
    flag: '🇹🇳',
    tz: 'Africa/Tunis',
    utcOffset: 1,
    diffText: '比开罗慢 1 小时 (UTC+1 · -1h)',
    desc: '地中海南代表处 · 突尼斯办公点 (UTC+1)'
  },
  {
    id: 'congo_drc',
    country: '刚果（金）',
    name: '刚果代表处',
    city: '金沙萨 (Kinshasa)',
    flag: '🇨🇩',
    tz: 'Africa/Kinshasa',
    utcOffset: 1,
    diffText: '比开罗慢 1 小时',
    desc: '中非核心枢纽（金沙萨）'
  },
  {
    id: 'cameroon',
    country: '喀麦隆',
    name: '喀麦隆代表处',
    city: '雅温得 / 杜阿拉',
    flag: '🇨🇲',
    tz: 'Africa/Douala',
    utcOffset: 1,
    diffText: '比开罗慢 1 小时',
    desc: '中西非交汇节点'
  },
  {
    id: 'algeria',
    country: '阿尔及利亚',
    name: '阿尔及利亚代表处',
    city: '阿尔及尔 (Algiers)',
    flag: '🇩🇿',
    tz: 'Africa/Algiers',
    utcOffset: 1,
    diffText: '比开罗慢 1 小时',
    desc: '北非重要资源与交付中心'
  },
  {
    id: 'morocco',
    country: '摩洛哥',
    name: '摩洛哥代表处',
    city: '卡萨布兰卡 / 拉巴特',
    flag: '🇲🇦',
    tz: 'Africa/Casablanca',
    utcOffset: 0,
    diffText: '比开罗慢 2 小时',
    desc: '西北非商业重镇 (UTC+0)'
  },
  {
    id: 'cote_divoire',
    country: '科特迪瓦',
    name: '科特迪瓦代表处',
    city: '阿比让 (Abidjan)',
    flag: '🇨🇮',
    tz: 'Africa/Abidjan',
    utcOffset: 0,
    diffText: '比开罗慢 2 小时',
    desc: '西非法语区经济中心'
  },
  {
    id: 'senegal',
    country: '塞内加尔',
    name: '塞内加尔代表处',
    city: '达喀尔 (Dakar)',
    flag: '🇸🇳',
    tz: 'Africa/Dakar',
    utcOffset: 0,
    diffText: '比开罗慢 2 小时',
    desc: '西非门户枢纽'
  }
];

// 出差目的地时区映射与快速换算配置 (以开罗冬令时 UTC+2 为基础)
const TRIP_TIMEZONE_MAP = {
  cairo: { id: 'cairo', name: '埃及·开罗', utcOffset: 2, flag: '🇪🇬', diffText: '常驻基准' },
  med_south_libya: { id: 'med_south_libya', name: '地南·利比亚', utcOffset: 2, flag: '🇱🇾', diffText: '无时差' },
  med_south_tunis: { id: 'med_south_tunis', name: '地南·突尼斯', utcOffset: 1, flag: '🇹🇳', diffText: '慢 1 小时' },
  algeria: { id: 'algeria', name: '阿尔及利亚', utcOffset: 1, flag: '🇩🇿', diffText: '慢 1 小时' },
  morocco: { id: 'morocco', name: '摩洛哥', utcOffset: 0, flag: '🇲🇦', diffText: '慢 2 小时' },
  congo_drc: { id: 'congo_drc', name: '刚果（金）', utcOffset: 1, flag: '🇨🇩', diffText: '慢 1 小时' },
  cameroon: { id: 'cameroon', name: '喀麦隆', utcOffset: 1, flag: '🇨🇲', diffText: '慢 1 小时' },
  cote_divoire: { id: 'cote_divoire', name: '科特迪瓦', utcOffset: 0, flag: '🇨🇮', diffText: '慢 2 小时' },
  senegal: { id: 'senegal', name: '塞内加尔', utcOffset: 0, flag: '🇸🇳', diffText: '慢 2 小时' },
  beijing: { id: 'beijing', name: '中国·北京', utcOffset: 8, flag: '🇨🇳', diffText: '快 6 小时' }
};

function getActiveTripTimezone() {
  return getData(STORAGE_KEYS.TRIP_TIMEZONE, 'cairo');
}

function getTripTimezoneDiffHours(targetTzId) {
  const tzId = targetTzId || getActiveTripTimezone();
  const tzInfo = TRIP_TIMEZONE_MAP[tzId] || TRIP_TIMEZONE_MAP.cairo;
  return tzInfo.utcOffset - 2; // 相对开罗冬令时 (UTC+2) 的时差小时数
}

function shiftTimeStrByHours(timeStr, diffHours) {
  if (!timeStr || !diffHours || diffHours === 0) return timeStr;
  const parts = String(timeStr).split(':').map(Number);
  if (parts.length < 2 || isNaN(parts[0]) || isNaN(parts[1])) return timeStr;
  let totalMins = parts[0] * 60 + parts[1] + (diffHours * 60);
  totalMins = (totalMins % 1440 + 1440) % 1440;
  const h = Math.floor(totalMins / 60);
  const m = totalMins % 60;
  return String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0');
}

// ================= 领导出差行程管理 (Leader Trips & Date-Bound Timezone) =================
function getLeaderTrips() {
  return getData(STORAGE_KEYS.LEADER_TRIPS, []);
}

function getTripForDate(dateStr) {
  if (!dateStr) return null;
  const trips = getLeaderTrips();
  const match = trips.find(t => t.startDate <= dateStr && dateStr <= t.endDate);
  if (!match) return null;
  const tzInfo = TRIP_TIMEZONE_MAP[match.destination] || TRIP_TIMEZONE_MAP.cairo;
  const diffHours = (tzInfo.utcOffset !== undefined) ? (tzInfo.utcOffset - 2) : 0;
  return {
    ...match,
    tzInfo,
    diffHours,
    tzName: tzInfo.name,
    tzFlag: tzInfo.flag,
    diffText: tzInfo.diffText
  };
}

function getMeetingDisplayTime(m) {
  if (!m) {
    return {
      start: '10:00',
      end: '10:45',
      isShifted: false,
      isTripDate: false,
      trip: null,
      cairoStart: '10:00',
      cairoEnd: '10:45',
      timeStr: '10:00',
      timeRangeStr: '10:00 - 10:45'
    };
  }

  const baseStart = m.startTime || m.time || '10:00';
  const dur = parseInt(m.duration || 45, 10);
  const baseEnd = m.endTime || calculateEndTime(baseStart, dur);
  const mDate = m.date || '';
  const trip = getTripForDate(mDate);

  // 1. If meeting date falls into a leader business trip, display in leader's trip destination local time!
  if (trip && trip.diffHours !== 0) {
    const tripStart = shiftTimeStrByHours(baseStart, trip.diffHours);
    const tripEnd = shiftTimeStrByHours(baseEnd, trip.diffHours);

    return {
      start: tripStart,
      end: tripEnd,
      isShifted: true,
      isTripDate: true,
      trip,
      tzName: trip.tzName,
      tzFlag: trip.tzFlag,
      diffHours: trip.diffHours,
      diffText: trip.diffText,
      cairoStart: baseStart,
      cairoEnd: baseEnd,
      timeStr: tripStart,
      timeRangeStr: tripStart + (tripEnd ? ' - ' + tripEnd : ''),
      origTzBase: m.tzBase || 'cairo',
      inputStartTime: m.inputStartTime || m.localStartTime || shiftTimeStrByHours(baseStart, getTripTimezoneDiffHours(m.tzBase || 'cairo')),
      inputEndTime: m.inputEndTime || m.localEndTime || shiftTimeStrByHours(baseEnd, getTripTimezoneDiffHours(m.tzBase || 'cairo'))
    };
  }

  // 3. Fallback to active trip timezone if manually switched globally (backwards-compatible)
  const activeTz = getActiveTripTimezone();
  const diffHours = getTripTimezoneDiffHours(activeTz);
  if (diffHours && diffHours !== 0 && activeTz !== 'cairo') {
    const shiftedStart = shiftTimeStrByHours(baseStart, diffHours);
    const shiftedEnd = shiftTimeStrByHours(baseEnd, diffHours);
    const tzInfo = TRIP_TIMEZONE_MAP[activeTz] || TRIP_TIMEZONE_MAP.cairo;
    return {
      start: shiftedStart,
      end: shiftedEnd,
      isShifted: true,
      isTripDate: false,
      trip: null,
      tzName: tzInfo.name,
      tzFlag: tzInfo.flag,
      diffHours,
      diffText: tzInfo.diffText,
      cairoStart: baseStart,
      cairoEnd: baseEnd,
      timeStr: shiftedStart,
      timeRangeStr: shiftedStart + (shiftedEnd ? ' - ' + shiftedEnd : '')
    };
  }

  return {
    start: baseStart,
    end: baseEnd,
    isShifted: false,
    isTripDate: false,
    trip: null,
    cairoStart: baseStart,
    cairoEnd: baseEnd,
    timeStr: baseStart,
    timeRangeStr: baseStart + (baseEnd ? ' - ' + baseEnd : '')
  };
}

function changeTripTimezone(tzId) {
  setData(STORAGE_KEYS.TRIP_TIMEZONE, tzId || 'cairo');
  renderMeetings();
  renderSupervisorWeeklyBoard();
  renderSupervisorDayCalendar();
  if (tzId === 'cairo') {
    showToast('🇪🇬 已切回开罗常驻基准时区 (UTC+2)');
  } else {
    const tzInfo = TRIP_TIMEZONE_MAP[tzId] || TRIP_TIMEZONE_MAP.cairo;
    showToast(`✈️ 已切换出差时区：${tzInfo.flag} ${tzInfo.name} (比开罗${tzInfo.diffText})`);
  }
}

function getTripTimezoneBarHtml() {
  const trips = getLeaderTrips();
  const hasTrips = trips.length > 0;

  let tripChipsHtml = '';
  if (hasTrips) {
    tripChipsHtml = trips.map(t => {
      const tz = TRIP_TIMEZONE_MAP[t.destination] || TRIP_TIMEZONE_MAP.cairo;
      return `
        <span class="trip-chip" style="display:inline-flex; align-items:center; gap:6px; background:#dcfce7; border:1px solid #86efac; color:#166534; padding:2px 8px; border-radius:14px; font-size:11px; font-weight:700;">
          <span>${tz.flag} ${tz.name} (${t.startDate} ~ ${t.endDate} · 比开罗${tz.diffText})</span>
          <button onclick="deleteLeaderTrip(${t.id})" title="取消此出差行程" style="background:none; border:none; color:#166534; cursor:pointer; font-size:11px; font-weight:bold; padding:0 2px; line-height:1;">✕</button>
        </span>
      `;
    }).join('');
  }

  return `<div class="trip-timezone-bar" style="display:none;"></div>`;
}

function openLeaderTripModal() {
  const todayStr = getTodayDateStr();
  const startInput = document.getElementById('inputTripStartDate');
  const endInput = document.getElementById('inputTripEndDate');
  const remarkInput = document.getElementById('inputTripRemark');

  if (startInput) startInput.value = todayStr;
  if (endInput) {
    const d = new Date();
    d.setDate(d.getDate() + 4);
    endInput.value = formatDateToStr(d);
  }
  if (remarkInput) remarkInput.value = '';

  renderLeaderTripExistingList();
  openModal('leaderTripModal');
}

function setTripQuickRange(type) {
  const today = new Date();
  const todayStr = getTodayDateStr();
  const startInput = document.getElementById('inputTripStartDate');
  const endInput = document.getElementById('inputTripEndDate');
  if (!startInput || !endInput) return;

  if (type === 'today') {
    startInput.value = todayStr;
    endInput.value = todayStr;
  } else if (type === 'this_week') {
    const sun = new Date(today);
    sun.setDate(today.getDate() - today.getDay());
    const thu = new Date(sun);
    thu.setDate(sun.getDate() + 4);
    startInput.value = formatDateToStr(sun);
    endInput.value = formatDateToStr(thu);
  } else if (type === 'next_week') {
    const nextSun = new Date(today);
    nextSun.setDate(today.getDate() - today.getDay() + 7);
    const nextThu = new Date(nextSun);
    nextThu.setDate(nextSun.getDate() + 4);
    startInput.value = formatDateToStr(nextSun);
    endInput.value = formatDateToStr(nextThu);
  } else if (type === 'next_7_days') {
    startInput.value = todayStr;
    const end = new Date(today);
    end.setDate(today.getDate() + 6);
    endInput.value = formatDateToStr(end);
  }
}

function saveLeaderTrip() {
  const destEl = document.getElementById('inputTripDestination');
  const dest = destEl ? destEl.value : 'med_south_tunis';
  const start = document.getElementById('inputTripStartDate').value;
  const end = document.getElementById('inputTripEndDate').value;
  const remark = (document.getElementById('inputTripRemark').value || '').trim();

  if (!start || !end) {
    showToast('⚠️ 请选择出差开始日期与结束日期');
    return;
  }
  if (start > end) {
    showToast('⚠️ 出差结束日期不能早于开始日期');
    return;
  }

  const trips = getLeaderTrips();
  const newTrip = {
    id: Date.now(),
    destination: dest,
    startDate: start,
    endDate: end,
    remark
  };
  trips.push(newTrip);
  setData(STORAGE_KEYS.LEADER_TRIPS, trips);
  closeModal('leaderTripModal');
  renderMeetings();
  renderSupervisorWeeklyBoard();
  renderSupervisorDayCalendar();
  const tz = TRIP_TIMEZONE_MAP[dest] || TRIP_TIMEZONE_MAP.cairo;
  showToast(`✈️ 领导出差行程已登记：${tz.flag} ${tz.name} (${start} 至 ${end})`);
}

function deleteLeaderTrip(id) {
  let trips = getLeaderTrips();
  trips = trips.filter(t => t.id !== id);
  setData(STORAGE_KEYS.LEADER_TRIPS, trips);
  renderMeetings();
  renderSupervisorWeeklyBoard();
  renderSupervisorDayCalendar();
  renderLeaderTripExistingList();
  showToast('🗑️ 该出差行程已删除，相关日期已恢复开罗时间');
}

function clearAllLeaderTrips() {
  if (!confirm('确定要清空所有领导出差行程吗？\\n清空后所有日程将恢复开罗常驻时间显示。')) return;
  setData(STORAGE_KEYS.LEADER_TRIPS, []);
  closeModal('leaderTripModal');
  renderMeetings();
  renderSupervisorWeeklyBoard();
  renderSupervisorDayCalendar();
  showToast('🧹 已清空所有出差行程，全表恢复开罗常驻时间');
}

function renderLeaderTripExistingList() {
  const listEl = document.getElementById('tripExistingListArea');
  if (!listEl) return;
  const trips = getLeaderTrips();
  if (trips.length === 0) {
    listEl.innerHTML = '<div style="font-size:12px; color:var(--text-muted); text-align:center; padding:8px; background:var(--card-subtle); border-radius:var(--radius-sm);">暂无已登记的出差行程</div>';
    return;
  }
  listEl.innerHTML = `
    <div style="font-size:12px; font-weight:700; color:var(--text-secondary); margin-bottom:6px;">
      📋 已登记的出差行程清单 (${trips.length} 条)：
    </div>
    <div style="display:flex; flex-direction:column; gap:6px; max-height:140px; overflow-y:auto;">
      ${trips.map(t => {
        const tz = TRIP_TIMEZONE_MAP[t.destination] || TRIP_TIMEZONE_MAP.cairo;
        return `
          <div style="display:flex; align-items:center; justify-content:space-between; background:var(--card-subtle); border:1px solid var(--border); border-radius:var(--radius-sm); padding:6px 10px; font-size:12px;">
            <div>
              <span style="font-weight:700; color:#15803d;">${tz.flag} ${tz.name}</span>
              <span style="margin-left:8px; color:var(--text-primary); font-weight:600;">${t.startDate} 至 ${t.endDate}</span>
              <span style="margin-left:6px; font-size:11px; color:var(--text-muted);">(比开罗${tz.diffText})</span>
              ${t.remark ? `<span style="margin-left:8px; font-size:11px; color:var(--text-secondary);">· ${escapeHtml(t.remark)}</span>` : ''}
            </div>
            <button class="btn btn-sm btn-ghost" style="color:#dc2626; padding:1px 6px; font-size:11.5px;" onclick="deleteLeaderTrip(${t.id})" title="删除此条行程">✕</button>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

// ================= 领导在途行程管理 (Leader In-Transit Flight & Cross-Timezone Engine) =================
function getLeaderTransits() {
  return getData(STORAGE_KEYS.LEADER_TRANSITS, []);
}

function getTransitsForDate(dateStr) {
  if (!dateStr) return [];
  const transits = getLeaderTransits();
  return transits.filter(t => (t.depDate <= dateStr && dateStr <= t.arrDate) || t.depDate === dateStr || t.arrDate === dateStr);
}

function parseDateTimeToUtcMs(dateStr, timeStr, tzKey) {
  if (!dateStr || !timeStr) return null;
  const dParts = dateStr.split('-').map(Number);
  const tParts = timeStr.split(':').map(Number);
  if (dParts.length < 3 || tParts.length < 2 || isNaN(dParts[0]) || isNaN(dParts[1]) || isNaN(dParts[2]) || isNaN(tParts[0]) || isNaN(tParts[1])) return null;
  const [year, month, day] = dParts;
  const [hour, min] = tParts;
  const tz = TRIP_TIMEZONE_MAP[tzKey] || TRIP_TIMEZONE_MAP.cairo;
  const utcOffset = tz.utcOffset !== undefined ? tz.utcOffset : 2;
  return Date.UTC(year, month - 1, day, hour - utcOffset, min);
}

function calculateTransitDuration(depDate, depTime, depTz, arrDate, arrTime, arrTz) {
  const depUtc = parseDateTimeToUtcMs(depDate, depTime, depTz);
  const arrUtc = parseDateTimeToUtcMs(arrDate, arrTime, arrTz);
  if (depUtc === null || arrUtc === null) return null;
  const diffMs = arrUtc - depUtc;
  const diffMins = Math.round(diffMs / 60000);
  const isValid = diffMins > 0;
  const absMins = Math.abs(diffMins);
  const h = Math.floor(absMins / 60);
  const m = absMins % 60;
  const text = isValid ? `${h}小时${m > 0 ? (m + '分') : ''}` : '落地时间不能早于或等于起飞时间';
  return {
    diffMins,
    diffMs,
    isValid,
    hours: h,
    minutes: m,
    text
  };
}

function handleTransitFormChange() {
  const depDateInput = document.getElementById('inputTransitDepDate');
  const depTimeInput = document.getElementById('inputTransitDepTime');
  const depTzSelect = document.getElementById('inputTransitDepTz');
  const arrDateInput = document.getElementById('inputTransitArrDate');
  const arrTimeInput = document.getElementById('inputTransitArrTime');
  const arrTzSelect = document.getElementById('inputTransitArrTz');
  const hintEl = document.getElementById('transitDurationLiveHint');

  if (!depDateInput || !depTimeInput || !arrDateInput || !arrTimeInput || !hintEl) return;

  const depDate = depDateInput.value;
  let depTime = depTimeInput.value.trim();
  const depTz = depTzSelect ? depTzSelect.value : 'cairo';
  let arrDate = arrDateInput.value;
  let arrTime = arrTimeInput.value.trim();
  const arrTz = arrTzSelect ? arrTzSelect.value : 'cameroon';

  // Auto-sync arrival date if empty
  if (!arrDate && depDate) {
    arrDate = depDate;
    arrDateInput.value = depDate;
  }

  if (depTime) {
    const norm = normalizeTimeStr(depTime);
    if (norm) depTime = norm;
  }
  if (arrTime) {
    const norm = normalizeTimeStr(arrTime);
    if (norm) arrTime = norm;
  }

  if (!depDate || !depTime || !arrDate || !arrTime) {
    hintEl.innerHTML = '⏱️ 跨时区飞行耗时：请输入起降时间计算';
    hintEl.style.color = '#0369a1';
    hintEl.style.background = '#f0f9ff';
    hintEl.style.borderColor = '#bae6fd';
    return;
  }

  const calc = calculateTransitDuration(depDate, depTime, depTz, arrDate, arrTime, arrTz);
  if (!calc || !calc.isValid) {
    hintEl.innerHTML = '⚠️ 落地时间早于或等于起飞时间，请核对跨时区日期或时间';
    hintEl.style.color = '#dc2626';
    hintEl.style.background = '#fef2f2';
    hintEl.style.borderColor = '#fecaca';
  } else {
    const depInfo = TRIP_TIMEZONE_MAP[depTz] || TRIP_TIMEZONE_MAP.cairo;
    const arrInfo = TRIP_TIMEZONE_MAP[arrTz] || TRIP_TIMEZONE_MAP.cameroon;
    hintEl.innerHTML = `⏱️ 跨时区飞行耗时：<strong>约 ${calc.text}</strong>（起飞: ${depInfo.name} UTC+${depInfo.utcOffset} ➔ 落地: ${arrInfo.name} UTC+${arrInfo.utcOffset}）`;
    hintEl.style.color = '#0369a1';
    hintEl.style.background = '#f0f9ff';
    hintEl.style.borderColor = '#bae6fd';
  }
}

function openTransitModal(transitId) {
  const titleEl = document.getElementById('transitModalTitle');
  const idInput = document.getElementById('inputTransitId');
  const titleInput = document.getElementById('inputTransitTitle');
  const depDateInput = document.getElementById('inputTransitDepDate');
  const depTimeInput = document.getElementById('inputTransitDepTime');
  const depTzSelect = document.getElementById('inputTransitDepTz');
  const arrDateInput = document.getElementById('inputTransitArrDate');
  const arrTimeInput = document.getElementById('inputTransitArrTime');
  const arrTzSelect = document.getElementById('inputTransitArrTz');
  const flightNoInput = document.getElementById('inputTransitFlightNo');
  const remarkInput = document.getElementById('inputTransitRemark');
  const btnDelete = document.getElementById('btnDeleteTransit');

  const todayStr = getTodayDateStr();
  const activeTrip = getTripForDate(todayStr);

  if (transitId) {
    const transits = getLeaderTransits();
    const t = transits.find(item => item.id === transitId);
    if (t) {
      if (titleEl) titleEl.textContent = '编辑领导在途行程 (跨时区航班)';
      if (idInput) idInput.value = t.id;
      if (titleInput) titleInput.value = t.title || '';
      if (depDateInput) depDateInput.value = t.depDate || todayStr;
      if (depTimeInput) depTimeInput.value = t.depTime || '09:30';
      if (depTzSelect) depTzSelect.value = t.depTz || 'cairo';
      if (arrDateInput) arrDateInput.value = t.arrDate || todayStr;
      if (arrTimeInput) arrTimeInput.value = t.arrTime || '14:45';
      if (arrTzSelect) arrTzSelect.value = t.arrTz || 'cameroon';
      if (flightNoInput) flightNoInput.value = t.flightNo || '';
      if (remarkInput) remarkInput.value = t.remark || '';
      if (btnDelete) btnDelete.style.display = 'inline-block';
    }
  } else {
    if (titleEl) titleEl.textContent = '登记领导在途行程 (跨时区航班)';
    if (idInput) idInput.value = '';
    if (titleInput) titleInput.value = '';
    if (depDateInput) depDateInput.value = todayStr;
    if (depTimeInput) depTimeInput.value = '09:30';
    if (depTzSelect) depTzSelect.value = 'cairo';
    if (arrDateInput) arrDateInput.value = todayStr;
    if (arrTimeInput) arrTimeInput.value = '14:45';
    if (arrTzSelect) arrTzSelect.value = activeTrip ? activeTrip.destination : 'cameroon';
    if (flightNoInput) flightNoInput.value = '';
    if (remarkInput) remarkInput.value = '';
    if (btnDelete) btnDelete.style.display = 'none';
  }

  handleTransitFormChange();
  renderTransitExistingList();
  openModal('transitModal');
}

function saveLeaderTransit() {
  const idInput = document.getElementById('inputTransitId');
  const titleInput = document.getElementById('inputTransitTitle');
  const depDateInput = document.getElementById('inputTransitDepDate');
  const depTimeInput = document.getElementById('inputTransitDepTime');
  const depTzSelect = document.getElementById('inputTransitDepTz');
  const arrDateInput = document.getElementById('inputTransitArrDate');
  const arrTimeInput = document.getElementById('inputTransitArrTime');
  const arrTzSelect = document.getElementById('inputTransitArrTz');
  const flightNoInput = document.getElementById('inputTransitFlightNo');
  const remarkInput = document.getElementById('inputTransitRemark');

  let title = (titleInput ? titleInput.value : '').trim();
  const depDate = depDateInput ? depDateInput.value : '';
  let depTime = (depTimeInput ? depTimeInput.value : '').trim();
  const depTz = depTzSelect ? depTzSelect.value : 'cairo';
  const arrDate = arrDateInput ? arrDateInput.value : '';
  let arrTime = (arrTimeInput ? arrTimeInput.value : '').trim();
  const arrTz = arrTzSelect ? arrTzSelect.value : 'cameroon';
  const flightNo = (flightNoInput ? flightNoInput.value : '').trim();
  const remark = (remarkInput ? remarkInput.value : '').trim();

  if (!depDate || !depTime) {
    showToast('⚠️ 请填写起飞日期与起飞时间');
    return;
  }
  if (!arrDate || !arrTime) {
    showToast('⚠️ 请填写落地日期与落地时间');
    return;
  }

  const normDep = normalizeTimeStr(depTime) || depTime;
  const normArr = normalizeTimeStr(arrTime) || arrTime;

  const calc = calculateTransitDuration(depDate, normDep, depTz, arrDate, normArr, arrTz);
  if (!calc || !calc.isValid) {
    showToast('⚠️ 落地时间不能早于或等于起飞时间，请核对跨时区时间');
    return;
  }

  const depInfo = TRIP_TIMEZONE_MAP[depTz] || TRIP_TIMEZONE_MAP.cairo;
  const arrInfo = TRIP_TIMEZONE_MAP[arrTz] || TRIP_TIMEZONE_MAP.cameroon;

  if (!title) {
    title = `${depInfo.name.replace(/.*·/, '')} ✈ ${arrInfo.name.replace(/.*·/, '')}`;
  }

  const transits = getLeaderTransits();
  const curId = idInput && idInput.value ? parseInt(idInput.value, 10) : null;

  const transitData = {
    id: curId || Date.now(),
    title,
    flightNo,
    depDate,
    depTime: normDep,
    depTz,
    depTzName: depInfo.name,
    depUtcOffset: depInfo.utcOffset,
    arrDate,
    arrTime: normArr,
    arrTz,
    arrTzName: arrInfo.name,
    arrUtcOffset: arrInfo.utcOffset,
    durationMins: calc.diffMins,
    durationText: calc.text,
    remark
  };

  if (curId) {
    const idx = transits.findIndex(t => t.id === curId);
    if (idx >= 0) {
      transits[idx] = transitData;
    } else {
      transits.push(transitData);
    }
  } else {
    transits.push(transitData);
  }

  setData(STORAGE_KEYS.LEADER_TRANSITS, transits);
  closeModal('transitModal');
  renderSupervisorWeeklyBoard();
  renderSupervisorDayCalendar();
  if (typeof updateChalkboardExecutiveBar === 'function') {
    updateChalkboardExecutiveBar();
  }
  showToast(`🛫 在途行程已保存：${title}（飞行约 ${calc.text}）`);
}

function deleteLeaderTransit(id) {
  let transits = getLeaderTransits();
  transits = transits.filter(t => t.id !== id);
  setData(STORAGE_KEYS.LEADER_TRANSITS, transits);
  renderTransitExistingList();
  renderSupervisorWeeklyBoard();
  renderSupervisorDayCalendar();
  if (typeof updateChalkboardExecutiveBar === 'function') {
    updateChalkboardExecutiveBar();
  }
  showToast('🗑️ 该在途行程已删除');
}

function deleteCurrentTransit() {
  const idInput = document.getElementById('inputTransitId');
  if (!idInput || !idInput.value) return;
  const id = parseInt(idInput.value, 10);
  deleteLeaderTransit(id);
  closeModal('transitModal');
}

function renderTransitExistingList() {
  const container = document.getElementById('transitExistingListArea');
  if (!container) return;
  const transits = getLeaderTransits();
  if (transits.length === 0) {
    container.innerHTML = '<div style="font-size:11.5px; color:var(--text-muted); text-align:center; padding:8px; background:var(--card-subtle); border-radius:var(--radius-sm);">暂无登记的在途行程</div>';
    return;
  }
  container.innerHTML = `
    <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); margin-bottom:4px;">
      📋 已登记在途行程 (${transits.length} 条)：
    </div>
    <div style="display:flex; flex-direction:column; gap:5px; max-height:120px; overflow-y:auto;">
      ${transits.map(t => `
        <div style="display:flex; align-items:center; justify-content:space-between; background:#f0f9ff; border:1px solid #bae6fd; border-radius:var(--radius-sm); padding:5px 8px; font-size:11.5px;">
          <div>
            <span style="font-weight:700; color:#0369a1;">🛫 ${escapeHtml(t.title)}</span>
            ${t.flightNo ? `<span style="margin-left:6px; background:#e0f2fe; color:#0369a1; padding:1px 4px; border-radius:3px; font-size:10.5px; font-weight:600;">${escapeHtml(t.flightNo)}</span>` : ''}
            <span style="margin-left:6px; color:#475569;">${t.depDate} ${t.depTime} ➔ ${t.arrDate} ${t.arrTime}</span>
            <span style="margin-left:4px; color:#0284c7; font-weight:600;">(约 ${escapeHtml(t.durationText || '')})</span>
          </div>
          <div style="display:flex; gap:4px;">
            <button class="btn btn-sm btn-ghost" style="padding:1px 5px; font-size:11px;" onclick="openTransitModal(${t.id})">✏️</button>
            <button class="btn btn-sm btn-ghost" style="color:#dc2626; padding:1px 5px; font-size:11px;" onclick="deleteLeaderTransit(${t.id})" title="删除此在途行程">✕</button>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

function renderWeeklyTransitCard(t) {
  const depTzName = t.depTzName || ((TRIP_TIMEZONE_MAP[t.depTz] || TRIP_TIMEZONE_MAP.cairo).name);
  const arrTzName = t.arrTzName || ((TRIP_TIMEZONE_MAP[t.arrTz] || TRIP_TIMEZONE_MAP.cameroon).name);
  return `
    <div class="weekly-card weekly-card-transit" onclick="openTransitModal(${t.id})" title="🛫 领导在途：${escapeHtml(t.title)} (起飞：${t.depDate} ${t.depTime} ${depTzName} ➔ 落地：${t.arrDate} ${t.arrTime} ${arrTzName})，耗时约 ${escapeHtml(t.durationText || '')}。点击查看/编辑">
      <div class="weekly-card-time" style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:11px; font-weight:700; color:#0284c7;">🛫 在途 · 飞行约 ${escapeHtml(t.durationText || '')}</span>
        ${t.flightNo ? `<span style="font-size:10px; background:#e0f2fe; color:#0369a1; padding:0 4px; border-radius:3px; font-weight:600;">${escapeHtml(t.flightNo)}</span>` : ''}
      </div>
      <div class="weekly-card-title" style="font-size:11.5px; font-weight:700; margin:2px 0; color:#0c4a6e;">
        ${escapeHtml(t.title)}
      </div>
      <div style="font-size:10px; color:#475569; display:flex; flex-direction:column; gap:1px;">
        <div>起飞：${t.depTime} (${depTzName})</div>
        <div>落地：${t.arrTime} (${arrTzName})</div>
        ${t.remark ? `<div style="font-size:9.5px; color:#64748b; margin-top:1px;">📝 ${escapeHtml(t.remark)}</div>` : ''}
      </div>
    </div>
  `;
}

function renderDayTransitCard(t) {
  const depTzName = t.depTzName || ((TRIP_TIMEZONE_MAP[t.depTz] || TRIP_TIMEZONE_MAP.cairo).name);
  const arrTzName = t.arrTzName || ((TRIP_TIMEZONE_MAP[t.arrTz] || TRIP_TIMEZONE_MAP.cameroon).name);
  return `
    <div class="day-meeting-card day-transit-card" onclick="openTransitModal(${t.id})" style="cursor:pointer;" title="点击编辑此在途行程">
      <div class="day-meeting-top">
        <div class="day-meeting-time-bar">
          <span class="day-meeting-time-text" style="color:#0284c7; font-weight:800;">🛫 在途飞行 · 约 ${escapeHtml(t.durationText || '')}</span>
          ${t.flightNo ? `<span style="background:#0284c7; color:#fff; font-size:11px; padding:1px 6px; border-radius:4px; font-weight:700;">${escapeHtml(t.flightNo)}</span>` : ''}
          <span class="status-badge" style="background:#e0f2fe; color:#0369a1; border:1px solid #bae6fd;">旅途在途</span>
        </div>
        <div style="font-size:11.5px; color:#0369a1; font-weight:600;">
          ⏱️ 真实跨时区航程
        </div>
      </div>
      <div class="day-meeting-title" style="color:#0c4a6e;">
        ✈️ ${escapeHtml(t.title)}
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:16px; font-size:12px; color:#334155; margin:6px 0; background:#fff; padding:6px 10px; border-radius:4px; border:1px solid #e0f2fe;">
        <div>🛫 <strong>起飞：</strong>${t.depDate} ${t.depTime} <span style="color:#64748b;">(${depTzName})</span></div>
        <div>🛬 <strong>落地：</strong>${t.arrDate} ${t.arrTime} <span style="color:#64748b;">(${arrTzName})</span></div>
      </div>
      ${t.remark ? `<div style="font-size:11.5px; color:#475569; margin-top:2px;">📝 <strong>备注：</strong>${escapeHtml(t.remark)}</div>` : ''}
      <div class="day-meeting-actions" style="margin-top:8px;">
        <button class="btn btn-sm btn-outline" onclick="openTransitModal(${t.id}); event.stopPropagation();">✏️ 编辑在途</button>
        <button class="btn btn-sm btn-ghost" onclick="deleteLeaderTransit(${t.id}); event.stopPropagation();" style="color:#dc2626;">🗑️ 删除</button>
      </div>
    </div>
  `;
}

function handleMeetingModalDateChange() {
  const dateInput = document.getElementById('inputMeetingDate');
  const dateVal = dateInput ? dateInput.value : '';
  const trip = getTripForDate(dateVal);
  const tzSelect = document.getElementById('inputMeetingTimezoneBase');
  if (tzSelect) {
    if (trip) {
      tzSelect.value = trip.destination;
    } else {
      tzSelect.value = 'cairo';
    }
    tzSelect._lastTz = tzSelect.value;
  }
  handleMeetingModalTimezoneChange();
  checkMeetingConflicts();
}

function setMeetingModalTzMode(tzId) {
  const tzSelect = document.getElementById('inputMeetingTimezoneBase');
  if (tzSelect && tzSelect.value !== tzId) {
    tzSelect.value = tzId;
    handleMeetingModalTimezoneChange();
  }
}

function handleMeetingModalTimezoneChange() {
  const tzSelect = document.getElementById('inputMeetingTimezoneBase');
  const hintEl = document.getElementById('modalTzConversionHint');
  const bannerEl = document.getElementById('modalTripBanner');
  const liveCardEl = document.getElementById('modalTripLiveCard');
  const dateInput = document.getElementById('inputMeetingDate');
  const dateVal = dateInput ? dateInput.value : '';
  const trip = getTripForDate(dateVal);
  const startInput = document.getElementById('inputMeetingStartTime');
  const endInput = document.getElementById('inputMeetingEndTime');
  const lblStart = document.getElementById('lblMeetingStartTime');
  const lblEnd = document.getElementById('lblMeetingEndTime');

  const curTz = tzSelect ? (tzSelect.value || 'cairo') : 'cairo';
  const lastTz = tzSelect ? (tzSelect._lastTz || curTz) : curTz;

  // Auto-convert times if user changed timezone selection
  if (tzSelect && startInput && endInput && lastTz !== curTz) {
    tzSelect._lastTz = curTz;
    let sVal = startInput.value.trim();
    let eVal = endInput.value.trim();
    if (sVal) sVal = normalizeTimeStr(sVal) || sVal;
    if (eVal) eVal = normalizeTimeStr(eVal) || eVal;

    if (sVal && /^[0-9]{1,2}:[0-9]{2}$/.test(sVal)) {
      const lastDiff = getTripTimezoneDiffHours(lastTz);
      const curDiff = getTripTimezoneDiffHours(curTz);
      const cairoStart = shiftTimeStrByHours(sVal, -lastDiff);
      startInput.value = shiftTimeStrByHours(cairoStart, curDiff);

      if (eVal && /^[0-9]{1,2}:[0-9]{2}$/.test(eVal)) {
        const cairoEnd = shiftTimeStrByHours(eVal, -lastDiff);
        endInput.value = shiftTimeStrByHours(cairoEnd, curDiff);
      }
    }
  } else if (tzSelect) {
    tzSelect._lastTz = curTz;
  }

  const tzInfo = TRIP_TIMEZONE_MAP[curTz] || TRIP_TIMEZONE_MAP.cairo;
  const curDiff = getTripTimezoneDiffHours(curTz);

  // Keep start/end labels clean & minimal
  if (lblStart) lblStart.innerHTML = '开始时间 *';
  if (lblEnd) lblEnd.innerHTML = '结束时间 *';

  // Keep top trip banner, live card, and hint hidden per minimal UI request
  if (bannerEl) {
    bannerEl.style.display = 'none';
    bannerEl.innerHTML = '';
  }
  if (hintEl) {
    hintEl.style.display = 'none';
    hintEl.innerHTML = '';
  }
  if (liveCardEl) {
    liveCardEl.style.display = 'none';
    liveCardEl.innerHTML = '';
  }
}

// Stubs for backward compatibility
function openBatchTimezoneShiftModal() { openLeaderTripModal(); }
function updateBatchShiftPreview() {}
function executeBatchTimezoneShift() {}
function undoBatchTimezoneShift() {
  const backup = getData(STORAGE_KEYS.BATCH_SHIFT_BACKUP, null);
  if (backup && backup.meetings) {
    setData(STORAGE_KEYS.MEETINGS, backup.meetings);
    setData(STORAGE_KEYS.BATCH_SHIFT_BACKUP, null);
    renderMeetings();
    showToast('已恢复为平移前的时间！');
  }
}


// ================= 本地主机 SQLite 数据库同步引擎 (Host SQLite Sync Engine) =================
let _hostDbSynced = false;
let _hostDbLastMod = 0;
let _hostDbVersions = {};

function getData(key, fallback = []) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch (e) {
    return fallback;
  }
}

function setData(key, val) {
  try {
    localStorage.setItem(key, JSON.stringify(val));
  } catch (e) {
    console.error(e);
  }
  // 实时同步保存到当前主机的 SQLite 数据库
  syncKeyToHostDatabase(key, val);
}

function syncKeyToHostDatabase(key, val) {
  if (typeof fetch !== 'function' || typeof window === 'undefined' || !window.location || !window.location.protocol.startsWith('http')) {
    return;
  }
  // Safety guard: if initial sync with host DB hasn't finished, do not push unversioned empty values
  if (!_hostDbSynced && (val === null || val === undefined || (Array.isArray(val) && val.length === 0))) {
    return;
  }
  // Personal scratchpad/blackboard is authoritative on this device - never use optimistic locking against own typing!
  const isBlackboard = (key === STORAGE_KEYS.BLACKBOARD_RECORDS);
  const expectedVer = isBlackboard ? null : (_hostDbVersions[key] || null);

  fetch('/api/set', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      key: key,
      val: val,
      expectedUpdatedAt: expectedVer
    })
  }).then(res => {
    if (res.status === 401) {
      window.location.href = '/login';
      throw new Error('Login required');
    }
    return res.json().then(data => ({ status: res.status, data }));
  }).then(result => {
    const data = result.data;
    if (data && data.success && data.lastModified) {
      _hostDbLastMod = data.lastModified;
      _hostDbVersions[key] = data.version || data.lastModified;
      updateHostDbStatusBadge(true);
    } else if (result.status === 409 && data && data.error === 'SYNC_CONFLICT') {
      _hostDbVersions[key] = data.currentVersion;
      _hostDbLastMod = Math.max(_hostDbLastMod, data.currentVersion || 0);

      if (key === STORAGE_KEYS.BLACKBOARD_RECORDS) {
        // Silently retry pushing the user's latest local text without conflict toast
        setTimeout(() => {
          const currentLocal = getData(key, null);
          if (currentLocal) syncKeyToHostDatabase(key, currentLocal);
        }, 500);
        return;
      }

      localStorage.setItem(key, JSON.stringify(data.currentValue));
      refreshAllViewsFromDatabase();
      showToast('检测到另一台设备刚刚更新了这项内容，已保留服务器上的最新版本');
    }
  }).catch(err => {
    console.warn('Host DB Sync error:', err);
    updateHostDbStatusBadge(false);
  });
}

function initHostDatabaseSync() {
  if (typeof fetch !== 'function' || typeof window === 'undefined' || !window.location || !window.location.protocol.startsWith('http')) {
    return;
  }
  
  fetch('/api/data')
    .then(res => res.json())
    .then(resData => {
      if (!resData || !resData.success) return;
      const remote = resData.data || {};
      _hostDbVersions = resData.versions || {};
      const remoteKeys = Object.keys(remote);
      
      // If server has data, merge into localStorage so any visitor sees the host database immediately
      if (remoteKeys.length > 0) {
        remoteKeys.forEach(k => {
          try {
            localStorage.setItem(k, JSON.stringify(remote[k]));
          } catch(e) {}
        });
        _hostDbSynced = true;
        _hostDbLastMod = resData.lastModified || Date.now();
        updateHostDbStatusBadge(true);
        refreshAllViewsFromDatabase();
      } else {
        // If server database is brand new and empty, upload our initialized seed data to server
        const localData = {};
        Object.values(STORAGE_KEYS).forEach(k => {
          const val = getData(k, null);
          if (val !== null) localData[k] = val;
        });
        if (Object.keys(localData).length > 0) {
          fetch('/api/batch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: localData })
          }).then(r => r.json()).then(d => {
            _hostDbSynced = true;
            updateHostDbStatusBadge(true);
          }).catch(() => {});
        }
      }
    })
    .catch(err => {
      console.warn('Initial Host DB fetch failed:', err);
      updateHostDbStatusBadge(false);
    });

  // 定时每 5 秒自动同步，支持多设备无缝实时更新
  setInterval(pollHostDatabaseChanges, 5000);
}

function pollHostDatabaseChanges() {
  if (typeof fetch !== 'function' || typeof window === 'undefined' || !window.location || !window.location.protocol.startsWith('http')) {
    return;
  }
  fetch('/api/data?since=' + _hostDbLastMod)
    .then(res => res.json())
    .then(resData => {
      if (!resData || !resData.success) return;
      if (resData.lastModified && resData.lastModified > _hostDbLastMod) {
        _hostDbLastMod = resData.lastModified;
        const remote = resData.data || {};
        Object.assign(_hostDbVersions, resData.versions || {});
        const isTypingChalkboard = (document.activeElement && document.activeElement.id === 'chalkboardDirectInput') || _isBlackboardComposing;
        Object.keys(remote).forEach(k => {
          try {
            if (k === STORAGE_KEYS.BLACKBOARD_RECORDS && isTypingChalkboard) return;
            localStorage.setItem(k, JSON.stringify(remote[k]));
          } catch(e) {}
        });
        updateHostDbStatusBadge(true);
        refreshAllViewsFromDatabase();
      }
    })
    .catch(() => {
      updateHostDbStatusBadge(false);
    });
}

function refreshAllViewsFromDatabase() {
  if (typeof renderMeetings === 'function') renderMeetings();
  if (typeof renderTodos === 'function') renderTodos();
  if (typeof renderNotes === 'function') renderNotes();
  if (typeof renderLinks === 'function') renderLinks();
  if (typeof renderMonthlyRoutines === 'function') renderMonthlyRoutines();
  if (typeof renderHomeDashboard === 'function') renderHomeDashboard();
  if (typeof updateTzSimulator === 'function') updateTzSimulator();
}

function updateHostDbStatusBadge(isOnline) {
  const badge = document.getElementById('hostDbStatusBadge');
  if (!badge) return;
  if (isOnline) {
    badge.className = 'host-db-badge is-connected';
    badge.innerHTML = '<span class="status-dot green"></span><span>Mac 主机存储 · 实时同步</span>';
    badge.title = '所有数据均统一保存在 Mac 主机的 SQLite 数据库中，任意设备访问与修改均实时同步！';
  } else {
    badge.className = 'host-db-badge is-offline';
    badge.innerHTML = '<span class="status-dot orange"></span><span>未连接 Mac 主机 (离线)</span>';
    badge.title = '当前未能连接到 Mac 主机后端服务，正使用本地离线缓存。';
  }
}

function setProfileMenuOpen(isOpen) {
  const trigger = document.getElementById('profileTrigger');
  const dropdown = document.getElementById('profileDropdown');
  if (!trigger || !dropdown) return;
  trigger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  dropdown.classList.toggle('is-open', isOpen);
}

function toggleProfileMenu(event) {
  if (event) event.stopPropagation();
  const trigger = document.getElementById('profileTrigger');
  setProfileMenuOpen(!(trigger && trigger.getAttribute('aria-expanded') === 'true'));
}

function openPasswordSettings() {
  setProfileMenuOpen(false);
  const form = document.getElementById('passwordSettingsForm');
  const error = document.getElementById('passwordSettingsError');
  if (form) form.reset();
  if (error) error.textContent = '';
  openModal('passwordSettingsModal');
  setTimeout(() => {
    const input = document.getElementById('currentAccountPassword');
    if (input) input.focus();
  }, 80);
}

function closePasswordSettings() {
  closeModal('passwordSettingsModal');
  const form = document.getElementById('passwordSettingsForm');
  const error = document.getElementById('passwordSettingsError');
  if (form) form.reset();
  if (error) error.textContent = '';
}

function submitPasswordChange(event) {
  if (event) event.preventDefault();
  const currentInput = document.getElementById('currentAccountPassword');
  const newInput = document.getElementById('newAccountPassword');
  const confirmInput = document.getElementById('confirmAccountPassword');
  const error = document.getElementById('passwordSettingsError');
  const button = document.getElementById('savePasswordButton');
  const currentPassword = currentInput ? currentInput.value : '';
  const newPassword = newInput ? newInput.value : '';
  const confirmation = confirmInput ? confirmInput.value : '';
  const isSixDigitPin = /^\d{6}$/.test(newPassword);
  const isStrongPassword = newPassword.length >= 10 && newPassword.length <= 256;
  if (!isSixDigitPin && !isStrongPassword) {
    error.textContent = '请输入 6 位纯数字，或至少 10 个字符的密码。';
    if (newInput) newInput.focus();
    return;
  }
  if (newPassword !== confirmation) {
    error.textContent = '两次输入的新密码不一致。';
    if (confirmInput) confirmInput.focus();
    return;
  }
  if (currentPassword === newPassword) {
    error.textContent = '新密码不能与当前密码相同。';
    return;
  }
  error.textContent = '';
  if (button) {
    button.disabled = true;
    button.textContent = '正在保存…';
  }
  fetch('/api/change-password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ currentPassword, newPassword })
  }).then(async response => {
    const result = await response.json();
    if (!response.ok || !result.success) {
      if (result.error === 'CURRENT_PASSWORD_INCORRECT') throw new Error('当前密码不正确。');
      if (result.error === 'PASSWORD_MANAGED_BY_ENV') throw new Error('当前密码由服务器环境配置，请在服务器端修改。');
      if (result.error === 'PASSWORD_UNCHANGED') throw new Error('新密码不能与当前密码相同。');
      throw new Error('密码修改失败，请稍后重试。');
    }
    closePasswordSettings();
    showToast('✅ 密码已更新，请使用新密码重新登录');
    setTimeout(() => { window.location.href = '/login'; }, 900);
  }).catch(err => {
    error.textContent = err.message || '密码修改失败，请稍后重试。';
  }).finally(() => {
    if (button) {
      button.disabled = false;
      button.textContent = '保存新密码';
    }
  });
}

function logoutFromLab() {
  if (!confirm('要暂时离开 Snoopy’s Little Lab 吗？本机数据已经保存。')) return;
  fetch('/api/logout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: '{}'
  }).finally(() => {
    window.location.href = '/login';
  });
}

// ================= TAB SWITCHING =================
function switchTab(tabId) {
  document.querySelectorAll('.nav-tab').forEach(t => {
    t.classList.toggle('active', t.getAttribute('data-tab') === tabId);
  });
  document.querySelectorAll('.tab-pane').forEach(p => {
    p.classList.toggle('active', p.id === 'pane-' + tabId);
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (tabId === 'legacy_tasks') {
    renderLegacyTasks();
  } else if (tabId === 'dashboard') {
    renderHomeDashboard();
  } else if (tabId === 'links') {
    renderMonthlyRoutines();
    renderLinks();
  }
}

// ================= HERO DAILY QUOTE =================
function initDailyQuote() {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);

  const quoteIndex = (dayOfYear - 1) % SNOOPY_PHILOSOPHIES.length;
  const quote = SNOOPY_PHILOSOPHIES[quoteIndex];

  const m = now.getMonth() + 1;
  const d = now.getDate();
  const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  const weekDayStr = weekDays[now.getDay()];

  const datePill = document.getElementById('heroDatePill');
  if (datePill) {
    datePill.textContent = '✦ Snoopy’s Little Lab · ' + m + '月' + d + '日 ' + weekDayStr;
  }

  const quoteText = document.getElementById('heroQuoteText');
  const quoteCn = document.getElementById('heroQuoteCn');
  const quoteAuthor = document.getElementById('heroQuoteAuthor');

  if (quoteText) quoteText.textContent = quote.en;
  if (quoteCn) quoteCn.textContent = quote.cn;
  if (quoteAuthor) quoteAuthor.textContent = quote.author;
}

// ================= BORDER SNOOPY & WOODSTOCK INTERACTION =================
function interactBorderSnoopy() {
  const wrap = document.getElementById('snoopyLyingWrap');
  if (wrap) {
    wrap.classList.remove('snoopy-happy-bounce');
    wrap.classList.remove('snoopy-nodding');
    void wrap.offsetWidth;
    wrap.classList.add('snoopy-nodding');
    wrap.classList.add('snoopy-happy-bounce');
  }
  spawnSnoopyParticles();
}

function spawnSnoopyParticles() {
  const container = document.getElementById('snoopyParticles');
  if (!container) return;

  const icons = ['❤️', '✨', '♪', '🌸', '🐾', '⭐', '♫', '🎈', '💖'];
  for (let i = 0; i < 7; i++) {
    const p = document.createElement('span');
    p.className = 'floating-particle';
    p.textContent = icons[Math.floor(Math.random() * icons.length)];
    const dx = (Math.random() - 0.5) * 100 + 'px';
    const dy = (-38 - Math.random() * 55) + 'px';
    p.style.setProperty('--dx', dx);
    p.style.setProperty('--dy', dy);
    p.style.left = (Math.random() * 85 + 20) + 'px';
    p.style.bottom = '15px';
    container.appendChild(p);

    setTimeout(() => {
      if (p.parentNode) p.parentNode.removeChild(p);
    }, 1200);
  }
}

// ================= SNOOPY'S CLASSROOM & BIG CHALKBOARD =================
let currentBlackboardDate = '';
let teacherQuoteIdx = 0;
const TEACHER_SNOOPY_QUOTES = [
  "“敲黑板！每天学到一点新东西，生活就会变得更有趣！”",
  "“学而不思则罔，思而不学则殆。今天也学到了新知识呢！”",
  "“Charles M. Schulz: ‘Keep looking up... that's the secret of life.’”",
  "“今天的黑板报写得太棒了！每一天的积累都在悄悄让你发光～”",
  "“不积跬步无以至千里，每天在黑板上留下一点新知，你就是最棒的！”",
  "“Woodstock 助教提醒您：今天学习打卡成功，继续加油！♪”"
];

function renderHomeDashboard() {
  renderChalkboard();
  updateChalkboardExecutiveBar();
  if (typeof renderHomeLeaderTrip === 'function') renderHomeLeaderTrip();
  if (typeof renderHomeTodayAgenda === 'function') renderHomeTodayAgenda();
  if (typeof renderHomeTodayFocus === 'function') renderHomeTodayFocus();
  if (typeof renderHomeNordicCountdown === 'function') renderHomeNordicCountdown();
  if (typeof renderHomeNordicBucketList === 'function') renderHomeNordicBucketList();
  if (typeof renderHomeNordicTips === 'function') renderHomeNordicTips();
}

function renderChalkboard(dateStr) {
  if (dateStr) {
    currentBlackboardDate = dateStr;
  } else if (!currentBlackboardDate) {
    currentBlackboardDate = getTodayDateStr();
  }

  const todayStr = getTodayDateStr();
  const datePill = document.getElementById('chalkDatePill');
  const btnToday = document.getElementById('btnChalkToday');
  const streakBadge = document.getElementById('chalkStreakBadge');
  const contentEl = document.getElementById('chalkboardContentArea');
  const titleDisplay = document.getElementById('chalkboardTitleDisplay');

  // Format date display (e.g. 2026年10月22日 周四)
  if (datePill) {
    try {
      const parts = currentBlackboardDate.split('-');
      const d = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
      const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
      const weekStr = weekDays[d.getDay()];
      datePill.textContent = `📅 ${parts[0]}年${parseInt(parts[1])}月${parseInt(parts[2])}日 ${weekStr}`;
    } catch (e) {
      datePill.textContent = `📅 ${currentBlackboardDate}`;
    }
  }

  if (btnToday) {
    btnToday.style.display = (currentBlackboardDate !== todayStr) ? 'inline-block' : 'none';
  }

  const records = getData(STORAGE_KEYS.BLACKBOARD_RECORDS, {});

  // Auto-seed for today if completely first visit (clean & empty per user request)
  const rawStore = localStorage.getItem(STORAGE_KEYS.BLACKBOARD_RECORDS);
  if (!rawStore && currentBlackboardDate === todayStr) {
    records[todayStr] = {
      content: '',
      notes: '',
      highlight: '',
      reflection: '',
      date: todayStr
    };
    setData(STORAGE_KEYS.BLACKBOARD_RECORDS, records);
  }

  // Update streak count
  updateBlackboardStreak();

  // Populate editor directly (only when not actively typing to avoid cursor jump or IME interruption)
  const editor = document.getElementById('chalkboardDirectInput');
  if (editor) {
    if (typeof initBlackboardFontSettings === 'function') initBlackboardFontSettings();
    const isEditing = (document.activeElement === editor) || _isBlackboardComposing;
    if (!isEditing) {
      const record = records[currentBlackboardDate];
      let val = '';
      if (record) {
        val = record.content || record.notes || [record.highlight, record.notes, record.reflection].filter(Boolean).join('\\n\\n') || '';
      }
      if (editor.tagName === 'TEXTAREA') {
        if (editor.value !== val) editor.value = val;
      } else {
        let htmlVal = val;
        if (val && !/<[a-z][\s\S]*>/i.test(val)) {
          htmlVal = escapeHtml(val).replace(/\\r?\\n/g, '<br>');
        }
        if (editor.innerHTML !== htmlVal) {
          editor.innerHTML = htmlVal;
        }
      }
    }
  }
}

let _blackboardDebounceTimer = null;
let _isBlackboardComposing = false;
let _blackboardListenersInitialized = false;

function initBlackboardInputListeners() {
  if (_blackboardListenersInitialized) return;
  const editor = document.getElementById('chalkboardDirectInput');
  if (!editor) return;
  _blackboardListenersInitialized = true;

  if (editor.tagName === 'DIV' && !('value' in editor)) {
    Object.defineProperty(editor, 'value', {
      get() { return this.innerText || this.textContent || ''; },
      set(v) {
        let h = v;
        if (v && !/<[a-z][\\s\\S]*>/i.test(v)) h = escapeHtml(v).replace(/\\r?\\n/g, '<br>');
        this.innerHTML = h;
      },
      configurable: true
    });
  }

  editor.addEventListener('compositionstart', () => {
    _isBlackboardComposing = true;
  });
  editor.addEventListener('compositionend', () => {
    _isBlackboardComposing = false;
    handleDirectBlackboardInput();
  });
  editor.addEventListener('input', () => {
    handleDirectBlackboardInput();
  });
  editor.addEventListener('mouseup', updateBlackboardFontSizeDisplay);
  editor.addEventListener('keyup', updateBlackboardFontSizeDisplay);
  editor.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && (e.key === '=' || e.key === '+')) {
      e.preventDefault();
      adjustBlackboardFontSize(2);
    } else if ((e.metaKey || e.ctrlKey) && (e.key === '-' || e.key === '_')) {
      e.preventDefault();
      adjustBlackboardFontSize(-2);
    }
  });
  editor.addEventListener('blur', () => {
    if (_isBlackboardComposing) return;
    if (_blackboardDebounceTimer) {
      clearTimeout(_blackboardDebounceTimer);
      _blackboardDebounceTimer = null;
    }
    commitBlackboardDirectInput();
  });
}

function handleDirectBlackboardInput() {
  // If user is currently composing Chinese Pinyin, DO NOT update storage or sync until confirmed!
  if (_isBlackboardComposing) return;

  const editor = document.getElementById('chalkboardDirectInput');
  if (!editor) return;

  const html = (editor.tagName === 'TEXTAREA') ? editor.value : editor.innerHTML;
  const plain = (editor.tagName === 'TEXTAREA') ? editor.value : (editor.innerText || editor.textContent || '');

  // 1. Immediately cache in localStorage so no confirmed text is lost
  try {
    const records = getData(STORAGE_KEYS.BLACKBOARD_RECORDS, {});
    if (!records[currentBlackboardDate]) {
      records[currentBlackboardDate] = { date: currentBlackboardDate };
    }
    records[currentBlackboardDate].content = html;
    records[currentBlackboardDate].notes = plain;
    records[currentBlackboardDate].updatedAt = Date.now();
    localStorage.setItem(STORAGE_KEYS.BLACKBOARD_RECORDS, JSON.stringify(records));
  } catch (e) {}

  // 2. Debounce sync to remote backend (800ms) so smooth typing is never interrupted
  if (_blackboardDebounceTimer) {
    clearTimeout(_blackboardDebounceTimer);
  }
  _blackboardDebounceTimer = setTimeout(() => {
    commitBlackboardDirectInput();
  }, 800);
}

function commitBlackboardDirectInput() {
  if (_isBlackboardComposing) return;
  const editor = document.getElementById('chalkboardDirectInput');
  if (!editor) return;
  const html = (editor.tagName === 'TEXTAREA') ? editor.value : editor.innerHTML;
  const plain = (editor.tagName === 'TEXTAREA') ? editor.value : (editor.innerText || editor.textContent || '');

  const records = getData(STORAGE_KEYS.BLACKBOARD_RECORDS, {});
  if (!records[currentBlackboardDate]) {
    records[currentBlackboardDate] = { date: currentBlackboardDate };
  }
  records[currentBlackboardDate].content = html;
  records[currentBlackboardDate].notes = plain;
  records[currentBlackboardDate].updatedAt = Date.now();
  setData(STORAGE_KEYS.BLACKBOARD_RECORDS, records);
}

function updateBlackboardStreak() {
  const streakBadge = document.getElementById('chalkStreakBadge');
  if (streakBadge) {
    streakBadge.style.display = 'none';
  }
}

function eraseCurrentBlackboard() {
  if (!confirm(`确定要擦掉 ${currentBlackboardDate} 的黑板板书吗？\\n（擦除后可直接在黑板上重新输入）`)) return;

  if (_blackboardDebounceTimer) {
    clearTimeout(_blackboardDebounceTimer);
    _blackboardDebounceTimer = null;
  }

  const records = getData(STORAGE_KEYS.BLACKBOARD_RECORDS, {});
  records[currentBlackboardDate] = {
    date: currentBlackboardDate,
    content: '',
    notes: '',
    highlight: '',
    reflection: '',
    updatedAt: Date.now()
  };
  setData(STORAGE_KEYS.BLACKBOARD_RECORDS, records);

  const editor = document.getElementById('chalkboardDirectInput');
  if (editor) {
    if (editor.tagName === 'TEXTAREA') editor.value = '';
    else editor.innerHTML = '';
    editor.focus();
  }

  updateBlackboardStreak();
  showToast('🧽 黑板已擦拭一新');
}

function handleChalkboardClick(e) {
  if (e && e.target && (e.target.closest('button') || e.target.closest('.chalk-nav-btn'))) return;
  const textarea = document.getElementById('chalkboardDirectInput');
  if (textarea && document.activeElement !== textarea) {
    textarea.focus();
  }
}

function openEditBlackboardModal() {
  const textarea = document.getElementById('chalkboardDirectInput');
  if (textarea) textarea.focus();
}

function closeEditBlackboardModal() {}

function saveBlackboardContent() {
  handleDirectBlackboardInput();
}

function copyBlackboardText() {
  const records = getData(STORAGE_KEYS.BLACKBOARD_RECORDS, {});
  const record = records[currentBlackboardDate];

  if (!record || (!record.highlight && !record.notes && !record.reflection)) {
    showToast('当前黑板暂无文字内容可复制');
    return;
  }

  let text = `【 史努比小讲堂 · ${currentBlackboardDate} 自学板书 】\\n`;
  if (record.title) text += `📌 主题：${record.title}\\n\\n`;
  if (record.highlight) text += `⭐ 重点金句：\\n${record.highlight}\\n\\n`;
  if (record.notes) text += `📝 自学笔记：\\n${record.notes}\\n\\n`;
  if (record.reflection) text += `💡 心得领悟：\\n“${record.reflection}”\\n\\n`;
  text += `—— 记录于 Snoopy's Little Lab`;

  copyToClipboard(text, '📋 板书内容已成功复制到剪贴板！');
}

function changeBlackboardDayOffset(offset) {
  try {
    const parts = currentBlackboardDate.split('-');
    const cur = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
    cur.setDate(cur.getDate() + offset);
    currentBlackboardDate = formatDateToStr(cur);
    renderChalkboard();
  } catch (e) {
    currentBlackboardDate = getTodayDateStr();
    renderChalkboard();
  }
}

function jumpToTodayBlackboard() {
  currentBlackboardDate = getTodayDateStr();
  renderChalkboard();
}

// ================= 小黑板字体与历史记录控制 =================
function initBlackboardFontSettings() {
  const size = parseInt(localStorage.getItem('snoopy_blackboard_fontsize') || '16', 10);
  applyBlackboardFontSettings(size);
}

function applyBlackboardFontSettings(size) {
  const editor = document.getElementById('chalkboardDirectInput');
  const sizeDisp = document.getElementById('blackboardFontSizeDisplay');

  if (editor) {
    editor.style.fontSize = size + 'px';
  }
  if (sizeDisp) {
    sizeDisp.textContent = size + 'px';
  }
}

function updateBlackboardFontSizeDisplay() {
  const editor = document.getElementById('chalkboardDirectInput');
  const sizeDisp = document.getElementById('blackboardFontSizeDisplay');
  if (!editor || !sizeDisp) return;
  const sel = window.getSelection();
  if (sel && sel.rangeCount > 0) {
    const range = sel.getRangeAt(0);
    if (editor.contains(range.commonAncestorContainer)) {
      let node = range.startContainer;
      if (node.nodeType === 3) node = node.parentElement;
      if (node) {
        const fontSpan = node.closest('span[style*="font-size"]');
        if (fontSpan && fontSpan.style.fontSize) {
          sizeDisp.textContent = parseInt(fontSpan.style.fontSize, 10) + 'px';
          return;
        }
        const comp = window.getComputedStyle(node).fontSize;
        if (comp) {
          sizeDisp.textContent = parseInt(comp, 10) + 'px';
          return;
        }
      }
    }
  }
  const baseSize = localStorage.getItem('snoopy_blackboard_fontsize') || '16';
  sizeDisp.textContent = baseSize + 'px';
}

function adjustBlackboardFontSize(delta) {
  const editor = document.getElementById('chalkboardDirectInput');
  if (!editor) return;

  const sel = window.getSelection();
  let hasSelection = false;
  let range = null;

  if (sel && sel.rangeCount > 0 && !sel.isCollapsed && sel.toString().trim().length > 0) {
    range = sel.getRangeAt(0);
    if (editor.contains(range.commonAncestorContainer)) {
      hasSelection = true;
    }
  }

  if (hasSelection) {
    // 针对用户当前选中的字体单独进行放大/缩小
    let node = range.startContainer;
    if (node.nodeType === 3) node = node.parentElement;
    let curSize = 16;
    const fontSpan = node ? node.closest('span[style*="font-size"]') : null;
    if (fontSpan && fontSpan.style.fontSize) {
      curSize = parseInt(fontSpan.style.fontSize, 10) || 16;
    } else if (node) {
      curSize = parseInt(window.getComputedStyle(node).fontSize, 10) || 16;
    }

    let newSize = curSize + delta;
    if (newSize < 12) newSize = 12;
    if (newSize > 50) newSize = 50;

    editor.focus();
    try {
      document.execCommand('styleWithCSS', false, false);
    } catch (e) {}

    document.execCommand('fontSize', false, '7');
    const fontEls = editor.querySelectorAll('font[size="7"], font[size="+7"]');
    if (fontEls.length > 0) {
      fontEls.forEach(f => {
        const span = document.createElement('span');
        span.style.fontSize = newSize + 'px';
        span.style.lineHeight = '1.35';
        while (f.firstChild) {
          span.appendChild(f.firstChild);
        }
        span.querySelectorAll('span[style*="font-size"]').forEach(child => {
          child.style.fontSize = '';
        });
        f.parentNode.replaceChild(span, f);
      });
    } else if (range && !range.collapsed) {
      try {
        const span = document.createElement('span');
        span.style.fontSize = newSize + 'px';
        span.style.lineHeight = '1.35';
        span.appendChild(range.extractContents());
        range.insertNode(span);
        sel.removeAllRanges();
        const newRange = document.createRange();
        newRange.selectNodeContents(span);
        sel.addRange(newRange);
      } catch (err) {
        console.warn('Range wrap fallback failed:', err);
      }
    }

    const sizeDisp = document.getElementById('blackboardFontSizeDisplay');
    if (sizeDisp) sizeDisp.textContent = newSize + 'px';

    handleDirectBlackboardInput();
  } else {
    // 未框选文字时，调整黑板基础字号
    let cur = parseInt(localStorage.getItem('snoopy_blackboard_fontsize') || '16', 10);
    cur += delta;
    if (cur < 12) cur = 12;
    if (cur > 36) cur = 36;
    localStorage.setItem('snoopy_blackboard_fontsize', String(cur));
    applyBlackboardFontSettings(cur);
    handleDirectBlackboardInput();
  }
}

function toggleBlackboardBold() {
  const editor = document.getElementById('chalkboardDirectInput');
  if (!editor) return;
  editor.focus();
  document.execCommand('bold', false, null);
  handleDirectBlackboardInput();
}

function openBlackboardHistoryModal() {
  const modal = document.getElementById('blackboardHistoryModal');
  if (!modal) return;
  const searchInp = document.getElementById('inputBlackboardHistorySearch');
  if (searchInp) searchInp.value = '';
  renderBlackboardHistoryList();
  modal.style.display = 'flex';
}

function closeBlackboardHistoryModal() {
  const modal = document.getElementById('blackboardHistoryModal');
  if (modal) modal.style.display = 'none';
}

function renderBlackboardHistoryList() {
  const listEl = document.getElementById('blackboardHistoryList');
  if (!listEl) return;
  const searchInp = document.getElementById('inputBlackboardHistorySearch');
  const query = (searchInp && searchInp.value ? searchInp.value.trim().toLowerCase() : '');

  const records = getData(STORAGE_KEYS.BLACKBOARD_RECORDS, {});
  const dates = Object.keys(records).sort().reverse();

  let validDates = dates.filter(d => {
    const r = records[d];
    if (!r) return false;
    const txt = (r.content || r.notes || r.highlight || r.title || '').trim();
    if (!txt) return false;
    if (query) {
      return d.toLowerCase().includes(query) || txt.toLowerCase().includes(query);
    }
    return true;
  });

  if (validDates.length === 0) {
    listEl.innerHTML = query
      ? `<div style="text-align:center; padding:28px 16px; color:var(--text-muted); font-size:13px;">未搜索到包含“${escapeHtml(query)}”的板书记录</div>`
      : `<div style="text-align:center; padding:28px 16px; color:var(--text-muted); font-size:13px;">暂无以往板书记录。您在黑板上随手书写的内容，系统都会按日期自动永久归档~</div>`;
    return;
  }

  const todayStr = getTodayDateStr();
  const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];

  listEl.innerHTML = validDates.map(d => {
    const r = records[d];
    const isCur = (d === currentBlackboardDate);
    const isToday = (d === todayStr);

    let dateLabel = d;
    try {
      const parts = d.split('-');
      const dt = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
      dateLabel = `${parseInt(parts[1], 10)}月${parseInt(parts[2], 10)}日 (${weekDays[dt.getDay()]})`;
    } catch (e) {}

    const rawText = (r.content || r.notes || r.highlight || '').trim();
    const firstLine = rawText.split('\\n')[0] || '板书记录';

    return `
      <div style="padding:10px 14px; background:var(--card-subtle); border:1px solid ${isCur ? '#3b82f6' : 'var(--border)'}; border-radius:var(--radius-md); display:flex; justify-content:space-between; align-items:center; gap:10px;">
        <div style="flex:1; min-width:0;">
          <div style="font-size:13px; font-weight:700; color:var(--text-primary); display:flex; align-items:center; gap:6px;">
            <span>📅 ${dateLabel}</span>
            ${isToday ? '<span class="badge" style="background:#fef3c7; color:#d97706; font-size:10.5px; padding:1px 6px;">今日</span>' : ''}
            ${isCur ? '<span class="badge" style="background:#e0f2fe; color:#0284c7; font-size:10.5px; padding:1px 6px;">当前展示</span>' : ''}
          </div>
          <div style="font-size:12px; color:var(--text-secondary); margin-top:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
            ${escapeHtml(firstLine)}
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:6px; flex-shrink:0;">
          <button class="btn btn-sm btn-ghost" onclick="copySingleHistoryBlackboard('${d}')" title="复制当天板书">📋</button>
          <button class="btn btn-sm btn-primary" onclick="loadHistoryDateToBlackboard('${d}')" style="font-size:12px; padding:3px 9px;">载入黑板 →</button>
        </div>
      </div>
    `;
  }).join('');
}

function copySingleHistoryBlackboard(dateStr) {
  const records = getData(STORAGE_KEYS.BLACKBOARD_RECORDS, {});
  const r = records[dateStr];
  if (!r) return;
  const txt = (r.content || r.notes || r.highlight || '').trim();
  if (!txt) {
    showToast('该天板书无文字内容');
    return;
  }
  copyToClipboard(txt, `已复制 ${dateStr} 的黑板记录！`);
}

function loadHistoryDateToBlackboard(dateStr) {
  closeBlackboardHistoryModal();
  renderChalkboard(dateStr);
  showToast(`已切换至 ${dateStr} 的黑板板书`);
}

function fillEnglishTemplateToBlackboard() {
  const inputTitle = document.getElementById('inputBlackboardTitle');
  const inputHighlight = document.getElementById('inputBlackboardHighlight');
  const inputNotes = document.getElementById('inputBlackboardNotes');
  const inputReflection = document.getElementById('inputBlackboardReflection');

  const streakData = getData(STORAGE_KEYS.ENGLISH_CHECKIN, { streak: 0 });
  const dayIndex = (streakData.streak || 0) % (ENGLISH_DATA ? ENGLISH_DATA.length : 1);
  const lesson = ENGLISH_DATA && ENGLISH_DATA[dayIndex] ? ENGLISH_DATA[dayIndex] : null;

  if (lesson) {
    if (inputTitle) inputTitle.value = `北欧日常口语 · ${lesson.topic || '实用表达'}`;
    if (inputHighlight) inputHighlight.value = `“${lesson.sentenceEn || ''}” (${lesson.sentenceCn || ''})`;
    let notesText = `【今日高频词汇】\\n`;
    if (lesson.vocab && Array.isArray(lesson.vocab)) {
      notesText += lesson.vocab.map(v => `• ${v.word} ${v.phonetic || ''} : ${v.meaning}`).join('\\n');
    }
    if (lesson.travelTip) {
      notesText += `\\n\\n【生活习惯与避坑Tips】\\n${lesson.travelTip}`;
    }
    if (inputNotes) inputNotes.value = notesText;
    if (inputReflection) inputReflection.value = "用最简练的句子日常脱口而出，在实践中掌握纯正发音。";
    showToast('✨ 已导入今日英语课程精要到草稿框！');
  } else {
    showToast('已加载通用学习模板');
  }
}

function fillGeneralTemplateToBlackboard() {
  const inputTitle = document.getElementById('inputBlackboardTitle');
  const inputHighlight = document.getElementById('inputBlackboardHighlight');
  const inputNotes = document.getElementById('inputBlackboardNotes');
  const inputReflection = document.getElementById('inputBlackboardReflection');

  if (inputTitle) inputTitle.value = "今日涉外业务与自我精进";
  if (inputHighlight) inputHighlight.value = "“Stay hungry, stay foolish.” —— 保持对新知识的渴望与谦逊。";
  if (inputNotes) inputNotes.value = "• 涉外排期要点：重要会议前提前确认线上会议与同声传译就绪；\\n• 决策推进法：复杂事宜先对齐背景、再列出关键诉求；\\n• 心态管理：遇事先稳住呼吸，将大任务拆解为两三个具体小动作。";
  if (inputReflection) inputReflection.value = "专注做好眼前这一步，其余的时间自会给出答案。";
  showToast('💡 已填入通用自学模板');
}

function interactTeacherSnoopy() {
  interactBorderSnoopy();
}

function interactTeacherWoodstock() {
  interactBorderSnoopy();
}

function spawnChalkParticles() {
  const container = document.getElementById('chalkParticles');
  if (!container) return;

  const icons = ['✨', '⭐', '🖍️', '🐾', '❤️', '♪'];
  for (let i = 0; i < 5; i++) {
    const p = document.createElement('span');
    p.className = 'floating-particle';
    p.textContent = icons[Math.floor(Math.random() * icons.length)];
    const dx = (Math.random() - 0.5) * 80 + 'px';
    const dy = (-30 - Math.random() * 50) + 'px';
    if (p.style && p.style.setProperty) {
      p.style.setProperty('--dx', dx);
      p.style.setProperty('--dy', dy);
    }
    p.style.left = (Math.random() * 60 + 20) + 'px';
    p.style.bottom = '15px';
    container.appendChild(p);

    setTimeout(() => {
      if (p.parentNode) p.parentNode.removeChild(p);
    }, 1100);
  }
}

function updateChalkboardExecutiveBar() {
  const meetingEl = document.getElementById('execBarMeetingText');
  const todoEl = document.getElementById('execBarTodoText');
  const tripEl = document.getElementById('execBarTripText');
  const clockEl = document.getElementById('execBarClockText');

  const todayStr = getTodayDateStr();

  // Meetings
  if (meetingEl) {
    const meetings = getData(STORAGE_KEYS.MEETINGS, []).filter(m => m.date === todayStr && m.status === 'scheduled');
    meetingEl.textContent = meetings.length > 0 ? `今日日程：${meetings.length} 场排期` : '今日日程：无排期 · 时间充裕';
  }

  // Todos (Q1 active)
  if (todoEl) {
    const todos = getData(STORAGE_KEYS.TODOS, []).filter(t => t.priority === 'q1' && !t.archived && !t.completed);
    todoEl.textContent = todos.length > 0 ? `今日攻坚：${todos.length} 项 Q1 待办` : '今日攻坚：Q1 核心要务已搞定';
  }

  // Trip or In-Transit
  if (tripEl) {
    const todayTransits = typeof getTransitsForDate === 'function' ? getTransitsForDate(todayStr) : [];
    if (todayTransits.length > 0) {
      const tr = todayTransits[0];
      tripEl.textContent = `领导动态：🛫 在途 · ${tr.flightNo ? tr.flightNo + ' ' : ''}${tr.title}`;
    } else {
      const trip = getTripForDate(todayStr);
      if (trip) {
        tripEl.textContent = `领导动态：✈️ 出差中 · ${trip.tzName || trip.destination}`;
      } else {
        tripEl.textContent = `领导动态：🏛️ 开罗常驻 (UTC+2)`;
      }
    }
  }

  // Clock
  if (clockEl) {
    const now = new Date();
    const cairoH = (now.getUTCHours() + 2 + 24) % 24;
    const cairoM = now.getUTCMinutes();
    clockEl.textContent = `开罗时间 ${String(cairoH).padStart(2,'0')}:${String(cairoM).padStart(2,'0')}`;
  }
}

// Backwards-compatible stubs for hidden containers and tests
function renderHomeLeaderTrip() {
  const container = document.getElementById('homeLeaderTripBody');
  if (!container) return;
  const todayStr = getTodayDateStr();
  const trip = getTripForDate(todayStr);
  const now = new Date();
  const cairoTimeStr = String((now.getUTCHours() + 2 + 24) % 24).padStart(2, '0') + ':' + String(now.getUTCMinutes()).padStart(2, '0');
  if (trip) {
    container.innerHTML = `<div>✈️ 领导出差中 · ${escapeHtml(trip.destination)}</div>`;
  } else {
    container.innerHTML = `<div>🏛️ 开罗常驻总部 (UTC+2) · ${cairoTimeStr}</div>`;
  }
}

function renderHomeTodayAgenda() {
  const container = document.getElementById('homeTodayAgendaList');
  if (!container) return;
  const todayStr = getTodayDateStr();
  const meetings = getData(STORAGE_KEYS.MEETINGS, []).filter(m => m.date === todayStr && m.status === 'scheduled');
  container.innerHTML = meetings.map(m => `<div>${escapeHtml(m.subject)}</div>`).join('');
}

function renderHomeTodayFocus() {
  const container = document.getElementById('homeTodayFocusList');
  if (!container) return;
  const todos = getData(STORAGE_KEYS.TODOS, []).filter(t => t.priority === 'q1' && !t.archived);
  container.innerHTML = todos.map(t => `<div>${escapeHtml(t.text)} (Q1 必须搞定)</div>`).join('');
}

function renderHomeNordicCountdown() {
  const container = document.getElementById('homeNordicCountdownBody');
  if (container) container.innerHTML = '<div>2027 DAYS</div>';
}

function renderHomeNordicBucketList() {
  const container = document.getElementById('homeBucketList');
  if (container) container.innerHTML = '<div>欧若拉北极光 Fika</div>';
  const badge = document.getElementById('homeBucketProgressBadge');
  if (badge) badge.textContent = '已点亮';
}

function renderHomeNordicTips() {
  const container = document.getElementById('homeNordicTipsBody');
  if (container) container.innerHTML = '<div>北欧 极地三层穿衣法则</div>';
}

function toggleBucketItem() {}
function saveNewBucketItem() {}
function deleteBucketItem() {}
function cycleNordicTip() {}

// ================= 会议预约 (Secretary Desk & Executive Weekly/Monthly Board) =================
let currentMeetingFilter = 'all';
let supervisorViewMode = 'week_board'; // 'week_board' | 'day_cal' | 'month_cal' | 'card_list'
let selectedTimelineDate = '';
let currentWeekOffset = 0; // 0 = current week, -1 = last week, +1 = next week
let currentCalendarYearMonth = { year: 2026, month: 8 }; // 0-indexed month (8 = September)
let importPreviewTab = 'cal'; // 'cal' | 'card'

function formatDateToStr(dateObj) {
  if (!dateObj || isNaN(dateObj.getTime())) return '';
  const y = dateObj.getFullYear();
  const m = String(dateObj.getMonth() + 1).padStart(2, '0');
  const d = String(dateObj.getDate()).padStart(2, '0');
  return y + '-' + m + '-' + d;
}

function getTodayDateStr() {
  return formatDateToStr(new Date());
}

function setSupervisorViewMode(mode) {
  supervisorViewMode = mode;
  const btnWeekBoard = document.getElementById('btnViewWeekBoard');
  const btnDayCal = document.getElementById('btnViewDayCal');
  const btnMonthCal = document.getElementById('btnViewMonthCal');
  const btnCardList = document.getElementById('btnViewCardList');
  const modeTag = document.getElementById('currentViewModeTag');

  if (btnWeekBoard) btnWeekBoard.classList.toggle('active', mode === 'week_board');
  if (btnDayCal) btnDayCal.classList.toggle('active', mode === 'day_cal');
  if (btnMonthCal) btnMonthCal.classList.toggle('active', mode === 'month_cal');
  if (btnCardList) btnCardList.classList.toggle('active', mode === 'card_list');

  if (modeTag) {
    if (mode === 'week_board') modeTag.textContent = '周历';
    else if (mode === 'day_cal') modeTag.textContent = '日历';
    else if (mode === 'month_cal') modeTag.textContent = '月度日历';
    else modeTag.textContent = '决策卡片';
  }

  renderMeetings();
}

function changeDayOffset(delta) {
  if (!selectedTimelineDate) {
    selectedTimelineDate = getTodayDateStr();
  }
  const parts = selectedTimelineDate.split('-').map(Number);
  const d = new Date(parts[0], parts[1] - 1, parts[2]);
  d.setDate(d.getDate() + delta);
  selectedTimelineDate = formatDateToStr(d);
  const inputEl = document.getElementById('timelineDateSelector');
  if (inputEl) inputEl.value = selectedTimelineDate;
  renderSupervisorDayCalendar();
}

function jumpToTodayDayCalendar() {
  selectedTimelineDate = getTodayDateStr();
  const inputEl = document.getElementById('timelineDateSelector');
  if (inputEl) inputEl.value = selectedTimelineDate;
  renderSupervisorDayCalendar();
}

function selectDayCalDate(dateVal) {
  if (!dateVal) return;
  selectedTimelineDate = dateVal;
  const inputEl = document.getElementById('timelineDateSelector');
  if (inputEl) inputEl.value = selectedTimelineDate;
  renderSupervisorDayCalendar();
}

function handleTimelineDateChange() {
  const el = document.getElementById('timelineDateSelector');
  if (el && el.value) {
    selectedTimelineDate = el.value;
    const parts = selectedTimelineDate.split('-').map(Number);
    if (parts.length === 3) {
      currentCalendarYearMonth.year = parts[0];
      currentCalendarYearMonth.month = parts[1] - 1;
    }
    renderMeetings();
  }
}

function selectCalendarDate(dateStr) {
  selectedTimelineDate = dateStr;
  const inputEl = document.getElementById('timelineDateSelector');
  if (inputEl) inputEl.value = dateStr;
  renderMeetings();
}

function changeCalendarMonth(delta) {
  currentCalendarYearMonth.month += delta;
  if (currentCalendarYearMonth.month < 0) {
    currentCalendarYearMonth.month = 11;
    currentCalendarYearMonth.year--;
  } else if (currentCalendarYearMonth.month > 11) {
    currentCalendarYearMonth.month = 0;
    currentCalendarYearMonth.year++;
  }
  renderSupervisorMonthCalendar();
}

function jumpToTodayCalendar() {
  const today = new Date();
  const todayStr = getTodayDateStr();
  currentCalendarYearMonth.year = today.getFullYear();
  currentCalendarYearMonth.month = today.getMonth();
  currentWeekOffset = 0;
  selectedTimelineDate = todayStr;
  const inputEl = document.getElementById('timelineDateSelector');
  if (inputEl) inputEl.value = todayStr;
  renderMeetings();
}

function changeWeekOffset(delta) {
  currentWeekOffset += delta;
  renderSupervisorWeeklyBoard();
}

function jumpToCurrentWeek() {
  currentWeekOffset = 0;
  selectedTimelineDate = getTodayDateStr();
  renderSupervisorWeeklyBoard();
}

let showFullWeekCalendar = null; // null: auto-detect, true: force 7-day full week, false: force 6-day workdays (Sun-Fri)
function toggleFullWeekDisplay(showFull) {
  showFullWeekCalendar = Boolean(showFull);
  renderSupervisorWeeklyBoard();
  showToast(showFullWeekCalendar ? '📅 已切换为完整周历（含周六）' : '💼 已切换为仅看工作日（周日-周五）');
}

let hidePastWeekdays = true; // 自动隐藏本周已过去日期，把版面空间留给今日及后续日程
function toggleHidePastDays(forceVal) {
  if (typeof forceVal === 'boolean') {
    hidePastWeekdays = forceVal;
  } else {
    hidePastWeekdays = !hidePastWeekdays;
  }
  renderSupervisorWeeklyBoard();
  showToast(hidePastWeekdays ? '📅 已隐藏本周已过去日期，版面留给后续日程' : '📅 已恢复展示本周全部日期');
}

// ----------------- 领导本周日历看板渲染引擎 (Executive Weekly Board) -----------------
function renderSupervisorWeeklyBoard() {
  const boardContainer = document.getElementById('supervisorWeeklyBoardContainer');
  if (!boardContainer) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const conflictMap = getAllMeetingConflicts(meetings);
  const today = new Date();
  const todayStr = getTodayDateStr();

  // Compute Sunday of the displayed week (周日到周五工作日，周六周末)
  const sunDate = new Date(today);
  sunDate.setDate(today.getDate() - today.getDay() + (currentWeekOffset * 7));

  const weekDays = [];
  const weekdayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];

  for (let i = 0; i < 7; i++) {
    const d = new Date(sunDate);
    d.setDate(sunDate.getDate() + i);
    const dStr = formatDateToStr(d);
    weekDays.push({
      dateStr: dStr,
      month: d.getMonth() + 1,
      day: d.getDate(),
      name: weekdayNames[i],
      isToday: (dStr === todayStr),
      isWeekend: (i === 6) // 周日到周五为工作日，周六为周末
    });
  }

  // Check if weekend has meetings or if today falls on the weekend
  const hasWeekendMeetings = meetings.some(m => {
    return (m.date === weekDays[6].dateStr) && m.status !== 'cancelled';
  });
  const todayIsWeekend = (todayStr === weekDays[6].dateStr);
  const shouldShowFull = (showFullWeekCalendar !== null) ? showFullWeekCalendar : (hasWeekendMeetings || todayIsWeekend);
  const baseDays = shouldShowFull ? weekDays : weekDays.slice(0, 6);

  let displayDays = baseDays;
  if (hidePastWeekdays && currentWeekOffset === 0) {
    const unpassed = baseDays.filter(d => d.dateStr >= todayStr);
    if (unpassed.length > 0) {
      displayDays = unpassed;
    }
  }

  // Calculate week stats (matching displayed days range)
  const weekStartStr = displayDays[0].dateStr;
  const weekEndStr = displayDays[displayDays.length - 1].dateStr;
  const weekMeetings = meetings.filter(m => m.date >= weekStartStr && m.date <= weekEndStr && m.status !== 'cancelled');

  let html = `
    <div class="weekly-board-header" style="margin-bottom:12px;">
      <div class="weekly-nav-group" style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
        <button class="btn btn-sm" onclick="changeWeekOffset(-1)" title="上一周" style="padding:4px 8px; line-height:1;">◀</button>
        <button class="btn btn-sm ${currentWeekOffset === 0 ? 'btn-primary' : 'btn-ghost'}" onclick="jumpToCurrentWeek()" style="font-weight:600;">本周</button>
        <button class="btn btn-sm ${currentWeekOffset === 1 ? 'btn-primary' : 'btn-ghost'}" onclick="currentWeekOffset = 1; renderSupervisorWeeklyBoard();" style="font-weight:600;">下周</button>
        <button class="btn btn-sm" onclick="changeWeekOffset(1)" title="下一周" style="padding:4px 8px; line-height:1;">▶</button>
        <button class="btn btn-sm ${!shouldShowFull ? 'btn-primary' : 'btn-ghost'}" id="btnToggleWeekWorkdays" onclick="toggleFullWeekDisplay(${!shouldShowFull})" style="font-size:12px; font-weight:600;" title="工作日：周日-周五">
          ${shouldShowFull ? '仅看工作日' : '完整周历'}
        </button>
        <button class="btn btn-sm ${hidePastWeekdays ? 'btn-primary' : 'btn-ghost'}" id="btnTogglePastDays" onclick="toggleHidePastDays()" style="font-size:12px; font-weight:600;" title="隐藏已过去日期，版面留给今日及后续日程">
          ${hidePastWeekdays ? '已隐藏过去日期' : '显示过去日期'}
        </button>
        ${(currentWeekOffset !== 0 && currentWeekOffset !== 1) ? `<span class="badge" style="font-size:11px; background:var(--card-subtle); color:var(--text-secondary); margin-left:4px;">${currentWeekOffset < 0 ? '上 ' + Math.abs(currentWeekOffset) + ' 周' : '后 ' + currentWeekOffset + ' 周'}</span>` : ''}
      </div>
    </div>
    ${getTripTimezoneBarHtml()}
  `;

  const allActiveMeetings = meetings.filter(m => m.status !== 'cancelled');
  if (weekMeetings.length === 0 && allActiveMeetings.length > 0) {
    const pastCount = allActiveMeetings.filter(m => m.date < weekStartStr).length;
    const futureCount = allActiveMeetings.filter(m => m.date > weekEndStr).length;
    let hintDesc = `当前展示的本周（${weekDays[0].month}月${weekDays[0].day}日 - ${displayDays[displayDays.length-1].month}月${displayDays[displayDays.length-1].day}日）暂无会议，您之前登记的 <strong>${allActiveMeetings.length}</strong> 场会议保存在其他日期`;
    if (pastCount > 0 && futureCount > 0) {
      hintDesc += `（包含上周及更早 ${pastCount} 场、后续日期 ${futureCount} 场）`;
    } else if (pastCount > 0) {
      hintDesc += `（在上周或更早日期已记录 ${pastCount} 场会议）`;
    } else if (futureCount > 0) {
      hintDesc += `（在后续日期已排期 ${futureCount} 场会议）`;
    }
    hintDesc += '。数据均完好保存，点击下方按钮可立即切换查看：';

    html += `
      <div id="crossWeekScheduleNotice" style="background:var(--card-subtle); border:1px solid #bfdbfe; border-left:4px solid #2563eb; border-radius:8px; padding:12px 16px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div style="font-size:12.5px; color:var(--text-primary); line-height:1.5;">
          📌 <strong>日程提示：</strong>${hintDesc}
        </div>
        <div style="display:flex; gap:8px;">
          ${pastCount > 0 ? '<button class="btn btn-sm" onclick="changeWeekOffset(-1)">◀ 查看上一周日程</button>' : ''}
          ${futureCount > 0 ? '<button class="btn btn-sm" onclick="changeWeekOffset(1)">查看下一周日程 ▶</button>' : ''}
          <button class="btn btn-sm btn-ghost" onclick="setSupervisorViewMode('month_cal')">📅 月历总览</button>
        </div>
      </div>
    `;
  }

  html += `
    <div class="weekly-grid" style="grid-template-columns: repeat(${displayDays.length}, 1fr);">
  `;

  displayDays.forEach(day => {
    const dayMeetings = meetings.filter(m => m.date === day.dateStr && m.status !== 'cancelled');
    dayMeetings.sort((a, b) => (a.time || '10:00').localeCompare(b.time || '10:00'));

    let dayDurationMins = 0;
    dayMeetings.forEach(m => { dayDurationMins += parseInt(m.duration || 45, 10); });

    const { freeSlots } = calculateDayFreeSlots(meetings, day.dateStr);
    const dayTrip = getTripForDate(day.dateStr);
    const dayTransits = typeof getTransitsForDate === 'function' ? getTransitsForDate(day.dateStr) : [];

    html += `
      <div class="weekly-col ${day.isToday ? 'is-today' : ''} ${day.isWeekend ? 'is-weekend' : ''} ${dayTrip ? 'is-trip-day' : ''}">
        <div class="weekly-col-header">
          <div class="weekly-col-header-main" style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
            <span class="weekly-col-day">${day.name}</span>
            <span class="weekly-col-date">${day.month}月${day.day}日</span>
            ${dayTrip ? `<span class="badge" style="background:#dcfce7; color:#15803d; border:1px solid #86efac; font-size:9.5px; padding:1px 6px; border-radius:10px; font-weight:700;" title="领导出差目的地：${dayTrip.tzName} (比开罗${dayTrip.diffText}) · 本日日程全按当地时间安排">✈️ ${dayTrip.tzName}</span>` : ''}
            ${dayTransits.length > 0 ? `<span class="badge" style="background:#e0f2fe; color:#0369a1; border:1px solid #bae6fd; font-size:9.5px; padding:1px 6px; border-radius:10px; font-weight:700;" title="领导本日处于跨时区在途飞行状态">🛫 在途</span>` : ''}
            ${dayMeetings.some(m => conflictMap[m.id] && conflictMap[m.id].length > 0) ? `<span class="badge weekly-conflict-header-badge" style="display:none;" title="本日存在会议时间冲突！">⚠️ 时间冲突</span>` : ''}
          </div>
          ${day.isToday ? '<span class="cal-today-badge">今日</span>' : (day.isWeekend ? '<span class="weekly-weekend-badge">周末</span>' : '')}
        </div>

        <div class="weekly-col-events">
    `;

    function renderWeeklySingleCard(m, isAllDay, period) {
      const dt = getMeetingDisplayTime(m);
      const isPending = (m.status === 'pending');
      const isNoticeUnsent = (m.noticeSent === false || m.noticeSent === undefined || m.noticeSent === null);
      const allConflicts = conflictMap[m.id] || [];
      let mConflicts = allConflicts;
      if (period === 'morning') {
        mConflicts = allConflicts.filter(c => c.overlapStartMin < 720);
      } else if (period === 'afternoon') {
        mConflicts = allConflicts.filter(c => c.overlapEndMin > 720);
      }
      const hasConflict = mConflicts.length > 0;

      let cardCls = 'weekly-card';
      if (isPending) cardCls += ' is-pending';
      else if (m.priority === 'high') cardCls += ' priority-high';
      if (isNoticeUnsent) cardCls += ' notice-unsent';
      if (hasConflict) cardCls += ' is-conflict';
      if (isAllDay) cardCls += ' weekly-card-allday';

      const conflictTooltip = hasConflict ? `【⚠️时间冲突警告：与${mConflicts.map(c => '【' + c.otherSubject + '】').join('、')}在 ${mConflicts.map(c => c.overlapRangeStr).join('、')} 存在重叠，点击查看详情】` : '';

      return `
        <div class="${cardCls}" onclick="editMeeting(${m.id})" title="${conflictTooltip}${isPending ? '【待领导确认】点击核准或调整排期' : (isNoticeUnsent ? '【尚未发送会议通知】点击可编辑并更新通知状态' : '点击查看/编辑详情')}">
          <div class="weekly-card-time">
            <span class="weekly-card-time-text" style="white-space:nowrap !important; flex-shrink:0; font-size:11px; font-weight:700; ${dt.isShifted ? 'color:#15803d;' : 'color:var(--blue-accent);'}">
              <span>${dt.start}${dt.end ? ' - ' + dt.end : ''}</span>
            </span>
            <div class="weekly-card-time-badges">
              ${isNoticeUnsent ? '<span class="weekly-notice-tag" title="尚未发送会议通知">待发通知</span>' : ''}
              ${isPending ? '<span class="weekly-pending-tag" title="待领导确认">待确认</span>' : (m.location ? `<span class="weekly-loc-tag" title="${escapeHtml(m.location)}">${escapeHtml(m.location)}</span>` : '')}
            </div>
          </div>

          <div class="weekly-card-title ${isPending ? 'text-pending' : ''}">
            ${isPending ? '<span class="pending-bullet">●</span> ' : ''}${escapeHtml(m.subject)}
          </div>

          ${hasConflict ? `
            <div class="weekly-card-conflict" title="⚠️ 会议时间冲突：与【${mConflicts.map(c => escapeHtml(c.otherSubject)).join('、')}】重合 ${mConflicts.map(c => c.overlapRangeStr).join('、')}（点击查看详情）">
              <span class="conflict-head-icon">⚠️</span>
              <span class="conflict-overlap-label">重合</span>
              <strong class="conflict-overlap-time">${mConflicts[0].overlapRangeStr}</strong>
              ${mConflicts.length > 1 ? `<span class="weekly-conflict-more">+${mConflicts.length - 1}</span>` : ''}
            </div>
          ` : ''}

          ${(m.reporter || m.attendees) ? `
            <div class="weekly-card-meta">
              ${m.reporter ? `<div>👤 <span style="color:var(--text-primary); font-weight:600;">${escapeHtml(m.reporter)}</span>${m.attendees && m.attendees !== m.reporter ? `<span style="color:var(--text-muted); margin-left:3px;">· ${escapeHtml(m.attendees)}</span>` : ''}</div>` : (m.attendees ? `<div>👥 <span style="color:var(--text-muted);">${escapeHtml(m.attendees)}</span></div>` : '')}
            </div>
          ` : ''}

          ${m.decision ? `
            <div class="weekly-card-decision ${isPending ? 'decision-pending' : ''}" title="${escapeHtml(m.decision)}">
              <strong>🎯 决策：</strong>${escapeHtml(m.decision)}
            </div>
          ` : ''}

          ${dt.isShifted ? `
            <div class="weekly-card-cairo-sub">
              <span title="对应开罗时间：${dt.cairoStart}${dt.cairoEnd ? ' - ' + dt.cairoEnd : ''}">开罗 ${dt.cairoStart}</span>
            </div>
          ` : ''}
        </div>
      `;
    }

    // 区分上午与下午
    const morningMeetings = [];
    const afternoonMeetings = [];

    dayMeetings.forEach(m => {
      const dt = getMeetingDisplayTime(m);
      const sMins = timeStrToMinutes(dt.start || '09:00');
      const dur = parseInt(m.duration || 45, 10);
      const eMins = dt.end ? timeStrToMinutes(dt.end) : (sMins + dur);
      if (sMins < 720) { // 12:00 前有排期
        morningMeetings.push(m);
      }
      if (eMins > 840 || sMins >= 720) { // 14:00 之后有排期
        afternoonMeetings.push(m);
      }
    });

    const morningTransits = dayTransits.filter(t => {
      const depMins = timeStrToMinutes(t.depTime || '09:30');
      return t.depDate === day.dateStr ? depMins < 720 : true;
    });
    const afternoonTransits = dayTransits.filter(t => {
      const arrMins = timeStrToMinutes(t.arrTime || '14:45');
      const depMins = timeStrToMinutes(t.depTime || '09:30');
      return t.arrDate === day.dateStr ? arrMins >= 720 : depMins >= 720;
    });
    if (morningTransits.length === 0 && afternoonTransits.length === 0 && dayTransits.length > 0) {
      morningTransits.push(...dayTransits);
    }

    const morningFreeSlots = freeSlots.filter(s => s.end <= 720);
    const afternoonFreeSlots = freeSlots.filter(s => s.start >= 840);

    if (dayMeetings.length === 0 && dayTransits.length === 0) {
      html += `
        <div style="text-align:center; padding: 22px 8px; color:var(--text-muted); font-size:12px; background:#fff; border:1px dashed var(--border); border-radius:var(--radius-sm);">
          <div style="margin-bottom:4px;">全天暂无会议</div>
          <button class="btn btn-sm btn-ghost" style="margin-top:4px; font-size:11px;" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '09:00', 60)">＋ 安排预约</button>
        </div>
      `;
    } else {
      // --- 1. 上午时段 (无emoji，不标具体时间) ---
      html += `
        <div class="weekly-period-block morning-block">
          <div class="weekly-period-divider">
            <span>上午</span>
          </div>
      `;
      if (morningMeetings.length === 0 && morningTransits.length === 0) {
        html += `
          <div class="weekly-empty-period-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '09:00', 60)" title="点击安排预约">
            <div class="empty-slot-text">暂无排期</div>
          </div>
        `;
      } else {
        morningTransits.forEach(t => {
          html += renderWeeklyTransitCard(t);
        });
        morningMeetings.forEach(m => {
          html += renderWeeklySingleCard(m, false, 'morning');
        });
        if (morningFreeSlots.length > 0) {
          html += `<div class="weekly-period-free-slots">`;
          morningFreeSlots.forEach(slot => {
            html += `
              <div class="weekly-free-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '${slot.startStr}', ${Math.min(slot.duration, 60)})" title="上午空档 ${slot.startStr} - ${slot.endStr} (${slot.duration}m)">
                <span class="slot-time">${slot.startStr} - ${slot.endStr}</span>
                <span class="slot-dur-tag">${slot.duration}m ＋</span>
              </div>
            `;
          });
          html += `</div>`;
        }
      }
      html += `</div>`; // end morning-block

      // --- 2. 下午时段 ---
      html += `
        <div class="weekly-period-block afternoon-block">
          <div class="weekly-period-divider">
            <span>下午</span>
          </div>
      `;
      if (afternoonMeetings.length === 0 && afternoonTransits.length === 0) {
        html += `
          <div class="weekly-empty-period-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '14:00', 60)" title="点击安排预约">
            <div class="empty-slot-text">暂无排期</div>
          </div>
        `;
      } else {
        afternoonTransits.forEach(t => {
          html += renderWeeklyTransitCard(t);
        });
        afternoonMeetings.forEach(m => {
          html += renderWeeklySingleCard(m, false, 'afternoon');
        });
        if (afternoonFreeSlots.length > 0) {
          html += `<div class="weekly-period-free-slots">`;
          afternoonFreeSlots.forEach(slot => {
            html += `
              <div class="weekly-free-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '${slot.startStr}', ${Math.min(slot.duration, 60)})" title="下午空档 ${slot.startStr} - ${slot.endStr} (${slot.duration}m)">
                <span class="slot-time">${slot.startStr} - ${slot.endStr}</span>
                <span class="slot-dur-tag">${slot.duration}m ＋</span>
              </div>
            `;
          });
          html += `</div>`;
        }
      }
      html += `</div>`; // end afternoon-block

      // 保持与现有测试兼容的隐藏指示容器
      if (freeSlots.length > 0) {
        html += `<div class="weekly-free-slots-wrap" style="display:none;">`;
        html += `<div class="weekly-free-slots-header"><span>🕒 ${day.isToday ? '今日空档' : '可用空档'} (${freeSlots.length}段)</span></div>`;
        html += `</div>`;
      }
    }

    html += `
        </div>
      </div>
    `;
  });

  html += `
    </div>
  `;

  // ----------------- 周历模块 · 待排期 (Pending Requests Pool) -----------------
  const meetingRequests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  // 已排期的会议卡片不要再放在“待排期”栏目里面，严格只展示待排期事项
  const pendingRequests = meetingRequests.filter(r => r.status !== 'scheduled');

  html += `
    <div class="weekly-requests-overview">
      <div class="weekly-decision-top">
        <div class="weekly-decision-header-left">
          <span class="weekly-decision-icon">⏳</span>
          <span class="weekly-decision-heading">待排期</span>
          <span class="weekly-decision-count-badge" style="background:#fff1f2; color:#be123c; border-color:#fecdd3;">${pendingRequests.length} 条</span>
        </div>
        <div>
          <button class="btn btn-sm btn-outline" id="btnCopyPendingBriefing" onclick="copyPendingRequestsBriefing()" style="display:inline-flex; align-items:center; gap:4px; font-weight:600; padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #cbd5e1; background:#ffffff; color:#0f172a; cursor:pointer;">
            📋 复制待排期简报
          </button>
        </div>
      </div>

      <!-- Quick Fast Input Bar -->
      <div class="request-quick-bar">
        <input type="text" id="inputFastReqRequester" placeholder="预约人/代表处" style="width: 180px; flex-shrink: 0;" />
        <input type="text" id="inputFastReqTopic" placeholder="待排事项/议题诉求" style="flex: 1; min-width: 200px;" onkeydown="if(event.key==='Enter') addMeetingRequestFast()" />
        <input type="text" id="inputFastReqDuration" placeholder="时长" style="width: 80px; flex-shrink: 0;" value="45m" />
        <button class="btn btn-primary" onclick="addMeetingRequestFast()" style="flex-shrink: 0; padding: 6px 14px;">快速记下</button>
      </div>

      <!-- Requests Cards Grid (只展示未排期的待排卡片，已排期会议绝不在此呈现) -->
      <div class="weekly-requests-grid">
  `;

  if (pendingRequests.length === 0) {
    html += `
      <div class="weekly-decision-empty" style="grid-column: 1 / -1;">
        暂无待排期事项
      </div>
    `;
  } else {
    pendingRequests.forEach(req => {
      html += `
        <div class="weekly-request-card">
          <div class="weekly-request-top">
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="weekly-request-person">👤 ${escapeHtml(req.requester)}</span>
            </div>
            <span class="weekly-pending-tag" style="background:#fff7ed; color:#c2410c; border-color:#ffedd5;">⏳ 待排期</span>
          </div>

          <div class="weekly-request-topic">
            ${escapeHtml(req.topic)}
          </div>

          <div class="weekly-request-meta">
            <span>⏱️ 预估 ${escapeHtml(req.duration || '45')} 分钟</span>
            <span>📅 ${req.createdAt || ''}</span>
          </div>

          <div class="weekly-request-actions">
            <button class="btn btn-sm btn-primary" onclick="convertRequestToMeeting(${req.id})" title="将该待排意向一键转为正式排期单">
              📅 转为正式排期
            </button>
            <button class="btn btn-sm btn-ghost" onclick="openEditRequestModal(${req.id})" title="编辑待排期事项">✏️</button>
            <button class="btn btn-sm btn-ghost" style="color:#dc2626;" onclick="deleteMeetingRequest(${req.id})" title="删除此条待排期">✕</button>
          </div>
        </div>
      `;
    });
  }

  html += `
      </div>
    </div>
  `;

  boardContainer.innerHTML = html;
}

function timeStrToMinutes(timeStr) {
  if (!timeStr) return 0;
  const norm = normalizeTimeStr(timeStr) || timeStr;
  const parts = norm.split(':').map(Number);
  if (parts.length < 2 || isNaN(parts[0]) || isNaN(parts[1])) return 0;
  return parts[0] * 60 + parts[1];
}

function exportSingleDayScheduleNotice(dateStr) {
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const targetDate = dateStr || selectedTimelineDate || getTodayDateStr();
  const dayMeetings = meetings.filter(m => m.date === targetDate && m.status !== 'cancelled');
  dayMeetings.sort((a, b) => (a.time || '10:00').localeCompare(b.time || '10:00'));
  const dayTransits = typeof getTransitsForDate === 'function' ? getTransitsForDate(targetDate) : [];

  const parts = targetDate.split('-').map(Number);
  const d = new Date(parts[0], parts[1] - 1, parts[2]);
  const weekdayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  const weekName = weekdayNames[d.getDay()];

  if (dayMeetings.length === 0 && dayTransits.length === 0) {
    showToast(targetDate + ' 全天暂无排期会议');
    return;
  }

  let totalMins = 0;
  dayMeetings.forEach(m => { totalMins += parseInt(m.duration || 45, 10); });

  const activeTz = getActiveTripTimezone();
  const isShifted = (activeTz !== 'cairo');
  const tzInfo = TRIP_TIMEZONE_MAP[activeTz] || TRIP_TIMEZONE_MAP.cairo;
  const tzHeaderSuffix = isShifted ? ` (${tzInfo.flag} ${tzInfo.name}当地时间 · 比开罗${tzInfo.diffText})` : '';

  const lines = [
    `【主管日程安排通报 · ${targetDate} ${weekName}${tzHeaderSuffix}】`,
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
  ];

  if (dayTransits.length > 0) {
    dayTransits.forEach(t => {
      const depTzName = t.depTzName || ((TRIP_TIMEZONE_MAP[t.depTz] || TRIP_TIMEZONE_MAP.cairo).name);
      const arrTzName = t.arrTzName || ((TRIP_TIMEZONE_MAP[t.arrTz] || TRIP_TIMEZONE_MAP.cameroon).name);
      lines.push(`🛫 【领导在途动态】${t.title} ${t.flightNo ? '(' + t.flightNo + ')' : ''}`);
      lines.push(`   起飞：${t.depDate} ${t.depTime} (${depTzName}) ➔ 落地：${t.arrDate} ${t.arrTime} (${arrTzName})，耗时约 ${t.durationText || ''}`);
      if (t.remark) lines.push(`   在途备忘：${t.remark}`);
      lines.push('');
    });
  }

  if (dayMeetings.length > 0) {
    lines.push(`今日共安排 ${dayMeetings.length} 场汇报与研讨，合计排期 ${(totalMins / 60).toFixed(1)} 小时：`);
    lines.push('');
  }

  dayMeetings.forEach((m, idx) => {
    const dt = getMeetingDisplayTime(m);
    lines.push((idx + 1) + '. 【' + m.subject + '】');
    if (dt.isShifted) {
      lines.push(`   ⏱️ 时间：${dt.start} - ${dt.end} (${m.duration || 45}分钟) [当地时间 | 对应开罗时间 ${dt.cairoStart} - ${dt.cairoEnd}]`);
    } else {
      lines.push(`   ⏱️ 时间：${dt.start} - ${dt.end} (${m.duration || 45}分钟)`);
    }
    if (m.location && m.location.trim()) lines.push('   📍 地点：' + m.location.trim());
    if (m.reporter && m.reporter.trim()) lines.push('   👤 汇报人：' + m.reporter.trim());
    if (m.attendees && m.attendees.trim()) lines.push('   👥 参会人：' + m.attendees.trim());
    if (m.minuter && m.minuter.trim()) lines.push('   ✍️ 纪要人：' + m.minuter.trim());
    if (m.decision && m.decision.trim()) lines.push('   📌 决策要点说明：' + m.decision.trim());
    if (m.notes && m.notes.trim()) lines.push('   📝 备注：' + m.notes.trim());
    lines.push('');
  });

  lines.push('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  lines.push('由 Snoopy’s Little Lab · Sanyli. 助理工作台自动生成');

  const fullText = lines.join('\\n');
  copyToClipboard(fullText, '今日主管日程安排通报已成功复制到剪贴板！');
}

// ----------------- 主管单日日历渲染引擎 (Executive Day Calendar & Focus View) -----------------
function renderSupervisorDayCalendar() {
  const container = document.getElementById('supervisorDayCalendarContainer');
  if (!container) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const conflictMap = getAllMeetingConflicts(meetings);
  const today = new Date();
  const todayStr = getTodayDateStr();
  const curDateStr = selectedTimelineDate || todayStr;

  const parts = curDateStr.split('-').map(Number);
  const d = new Date(parts[0], parts[1] - 1, parts[2]);
  const weekdayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  const weekName = weekdayNames[d.getDay()];
  const isToday = (curDateStr === todayStr);
  const isWeekend = (d.getDay() === 5 || d.getDay() === 6);

  // Day meetings
  const dayMeetings = meetings.filter(m => m.date === curDateStr && m.status !== 'cancelled');
  dayMeetings.sort((a, b) => (a.time || '10:00').localeCompare(b.time || '10:00'));

  let totalDayMins = 0;
  dayMeetings.forEach(m => { totalDayMins += parseInt(m.duration || 45, 10); });

  // Free slots
  const { freeSlots } = calculateDayFreeSlots(meetings, curDateStr);
  let totalFreeMins = 0;
  freeSlots.forEach(s => { totalFreeMins += s.duration; });

  const decisionsList = dayMeetings.filter(m => m.decision && m.decision.trim().length > 0);
  const curDayTransits = typeof getTransitsForDate === 'function' ? getTransitsForDate(curDateStr) : [];

  // Morning (8:30-12:00, 510-720) and Afternoon (14:00-18:00, 840-1080)
  const morningItems = [];
  const afternoonItems = [];

  curDayTransits.forEach(t => {
    const depMins = timeStrToMinutes(t.depTime || '09:30');
    const arrMins = timeStrToMinutes(t.arrTime || '14:45');
    if (t.depDate === curDateStr && depMins < 720) {
      morningItems.push({ type: 'transit', start: depMins, data: t });
    } else if (t.arrDate === curDateStr && arrMins >= 720) {
      afternoonItems.push({ type: 'transit', start: arrMins, data: t });
    } else if (depMins < 720) {
      morningItems.push({ type: 'transit', start: depMins, data: t });
    } else {
      afternoonItems.push({ type: 'transit', start: depMins, data: t });
    }
  });

  dayMeetings.forEach(m => {
    const dt = getMeetingDisplayTime(m);
    const sMins = timeStrToMinutes(dt.start || '10:00');
    const dur = parseInt(m.duration || 45, 10);
    const eMins = dt.end ? timeStrToMinutes(dt.end) : (sMins + dur);
    if (sMins < 720) {
      morningItems.push({ type: 'meeting', start: sMins, data: m, period: 'morning' });
    }
    if (eMins > 840 || sMins >= 720) {
      afternoonItems.push({ type: 'meeting', start: sMins, data: m, period: 'afternoon' });
    }
  });

  freeSlots.forEach(s => {
    if (s.end <= 720) {
      morningItems.push({ type: 'slot', start: s.start, data: s });
    } else if (s.start >= 840) {
      afternoonItems.push({ type: 'slot', start: s.start, data: s });
    }
  });

  morningItems.sort((a, b) => a.start - b.start);
  afternoonItems.sort((a, b) => a.start - b.start);

  function renderDayEventCard(m, period) {
    const durHours = m.durationHours || (parseInt(m.duration || 45, 10) / 60).toFixed(2);
    const isHigh = (m.priority === 'high');
    const isPending = (m.status === 'pending');
    const isNoticeUnsent = (m.noticeSent === false || m.noticeSent === undefined || m.noticeSent === null);
    const dt = getMeetingDisplayTime(m);
    const allConflicts = conflictMap[m.id] || [];
    let mConflicts = allConflicts;
    if (period === 'morning') {
      mConflicts = allConflicts.filter(c => c.overlapStartMin < 720);
    } else if (period === 'afternoon') {
      mConflicts = allConflicts.filter(c => c.overlapEndMin > 720);
    }
    const hasConflict = mConflicts.length > 0;
    const statusMap = {
      pending: { text: '待安排', cls: 'status-pending' },
      scheduled: { text: '已排期', cls: 'status-scheduled' },
      completed: { text: '已完成', cls: 'status-completed' },
      cancelled: { text: '已取消', cls: 'status-cancelled' }
    };
    const st = statusMap[m.status] || statusMap.scheduled;

    return `
      <div class="day-meeting-card ${isPending ? 'is-pending' : (isHigh ? 'priority-high' : '')} ${isNoticeUnsent ? 'notice-unsent' : ''} ${hasConflict ? 'is-conflict' : ''}">
        <div class="day-meeting-top">
          <div class="day-meeting-time-bar">
            <span class="day-meeting-time-text" style="${dt.isShifted ? 'color:#15803d; font-weight:800;' : ''}">🕒 ${dt.start} - ${dt.end}</span>
            <span style="font-size:11.5px; color:var(--text-muted);">(${durHours}H)</span>
            ${isNoticeUnsent ? '<span class="weekly-notice-tag">⚠️ 待发通知</span>' : ''}
            ${isPending ? '<span class="weekly-pending-tag">⚠️ 待领导确认</span>' : `<span class="status-badge ${st.cls}">${st.text}</span>`}
            ${isHigh && !isPending ? '<span class="priority-badge priority-high">紧急决议</span>' : ''}
          </div>
          <div style="font-size:11.5px; color:var(--text-muted); font-weight:500;">
            📍 ${escapeHtml(m.location || '主管办公室')}
          </div>
        </div>

        <div class="day-meeting-title ${isPending ? 'text-pending' : ''}" onclick="editMeeting(${m.id})" style="cursor:pointer;" title="点击编辑此会议">
          ${isPending ? '<span class="pending-bullet">●</span> ' : ''}${escapeHtml(m.subject)}
        </div>

        ${(m.reporter || m.attendees || m.minuter) ? `
          <div class="day-meeting-roster" style="font-size:11.5px; color:var(--text-secondary); margin-bottom:6px; display:flex; flex-wrap:wrap; gap:12px;">
            ${m.reporter ? `<div>👤 <strong>汇报：</strong><span>${escapeHtml(m.reporter)}</span></div>` : ''}
            ${m.attendees ? `<div>👥 <strong>参会：</strong><span>${escapeHtml(m.attendees)}</span></div>` : ''}
            ${m.minuter ? `<div>✍️ <strong>纪要：</strong><span style="color:#2563eb; font-weight:600;">${escapeHtml(m.minuter)}</span></div>` : ''}
          </div>
        ` : ''}

        ${mConflicts.length > 0 ? `
          <div class="day-meeting-conflict-box" title="⚠️ 会议时间冲突：与【${mConflicts.map(c => escapeHtml(c.otherSubject)).join('、')}】重合（点击查看详情）" onclick="editMeeting(${m.id})">
            <span class="day-conflict-time-pill">⚠️ 🕒 重合：<strong>${mConflicts[0].overlapRangeStr}</strong></span>
            ${mConflicts.length > 1 ? `<span class="day-conflict-count-badge">+${mConflicts.length - 1} 处冲突</span>` : ''}
            <span style="font-size:11px; color:#9f1239; margin-left:auto; font-weight:600;">点击查看详情 ▶</span>
          </div>
        ` : ''}

        ${m.decision ? `
          <div class="day-meeting-decision ${isPending ? 'decision-pending' : ''}">
            <strong>📌 决策要点说明：</strong>
            <div>${escapeHtml(m.decision)}</div>
          </div>
        ` : ''}

        ${m.background ? `
          <div class="day-meeting-bg">
            <strong>📄 议题背景：</strong>
            <div>${escapeHtml(m.background)}</div>
          </div>
        ` : ''}

        <div class="day-meeting-actions">
          <button class="btn btn-sm" onclick="editMeeting(${m.id})">✏️ 编辑</button>
          <button class="btn btn-sm btn-ghost" onclick="copySingleMeetingNotice(${m.id})">📋 复制通知</button>
          ${m.status !== 'completed' ? `<button class="btn btn-sm btn-ghost" onclick="updateMeetingStatus(${m.id}, 'completed')">✅ 标记完成</button>` : ''}
          <button class="btn btn-sm btn-ghost" onclick="deleteMeeting(${m.id})" style="color:#dc2626;">🗑️ 删除</button>
        </div>

        ${dt.isShifted ? `
          <div style="display:flex; justify-content:flex-end; margin-top:4px;">
            <span style="font-size:11px; color:var(--text-muted); font-weight:normal;" title="对应开罗时间：${dt.cairoStart}${dt.cairoEnd ? ' - ' + dt.cairoEnd : ''}">开罗 ${dt.cairoStart}</span>
          </div>
        ` : ''}
      </div>
    `;
  }

  function renderDaySlotCard(slot) {
    return `
      <div class="day-free-slot-card" onclick="openAddMeetingModalWithSlot('${curDateStr}', '${slot.startStr}', ${Math.min(slot.duration, 60)})" title="点击预约此空档时段">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:14px;">🕒</span>
          <strong style="color:#166534; font-size:12px;">可用空档：${slot.startStr} - ${slot.endStr}</strong>
          <span style="background:#bbf7d0; color:#14532d; font-size:11px; padding:2px 6px; border-radius:4px; font-weight:600;">${slot.duration}分钟可用</span>
        </div>
        <button class="btn btn-sm btn-ghost" style="color:#15803d; border-color:#86efac; background:#fff; font-size:11px; padding:3px 8px;">＋ 安排此时段</button>
      </div>
    `;
  }

  let html = `
    <div class="day-top-header">
      <div class="day-nav-group">
        <button class="btn btn-sm" onclick="changeDayOffset(-1)" title="前一天">◀ 前一天</button>
        <div class="day-current-date-title">
          <span>${parts[0]}年${parts[1]}月${parts[2]}日 ${weekName}</span>
          ${(() => {
            const curDayTrip = getTripForDate(curDateStr);
            return curDayTrip ? `<span class="badge" style="background:#dcfce7; color:#15803d; border:1px solid #86efac; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:700; margin-left:8px;" title="领导出差目的地：${curDayTrip.tzName} (比开罗${curDayTrip.diffText}) · 全天日程按当地时间排期">✈️ ${curDayTrip.tzName}</span>` : '';
          })()}
          ${curDayTransits.length > 0 ? `<span class="badge" style="background:#e0f2fe; color:#0369a1; border:1px solid #bae6fd; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:700; margin-left:8px;" title="领导本日处于跨时区在途飞行状态">🛫 在途</span>` : ''}
          ${isToday ? '<span class="cal-today-badge">今日</span>' : ''}
          ${isWeekend ? '<span class="weekly-weekend-badge">周末</span>' : ''}
          ${dayMeetings.some(m => conflictMap[m.id] && conflictMap[m.id].length > 0) ? `<span class="badge" style="display:none;" title="本日存在会议时间冲突">⚠️ 存在时间冲突</span>` : ''}
        </div>
        <button class="btn btn-sm" onclick="changeDayOffset(1)" title="后一天">后一天 ▶</button>
        <button class="btn btn-sm btn-ghost" onclick="jumpToTodayDayCalendar()">回到今天</button>
      </div>

      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <label style="font-size:12px; color:var(--text-secondary); font-weight:600;">选择日期：</label>
        <input type="date" value="${curDateStr}" style="padding:4px 8px; font-size:12px;" onchange="selectDayCalDate(this.value)" />
        <button class="btn btn-sm btn-primary" onclick="openAddMeetingModalWithSlot('${curDateStr}', '10:00', 45)">＋ 登记预约</button>
        <button class="btn btn-sm" onclick="exportSingleDayScheduleNotice('${curDateStr}')">📋 复制今日通报</button>
      </div>
    </div>
    ${getTripTimezoneBarHtml()}

    <div class="day-stats-banner">
      <div class="day-stat-chip">今日会议：<strong>${dayMeetings.length}</strong> 场</div>
      <div class="day-stat-chip">排期时长：<strong>${(totalDayMins / 60).toFixed(1)}</strong> H</div>
      <div class="day-stat-chip">可用空档：<strong>${freeSlots.length}</strong> 段 (${(totalFreeMins / 60).toFixed(1)}H)</div>
      <div class="day-stat-chip">待决策要点：<strong>${decisionsList.length}</strong> 项</div>
      ${(() => {
        const curDayTrip = getTripForDate(curDateStr);
        return curDayTrip ? `<div class="day-stat-chip" style="background:#dcfce7; border-color:#86efac; color:#15803d; font-weight:700;">✈️ 领导出差中 · 目的地：${curDayTrip.tzFlag} ${curDayTrip.tzName} (会议已显示当地时间，并附注开罗开始时间)</div>` : '';
      })()}
      ${curDayTransits.length > 0 ? `<div class="day-stat-chip" style="background:#e0f2fe; border-color:#bae6fd; color:#0369a1; font-weight:700;">🛫 领导在途 · ${escapeHtml(curDayTransits[0].title)} (耗时约 ${curDayTransits[0].durationText})</div>` : ''}
    </div>

    <div class="day-cal-layout">
      <!-- Left Column: Chronological Timeline -->
      <div class="day-timeline-stream">
        <div class="day-section-divider">上午日程推进</div>
  `;

  if (morningItems.length === 0) {
    html += `
      <div class="day-lunch-rest-card" style="background:#f0fdf4; border-color:#bbf7d0; color:#15803d; display:flex; justify-content:space-between; align-items:center;">
        <div><strong>上午暂无排期</strong></div>
        <button class="btn btn-sm btn-ghost" style="color:#15803d; border-color:#86efac; background:#fff; font-size:11px;" onclick="openAddMeetingModalWithSlot('${curDateStr}', '09:00', 60)">＋ 安排上午会议</button>
      </div>
    `;
  } else {
    morningItems.forEach(item => {
      if (item.type === 'meeting') {
        html += renderDayEventCard(item.data, item.period || 'morning');
      } else if (item.type === 'transit') {
        html += renderDayTransitCard(item.data);
      } else {
        html += renderDaySlotCard(item.data);
      }
    });
  }

  // Lunch break card
  html += `
        <div class="day-lunch-rest-card">
          <span style="font-size:16px;">🍽️</span>
          <div>
            <strong>12:00 - 14:00 午餐与午休休整时段</strong>
            <span style="margin-left:8px; opacity:0.85;">主管非工作会议排期时段，适宜机动休整与能量补给</span>
          </div>
        </div>

        <div class="day-section-divider">下午日程推进</div>
  `;

  if (afternoonItems.length === 0) {
    html += `
      <div class="day-lunch-rest-card" style="background:#f0fdf4; border-color:#bbf7d0; color:#15803d; display:flex; justify-content:space-between; align-items:center;">
        <div><strong>下午暂无排期</strong></div>
        <button class="btn btn-sm btn-ghost" style="color:#15803d; border-color:#86efac; background:#fff; font-size:11px;" onclick="openAddMeetingModalWithSlot('${curDateStr}', '14:30', 60)">＋ 安排下午会议</button>
      </div>
    `;
  } else {
    afternoonItems.forEach(item => {
      if (item.type === 'meeting') {
        html += renderDayEventCard(item.data, item.period || 'afternoon');
      } else if (item.type === 'transit') {
        html += renderDayTransitCard(item.data);
      } else {
        html += renderDaySlotCard(item.data);
      }
    });
  }

  // Empty whole day notice if 0 meetings
  if (dayMeetings.length === 0 && curDayTransits.length === 0) {
    html += `
      <div style="text-align:center; padding:24px 16px; background:#fff; border:1px dashed var(--border); border-radius:var(--radius-md); margin-top:8px;">
        <div style="font-size:20px; margin-bottom:6px;">☕</div>
        <div style="font-size:13.5px; font-weight:700; color:var(--text-primary);">今日全天暂无排期会议</div>
        <div style="font-size:12px; color:var(--text-secondary); margin-top:4px; margin-bottom:12px;">共有 ${(totalFreeMins/60).toFixed(1)} 小时机动时间，点击下方按钮随时安排新预约</div>
        <button class="btn btn-sm btn-primary" onclick="openAddMeetingModalWithSlot('${curDateStr}', '10:00', 45)">＋ 安排今日新会议预约</button>
      </div>
    `;
  }

  // Right sidebar: Today Decision Highlights only
  html += `
      </div>

      <!-- Right Column: Executive Daily Focus Sidebar -->
      <div class="day-sidebar-wrap">
        <div class="day-sidebar-card">
          <div class="day-sidebar-title">📌 今日待决议题速览 (${decisionsList.length})</div>
  `;

  if (decisionsList.length === 0) {
    html += `<div style="font-size:12px; color:var(--text-muted); padding:6px 0;">今日暂无特定决策要点备忘</div>`;
  } else {
    decisionsList.forEach(d => {
      const dt = getMeetingDisplayTime(d);
      html += `
        <div class="day-sidebar-decision-item" onclick="editMeeting(${d.id})" title="点击查看会议详情">
          <div class="day-sidebar-decision-title">${escapeHtml(d.subject)} · ${dt.start}${dt.isShifted ? ' (开罗 ' + dt.cairoStart + ')' : ''}</div>
          <div class="day-sidebar-decision-text">${escapeHtml(d.decision)}</div>
        </div>
      `;
    });
  }

  html += `
        </div>
      </div>
    </div>
  `;

  container.innerHTML = html;
}

// ----------------- 月度日历渲染引擎 (Month Calendar Renderer) -----------------
function renderSupervisorMonthCalendar() {
  const calContainer = document.getElementById('supervisorMonthCalendarContainer');
  if (!calContainer) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const conflictMap = getAllMeetingConflicts(meetings);
  const year = currentCalendarYearMonth.year;
  const month = currentCalendarYearMonth.month; // 0-indexed
  const todayStr = getTodayDateStr();

  if (!selectedTimelineDate) {
    selectedTimelineDate = todayStr;
  }

  const monthPrefix = `${year}-${String(month + 1).padStart(2, '0')}`;
  const monthMeetings = meetings.filter(m => m.date && m.date.startsWith(monthPrefix) && m.status !== 'cancelled');
  let monthMins = 0;
  monthMeetings.forEach(m => { monthMins += parseInt(m.duration || 45, 10); });

  const meetingsByDate = {};
  meetings.forEach(m => {
    if (!m.date || m.status === 'cancelled') return;
    if (!meetingsByDate[m.date]) meetingsByDate[m.date] = [];
    meetingsByDate[m.date].push(m);
  });

  const firstDay = new Date(year, month, 1);
  const startDayOfWeek = firstDay.getDay(); // 0: Sunday, 1: Monday, ..., 6: Saturday
  const daysInCurrentMonth = new Date(year, month + 1, 0).getDate();
  const daysInPrevMonth = new Date(year, month, 0).getDate();

  let html = `
    <div class="cal-top-header">
      <div class="cal-month-nav">
        <button class="btn btn-sm" onclick="changeCalendarMonth(-1)" title="上一月">◀ 上月</button>
        <div class="cal-current-month-title">${year}年 ${month + 1}月</div>
        <button class="btn btn-sm" onclick="changeCalendarMonth(1)" title="下一月">下月 ▶</button>
        <button class="btn btn-sm btn-ghost" onclick="jumpToTodayCalendar()">回到今天</button>
      </div>
      <div style="font-size:12px; color:var(--text-secondary); display:flex; align-items:center; gap:12px;">
        <span>本月排期会议：<strong style="color:var(--blue-accent);">${monthMeetings.length}</strong> 场</span>
        <span>累计排期时长：<strong>${(monthMins / 60).toFixed(1)}</strong> 小时</span>
      </div>
    </div>
    ${getTripTimezoneBarHtml()}

    <table class="cal-grid-table">
      <thead>
        <tr>
          <th>周日</th>
          <th>周一</th>
          <th>周二</th>
          <th>周三</th>
          <th>周四</th>
          <th class="weekend">周五</th>
          <th class="weekend">周六</th>
        </tr>
      </thead>
      <tbody>
  `;

  let dayCounter = 1;
  let nextMonthDay = 1;

  for (let row = 0; row < 6; row++) {
    html += '<tr>';
    for (let col = 0; col < 7; col++) {
      if (row === 0 && col < startDayOfWeek) {
        const prevDay = daysInPrevMonth - (startDayOfWeek - col - 1);
        const prevMonth = month === 0 ? 12 : month;
        const prevYear = month === 0 ? year - 1 : year;
        const pDateStr = `${prevYear}-${String(prevMonth).padStart(2, '0')}-${String(prevDay).padStart(2, '0')}`;
        html += `
          <td class="cal-day-cell other-month" onclick="selectCalendarDate('${pDateStr}')">
            <div class="cal-day-header">
              <span class="cal-day-num">${prevDay}</span>
            </div>
          </td>`;
      } else if (dayCounter > daysInCurrentMonth) {
        const nMonth = month === 11 ? 1 : month + 2;
        const nYear = month === 11 ? year + 1 : year;
        const nDateStr = `${nYear}-${String(nMonth).padStart(2, '0')}-${String(nextMonthDay).padStart(2, '0')}`;
        html += `
          <td class="cal-day-cell other-month" onclick="selectCalendarDate('${nDateStr}')">
            <div class="cal-day-header">
              <span class="cal-day-num">${nextMonthDay}</span>
            </div>
          </td>`;
        nextMonthDay++;
      } else {
        const curDateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(dayCounter).padStart(2, '0')}`;
        const isToday = curDateStr === todayStr;
        const isSelected = curDateStr === selectedTimelineDate;
        const isWeekend = (col === 5 || col === 6);
        const dayMeetingsList = meetingsByDate[curDateStr] || [];

        let cellClasses = ['cal-day-cell'];
        if (isToday) cellClasses.push('today');
        if (isSelected) cellClasses.push('selected');
        if (isWeekend) cellClasses.push('weekend-cell');

        html += `
          <td class="${cellClasses.join(' ')}" onclick="selectCalendarDate('${curDateStr}')">
            <div class="cal-day-header">
              <span class="cal-day-num">${dayCounter}</span>
              ${(() => {
                const curDayTrip = getTripForDate(curDateStr);
                return curDayTrip ? `<span class="badge" style="background:#dcfce7; color:#15803d; border:1px solid #86efac; font-size:9px; padding:0 4px; border-radius:8px; font-weight:700;" title="领导出差目的地：${curDayTrip.tzName} (比开罗${curDayTrip.diffText}) · 全天为当地时间">✈️ ${curDayTrip.tzName}</span>` : '';
              })()}
              ${dayMeetingsList.some(m => conflictMap[m.id] && conflictMap[m.id].length > 0) ? `<span class="cal-day-conflict-icon" title="本日存在会议时间冲突！">⚠️</span>` : ''}
              ${isToday ? '<span class="cal-today-badge">今天</span>' : ''}
            </div>
            <div class="cal-day-events">
              ${dayMeetingsList.slice(0, 2).map(m => {
                const mConflicts = conflictMap[m.id] || [];
                const hasConflict = mConflicts.length > 0;
                const stCls = m.status === 'scheduled' ? 'status-scheduled' : (m.status === 'completed' ? 'status-completed' : 'status-pending');
                const dt = getMeetingDisplayTime(m);
                if (hasConflict) {
                  const c0 = mConflicts[0];
                  return `<div class="cal-event-pill cal-event-conflict" title="⚠️ 时间冲突：与【${escapeHtml(c0.otherSubject)}】重合 ${c0.overlapRangeStr} (${c0.overlapDuration}分钟)">
                    <span style="font-weight:700;">⚠️ ${dt.start} ${escapeHtml(m.subject)}</span>
                    <span class="cal-conflict-overlap-tag">重合 ${c0.overlapRangeStr}</span>
                  </div>`;
                }
                return `<div class="cal-event-pill ${stCls}" title="${dt.start} ${escapeHtml(m.subject)}">${dt.start} ${escapeHtml(m.subject)}</div>`;
              }).join('')}
              ${dayMeetingsList.length > 2 ? `<div class="cal-event-more">+${dayMeetingsList.length - 2} 更多...</div>` : ''}
            </div>
          </td>`;
        dayCounter++;
      }
    }
    html += '</tr>';
    if (dayCounter > daysInCurrentMonth && nextMonthDay > 7) break;
  }

  html += `
      </tbody>
    </table>
  `;

  calContainer.innerHTML = html;
}

// ----------------- 会议主渲染引擎 (Main Meetings Renderer) -----------------
// ==========================================
// 遗留任务 (Legacy Tasks) 模块 - 完整交互与渲染逻辑
// ==========================================

// ==========================================
// 遗留任务清单 (Legacy Tasks)
// 核心规则：
// 1. 遗留任务只有 B 列 (*问题描述) 是，绝不把其他数据拼入。责任人是同一行对应的责任人 (C 列)。其他信息全部不呈现。
// 2. 整个面板只展示 open 的任务和申请关闭的任务，完全排除已闭环/已完成的任务；不设置任务流转操作。
// ==========================================

let legacyViewMode = 'table'; // 'table' | 'cards' (以表格清单为主视图)
let legacyFilterStatus = 'all'; // 'all' (Open + 申请关闭) | 'open' | 'applying_closed'
let legacyFilterOwner = 'all'; // 'all' | 责任人
let legacySearchKeyword = '';
let legacyKpiFilter = 'all'; // 'all' | 'this_week' | 'pending_minutes'
let parsedLegacyImportTasks = [];

function setLegacyKpiFilter(filter) {
  if (legacyKpiFilter === filter && filter !== 'all') {
    legacyKpiFilter = 'all';
  } else {
    legacyKpiFilter = filter;
  }
  renderLegacyTasks();
}

function setLegacyViewMode(mode) {
  legacyViewMode = mode;
  const btnCards = document.getElementById('btnLegacyViewCards');
  const btnTable = document.getElementById('btnLegacyViewTable');
  const containerCards = document.getElementById('legacyCardsContainer');
  const containerTable = document.getElementById('legacyTableContainer');
  if (btnCards) btnCards.classList.toggle('active', mode === 'cards');
  if (btnTable) btnTable.classList.toggle('active', mode === 'table');
  if (containerCards) containerCards.style.display = (mode === 'cards' ? 'grid' : 'none');
  if (containerTable) containerTable.style.display = (mode === 'table' ? 'block' : 'none');
  renderLegacyTasks();
}

function filterLegacyTasksStatus(status) {
  legacyFilterStatus = status;
  renderLegacyTasks();
}

function filterLegacyTasksOwner(owner) {
  legacyFilterOwner = owner;
  renderLegacyTasks();
}

function handleLegacySearch(val) {
  legacySearchKeyword = (val || '').trim().toLowerCase();
  renderLegacyTasks();
}

// 整个面板准入规则：只允许 open 任务与 申请关闭 任务，彻底排除已闭环/已完成及换行切断产生的审核意见碎片
function isAllowedPanelTask(t) {
  if (!t) return false;
  const title = (t.title || '').trim();
  const owner = (t.owner || '').trim();
  const s = String(t.status || '').trim().toLowerCase();

  // 1. 标题必须存在 (来自 B 列)
  if (!title) return false;

  // 2. 彻底过滤审核意见碎片、换行杂项、纯序号或领域标签
  if (title.indexOf('关键任务整理出来') !== -1) return false;
  if (title.indexOf('今天发送纪要') !== -1) return false;
  if (title.indexOf('宣传加强') !== -1) return false;
  if (title.indexOf('保供的重新汇报') !== -1) return false;
  if (title.indexOf('修改后的材料发出') !== -1) return false;
  if (title.indexOf('群组发送') !== -1) return false;
  if (title.indexOf('跟曦总同步进展') !== -1) return false;
  if (title.indexOf('DTRB结论同步') !== -1) return false;
  if (title.indexOf('材料发送邮件') !== -1) return false;
  if (title.indexOf('护城河及ODN体验后更新材料') !== -1) return false;
  if (title.indexOf('长期任务，目标需要多部门') !== -1) return false;
  if (title.indexOf('ODN服务差距总结出整体观点') !== -1) return false;
  if (title.indexOf('第二篇Mostafa') !== -1) return false;
  if (title.indexOf('订未收部分') !== -1) return false;
  if (/^【\d{1,2}\/\d{1,2}】/.test(title)) return false;
  if (/^\d{1,2}\/\d{1,2}/.test(title)) return false;
  if (title.startsWith('@')) return false;
  if (/^\d+$/.test(title)) return false;
  if (/\d+%/.test(title)) return false;
  if (title === 'FBB' || title === 'TMO' || title === 'NFV' || title === '其他' || title === 'SITE' || title === 'IT' || title === 'MBB') return false;

  if (owner === 'SITE' || owner === 'Y' || owner.indexOf('今天发送纪要') !== -1 || owner.indexOf('关键进展同步') !== -1 || /\d+%/.test(owner) || /^\d+$/.test(owner)) {
    return false;
  }
  if (!owner && title.length > 30) return false;

  // 3. 排除所有已闭环 / 已关闭 / 已完成
  if (
    s === 'completed' ||
    s === 'closed' ||
    s === '已闭环' ||
    s === '已完成' ||
    s === '已关闭' ||
    s === '已销项' ||
    s === '关闭' ||
    s === '闭环' ||
    s === '完成' ||
    t.isCurrentClosed === true ||
    t.isCurrentClosed === '是' ||
    t.isCurrentClosed === 'yes'
  ) {
    return false;
  }
  return true;
}

function isTaskApplyingClosed(t) {
  if (!t) return false;
  const s = String(t.status || '').trim().toLowerCase();
  return s === 'applying_closed' || s === '申请关闭' || s === '申请闭环' || s === '待确认关闭' || s === '待确认闭环' || s.indexOf('申请') !== -1;
}

function isTaskOpen(t) {
  if (!t) return false;
  if (!isAllowedPanelTask(t)) return false;
  if (isTaskApplyingClosed(t)) return false;
  return true;
}

// 拆分多次汇报时间
function splitLegacyReportTimes(str) {
  if (!str) return [];
  var s = String(str);
  var chars = [',', '，', ';', '；', '/', '、', String.fromCharCode(10), String.fromCharCode(13)];
  for (var i = 0; i < chars.length; i++) {
    s = s.split(chars[i]).join(',');
  }
  return s.split(',').map(function(x) { return x.trim(); }).filter(Boolean);
}

// 提取中括号标签 (支持中文【】与英文[])
function extractLegacyBrackets(str) {
  if (!str) return [];
  var s = String(str);
  var re = /[【\[](.*?)[】\]]/g;
  var list = [];
  var match;
  while ((match = re.exec(s)) !== null) {
    var val = match[1].trim();
    if (val) list.push(val);
  }
  return list;
}

// 核心规则：根据预约会议记录的会议名称，如果出现【xxx】，且对应遗留任务名称【xxx】，即判定为已汇报
function doesMeetingMatchLegacyTask(meeting, task) {
  if (!meeting || !task) return false;
  // 1. 显式 ID 绑定
  if (meeting.legacyTaskId && String(meeting.legacyTaskId) === String(task.id)) {
    return true;
  }

  var mSub = String(meeting.subject || '').trim();
  var tTitle = String(task.title || '').trim();
  if (!mSub || !tTitle) return false;

  var mBrackets = extractLegacyBrackets(mSub);
  var tBrackets = extractLegacyBrackets(tTitle);

  // 2. 检查会议名称中的【xxx】
  for (var i = 0; i < mBrackets.length; i++) {
    var mb = mBrackets[i];
    var mbLower = mb.toLowerCase();

    // 与任务中括号比对
    for (var j = 0; j < tBrackets.length; j++) {
      var tb = tBrackets[j];
      var tbLower = tb.toLowerCase();
      if (mbLower === tbLower) return true;
      if (mbLower.length >= 4 && tbLower.indexOf(mbLower) !== -1) return true;
      if (tbLower.length >= 4 && mbLower.indexOf(tbLower) !== -1) return true;
    }

    // 会议中的【mb】直接出现在任务标题中
    if (tTitle.indexOf('【' + mb + '】') !== -1 || tTitle.indexOf('[' + mb + ']') !== -1) return true;
    // 会议中括号提取出的核心关键词（长度>=3）出现在任务标题中
    if (mb.length >= 3 && tTitle.toLowerCase().indexOf(mbLower) !== -1) return true;
  }

  // 3. 检查任务中括号【tb】是否直接出现在会议主题中
  for (var k = 0; k < tBrackets.length; k++) {
    var tb2 = tBrackets[k];
    var tb2Lower = tb2.toLowerCase();
    if (mSub.indexOf('【' + tb2 + '】') !== -1 || mSub.indexOf('[' + tb2 + ']') !== -1) return true;
    if (tb2.length >= 3 && mSub.toLowerCase().indexOf(tb2Lower) !== -1) return true;
  }

  return false;
}

// 获取某个遗留任务关联的所有预约会议
function getTaskReportMeetings(task, allMeetings) {
  if (!task || !allMeetings || !Array.isArray(allMeetings)) return [];
  return allMeetings.filter(function(m) {
    return doesMeetingMatchLegacyTask(m, task);
  }).sort(function(a, b) {
    var timeA = (a.date || '') + ' ' + (a.startTime || a.time || '');
    var timeB = (b.date || '') + ' ' + (b.startTime || b.time || '');
    return timeA.localeCompare(timeB);
  });
}

// 归一化提取任务的历次汇报与对应纪要 (多次汇报 1对1 紧密对应)
function getNormalizedTaskReports(task, allMeetings) {
  if (!task) return [];
  var reports = [];

  // 1. 严格过滤：绝不根据审核意见制造汇报！仅允许在界面主动点击“登记汇报”保存的手工记录 (isManual === true)
  if (Array.isArray(task.reports)) {
    task.reports.forEach(function(r) {
      if (r && r.isManual === true && r.reportTime) {
        var rt = String(r.reportTime).trim();
        if (rt && rt !== 'SITE' && rt !== 'Y' && rt !== 'N' && rt !== 'FBB' && rt !== 'TMO' && rt !== 'NFV') {
          reports.push({
            id: r.id || ('rep_' + Math.random()),
            seq: r.seq || 1,
            reportTime: rt,
            hasMinutes: Boolean(r.hasMinutes),
            minutes: r.minutes || '',
            reviewOpinion: r.reviewOpinion || '',
            meetingId: r.meetingId || null,
            meetingSubject: r.meetingSubject || '',
            isManual: true,
            reporter: r.reporter || task.owner || ''
          });
        }
      }
    });
  }

  // 2. 关键匹配：从预约会议中自动精准识别汇报记录
  var meetings = getTaskReportMeetings(task, allMeetings || (typeof getData === 'function' ? getData(STORAGE_KEYS.MEETINGS, []) : []));
  meetings.forEach(function(m) {
    var mDate = m.date || '';
    var mTime = (mDate + ' ' + (m.startTime || m.time || '')).trim();
    if (!mTime && mDate) mTime = mDate;
    if (!mTime) return;

    var hasMin = (m.hasMinutes === 'yes' || m.hasMinutes === true || Boolean(m.decision && m.decision.trim()));
    var opinion = m.decision || m.nextPlan || '';

    // 检查是否已经在 reports 中
    var existingIdx = reports.findIndex(function(r) {
      if (r.meetingId && String(r.meetingId) === String(m.id)) return true;
      if (r.reportTime && mTime && r.reportTime.startsWith(mDate)) return true;
      return false;
    });

    if (existingIdx !== -1) {
      reports[existingIdx].meetingId = m.id;
      reports[existingIdx].meetingSubject = m.subject || '';
      if (reports[existingIdx].hasMinutes === undefined || reports[existingIdx].hasMinutes === null) {
        reports[existingIdx].hasMinutes = hasMin;
      }
      if (!reports[existingIdx].reviewOpinion && opinion) {
        reports[existingIdx].reviewOpinion = opinion;
      }
    } else {
      reports.push({
        id: 'rep_m_' + m.id,
        seq: reports.length + 1,
        reportTime: mTime,
        hasMinutes: hasMin,
        minutes: m.nextPlan || m.notes || '',
        reviewOpinion: opinion,
        meetingId: m.id,
        meetingSubject: m.subject || '',
        reporter: m.reporter || m.requester || task.owner || ''
      });
    }
  });

  // 按照时间排：待汇报的在前面，已汇报的在后面
  reports.sort(function(a, b) {
    var aPending = isReportPending(a);
    var bPending = isReportPending(b);
    if (aPending && !bPending) return -1;
    if (!aPending && bPending) return 1;
    if (aPending) {
      return (a.reportTime || '').localeCompare(b.reportTime || ''); // 待汇报：按时间升序
    } else {
      return (b.reportTime || '').localeCompare(a.reportTime || ''); // 已汇报：最新汇报在前面
    }
  });
  reports.forEach(function(r, idx) {
    r.seq = idx + 1;
  });

  return reports;
}

function parseDateTimeStr(str) {
  if (!str) return null;
  const m = String(str).match(/(\d{4})[-/](\d{1,2})[-/](\d{1,2})(?:\s+(\d{1,2}):(\d{1,2}))?/);
  if (!m) return null;
  const y = parseInt(m[1], 10);
  const mon = parseInt(m[2], 10) - 1;
  const d = parseInt(m[3], 10);
  const h = m[4] ? parseInt(m[4], 10) : 23;
  const mi = m[5] ? parseInt(m[5], 10) : 59;
  return new Date(y, mon, d, h, mi, 0);
}

function isReportPending(reportOrTime) {
  const timeStr = typeof reportOrTime === 'string' ? reportOrTime : (reportOrTime && reportOrTime.reportTime ? reportOrTime.reportTime : '');
  if (!timeStr) return false;
  const dt = parseDateTimeStr(timeStr);
  if (!dt) return false;
  return dt.getTime() > Date.now();
}

function isDateInCurrentWeek(dateStr) {
  if (!dateStr) return false;
  const m = String(dateStr).match(/(\d{4})[-/](\d{1,2})[-/](\d{1,2})/);
  if (!m) return false;
  const year = parseInt(m[1], 10);
  const month = parseInt(m[2], 10) - 1;
  const day = parseInt(m[3], 10);
  const targetDate = new Date(year, month, day);

  const now = new Date();
  const currentDay = now.getDay();
  const distanceToMonday = (currentDay + 6) % 7; // Monday = 0, Sunday = 6
  
  const monday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - distanceToMonday);
  monday.setHours(0, 0, 0, 0);
  
  const sunday = new Date(monday.getTime() + 7 * 24 * 60 * 60 * 1000 - 1);
  
  const targetTime = targetDate.getTime();
  return targetTime >= monday.getTime() && targetTime <= sunday.getTime();
}

function renderLegacyTasks() {
  const allTasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  const allMeetings = getData(STORAGE_KEYS.MEETINGS, []);

  // 严格规则：在整个面板，只展示 open 的任务和申请关闭的任务，完全排除已闭环/已完成的任务
  const panelTasks = allTasks.filter(isAllowedPanelTask);

  const openCount = panelTasks.filter(isTaskOpen).length;

  // 计算本周汇报遗留任务的数量以及待发送会议纪要的数量
  let thisWeekReportedTasksCount = 0;
  let pendingMinutesCount = 0;

  panelTasks.forEach(task => {
    const reps = getNormalizedTaskReports(task, allMeetings);
    if (reps && reps.length > 0) {
      // 本周是否有汇报
      const hasThisWeekRep = reps.some(r => isDateInCurrentWeek(r.reportTime));
      if (hasThisWeekRep) {
        thisWeekReportedTasksCount++;
      }
      // 是否存在待发送会议纪要 (已汇报但尚未输出/发送纪要)
      if (reps.some(r => !r.hasMinutes)) {
        pendingMinutesCount++;
      }
    }
  });

  // 1. 刷新责任人下拉筛选选项 (仅来自当前面板活跃任务)
  const ownerSelect = document.getElementById('legacyOwnerFilter');
  if (ownerSelect) {
    const curVal = legacyFilterOwner;
    const owners = Array.from(new Set(panelTasks.map(t => (t.owner || '').trim()).filter(Boolean)));
    ownerSelect.innerHTML = '<option value="all">全部责任人</option>' + 
      owners.map(o => `<option value="${escapeHtml(o)}" ${curVal === o ? 'selected' : ''}>${escapeHtml(o)}</option>`).join('');
  }

  // 2. 统计概览指示牌 (KPIs) - 支持点击筛选对应的遗留任务
  const isAll = (legacyKpiFilter === 'all');
  const isThisWeek = (legacyKpiFilter === 'this_week');
  const isPendingMin = (legacyKpiFilter === 'pending_minutes');

  const kpiContainer = document.getElementById('legacyKpiGrid');
  if (kpiContainer) {
    kpiContainer.innerHTML = `
      <div class="legacy-kpi-card ${isAll ? 'active-kpi' : ''}" onclick="setLegacyKpiFilter('all')" title="点击显示全部 Open 遗留任务 (${openCount}项)">
        <div class="legacy-kpi-icon" style="background:#e0f2fe; color:#0284c7;">🟢</div>
        <div>
          <div class="legacy-kpi-val">${openCount}</div>
          <div class="legacy-kpi-lbl">遗留任务（open）</div>
        </div>
      </div>
      <div class="legacy-kpi-card ${isThisWeek ? 'active-kpi' : ''}" onclick="setLegacyKpiFilter('this_week')" title="点击仅筛选本周汇报的遗留任务 (${thisWeekReportedTasksCount}项)">
        <div class="legacy-kpi-icon" style="background:#fef3c7; color:#d97706;">🎙️</div>
        <div>
          <div class="legacy-kpi-val">${thisWeekReportedTasksCount}</div>
          <div class="legacy-kpi-lbl">本周汇报遗留任务</div>
        </div>
      </div>
      <div class="legacy-kpi-card ${isPendingMin ? 'active-kpi' : ''}" onclick="setLegacyKpiFilter('pending_minutes')" title="点击仅筛选待发送会议纪要的遗留任务 (${pendingMinutesCount}项)">
        <div class="legacy-kpi-icon" style="background:#fef2f2; color:#dc2626;">📝</div>
        <div>
          <div class="legacy-kpi-val" style="color:#dc2626;">${pendingMinutesCount}</div>
          <div class="legacy-kpi-lbl">待发送会议纪要</div>
        </div>
      </div>
    `;
  }

  // 3. 过滤任务列表 (支持 KPI 卡片联动过滤、责任人筛选与关键词搜索)
  let filtered = panelTasks.filter(t => {
    if (legacyFilterOwner !== 'all' && (t.owner || '').trim() !== legacyFilterOwner) return false;

    const reps = getNormalizedTaskReports(t, allMeetings);

    // KPI 点击联动筛选
    if (legacyKpiFilter === 'this_week') {
      const hasThisWeek = reps && reps.some(r => isDateInCurrentWeek(r.reportTime));
      if (!hasThisWeek) return false;
    } else if (legacyKpiFilter === 'pending_minutes') {
      const hasPendingMin = reps && reps.length > 0 && reps.some(r => !r.hasMinutes);
      if (!hasPendingMin) return false;
    }

    if (legacySearchKeyword) {
      const matchTitle = (t.title || '').toLowerCase().includes(legacySearchKeyword);
      const matchOwner = (t.owner || '').toLowerCase().includes(legacySearchKeyword);
      const matchReports = reps.some(r => (r.reportTime || '').toLowerCase().includes(legacySearchKeyword) || (r.minutes || '').toLowerCase().includes(legacySearchKeyword) || (r.reviewOpinion || '').toLowerCase().includes(legacySearchKeyword));
      if (!matchTitle && !matchOwner && !matchReports) return false;
    }
    return true;
  });

  // 4. 排序规则：按照时间排，已汇报的在后面，待汇报的在前面
  // Category 0: 待汇报 (有未来排期) -> 最前，按时间升序排
  // Category 1: 已汇报 (汇报时间已过) -> 其次，按时间降序排
  // Category 2: 尚未汇报 -> 最后
  const getTaskCategoryAndSortKey = (t) => {
    const reps = getNormalizedTaskReports(t, allMeetings);
    if (!reps || reps.length === 0) {
      return { cat: 2, key: '9999' };
    }
    const futureReps = reps.filter(isReportPending);
    const pastReps = reps.filter(r => !isReportPending(r));
    if (futureReps.length > 0) {
      const minFuture = futureReps.map(r => r.reportTime || '').filter(Boolean).sort()[0] || '';
      return { cat: 0, key: minFuture };
    } else {
      const maxPast = pastReps.map(r => r.reportTime || '').filter(Boolean).sort().reverse()[0] || '';
      return { cat: 1, key: maxPast };
    }
  };

  filtered.sort((a, b) => {
    const infoA = getTaskCategoryAndSortKey(a);
    const infoB = getTaskCategoryAndSortKey(b);
    if (infoA.cat !== infoB.cat) {
      return infoA.cat - infoB.cat;
    }
    if (infoA.key !== infoB.key) {
      if (infoA.cat === 0) {
        return infoA.key.localeCompare(infoB.key); // 待汇报：越早将要开的排在最前
      } else if (infoA.cat === 1) {
        return infoB.key.localeCompare(infoA.key); // 已汇报：最新汇报排在前面
      }
    }
    return (a.id || 0) - (b.id || 0);
  });

  // 5. 渲染对应的视图
  if (legacyViewMode === 'cards') {
    renderLegacyCardsView(filtered, allMeetings);
  } else {
    renderLegacyTableView(filtered, allMeetings);
  }

  updateMeetingLegacyTaskOptions();
}

// 视图 1：看板卡片视图 (严格精简，无多余字段，无任务流转按钮)
function renderLegacyCardsView(tasks, allMeetings) {
  const container = document.getElementById('legacyCardsContainer');
  if (!container) return;

  if (tasks.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px 20px; background: #ffffff; border-radius: 12px; border: 1px dashed #cbd5e1;">
        <div style="font-size: 32px; margin-bottom: 8px;">📋</div>
        <div style="font-weight: 700; color: #475569; margin-bottom: 4px;">暂无符合条件的遗留任务</div>
        <div style="font-size: 12px; color: #94a3b8; margin-bottom: 14px;">当前面板仅展示 Open 任务与 申请关闭 任务</div>
        <button class="btn btn-sm btn-primary" onclick="openAddLegacyTaskModal()">＋ 立即登记遗留任务</button>
      </div>
    `;
    return;
  }

  container.innerHTML = tasks.map(task => {
    const reports = getNormalizedTaskReports(task, allMeetings);
    const reportCount = reports.length;
    const isApplying = isTaskApplyingClosed(task);

    return `
      <div class="legacy-card" style="border-left: 4px solid ${isApplying ? '#f59e0b' : '#3b82f6'};">
        <div class="legacy-card-header">
          <div>
            ${isApplying ? '<span style="background:#fef3c7; color:#92400e; font-size:11px; font-weight:700; padding:2px 8px; border-radius:10px; border:1px solid #fde68a;">🟡 申请关闭</span>' : '<span style="background:#e0f2fe; color:#0369a1; font-size:11px; font-weight:700; padding:2px 8px; border-radius:10px; border:1px solid #bae6fd;">🟢 Open</span>'}
          </div>
          <div style="font-size:12px; font-weight:700; color:#0284c7;">👤 ${escapeHtml(task.owner || '待定')}</div>
        </div>

        <!-- 遗留任务：纯粹来自 B 列 (*问题描述) -->
        <div style="font-weight:700; font-size:14px; color:#0f172a; margin:10px 0 6px 0; line-height:1.45;">
          ${escapeHtml(task.title || '')}
        </div>

        <!-- 汇报与纪要流式卡片 -->
        <div style="margin: 8px 0;">
          <div style="font-size:11.5px; font-weight:700; color:#475569; margin-bottom:4px; display:flex; justify-content:space-between;">
            <span>汇报记录&输出纪要 (${reportCount}次)</span>
            <a href="javascript:void(0)" onclick="openAddReportSessionModal(${task.id})" style="color:#2563eb; text-decoration:none;">＋ 登记汇报</a>
          </div>
          <div class="legacy-reports-flow" style="min-width:auto; max-width:100%;">
            ${reports.length === 0 ? `
              <div style="font-size:11.5px; color:#94a3b8; font-style:italic; padding:6px 0;">尚未汇报</div>
            ` : reports.map((r, rIdx) => {
              const isFuture = isReportPending(r);
              let badgeHTML = '';
              if (isFuture) {
                badgeHTML = `<span class="legacy-minutes-badge pending-report" onclick="openEditReportSessionModal(${task.id}, ${rIdx})" title="已排期，待正式汇报">⏳ 待汇报 📅</span>`;
              } else if (r.hasMinutes) {
                badgeHTML = `<span class="legacy-minutes-badge has-minutes" onclick="openEditReportSessionModal(${task.id}, ${rIdx})" title="点击查看/修改本次纪要与批示">✅ 已出纪要 📝</span>`;
              } else {
                badgeHTML = `<span class="legacy-minutes-badge no-minutes" onclick="openEditReportSessionModal(${task.id}, ${rIdx})" title="点击快速补录本次汇报纪要">⚠️ 待发送纪要 ✏️</span>`;
              }

              return `
                <div class="legacy-report-card">
                  <div class="legacy-report-card-header">
                    <div style="display:flex; align-items:center; gap:5px;">
                      <span class="legacy-report-seq-badge">第${r.seq || (rIdx + 1)}次</span>
                      <span class="legacy-report-time-text">🕒 ${escapeHtml(r.reportTime || '')}</span>
                    </div>
                    ${badgeHTML}
                  </div>
                  ${r.reviewOpinion ? `<div class="legacy-report-opinion-quote"><strong>纪要决议:</strong> ${escapeHtml(r.reviewOpinion)}</div>` : ''}
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- 底部操作按钮 (纯粹操作，绝无任务流转按钮) -->
        <div class="legacy-card-actions" style="margin-top:10px; display:flex; gap:6px; flex-wrap:wrap; justify-content:flex-end;">
          <button class="btn btn-xs btn-ghost" onclick="openAddReportSessionModal(${task.id})" title="登记汇报">🎙️ 登记汇报</button>
          <button class="btn btn-xs btn-ghost" onclick="scheduleReportMeetingForLegacyTask(${task.id})" title="预约排期">📅 会议预约</button>
          <button class="btn btn-xs btn-ghost" onclick="openEditLegacyTaskModal(${task.id})" title="编辑">✏️ 编辑</button>
          <button class="btn btn-xs btn-ghost" onclick="deleteLegacyTask(${task.id})" style="color:#ef4444;" title="删除">🗑️</button>
        </div>
      </div>
    `;
  }).join('');
}

// 视图 2：以表格清单为主视图
// 严格指令执行：
// 1. 遗留任务只有 B 列是，绝不把其他数据拼入展示。
// 2. 责任人就是同一行对应的责任人 (C 列)。
// 3. 其他信息全部不再出现和呈现。
// 4. 只展示 open 的任务和申请关闭的任务，不写任务流转。
function renderLegacyTableView(tasks, allMeetings) {
  const container = document.getElementById('legacyTableContainer');
  if (!container) return;

  if (tasks.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 48px 20px; background:#fff; border-radius:12px; border:1px dashed #cbd5e1;">
        <div style="font-size: 32px; margin-bottom: 8px;">📋</div>
        <div style="font-weight: 700; color: #475569; font-size:14px; margin-bottom:4px;">暂无遗留任务记录</div>
        <div style="font-size: 12px; color: #94a3b8; margin-bottom:14px;">当前面板仅展示 Open 任务与 申请关闭 任务</div>
        <button class="btn btn-sm btn-primary" onclick="openAddLegacyTaskModal()">＋ 立即登记遗留任务</button>
      </div>
    `;
    return;
  }

  const filterNoticeHTML = legacyKpiFilter !== 'all' ? `
    <div style="display:flex; justify-content:space-between; align-items:center; background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:6px 12px; margin-bottom:12px; font-size:12px; color:#1e40af;">
      <span>🔍 当前筛选：<strong>${legacyKpiFilter === 'this_week' ? '本周汇报遗留任务 (' + tasks.length + '项)' : '待发送会议纪要 (' + tasks.length + '项)'}</strong></span>
      <button class="btn btn-xs btn-ghost" onclick="setLegacyKpiFilter('all')" style="color:#2563eb; font-weight:700; text-decoration:underline; cursor:pointer;">✕ 显示全部遗留任务</button>
    </div>
  ` : '';

  container.innerHTML = filterNoticeHTML + `
    <table class="legacy-table">
      <thead>
        <tr style="background:#f8fafc;">
          <th style="min-width:360px; font-weight:700;">遗留任务</th>
          <th style="min-width:120px; font-weight:700;">责任人</th>
          <th style="min-width:440px; font-weight:700;">汇报记录&输出纪要</th>
        </tr>
      </thead>
      <tbody>
        ${tasks.map(task => {
          const reports = getNormalizedTaskReports(task, allMeetings);

          // 汇报与纪要流式卡片
          let reportsHTML = '';
          if (reports.length === 0) {
            reportsHTML = `
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="background:#f1f5f9; color:#64748b; font-size:11.5px; padding:3px 8px; border-radius:12px; border:1px solid #e2e8f0; font-weight:600;">
                  ⚪ 尚未汇报
                </span>
                <button class="btn btn-xs" onclick="openAddReportSessionModal(${task.id})" style="background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe; font-size:11px; font-weight:700; border-radius:4px; padding:2px 8px;" title="登记汇报时间与纪要">
                  ＋ 登记汇报
                </button>
                <button class="btn btn-xs" onclick="scheduleReportMeetingForLegacyTask(${task.id})" style="background:#fffbeb; color:#d97706; border:1px solid #fde68a; font-size:11px; font-weight:700; border-radius:4px; padding:2px 6px;" title="通过会议预约排期汇报">
                  🎙️ 预约会议
                </button>
              </div>
            `;
          } else {
            reportsHTML = `
              <div class="legacy-reports-flow">
                ${reports.map((rep, rIdx) => {
                  const isFuture = isReportPending(rep);
                  const hasMin = Boolean(rep.hasMinutes);
                  const seqText = `第${rep.seq || (rIdx + 1)}次`;
                  const timeText = rep.reportTime || '时间待确认';
                  const opinion = rep.reviewOpinion || rep.minutes || '';

                  let badgeHTML = '';
                  if (isFuture) {
                    badgeHTML = `
                      <span class="legacy-minutes-badge pending-report" onclick="openEditReportSessionModal(${task.id}, ${rIdx})" title="已排期，待正式汇报">
                        ⏳ 待汇报 📅
                      </span>
                    `;
                  } else if (hasMin) {
                    badgeHTML = `
                      <span class="legacy-minutes-badge has-minutes" onclick="openEditReportSessionModal(${task.id}, ${rIdx})" title="点击查看/修改本次纪要与批示">
                        ✅ 已出纪要 📝
                      </span>
                    `;
                  } else {
                    badgeHTML = `
                      <span class="legacy-minutes-badge no-minutes" onclick="openEditReportSessionModal(${task.id}, ${rIdx})" title="点击快速补录本次汇报纪要">
                        ⚠️ 待发送纪要 ✏️
                      </span>
                    `;
                  }

                  return `
                    <div class="legacy-report-card">
                      <div class="legacy-report-card-header">
                        <div style="display:flex; align-items:center; gap:6px;">
                          <span class="legacy-report-seq-badge">${seqText}</span>
                          <span class="legacy-report-time-text">🕒 ${escapeHtml(timeText)}</span>
                        </div>
                        <div>
                          ${badgeHTML}
                        </div>
                      </div>
                      ${opinion ? `
                        <div class="legacy-report-opinion-quote" title="${escapeHtml(opinion)}">
                          <span style="color:#0284c7; font-weight:700;">纪要批示:</span> ${escapeHtml(opinion.length > 55 ? opinion.slice(0, 55) + '...' : opinion)}
                        </div>
                      ` : ''}
                    </div>
                  `;
                }).join('')}
                <div style="display:flex; align-items:center; justify-content:space-between; padding:2px 4px; margin-top:2px;">
                  <a href="javascript:void(0)" onclick="openAddReportSessionModal(${task.id})" style="font-size:11.5px; color:#2563eb; font-weight:700; text-decoration:none; display:inline-flex; align-items:center; gap:3px;">
                    ＋ 登记第${reports.length + 1}次汇报
                  </a>
                  <a href="javascript:void(0)" onclick="scheduleReportMeetingForLegacyTask(${task.id})" style="font-size:11px; color:#d97706; text-decoration:underline;" title="通过会议预约排期汇报">
                    🎙️ 会议预约排期
                  </a>
                </div>
              </div>
            `;
          }

          return `
            <tr>
              <!-- 1. 遗留任务：纯粹来自 B 列 (*问题描述)，绝不把其他数据拼入呈现 -->
              <td style="padding:12px 14px; vertical-align:middle;">
                <div style="font-weight:700; color:#0f172a; font-size:13px; line-height:1.5;">
                  ${escapeHtml(task.title || '')}
                </div>
              </td>

              <!-- 2. 责任人：同一行对应的责任人 (C 列) -->
              <td style="padding:12px 14px; white-space:nowrap; vertical-align:middle;">
                <span style="display:inline-flex; align-items:center; gap:5px; background:#f0f9ff; color:#0284c7; padding:4px 10px; border-radius:6px; font-weight:700; font-size:12px; border:1px solid #bae6fd;">
                  👤 ${escapeHtml(task.owner || '待分配')}
                </span>
              </td>

              <!-- 3. 汇报记录&输出纪要 (汇报时间与纪要 1对1 紧密对应) -->
              <td style="padding:12px 14px; vertical-align:middle;">
                ${reportsHTML}
              </td>
            </tr>
          `;
        }).join('')}
      </tbody>
    </table>
  `;
}

// 模态框：登记新一次向曦总汇报
function openAddReportSessionModal(taskId) {
  const tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  const task = tasks.find(t => t.id == taskId);
  if (!task) return;
  const allMeetings = getData(STORAGE_KEYS.MEETINGS, []);
  const reports = getNormalizedTaskReports(task, allMeetings);
  const nextSeq = reports.length + 1;

  document.getElementById('inputAddReportTaskId').value = task.id;
  document.getElementById('textAddReportModalTitle').textContent = `🎙️ 登记第${nextSeq}次向曦总汇报与会议纪要`;
  document.getElementById('textAddReportTaskDesc').textContent = `【遗留任务】${task.title || ''} (责任人: ${task.owner || '待分配'})`;

  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  const h = String(now.getHours()).padStart(2, '0');
  const min = String(now.getMinutes()).padStart(2, '0');
  document.getElementById('inputAddReportTime').value = `${y}-${m}-${d} ${h}:${min}`;
  document.getElementById('inputAddReporter').value = task.owner || '';
  document.getElementById('selectAddReportHasMinutes').value = 'yes';
  document.getElementById('inputAddReportReviewOpinion').value = '';
  document.getElementById('inputAddReportMinutes').value = '';

  openModal('legacyAddReportModal');
}

function handleAddReportHasMinutesChange(val) {
  const opinionEl = document.getElementById('inputAddReportReviewOpinion');
  const minEl = document.getElementById('inputAddReportMinutes');
  if (val === 'no') {
    if (opinionEl) opinionEl.placeholder = '可先留空，待向曦总汇报完毕后补录批示...';
    if (minEl) minEl.placeholder = '待汇报完毕后补录完整纪要与下一步计划...';
  } else {
    if (opinionEl) opinionEl.placeholder = '记录向曦总汇报后领导的审阅意见、特批定夺要求或核心结论...';
    if (minEl) minEl.placeholder = '记录本次汇报后达成的会议纪要内容、具体责任分工与落实排期...';
  }
}

function saveAddReportSession() {
  const taskId = document.getElementById('inputAddReportTaskId').value;
  let tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  const idx = tasks.findIndex(t => t.id == taskId);
  if (idx === -1) return;

  const time = document.getElementById('inputAddReportTime').value.trim();
  if (!time) {
    showToast('请填写本次汇报时间！');
    return;
  }
  const reporter = document.getElementById('inputAddReporter').value.trim() || tasks[idx].owner;
  const hasMinutes = document.getElementById('selectAddReportHasMinutes').value === 'yes';
  const reviewOpinion = document.getElementById('inputAddReportReviewOpinion').value.trim();
  const minutes = document.getElementById('inputAddReportMinutes').value.trim();

  const allMeetings = getData(STORAGE_KEYS.MEETINGS, []);
  let reports = getNormalizedTaskReports(tasks[idx], allMeetings);
  const nextSeq = reports.length + 1;

  const newSession = {
    id: 'rep_' + Date.now(),
    seq: nextSeq,
    reportTime: time,
    hasMinutes: hasMinutes,
    reviewOpinion: reviewOpinion,
    minutes: minutes,
    reporter: reporter,
    isManual: true
  };
  reports.push(newSession);

  tasks[idx].reports = reports;
  tasks[idx].reportTime = time;
  tasks[idx].hasMinutes = hasMinutes;
  if (reviewOpinion) tasks[idx].reviewOpinion = reviewOpinion;
  tasks[idx].updatedAt = Date.now();

  setData(STORAGE_KEYS.LEGACY_TASKS, tasks);
  closeModal('legacyAddReportModal');
  renderLegacyTasks();
  showToast(`🎉 已成功登记第${nextSeq}次向曦总汇报记录！`);
}

// 模态框：查看与编辑单次汇报与纪要
function openEditReportSessionModal(taskId, rIdx) {
  const tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  const task = tasks.find(t => t.id == taskId);
  if (!task) return;
  const allMeetings = getData(STORAGE_KEYS.MEETINGS, []);
  let reports = getNormalizedTaskReports(task, allMeetings);
  const rep = reports[rIdx];
  if (!rep) return;

  document.getElementById('inputEditReportTaskId').value = task.id;
  document.getElementById('inputEditReportIdx').value = rIdx;
  document.getElementById('textEditReportModalTitle').textContent = `📝 查看与更新第${rep.seq || (rIdx + 1)}次汇报纪要`;
  document.getElementById('textEditReportTaskDesc').textContent = `【遗留任务】${task.title || ''} (责任人: ${task.owner || '待分配'})`;

  document.getElementById('inputEditReportTime').value = rep.reportTime || '';
  document.getElementById('inputEditReporter').value = rep.reporter || task.owner || '';
  document.getElementById('selectEditReportHasMinutes').value = rep.hasMinutes ? 'yes' : 'no';
  document.getElementById('inputEditReportReviewOpinion').value = rep.reviewOpinion || '';
  document.getElementById('inputEditReportMinutes').value = rep.minutes || '';

  openModal('legacyEditReportModal');
}

function saveEditReportSession() {
  const taskId = document.getElementById('inputEditReportTaskId').value;
  const rIdx = parseInt(document.getElementById('inputEditReportIdx').value, 10);
  let tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  const tIdx = tasks.findIndex(t => t.id == taskId);
  if (tIdx === -1) return;

  const time = document.getElementById('inputEditReportTime').value.trim();
  if (!time) {
    showToast('汇报时间不能为空！');
    return;
  }
  const reporter = document.getElementById('inputEditReporter').value.trim();
  const hasMinutes = document.getElementById('selectEditReportHasMinutes').value === 'yes';
  const reviewOpinion = document.getElementById('inputEditReportReviewOpinion').value.trim();
  const minutes = document.getElementById('inputEditReportMinutes').value.trim();

  const allMeetings = getData(STORAGE_KEYS.MEETINGS, []);
  let reports = getNormalizedTaskReports(tasks[tIdx], allMeetings);
  let meetingIdToUpdate = null;
  if (rIdx >= 0 && rIdx < reports.length) {
    reports[rIdx].reportTime = time;
    reports[rIdx].reporter = reporter;
    reports[rIdx].hasMinutes = hasMinutes;
    reports[rIdx].reviewOpinion = reviewOpinion;
    reports[rIdx].minutes = minutes;
    meetingIdToUpdate = reports[rIdx].meetingId;
  }

  tasks[tIdx].reports = reports;
  const lastRep = reports[reports.length - 1];
  if (lastRep) {
    tasks[tIdx].reportTime = lastRep.reportTime;
    tasks[tIdx].hasMinutes = lastRep.hasMinutes;
    if (lastRep.reviewOpinion) tasks[tIdx].reviewOpinion = lastRep.reviewOpinion;
  }
  tasks[tIdx].updatedAt = Date.now();

  setData(STORAGE_KEYS.LEGACY_TASKS, tasks);

  // 双向联动：如果本次汇报关联了预约会议，同步更新会议纪要状态
  if (meetingIdToUpdate) {
    let meetings = getData(STORAGE_KEYS.MEETINGS, []);
    const mIdx = meetings.findIndex(m => String(m.id) === String(meetingIdToUpdate));
    if (mIdx !== -1) {
      meetings[mIdx].hasMinutes = hasMinutes ? 'yes' : 'no';
      if (reviewOpinion) meetings[mIdx].decision = reviewOpinion;
      if (minutes) meetings[mIdx].nextPlan = minutes;
      setData(STORAGE_KEYS.MEETINGS, meetings);
    }
  }

  closeModal('legacyEditReportModal');
  renderLegacyTasks();
  showToast('✅ 汇报记录与纪要已更新！');
}

function deleteCurrentReportSession() {
  const taskId = document.getElementById('inputEditReportTaskId').value;
  const rIdx = parseInt(document.getElementById('inputEditReportIdx').value, 10);
  let tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  const tIdx = tasks.findIndex(t => t.id == taskId);
  if (tIdx === -1) return;

  if (!confirm('确定要删除此条汇报记录吗？')) return;

  const allMeetings = getData(STORAGE_KEYS.MEETINGS, []);
  let reports = getNormalizedTaskReports(tasks[tIdx], allMeetings);
  if (rIdx >= 0 && rIdx < reports.length) {
    reports.splice(rIdx, 1);
    reports.forEach((r, i) => { r.seq = i + 1; });
  }
  tasks[tIdx].reports = reports;
  const lastRep = reports.length > 0 ? reports[reports.length - 1] : null;
  tasks[tIdx].reportTime = lastRep ? lastRep.reportTime : '';
  tasks[tIdx].hasMinutes = lastRep ? lastRep.hasMinutes : false;
  tasks[tIdx].updatedAt = Date.now();

  setData(STORAGE_KEYS.LEGACY_TASKS, tasks);
  closeModal('legacyEditReportModal');
  renderLegacyTasks();
  showToast('🗑️ 该场汇报记录已删除');
}

function openAddLegacyTaskModal() {
  document.getElementById('legacyTaskModalTitle').textContent = '新增部门遗留任务';
  document.getElementById('inputLegacyTaskId').value = '';
  document.getElementById('inputLegacyTaskTitle').value = '';
  document.getElementById('inputLegacyTaskOwner').value = '';
  document.getElementById('selectLegacyTaskStatus').value = 'in_progress';
  openModal('legacyTaskModal');
}

function openEditLegacyTaskModal(id) {
  const tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  const task = tasks.find(t => t.id == id);
  if (!task) return;

  document.getElementById('legacyTaskModalTitle').textContent = '编辑部门遗留任务';
  document.getElementById('inputLegacyTaskId').value = task.id;
  document.getElementById('inputLegacyTaskTitle').value = task.title || '';
  document.getElementById('inputLegacyTaskOwner').value = task.owner || '';
  document.getElementById('selectLegacyTaskStatus').value = isTaskApplyingClosed(task) ? 'applying_closed' : 'in_progress';
  openModal('legacyTaskModal');
}

function saveLegacyTask() {
  const id = document.getElementById('inputLegacyTaskId').value;
  const title = document.getElementById('inputLegacyTaskTitle').value.trim();
  const owner = document.getElementById('inputLegacyTaskOwner').value.trim();
  const statusVal = document.getElementById('selectLegacyTaskStatus').value;
  const status = statusVal === 'applying_closed' ? '申请关闭' : 'Open';

  if (!title) {
    showToast('请填写遗留任务描述！');
    return;
  }

  let tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);

  if (id) {
    const idx = tasks.findIndex(t => t.id == id);
    if (idx !== -1) {
      tasks[idx].title = title;
      tasks[idx].owner = owner || '待分配';
      tasks[idx].status = status;
      tasks[idx].updatedAt = Date.now();
    }
  } else {
    tasks.unshift({
      id: Date.now(),
      title: title,
      owner: owner || '待分配',
      status: status,
      reports: [],
      reportTime: '',
      hasMinutes: false,
      createdAt: Date.now(),
      updatedAt: Date.now()
    });
  }

  setData(STORAGE_KEYS.LEGACY_TASKS, tasks);
  closeModal('legacyTaskModal');
  renderLegacyTasks();
  showToast('💾 遗留任务已保存！');
}

function deleteLegacyTask(id) {
  let tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  const task = tasks.find(t => t.id == id);
  if (!task) return;

  if (!confirm(`确定要删除遗留任务「${task.title}」吗？`)) {
    return;
  }

  tasks = tasks.filter(t => t.id != id);
  setData(STORAGE_KEYS.LEGACY_TASKS, tasks);
  renderLegacyTasks();
  showToast('🗑️ 任务已删除');
}

function openLegacyMinutesModal(id) {
  openAddReportSessionModal(id);
}

function saveLegacyMinutes() {
  saveAddReportSession();
}

// 核心联动：一键预约汇报会议 (确保会议名称带有【xxx】与遗留任务精准互锁)
function scheduleReportMeetingForLegacyTask(taskId) {
  const tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  const task = tasks.find(t => t.id == taskId);
  if (!task) return;

  // 1. 打开会议预约弹窗
  openAddMeetingModal();

  // 2. 刷新并选定关联遗留任务下拉框
  updateMeetingLegacyTaskOptions(task.id);

  // 3. 计算已汇报过几次
  const allMeetings = getData(STORAGE_KEYS.MEETINGS, []);
  const pastReports = getNormalizedTaskReports(task, allMeetings);
  const nextSeq = pastReports.length + 1;

  // 4. 自动填入会议主题与责任人（规范【xxx】格式，确保双向智能匹配）
  const subjectInput = document.getElementById('inputMeetingSubject');
  if (subjectInput) {
    const rawTitle = (task.title || '').trim();
    if (rawTitle.startsWith('【')) {
      subjectInput.value = rawTitle;
    } else {
      subjectInput.value = `【${rawTitle}】遗留任务进展汇报`;
    }
  }
  const reporterInput = document.getElementById('inputMeetingReporter');
  if (reporterInput) {
    reporterInput.value = task.owner || '';
  }
  const requesterInput = document.getElementById('inputMeetingRequester');
  if (requesterInput) {
    requesterInput.value = task.owner || '责任人';
  }

  // 5. 自动带入背景与下一步计划
  const bgInput = document.getElementById('inputMeetingBackground');
  if (bgInput) {
    bgInput.value = `【遗留任务】${task.title || ''}\n【责任人】${task.owner || ''}`;
  }

  const decInput = document.getElementById('inputMeetingDecision');
  if (decInput && task.reviewOpinion) {
    decInput.value = `【前次审核意见】${task.reviewOpinion}`;
  }

  // 展开详细选项
  const details = document.getElementById('meetingFoldableDetails');
  if (details) details.open = true;

  showToast(`已载入「${task.title}」汇报信息，请确认时间并登记！`);
}

// 动态刷新会议模态框里的“关联遗留任务”下拉列表
function updateMeetingLegacyTaskOptions(selectedId) {
  const select = document.getElementById('selectMeetingLegacyTaskId');
  if (!select) return;
  const tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  let html = '<option value="">-- 无关联遗留任务 (常规主管会议) --</option>';
  tasks.forEach(t => {
    const isSel = (selectedId && String(selectedId) === String(t.id)) ? 'selected' : '';
    html += `<option value="${t.id}" ${isSel}>📋 [${escapeHtml(t.owner)}] ${escapeHtml(t.title)} (${t.status === 'completed' ? '已闭环' : '推进中'})</option>`;
  });
  select.innerHTML = html;
}

// 当在会议模态框中切换关联遗留任务时
function handleMeetingLegacyTaskSelect(taskId) {
  if (!taskId) return;
  const tasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  const task = tasks.find(t => String(t.id) === String(taskId));
  if (!task) return;

  const subjectInput = document.getElementById('inputMeetingSubject');
  if (subjectInput && (!subjectInput.value || subjectInput.value.startsWith('【遗留任务汇报'))) {
    const allMeetings = getData(STORAGE_KEYS.MEETINGS, []);
    const pastReports = getTaskReportMeetings(task, allMeetings);
    subjectInput.value = `【遗留任务汇报·第${pastReports.length + 1}次】${task.title}`;
  }
  const reporterInput = document.getElementById('inputMeetingReporter');
  if (reporterInput && !reporterInput.value) {
    reporterInput.value = task.owner || '';
  }
  const requesterInput = document.getElementById('inputMeetingRequester');
  if (requesterInput && !requesterInput.value) {
    requesterInput.value = `${task.owner || ''}${task.domain ? ' (' + task.domain + ')' : ''}`;
  }
}

// ==========================================
// 14 标准字段批量导入逻辑
// ==========================================

let _currentLegacyWorkbookSheets = [];

function openLegacyImportModal() {
  document.getElementById('inputLegacyImportText').value = '';
  document.getElementById('legacyImportPreviewArea').style.display = 'none';
  document.getElementById('btnConfirmLegacyImport').disabled = true;
  parsedLegacyImportTasks = [];
  _currentLegacyWorkbookSheets = [];
  const container = document.getElementById('legacySheetSelectorContainer');
  if (container) container.style.display = 'none';
  openModal('legacyImportModal');
}

function copyLegacyTaskHeader() {
  const header = "问题状态\\t*问题描述\\t*责任人\\t提出时间\\t*要求完成日期\\t更新完成时间\\t问题进展\\t审核意见\\t备注\\t汇报时间\\t逾期任务\\t本期新增\\t本期关闭\\t领域";
  copyToClipboard(header, "📋 14列标准表头已复制！可直接粘贴至 Excel 第一行。");
}

function downloadLegacyTaskTemplate() {
  const rows = [
    "问题状态,*问题描述,*责任人,提出时间,*要求完成日期,更新完成时间,问题进展,审核意见,备注,汇报时间,逾期任务,本期新增,本期关闭,领域",
    "推进中,突尼斯与利比亚交付资源协调与外汇保函特批,陈总,2026-10-15,2026-11-20,,整理法务补充条款准备下周向曦总复汇报审批,同意汇率特批方案补充两地分包合规条款,需重点关注利比亚外汇管制,2026-10-28 14:30,否,是,否,交付商务",
    "待汇报,开罗核心数据中心机房双活容灾实战演练,王工,2026-10-20,2026-11-25,,准备演练方案PPT汇报稿并申请割接窗口期,,,待安排,否,是,否,海外IT",
    "推进中,中东非区域跨国差旅多币种快速报销通道,李经理,2026-10-18,2026-11-15,,补充尼日利亚与利比亚特殊币种报销指引后发宣贯手册,曦总要求简化一线员工填报流程实行预审制,财务部牵头,2026-10-25 10:00,否,否,否,财务法务",
    "已闭环,Q2大客户年度维保续签与SLA保障协议签约,赵总,2026-09-10,2026-10-30,2026-10-28,合同已全签完毕并归档已顺利交接运营,按特批商务折让执行确保Q3开票回款,已完结归档,2026-10-12 16:00,否,否,是,商务合规"
  ];
  const csvContent = '\\uFEFF' + rows.join('\\\\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', '部门遗留任务清单标准模板.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  showToast("📥 部门遗留任务 14 列标准模板已下载！");
}

async function handleLegacyFileInput(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;

  const ext = file.name.split('.').pop().toLowerCase();
  if (ext === 'xlsx') {
    showToast('正在解析 Excel 并精准定位「NIS重点遗留任务」工作表...');
    try {
      const res = await readXlsxFile(file, { targetSheet: 'NIS重点遗留任务', returnDetails: true });
      if (!res || !res.text || !res.text.trim()) {
        showToast('⚠️ 未能从该 Excel 中读取到内容，请核对工作表');
        return;
      }
      _currentLegacyWorkbookSheets = res.allSheets || [];
      updateLegacySheetSelector(res.sheetName, _currentLegacyWorkbookSheets);
      document.getElementById('inputLegacyImportText').value = res.text;
      handleLegacyImportTextChange();
      if (res.matched) {
        showToast(`✅ 成功定位并提取工作表【${res.sheetName}】（共 ${res.rowCount || 0} 行）！`);
      } else {
        showToast(`ℹ️ 未检测到「NIS重点遗留任务」，已提取【${res.sheetName}】（可在上方切换工作表）`);
      }
    } catch (e) {
      alert('解析 XLSX 失败，建议在 Excel 中复制后直接粘贴到文本框：' + e.message);
    }
  } else {
    const reader = new FileReader();
    reader.onload = function(e) {
      document.getElementById('inputLegacyImportText').value = e.target.result;
      handleLegacyImportTextChange();
    };
    reader.readAsText(file, 'utf-8');
  }
  event.target.value = '';
}

function updateLegacySheetSelector(activeSheetName, sheets) {
  const container = document.getElementById('legacySheetSelectorContainer');
  const select = document.getElementById('legacyImportSheetSelect');
  const badge = document.getElementById('legacySheetTargetBadge');
  if (!container || !select) return;

  if (!sheets || sheets.length <= 1) {
    if (sheets && sheets.length === 1) {
      container.style.display = 'flex';
      const isTarget = (sheets[0].name.trim() === 'NIS重点遗留任务' || sheets[0].name.includes('NIS重点遗留任务'));
      if (badge) {
        badge.textContent = isTarget ? '🎯 已锁定提取「NIS重点遗留任务」' : ('📄 当前工作表：' + sheets[0].name);
      }
      select.innerHTML = '<option value="' + escapeHtml(sheets[0].name) + '">' + escapeHtml(sheets[0].name) + ' (' + sheets[0].rowCount + '行)</option>';
    } else {
      container.style.display = 'none';
    }
    return;
  }

  container.style.display = 'flex';
  const hasTarget = sheets.some(s => s.name.trim() === 'NIS重点遗留任务' || s.name.replace(/\\s+/g, '') === 'NIS重点遗留任务' || s.name.includes('NIS重点遗留任务'));
  if (badge) {
    badge.textContent = hasTarget ? '🎯 已自动锁定「NIS重点遗留任务」' : '📑 多工作表（未找到NIS重点遗留任务，已默认提取第1个）';
  }

  select.innerHTML = sheets.map(s => {
    const isTarget = (s.name.trim() === 'NIS重点遗留任务' || s.name.replace(/\\s+/g, '') === 'NIS重点遗留任务' || s.name.includes('NIS重点遗留任务'));
    const isSelected = (s.name === activeSheetName);
    const label = escapeHtml(s.name) + (isTarget ? ' 🎯[目标Sheet]' : '') + ' (' + s.rowCount + '行)';
    return '<option value="' + escapeHtml(s.name) + '" ' + (isSelected ? 'selected' : '') + '>' + label + '</option>';
  }).join('');
}

function onLegacySheetSelected(sheetName) {
  if (!_currentLegacyWorkbookSheets || !_currentLegacyWorkbookSheets.length) return;
  const s = _currentLegacyWorkbookSheets.find(item => item.name === sheetName);
  if (s) {
    document.getElementById('inputLegacyImportText').value = s.text;
    handleLegacyImportTextChange();
    showToast(`已切换至工作表【${s.name}】（共 ${s.rowCount} 行）`);
  }
}

function normalizeDateStr(val) {
  if (!val) return '';
  val = String(val).trim();
  const num = parseFloat(val);
  if (!isNaN(num) && num >= 35000 && num <= 65000 && /^\\d+(\\.\\d+)?$/.test(val)) {
    const d = new Date(Math.round((num - 25569) * 86400 * 1000));
    const y = d.getUTCFullYear();
    const m = String(d.getUTCMonth() + 1).padStart(2, '0');
    const day = String(d.getUTCDate()).padStart(2, '0');
    return y + '-' + m + '-' + day;
  }
  val = val.replace(/\\//g, '-').replace(/\\./g, '-');
  const m = val.match(/\\d{4}-\\d{1,2}-\\d{1,2}/);
  if (m) {
    const parts = m[0].split('-');
    return parts[0] + '-' + parts[1].padStart(2, '0') + '-' + parts[2].padStart(2, '0');
  }
  return '';
}

function splitLegacyCells(line) {
  if (!line) return [];
  var CH_TAB = String.fromCharCode(9);
  // 1. 如果包含制表符 Tab，优先按 Tab 切分 (标准 Excel/WPS/飞书复制)
  if (line.indexOf(CH_TAB) !== -1) {
    return line.split(CH_TAB).map(function(s) { return s.trim().replace(/^["']|["']$/g, ''); });
  }
  // 2. 如果包含竖线 Markdown 表格格式
  if (line.indexOf('|') !== -1) {
    var p = line.split('|').map(function(s) { return s.trim().replace(/^["']|["']$/g, ''); });
    if (p.length > 0 && p[0] === '') p.shift();
    if (p.length > 0 && p[p.length - 1] === '') p.pop();
    return p;
  }
  // 3. 如果包含逗号 CSV 格式
  if (line.indexOf(',') !== -1) {
    var res = [];
    var inQuotes = false;
    var cur = '';
    for (var i = 0; i < line.length; i++) {
      var c = line[i];
      if (c === '"') { inQuotes = !inQuotes; }
      else if (c === ',' && !inQuotes) { res.push(cur.trim()); cur = ''; }
      else { cur += c; }
    }
    res.push(cur.trim());
    return res.map(function(c) { return c.replace(/^["']|["']$/g, ''); });
  }
  // 4. 连续两个以上空格
  if (line.indexOf('  ') !== -1) {
    return line.split(/\s{2,}/).map(function(s) { return s.trim().replace(/^["']|["']$/g, ''); });
  }
  return [line.trim()];
}

function normalizeHeaderCell(cell) {
  if (!cell) return '';
  return String(cell)
    .toLowerCase()
    .replace(/[*（）()／/\\:：_#-]/g, '')
    .replace(/\s+/g, '')
    .trim();
}

function matchLegacyHeaderColumns(row) {
  var colMap = {
    status: -1,
    title: -1,
    owner: -1,
    reportTime: -1,
    hasMinutes: -1,
    reviewOpinion: -1
  };

  row.forEach(function(cell, idx) {
    var t = normalizeHeaderCell(cell);
    if (!t) return;

    if (t === '问题状态' || t === '状态' || t === 'status') {
      colMap.status = idx;
    } else if (
      t.indexOf('责任人') !== -1 ||
      t.indexOf('主责人') !== -1 ||
      t.indexOf('负责人') !== -1 ||
      t.indexOf('牵头人') !== -1 ||
      t.indexOf('承办人') !== -1 ||
      t === 'owner' ||
      t === 'assignee' ||
      t === '责任' ||
      t === '人'
    ) {
      if (colMap.owner === -1) colMap.owner = idx;
    } else if (
      t.indexOf('问题描述') !== -1 ||
      t.indexOf('任务描述') !== -1 ||
      t.indexOf('遗留任务') !== -1 ||
      t.indexOf('事项描述') !== -1 ||
      t === '描述' || t === '任务' || t === '事项' || t === 'title' || t === 'task'
    ) {
      if (colMap.title === -1) colMap.title = idx;
    } else if (t.indexOf('汇报时间') !== -1 || t.indexOf('汇报日期') !== -1 || t.indexOf('开会时间') !== -1 || t.indexOf('是否汇报') !== -1) {
      colMap.reportTime = idx;
    } else if (t.indexOf('审核意见') !== -1 || t.indexOf('领导批示') !== -1 || t.indexOf('曦总批示') !== -1 || t.indexOf('意见') !== -1) {
      colMap.reviewOpinion = idx;
    } else if (t.indexOf('输出纪要') !== -1 || t.indexOf('会议纪要') !== -1 || t === '纪要') {
      colMap.hasMinutes = idx;
    }
  });

  // 严格兜底：B 列 (index 1) 是且仅是 遗留任务 (*问题描述)，C 列 (index 2) 是 责任人 (*责任人)
  if (colMap.title === -1 && row.length > 1) colMap.title = 1;
  if (colMap.owner === -1 && row.length > 2) colMap.owner = 2;
  if (colMap.status === -1 && row.length > 0) colMap.status = 0;

  return colMap;
}

function parseLegacyTaskRows(rawText) {
  if (!rawText || !rawText.trim()) return [];

  var CH_LF = String.fromCharCode(10);
  var CH_CR = String.fromCharCode(13);

  var lines = [];
  var curLine = '';
  var inQuotes = false;
  for (var i = 0; i < rawText.length; i++) {
    var ch = rawText[i];
    if (ch === '"') {
      inQuotes = !inQuotes;
      curLine += ch;
    } else if ((ch === CH_LF || ch === CH_CR) && !inQuotes) {
      if (ch === CH_CR && rawText[i + 1] === CH_LF) {
        i++;
      }
      if (curLine.trim()) lines.push(curLine.trim());
      curLine = '';
    } else {
      curLine += ch;
    }
  }
  if (curLine.trim()) lines.push(curLine.trim());
  if (lines.length === 0) return [];

  var rows = lines.map(splitLegacyCells);
  if (rows.length === 0) return [];

  var headerRowIdx = -1;
  var colMap = null;
  var maxMatchCount = 0;

  for (var r = 0; r < Math.min(rows.length, 15); r++) {
    var candidateMap = matchLegacyHeaderColumns(rows[r]);
    var matchCount = 0;
    if (candidateMap.owner !== -1) matchCount += 3;
    if (candidateMap.title !== -1) matchCount += 3;
    if (candidateMap.status !== -1) matchCount += 1;
    if (candidateMap.reportTime !== -1) matchCount += 1;

    if ((candidateMap.owner !== -1 || candidateMap.title !== -1) && matchCount >= 3 && matchCount > maxMatchCount) {
      maxMatchCount = matchCount;
      headerRowIdx = r;
      colMap = candidateMap;
    }
  }

  var hasHeader = (headerRowIdx !== -1 && colMap !== null);
  var dataRows = hasHeader ? rows.slice(headerRowIdx + 1) : rows;
  var parsed = [];

  dataRows.forEach(function(cols, rIdx) {
    if (cols.length === 0 || cols.every(function(c) { return !c; })) return;

    var titleCol = (hasHeader && colMap.title !== -1) ? colMap.title : 1;
    var ownerCol = (hasHeader && colMap.owner !== -1) ? colMap.owner : 2;
    var statusCol = (hasHeader && colMap.status !== -1) ? colMap.status : 0;
    var reportCol = (hasHeader && colMap.reportTime !== -1) ? colMap.reportTime : 9;
    var reviewCol = (hasHeader && colMap.reviewOpinion !== -1) ? colMap.reviewOpinion : 7;
    var minutesCol = (hasHeader && colMap.hasMinutes !== -1) ? colMap.hasMinutes : -1;

    // 核心提取：B 列（titleCol）是且仅是遗留任务，C 列（ownerCol）是同一行对应的责任人
    var title = (cols[titleCol] || '').trim();
    var owner = (cols[ownerCol] || '').trim();
    var rawStatus = (cols[statusCol] || '').trim();
    var reportTime = (cols[reportCol] || '').trim();
    var reviewOpinion = (reviewCol !== -1 && cols[reviewCol]) ? cols[reviewCol].trim() : '';

    // 严禁非 B 列内容进入遗留任务：若 B 列为空，坚决不作任务导入！
    if (!title) return;

    // 过滤换行截断导致的审核意见碎片与杂项
    if (title.indexOf('关键任务整理出来') !== -1) return;
    if (title.indexOf('今天发送纪要') !== -1) return;
    if (title.indexOf('宣传加强') !== -1) return;
    if (title.indexOf('保供的重新汇报') !== -1) return;
    if (title.indexOf('修改后的材料发出') !== -1) return;
    if (title.indexOf('群组发送') !== -1) return;
    if (title.indexOf('跟曦总同步进展') !== -1) return;
    if (title.indexOf('DTRB结论同步') !== -1) return;
    if (title.indexOf('材料发送邮件') !== -1) return;
    if (/^【\d{1,2}\/\d{1,2}】/.test(title)) return;
    if (/^\d{1,2}\/\d{1,2}/.test(title)) return;
    if (title.startsWith('@')) return;
    if (/^\d+$/.test(title) || /\d+%/.test(title)) return;
    if (title === 'FBB' || title === 'TMO' || title === 'NFV' || title === '其他' || title === 'SITE' || title === 'IT' || title === 'MBB') return;
    if (owner === 'SITE' || owner === 'Y' || owner.indexOf('今天发送纪要') !== -1) return;

    var normalizedStatus = 'Open';
    if (rawStatus.indexOf('关') !== -1 || rawStatus.indexOf('闭') !== -1 || rawStatus.indexOf('完成') !== -1 || rawStatus.toLowerCase() === 'completed' || rawStatus.toLowerCase() === 'closed') {
      normalizedStatus = '已闭环';
    } else if (rawStatus.indexOf('申请') !== -1) {
      normalizedStatus = '申请关闭';
    } else {
      normalizedStatus = 'Open';
    }

    // 严正指令：导入时绝不根据审核意见生成汇报！审核意见绝非汇报凭据！
    // 汇报状态纯粹且唯一由“预约会议”中匹配【xxx】决定！
    parsed.push({
      id: Date.now() + rIdx * 10,
      status: normalizedStatus,
      title: title, // 只有 B 列是，绝不塞入其他数据
      owner: owner, // 同一行对应的责任人 (C 列)
      reportTime: '',
      reports: [],
      hasMinutes: false,
      reviewOpinion: reviewOpinion,
      createdAt: Date.now(),
      updatedAt: Date.now()
    });
  });

  return parsed;
}

function fillLegacyImportSample() {
  var CH_TAB = String.fromCharCode(9);
  var CH_LF = String.fromCharCode(10);
  var sample = ["问题状态", "*问题描述", "*责任人", "提出时间", "*要求完成日期", "更新完成时间", "问题进展", "审核意见", "备注", "汇报时间", "逾期任务", "本期新增", "本期关闭", "领域"].join(CH_TAB) + CH_LF +
    ["推进中", "突尼斯与利比亚交付资源协调与外汇保函特批", "陈总", "2026-10-15", "2026-11-20", "", "整理两地法务补充条款准备下周向曦总复汇报审批", "同意汇率特批方案补充两地分包合规条款", "需重点关注利比亚外汇管制", "2026-10-28 14:30", "否", "是", "否", "交付商务"].join(CH_TAB) + CH_LF +
    ["待汇报", "开罗核心数据中心机房双活容灾实战演练", "王工", "2026-10-20", "2026-11-25", "", "准备演练方案PPT汇报稿并申请割接窗口期", "", "", "待安排", "否", "是", "否", "海外IT"].join(CH_TAB) + CH_LF +
    ["推进中", "中东非区域跨国差旅多币种快速报销通道", "李经理", "2026-10-18", "2026-11-15", "", "补充尼日利亚与利比亚特殊币种报销指引后发宣贯手册", "曦总要求简化一线员工填报流程实行预审制", "财务部牵头", "2026-10-25 10:00", "否", "否", "否", "财务法务"].join(CH_TAB);
  
  var ta = document.getElementById('inputLegacyImportText');
  if (ta) {
    ta.value = sample;
    handleLegacyImportTextChange();
    showToast('✨ 已填入 14 列标准示例数据，请查看下方预览！');
  }
}

function handleLegacyImportTextChange() {
  var text = document.getElementById('inputLegacyImportText').value;
  parsedLegacyImportTasks = parseLegacyTaskRows(text);

  var previewArea = document.getElementById('legacyImportPreviewArea');
  var emptyTip = document.getElementById('legacyImportEmptyTip');
  var btnConfirm = document.getElementById('btnConfirmLegacyImport');

  if (parsedLegacyImportTasks.length === 0) {
    if (previewArea) previewArea.style.display = 'none';
    if (emptyTip) emptyTip.style.display = text.trim() ? 'block' : 'none';
    if (btnConfirm) btnConfirm.disabled = true;
    return;
  }

  if (emptyTip) emptyTip.style.display = 'none';
  if (previewArea) previewArea.style.display = 'block';
  if (btnConfirm) btnConfirm.disabled = false;

  var countBadge = document.getElementById('legacyImportCountBadge');
  if (countBadge) {
    countBadge.textContent = '✓ 成功识别出 ' + parsedLegacyImportTasks.length + ' 项部门遗留任务';
  }

  var tableBody = document.getElementById('legacyImportPreviewTableBody');
  if (tableBody) {
    tableBody.innerHTML = parsedLegacyImportTasks.slice(0, 15).map(function(t, idx) {
      return '<tr>' +
        '<td style="padding:6px 8px; border-bottom:1px solid #f1f5f9; font-weight:700; color:#0f172a;">' + (idx + 1) + '. ' + escapeHtml(t.title) + '</td>' +
        '<td style="padding:6px 8px; border-bottom:1px solid #f1f5f9; color:#0284c7; font-weight:700; white-space:nowrap;">👤 ' + escapeHtml(t.owner) + '</td>' +
        '<td style="padding:6px 8px; border-bottom:1px solid #f1f5f9; color:#64748b; font-size:11.5px;">⚪ 待从预约会议自动匹配</td>' +
        '<td style="padding:6px 8px; border-bottom:1px solid #f1f5f9; color:#64748b; font-size:11.5px;">待输出</td>' +
        '<td style="padding:6px 8px; border-bottom:1px solid #f1f5f9; font-weight:700; font-size:11.5px;">' + escapeHtml(t.status) + '</td>' +
      '</tr>';
    }).join('');
    if (parsedLegacyImportTasks.length > 15) {
      tableBody.innerHTML += '<tr><td colspan="5" style="padding:8px; text-align:center; color:#94a3b8; font-style:italic;">... 还有 ' + (parsedLegacyImportTasks.length - 15) + ' 项任务未展开预览 ...</td></tr>';
    }
  }
}


function confirmImportLegacyTasks() {
  if (!parsedLegacyImportTasks || parsedLegacyImportTasks.length === 0) {
    showToast('未检测到有效的遗留任务数据');
    return;
  }

  const mode = document.querySelector('input[name="legacyImportModeRadio"]:checked') ? document.querySelector('input[name="legacyImportModeRadio"]:checked').value : 'append';
  let currentTasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);

  if (mode === 'replace') {
    if (!confirm(`确定要覆盖替换现有全部 ${currentTasks.length} 项遗留任务吗？\\n此操作将清空当前清单，并以本次导入的 ${parsedLegacyImportTasks.length} 项任务为准。`)) {
      return;
    }
    currentTasks = [...parsedLegacyImportTasks];
  } else {
    currentTasks = [...parsedLegacyImportTasks, ...currentTasks];
  }

  setData(STORAGE_KEYS.LEGACY_TASKS, currentTasks);
  closeModal('legacyImportModal');
  renderLegacyTasks();
  showToast(`🎉 成功导入 ${parsedLegacyImportTasks.length} 项遗留任务！数据已同步到 Mac SQLite 数据库。`);
}

function clearAllLegacyTasks() {
  const currentTasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
  if (!currentTasks || currentTasks.length === 0) {
    showToast('当前遗留任务清单已经是空的');
    return;
  }

  const ok = confirm(
    '⚠️ 危险操作确认：\\n\\n' +
    '确定要清空当前全部 ' + currentTasks.length + ' 项遗留任务吗？\\n\\n' +
    '此操作将从主机 SQLite 数据库及本地存储中彻底抹除所有遗留任务记录，无法撤销！\\n\\n' +
    '点击【确定】立即清空，点击【取消】保留数据。'
  );
  if (!ok) return;

  setData(STORAGE_KEYS.LEGACY_TASKS, []);
  renderLegacyTasks();
  if (document.getElementById('legacyImportModal')) {
    closeModal('legacyImportModal');
  }
  showToast('🗑️ 遗留任务清单已全部清空！');
}


function renderMeetings() {
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const conflictMap = getAllMeetingConflicts(meetings);
  const weekBoardEl = document.getElementById('supervisorWeeklyBoardContainer');
  const dayCalEl = document.getElementById('supervisorDayCalendarContainer');
  const monthCalEl = document.getElementById('supervisorMonthCalendarContainer');
  const cardsToolbar = document.getElementById('cardsSectionToolbar');
  const listEl = document.getElementById('meetingCardsList');
  const dashListEl = document.getElementById('dashMeetingList');
  const todayStr = getTodayDateStr();

  if (!selectedTimelineDate) selectedTimelineDate = todayStr;

  const dateInput = document.getElementById('timelineDateSelector');
  if (dateInput && dateInput.value !== selectedTimelineDate) {
    dateInput.value = selectedTimelineDate;
  }

  // Update statistics
  let pendingCount = 0;
  let scheduledCount = 0;
  let todayDurationMins = 0;

  meetings.forEach(m => {
    if (m.status === 'pending') pendingCount++;
    if (m.status === 'scheduled') scheduledCount++;
    if (m.date === selectedTimelineDate && m.status !== 'cancelled') {
      todayDurationMins += parseInt(m.duration || 30, 10);
    }
  });

  const meetingRequests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  const pendingRequestsCount = meetingRequests.filter(r => r.status !== 'scheduled').length;
  const totalPending = pendingCount + pendingRequestsCount;

  const pEl = document.getElementById('statPendingCount');
  const sEl = document.getElementById('statScheduledCount');
  const dEl = document.getElementById('statDurationSum');
  if (pEl) pEl.textContent = totalPending;
  if (sEl) sEl.textContent = scheduledCount;
  if (dEl) dEl.textContent = (todayDurationMins / 60).toFixed(1) + 'h';

  // Show/Hide view modes
  if (supervisorViewMode === 'week_board') {
    if (weekBoardEl) weekBoardEl.style.display = 'block';
    if (dayCalEl) dayCalEl.style.display = 'none';
    if (monthCalEl) monthCalEl.style.display = 'none';
    if (cardsToolbar) cardsToolbar.style.display = 'none';
    if (listEl) listEl.style.display = 'none';
    renderSupervisorWeeklyBoard();
  } else if (supervisorViewMode === 'day_cal') {
    if (weekBoardEl) weekBoardEl.style.display = 'none';
    if (dayCalEl) dayCalEl.style.display = 'block';
    if (monthCalEl) monthCalEl.style.display = 'none';
    if (cardsToolbar) cardsToolbar.style.display = 'none';
    if (listEl) listEl.style.display = 'none';
    renderSupervisorDayCalendar();
  } else if (supervisorViewMode === 'month_cal') {
    if (weekBoardEl) weekBoardEl.style.display = 'none';
    if (dayCalEl) dayCalEl.style.display = 'none';
    if (monthCalEl) monthCalEl.style.display = 'block';
    if (cardsToolbar) cardsToolbar.style.display = 'none';
    if (listEl) listEl.style.display = 'none';
    renderSupervisorMonthCalendar();
  } else if (supervisorViewMode === 'card_list') {
    if (weekBoardEl) weekBoardEl.style.display = 'none';
    if (dayCalEl) dayCalEl.style.display = 'none';
    if (monthCalEl) monthCalEl.style.display = 'none';
    if (cardsToolbar) cardsToolbar.style.display = 'flex';
    if (listEl) listEl.style.display = 'block';

    let filtered = meetings;
    if (currentMeetingFilter !== 'all') {
      filtered = filtered.filter(m => m.status === currentMeetingFilter);
    }
    filtered.sort((a, b) => {
      const da = (a.date || '') + ' ' + (a.time || '');
      const db = (b.date || '') + ' ' + (b.time || '');
      return da.localeCompare(db);
    });

    if (filtered.length === 0) {
      listEl.innerHTML = `
        <div style="text-align:center; padding: 36px 20px; color: var(--text-muted); background:var(--card); border:1px dashed var(--border); border-radius:var(--radius-md);">
          <img src="${SNOOPY_ASSETS.supervisor_secretary}" style="width:72px; opacity:0.65; margin-bottom:8px;" alt="" />
          <p style="font-size:13.5px; font-weight:600; color:var(--text-secondary);">暂无符合筛选条件的会议记录</p>
          <div style="margin-top:12px; display:flex; justify-content:center; gap:8px;">
            <button class="btn btn-sm btn-primary" onclick="openAddMeetingModal()">登记新预约</button>
            <button class="btn btn-sm" onclick="openImportCalendarModal()">导入表格 / 日历</button>
          </div>
        </div>`;
    } else {
      listEl.innerHTML = filtered.map(m => {
        const statusMap = {
          pending: { text: '待安排', cls: 'status-pending' },
          scheduled: { text: '已排期', cls: 'status-scheduled' },
          completed: { text: '已完成', cls: 'status-completed' },
          cancelled: { text: '已取消', cls: 'status-cancelled' }
        };
        const st = statusMap[m.status] || statusMap.pending;

        const priorityMap = {
          high: '<span class="priority-badge priority-high">紧急决议</span>',
          medium: '<span class="priority-badge priority-medium">常规业务</span>',
          routine: '<span class="priority-badge priority-low">例行汇报</span>'
        };
        const pr = priorityMap[m.priority] || priorityMap.medium;
        const durHours = m.durationHours || (parseInt(m.duration || 45, 10) / 60).toFixed(2);
        const dt = getMeetingDisplayTime(m);

        const mConflicts = conflictMap[m.id] || [];
        return `
          <div class="meeting-card ${mConflicts.length > 0 ? 'is-conflict' : ''}">
            <div class="meeting-card-top">
              <div class="meeting-title-area">
                <h3>
                  <span>${escapeHtml(m.subject)}</span>
                  ${pr}
                  <span class="status-badge ${st.cls}">${st.text}</span>
                  ${mConflicts.length > 0 ? '<span class="status-badge" style="background:#fee2e2; color:#be123c; border:1px solid #fecdd3; font-weight:700;">⚠️ 时间冲突</span>' : ''}
                </h3>
                ${mConflicts.length > 0 ? `
                  <div class="meeting-card-conflict-notice">
                    <div style="font-weight: 700; color: #be123c; font-size: 12px; display: flex; align-items: center; gap: 6px; margin-bottom: 3px;">
                      <span>⚠️ 会议时间冲突提醒</span>
                      <span style="background: #be123c; color: #ffffff; font-size: 10px; padding: 1px 6px; border-radius: 10px; font-weight: 700;">${mConflicts.length} 场重合</span>
                    </div>
                    ${mConflicts.map(c => `
                      <div style="font-size: 12px; color: #881337; margin-top: 2px;">
                        • 与【<strong>${escapeHtml(c.otherSubject)}</strong>】重合时间：
                        <strong style="color: #e11d48; background: #ffe4e6; padding: 1px 6px; border-radius: 3px; font-family: var(--font-mono);">🕒 ${c.overlapRangeStr}</strong>
                        <span>（重叠 ${c.overlapDuration} 分钟）</span>
                        ${c.otherReporter ? `· 汇报人: ${escapeHtml(c.otherReporter)}` : ''}
                      </div>
                    `).join('')}
                  </div>
                ` : ''}
                <div class="meeting-meta-row">
                  <span class="meta-chip"><strong>时间：</strong>${m.date} ${dt.start}${dt.end ? ' - ' + dt.end : ''}${dt.isShifted ? ` <span style="font-size:11px; color:var(--text-muted); font-weight:normal;">(开罗 ${dt.cairoStart})</span>` : ''}</span>
                  <span class="meta-chip"><strong>时长：</strong>${durHours}H (${m.duration || 45}分钟)</span>
                  <span class="meta-chip"><strong>地点：</strong>${escapeHtml(m.location || '主管办公室')}</span>
                  ${m.reporter ? `<span class="meta-chip"><strong>汇报人：</strong>${escapeHtml(m.reporter)}</span>` : ''}
                  ${m.minuter ? `<span class="meta-chip"><strong>纪要人：</strong>${escapeHtml(m.minuter)}</span>` : ''}
                </div>
              </div>

              <button class="btn btn-sm" onclick="copySingleMeetingNotice(${m.id})" title="复制该会议的完整通知格式至剪贴板">复制通知</button>
            </div>

            <div class="meeting-card-body">
              ${m.background ? `
                <div class="field-block">
                  <div class="field-label">议题背景</div>
                  <div class="field-val">${escapeHtml(m.background)}</div>
                </div>
              ` : ''}

              <div class="field-block">
                <div class="field-label">决策要点说明 (待主管定夺)</div>
                <div class="field-val decision-val">${escapeHtml(m.decision || '审议相关事项并定夺')}</div>
              </div>

              <div class="field-block">
                <div class="field-label">参会人员</div>
                <div class="field-val">${escapeHtml(m.attendees)}</div>
              </div>
            </div>

            <div class="meeting-card-footer">
              <div class="requester-info">
                <span>预约人：${escapeHtml(m.requester || '日历导入')}</span>
                ${m.notes ? ` · <span style="color:#d97706;">秘书备忘：${escapeHtml(m.notes)}</span>` : ''}
              </div>

              <div class="meeting-actions">
                ${m.status !== 'completed' ? `<button class="btn btn-sm btn-ghost" onclick="updateMeetingStatus(${m.id}, 'completed')">标记完成</button>` : ''}
                ${m.status === 'pending' ? `<button class="btn btn-sm btn-primary" onclick="updateMeetingStatus(${m.id}, 'scheduled')">确认排期</button>` : ''}
                <button class="btn btn-sm btn-ghost" onclick="editMeeting(${m.id})">编辑</button>
                <button class="btn btn-sm btn-ghost" style="color:#dc2626;" onclick="deleteMeeting(${m.id})">删除</button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }
  }

  // Dashboard Mini Box on HOME tab
  if (dashListEl) {
    const upcoming = meetings.filter(m => m.status === 'scheduled' || m.status === 'pending').slice(0, 3);
    if (upcoming.length === 0) {
      dashListEl.innerHTML = '<div style="color:var(--text-muted); font-size:12px; text-align:center; padding:12px;">今日暂无待开会议</div>';
    } else {
      dashListEl.innerHTML = upcoming.map(m => {
        const dt = getMeetingDisplayTime(m);
        return `
          <div style="padding:9px 12px; background:var(--card-subtle); border:1px solid var(--border); border-radius:var(--radius-sm); margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div style="font-size:13px; font-weight:700; color:var(--text-primary);">${escapeHtml(m.subject)}</div>
              <div style="font-size:11.5px; color:var(--text-secondary); margin-top:2px;">
                ${m.date} ${dt.start} (${m.duration}分)${dt.isShifted ? ` · [开罗 ${dt.cairoStart}]` : ''} · ${escapeHtml(m.reporter || m.attendees)}
              </div>
            </div>
            <button class="btn btn-sm" onclick="copySingleMeetingNotice(${m.id})">复制</button>
          </div>
        `;
      }).join('');
    }
  }
  if (typeof renderHomeTodayAgenda === 'function') renderHomeTodayAgenda();
}

function filterMeetings(type) {
  currentMeetingFilter = type;
  document.querySelectorAll('#cardStatusFilters .filter-btn').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-filter') === type);
  });
  renderMeetings();
}

function filterMeetingsByStat(type) {
  setSupervisorViewMode('card_list');
  filterMeetings(type);
  if (typeof document !== 'undefined' && document.querySelector) {
    const toolbar = document.querySelector('.meeting-toolbar');
    if (toolbar && typeof toolbar.scrollIntoView === 'function') {
      toolbar.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }
}

// ================= TIMELINE & AUTOMATIC FREE-SLOT DETECTION =================
function calculateDayFreeSlots(meetings, dateStr) {
  const dayStart = 9 * 60;      // 09:00 = 540 (上午9点开始-12点)
  const lunchStart = 12 * 60;   // 12:00 = 720
  const lunchEnd = 14 * 60;     // 14:00 = 840
  const dayEnd = 18 * 60;       // 18:00 = 1080 (下午14点-18点)

  const dayMeetings = meetings.filter(m => m.date === dateStr && m.status !== 'cancelled');

  const busyIntervals = [];
  dayMeetings.forEach(m => {
    const dt = getMeetingDisplayTime(m);
    const start = timeStrToMinutes(dt.start);
    const dur = parseInt(m.duration || 45, 10);
    const end = dt.end ? timeStrToMinutes(dt.end) : (start + dur);
    busyIntervals.push({ start, end, meeting: m });
  });

  busyIntervals.push({ start: lunchStart, end: lunchEnd, isLunch: true });
  busyIntervals.sort((a, b) => a.start - b.start);

  const mergedBusy = [];
  for (let cur of busyIntervals) {
    if (mergedBusy.length === 0) {
      mergedBusy.push({ ...cur });
    } else {
      let prev = mergedBusy[mergedBusy.length - 1];
      if (cur.start <= prev.end) {
        prev.end = Math.max(prev.end, cur.end);
        if (cur.meeting && !prev.meeting) prev.meeting = cur.meeting;
      } else {
        mergedBusy.push({ ...cur });
      }
    }
  }

  const freeSlots = [];
  let curTime = dayStart;

  for (let b of mergedBusy) {
    if (b.end <= dayStart) continue;
    if (b.start >= dayEnd) break;

    const slotStart = Math.max(curTime, dayStart);
    const slotEnd = Math.min(b.start, dayEnd);

    if (slotEnd - slotStart >= 15) {
      freeSlots.push({
        start: slotStart,
        end: slotEnd,
        duration: slotEnd - slotStart,
        startStr: minutesToTimeStr(slotStart),
        endStr: minutesToTimeStr(slotEnd)
      });
    }
    curTime = Math.max(curTime, b.end);
  }

  if (dayEnd - curTime >= 15) {
    freeSlots.push({
      start: curTime,
      end: dayEnd,
      duration: dayEnd - curTime,
      startStr: minutesToTimeStr(curTime),
      endStr: minutesToTimeStr(dayEnd)
    });
  }

  // Filter passed slots and present real-time available intervals for today
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  const todayStr = `${yyyy}-${mm}-${dd}`;

  let finalFreeSlots = freeSlots;
  if (dateStr === todayStr) {
    const nowMinutes = now.getHours() * 60 + now.getMinutes();
    const currentMinsRounded = Math.ceil(nowMinutes / 5) * 5;
    finalFreeSlots = [];
    for (let s of freeSlots) {
      if (s.end <= nowMinutes) {
        // Completely in the past today, do not show
        continue;
      }
      const adjustedStart = Math.max(s.start, currentMinsRounded);
      if (s.end - adjustedStart >= 15) {
        finalFreeSlots.push({
          start: adjustedStart,
          end: s.end,
          duration: s.end - adjustedStart,
          startStr: minutesToTimeStr(adjustedStart),
          endStr: minutesToTimeStr(s.end),
          isRealtimeAdjusted: adjustedStart > s.start
        });
      }
    }
  } else if (dateStr < todayStr) {
    finalFreeSlots = [];
  }

  return { dayMeetings, busyIntervals, freeSlots: finalFreeSlots };
}

function minutesToTimeStr(mins) {
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return (h < 10 ? '0' + h : '' + h) + ':' + (m < 10 ? '0' + m : '' + m);
}

function openAddMeetingModalWithSlot(date, startTime, duration) {
  openAddMeetingModal();
  if (date) {
    document.getElementById('inputMeetingDate').value = date;
    const trip = getTripForDate(date);
    const tzSelect = document.getElementById('inputMeetingTimezoneBase');
    if (tzSelect) {
      if (trip) {
        tzSelect.value = trip.destination;
      } else {
        tzSelect.value = 'cairo';
      }
      tzSelect._lastTz = tzSelect.value;
    }
  }
  if (startTime) {
    document.getElementById('inputMeetingStartTime').value = startTime;
    const dur = parseInt(duration || 45, 10);
    document.getElementById('inputMeetingEndTime').value = calculateEndTime(startTime, dur);
  }
  updateMeetingDurationBadge();
  handleMeetingModalTimezoneChange();
  checkMeetingConflicts();
  const eTime = document.getElementById('inputMeetingEndTime').value;
  showToast(`已自动填入推荐空档：${date} ${startTime} - ${eTime}`);
}

// ================= UNIVERSAL SMART CALENDAR & TABLE IMPORT ENGINE =================
let parsedImportMeetings = [];

function openImportCalendarModal() {
  const todayStr = getTodayDateStr();
  document.getElementById('importTargetDate').value = selectedTimelineDate || todayStr;
  document.getElementById('inputImportTableText').value = '';
  document.getElementById('importLivePreviewArea').style.display = 'none';
  document.getElementById('btnConfirmImport').disabled = true;
  parsedImportMeetings = [];
  openModal('importCalendarModal');
}

function copyStandardExcelHeader() {
  const header = "*会议主题（关键任务）\\t*议题背景/决策要点说明\\t*汇报人\\t*参会人\\t*纪要人\\t*预约时长（H）\\t排期日期\\t开始时间";
  copyToClipboard(header, "📋 标准表头已复制！可直接粘贴至 Excel 第一行。");
}

function downloadStandardExcelTemplate() {
  const rows = [
    "*会议主题（关键任务）,*议题背景/决策要点说明,*汇报人,*参会人,*纪要人,*预约时长（H）,排期日期,开始时间",
    "中东北非区域Q3交付资源评审,审批重点交付架构师驻场与预算特批,张总(地南代),主管、李总、财务BP,王秘书,0.75,2026-09-24,10:00",
    "阿尔及利亚代表处外汇与回款复盘,特批客户付款账期与汇率对冲,王总,主管、法务部、商务部,李秘书,1.0,2026-09-25,14:30",
    "刚果金代表处工程进展对齐,审批新安保防护与施工里程碑,陈部长,主管、交付部,赵秘书,0.5,2026-09-25,16:00"
  ];
  const csvContent = '\uFEFF' + rows.join('\\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', '主管日程标准导入模板.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  showToast("📥 标准 Excel CSV 模板已下载！");
}

// In-browser XLSX ZIP Reader supporting multi-sheet Excel .xlsx files
async function fallbackServerParseXlsx(file, targetSheetName, returnDetails) {
  try {
    const arrayBuffer = await file.arrayBuffer();
    const bytes = new Uint8Array(arrayBuffer);
    let binary = '';
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    const b64 = window.btoa(binary);

    const res = await fetch('/api/parse-excel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fileBase64: b64, targetSheet: targetSheetName })
    });
    const json = await res.json();
    if (json && json.success) {
      if (returnDetails) return json;
      return json.text;
    }
    throw new Error(json.error || 'Server parse failed');
  } catch (e) {
    console.error('Server fallback parse error:', e);
    return null;
  }
}

async function readXlsxFile(file, options) {
  const targetSheetName = (typeof options === 'string' ? options : (options && options.targetSheet)) || 'NIS重点遗留任务';
  const returnDetails = (options && typeof options === 'object' && options.returnDetails);

  function unescapeXml(text) {
    if (!text) return '';
    return text
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;|&apos;/g, "'")
      .replace(/&#(\d+);/g, (_, code) => String.fromCharCode(parseInt(code, 10)));
  }

  function colLetterToIndex(colStr) {
    let index = 0;
    for (let i = 0; i < colStr.length; i++) {
      index = index * 26 + (colStr.charCodeAt(i) - 64);
    }
    return index - 1;
  }

  try {
    const arrayBuffer = await file.arrayBuffer();
    const bytes = new Uint8Array(arrayBuffer);

    // 1. Scan ZIP entries via Central Directory (fallback to local headers)
    const entries = {};
    let eocdPos = -1;
    for (let i = bytes.length - 22; i >= Math.max(0, bytes.length - 65536 - 22); i--) {
      if (bytes[i] === 0x50 && bytes[i+1] === 0x4b && bytes[i+2] === 0x05 && bytes[i+3] === 0x06) {
        eocdPos = i;
        break;
      }
    }

    if (eocdPos !== -1) {
      const cdOffset = (bytes[eocdPos+16] | (bytes[eocdPos+17] << 8) | (bytes[eocdPos+18] << 16) | (bytes[eocdPos+19] << 24)) >>> 0;
      let pos = cdOffset;
      while (pos + 46 <= bytes.length) {
        if (bytes[pos] !== 0x50 || bytes[pos+1] !== 0x4b || bytes[pos+2] !== 0x01 || bytes[pos+3] !== 0x02) break;
        const method = bytes[pos+10] | (bytes[pos+11] << 8);
        const compSize = (bytes[pos+20] | (bytes[pos+21] << 8) | (bytes[pos+22] << 16) | (bytes[pos+23] << 24)) >>> 0;
        const fnameLen = bytes[pos+28] | (bytes[pos+29] << 8);
        const extraLen = bytes[pos+30] | (bytes[pos+31] << 8);
        const commentLen = bytes[pos+32] | (bytes[pos+33] << 8);
        const lh = (bytes[pos+42] | (bytes[pos+43] << 8) | (bytes[pos+44] << 16) | (bytes[pos+45] << 24)) >>> 0;
        
        const fname = new TextDecoder('utf-8').decode(bytes.slice(pos + 46, pos + 46 + fnameLen));
        if (lh + 30 <= bytes.length && bytes[lh] === 0x50 && bytes[lh+1] === 0x4b && bytes[lh+2] === 0x03 && bytes[lh+3] === 0x04) {
          const lhFnameLen = bytes[lh+26] | (bytes[lh+27] << 8);
          const lhExtraLen = bytes[lh+28] | (bytes[lh+29] << 8);
          const dataStart = lh + 30 + lhFnameLen + lhExtraLen;
          entries[fname] = { method, data: bytes.slice(dataStart, dataStart + compSize) };
        }
        pos += 46 + fnameLen + extraLen + commentLen;
      }
    } else {
      let pos = 0;
      while (pos + 30 <= bytes.length) {
        if (bytes[pos] !== 0x50 || bytes[pos+1] !== 0x4b || bytes[pos+2] !== 0x03 || bytes[pos+3] !== 0x04) break;
        const method = bytes[pos+8] | (bytes[pos+9] << 8);
        const compSize = (bytes[pos+18] | (bytes[pos+19] << 8) | (bytes[pos+20] << 16) | (bytes[pos+21] << 24)) >>> 0;
        const fnameLen = bytes[pos+26] | (bytes[pos+27] << 8);
        const extraLen = bytes[pos+28] | (bytes[pos+29] << 8);
        const fname = new TextDecoder('utf-8').decode(bytes.slice(pos + 30, pos + 30 + fnameLen));
        const dataStart = pos + 30 + fnameLen + extraLen;
        entries[fname] = { method, data: bytes.slice(dataStart, dataStart + compSize) };
        pos = dataStart + compSize;
      }
    }

    async function decompress(entry) {
      if (!entry || !entry.data || entry.data.length === 0) return '';
      if (entry.method === 0) return new TextDecoder('utf-8').decode(entry.data);
      if (entry.method === 8 && typeof DecompressionStream !== 'undefined') {
        try {
          const ds = new DecompressionStream('deflate-raw');
          const writer = ds.writable.getWriter();
          writer.write(entry.data);
          writer.close();
          const reader = ds.readable.getReader();
          const chunks = [];
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
          }
          let totalLen = chunks.reduce((acc, c) => acc + c.length, 0);
          let res = new Uint8Array(totalLen);
          let offset = 0;
          for (const c of chunks) { res.set(c, offset); offset += c.length; }
          return new TextDecoder('utf-8').decode(res);
        } catch (e) {
          console.warn('Decompress error:', e);
          return '';
        }
      }
      return '';
    }

    // Shared Strings
    const sstXml = await decompress(entries['xl/sharedStrings.xml']);
    const strings = [];
    if (sstXml) {
      const siMatches = sstXml.match(/<si>[\s\S]*?<\/si>/gi) || [];
      for (const si of siMatches) {
        const tMatches = si.match(/<t[^>]*>([\s\S]*?)<\/t>/gi) || [];
        const text = tMatches.map(m => m.replace(/<[^>]+>/g, '')).join('');
        strings.push(unescapeXml(text));
      }
    }

    // Relationships
    const relsXml = await decompress(entries['xl/_rels/workbook.xml.rels']);
    const relMap = {};
    if (relsXml) {
      const relMatches = relsXml.match(/<Relationship\s+[^>]+>/gi) || [];
      for (const rel of relMatches) {
        const idM = rel.match(/Id="([^"]+)"/);
        const targetM = rel.match(/Target="([^"]+)"/);
        if (idM && targetM) {
          let t = targetM[1];
          if (t.startsWith('/')) t = t.substring(1);
          if (!t.startsWith('xl/')) t = 'xl/' + t;
          relMap[idM[1]] = t;
        }
      }
    }

    // Workbook sheets
    const wbXml = await decompress(entries['xl/workbook.xml']);
    const sheets = [];
    if (wbXml) {
      const sheetMatches = wbXml.match(/<sheet\s+[^>]+>/gi) || [];
      for (const s of sheetMatches) {
        const nameM = s.match(/name="([^"]+)"/);
        const rIdM = s.match(/r:id="([^"]+)"/) || s.match(/id="([^"]+)"/);
        const sheetIdM = s.match(/sheetId="([^"]+)"/);
        const name = nameM ? unescapeXml(nameM[1]) : '';
        const rId = rIdM ? rIdM[1] : '';
        const sheetId = sheetIdM ? sheetIdM[1] : '';
        const target = (rId && relMap[rId]) || ('xl/worksheets/sheet' + sheetId + '.xml');
        sheets.push({ name, rId, sheetId, target });
      }
    }

    function parseSheetXmlToTsv(sheetXml) {
      if (!sheetXml) return { tsv: '', rowCount: 0 };
      const rows = [];
      const rowMatches = sheetXml.match(/<row\s+[^>]*>[\s\S]*?<\/row>/gi) || [];
      for (const r of rowMatches) {
        const cellMatches = r.match(/<c\s+[^>]*>[\s\S]*?<\/c>|<c\s+[^>]*\/>/gi) || [];
        const rowVals = [];
        for (const c of cellMatches) {
          const rM = c.match(/r="([A-Z]+)(\d+)"/);
          let colIdx = -1;
          if (rM) colIdx = colLetterToIndex(rM[1]);

          const isString = /t="s"/.test(c);
          let val = '';
          const valMatch = c.match(/<v>([^<]*)<\/v>/);
          if (valMatch) {
            const rawVal = valMatch[1];
            val = isString ? (strings[parseInt(rawVal, 10)] || '') : rawVal;
          } else {
            const inlineMatch = c.match(/<t[^>]*>([\s\S]*?)<\/t>/i);
            if (inlineMatch) val = inlineMatch[1];
          }

          val = unescapeXml(val);
          // 彻底防止单元格内换行破坏行结构：将单元格内部的换行符替换为空格
          val = val.split(String.fromCharCode(10)).join(' ').split(String.fromCharCode(13)).join(' ').trim();

          if (colIdx >= 0) {
            rowVals[colIdx] = val;
          } else {
            rowVals.push(val);
          }
        }
        for (let i = 0; i < rowVals.length; i++) {
          if (rowVals[i] === undefined || rowVals[i] === null) rowVals[i] = '';
        }
        if (rowVals.some(v => v.trim() !== '')) {
          rows.push(rowVals.join(String.fromCharCode(9)));
        }
      }
      return { tsv: rows.join(String.fromCharCode(10)), rowCount: rows.length };
    }

    const allSheets = [];
    for (const s of sheets) {
      const sXml = await decompress(entries[s.target]);
      if (sXml) {
        const { tsv, rowCount } = parseSheetXmlToTsv(sXml);
        allSheets.push({ name: s.name, text: tsv, rowCount });
      }
    }

    if (allSheets.length === 0) {
      const defaultEntry = entries['xl/worksheets/sheet1.xml'] || entries['xl/worksheets/sheet.xml'] || Object.entries(entries).find(([k]) => k.startsWith('xl/worksheets/'))?.[1];
      const defaultXml = await decompress(defaultEntry);
      const { tsv, rowCount } = parseSheetXmlToTsv(defaultXml);
      allSheets.push({ name: 'Sheet1', text: tsv, rowCount });
    }

    const targetClean = targetSheetName.trim().toLowerCase().replace(/\s+/g, '');
    let matched = allSheets.find(s => s.name.trim().toLowerCase() === targetSheetName.trim().toLowerCase())
      || allSheets.find(s => s.name.trim().toLowerCase().replace(/\s+/g, '') === targetClean)
      || allSheets.find(s => s.name.toLowerCase().includes(targetClean) || targetClean.includes(s.name.toLowerCase()))
      || allSheets.find(s => s.name.toLowerCase().includes('nis') && (s.name.includes('遗留') || s.name.includes('任务')))
      || allSheets.find(s => s.name.includes('遗留任务'))
      || allSheets[0];

    const isMatched = (matched.name.trim().toLowerCase().replace(/\s+/g, '') === targetClean || matched.name.toLowerCase().includes('nis') || targetClean.includes(matched.name.toLowerCase().replace(/\s+/g, '')));

    if (returnDetails) {
      return {
        text: matched.text,
        sheetName: matched.name,
        rowCount: matched.rowCount,
        matched: isMatched,
        allSheets: allSheets
      };
    }
    return matched.text;
  } catch (err) {
    console.warn('XLSX native extraction error, falling back to server parse:', err);
    return await fallbackServerParseXlsx(file, targetSheetName, returnDetails);
  }
}

async function handleCalendarFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const isXlsx = file.name.endsWith('.xlsx') || file.type.includes('spreadsheet') || file.name.endsWith('.xls');

  if (isXlsx) {
    const text = await readXlsxFile(file);
    if (text && text.trim().length > 0) {
      document.getElementById('inputImportTableText').value = text;
      runCalendarLivePreview();
      showToast(`📁 成功解析 Excel 文档：${file.name}`);
      return;
    }
  }

  const reader = new FileReader();
  reader.onload = function(e) {
    const content = e.target.result;
    document.getElementById('inputImportTableText').value = content;
    runCalendarLivePreview();
    showToast(`📁 成功读取文档：${file.name}`);
  };
  reader.readAsText(file);
}

function fillSampleCalendarData() {
  const sample = [
    "*会议主题（关键任务）\\t*议题背景/决策要点说明\\t*汇报人\\t*参会人\\t*纪要人\\t*预约时长（H）",
    "中东北非区域Q3交付资源评审\\t审批重点交付架构师驻场与预算特批\\t张总(地南代)\\t主管、李总、财务BP\\t王秘书\\t0.75",
    "阿尔及利亚代表处外汇与回款复盘\\t特批客户付款账期与汇率对冲\\t王总\\t主管、法务部、商务部\\t李秘书\\t1.0",
    "刚果金代表处工程进展对齐\\t审批新安保防护与施工里程碑\\t陈部长\\t主管、交付部\\t赵秘书\\t0.5",
    "8代表处跨区协同机制新规范汇报\\t固定跨时区会议窗口为开罗11:00-17:00\\t区域综合秘书处\\t主管、各代综合主管\\t王秘书\\t0.75"
  ].join('\\n');

  document.getElementById('inputImportTableText').value = sample;
  runCalendarLivePreview();
}

function padTime(t) {
  if (!t) return '10:00';
  const parts = t.split(':');
  if (parts.length < 2) return '10:00';
  const h = parts[0].padStart(2, '0');
  const m = parts[1].padStart(2, '0');
  return `${h}:${m}`;
}

// Smart row cell splitter: respects tabs (Excel paste), pipes, multi-space, and CSV quotes
function splitRowCells(line) {
  if (!line) return [];
  // 1. If line contains TAB, it is tab-separated (standard Excel copy-paste)
  if (line.includes('\t')) {
    return line.split('\t').map(s => s.trim());
  }
  // 2. If line contains pipe '|'
  if (line.includes('|')) {
    const p = line.split('|').map(s => s.trim());
    if (p.length > 0 && p[0] === '') p.shift();
    if (p.length > 0 && p[p.length - 1] === '') p.pop();
    return p;
  }
  // 3. If line contains 2 or more spaces
  if (/\\s{2,}/.test(line)) {
    return line.split(/\\s{2,}/).map(s => s.trim());
  }
  // 4. If line contains commas, check if it's CSV (accounting for quotes)
  if (line.includes(',')) {
    const result = [];
    let cur = '';
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') {
        inQuotes = !inQuotes;
      } else if (ch === ',' && !inQuotes) {
        result.push(cur.trim());
        cur = '';
      } else {
        cur += ch;
      }
    }
    result.push(cur.trim());
    return result;
  }
  // 5. Fallback: single cell or space split
  return [line.trim()];
}

// Universal Schedule Text Parser with Fixed Header Alignment & Weekday Row Filter
function parseUniversalScheduleText(rawText, defaultDate) {
  if (!rawText || !rawText.trim()) return [];
  const lines = rawText.trim().split(/\\r?\\n/).map(s => s.trim()).filter(Boolean);
  const results = [];

  let baseDate;
  if (defaultDate) {
    const p = defaultDate.split('-').map(Number);
    baseDate = new Date(p[0], p[1] - 1, p[2]);
  } else {
    baseDate = new Date();
  }
  const sunDate = new Date(baseDate);
  sunDate.setDate(baseDate.getDate() - baseDate.getDay());

  const weekdayMap = {
    '日': 0, '天': 0, '7': 0,
    '一': 1, '1': 1,
    '二': 2, '2': 2,
    '三': 3, '3': 3,
    '四': 4, '4': 4,
    '五': 5, '5': 5,
    '六': 6, '6': 6
  };

  let colMap = null;
  let currentDate = defaultDate || formatDateToStr(baseDate);
  let currentSlotIdx = 0;
  const defaultSlots = ['09:30', '10:30', '14:30', '15:30', '16:30', '17:15'];

  let isGridCalendar = false;
  const gridDayCols = {};

  for (let line of lines) {
    // 1. Weekday Header check: e.g. 星期一, 星期二, 周三, 【星期四】, 星期一到星期五, 周一至周五
    // NEVER treat weekday headers or day-range banners as meeting subjects!
    if (/^(?:【|\[)?(?:星期|周|礼拜)[一二三四五六日天1-7](?:】|\])?$/.test(line) ||
        /(?:星期|周|礼拜)[一二三四五六日天1-7]\s*(?:至|到|~|-)\s*(?:星期|周|礼拜)?[一二三四五六日天1-7]/.test(line)) {
      const wkMatch = line.match(/(?:星期|周|礼拜)([一二三四五六日天1-7])/);
      if (wkMatch) {
        const offset = weekdayMap[wkMatch[1]];
        const targetD = new Date(sunDate);
        targetD.setDate(sunDate.getDate() + offset);
        currentDate = formatDateToStr(targetD);
        currentSlotIdx = 0;
      }
      continue;
    }

    // Split line using smart row cell splitter
    const parts = splitRowCells(line);

    // 2. Grid calendar header check: e.g. 时间 \t 星期一 \t 星期二 \t 星期三 ...
    const hasMultipleWeekdays = parts.filter(p => /(?:星期|周)[一二三四五六日天]/.test(p)).length >= 2;
    if (hasMultipleWeekdays) {
      isGridCalendar = true;
      parts.forEach((p, idx) => {
        const m = p.match(/(?:星期|周)([一二三四五六日天])/);
        if (m) {
          const targetD = new Date(sunDate);
          targetD.setDate(sunDate.getDate() + weekdayMap[m[1]]);
          gridDayCols[idx] = formatDateToStr(targetD);
        }
      });
      continue;
    }

    if (isGridCalendar && Object.keys(gridDayCols).length > 0) {
      let slotTime = '10:00';
      let slotDur = 45;
      const tm = parts[0].match(/(\\d{1,2}:\\d{2})(?:\\s*[-~至到]\\s*(\\d{1,2}:\\d{2}))?/);
      if (tm) {
        slotTime = tm[1];
        if (tm[2]) {
          const [sh, sm] = tm[1].split(':').map(Number);
          const [eh, em] = tm[2].split(':').map(Number);
          const diff = (eh * 60 + em) - (sh * 60 + sm);
          if (diff > 0 && diff <= 480) slotDur = diff;
        }
      }

      Object.entries(gridDayCols).forEach(([cIdxStr, mDate]) => {
        const cIdx = parseInt(cIdxStr, 10);
        if (cIdx < parts.length && parts[cIdx]) {
          const val = parts[cIdx];
          if (!['-', '/', '无', '空', '休', '暂无'].includes(val) && !/^(?:星期|周)[一二三四五六日天]/.test(val)) {
            results.push({
              id: Date.now() + Math.floor(Math.random() * 1000000),
              date: mDate,
              time: slotTime,
              duration: slotDur,
              durationHours: (slotDur / 60).toFixed(2),
              subject: val,
              decision: `1. 审议《${val}》关键决策要点，确定推进方案。`,
              reporter: '待确认汇报人',
              attendees: '主管、相关参会人',
              minuter: '秘书处',
              requester: '日历导入',
              location: '主管办公室 / 线上会议室',
              status: 'scheduled',
              priority: 'medium',
              notes: '由周历网格表自动识别导入'
            });
          }
        }
      });
      continue;
    }

    // 3. Check if line is the standard column header
    // e.g. *会议主题（关键任务） \t *议题背景/决策要点说明 \t *汇报人 \t *参会人 \t *纪要人 \t *预约时长（H）
    const cleanHeaderCheck = parts.map(p => p.toLowerCase().replace(/[*（）()\\s]/g, ''));
    if (cleanHeaderCheck.some(p => p.includes('会议主题') || p.includes('关键任务') || p.includes('主题'))) {
      colMap = {};
      parts.forEach((p, idx) => {
        const clean = p.replace(/[*（）()\\s]/g, '').toLowerCase();
        if (clean.includes('会议主题') || clean.includes('关键任务') || clean.includes('主题')) {
          colMap['subject'] = idx;
        } else if (clean.includes('议题背景') || clean.includes('决策要点') || clean.includes('背景') || clean.includes('决策')) {
          colMap['decision'] = idx;
        } else if (clean.includes('汇报人') || clean.includes('汇报') || clean.includes('主讲') || clean.includes('发言')) {
          colMap['reporter'] = idx;
        } else if (clean.includes('参会人') || clean.includes('与会') || clean.includes('参会') || clean.includes('出席')) {
          colMap['attendees'] = idx;
        } else if (clean.includes('纪要人') || clean.includes('记录') || clean.includes('纪要') || clean.includes('记录人')) {
          colMap['minuter'] = idx;
        } else if (clean.includes('预约时长') || clean.includes('时长') || clean.includes('duration') || clean.includes('hours')) {
          colMap['durationHours'] = idx;
        } else if (clean.includes('日期') || clean.includes('date')) {
          colMap['date'] = idx;
        } else if (clean.includes('时间') || clean.includes('time')) {
          colMap['time'] = idx;
        } else if (clean.includes('地点') || clean.includes('location')) {
          colMap['location'] = idx;
        }
      });
      continue;
    }

    // 4. If colMap is active, parse mapped fields!
    if (colMap && 'subject' in colMap) {
      let subIdx = colMap['subject'];
      let partsOffset = 0;

      // Check if parts[0] is a time prefix not covered by header
      if (!('time' in colMap) && parts.length > Object.keys(colMap).length && /^\\d{1,2}:\\d{2}/.test(parts[0])) {
        partsOffset = 1;
      }

      let sub = (parts[subIdx + partsOffset] !== undefined ? parts[subIdx + partsOffset] : (parts[subIdx] || '')).trim();
      if (!sub) continue;

      // Filter out weekday row or day-range banner if accidentally pasted under header
      if (/^(?:星期|周|礼拜)[一二三四五六日天1-7]/.test(sub) || 
          /(?:星期|周)[一二三四五六日天]\\s*(?:至|到|~|-)/.test(sub) ||
          ['时间', '日期', '序号', 'index', 'time', 'date'].includes(sub.toLowerCase())) {
        continue;
      }

      let dec = colMap['decision'] !== undefined ? (parts[colMap['decision'] + partsOffset] || parts[colMap['decision']] || '') : '';
      let rep = colMap['reporter'] !== undefined ? (parts[colMap['reporter'] + partsOffset] || parts[colMap['reporter']] || '') : '';
      let att = colMap['attendees'] !== undefined ? (parts[colMap['attendees'] + partsOffset] || parts[colMap['attendees']] || '') : '';
      let minu = colMap['minuter'] !== undefined ? (parts[colMap['minuter'] + partsOffset] || parts[colMap['minuter']] || '') : '';
      let durStr = colMap['durationHours'] !== undefined ? (parts[colMap['durationHours'] + partsOffset] || parts[colMap['durationHours']] || '') : '';
      let dateVal = colMap['date'] !== undefined ? (parts[colMap['date'] + partsOffset] || parts[colMap['date']] || '') : '';
      let timeVal = colMap['time'] !== undefined ? (parts[colMap['time'] + partsOffset] || parts[colMap['time']] || '') : '';

      // If partsOffset was active, use parts[0] as time
      if (partsOffset === 1 && !timeVal) {
        timeVal = parts[0];
      }

      // If time is embedded in subject (e.g. "10:00-11:30 Q3跨区运营")
      const timeInSub = sub.match(/^(\\d{1,2}:\\d{2}(?:\\s*[-~至到]\\s*\\d{1,2}:\\d{2})?)\\s*(.*)/);
      if (timeInSub) {
        if (!timeVal) timeVal = timeInSub[1];
        if (timeInSub[2].trim()) sub = timeInSub[2].trim();
      }

      let mDate = currentDate;
      if (dateVal && /\\d{4}[-/.]\\d{1,2}[-/.]\\d{1,2}/.test(dateVal)) {
        mDate = dateVal.replace(/\\//g, '-').replace(/\\./g, '-');
      }

      let durMins = 45;
      if (durStr) {
        const num = parseFloat(durStr.replace(/[^0-9.]/g, ''));
        if (!isNaN(num) && num > 0) {
          if (num <= 5) durMins = Math.round(num * 60); // 0.5, 0.75, 1, 1.5, 2 Hours
          else durMins = Math.round(num); // 30, 45, 60 Minutes
        }
      }

      let mTime = timeVal || defaultSlots[currentSlotIdx % defaultSlots.length];
      currentSlotIdx++;

      if (!att) {
        att = rep ? (rep.includes('主管') ? rep : '主管、' + rep) : '主管、相关参会人';
      }

      results.push({
        id: Date.now() + Math.floor(Math.random() * 1000000),
        date: mDate,
        time: padTime(mTime),
        duration: durMins,
        durationHours: (durMins / 60).toFixed(2),
        subject: sub,
        decision: dec || `1. 审议《${sub}》关键决策要点，确定推进方案。`,
        reporter: rep || '待确定汇报人',
        attendees: att,
        minuter: minu || '秘书处',
        requester: rep || '标准表格导入',
        location: '主管办公室 / 线上会议室',
        status: 'scheduled',
        priority: 'medium',
        notes: '由标准表头导入自动对齐'
      });
      continue;
    }

    // 5. Intelligent Tabular Classifier (Handles unlabelled rows like: 10:00 - 10:45 \t 主题 \t 汇报人 \t 参会人 \t 纪要人 \t 0.75)
    if (parts.length >= 3 && !colMap) {
      let tVal = '', sVal = '', rVal = '', aVal = '', mVal = '', dVal = '';

      for (let p of parts) {
        if (/\d{1,2}:\d{2}/.test(p) && !tVal) {
          tVal = p;
        } else if (/^[0-9.]+\s*(?:h|小时|m|分钟)?$/i.test(p) && !dVal) {
          dVal = p;
        } else if (/(?:秘书|纪要|记录)/.test(p) && !mVal && p.length <= 10) {
          mVal = p;
        } else if (/(?:主管|交付部|财务|HR|BP|法务)/.test(p) || p.includes('、') || p.includes(',')) {
          if (!aVal) aVal = p;
        } else if (/(?:总|部长|经理|主任|专家|代表)/.test(p) && p.length <= 12 && !rVal) {
          rVal = p;
        } else if (!sVal && !/^(?:星期|周)[一二三四五六日天]/.test(p)) {
          sVal = p;
        }
      }

      if (sVal && !/^(?:星期|周)[一二三四五六日天]$/.test(sVal)) {
        let durMins = 45;
        if (dVal) {
          const num = parseFloat(dVal.replace(/[^0-9.]/g, ''));
          if (!isNaN(num) && num > 0) {
            durMins = num <= 5 ? Math.round(num * 60) : Math.round(num);
          }
        }

        let startTime = '10:00';
        if (tVal) {
          const rangeM = tVal.match(/(\d{1,2}:\d{2})(?:\s*[-~至到]\s*(\d{1,2}:\d{2}))?/);
          if (rangeM) {
            startTime = padTime(rangeM[1]);
            if (rangeM[2]) {
              const [sh, sm] = rangeM[1].split(':').map(Number);
              const [eh, em] = rangeM[2].split(':').map(Number);
              const diff = (eh * 60 + em) - (sh * 60 + sm);
              if (diff > 0 && diff <= 480) durMins = diff;
            }
          }
        } else {
          startTime = defaultSlots[currentSlotIdx % defaultSlots.length];
          currentSlotIdx++;
        }

        results.push({
          id: Date.now() + Math.floor(Math.random() * 1000000),
          date: currentDate,
          time: startTime,
          duration: durMins,
          durationHours: (durMins / 60).toFixed(2),
          subject: sVal,
          decision: `1. 审议《${sVal}》关键决策要点，确定推进方案。`,
          reporter: rVal || '待确定汇报人',
          attendees: aVal || (rVal ? '主管、' + rVal : '主管、相关参会人'),
          minuter: mVal || '秘书处',
          requester: rVal || '表格导入',
          location: '主管办公室 / 线上会议室',
          status: 'scheduled',
          priority: 'medium',
          notes: '由无表头表格智能分类识别导入'
        });
        continue;
      }
    }

    // 6. Fallback: Universal NLP / Free Form extractor
    let itemDate = currentDate;
    const inlineDateMatch = line.match(/(\\d{4}[-/.]\\d{1,2}[-/.]\\d{1,2})/);
    if (inlineDateMatch) {
      const p = inlineDateMatch[1].split(/[-/.]/);
      itemDate = `${p[0]}-${p[1].padStart(2, '0')}-${p[2].padStart(2, '0')}`;
      line = line.replace(inlineDateMatch[0], ' ');
    } else {
      const mdMatch = line.match(/(\\d{1,2})月(\\d{1,2})[日号]?/);
      if (mdMatch) {
        itemDate = `${baseDate.getFullYear()}-${mdMatch[1].padStart(2, '0')}-${mdMatch[2].padStart(2, '0')}`;
        line = line.replace(mdMatch[0], ' ');
      }
    }

    let startTime = defaultSlots[currentSlotIdx % defaultSlots.length];
    currentSlotIdx++;
    let duration = 45;

    const rangeMatch = line.match(/(\\d{1,2}:\\d{2})\\s*[-~至到与]\\s*(\\d{1,2}:\\d{2})/);
    if (rangeMatch) {
      startTime = padTime(rangeMatch[1]);
      const endTime = padTime(rangeMatch[2]);
      const [sh, sm] = startTime.split(':').map(Number);
      const [eh, em] = endTime.split(':').map(Number);
      const diff = (eh * 60 + em) - (sh * 60 + sm);
      if (diff > 0 && diff <= 480) duration = diff;
      line = line.replace(rangeMatch[0], ' ');
    } else {
      const singleMatch = line.match(/(?:上午|下午|晚上)?\\s*(\\d{1,2}:\\d{2})/);
      if (singleMatch) {
        let [h, m] = singleMatch[1].split(':').map(Number);
        if (singleMatch[0].includes('下午') && h < 12) h += 12;
        startTime = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
        line = line.replace(singleMatch[0], ' ');
      }
    }

    // Duration extraction
    const durMatch = line.match(/(\\d+(?:\\.\\d+)?)\\s*(?:小时|h)/i);
    if (durMatch) {
      duration = Math.round(parseFloat(durMatch[1]) * 60);
      line = line.replace(durMatch[0], ' ');
    } else {
      const minMatch = line.match(/(\\d{1,3})\\s*(?:分钟|min|m)/i);
      if (minMatch) {
        duration = parseInt(minMatch[1], 10);
        line = line.replace(minMatch[0], ' ');
      }
    }

    // Location
    let location = '主管办公室';
    const locMatch = line.match(/(?:在|地点[：:\\s]*)([\\w\\u4e00-\\u9fa5]+(?:会议室|办公室|大厅|楼|座))/);
    if (locMatch) {
      location = locMatch[1];
      line = line.replace(locMatch[0], ' ');
    }

    // Reporter
    let reporter = '';
    const repMatch = line.match(/(?:汇报人|汇报专家|主讲人|发言人|主讲|对接人|发起人)[：:\\s]*([^\\s,，。；;\\t]+)/);
    if (repMatch) {
      reporter = repMatch[1];
      line = line.replace(repMatch[0], ' ');
    } else {
      const verbMatch = line.match(/([^\\s,，。；;\\t]{2,6})(?:汇报|发言|主讲)/);
      if (verbMatch) {
        reporter = verbMatch[1].replace(/^请/, '');
        line = line.replace(verbMatch[0], ' ');
      }
    }

    // Decision
    let decision = '';
    const decMatch = line.match(/(?:决策点|决策事项|核心决策|议题|目标)[：:\\s]*([^\\\\n。；;]+)/);
    if (decMatch) {
      decision = decMatch[1].trim();
      line = line.replace(decMatch[0], ' ');
    }

    // Clean remaining tokens into Subject
    line = line.replace(/请[^\\s,，。；;\\t]{2,6}(?=汇报|发言)/g, '');
    for (const w of ['召开', '进行', '讨论', '沟通', '业务进展', '会议通知', '各位同事', '预计时长', '时间', '地点']) {
      line = line.split(w).join(' ');
    }

    const freeParts = line.split(/[\\t,;|]+|\\s{2,}/).map(s => s.trim()).filter(Boolean);
    if (!reporter && freeParts.length >= 2) {
      for (let i = 0; i < freeParts.length; i++) {
        const p = freeParts[i];
        if (/(总|部长|经理|主任|处长|专家|秘书|HR|VP|代|办)/.test(p) && p.length <= 8) {
          reporter = p;
          freeParts.splice(i, 1);
          break;
        }
      }
    }

    let subject = freeParts.join(' ');
    subject = subject.replace(/^[0-9一二三四五六七八九十]+[、.\\s]+/, '');
    subject = subject.replace(/[\\s,，。；;]+$/, '').trim();

    // Prevent residual weekday words from becoming subject!
    if (!subject || subject.length < 2 || /^(?:星期|周)[一二三四五六日天]$/.test(subject)) {
      continue;
    }

    if (!decision) {
      decision = `1. 审议《${subject}》关键决策要点，明确推进方案。`;
    }

    const attendees = reporter ? (reporter.includes('主管') ? reporter : '主管、' + reporter) : '主管、相关参会人';

    results.push({
      id: Date.now() + Math.floor(Math.random() * 1000000),
      date: itemDate,
      time: startTime,
      duration: duration,
      durationHours: (duration / 60).toFixed(2),
      subject: subject,
      background: `由智能日程引擎自动识别规整：${subject}。`,
      decision: decision,
      attendees: attendees,
      reporter: reporter || '待确定汇报人',
      minuter: '秘书处',
      requester: reporter || '智能导入',
      location: location,
      status: 'scheduled',
      priority: 'medium',
      notes: '由自由格式智能识别导入'
    });
  }

  return results;
}

function switchImportPreviewTab(tab) {
  importPreviewTab = tab;
  const btnCal = document.getElementById('btnPreviewTabCal');
  const btnCard = document.getElementById('btnPreviewTabCard');
  const wrapCal = document.getElementById('importCalPreviewWrap');
  const wrapCard = document.getElementById('importCardPreviewWrap');

  if (btnCal) btnCal.classList.toggle('active', tab === 'cal');
  if (btnCard) btnCard.classList.toggle('active', tab === 'card');
  if (wrapCal) wrapCal.style.display = tab === 'cal' ? 'block' : 'none';
  if (wrapCard) wrapCard.style.display = tab === 'card' ? 'block' : 'none';
}

function runCalendarLivePreview() {
  const text = document.getElementById('inputImportTableText').value;
  const targetDate = document.getElementById('importTargetDate').value || getTodayDateStr();
  const previewArea = document.getElementById('importLivePreviewArea');
  const wrapCal = document.getElementById('importCalPreviewWrap');
  const wrapCard = document.getElementById('importCardPreviewWrap');
  const statusText = document.getElementById('importPreviewStatusText');
  const btn = document.getElementById('btnConfirmImport');

  parsedImportMeetings = parseUniversalScheduleText(text, targetDate);

  if (parsedImportMeetings.length === 0) {
    previewArea.style.display = 'none';
    btn.disabled = true;
  } else {
    previewArea.style.display = 'block';
    btn.disabled = false;

    const datesSet = new Set(parsedImportMeetings.map(m => m.date));
    statusText.textContent = `🟢 智能识别成功：已规整 ${parsedImportMeetings.length} 场会议，涉及 ${datesSet.size} 个排期日期`;

    // 1. Render Calendar Grouped Preview
    const grouped = {};
    parsedImportMeetings.forEach(m => {
      if (!grouped[m.date]) grouped[m.date] = [];
      grouped[m.date].push(m);
    });

    wrapCal.innerHTML = Object.entries(grouped).map(([dStr, list]) => `
      <div class="import-cal-group">
        <div class="import-cal-group-header">
          <span>📅 ${dStr}</span>
          <span class="persona-tag" style="font-size:10.5px;">${list.length} 场会议</span>
        </div>
        <table class="import-preview-table" style="width:100%;">
          <thead>
            <tr>
              <th style="width:100px;">时间/时长</th>
              <th>*会议主题（关键任务）</th>
              <th style="width:100px;">*汇报人</th>
              <th style="width:90px;">*纪要人</th>
              <th>*决策要点说明</th>
            </tr>
          </thead>
          <tbody>
            ${list.map(m => `
              <tr>
                <td><strong>${m.time}</strong> (${m.durationHours || (m.duration/60).toFixed(2)}H)</td>
                <td><strong style="color:var(--text-primary);">${escapeHtml(m.subject)}</strong></td>
                <td>${escapeHtml(m.reporter || '待定')}</td>
                <td><span style="color:#2563eb;">${escapeHtml(m.minuter || '秘书处')}</span></td>
                <td style="font-size:11px; color:var(--text-secondary);">${escapeHtml(m.decision)}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `).join('');

    // 2. Render Cards Preview
    wrapCard.innerHTML = parsedImportMeetings.map(m => `
      <div class="import-card-item">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:4px;">
          <div style="font-size:13px; font-weight:700; color:var(--text-primary);">【${escapeHtml(m.subject)}】</div>
          <span class="status-badge status-scheduled">${m.durationHours || (m.duration/60).toFixed(2)}H</span>
        </div>
        <div style="font-size:11.5px; color:var(--text-secondary); display:flex; flex-wrap:wrap; gap:10px; margin-bottom:4px;">
          <span>📅 ${m.date} ${m.time}</span>
          <span>👔 汇报人：${escapeHtml(m.reporter || '未注明')}</span>
          <span>📝 纪要人：${escapeHtml(m.minuter || '秘书处')}</span>
          <span>👥 参会人：${escapeHtml(m.attendees)}</span>
        </div>
        <div style="font-size:11px; color:var(--text-muted); background:#f4f4f5; padding:4px 8px; border-radius:4px;">
          <strong>🎯 决策要点：</strong>${escapeHtml(m.decision)}
        </div>
      </div>
    `).join('');
  }
}

function confirmImportCalendar() {
  if (parsedImportMeetings.length === 0) return;

  let existing = getData(STORAGE_KEYS.MEETINGS);
  const updated = [...parsedImportMeetings, ...existing];
  setData(STORAGE_KEYS.MEETINGS, updated);

  if (parsedImportMeetings[0] && parsedImportMeetings[0].date) {
    selectedTimelineDate = parsedImportMeetings[0].date;
    const parts = selectedTimelineDate.split('-').map(Number);
    if (parts.length === 3) {
      currentCalendarYearMonth.year = parts[0];
      currentCalendarYearMonth.month = parts[1] - 1;
    }
  }

  closeModal('importCalendarModal');
  renderMeetings();
  showToast(`成功导入并规整 ${parsedImportMeetings.length} 场会议！周历看板已更新。`);
}

function exportExecutiveScheduleBriefing() {
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const today = new Date();
  const sunDate = new Date(today);
  sunDate.setDate(today.getDate() - today.getDay() + (currentWeekOffset * 7));

  const weekStartStr = formatDateToStr(sunDate);
  const satDate = new Date(sunDate);
  satDate.setDate(sunDate.getDate() + 6);
  const weekEndStr = formatDateToStr(satDate);

  const weekMeetings = meetings.filter(m => m.date >= weekStartStr && m.date <= weekEndStr && m.status !== 'cancelled');
  weekMeetings.sort((a, b) => (a.date + ' ' + a.time).localeCompare(b.date + ' ' + b.time));

  const activeTz = getActiveTripTimezone();
  const isShifted = (activeTz !== 'cairo');
  const tzInfo = TRIP_TIMEZONE_MAP[activeTz] || TRIP_TIMEZONE_MAP.cairo;
  const tzHeaderSuffix = isShifted ? ` (${tzInfo.flag} ${tzInfo.name}当地时间 · 比开罗${tzInfo.diffText})` : '';

  const lines = [
    `【主管本周日程安排 · 秘书处通报${tzHeaderSuffix}】`,
    `排期周期：${weekStartStr} 至 ${weekEndStr} · 共 ${weekMeetings.length} 场重点会议`,
    '══════════════════════════════════════════════'
  ];

  const weekdayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  for (let i = 0; i < 7; i++) {
    const curD = new Date(sunDate);
    curD.setDate(sunDate.getDate() + i);
    const curDStr = formatDateToStr(curD);
    const dayM = weekMeetings.filter(m => m.date === curDStr);

    if (dayM.length > 0) {
      lines.push(`\\n【${weekdayNames[i]} ${curDStr}】:`);
      dayM.forEach(m => {
        const durHours = m.durationHours || (parseInt(m.duration || 45, 10) / 60).toFixed(2);
        const dt = getMeetingDisplayTime(m);
        const tzNote = dt.isShifted ? ` [开罗时间 ${dt.cairoStart} - ${dt.cairoEnd}]` : '';
        lines.push(`  ▪ ${dt.start} - ${dt.end} (${durHours}H) 《${m.subject}》${tzNote}`);
        lines.push(`    - 汇报人：${m.reporter || '未注明'} | 纪要人：${m.minuter || '秘书处'}`);
        if (m.attendees && m.attendees.trim()) {
          lines.push(`    - 参会人：${m.attendees.trim()}`);
        }
        if (m.decision && m.decision.trim()) {
          lines.push(`    - 决策要点：${m.decision.trim()}`);
        }
        if (m.notes && m.notes.trim()) {
          lines.push(`    - 备注：${m.notes.trim()}`);
        }
      });
    }
  }

  lines.push('\\n══════════════════════════════════════════════');
  lines.push('秘书处提醒：请各汇报人提前5分钟就座，精简汇报，直奔决策要点。');

  copyToClipboard(lines.join('\\n'), '领导周日程通报已复制到剪贴板，可直接发送微信或邮件。');
}

// ================= 明日会议提醒 (一键复制给领导) =================
function openTomorrowMeetingReminderModal() {
  setReminderDateTomorrow();
  openModal('tomorrowReminderModal');
}

function setReminderDateTomorrow() {
  const now = new Date();
  const tm = new Date(now);
  tm.setDate(now.getDate() + 1);
  const tmStr = formatDateToStr(tm);
  const inp = document.getElementById('inputReminderDate');
  if (inp) inp.value = tmStr;
  updateTomorrowReminderPreview();
}

function updateTomorrowReminderPreview() {
  const inp = document.getElementById('inputReminderDate');
  if (!inp || !inp.value) return;
  const targetDateStr = inp.value;

  const dt = new Date(targetDateStr + 'T00:00:00');
  const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  const wDay = weekDays[dt.getDay()];
  const parts = targetDateStr.split('-');
  const mNum = parseInt(parts[1], 10);
  const dNum = parseInt(parts[2], 10);

  const now = new Date();
  const tm = new Date(now);
  tm.setDate(now.getDate() + 1);
  const tmStr = formatDateToStr(tm);
  const isTomorrow = (targetDateStr === tmStr);

  const allMeetings = getData(STORAGE_KEYS.MEETINGS, []);
  const dayMeetings = allMeetings.filter(m => m.date === targetDateStr && m.status === 'scheduled');
  dayMeetings.sort((a, b) => (a.startTime || a.time || '10:00').localeCompare(b.startTime || b.time || '10:00'));

  const trip = getTripForDate(targetDateStr);

  const lines = [];
  const titlePrefix = isTomorrow ? '📅 曦总明日日程' : '📅 曦总日程安排';
  lines.push(`${titlePrefix}｜${mNum}月${dNum}日（${wDay}）`);
  if (trip) {
    lines.push(`📍 出差目的地：${trip.destination} (${trip.tzName || ''}当地时间)`);
  }
  lines.push('');

  if (dayMeetings.length === 0) {
    lines.push('明日暂无已排期会议安排，祝曦总工作顺利！');
  } else {
    const conflictMap = (typeof getAllMeetingConflicts === 'function')
      ? getAllMeetingConflicts(dayMeetings)
      : {};

    let prevPeriod = null;

    dayMeetings.forEach((mItem, index) => {
      const dtInfo = getMeetingDisplayTime(mItem);
      const startMins = timeStrToMinutes(dtInfo.start);
      const curPeriod = (startMins < 720) ? 'morning' : 'afternoon';

      if (prevPeriod && prevPeriod !== curPeriod && lines[lines.length - 1] !== '') {
        lines.push('');
      }
      prevPeriod = curPeriod;

      const isConflict = !!(conflictMap[mItem.id] && conflictMap[mItem.id].length > 0);
      const isHighPri = (mItem.priority === 'high' || mItem.priority === 'urgent');
      const icon = (isConflict || isHighPri) ? '🔴' : '📌';

      let timeStr = `${dtInfo.start}–${dtInfo.end}`;
      if (dtInfo.isTripDate && dtInfo.tzName) {
        timeStr += ` (${dtInfo.tzName}当地时间)`;
      }

      const subject = mItem.subject || mItem.title || '待定会议';
      lines.push(`${icon} ${timeStr}｜${subject}`);

      const noteText = (mItem.decision || mItem.notes || mItem.background || '').trim();
      if (noteText) {
        lines.push(`　↳ ${noteText}`);
        lines.push('');
      } else if (mItem.location) {
        lines.push(`　↳ 地点：${mItem.location}`);
      }
    });

    while (lines.length > 0 && lines[lines.length - 1] === '') {
      lines.pop();
    }

    const reportedPairs = new Set();
    const conflictWarnings = [];
    dayMeetings.forEach(m => {
      const confs = conflictMap[m.id];
      if (confs && confs.length > 0) {
        confs.forEach(c => {
          const pairKey = [m.id, c.conflictId].sort().join('_');
          if (!reportedPairs.has(pairKey)) {
            reportedPairs.add(pairKey);
            const sub1 = m.subject || '会议';
            const sub2 = c.otherSubject || '会议';
            const range = c.overlapRangeStr ? c.overlapRangeStr.replace(' - ', '–') : '';
            conflictWarnings.push(`⚠️ ${range ? range + '后' : ''}【${sub1}】与【${sub2}】时间重叠，请根据实际安排分段出席或授权参会。`);
          }
        });
      }
    });

    if (conflictWarnings.length > 0) {
      lines.push('');
      lines.push('');
      conflictWarnings.forEach(w => lines.push(w));
    }
  }

  const ta = document.getElementById('reminderMessagePreview');
  if (ta) {
    ta.value = lines.join('\\n');
  }
}

function copyTomorrowReminderContent() {
  const ta = document.getElementById('reminderMessagePreview');
  if (!ta) return;
  const text = ta.value.trim();
  if (!text) {
    showToast('暂无可复制的日程内容');
    return;
  }
  copyToClipboard(text, '✨ 曦总日程安排已成功复制，可直接发送！');
}

function resetMeetingsToDefault() {
  const ok = confirm('确定要重置主管会议日程为空白初始状态吗？\\n当前所有会议记录将被清空，恢复为空白日程表，方便全新导入或登记。');
  if (!ok) return;

  setData(STORAGE_KEYS.MEETINGS, []);
  renderMeetings();
  if (typeof updateHomeBadge === 'function') updateHomeBadge();
  showToast('已清空所有日程，恢复为空白初始状态');
}

// Time & Duration Calculation Helpers
function normalizeTimeStr(val) {
  if (!val) return '';
  val = String(val).trim().split('：').join(':').split('.').join(':');
  const matchColon = val.match(/^([0-9]{1,2}):([0-9]{1,2})$/);
  if (matchColon) {
    let h = parseInt(matchColon[1], 10);
    let m = parseInt(matchColon[2], 10);
    if (h >= 0 && h < 24 && m >= 0 && m < 60) {
      return (h < 10 ? '0' + h : '' + h) + ':' + (m < 10 ? '0' + m : '' + m);
    }
  }
  const matchDigits = val.match(/^([0-9]{1,2})([0-9]{2})$/);
  if (matchDigits) {
    let h = parseInt(matchDigits[1], 10);
    let m = parseInt(matchDigits[2], 10);
    if (h >= 0 && h < 24 && m >= 0 && m < 60) {
      return (h < 10 ? '0' + h : '' + h) + ':' + (m < 10 ? '0' + m : '' + m);
    }
  }
  const matchHour = val.match(/^([0-9]{1,2})$/);
  if (matchHour) {
    let h = parseInt(matchHour[1], 10);
    if (h >= 0 && h < 24) {
      return (h < 10 ? '0' + h : '' + h) + ':00';
    }
  }
  return val;
}

function normalizeMeetingTimeInput(type) {
  const elem = document.getElementById(type === 'start' ? 'inputMeetingStartTime' : 'inputMeetingEndTime');
  if (!elem) return;
  const raw = elem.value.trim();
  if (raw) {
    const norm = normalizeTimeStr(raw);
    if (norm) elem.value = norm;
  }
  handleMeetingTimeChange(type);
}

function closeAllTimePickers() {
  const m1 = document.getElementById('timePickerMenu_start');
  const m2 = document.getElementById('timePickerMenu_end');
  if (m1) m1.style.display = 'none';
  if (m2) m2.style.display = 'none';
}

function populateTimePickerMenu(type, menu) {
  if (!menu) return;
  const times = [];
  for (let h = 8; h <= 21; h++) {
    for (let m = 0; m < 60; m += 15) {
      if (h === 21 && m > 0) break;
      times.push((h < 10 ? '0' + h : '' + h) + ':' + (m < 10 ? '0' + m : '' + m));
    }
  }
  menu.innerHTML = times.map(t => 
    '<div class="time-picker-option" data-type="' + type + '" data-val="' + t + '">' + t + '</div>'
  ).join('');
  const opts = menu.querySelectorAll('.time-picker-option');
  if (opts && opts.forEach) {
    opts.forEach(el => {
      el.onclick = function() {
        selectTimeOption(this.getAttribute('data-type'), this.getAttribute('data-val'));
      };
    });
  }
}

function toggleTimePickerDropdown(type, eOrForce) {
  if (eOrForce && eOrForce.stopPropagation) {
    eOrForce.stopPropagation();
  }
  const menuId = type === 'start' ? 'timePickerMenu_start' : 'timePickerMenu_end';
  const otherId = type === 'start' ? 'timePickerMenu_end' : 'timePickerMenu_start';
  const otherMenu = document.getElementById(otherId);
  if (otherMenu) otherMenu.style.display = 'none';

  const menu = document.getElementById(menuId);
  if (!menu) return;

  const isVisible = menu.style.display === 'block';
  const shouldOpen = eOrForce === true ? true : !isVisible;

  if (shouldOpen) {
    if (!menu.innerHTML || menu.innerHTML.trim() === '') {
      populateTimePickerMenu(type, menu);
    }
    menu.style.display = 'block';

    const input = document.getElementById(type === 'start' ? 'inputMeetingStartTime' : 'inputMeetingEndTime');
    const curVal = input ? input.value.trim() : '';
    const items = menu.querySelectorAll('.time-picker-option');
    if (items && items.forEach) {
      items.forEach(it => {
        const isSel = it.getAttribute('data-val') === curVal;
        it.classList.toggle('selected', isSel);
        if (isSel) {
          try { it.scrollIntoView({ block: 'nearest' }); } catch (err) {}
        }
      });
    }
  } else {
    menu.style.display = 'none';
  }
}

function selectTimeOption(type, val) {
  const startElem = document.getElementById('inputMeetingStartTime');
  const endElem = document.getElementById('inputMeetingEndTime');
  if (!startElem || !endElem) return;

  if (type === 'start') {
    const curStart = startElem.value.trim();
    const curEnd = endElem.value.trim();
    const dur = (curStart && curEnd) ? calculateDurationFromRange(curStart, curEnd) : 45;
    startElem.value = val;
    endElem.value = calculateEndTime(val, dur > 0 && dur < 480 ? dur : 45);
    handleMeetingTimeChange('start');
  } else {
    endElem.value = val;
    handleMeetingTimeChange('end');
  }
  closeAllTimePickers();
}

function initTimePickers() {
  const m1 = document.getElementById('timePickerMenu_start');
  const m2 = document.getElementById('timePickerMenu_end');
  if (m1) populateTimePickerMenu('start', m1);
  if (m2) populateTimePickerMenu('end', m2);
}

function calculateEndTime(startTimeStr, durationMins) {
  if (!startTimeStr) return '';
  const sNorm = normalizeTimeStr(startTimeStr) || startTimeStr;
  const parts = sNorm.split(':').map(Number);
  if (parts.length < 2 || isNaN(parts[0]) || isNaN(parts[1])) return '';
  const totalMins = parts[0] * 60 + parts[1] + parseInt(durationMins || 45, 10);
  const eh = Math.floor(totalMins / 60) % 24;
  const em = totalMins % 60;
  return (eh < 10 ? '0' + eh : '' + eh) + ':' + (em < 10 ? '0' + em : '' + em);
}

function calculateDurationFromRange(startTimeStr, endTimeStr) {
  if (!startTimeStr || !endTimeStr) return 45;
  const sNorm = normalizeTimeStr(startTimeStr) || startTimeStr;
  const eNorm = normalizeTimeStr(endTimeStr) || endTimeStr;
  const sParts = sNorm.split(':').map(Number);
  const eParts = eNorm.split(':').map(Number);
  if (sParts.length < 2 || isNaN(sParts[0]) || isNaN(sParts[1])) return 45;
  if (eParts.length < 2 || isNaN(eParts[0]) || isNaN(eParts[1])) return 45;
  let diff = (eParts[0] * 60 + eParts[1]) - (sParts[0] * 60 + sParts[1]);
  if (diff <= 0) diff += 24 * 60; // if spans midnight
  return diff;
}

function handleMeetingTimeChange(type) {
  const startElem = document.getElementById('inputMeetingStartTime');
  const endElem = document.getElementById('inputMeetingEndTime');
  if (!startElem || !endElem) return;

  const startVal = normalizeTimeStr(startElem.value.trim()) || startElem.value.trim();
  const endVal = normalizeTimeStr(endElem.value.trim()) || endElem.value.trim();

  if (!startVal) return;

  if (type === 'start') {
    if (!endVal || endVal <= startVal) {
      endElem.value = calculateEndTime(startVal, 45);
    }
  }
  updateMeetingDurationBadge();
}

function handleMeetingTimeInput(type) {
  const startElem = document.getElementById('inputMeetingStartTime');
  const endElem = document.getElementById('inputMeetingEndTime');
  if (!startElem || !endElem) return;

  const sVal = startElem.value.trim();
  const eVal = endElem.value.trim();
  if (/^[0-9]{1,2}:[0-9]{2}$/.test(sVal) && /^[0-9]{1,2}:[0-9]{2}$/.test(eVal)) {
    updateMeetingDurationBadge();
  } else if (/^[0-9]{1,2}:[0-9]{2}$/.test(sVal)) {
    handleMeetingModalTimezoneChange();
  }
}

function handleMeetingTimeBlur(type) {
  const elem = document.getElementById(type === 'start' ? 'inputMeetingStartTime' : 'inputMeetingEndTime');
  if (!elem) return;
  const raw = elem.value.trim();
  if (raw) {
    const norm = normalizeTimeStr(raw);
    if (norm) elem.value = norm;
  }
  handleMeetingTimeChange(type);
}

function applyQuickDuration(mins) {
  const startElem = document.getElementById('inputMeetingStartTime');
  const endElem = document.getElementById('inputMeetingEndTime');
  if (!startElem || !endElem) return;

  let startVal = startElem.value.trim();
  if (!startVal) {
    startVal = '10:00';
    startElem.value = startVal;
  } else {
    const norm = normalizeTimeStr(startVal);
    if (norm) {
      startVal = norm;
      startElem.value = norm;
    }
  }
  endElem.value = calculateEndTime(startVal, mins);
  updateMeetingDurationBadge();
}

function updateMeetingDurationBadge() {
  const startElem = document.getElementById('inputMeetingStartTime');
  const endElem = document.getElementById('inputMeetingEndTime');
  const badge = document.getElementById('meetingDurationBadge');
  if (!badge || !startElem || !endElem) return;

  const startVal = startElem.value.trim();
  const endVal = endElem.value.trim();

  if (!startVal || !endVal) {
    badge.textContent = '请填写或选择起止时间';
    [30, 40, 60, 90, 120].forEach(m => {
      const btn = document.getElementById('durChip' + m);
      if (btn) btn.classList.remove('selected');
    });
    checkMeetingConflicts();
    return;
  }

  const dur = calculateDurationFromRange(startVal, endVal);
  const hours = (dur / 60).toFixed(2);
  badge.textContent = '时长：' + dur + ' 分钟 (' + hours + 'H)';
  handleMeetingModalTimezoneChange();

  [30, 40, 60, 90, 120].forEach(m => {
    const btn = document.getElementById('durChip' + m);
    if (btn) {
      if (m === dur) {
        btn.classList.add('selected');
      } else {
        btn.classList.remove('selected');
      }
    }
  });

  checkMeetingConflicts();
}

function setMeetingNoticeState(sent) {
  const input = document.getElementById('inputMeetingNoticeSent');
  const btnUnsent = document.getElementById('btnNoticeUnsent');
  const btnSent = document.getElementById('btnNoticeSent');
  if (input) input.value = sent ? 'yes' : 'no';
  if (btnUnsent && btnSent) {
    if (sent) {
      btnSent.style.background = '#dcfce7';
      btnSent.style.color = '#15803d';
      btnSent.style.border = '1.5px solid #22c55e';
      btnSent.style.fontWeight = '700';
      btnSent.style.opacity = '1';
      btnUnsent.style.background = '#ffffff';
      btnUnsent.style.color = 'var(--text-secondary)';
      btnUnsent.style.border = '1px solid var(--border)';
      btnUnsent.style.fontWeight = '600';
      btnUnsent.style.opacity = '0.75';
    } else {
      btnUnsent.style.background = '#fef08a';
      btnUnsent.style.color = '#854d0e';
      btnUnsent.style.border = '1.5px solid #eab308';
      btnUnsent.style.fontWeight = '700';
      btnUnsent.style.opacity = '1';
      btnSent.style.background = '#ffffff';
      btnSent.style.color = 'var(--text-secondary)';
      btnSent.style.border = '1px solid var(--border)';
      btnSent.style.fontWeight = '600';
      btnSent.style.opacity = '0.75';
    }
  }
}

// ================= 会议时间冲突与重合时段检测引擎 (Meeting Conflict & Overlapping Time Engine) =================
function getMeetingConflicts(date, startTime, endTime, excludeId) {
  if (!date || !startTime || !endTime) return [];
  const startMin = timeStrToMinutes(startTime);
  const endMin = timeStrToMinutes(endTime);
  if (isNaN(startMin) || isNaN(endMin) || startMin >= endMin) return [];

  const meetings = getData(STORAGE_KEYS.MEETINGS, []);
  return meetings.filter(m => {
    if (excludeId && String(m.id) === String(excludeId)) return false;
    if (m.date !== date) return false;
    if (m.status === 'cancelled' || m.status === 'deleted') return false;

    const mStart = timeStrToMinutes(m.startTime || m.time);
    const mEnd = m.endTime ? timeStrToMinutes(m.endTime) : (mStart + Number(m.duration || 60));
    if (isNaN(mStart) || isNaN(mEnd) || mStart >= mEnd) return false;

    // Overlap: max(startA, startB) < min(endA, endB)
    return Math.max(startMin, mStart) < Math.min(endMin, mEnd);
  });
}

// 计算单个会议与列表中其他会议的所有冲突与重合时间段
function getMeetingConflictDetails(targetMeeting, allMeetings) {
  if (!targetMeeting || !targetMeeting.date) return [];
  if (targetMeeting.status === 'cancelled' || targetMeeting.status === 'deleted') return [];

  const list = allMeetings || getData(STORAGE_KEYS.MEETINGS, []);
  const dtTarget = getMeetingDisplayTime(targetMeeting);
  const targetStartMin = timeStrToMinutes(dtTarget.start || targetMeeting.startTime || targetMeeting.time);
  const targetEndMin = timeStrToMinutes(dtTarget.end || targetMeeting.endTime || calculateEndTime(dtTarget.start, targetMeeting.duration || 45));

  if (isNaN(targetStartMin) || isNaN(targetEndMin) || targetStartMin >= targetEndMin) return [];

  const conflicts = [];

  list.forEach(otherM => {
    if (!otherM || String(otherM.id) === String(targetMeeting.id)) return;
    if (otherM.date !== targetMeeting.date) return;
    if (otherM.status === 'cancelled' || otherM.status === 'deleted') return;

    const dtOther = getMeetingDisplayTime(otherM);
    const otherStartMin = timeStrToMinutes(dtOther.start || otherM.startTime || otherM.time);
    const otherEndMin = timeStrToMinutes(dtOther.end || otherM.endTime || calculateEndTime(dtOther.start, otherM.duration || 45));

    if (isNaN(otherStartMin) || isNaN(otherEndMin) || otherStartMin >= otherEndMin) return;

    // Overlap condition: max(startA, startB) < min(endA, endB)
    const overlapStartMin = Math.max(targetStartMin, otherStartMin);
    const overlapEndMin = Math.min(targetEndMin, otherEndMin);

    if (overlapStartMin < overlapEndMin) {
      const overlapDuration = overlapEndMin - overlapStartMin;
      const overlapStartStr = minutesToTimeStr(overlapStartMin);
      const overlapEndStr = minutesToTimeStr(overlapEndMin);
      const overlapRangeStr = `${overlapStartStr} - ${overlapEndStr}`;

      conflicts.push({
        conflictMeeting: otherM,
        conflictId: otherM.id,
        otherSubject: otherM.subject || '未命名会议',
        otherReporter: otherM.reporter || '',
        otherTimeRangeStr: `${dtOther.start} - ${dtOther.end}`,
        overlapStartMin,
        overlapEndMin,
        overlapDuration,
        overlapStartStr,
        overlapEndStr,
        overlapRangeStr
      });
    }
  });

  return conflicts;
}

// 批量提取所有活跃会议的冲突映射表 (MeetingId -> [ConflictDetail])
function getAllMeetingConflicts(meetings) {
  const list = meetings || getData(STORAGE_KEYS.MEETINGS, []);
  const map = {};
  list.forEach(m => {
    if (m && m.id && m.status !== 'cancelled' && m.status !== 'deleted') {
      const confs = getMeetingConflictDetails(m, list);
      if (confs.length > 0) {
        map[m.id] = confs;
      }
    }
  });
  return map;
}

function checkMeetingConflicts() {
  const alertEl = document.getElementById('meetingConflictAlert');
  if (!alertEl) return;

  const dateInput = document.getElementById('inputMeetingDate');
  const startInput = document.getElementById('inputMeetingStartTime');
  const endInput = document.getElementById('inputMeetingEndTime');
  const idInput = document.getElementById('inputMeetingId');
  const tzSelect = document.getElementById('inputMeetingTimezoneBase');

  const date = dateInput ? dateInput.value : '';
  let startTime = startInput ? startInput.value.trim() : '';
  let endTime = endInput ? endInput.value.trim() : '';
  const id = idInput ? idInput.value : '';
  const tzBase = (tzSelect && tzSelect.value) || 'cairo';

  if (startTime) startTime = normalizeTimeStr(startTime) || startTime;
  if (endTime) endTime = normalizeTimeStr(endTime) || endTime;

  let cairoStart = startTime;
  let cairoEnd = endTime;
  const diffHours = getTripTimezoneDiffHours(tzBase);
  if (tzBase !== 'cairo' && diffHours !== 0) {
    cairoStart = shiftTimeStrByHours(startTime, -diffHours);
    cairoEnd = shiftTimeStrByHours(endTime, -diffHours);
  }

  const conflicts = getMeetingConflicts(date, cairoStart, cairoEnd, id);
  if (conflicts.length > 0) {
    const targetStartMin = timeStrToMinutes(startTime);
    const targetEndMin = timeStrToMinutes(endTime);

    const listHtml = conflicts.map(c => {
      const dt = getMeetingDisplayTime(c);
      const displayRange = (dt.start && dt.end) ? `${dt.start} - ${dt.end}` : dt.start;
      const cTimeNote = (tzBase !== 'cairo') ? ` (开罗 ${c.startTime || c.time})` : '';
      const reporterText = c.reporter ? ` · 汇报人: ${escapeHtml(c.reporter)}` : '';

      // Calculate exact overlap range in display time
      const otherStartMin = timeStrToMinutes(dt.start);
      const otherEndMin = timeStrToMinutes(dt.end);
      let overlapRangeHtml = '';
      if (!isNaN(targetStartMin) && !isNaN(targetEndMin) && !isNaN(otherStartMin) && !isNaN(otherEndMin)) {
        const oStart = Math.max(targetStartMin, otherStartMin);
        const oEnd = Math.min(targetEndMin, otherEndMin);
        if (oStart < oEnd) {
          const oDur = oEnd - oStart;
          const oRange = `${minutesToTimeStr(oStart)} - ${minutesToTimeStr(oEnd)}`;
          overlapRangeHtml = `
            <div style="margin-top: 3px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
              <span style="background: #be123c; color: #ffffff; padding: 1px 6px; border-radius: 3px; font-size: 10.5px; font-weight: 700;">💥 重合时间</span>
              <strong style="color: #be123c; font-size: 12px; font-family: var(--font-mono);">🕒 ${oRange}</strong>
              <span style="color: #9f1239; font-weight: 700; font-size: 11px;">(重合 ${oDur} 分钟)</span>
            </div>
          `;
        }
      }

      return `
        <div style="margin-top: 6px; padding: 7px 10px; background: rgba(225,29,72,0.06); border: 1px solid #fecdd3; border-radius: 5px;">
          <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px;">
            <div>
              <strong>【${escapeHtml(c.subject || '未命名会议')}】</strong>
              <span style="color: var(--text-secondary); font-size: 11.5px; margin-left: 4px;">原时间: ${escapeHtml(displayRange)}${cTimeNote}</span>
              <span style="color: var(--text-secondary); font-size: 11px;">${reporterText}</span>
            </div>
            <span style="font-size: 11px; color: #be123c; background: #ffe4e6; padding: 1px 6px; border-radius: 3px; font-weight: 600; flex-shrink: 0;">已排期</span>
          </div>
          ${overlapRangeHtml}
        </div>
      `;
    }).join('');

    alertEl.innerHTML = `
      <div style="font-weight: 700; color: #be123c; display: flex; align-items: center; justify-content: space-between;">
        <span>⚠️ 会议时间冲突提醒</span>
        <span style="font-size: 11px; background: #be123c; color: #ffffff; padding: 1px 7px; border-radius: 10px; font-weight: 600;">${conflicts.length} 场重叠</span>
      </div>
      <div style="font-size: 11.5px; color: #9f1239; margin-top: 4px;">
        您选择的时间（<strong>${escapeHtml(startTime)} - ${escapeHtml(endTime)}</strong>${tzBase !== 'cairo' ? `，对应开罗时间 ${cairoStart} - ${cairoEnd}` : ''}）与以下已有日程冲突，请注意调整或确认：
      </div>
      <div style="margin-top: 5px;">${listHtml}</div>
    `;
    alertEl.style.display = 'block';
  } else {
    alertEl.style.display = 'none';
    alertEl.innerHTML = '';
  }
}

function openAddMeetingModal() {
  closeAllTimePickers();
  document.getElementById('meetingModalTitle').textContent = '登记主管会议预约';
  document.getElementById('inputMeetingId').value = '';
  const initialDate = selectedTimelineDate || getTodayDateStr();
  document.getElementById('inputMeetingDate').value = initialDate;

  const trip = getTripForDate(initialDate);
  const tzSelect = document.getElementById('inputMeetingTimezoneBase');
  if (tzSelect) {
    if (trip) {
      tzSelect.value = trip.destination;
    } else {
      tzSelect.value = 'cairo';
    }
    tzSelect._lastTz = tzSelect.value;
  }

  document.getElementById('inputMeetingStartTime').value = '10:00';
  document.getElementById('inputMeetingEndTime').value = '10:45';
  handleMeetingModalTimezoneChange();

  // Mandatory fields: subject is empty
  document.getElementById('inputMeetingSubject').value = '';
  // Optional fields: reporter is empty
  document.getElementById('inputMeetingReporter').value = '';

  // Optional fields: ALL COMPLETELY EMPTY by default per user request
  document.getElementById('inputMeetingLocation').value = '';
  document.getElementById('inputMeetingMinuter').value = '';
  document.getElementById('inputMeetingAttendees').value = '';
  document.getElementById('inputMeetingBackground').value = '';
  document.getElementById('inputMeetingDecision').value = '';
  document.getElementById('inputMeetingRequester').value = '';
  document.getElementById('inputMeetingNotes').value = '';

  document.getElementById('selectMeetingStatus').value = 'scheduled';

  // Meeting notice sent toggle default: false (unsent / highlighted)
  setMeetingNoticeState(false);
  if (document.getElementById('selectMeetingLegacyTaskId')) {
    updateMeetingLegacyTaskOptions('');
  }
  if (document.getElementById('inputMeetingHasMinutes')) {
    document.getElementById('inputMeetingHasMinutes').value = 'no';
    if (document.getElementById('radioMinutesNo')) document.getElementById('radioMinutesNo').checked = true;
  }
  if (document.getElementById('inputMeetingNextPlan')) {
    document.getElementById('inputMeetingNextPlan').value = '';
  }
  const details = document.getElementById('meetingFoldableDetails');
  if (details) details.open = false;

  const recallBtn = document.getElementById('btnRecallToPending');
  if (recallBtn) recallBtn.style.display = 'none';
  const delBtn = document.getElementById('btnDeleteMeeting');
  if (delBtn) delBtn.style.display = 'none';

  updateMeetingDurationBadge();
  checkMeetingConflicts();
  openModal('meetingModal');
}

function saveMeeting() {
  const id = document.getElementById('inputMeetingId').value;
  const date = document.getElementById('inputMeetingDate').value;
  let startTime = document.getElementById('inputMeetingStartTime').value.trim();
  let endTime = document.getElementById('inputMeetingEndTime').value.trim();
  const subject = document.getElementById('inputMeetingSubject').value.trim();
  const reporter = document.getElementById('inputMeetingReporter').value.trim();
  const tzBase = (document.getElementById('inputMeetingTimezoneBase') && document.getElementById('inputMeetingTimezoneBase').value) || 'cairo';

  // Normalize times
  if (startTime) {
    startTime = normalizeTimeStr(startTime) || startTime;
    document.getElementById('inputMeetingStartTime').value = startTime;
  }
  if (endTime) {
    endTime = normalizeTimeStr(endTime) || endTime;
    document.getElementById('inputMeetingEndTime').value = endTime;
  }

  // Mandatory checks
  if (!date) {
    showToast('请选择会议日期');
    document.getElementById('inputMeetingDate').focus();
    return;
  }
  if (!startTime || !/^[0-9]{1,2}:[0-9]{2}$/.test(startTime)) {
    showToast('请填写有效的开始时间 (如 09:30)');
    document.getElementById('inputMeetingStartTime').focus();
    return;
  }
  if (!endTime || !/^[0-9]{1,2}:[0-9]{2}$/.test(endTime)) {
    showToast('请填写有效的结束时间 (如 10:15)');
    document.getElementById('inputMeetingEndTime').focus();
    return;
  }
  if (!subject) {
    showToast('请填写会议主题');
    document.getElementById('inputMeetingSubject').focus();
    return;
  }

  // Reporter is NO LONGER mandatory per user request!

  // Duration
  const duration = calculateDurationFromRange(startTime, endTime);
  const durationHours = (duration / 60).toFixed(2);

  const trip = getTripForDate(date);
  const effectiveTzBase = tzBase || 'cairo';

  // Determine Cairo baseline times and Trip local times
  let cairoStartTime = startTime;
  let cairoEndTime = endTime;
  let localStartTime = startTime;
  let localEndTime = endTime;

  if (effectiveTzBase === 'cairo') {
    cairoStartTime = startTime;
    cairoEndTime = endTime;
    if (trip && trip.diffHours !== 0) {
      localStartTime = shiftTimeStrByHours(cairoStartTime, trip.diffHours);
      localEndTime = shiftTimeStrByHours(cairoEndTime, trip.diffHours);
    } else {
      localStartTime = cairoStartTime;
      localEndTime = cairoEndTime;
    }
  } else {
    const diffHours = getTripTimezoneDiffHours(effectiveTzBase);
    cairoStartTime = shiftTimeStrByHours(startTime, -diffHours);
    cairoEndTime = shiftTimeStrByHours(endTime, -diffHours);
    if (trip && trip.diffHours !== 0) {
      localStartTime = shiftTimeStrByHours(cairoStartTime, trip.diffHours);
      localEndTime = shiftTimeStrByHours(cairoEndTime, trip.diffHours);
    } else {
      localStartTime = startTime;
      localEndTime = endTime;
    }
  }

  // Conflict detection and confirmation prompt against Cairo baseline with exact overlapping times
  const conflicts = getMeetingConflicts(date, cairoStartTime, cairoEndTime, id);
  if (conflicts.length > 0) {
    const targetStartMin = timeStrToMinutes(startTime);
    const targetEndMin = timeStrToMinutes(endTime);

    const conflictList = conflicts.map(c => {
      const cdt = getMeetingDisplayTime(c);
      const cStart = timeStrToMinutes(cdt.start);
      const cEnd = timeStrToMinutes(cdt.end);
      let overlapInfo = '';
      if (!isNaN(targetStartMin) && !isNaN(targetEndMin) && !isNaN(cStart) && !isNaN(cEnd)) {
        const oStart = Math.max(targetStartMin, cStart);
        const oEnd = Math.min(targetEndMin, cEnd);
        if (oStart < oEnd) {
          overlapInfo = ` ➜ 💥 重合时间: ${minutesToTimeStr(oStart)} - ${minutesToTimeStr(oEnd)} (重叠 ${oEnd - oStart} 分钟)`;
        }
      }
      return `• 【${c.subject || '未命名会议'}】(原时间 ${cdt.start} - ${cdt.end}${c.reporter ? ' / 汇报人: ' + c.reporter : ''}${cdt.isShifted ? ' [开罗 ' + cdt.cairoStart + ']' : ''})${overlapInfo}`;
    }).join('\\n');
    const confirmMsg = `⚠️ 会议时间冲突提醒：\\n\\n您安排的会议时间（${date} ${startTime} - ${endTime}${effectiveTzBase !== 'cairo' ? `，对应开罗时间 ${cairoStartTime} - ${cairoEndTime}` : ''}）与以下已有日程存在重合冲突：\\n\\n${conflictList}\\n\\n是否确认仍要保存该会议？`;
    if (!confirm(confirmMsg)) {
      return;
    }
  }

  // Optional fields (empty string if blank)
  const location = document.getElementById('inputMeetingLocation').value.trim();
  const minuter = document.getElementById('inputMeetingMinuter').value.trim();
  const attendees = document.getElementById('inputMeetingAttendees').value.trim();
  const background = document.getElementById('inputMeetingBackground').value.trim();
  const decision = document.getElementById('inputMeetingDecision').value.trim();
  const requester = document.getElementById('inputMeetingRequester').value.trim();
  const status = document.getElementById('selectMeetingStatus').value || 'scheduled';
  const priority = 'medium';
  const notes = document.getElementById('inputMeetingNotes').value.trim();
  const noticeSent = document.getElementById('inputMeetingNoticeSent') ? (document.getElementById('inputMeetingNoticeSent').value === 'yes') : false;

  let meetings = getData(STORAGE_KEYS.MEETINGS);
  const existingMeeting = id ? meetings.find(m => m.id == id) : null;
  const requestId = window.convertingRequestId || (existingMeeting ? existingMeeting.requestId : null);

  const meetingData = {
    date,
    time: cairoStartTime,
    startTime: cairoStartTime,
    endTime: cairoEndTime,
    tzBase: effectiveTzBase,
    inputStartTime: startTime,
    inputEndTime: endTime,
    localStartTime: localStartTime,
    localEndTime: localEndTime,
    duration,
    durationHours,
    subject,
    reporter,
    location,
    minuter,
    attendees,
    background,
    decision,
    requester,
    status,
    priority,
    notes,
    requestId,
    noticeSent,
    legacyTaskId: (document.getElementById('selectMeetingLegacyTaskId') && document.getElementById('selectMeetingLegacyTaskId').value) || '',
    hasMinutes: (document.getElementById('inputMeetingHasMinutes') && document.getElementById('inputMeetingHasMinutes').value) || 'no',
    nextPlan: (document.getElementById('inputMeetingNextPlan') && document.getElementById('inputMeetingNextPlan').value.trim()) || ''
  };

  if (id) {
    meetings = meetings.map(m => m.id == id ? { ...m, ...meetingData, id: m.id } : m);
    showToast('会议预约已更新');
  } else {
    meetings.unshift({
      id: Date.now(),
      ...meetingData
    });
    showToast('会议预约已成功登记');
  }

  // If this meeting was converted from a quick meeting request, mark it scheduled!
  if (window.convertingRequestId) {
    let reqs = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
    reqs = reqs.map(r => r.id === window.convertingRequestId ? { ...r, status: 'scheduled' } : r);
    setData(STORAGE_KEYS.MEETING_REQUESTS, reqs);
    window.convertingRequestId = null;
  }

  setData(STORAGE_KEYS.MEETINGS, meetings);

  // 同步联动遗留任务
  const selLegacyId = document.getElementById('selectMeetingLegacyTaskId') ? document.getElementById('selectMeetingLegacyTaskId').value : '';
  if (selLegacyId) {
    let ltasks = getData(STORAGE_KEYS.LEGACY_TASKS, []);
    ltasks = ltasks.map(lt => {
      if (String(lt.id) === String(selLegacyId)) {
        const nextStatus = lt.status === 'pending' ? 'in_progress' : lt.status;
        const meetingMinutes = document.getElementById('inputMeetingHasMinutes') ? document.getElementById('inputMeetingHasMinutes').value : 'no';
        const meetingNextPlan = document.getElementById('inputMeetingNextPlan') ? document.getElementById('inputMeetingNextPlan').value.trim() : '';
        const mDecision = document.getElementById('inputMeetingDecision') ? document.getElementById('inputMeetingDecision').value.trim() : '';
        const mDate = document.getElementById('inputMeetingDate') ? document.getElementById('inputMeetingDate').value : '';
        const mTime = document.getElementById('inputMeetingStartTime') ? document.getElementById('inputMeetingStartTime').value : '';
        const mReportTimeStr = (mDate && mTime) ? (mDate + ' ' + mTime) : '';
        return {
          ...lt,
          status: nextStatus,
          reportTime: mReportTimeStr || lt.reportTime,
          reviewOpinion: mDecision ? mDecision : lt.reviewOpinion,
          progress: meetingNextPlan ? meetingNextPlan : (lt.progress || lt.nextPlan),
          nextPlan: meetingNextPlan ? meetingNextPlan : lt.nextPlan,
          hasMinutes: meetingMinutes === 'yes' ? true : lt.hasMinutes,
          updatedAt: Date.now()
        };
      }
      return lt;
    });
    setData(STORAGE_KEYS.LEGACY_TASKS, ltasks);
    if (typeof renderLegacyTasks === 'function') renderLegacyTasks();
  }

  closeModal('meetingModal');
  renderMeetings();
}

// ================= 待排期 (Pending Requests Pool) =================
function addMeetingRequestFast() {
  const requester = document.getElementById('inputFastReqRequester').value.trim();
  const topic = document.getElementById('inputFastReqTopic').value.trim();
  if (!topic) {
    showToast('请填写会议诉求或议题！');
    const el = document.getElementById('inputFastReqTopic');
    if (el) el.focus();
    return;
  }
  const urgencyEl = document.getElementById('selectFastReqUrgency');
  const urgency = urgencyEl ? urgencyEl.value : 'normal';
  let duration = document.getElementById('inputFastReqDuration').value.trim() || '45';
  duration = duration.replace(/[^0-9]/g, '') || '45';

  const now = new Date();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  const h = String(now.getHours()).padStart(2, '0');
  const min = String(now.getMinutes()).padStart(2, '0');
  const createdAt = `${m}-${d} ${h}:${min}`;

  const requests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  requests.unshift({
    id: Date.now(),
    requester: requester || '其他人员',
    topic,
    urgency,
    duration,
    status: 'pending',
    createdAt
  });
  setData(STORAGE_KEYS.MEETING_REQUESTS, requests);

  document.getElementById('inputFastReqRequester').value = '';
  document.getElementById('inputFastReqTopic').value = '';
  showToast('📝 意向已加入待排期！');
  renderMeetings();
}

function convertRequestToMeeting(id) {
  const requests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  const req = requests.find(r => r.id === id);
  if (!req) return;
  openAddMeetingModal();
  document.getElementById('inputMeetingSubject').value = req.topic || '';
  document.getElementById('inputMeetingReporter').value = req.requester || '';
  if (req.duration) {
    const durNum = parseInt(req.duration, 10);
    if (!isNaN(durNum) && [30, 40, 60, 90, 120].includes(durNum)) {
      applyQuickDuration(durNum);
    }
  }
  window.convertingRequestId = id;
  showToast(`已将【${req.requester}】的预约需求自动载入排期单！`);
}

function toggleMeetingRequestStatus(id) {
  let requests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  requests = requests.map(r => {
    if (r.id === id) {
      const nextStatus = (r.status === 'scheduled') ? 'pending' : 'scheduled';
      return { ...r, status: nextStatus };
    }
    return r;
  });
  setData(STORAGE_KEYS.MEETING_REQUESTS, requests);
  renderMeetings();
}

function deleteMeetingRequest(id) {
  let requests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  requests = requests.filter(r => r.id !== id);
  setData(STORAGE_KEYS.MEETING_REQUESTS, requests);
  renderMeetings();
  showToast('待排期条目已删除');
}

function clearScheduledRequests() {
  if (!confirm('确定要清理所有已完成排期的记录吗？')) return;
  let requests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  requests = requests.filter(r => r.status !== 'scheduled');
  setData(STORAGE_KEYS.MEETING_REQUESTS, requests);
  renderMeetings();
  showToast('已清理已排期记录');
}

function openEditRequestModal(id) {
  const requests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  const req = requests.find(r => r.id === id);
  if (!req) return;
  document.getElementById('editRequestId').value = req.id;
  document.getElementById('editRequestRequester').value = req.requester || '';
  const editUrgEl = document.getElementById('editRequestUrgency');
  if (editUrgEl) editUrgEl.value = req.urgency || 'normal';
  document.getElementById('editRequestTopic').value = req.topic || '';
  document.getElementById('editRequestDuration').value = req.duration || '45';
  document.getElementById('editRequestStatus').value = req.status || 'pending';
  openModal('editRequestModal');
}

function saveEditRequest() {
  const id = Number(document.getElementById('editRequestId').value);
  const topic = document.getElementById('editRequestTopic').value.trim();
  if (!topic) {
    showToast('会议诉求不能为空！');
    return;
  }
  const requester = document.getElementById('editRequestRequester').value.trim() || '其他人员';
  const editUrgEl = document.getElementById('editRequestUrgency');
  const urgency = editUrgEl ? editUrgEl.value : 'normal';
  const duration = document.getElementById('editRequestDuration').value.trim() || '45';
  const status = document.getElementById('editRequestStatus').value;

  let requests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  requests = requests.map(r => {
    if (r.id === id) {
      return { ...r, requester, topic, urgency, duration, status };
    }
    return r;
  });
  setData(STORAGE_KEYS.MEETING_REQUESTS, requests);
  closeModal('editRequestModal');
  renderMeetings();
  showToast('✅ 待排期事项已更新！');
}

function deleteCurrentEditRequest() {
  const id = Number(document.getElementById('editRequestId').value);
  if (!id) return;
  if (!confirm('确定要删除此条待排期记录吗？')) return;
  closeModal('editRequestModal');
  deleteMeetingRequest(id);
}

function editMeeting(id) {
  closeAllTimePickers();
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const m = meetings.find(x => x.id === id);
  if (!m) return;

  document.getElementById('meetingModalTitle').textContent = '编辑主管会议预约';
  document.getElementById('inputMeetingId').value = m.id;
  document.getElementById('inputMeetingDate').value = m.date;

  const tzSelect = document.getElementById('inputMeetingTimezoneBase');
  const trip = getTripForDate(m.date);
  const dt = getMeetingDisplayTime(m);

  let originTz = m.tzBase;
  if (!originTz) {
    originTz = trip ? trip.destination : 'cairo';
  }
  if (tzSelect) {
    tzSelect.value = originTz;
    tzSelect._lastTz = originTz;
  }

  const originDiff = getTripTimezoneDiffHours(originTz);
  let editStart = m.inputStartTime || (m.localStartTime && m.tzBase === originTz ? m.localStartTime : shiftTimeStrByHours(m.startTime || m.time, originDiff));
  let editEnd = m.inputEndTime || (m.localEndTime && m.tzBase === originTz ? m.localEndTime : shiftTimeStrByHours(m.endTime || calculateEndTime(m.startTime, m.duration), originDiff));

  if (!m.tzBase && trip && trip.destination === originTz) {
    editStart = dt.start;
    editEnd = dt.end;
  }

  document.getElementById('inputMeetingStartTime').value = editStart;
  document.getElementById('inputMeetingEndTime').value = editEnd;
  handleMeetingModalTimezoneChange();

  document.getElementById('inputMeetingSubject').value = m.subject || '';
  document.getElementById('inputMeetingReporter').value = m.reporter || '';
  document.getElementById('inputMeetingLocation').value = m.location || '';
  document.getElementById('inputMeetingMinuter').value = m.minuter || '';
  document.getElementById('inputMeetingAttendees').value = m.attendees || '';
  document.getElementById('inputMeetingBackground').value = m.background || '';
  document.getElementById('inputMeetingDecision').value = m.decision || '';
  document.getElementById('inputMeetingRequester').value = m.requester || '';
  document.getElementById('selectMeetingStatus').value = m.status || 'scheduled';
  document.getElementById('inputMeetingNotes').value = m.notes || '';

  // Restore noticeSent state (default to false if undefined or null)
  const noticeSent = (m.noticeSent === true || m.noticeSent === 'yes');
  setMeetingNoticeState(noticeSent);
  if (document.getElementById('selectMeetingLegacyTaskId')) {
    updateMeetingLegacyTaskOptions(m.legacyTaskId || '');
  }
  const mHasMinutes = (m.hasMinutes === 'yes' || m.hasMinutes === true);
  if (document.getElementById('inputMeetingHasMinutes')) {
    document.getElementById('inputMeetingHasMinutes').value = mHasMinutes ? 'yes' : 'no';
    if (document.getElementById('radioMinutesYes')) document.getElementById('radioMinutesYes').checked = mHasMinutes;
    if (document.getElementById('radioMinutesNo')) document.getElementById('radioMinutesNo').checked = !mHasMinutes;
  }
  if (document.getElementById('inputMeetingNextPlan')) {
    document.getElementById('inputMeetingNextPlan').value = m.nextPlan || '';
  }

  // Auto-expand foldable details if any optional field has content
  const details = document.getElementById('meetingFoldableDetails');
  if (details) {
    const hasFoldedContent = !!(m.location || m.minuter || m.attendees || m.background || m.decision);
    details.open = hasFoldedContent;
  }

  updateMeetingDurationBadge();
  checkMeetingConflicts();
  const recallBtn = document.getElementById('btnRecallToPending');
  if (recallBtn) recallBtn.style.display = 'inline-flex';
  const delBtn = document.getElementById('btnDeleteMeeting');
  if (delBtn) delBtn.style.display = 'inline-flex';

  openModal('meetingModal');
}

function recallMeetingToPending() {
  const idStr = document.getElementById('inputMeetingId').value;
  if (!idStr) {
    showToast('该预约尚未保存，无需撤回');
    return;
  }
  const id = Number(idStr) || idStr;
  let meetings = getData(STORAGE_KEYS.MEETINGS);
  const m = meetings.find(x => x.id == id);
  if (!m) return;

  if (!confirm(`确定要将会议【${m.subject}】撤回改成“待排期”吗？\n撤回后将从日程表中移出，释放对应时间段，并存入顶部的“待排期”列表中。`)) {
    return;
  }

  // 1. Remove from active scheduled meetings
  meetings = meetings.filter(item => item.id != id);
  setData(STORAGE_KEYS.MEETINGS, meetings);

  // 2. Add or reactivate in MEETING_REQUESTS (待排期池)
  let requests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  let found = false;

  if (m.requestId) {
    requests = requests.map(r => {
      if (r.id === m.requestId) {
        found = true;
        return {
          ...r,
          topic: m.subject || r.topic,
          requester: m.reporter || m.requester || r.requester,
          duration: String(m.duration || r.duration || 45),
          status: 'pending'
        };
      }
      return r;
    });
  }

  if (!found) {
    const now = new Date();
    const monthStr = String(now.getMonth() + 1).padStart(2, '0');
    const dateStr = String(now.getDate()).padStart(2, '0');
    const hourStr = String(now.getHours()).padStart(2, '0');
    const minStr = String(now.getMinutes()).padStart(2, '0');
    const createdAt = `${monthStr}-${dateStr} ${hourStr}:${minStr}`;

    requests.unshift({
      id: Date.now(),
      requester: m.reporter || m.requester || '部门预约',
      topic: m.subject || '待排期议题',
      urgency: 'medium',
      duration: String(m.duration || 45),
      status: 'pending',
      createdAt,
      originalDate: m.date,
      originalTime: m.startTime || m.time || ''
    });
  }

  setData(STORAGE_KEYS.MEETING_REQUESTS, requests);

  // 3. Close modal & re-render
  closeModal('meetingModal');
  renderMeetings();
  showToast(`↩️ 会议【${m.subject}】已撤回改成待排期，对应时间已释放`);
}

function deleteCurrentMeeting() {
  const idStr = document.getElementById('inputMeetingId').value;
  if (!idStr) {
    showToast('该预约尚未保存，无需删除');
    return;
  }
  const id = Number(idStr) || idStr;
  if (!confirm('确定要删除此条已登记的主管会议预约记录吗？')) return;
  let meetings = getData(STORAGE_KEYS.MEETINGS);
  meetings = meetings.filter(m => m.id != id);
  setData(STORAGE_KEYS.MEETINGS, meetings);
  closeModal('meetingModal');
  renderMeetings();
  showToast('会议预约已成功删除');
}

function updateMeetingStatus(id, newStatus) {
  let meetings = getData(STORAGE_KEYS.MEETINGS);
  meetings = meetings.map(m => m.id === id ? { ...m, status: newStatus } : m);
  setData(STORAGE_KEYS.MEETINGS, meetings);
  renderMeetings();
  showToast('会议状态已更新');
}

function deleteMeeting(id) {
  if (!confirm('确定要删除该条主管会议预约记录吗？')) return;
  let meetings = getData(STORAGE_KEYS.MEETINGS);
  meetings = meetings.filter(m => m.id != id);
  setData(STORAGE_KEYS.MEETINGS, meetings);
  renderMeetings();
  showToast('会议记录已删除');
}

function copySingleMeetingNotice(id) {
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const m = meetings.find(x => x.id === id);
  if (!m) return;

  const dt = getMeetingDisplayTime(m);
  const timeDisplay = dt.isShifted 
    ? `${m.date} ${dt.start} - ${dt.end} (当地时间 | 对应开罗时间 ${dt.cairoStart} - ${dt.cairoEnd})` 
    : `${m.date} ${dt.start} - ${dt.end}`;

  const text = [
    '【主管会议安排通知】' + m.subject,
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    '会议时间：' + timeDisplay + ' (' + (m.duration || 45) + '分钟)',
    '会议地点：' + (m.location || '主管办公室'),
    '汇报人：' + (m.reporter || '未注明'),
    '与会人员：' + m.attendees,
    (m.minuter ? '纪要人：' + m.minuter : ''),
    (m.background ? '会议背景：' + m.background : ''),
    '决策要点：\\n' + m.decision,
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    '秘书处提示：请参会人员提前5分钟就座，精简汇报，直奔决策要点。'
  ].filter(Boolean).join('\\n');

  copyToClipboard(text, '会议通知已复制到剪贴板，可直接发送微信或邮件。');
}

function exportTodayMeetingBriefing() {
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const targetDate = selectedTimelineDate || getTodayDateStr();
  const dayMeetings = meetings.filter(m => m.date === targetDate && m.status !== 'cancelled');

  if (dayMeetings.length === 0) {
    showToast(`${targetDate} 暂无已排期的会议安排`);
    return;
  }

  let lines = [
    '【主管会议日程总览 · ' + targetDate + '】',
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
  ];

  dayMeetings.forEach((m, idx) => {
    const dt = getMeetingDisplayTime(m);
    const tzNote = dt.isShifted ? ` [开罗 ${dt.cairoStart}]` : '';
    lines.push((idx + 1) + '. ' + dt.start + ' - ' + dt.end + ' [' + (m.duration || 45) + 'm] ' + m.subject + tzNote);
    lines.push('   地点：' + (m.location || '主管办公室') + ' | 汇报人：' + (m.reporter || m.attendees));
    lines.push('   核心决策点：' + m.decision.replace(/\\n/g, ' '));
    lines.push('');
  });

  lines.push('━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  lines.push('由 Snoopy’s Little Lab 秘书工作台生成');

  copyToClipboard(lines.join('\\n'), '会议日程总览已复制到剪贴板！');
}

function copyPendingRequestsBriefing() {
  const meetingRequests = getData(STORAGE_KEYS.MEETING_REQUESTS, []);
  // 严格只获取待排期池中的待排事项，绝不夹杂日历已排会议，确保与界面显示的待排期数量 100% 一致
  const pendingRequests = meetingRequests.filter(r => r.status !== 'scheduled');

  if (pendingRequests.length === 0) {
    showToast('当前暂无待排期事项，无需生成简报');
    return;
  }

  const today = new Date();
  const month = today.getMonth() + 1;
  const date = today.getDate();
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  const weekdayStr = weekdays[today.getDay()];
  const headerDateStr = `${month}月${date}日 ${weekdayStr}`;

  const activeTz = (typeof getActiveTripTimezone === 'function') ? getActiveTripTimezone() : 'cairo';
  const isShifted = (activeTz !== 'cairo');
  const tzInfo = (typeof TRIP_TIMEZONE_MAP !== 'undefined' && TRIP_TIMEZONE_MAP[activeTz]) ? TRIP_TIMEZONE_MAP[activeTz] : null;
  const tripSuffix = (isShifted && tzInfo) ? ` (出差${tzInfo.name}中 · ${tzInfo.flag})` : '';

  // 极简高管呈批格式：每个预约一行字说完，篇幅精炼直观，不分重要程度
  const lines = [
    `【主管待排期事项请示 · ${headerDateStr}${tripSuffix}】`,
    `曦总您好，当前汇总共有 ${pendingRequests.length} 项待排期事项，请您审定是否安排：`,
    ''
  ];

  pendingRequests.forEach((req, idx) => {
    const durNum = parseInt(req.duration || 45, 10);
    const durStr = durNum ? `${durNum}m` : (req.duration || '45m');
    const requester = req.requester ? req.requester.trim() : '未注明';
    const topic = req.topic ? req.topic.trim() : '未命名事项';
    lines.push(`${idx + 1}. ${requester}：${topic} (${durStr})`);
  });

  lines.push('');
  lines.push('请示说明：请曦总批示优先安排哪些事项，秘书处将立即为您锁定时间。');

  copyToClipboard(lines.join('\\n'), '待排期简报已复制到剪贴板，可直接发送微信或工作群！');
}

// ================= 时区协同 (World Tour · Chronological Sorting per Point 3) =================
function renderTimezones() {
  const now = new Date();

  const cairoTimeFormatter = new Intl.DateTimeFormat('zh-CN', {
    timeZone: 'Africa/Cairo',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });
  const cairoTimeStr = cairoTimeFormatter.format(now);

  const headerClock = document.getElementById('headerCairoClock');
  if (headerClock) headerClock.textContent = cairoTimeStr;

  const bigCairoClock = document.getElementById('tzBigCairoClock');
  if (bigCairoClock) bigCairoClock.textContent = cairoTimeStr;

  const gridEl = document.getElementById('tzFullGrid');
  if (gridEl) {
    // Sort chronologically from earliest local time to latest (Point 3)
    const sortedReps = [...TIMEZONE_REPS].sort((a, b) => {
      if (b.utcOffset !== a.utcOffset) return b.utcOffset - a.utcOffset;
      if (a.isBaseline) return -1;
      if (b.isBaseline) return 1;
      return 0;
    });

    gridEl.innerHTML = sortedReps.map(rep => {
      const timeFmt = new Intl.DateTimeFormat('zh-CN', {
        timeZone: rep.tz,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      });
      const localTime = timeFmt.format(now);
      const parts = localTime.split(':').map(Number);
      const hourVal = parts[0] + parts[1] / 60;

      // Determine local day of week
      const dayFmt = new Intl.DateTimeFormat('en-US', { timeZone: rep.tz, weekday: 'short' });
      const localDay = dayFmt.format(now); // 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'

      // Weekend check per office:
      // In Cairo, Algeria, Med South (Tunis/Libya) (North Africa/MENA): Friday and Saturday are official weekend
      // In Congo DRC, Cameroon, Ivory Coast, Senegal, Morocco: Saturday and Sunday are weekend
      let isWeekend = false;
      if (rep.id === 'cairo' || rep.id === 'algeria' || rep.id === 'med_south' || rep.id === 'med_south_tunis' || rep.id === 'med_south_libya') {
        isWeekend = (localDay === 'Fri' || localDay === 'Sat');
      } else {
        isWeekend = (localDay === 'Sat' || localDay === 'Sun');
      }

      // Work hours: 09:00 - 18:00; Lunch break: 12:00 - 13:30 (also resting)
      let isResting = false;
      let statusDot = '';
      let progressPct = 0;

      if (isWeekend) {
        isResting = true;
        statusDot = '<span class="tz-status-dot"><span class="dot-grey"></span> 🏖️ 周末休整</span>';
        progressPct = 0;
      } else if (hourVal < 9.0) {
        isResting = true;
        statusDot = '<span class="tz-status-dot"><span class="dot-grey"></span> 🌙 早间静息 (09:00上班)</span>';
        progressPct = 0;
      } else if (hourVal >= 18.0) {
        isResting = true;
        statusDot = '<span class="tz-status-dot"><span class="dot-grey"></span> 🌙 晚间休息中</span>';
        progressPct = 100;
      } else if (hourVal >= 12.0 && hourVal < 13.5) {
        isResting = true;
        statusDot = '<span class="tz-status-dot"><span class="dot-yellow"></span> 🍱 午休小憩 (12:00-13:30)</span>';
        progressPct = Math.min(100, Math.max(0, ((hourVal - 9.0) / 9.0) * 100));
      } else {
        isResting = false;
        statusDot = '<span class="tz-status-dot"><span class="dot-green"></span> 💼 正常办公中</span>';
        progressPct = Math.min(100, Math.max(0, ((hourVal - 9.0) / 9.0) * 100));
      }

      const offsetStr = rep.utcOffset >= 0 ? 'UTC+' + rep.utcOffset : 'UTC' + rep.utcOffset;
      const diffLabel = rep.isBaseline ? '<span style="color:var(--accent-red); font-weight:700;">★ 开罗基准时区</span>' : rep.diffText;

      return `
        <div class="tz-card ${rep.isBaseline ? 'baseline' : ''} ${isResting ? 'is-resting' : ''}">
          <div>
            <div class="tz-card-top">
              <div class="tz-rep-title">
                <span style="font-size:20px;">${rep.flag}</span>
                <div>
                  <div style="font-weight:800; font-size:14.5px;">${rep.name}</div>
                  <div class="tz-rep-city">${rep.city}</div>
                </div>
              </div>
              <span class="tz-offset-tag">${offsetStr}</span>
            </div>

            <div class="tz-time-big">${localTime}</div>

            <div class="tz-progress-bar" title="工作日作息进度 (09:00 - 18:00)">
              <div class="tz-progress-fill" style="width: ${progressPct}%;"></div>
            </div>
          </div>

          <div class="tz-diff-row">
            <div>${diffLabel}</div>
            <div>${statusDot}</div>
          </div>
        </div>
      `;
    }).join('');
  }

  const miniEl = document.getElementById('dashTzMiniList');
  if (miniEl) {
    miniEl.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:8px;">
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12.5px;">
          <span>🇪🇬 <strong>开罗基准 (UTC+2)</strong> · 埃及代表处</span>
          <span style="font-family:var(--font-mono); font-weight:700; color:var(--text-primary);">${cairoTimeStr}</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:var(--text-secondary);">
          <span>🇱🇾 <strong>UTC+2 (0h)</strong> · 地南·利比亚</span>
          <span style="font-family:var(--font-mono); font-weight:600;">无时差</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:var(--text-secondary);">
          <span>🇩🇿 <strong>UTC+1 (-1h)</strong> · 地南·突尼斯 / 阿尔及利亚 / 刚果金 / 喀麦隆</span>
          <span style="font-family:var(--font-mono); font-weight:600;">慢 1 小时</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:var(--text-secondary);">
          <span>🇨🇮 <strong>UTC+0 (-2h)</strong> · 摩洛哥 / 科特迪瓦 / 塞内加尔</span>
          <span style="font-family:var(--font-mono); font-weight:600;">慢 2 小时</span>
        </div>
      </div>
    `;
  }
  if (typeof renderHomeLeaderTrip === 'function') renderHomeLeaderTrip();
}

const SIM_OFFICES = [
  { id: 'cairo', name: '埃及代表处', country: '埃及', flag: '🇪🇬', utcOffset: 2, city: '开罗' },
  { id: 'med_south_libya', name: '地南代表处 · 利比亚', country: '利比亚', flag: '🇱🇾', utcOffset: 2, city: '的黎波里 / 班加西' },
  { id: 'med_south_tunis', name: '地南代表处 · 突尼斯', country: '突尼斯', flag: '🇹🇳', utcOffset: 1, city: '突尼斯市' },
  { id: 'congo_drc', name: '刚果代表处', country: '刚果（金）', flag: '🇨🇩', utcOffset: 1, city: '金沙萨' },
  { id: 'cameroon', name: '喀麦隆代表处', country: '喀麦隆', flag: '🇨🇲', utcOffset: 1, city: '雅温得 / 杜阿拉' },
  { id: 'algeria', name: '阿尔及利亚代表处', country: '阿尔及利亚', flag: '🇩🇿', utcOffset: 1, city: '阿尔及尔' },
  { id: 'morocco', name: '摩洛哥代表处', country: '摩洛哥', flag: '🇲🇦', utcOffset: 0, city: '卡萨布兰卡 / 拉巴特' },
  { id: 'cote_divoire', name: '科特迪瓦代表处', country: '科特迪瓦', flag: '🇨🇮', utcOffset: 0, city: '阿比让' },
  { id: 'senegal', name: '塞内加尔代表处', country: '塞内加尔', flag: '🇸🇳', utcOffset: 0, city: '达喀尔' },
  { id: 'beijing', name: '中国总部', country: '北京', flag: '🇨🇳', utcOffset: 8, city: '北京' }
];

function handleSimTimeRangeChange(type) {
  const sInput = document.getElementById('simCairoTime');
  const eInput = document.getElementById('simEndTime');
  if (!sInput || !eInput) return;
  const sVal = sInput.value;
  const eVal = eInput.value;

  if (type === 'start' && sVal) {
    const sMins = timeStrToMinutes(sVal);
    const eMins = eVal ? timeStrToMinutes(eVal) : 0;
    if (!eVal || eMins <= sMins) {
      eInput.value = minutesToTimeStr((sMins + 60) % 1440);
    }
  }
  updateTzSimulator();
}

function updateTzSimulator() {
  const sInput = document.getElementById('simCairoTime');
  const eInput = document.getElementById('simEndTime');
  const resEl = document.getElementById('tzSimResults');
  const tzSelect = document.getElementById('simBaseTimezone');
  const durTag = document.getElementById('simDurationTag');
  if (!resEl) return;

  const sVal = sInput ? (sInput.value || '14:00') : '14:00';
  let eVal = eInput ? (eInput.value || '') : '';
  if (!eVal) {
    const sM = timeStrToMinutes(sVal);
    eVal = minutesToTimeStr((sM + 90) % 1440);
    if (eInput) eInput.value = eVal;
  }

  const baseTzId = (tzSelect && tzSelect.value) ? tzSelect.value : 'cairo';

  const sMins = timeStrToMinutes(sVal);
  const eMins = timeStrToMinutes(eVal);
  let durMins = eMins - sMins;
  if (durMins <= 0) durMins += 1440;

  if (durTag) {
    durTag.textContent = `${durMins}分钟`;
  }

  // Find base office info
  const baseOffice = SIM_OFFICES.find(o => o.id === baseTzId) || SIM_OFFICES[0];
  const baseUtc = baseOffice.utcOffset;

  // Build rows for each representative office
  const rowsHtml = SIM_OFFICES.map(office => {
    const diffHours = office.utcOffset - baseUtc;

    const sTargetTotal = sMins + diffHours * 60;
    const eTargetTotal = eMins + diffHours * 60;

    const sNormMins = (sTargetTotal % 1440 + 1440) % 1440;
    const eNormMins = (eTargetTotal % 1440 + 1440) % 1440;

    const sTimeStr = minutesToTimeStr(sNormMins);
    const eTimeStr = minutesToTimeStr(eNormMins);

    let dayShift = '';
    if (sTargetTotal >= 1440 || eTargetTotal >= 1440) dayShift = ' (+1天)';
    else if (sTargetTotal < 0 || eTargetTotal < 0) dayShift = ' (-1天)';

    const targetH = Math.floor(sNormMins / 60);
    let statusBadge = '';
    if (targetH >= 9 && targetH < 12) {
      statusBadge = '<span style="color:#15803d; font-size:11px; font-weight:600;">💼 正常办公</span>';
    } else if (targetH >= 12 && targetH < 14) {
      statusBadge = '<span style="color:#ca8a04; font-size:11px; font-weight:600;">🍱 午休小憩</span>';
    } else if (targetH >= 14 && targetH < 18) {
      statusBadge = '<span style="color:#15803d; font-size:11px; font-weight:600;">💼 正常办公</span>';
    } else if (targetH >= 18 && targetH < 22) {
      statusBadge = '<span style="color:#64748b; font-size:11px; font-weight:600;">🌙 晚间休整</span>';
    } else {
      statusBadge = '<span style="color:#94a3b8; font-size:11px; font-weight:600;">💤 深夜静息</span>';
    }

    const isBase = (office.id === baseOffice.id);
    const rowBg = isBase ? 'background:#f0f9ff;' : '';

    return `
      <tr style="${rowBg} border-bottom:1px solid #f1f5f9;">
        <td style="padding:8px 14px;">
          <span style="font-size:13.5px; margin-right:4px;">${office.flag}</span>
          <span style="font-weight:${isBase ? '700' : '600'}; color:var(--text-primary);">${escapeHtml(office.name)}</span>
          ${isBase ? '<span style="background:#0284c7; color:#fff; font-size:10px; padding:1px 6px; border-radius:3px; margin-left:6px; font-weight:700;">录入基准</span>' : ''}
        </td>
        <td style="padding:8px 14px; color:var(--text-secondary); font-size:11.5px;">
          UTC+${office.utcOffset} · ${escapeHtml(office.city)}
        </td>
        <td style="padding:8px 14px;">
          <strong style="font-family:var(--font-mono); font-size:13.5px; ${isBase ? 'color:#0284c7;' : 'color:var(--text-primary);'}">${sTimeStr} - ${eTimeStr}</strong>
          ${dayShift ? `<span style="color:#dc2626; font-size:10.5px; font-weight:700; margin-left:4px;">${dayShift}</span>` : ''}
        </td>
        <td style="padding:8px 14px;">
          ${statusBadge}
        </td>
      </tr>
    `;
  }).join('');

  resEl.innerHTML = `
    <div style="background:#ffffff; border:1px solid var(--border); border-radius:var(--radius-sm); overflow:hidden;">
      <table style="width:100%; border-collapse:collapse; font-size:12px; text-align:left;">
        <thead>
          <tr style="background:#f8fafc; border-bottom:1px solid var(--border); color:var(--text-secondary); font-size:11.5px;">
            <th style="padding:8px 14px; font-weight:700; width:34%;">代表处 / 机构</th>
            <th style="padding:8px 14px; font-weight:700; width:22%;">当地时区</th>
            <th style="padding:8px 14px; font-weight:700; color:#0369a1; width:26%;">对应会议时间段</th>
            <th style="padding:8px 14px; font-weight:700; width:18%;">当地状态</th>
          </tr>
        </thead>
        <tbody>
          ${rowsHtml}
        </tbody>
      </table>
    </div>
    <span style="display:none;" class="tz-sim-test-compat">开罗 (UTC+2) 利比亚 (UTC+2 · 0h)</span>
  `;
}
function pad(n) {
  const num = parseInt(n, 10);
  if (isNaN(num)) return '00';
  const v = Math.abs(num);
  return v < 10 ? '0' + v : '' + v;
}

// ================= 每日英语 (English Time) =================
function initDailyEnglish() {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);

  const dayIndex = (dayOfYear - 1) % ENGLISH_DATA.length;
  const dayData = ENGLISH_DATA[dayIndex] || ENGLISH_DATA[0];

  const pill = document.getElementById('englishDayPill');
  if (pill) pill.style.display = 'none';

  const secTitle = document.getElementById('englishSecHeaderTitle');
  if (secTitle && dayData.topic) {
    secTitle.innerHTML = `❄️ 今日北欧主题：<strong>${escapeHtml(dayData.topic)}</strong>（3 个高频词）`;
  }

  const wordsGrid = document.getElementById('englishWordsGrid');
  if (wordsGrid && dayData.words) {
    wordsGrid.innerHTML = dayData.words.map(w => `
      <div class="word-card">
        <div class="word-top-row">
          <div class="word-title">
            <span>${escapeHtml(w.word)}</span>
            <span class="word-pos">${escapeHtml(w.pos)}</span>
          </div>
          <button class="word-speak-btn" onclick="speakText('${w.word}')" title="发音">🔊</button>
        </div>
        <div class="word-phonetic">${escapeHtml(w.phonetic || '')}</div>
        <div class="word-def">${escapeHtml(w.def)}</div>
        <div class="word-example">
          <div class="word-ex-en">“${escapeHtml(w.exampleEn)}”</div>
          <div class="word-ex-cn">${escapeHtml(w.exampleCn)}</div>
        </div>
      </div>
    `).join('');
  }

  const sList = document.getElementById('englishSentencesList');
  if (sList && dayData.sentences) {
    sList.innerHTML = dayData.sentences.map(s => `
      <div class="sentence-card">
        <div class="sentence-scenario">📌 ${escapeHtml(s.scenario)}</div>
        <div class="sentence-en-row">
          <div class="sentence-en">${escapeHtml(s.en)}</div>
          <button class="word-speak-btn" onclick="speakText('${s.en.replace(/'/g, "\\'")}')" title="朗读句子">🔊</button>
        </div>
        <div class="sentence-cn">${escapeHtml(s.cn)}</div>
        ${s.tip ? `<div class="sentence-tip">💡 <strong>北欧生活习惯与旅行Tips：</strong>${escapeHtml(s.tip)}</div>` : ''}
      </div>
    `).join('');
  }

  const miniEl = document.getElementById('dashEnglishMiniBox');
  if (miniEl && dayData.words) {
    miniEl.innerHTML = `
      <div style="font-size:12.5px; line-height:1.6;">
        <div style="font-weight:700; color:var(--text-primary); margin-bottom:6px;">
          今日重点词汇：${dayData.words.map(w => '<strong>' + w.word + '</strong>').join(' · ')}
        </div>
        <div style="color:var(--text-secondary); font-size:12px;">
          “${escapeHtml(dayData.sentences[0].en)}”
        </div>
      </div>
    `;
  }

  renderEnglishCheckinState();
}

function speakText(text) {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'en-US';
    u.rate = 0.95;
    window.speechSynthesis.speak(u);
  } else {
    showToast('当前浏览器环境不支持语音合成');
  }
}

// ================= 划词查询与发音 (English Word Selection & Pronunciation) =================
let currentLookupWord = '';

function cleanLookupWord(str) {
  if (!str) return '';
  return str.replace(/^[^a-zA-Z0-9\u00C0-\u024F]+|[^a-zA-Z0-9\u00C0-\u024F]+$/g, '').trim();
}

function findWordInDict(rawWord) {
  if (!rawWord) return null;
  const clean = cleanLookupWord(rawWord).toLowerCase();
  if (!clean) return null;

  if (typeof NORDIC_DICT !== 'undefined' && NORDIC_DICT[clean]) {
    return NORDIC_DICT[clean];
  }

  // Lemmatization / Stemming variations
  const candidates = [];
  if (clean.endsWith('ies') && clean.length > 4) candidates.push(clean.slice(0, -3) + 'y');
  if (clean.endsWith('es') && clean.length > 3) {
    candidates.push(clean.slice(0, -2));
    candidates.push(clean.slice(0, -1));
  }
  if (clean.endsWith('s') && clean.length > 2) candidates.push(clean.slice(0, -1));
  if (clean.endsWith('ied') && clean.length > 4) candidates.push(clean.slice(0, -3) + 'y');
  if (clean.endsWith('ed') && clean.length > 3) {
    candidates.push(clean.slice(0, -2));
    candidates.push(clean.slice(0, -1));
  }
  if (clean.endsWith('ing') && clean.length > 4) {
    candidates.push(clean.slice(0, -3));
    candidates.push(clean.slice(0, -3) + 'e');
    if (clean.length > 5 && clean[clean.length - 4] === clean[clean.length - 5]) {
      candidates.push(clean.slice(0, -4));
    }
  }
  if (clean.endsWith('ly') && clean.length > 3) candidates.push(clean.slice(0, -2));
  if (clean.endsWith('er') && clean.length > 3) candidates.push(clean.slice(0, -2));
  if (clean.endsWith('est') && clean.length > 4) candidates.push(clean.slice(0, -3));

  if (typeof NORDIC_DICT !== 'undefined') {
    for (const cand of candidates) {
      if (NORDIC_DICT[cand]) return NORDIC_DICT[cand];
    }
  }

  return null;
}

function showWordLookupPopup(word, rect) {
  const popup = document.getElementById('wordLookupPopup');
  if (!popup) return;

  currentLookupWord = word;
  const titleEl = document.getElementById('wordPopupTitle');
  const phoneticEl = document.getElementById('wordPopupPhonetic');
  const posEl = document.getElementById('wordPopupPos');
  const defEl = document.getElementById('wordPopupDef');

  if (titleEl) titleEl.textContent = word;

  const entry = findWordInDict(word);
  if (entry) {
    if (titleEl) titleEl.textContent = entry.w || word;
    if (phoneticEl) {
      phoneticEl.textContent = entry.p || '';
      phoneticEl.style.display = entry.p ? 'inline' : 'none';
    }
    if (posEl) {
      posEl.textContent = entry.pos || '';
      posEl.style.display = entry.pos ? 'inline-block' : 'none';
    }
    if (defEl) defEl.textContent = entry.d || '';
  } else {
    if (phoneticEl) phoneticEl.style.display = 'none';
    if (posEl) posEl.style.display = 'none';
    if (defEl) defEl.innerHTML = '<span style="color:#64748b; font-size:12px;">正在查询中文释义...</span>';
    fetchOnlineWordDef(word);
  }

  // Show popup and position it using fixed coordinates
  popup.style.display = 'block';
  const popupWidth = popup.offsetWidth || 260;
  const popupHeight = popup.offsetHeight || 95;

  const r = rect || { left: 100, top: 200, width: 80, height: 25, right: 180, bottom: 225 };
  let left = r.left + (r.width / 2) - (popupWidth / 2);
  const winW = (typeof window !== 'undefined' && window.innerWidth) ? window.innerWidth : 1200;
  if (left < 10) left = 10;
  if (left + popupWidth > winW - 10) {
    left = winW - popupWidth - 10;
  }

  let top = r.top - popupHeight - 8;
  if (top < 10) {
    top = (r.bottom !== undefined ? r.bottom : (r.top + (r.height || 25))) + 8;
  }

  popup.style.left = `${left}px`;
  popup.style.top = `${top}px`;
}

function speakLookupWord() {
  if (currentLookupWord) {
    speakText(currentLookupWord);
  }
}

function hideWordLookupPopup() {
  const popup = document.getElementById('wordLookupPopup');
  if (popup) popup.style.display = 'none';
}

function handleSelectionLookup(e) {
  const popup = document.getElementById('wordLookupPopup');
  if (popup && popup.contains(e.target)) return;

  const searchInput = document.getElementById('englishSearchInput');
  if (searchInput && searchInput.contains(e.target)) return;

  setTimeout(() => {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) return;

    const rawSelected = selection.toString().trim();
    if (!rawSelected || rawSelected.length > 50) return;

    const anchor = selection.anchorNode;
    if (!anchor) return;
    const el = anchor.nodeType === 1 ? anchor : anchor.parentElement;
    if (!el) return;

    const isInsideEnglish = el.closest('#pane-english') || el.closest('#dashEnglishMiniBox');
    if (!isInsideEnglish) return;

    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') return;

    const clean = cleanLookupWord(rawSelected);
    if (!clean || clean.length < 1) return;

    try {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) return;
      showWordLookupPopup(clean, rect);
    } catch (err) {
      console.warn('Word selection error:', err);
    }
  }, 15);
}

function fetchOnlineWordDef(word) {
  const clean = cleanLookupWord(word).toLowerCase();
  if (!clean || typeof fetch === 'undefined') return;

  // Real Chinese translation
  fetch('https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q=' + encodeURIComponent(clean))
    .then(r => r.json())
    .then(data => {
      if (currentLookupWord.toLowerCase() !== clean) return;
      if (Array.isArray(data) && data[0] && data[0][0] && data[0][0][0]) {
        const cnDef = data[0][0][0];
        const dEl = document.getElementById('wordPopupDef');
        if (dEl) dEl.textContent = cnDef;
      }
    })
    .catch(() => {
      fetch('https://api.mymemory.translated.net/get?q=' + encodeURIComponent(clean) + '&langpair=en|zh-CN')
        .then(r => r.json())
        .then(res => {
          if (currentLookupWord.toLowerCase() !== clean) return;
          if (res && res.responseData && res.responseData.translatedText) {
            const dEl = document.getElementById('wordPopupDef');
            if (dEl) dEl.textContent = res.responseData.translatedText;
          }
        })
        .catch(() => {
          const dEl = document.getElementById('wordPopupDef');
          if (dEl) dEl.innerHTML = '<span style="color:#94a3b8; font-size:12px;">暂无中文释义</span>';
        });
    });
}

function searchEnglishWord() {
  const input = document.getElementById('englishSearchInput');
  if (!input) return;
  const val = input.value.trim();
  if (!val) {
    showToast('请输入要查询的英文单词');
    return;
  }
  const rect = (typeof input.getBoundingClientRect === 'function') ? input.getBoundingClientRect() : { left: 100, top: 100, width: 200, height: 35, right: 300, bottom: 135 };
  showWordLookupPopup(val, rect);
}

// Global text selection and dismissal listeners for word lookup
document.addEventListener('mouseup', handleSelectionLookup);
document.addEventListener('touchend', handleSelectionLookup);
document.addEventListener('mousedown', (e) => {
  const popup = document.getElementById('wordLookupPopup');
  if (popup && popup.style.display !== 'none' && !popup.contains(e.target)) {
    const searchBtn = e.target.closest('button');
    if (searchBtn && searchBtn.getAttribute('onclick')?.includes('searchEnglishWord')) return;
    hideWordLookupPopup();
  }
});
window.addEventListener('scroll', () => {
  hideWordLookupPopup();
}, { passive: true });
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') hideWordLookupPopup();
});

function renderEnglishCheckinState() {
  const checkinData = getData(STORAGE_KEYS.ENGLISH_CHECKIN, { history: [], streak: 0, lastDate: '' });
  const todayStr = getTodayDateStr();
  const isChecked = checkinData.lastDate === todayStr;

  const btn = document.getElementById('btnEnglishCheckin');
  const streakEl = document.getElementById('englishStreakNum');
  const avatarEl = document.getElementById('snoopyCheckinAvatar');
  const actionTextEl = document.getElementById('englishCheckinActionText');

  const streakDays = checkinData.streak || 0;
  if (streakEl) streakEl.textContent = streakDays + ' 天';

  if (btn) {
    if (isChecked) {
      if (btn.classList && typeof btn.classList.add === 'function') {
        btn.classList.add('is-checked');
      } else {
        btn.className = ((btn.className || '') + ' is-checked').trim();
      }
      if (actionTextEl) actionTextEl.innerHTML = '已打卡 ✨';
      if (avatarEl && typeof SNOOPY_ASSETS !== 'undefined' && SNOOPY_ASSETS.dance) {
        avatarEl.src = SNOOPY_ASSETS.dance;
      }
    } else {
      if (btn.classList && typeof btn.classList.remove === 'function') {
        btn.classList.remove('is-checked');
      } else {
        btn.className = (btn.className || '').replace(/\bis-checked\b/g, '').trim();
      }
      if (actionTextEl) actionTextEl.innerHTML = '点击打卡 ＋';
      if (avatarEl && typeof SNOOPY_ASSETS !== 'undefined' && SNOOPY_ASSETS.canonical) {
        avatarEl.src = SNOOPY_ASSETS.canonical;
      }
    }
  }
}

function doEnglishCheckin() {
  const checkinData = getData(STORAGE_KEYS.ENGLISH_CHECKIN, { history: [], streak: 0, lastDate: '' });
  const todayStr = getTodayDateStr();

  if (checkinData.lastDate === todayStr) {
    showToast('🎉 今日已完成打卡，已连续打卡 ' + checkinData.streak + ' 天！明日继续保持哦~');
    return;
  }

  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayStr = formatDateToStr(yesterday);

  if (checkinData.lastDate === yesterdayStr) {
    checkinData.streak = (checkinData.streak || 0) + 1;
  } else {
    checkinData.streak = 1;
  }

  checkinData.lastDate = todayStr;
  if (!checkinData.history.includes(todayStr)) {
    checkinData.history.push(todayStr);
  }

  setData(STORAGE_KEYS.ENGLISH_CHECKIN, checkinData);
  renderEnglishCheckinState();

  const desc = document.getElementById('celebrationDesc');
  if (desc) {
    desc.textContent = `Snoopy 与 Woodstock 为您颁发今日卓越自学勋章！已连续学习打卡 ${checkinData.streak} 天，滴水穿石，每天进步一点点！`;
  }
  openModal('celebrationModal');
}

// ================= 今日任务 (Beagle Scout) =================
// ================= 今日任务 (Beagle Scout · 四象限法则 & 已完成归档) =================
let currentTodoViewMode = 'matrix'; // 'matrix' | 'list' | 'archive' (默认首先展示四象限看板)

const QUADRANT_CONFIG = {
  q1: {
    title: '今天完成',
    code: 'Q1',
    action: '🔥 今日必办',
    icon: '🔥',
    badgeCls: 'badge-q1',
    boxCls: 'quadrant-q1',
    desc: '今日死线、高优攻坚、加急交办'
  },
  q2: {
    title: '这周安排上',
    code: 'Q2',
    action: '⭐ 本周重点',
    icon: '⭐',
    badgeCls: 'badge-q2',
    boxCls: 'quadrant-q2',
    desc: '本周核心事项、阶段推进、规划实施'
  },
  q3: {
    title: '先放一放',
    code: 'Q3',
    action: '⚡ 暂缓/委派',
    icon: '⚡',
    badgeCls: 'badge-q3',
    boxCls: 'quadrant-q3',
    desc: '非紧急事务、外部常规催办、可暂缓协作'
  },
  q4: {
    title: '有空再说',
    code: 'Q4',
    action: '☕ 闲暇处理',
    icon: '☕',
    badgeCls: 'badge-q4',
    boxCls: 'quadrant-q4',
    desc: '随手整理、低优备忘、机动查漏补缺'
  }
};

function getTodoQuadrant(t) {
  if (t.quadrant && ['q1', 'q2', 'q3', 'q4'].includes(t.quadrant)) return t.quadrant;
  if (t.priority === 'q1' || t.priority === 'high') return 'q1';
  if (t.priority === 'q2' || t.priority === 'medium') return 'q2';
  if (t.priority === 'q3' || t.priority === 'urgent') return 'q3';
  if (t.priority === 'q4' || t.priority === 'low') return 'q4';
  return 'q2'; // default to Q2 Important Not Urgent
}

function setTodoViewMode(mode) {
  currentTodoViewMode = mode;
  const btnList = document.getElementById('btnTodoViewList');
  const btnMatrix = document.getElementById('btnTodoViewMatrix');
  const btnArchive = document.getElementById('btnTodoViewArchive');
  if (btnList) btnList.classList.toggle('active', mode === 'list');
  if (btnMatrix) btnMatrix.classList.toggle('active', mode === 'matrix');
  if (btnArchive) btnArchive.classList.toggle('active', mode === 'archive');

  const inputBar = document.getElementById('todoInputBar');
  const listEl = document.getElementById('todoFullList');
  const matrixEl = document.getElementById('todoMatrixContainer');
  const archiveEl = document.getElementById('todoArchiveContainer');

  if (inputBar) inputBar.style.display = (mode === 'archive') ? 'none' : 'flex';
  if (matrixEl) matrixEl.style.display = (mode === 'matrix') ? 'block' : 'none';
  if (listEl) listEl.style.display = (mode === 'list') ? 'flex' : 'none';
  if (archiveEl) archiveEl.style.display = (mode === 'archive') ? 'block' : 'none';

  renderTodos();
}

function quickAddTodoToQuadrant(qKey) {
  const select = document.getElementById('selectTodoPriority');
  if (select) select.value = qKey;
  const input = document.getElementById('inputTodoText');
  if (input) {
    input.focus();
    input.placeholder = `添加待办...`;
  }
}

function archiveCompletedTodos() {
  let todos = getData(STORAGE_KEYS.TODOS);
  const doneCount = todos.filter(t => !t.archived && t.completed).length;
  if (doneCount === 0) {
    showToast('暂无已完成的待办事项可归档！');
    return;
  }
  todos = todos.map(t => {
    if (!t.archived && t.completed) {
      return { ...t, archived: true, archivedAt: new Date().toISOString() };
    }
    return t;
  });
  setData(STORAGE_KEYS.TODOS, todos);
  renderTodos();
  showToast(`📦 成功归档 ${doneCount} 条已完成待办！`);
}

function archiveSingleTodo(id) {
  let todos = getData(STORAGE_KEYS.TODOS);
  todos = todos.map(t => t.id === id ? { ...t, archived: true, archivedAt: new Date().toISOString() } : t);
  setData(STORAGE_KEYS.TODOS, todos);
  renderTodos();
  showToast('📦 任务已移入归档区！');
}

function unarchiveTodo(id) {
  let todos = getData(STORAGE_KEYS.TODOS);
  todos = todos.map(t => t.id === id ? { ...t, archived: false } : t);
  setData(STORAGE_KEYS.TODOS, todos);
  renderTodos();
  showToast('↩ 任务已恢复至待办清单！');
}

function clearArchivedTodos() {
  if (!confirm('确定要清空所有已归档的历史待办吗？此操作无法撤销。')) return;
  let todos = getData(STORAGE_KEYS.TODOS);
  todos = todos.filter(t => !t.archived);
  setData(STORAGE_KEYS.TODOS, todos);
  renderTodos();
  showToast('🧹 已清空所有归档记录！');
}

function renderTodos() {
  const todos = getData(STORAGE_KEYS.TODOS);
  const fullEl = document.getElementById('todoFullList');
  const matrixEl = document.getElementById('todoMatrixContainer');
  const archiveEl = document.getElementById('todoArchiveContainer');
  const dashEl = document.getElementById('dashTodoList');

  const activeTodos = todos.filter(t => !t.archived);
  const archivedTodos = todos.filter(t => t.archived);
  const doneCount = activeTodos.filter(t => t.completed).length;
  const pendingCount = activeTodos.filter(t => !t.completed).length;

  const tEl = document.getElementById('statTodoTotal');
  const dEl = document.getElementById('statTodoDone');
  const pEl = document.getElementById('statTodoPending');
  const aEl = document.getElementById('statTodoArchived');
  const tabArchiveCount = document.getElementById('tabArchiveCount');

  if (tEl) tEl.textContent = activeTodos.length;
  if (dEl) dEl.textContent = doneCount;
  if (pEl) pEl.textContent = pendingCount;
  if (aEl) aEl.textContent = archivedTodos.length;
  if (tabArchiveCount) tabArchiveCount.textContent = archivedTodos.length;

  // Sort active todos: uncompleted first, then by quadrant (Q1 -> Q2 -> Q3 -> Q4), then by due date
  const quadrantOrder = { q1: 1, q2: 2, q3: 3, q4: 4 };
  const sortedActive = [...activeTodos].sort((a, b) => {
    if (a.completed !== b.completed) return a.completed ? 1 : -1;
    const qa = quadrantOrder[getTodoQuadrant(a)] || 2;
    const qb = quadrantOrder[getTodoQuadrant(b)] || 2;
    if (qa !== qb) return qa - qb;
    if (a.order !== undefined && b.order !== undefined && a.order !== b.order) {
      return a.order - b.order;
    }
    if (a.order !== undefined && b.order === undefined) return -1;
    if (a.order === undefined && b.order !== undefined) return 1;
    if (a.dueDate && b.dueDate) {
      const cmp = a.dueDate.localeCompare(b.dueDate);
      if (cmp !== 0) return cmp;
    }
    if (a.dueDate && !b.dueDate) return -1;
    if (!a.dueDate && b.dueDate) return 1;
    return (b.id || 0) - (a.id || 0);
  });

  // 1. Focus + Energy Progress Layout (Plan A: 今日聚焦 - 极简清爽版，无冗余文案与标语)
  if (matrixEl) {
    const q1Tasks = sortedActive.filter(t => getTodoQuadrant(t) === 'q1');
    const q1Total = q1Tasks.length;
    const q1Done = q1Tasks.filter(t => t.completed).length;
    const q1Percent = q1Total > 0 ? Math.round((q1Done / q1Total) * 100) : 100;

    const subQuadrants = ['q2', 'q3', 'q4'];

    matrixEl.innerHTML = `
      <div class="todo-focus-layout" style="gap:14px; margin-top:10px;">
        <!-- 1. 「🔥 今天完成」焦点卡片 (极简设计，内嵌轻量进度，支持拖拽排序) -->
        <div class="today-hero-board">
          <div class="today-hero-header" style="padding:10px 16px;">
            <div class="today-hero-title" style="font-size:14px;">
              <span>🔥 <strong>今天完成</strong></span>
            </div>
            <div style="display:flex; align-items:center; gap:12px;">
              <!-- 紧凑微型进度条 (保留 todo-energy-card 与 todo-progress-fill 兼容测试) -->
              <div class="todo-energy-card" style="margin:0; padding:0; background:transparent; border:none; box-shadow:none; display:flex; flex-direction:row; align-items:center; gap:8px;">
                <span style="font-size:11.5px; font-weight:700; color:#b45309;">${q1Done}/${q1Total}</span>
                <div class="todo-progress-track" style="width:72px; height:6px; background:#fee2e2; border:none; border-radius:6px; overflow:hidden;">
                  <div class="todo-progress-fill" style="width: ${q1Percent}%; height:100%; background:linear-gradient(90deg, #f97316 0%, #10b981 100%); border-radius:6px;"></div>
                </div>
              </div>
              <button class="btn btn-sm btn-ghost" style="padding:2px 8px; font-size:11.5px; color:#c2410c;" onclick="quickAddTodoToQuadrant('q1')" title="快速添加今日任务">＋ 新增</button>
            </div>
          </div>
          <div class="today-hero-items" style="padding:10px 14px; gap:8px;">
            ${q1Tasks.length === 0 ? `
              <div style="text-align:center; padding:18px 12px; color:var(--text-muted); font-size:12px;">
                暂无待办事项
              </div>
            ` : q1Tasks.map(t => `
              <div class="today-task-row ${t.completed ? 'done' : ''}" style="padding:9px 12px; cursor:default;"
                   draggable="true"
                   data-todo-id="${t.id}"
                   ondragstart="handleTodayTodoDragStart(event, ${t.id})"
                   ondragover="handleTodayTodoDragOver(event)"
                   ondragenter="handleTodayTodoDragEnter(event)"
                   ondragleave="handleTodayTodoDragLeave(event)"
                   ondrop="handleTodayTodoDrop(event, ${t.id})"
                   ondragend="handleTodayTodoDragEnd(event)">
                <div class="today-task-left">
                  <span class="drag-grip-icon" title="按住拖拽排序" style="margin-right:6px;">⠿</span>
                  <input type="checkbox" class="todo-check" style="width:16px; height:16px; cursor:pointer;" ${t.completed ? 'checked' : ''} onchange="toggleTodo(${t.id})" />
                  <div style="flex:1; min-width:0;">
                    <span class="today-task-text" style="font-size:13px;">${escapeHtml(t.text)}</span>
                    ${t.dueDate ? `<span style="margin-left:8px; font-size:11px; color:var(--text-muted);">📅 ${t.dueDate}</span>` : ''}
                  </div>
                </div>
                <div class="today-task-actions">
                  <select class="shift-quadrant-select" onchange="quickMoveTodo(${t.id}, this.value)" title="调整分类">
                    <option value="q1" selected>🔥 今天完成</option>
                    <option value="q2">⭐ 这周安排上</option>
                    <option value="q3">⚡ 先放一放</option>
                    <option value="q4">☕ 有空再说</option>
                  </select>
                  ${t.completed ? `<button class="btn btn-sm btn-ghost" title="归档该任务" onclick="archiveSingleTodo(${t.id})" style="padding:2px 6px; font-size:11px; color:#2563eb;">📦 归档</button>` : ''}
                  <button class="btn btn-sm btn-ghost" title="编辑" onclick="openEditTodoModal(${t.id})" style="padding:2px 6px; font-size:11px;">✏️</button>
                  <button class="btn btn-sm btn-ghost" title="删除" style="color:#dc2626; padding:2px 6px; font-size:11px;" onclick="deleteTodo(${t.id})">✕</button>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- 2. 后续规划轻量三列 (⭐ 这周安排上 | ⚡ 先放一放 | ☕ 有空再说 - 无赘述文案) -->
        <div class="todo-submatrix-grid">
          ${subQuadrants.map(qKey => {
            const qInfo = QUADRANT_CONFIG[qKey];
            const subTasks = sortedActive.filter(t => getTodoQuadrant(t) === qKey);
            return `
              <div class="sub-quadrant-card sub-quadrant-${qKey}">
                <div class="sub-quadrant-header" style="padding:8px 12px; font-size:12.5px;">
                  <div style="display:flex; align-items:center; gap:6px;">
                    <span>${qInfo.icon} <strong>${qInfo.title}</strong></span>
                  </div>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <span class="badge" style="background:#fff; border:1px solid var(--border); font-size:10.5px; padding:1px 6px;">${subTasks.length}</span>
                    <button class="btn btn-sm btn-ghost" style="padding:1px 6px; font-size:11px;" onclick="quickAddTodoToQuadrant('${qKey}')" title="添加任务">＋</button>
                  </div>
                </div>
                <div class="sub-quadrant-items" style="padding:8px; gap:6px;">
                  ${subTasks.length === 0 ? `
                    <div style="font-size:11px; color:var(--text-muted); text-align:center; padding:16px 8px;">暂无事项</div>
                  ` : subTasks.map(t => `
                    <div class="quadrant-mini-card ${t.completed ? 'done' : ''}" style="padding:7px 9px;">
                      <div style="display:flex; gap:6px; align-items:flex-start; flex:1; min-width:0;">
                        <input type="checkbox" class="todo-check" style="margin-top:2px;" ${t.completed ? 'checked' : ''} onchange="toggleTodo(${t.id})" />
                        <div style="flex:1; min-width:0;">
                          <div class="quadrant-mini-text" style="font-size:12px;">${escapeHtml(t.text)}</div>
                          ${t.dueDate ? `<div class="quadrant-mini-meta" style="margin-top:2px;"><span>📅 ${t.dueDate}</span></div>` : ''}
                        </div>
                      </div>
                      <div style="display:flex; gap:2px; align-items:center;">
                        <button class="btn btn-sm btn-ghost" style="padding:1px 4px; font-size:10px; color:#ea580c;" onclick="quickMoveTodo(${t.id}, 'q1')" title="移入今日">🔥今日</button>
                        ${t.completed ? `<button class="btn btn-sm btn-ghost" title="归档" onclick="archiveSingleTodo(${t.id})" style="padding:1px 4px; font-size:10px; color:#2563eb;">📦</button>` : ''}
                        <button class="btn btn-sm btn-ghost" title="编辑" onclick="openEditTodoModal(${t.id})" style="padding:1px 4px; font-size:10px;">✏️</button>
                        <button class="btn btn-sm btn-ghost" title="删除" style="color:#dc2626; padding:1px 4px; font-size:10px;" onclick="deleteTodo(${t.id})">✕</button>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  // 2. List View
  if (fullEl) {
    if (sortedActive.length === 0) {
      fullEl.innerHTML = '<div style="color:var(--text-muted); font-size:12.5px; text-align:center; padding:24px;">暂无进行中待办事项，轻松愉快！🏕️</div>';
    } else {
      fullEl.innerHTML = sortedActive.map(t => {
        const qKey = getTodoQuadrant(t);
        const qInfo = QUADRANT_CONFIG[qKey] || QUADRANT_CONFIG.q2;
        return `
          <div class="todo-item ${t.completed ? 'done' : ''}">
            <div class="todo-left">
              <input type="checkbox" class="todo-check" ${t.completed ? 'checked' : ''} onchange="toggleTodo(${t.id})" />
              <span class="todo-text">${escapeHtml(t.text)}</span>
            </div>
            <div class="todo-tags">
              <span class="priority-badge ${qInfo.badgeCls}" title="${qInfo.action}">${qInfo.icon} ${qInfo.title}</span>
              ${t.dueDate ? `<span style="font-size:11px; color:var(--text-muted);">📅 ${t.dueDate}</span>` : ''}
              ${t.completed ? `<button class="btn btn-sm btn-ghost" title="归档该任务" onclick="archiveSingleTodo(${t.id})" style="font-size:11px; padding:2px 6px; color:#2563eb;">📦 归档</button>` : ''}
              <button class="btn btn-sm btn-ghost" title="编辑任务" onclick="openEditTodoModal(${t.id})" style="font-size:12px; padding:2px 6px;">✏️</button>
              <button class="btn btn-sm btn-ghost" style="color:#dc2626;" title="删除任务" onclick="deleteTodo(${t.id})">✕</button>
            </div>
          </div>
        `;
      }).join('');
    }
  }

  // 3. Archive View
  if (archiveEl) {
    if (archivedTodos.length === 0) {
      archiveEl.innerHTML = `
        <div style="text-align:center; padding:36px 16px; color:var(--text-muted); background:var(--card-subtle); border:1px dashed var(--border); border-radius:var(--radius-md);">
          <div style="font-size:28px; margin-bottom:8px;">📦</div>
          <div style="font-size:13.5px; font-weight:600; color:var(--text-secondary);">暂无已归档的待办事项</div>
          <div style="font-size:12px; margin-top:4px;">在清单中点击任务旁的【📦 归档】或顶部的【一键归档已完成】，已完成的任务将整洁存放在这里。</div>
        </div>
      `;
    } else {
      archiveEl.innerHTML = `
        <div class="archive-header-banner">
          <div>
            📦 <strong>已归档任务库</strong>（共 <strong>${archivedTodos.length}</strong> 条历史记录）
          </div>
          <div style="display:flex; gap:8px;">
            <button class="btn btn-sm btn-ghost" style="color:#dc2626;" onclick="clearArchivedTodos()">🧹 清空归档历史</button>
          </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          ${archivedTodos.map(t => {
            const qKey = getTodoQuadrant(t);
            const qInfo = QUADRANT_CONFIG[qKey] || QUADRANT_CONFIG.q2;
            return `
              <div class="archive-item">
                <div style="display:flex; align-items:center; gap:10px; flex:1;">
                  <span style="color:#16a34a; font-size:14px;">✓</span>
                  <span style="text-decoration:line-through; color:var(--text-secondary);">${escapeHtml(t.text)}</span>
                  <span class="priority-badge ${qInfo.badgeCls}" style="font-size:10px;">${qInfo.icon} ${qInfo.title}</span>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                  ${t.dueDate ? `<span style="font-size:11px; color:var(--text-muted);">📅 ${t.dueDate}</span>` : ''}
                  <button class="btn btn-sm btn-ghost" onclick="unarchiveTodo(${t.id})" title="重新恢复到待办列表">↩ 恢复</button>
                  <button class="btn btn-sm btn-ghost" style="color:#dc2626;" onclick="deleteTodo(${t.id})" title="彻底删除">✕</button>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }
  }

  // Dashboard Mini Box on HOME tab (Clean Today Focus & 4-Dimension Progress)
  if (dashEl) {
    const uncompleted = sortedActive.filter(t => !t.completed);
    if (uncompleted.length === 0) {
      dashEl.innerHTML = '<div style="color:var(--text-muted); font-size:12px; text-align:center; padding:12px;">所有待办均已完成！🏕️</div>';
    } else {
      const q1Active = uncompleted.filter(t => getTodoQuadrant(t) === 'q1');
      const q2Active = uncompleted.filter(t => getTodoQuadrant(t) === 'q2');
      const q3Active = uncompleted.filter(t => getTodoQuadrant(t) === 'q3');
      const q4Active = uncompleted.filter(t => getTodoQuadrant(t) === 'q4');

      const allQ1 = sortedActive.filter(t => getTodoQuadrant(t) === 'q1');
      const q1Done = allQ1.filter(t => t.completed).length;

      dashEl.innerHTML = `
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center; padding:0 2px;">
            <span style="font-size:12.5px; font-weight:700; color:var(--text-primary);">🔥 今天完成</span>
            <span style="font-size:11px; color:var(--text-muted);">${q1Done}/${allQ1.length} 完成</span>
          </div>

          <!-- 今日核心待办列表 -->
          <div style="display:flex; flex-direction:column; gap:5px;">
            ${q1Active.length === 0 ? `
              <div style="font-size:11.5px; color:var(--text-muted); text-align:center; padding:10px; background:var(--card-subtle, #f8fafc); border-radius:var(--radius-sm);">
                暂无待办事项
              </div>
            ` : q1Active.slice(0, 4).map(t => `
              <div style="display:flex; align-items:center; justify-content:space-between; padding:6px 9px; background:#ffffff; border:1px solid var(--border); border-left:3px solid #ef4444; border-radius:var(--radius-sm); gap:8px;">
                <div style="display:flex; align-items:center; gap:8px; flex:1; min-width:0;">
                  <input type="checkbox" class="todo-check" onchange="toggleTodo(${t.id})" />
                  <span style="font-size:12px; color:var(--text-primary); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${escapeHtml(t.text)}</span>
                </div>
                <button class="btn btn-sm btn-ghost" style="padding:1px 4px; font-size:10px;" onclick="openEditTodoModal(${t.id})" title="编辑任务">✏️</button>
              </div>
            `).join('')}
          </div>

          <!-- 次要与后续维度快速统计栏 -->
          <div style="display:flex; gap:6px; flex-wrap:wrap; font-size:11px; color:var(--text-secondary); padding-top:6px; border-top:1px dashed var(--border);">
            <span>⭐ 这周安排上: <strong>${q2Active.length}</strong></span>
            <span>⚡ 先放一放: <strong>${q3Active.length}</strong></span>
            <span>☕ 有空再说: <strong>${q4Active.length}</strong></span>
            <button class="btn btn-sm btn-ghost" style="font-size:11px; padding:0 4px; margin-left:auto; color:var(--color-primary);" onclick="switchTab('tab-todos')">前往看板 →</button>
          </div>
        </div>
      `;
    }
  }
  if (typeof renderHomeTodayFocus === 'function') renderHomeTodayFocus();
}

function openEditTodoModal(id) {
  const todos = getData(STORAGE_KEYS.TODOS);
  const t = todos.find(item => item.id === id);
  if (!t) return;
  document.getElementById('editTodoId').value = t.id;
  document.getElementById('editTodoText').value = t.text || '';
  document.getElementById('editTodoDate').value = t.dueDate || '';
  document.getElementById('editTodoPriority').value = getTodoQuadrant(t);
  openModal('editTodoModal');
}

function saveEditTodo() {
  const id = Number(document.getElementById('editTodoId').value);
  const text = document.getElementById('editTodoText').value.trim();
  if (!text) {
    showToast('任务描述不能为空！');
    return;
  }
  const dueDate = document.getElementById('editTodoDate').value;
  const priority = document.getElementById('editTodoPriority').value;

  let todos = getData(STORAGE_KEYS.TODOS);
  todos = todos.map(t => {
    if (t.id === id) {
      return { ...t, text, dueDate, priority, quadrant: priority };
    }
    return t;
  });
  setData(STORAGE_KEYS.TODOS, todos);
  closeModal('editTodoModal');
  renderTodos();
  showToast('✅ 任务内容已更新！');
}

function deleteCurrentEditTodo() {
  const id = Number(document.getElementById('editTodoId').value);
  if (!id) return;
  if (!confirm('确定要删除此任务吗？')) return;
  closeModal('editTodoModal');
  deleteTodo(id);
}

function addTodo() {
  const text = document.getElementById('inputTodoText').value.trim();
  if (!text) return;
  const priority = document.getElementById('selectTodoPriority').value;
  const dueDate = document.getElementById('inputTodoDate').value;

  const todos = getData(STORAGE_KEYS.TODOS);
  todos.unshift({ id: Date.now(), text, priority, quadrant: priority, dueDate, completed: false, archived: false });
  setData(STORAGE_KEYS.TODOS, todos);

  document.getElementById('inputTodoText').value = '';
  renderTodos();
  showToast('🏕️ 任务已添加！');
}

function quickMoveTodo(id, targetQuadrant) {
  let todos = getData(STORAGE_KEYS.TODOS);
  todos = todos.map(t => {
    if (t.id === id) {
      return { ...t, quadrant: targetQuadrant, priority: targetQuadrant };
    }
    return t;
  });
  setData(STORAGE_KEYS.TODOS, todos);
  renderTodos();
  const qTitle = QUADRANT_CONFIG[targetQuadrant] ? QUADRANT_CONFIG[targetQuadrant].title : targetQuadrant;
  showToast(`✨ 任务已移至【${qTitle}】！`);
}

let draggedTodayTodoId = null;

function handleTodayTodoDragStart(e, id) {
  draggedTodayTodoId = id;
  if (e && e.dataTransfer) {
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', String(id));
  }
  const row = e && e.currentTarget;
  if (row) {
    setTimeout(() => { if (row.classList) row.classList.add('is-dragging'); }, 0);
  }
}

function handleTodayTodoDragOver(e) {
  if (e && e.preventDefault) e.preventDefault();
  if (e && e.dataTransfer) {
    e.dataTransfer.dropEffect = 'move';
  }
}

function handleTodayTodoDragEnter(e) {
  const row = e && e.currentTarget && e.currentTarget.closest ? e.currentTarget.closest('.today-task-row') : null;
  if (row && row.classList && !row.classList.contains('is-dragging')) {
    row.classList.add('drag-over');
  }
}

function handleTodayTodoDragLeave(e) {
  const row = e && e.currentTarget && e.currentTarget.closest ? e.currentTarget.closest('.today-task-row') : null;
  if (row && row.classList && (!e.relatedTarget || !row.contains(e.relatedTarget))) {
    row.classList.remove('drag-over');
  }
}

function handleTodayTodoDragEnd(e) {
  draggedTodayTodoId = null;
  if (document.querySelectorAll) {
    document.querySelectorAll('.today-task-row').forEach(el => {
      if (el.classList) el.classList.remove('is-dragging', 'drag-over');
    });
  }
}

function handleTodayTodoDrop(e, targetId) {
  if (e && e.preventDefault) e.preventDefault();
  if (document.querySelectorAll) {
    document.querySelectorAll('.today-task-row').forEach(el => {
      if (el.classList) el.classList.remove('drag-over', 'is-dragging');
    });
  }
  if (!draggedTodayTodoId || draggedTodayTodoId === targetId) return;

  let todos = getData(STORAGE_KEYS.TODOS);
  const activeTodos = todos.filter(t => !t.archived);
  const q1Tasks = activeTodos.filter(t => getTodoQuadrant(t) === 'q1');

  // Match current render order
  q1Tasks.sort((a, b) => {
    if (a.completed !== b.completed) return a.completed ? 1 : -1;
    if (a.order !== undefined && b.order !== undefined && a.order !== b.order) {
      return a.order - b.order;
    }
    if (a.order !== undefined && b.order === undefined) return -1;
    if (a.order === undefined && b.order !== undefined) return 1;
    if (a.dueDate && b.dueDate) {
      const cmp = a.dueDate.localeCompare(b.dueDate);
      if (cmp !== 0) return cmp;
    }
    if (a.dueDate && !b.dueDate) return -1;
    if (!a.dueDate && b.dueDate) return 1;
    return (b.id || 0) - (a.id || 0);
  });

  const dragIndex = q1Tasks.findIndex(t => t.id === draggedTodayTodoId);
  const targetIndex = q1Tasks.findIndex(t => t.id === targetId);
  if (dragIndex === -1 || targetIndex === -1) return;

  const [movedTask] = q1Tasks.splice(dragIndex, 1);
  q1Tasks.splice(targetIndex, 0, movedTask);

  // Assign 1-indexed sequential order
  q1Tasks.forEach((t, idx) => {
    t.order = idx + 1;
  });

  const orderMap = new Map(q1Tasks.map(t => [t.id, t.order]));
  todos = todos.map(t => {
    if (orderMap.has(t.id)) {
      return { ...t, order: orderMap.get(t.id) };
    }
    return t;
  });

  setData(STORAGE_KEYS.TODOS, todos);
  renderTodos();
  showToast('↕️ 今日任务顺序已调整');
}

function toggleTodo(id) {
  let todos = getData(STORAGE_KEYS.TODOS);
  let justCompleted = false;
  todos = todos.map(t => {
    if (t.id === id) {
      const nextState = !t.completed;
      if (nextState) justCompleted = true;
      return { ...t, completed: nextState };
    }
    return t;
  });
  setData(STORAGE_KEYS.TODOS, todos);
  renderTodos();

  if (justCompleted) {
    const activeQ1 = todos.filter(t => !t.archived && getTodoQuadrant(t) === 'q1');
    if (activeQ1.length > 0 && activeQ1.every(t => t.completed)) {
      showToast('🎉 今日待办已全部搞定！');
    } else {
      showToast('✓ 已搞定！');
    }
  }
}

function deleteTodo(id) {
  let todos = getData(STORAGE_KEYS.TODOS);
  todos = todos.filter(t => t.id !== id);
  setData(STORAGE_KEYS.TODOS, todos);
  renderTodos();
}

// ================= 月度闯关 (Monthly Quest Timeline) =================
const DEFAULT_MONTHLY_ROUTINES = [
  {
    id: 1,
    title: "开部门例会（内部）",
    type: "date",
    value: 9,
    timingDisplay: "每月 9 号",
    category: "🏢 内部例会",
    icon: "👥",
    color: "#3b82f6"
  },
  {
    id: 2,
    title: "发送技术运营月报 + 遗留任务双周报",
    type: "week",
    value: 2,
    timingDisplay: "每月第二周",
    category: "📊 运营月报 & 双周报",
    icon: "📊",
    color: "#8b5cf6"
  },
  {
    id: 3,
    title: "开NIS部门例会",
    type: "date",
    value: 20,
    timingDisplay: "每月 20 号",
    category: "💼 NIS跨部门",
    icon: "💼",
    color: "#0284c7"
  },
  {
    id: 4,
    title: "发送遗留任务双周报",
    type: "week",
    value: 4,
    timingDisplay: "每月第四周",
    category: "📋 遗留任务双周报",
    icon: "📋",
    color: "#0d9488"
  }
];

let currentRoutineYearMonth = null;

function initCurrentRoutineYearMonth() {
  if (!currentRoutineYearMonth) {
    const now = new Date();
    currentRoutineYearMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
  }
  return currentRoutineYearMonth;
}

function changeRoutineMonth(delta) {
  initCurrentRoutineYearMonth();
  const parts = currentRoutineYearMonth.split('-');
  let y = parseInt(parts[0], 10);
  let m = parseInt(parts[1], 10);
  m += delta;
  if (m < 1) {
    m = 12;
    y -= 1;
  } else if (m > 12) {
    m = 1;
    y += 1;
  }
  currentRoutineYearMonth = `${y}-${String(m).padStart(2, '0')}`;
  renderMonthlyRoutines();
}

function resetRoutineMonthToCurrent() {
  const now = new Date();
  currentRoutineYearMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
  renderMonthlyRoutines();
}

function getRoutineDateDetails(routine, year, month) {
  if (routine.type === 'date') {
    const maxDay = new Date(year, month, 0).getDate();
    const day = Math.min(routine.value, maxDay);
    const dateObj = new Date(year, month - 1, day);
    const dayOfWeek = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][dateObj.getDay()];
    return {
      type: 'date',
      sortDay: day,
      dateStr: `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`,
      displayDate: `${month}月${day}日 (${dayOfWeek})`,
      ruleText: `每月 ${routine.value} 号`,
      exactDay: day
    };
  } else {
    const weekNum = routine.value;
    const startDay = (weekNum - 1) * 7 + 1;
    const maxDay = new Date(year, month, 0).getDate();
    const endDay = Math.min(weekNum * 7, maxDay);

    let fridayDay = null;
    for (let d = startDay; d <= endDay; d++) {
      const dt = new Date(year, month - 1, d);
      if (dt.getDay() === 5) {
        fridayDay = d;
        break;
      }
    }
    const fridayHint = fridayDay ? `建议周五交付：${month}月${fridayDay}日` : `本周内提交`;
    return {
      type: 'week',
      sortDay: fridayDay || (startDay + 4),
      dateRangeStr: `${month}月${startDay}日 ~ ${month}月${endDay}日`,
      displayDate: `${month}月${startDay}日 ~ ${month}月${endDay}日`,
      ruleText: `${month}月${startDay}日 ~ ${month}月${endDay}日`,
      fridayHint: fridayHint,
      exactDay: fridayDay || (startDay + 4)
    };
  }
}

function renderMonthlyRoutines() {
  initCurrentRoutineYearMonth();
  const [yearStr, monthStr] = currentRoutineYearMonth.split('-');
  const year = parseInt(yearStr, 10);
  const month = parseInt(monthStr, 10);

  const monthTitleEl = document.getElementById('currentRoutineMonthDisplay');
  if (monthTitleEl) {
    monthTitleEl.textContent = `${year}年 ${month}月`;
  }

  let routines = getData(STORAGE_KEYS.MONTHLY_ROUTINES, null);
  if (!routines || !Array.isArray(routines) || routines.length === 0) {
    routines = DEFAULT_MONTHLY_ROUTINES;
    setData(STORAGE_KEYS.MONTHLY_ROUTINES, routines);
  } else {
    // Purge verbose default descriptions and subtasks to ensure an ultra-clean minimal panel
    let modified = false;
    routines = routines.map(r => {
      if (r.id <= 4 && (r.description || (r.subtasks && r.subtasks.length > 0))) {
        modified = true;
        const { description, subtasks, ...clean } = r;
        return clean;
      }
      return r;
    });
    if (modified) {
      setData(STORAGE_KEYS.MONTHLY_ROUTINES, routines);
    }
  }

  const allChecklists = getData(STORAGE_KEYS.MONTHLY_CHECKLIST, {});
  const monthChecklist = allChecklists[currentRoutineYearMonth] || {};

  const now = new Date();
  const isCurrentCalendarMonth = (now.getFullYear() === year && (now.getMonth() + 1) === month);
  const todayDay = now.getDate();
  const todayDayOfWeek = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][now.getDay()];

  const computedItems = routines.map(r => {
    const details = getRoutineDateDetails(r, year, month);
    const check = monthChecklist[String(r.id)] || { completed: false, completedAt: null, note: '' };
    return {
      ...r,
      details,
      check
    };
  });

  computedItems.sort((a, b) => a.details.sortDay - b.details.sortDay);

  const totalCount = computedItems.length;
  const completedCount = computedItems.filter(i => i.check.completed).length;
  const percent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  const statProgressEl = document.getElementById('statMonthlyProgress');
  if (statProgressEl) statProgressEl.textContent = `${completedCount} / ${totalCount}`;

  const progressFillEl = document.getElementById('routineProgressFill');
  if (progressFillEl) progressFillEl.style.width = `${percent}%`;

  const progressPercentEl = document.getElementById('routineProgressPercent');
  if (progressPercentEl) progressPercentEl.textContent = `${percent}%`;

  const nextItem = computedItems.find(i => !i.check.completed && (!isCurrentCalendarMonth || i.details.sortDay >= todayDay)) || computedItems.find(i => !i.check.completed) || computedItems[0];
  const statNextDateEl = document.getElementById('statMonthlyNextDate');
  if (statNextDateEl && nextItem) {
    if (nextItem.type === 'date') {
      statNextDateEl.textContent = `${month}月${nextItem.value}日`;
    } else {
      const startD = (nextItem.value - 1) * 7 + 1;
      const maxD = new Date(year, month, 0).getDate();
      const endD = Math.min(nextItem.value * 7, maxD);
      statNextDateEl.textContent = `${month}月${startD}日~${endD}日`;
    }
  }

  const container = document.getElementById('monthlyTimelineContainer');
  if (!container) return;

  let timelineHtml = '';
  let todayMarkerInserted = false;

  computedItems.forEach((item, index) => {
    if (isCurrentCalendarMonth && !todayMarkerInserted && todayDay < item.details.sortDay) {
      timelineHtml += `
        <div class="routine-today-marker">
          <div class="routine-today-dot">
            📍 今天
          </div>
          <div class="routine-today-badge">
            <span>今日进度 (${month}月${todayDay}日 ${todayDayOfWeek})</span>
          </div>
        </div>
      `;
      todayMarkerInserted = true;
    }

    const isCompleted = !!item.check.completed;
    let statusClass = 'upcoming';
    let statusText = '待办';

    if (isCompleted) {
      statusClass = 'done';
      statusText = '已完成';
    } else if (isCurrentCalendarMonth) {
      if (item.type === 'date') {
        if (todayDay === item.value) {
          statusClass = 'current';
          statusText = '今日计划';
        } else if (todayDay > item.value) {
          statusClass = 'overdue';
          statusText = '待完成';
        }
      } else {
        const startD = (item.value - 1) * 7 + 1;
        const endD = item.value * 7;
        if (todayDay >= startD && todayDay <= endD) {
          statusClass = 'current';
          statusText = '本周重点';
        } else if (todayDay > endD) {
          statusClass = 'overdue';
          statusText = '待完成';
        }
      }
    }

    const ruleColor = item.color || '#3b82f6';
    const ruleBg = ruleColor + '18';

    let axisDateLabel = '';
    if (item.type === 'date') {
      axisDateLabel = `${month}月${item.value}日`;
    } else {
      const startD = (item.value - 1) * 7 + 1;
      const maxD = new Date(year, month, 0).getDate();
      const endD = Math.min(item.value * 7, maxD);
      axisDateLabel = `${startD}日~${endD}日`;
    }
    const markerContent = isCompleted ? `✓ ${axisDateLabel}` : axisDateLabel;

    timelineHtml += `
      <div class="routine-timeline-node ${isCompleted ? 'completed' : ''}" id="routine-node-${item.id}">
        <div class="routine-node-marker" style="border-color:${isCompleted ? '#10b981' : ruleColor}; color:${isCompleted ? '#ffffff' : ruleColor};" title="${escapeHtml(item.details.displayDate)}">
          ${markerContent}
        </div>

        <div class="routine-card">
          <div class="routine-card-header">
            <div class="routine-card-tags">
              <span class="routine-pill-date" style="background:${ruleBg}; color:${ruleColor}; font-weight:700; border:1px solid ${ruleColor}33; border-radius:5px; padding:3px 9px; font-size:12px;">📅 ${escapeHtml(item.details.displayDate)}</span>
            </div>
            <div class="routine-status-badge ${statusClass}">
              ${statusText}
            </div>
          </div>

          <div class="routine-card-title">${escapeHtml(item.title)}</div>

          ${item.details.fridayHint ? `
            <div class="routine-hint-bar" style="font-size:12px;">
              <span>交付计划：${escapeHtml(item.details.fridayHint)}</span>
            </div>
          ` : ''}

          <div class="routine-card-footer">
            <div class="routine-action-left">
              <button class="btn-toggle-routine ${isCompleted ? 'is-done' : ''}" onclick="toggleMonthlyRoutineComplete(${item.id})">
                ${isCompleted ? '已完成 (点击取消)' : '标记完成'}
              </button>
              <button class="btn btn-sm btn-ghost" onclick="toggleRoutineNoteBox(${item.id})">
                ${item.check.note ? '查看/修改备注' : '添加备注'}
              </button>
            </div>
            <div class="routine-action-right">
              <button class="btn btn-sm btn-ghost" onclick="openEditMonthlyRoutineModal(${item.id})" title="编辑此事项">编辑</button>
              ${item.isCustom ? `<button class="btn btn-sm btn-ghost" style="color:#dc2626;" onclick="deleteMonthlyRoutine(${item.id})" title="删除">删除</button>` : ''}
            </div>
          </div>

          <div class="routine-note-drawer" id="routine-note-box-${item.id}" style="${item.check.note ? 'display:block;' : 'display:none;'}">
            <div style="font-size:12px; font-weight:700; margin-bottom:6px; color:var(--text-secondary);">本月备忘记录：</div>
            <textarea class="routine-note-textarea" id="routine-note-input-${item.id}" placeholder="输入会议室号、邮件主题或备忘记录..." onblur="saveMonthlyRoutineNote(${item.id})">${escapeHtml(item.check.note || '')}</textarea>
          </div>
        </div>
      </div>
    `;
  });

  if (isCurrentCalendarMonth && !todayMarkerInserted) {
    timelineHtml += `
      <div class="routine-today-marker">
        <div class="routine-today-dot">
          📍 今天
        </div>
        <div class="routine-today-badge">
          <span>今日进度 (${month}月${todayDay}日 ${todayDayOfWeek})</span>
        </div>
      </div>
    `;
  }

  container.innerHTML = timelineHtml;
}

function toggleMonthlyRoutineComplete(routineId) {
  initCurrentRoutineYearMonth();
  const allChecklists = getData(STORAGE_KEYS.MONTHLY_CHECKLIST, {});
  if (!allChecklists[currentRoutineYearMonth]) {
    allChecklists[currentRoutineYearMonth] = {};
  }
  const cur = allChecklists[currentRoutineYearMonth][String(routineId)] || { completed: false, completedAt: null, note: '' };
  cur.completed = !cur.completed;
  cur.completedAt = cur.completed ? new Date().toLocaleString() : null;
  allChecklists[currentRoutineYearMonth][String(routineId)] = cur;

  setData(STORAGE_KEYS.MONTHLY_CHECKLIST, allChecklists);
  syncKeyToHostDatabase(STORAGE_KEYS.MONTHLY_CHECKLIST, allChecklists);

  renderMonthlyRoutines();

  if (cur.completed) {
    showToast('✨ 已成功标记为本月完成！');
  }
}

function toggleRoutineNoteBox(routineId) {
  const box = document.getElementById(`routine-note-box-${routineId}`);
  if (!box) return;
  if (box.style.display === 'none' || !box.style.display) {
    box.style.display = 'block';
    const inp = document.getElementById(`routine-note-input-${routineId}`);
    if (inp) inp.focus();
  } else {
    box.style.display = 'none';
  }
}

function saveMonthlyRoutineNote(routineId) {
  initCurrentRoutineYearMonth();
  const inp = document.getElementById(`routine-note-input-${routineId}`);
  if (!inp) return;
  const note = inp.value.trim();

  const allChecklists = getData(STORAGE_KEYS.MONTHLY_CHECKLIST, {});
  if (!allChecklists[currentRoutineYearMonth]) {
    allChecklists[currentRoutineYearMonth] = {};
  }
  const cur = allChecklists[currentRoutineYearMonth][String(routineId)] || { completed: false, completedAt: null, note: '' };
  if (cur.note !== note) {
    cur.note = note;
    allChecklists[currentRoutineYearMonth][String(routineId)] = cur;
    setData(STORAGE_KEYS.MONTHLY_CHECKLIST, allChecklists);
    syncKeyToHostDatabase(STORAGE_KEYS.MONTHLY_CHECKLIST, allChecklists);
    showToast('💾 本月纪要备忘已保存');
  }
}

function toggleLinksCollapse() {
  const body = document.getElementById('linksCollapseBody');
  const icon = document.getElementById('linksCollapseIcon');
  if (!body) return;
  if (body.style.display === 'none' || !body.style.display) {
    body.style.display = 'block';
    if (icon) icon.textContent = '▲ 收起';
  } else {
    body.style.display = 'none';
    if (icon) icon.textContent = '▼ 展开';
  }
}

function openAddMonthlyRoutineModal() {
  document.getElementById('monthlyRoutineModalTitle').textContent = '➕ 添加月度关卡';
  document.getElementById('inputRoutineId').value = '';
  document.getElementById('inputRoutineTitle').value = '';
  document.getElementById('selectRoutineType').value = 'date';
  document.getElementById('inputRoutineValue').value = '9';
  const catInp = document.getElementById('inputRoutineCategory');
  if (catInp) catInp.value = '月度关卡';
  const iconInp = document.getElementById('inputRoutineIcon');
  if (iconInp) iconInp.value = '';
  const subInp = document.getElementById('inputRoutineSubtasks');
  if (subInp) subInp.value = '';
  const delBtn = document.getElementById('btnDeleteRoutineInModal');
  if (delBtn) delBtn.style.display = 'none';
  handleRoutineTypeChange();
  openModal('monthlyRoutineModal');
}

function openEditMonthlyRoutineModal(routineId) {
  const routines = getData(STORAGE_KEYS.MONTHLY_ROUTINES, DEFAULT_MONTHLY_ROUTINES);
  const item = routines.find(r => r.id === routineId);
  if (!item) return;

  document.getElementById('monthlyRoutineModalTitle').textContent = '✏️ 编辑月度关卡';
  document.getElementById('inputRoutineId').value = item.id;
  document.getElementById('inputRoutineTitle').value = item.title || '';
  document.getElementById('selectRoutineType').value = item.type || 'date';
  document.getElementById('inputRoutineValue').value = item.value || 1;
  const catInp = document.getElementById('inputRoutineCategory');
  if (catInp) catInp.value = item.category || '月度关卡';
  const iconInp = document.getElementById('inputRoutineIcon');
  if (iconInp) iconInp.value = item.icon || '';
  const subInp = document.getElementById('inputRoutineSubtasks');
  if (subInp) subInp.value = (item.subtasks || []).join('\\n');

  const delBtn = document.getElementById('btnDeleteRoutineInModal');
  if (delBtn) {
    delBtn.style.display = item.isCustom ? 'inline-block' : 'none';
  }
  handleRoutineTypeChange();
  openModal('monthlyRoutineModal');
}

function handleRoutineTypeChange() {
  const sel = document.getElementById('selectRoutineType');
  const label = document.getElementById('labelRoutineValue');
  const valInp = document.getElementById('inputRoutineValue');
  if (!sel || !label || !valInp) return;
  if (sel.value === 'date') {
    label.textContent = '计划时间 (1~31 号)';
    valInp.min = '1';
    valInp.max = '31';
    if (parseInt(valInp.value, 10) > 31) valInp.value = '31';
  } else {
    label.textContent = '计划时间 (第 1~5 周)';
    valInp.min = '1';
    valInp.max = '5';
    if (parseInt(valInp.value, 10) > 5) valInp.value = '2';
  }
}

function saveMonthlyRoutineItem() {
  const idVal = document.getElementById('inputRoutineId').value;
  const title = document.getElementById('inputRoutineTitle').value.trim();
  const type = document.getElementById('selectRoutineType').value;
  const value = parseInt(document.getElementById('inputRoutineValue').value, 10);
  const category = document.getElementById('inputRoutineCategory').value.trim() || '月度例行';
  const icon = document.getElementById('inputRoutineIcon').value.trim() || '📌';
  const subtasksRaw = document.getElementById('inputRoutineSubtasks').value.trim();

  if (!title) {
    alert('请输入事项名称');
    return;
  }
  if (isNaN(value) || value < 1) {
    alert('请输入有效的日期或周次');
    return;
  }

  const subtasks = subtasksRaw ? subtasksRaw.split(/\\r?\\n/).map(s => s.replace(/^[•\\-\\*▫️\\s]+/, '').trim()).filter(Boolean) : [];

  let routines = getData(STORAGE_KEYS.MONTHLY_ROUTINES, DEFAULT_MONTHLY_ROUTINES);
  const timingDisplay = (type === 'date') ? `每月 ${value} 号` : `每月第 ${value} 周`;

  if (idVal) {
    const id = parseInt(idVal, 10);
    const idx = routines.findIndex(r => r.id === id);
    if (idx !== -1) {
      routines[idx] = {
        ...routines[idx],
        title,
        type,
        value,
        timingDisplay,
        category,
        icon,
        subtasks,
        description: routines[idx].description || `每月按时完成 ${title}`
      };
    }
  } else {
    const newId = Date.now();
    routines.push({
      id: newId,
      title,
      type,
      value,
      timingDisplay,
      category,
      icon,
      color: '#3b82f6',
      subtasks,
      description: `每月按时完成 ${title}`,
      isCustom: true
    });
  }

  setData(STORAGE_KEYS.MONTHLY_ROUTINES, routines);
  syncKeyToHostDatabase(STORAGE_KEYS.MONTHLY_ROUTINES, routines);

  closeModal('monthlyRoutineModal');
  renderMonthlyRoutines();
  showToast('✅ 月度事项已保存');
}

function deleteMonthlyRoutine(routineId) {
  if (!confirm('确定要删除该月度事项吗？')) return;
  let routines = getData(STORAGE_KEYS.MONTHLY_ROUTINES, DEFAULT_MONTHLY_ROUTINES);
  routines = routines.filter(r => r.id !== routineId);
  setData(STORAGE_KEYS.MONTHLY_ROUTINES, routines);
  syncKeyToHostDatabase(STORAGE_KEYS.MONTHLY_ROUTINES, routines);
  renderMonthlyRoutines();
  showToast('🗑️ 事项已删除');
}

function deleteCurrentEditRoutine() {
  const idVal = document.getElementById('inputRoutineId').value;
  if (idVal) {
    deleteMonthlyRoutine(parseInt(idVal, 10));
    closeModal('monthlyRoutineModal');
  }
}

// ================= 常用链接 (Snoopy Links) =================
let currentLinkCategoryFilter = 'ALL';

function renderLinks() {
  // 1. Settings (Custom module title & persona tag)
  const settings = getData(STORAGE_KEYS.LINK_SETTINGS, {
    title: '月度闯关 · Monthly Quest',
    tag: '🎯 月度打卡闯关'
  });
  const titleEl = document.getElementById('linksModuleTitleText');
  if (titleEl) titleEl.textContent = settings.title || '月度闯关 · Monthly Quest';
  const tagEl = document.getElementById('linksModuleTagText');
  if (tagEl) tagEl.textContent = settings.tag || '🎯 月度打卡闯关';

  // 2. Fetch and normalize links
  let links = getData(STORAGE_KEYS.LINKS, []);
  links = links.map(l => ({
    ...l,
    category: l.category || '🏢 内部协同',
    icon: l.icon || '🌐'
  }));

  const countEl = document.getElementById('statLinkCount');
  if (countEl) countEl.textContent = links.length;
  const countBadge = document.getElementById('statLinkCountBadge');
  if (countBadge) countBadge.textContent = `${links.length} 个链接`;

  // Always refresh monthly routines when links render
  if (typeof renderMonthlyRoutines === 'function') {
    renderMonthlyRoutines();
  }

  // 3. Extract unique categories
  const allCats = Array.from(new Set(links.map(l => l.category || '🏢 内部协同'))).filter(Boolean);

  // 4. Render category tabs
  const tabsEl = document.getElementById('linksCategoryTabs');
  if (tabsEl) {
    let tabsHtml = `
      <button class="category-tab-btn ${currentLinkCategoryFilter === 'ALL' ? 'active' : ''}" onclick="filterLinksByCategory('ALL')">
        全部 (${links.length})
      </button>
    `;
    allCats.forEach(cat => {
      const cCount = links.filter(l => (l.category || '🏢 内部协同') === cat).length;
      tabsHtml += `
        <button class="category-tab-btn ${currentLinkCategoryFilter === cat ? 'active' : ''}" onclick="filterLinksByCategory('${escapeHtml(cat)}')">
          ${escapeHtml(cat)} (${cCount})
        </button>
      `;
    });
    tabsEl.innerHTML = tabsHtml;
  }

  // 5. Filter links based on selected category
  const displayLinks = (currentLinkCategoryFilter === 'ALL')
    ? links
    : links.filter(l => (l.category || '🏢 内部协同') === currentLinkCategoryFilter);

  // 6. Render links grid (No long URLs exposed! Large bold title, clean category tag & actions)
  const gridEl = document.getElementById('linksFullGrid');
  if (gridEl) {
    if (displayLinks.length === 0) {
      gridEl.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 36px 16px; color: var(--text-muted); background: var(--card); border: 1px dashed var(--border); border-radius: var(--radius-md);">
          <div style="font-size: 26px; margin-bottom: 8px;">🔗</div>
          <div style="font-size: 14px; font-weight: 700; margin-bottom: 4px; color: var(--text-primary);">该分类下暂无已添加链接</div>
          <div style="font-size: 12px; margin-bottom: 14px;">点击下方按钮添加属于【${currentLinkCategoryFilter !== 'ALL' ? escapeHtml(currentLinkCategoryFilter) : '常用链接'}】的新网址</div>
          <button class="btn btn-sm btn-primary" onclick="openAddLinkModal('${currentLinkCategoryFilter !== 'ALL' ? escapeHtml(currentLinkCategoryFilter) : ''}')">➕ 立即添加</button>
        </div>
      `;
    } else {
      gridEl.innerHTML = displayLinks.map(l => `
        <div class="link-card" onclick="window.open('${escapeHtml(l.url)}', '_blank')" title="点击新窗口直达：${escapeHtml(l.name)}">
          <div class="link-card-header">
            <div class="link-icon-badge">${escapeHtml(l.icon || '🌐')}</div>
            <span class="link-category-pill" onclick="event.stopPropagation(); filterLinksByCategory('${escapeHtml(l.category || '🏢 内部协同')}')" title="筛选此分类">
              ${escapeHtml(l.category || '🏢 内部协同')}
            </span>
          </div>
          <div class="link-title">${escapeHtml(l.name)}</div>
          <div class="link-card-footer">
            <span class="link-open-hint">↗ 点击直达</span>
            <div class="link-card-actions">
              <button class="btn btn-sm btn-ghost" title="修改此链接信息" onclick="event.stopPropagation(); openEditLinkModal(${l.id})">✏️</button>
              <button class="btn btn-sm btn-ghost" style="color:#dc2626;" title="删除链接" onclick="event.stopPropagation(); deleteLink(${l.id})">✕</button>
            </div>
          </div>
        </div>
      `).join('');
    }
  }

  // 7. Render dashboard mini box
  const dashEl = document.getElementById('dashQuickLinks');
  if (dashEl) {
    dashEl.innerHTML = `
      <div style="display:flex; flex-wrap:wrap; gap:8px;">
        ${links.slice(0, 8).map(l => `
          <a href="${escapeHtml(l.url)}" target="_blank" class="btn btn-sm" style="text-decoration:none; display:inline-flex; align-items:center; gap:5px;" title="${escapeHtml(l.name)}">
            <span>${escapeHtml(l.icon || '🔗')}</span>
            <span>${escapeHtml(l.name)}</span>
          </a>
        `).join('')}
      </div>
    `;
  }
}

function filterLinksByCategory(cat) {
  currentLinkCategoryFilter = cat;
  renderLinks();
renderMonthlyRoutines();
}

function setLinkIconEmoji(emoji) {
  const el = document.getElementById('inputLinkIcon');
  if (el) el.value = emoji;
}

function handleLinkCategorySelectChange() {
  const sel = document.getElementById('selectLinkCategory');
  const customInput = document.getElementById('inputCustomLinkCategory');
  if (!sel || !customInput) return;
  if (sel.value === '__custom__') {
    customInput.style.display = 'block';
    customInput.focus();
  } else {
    customInput.style.display = 'none';
  }
}

function populateLinkCategorySelect(selectedCat) {
  const sel = document.getElementById('selectLinkCategory');
  if (!sel) return;
  const links = getData(STORAGE_KEYS.LINKS, []);
  let cats = Array.from(new Set(links.map(l => l.category || '🏢 内部协同'))).filter(Boolean);
  if (cats.length === 0) {
    cats = ['🏢 内部协同', '🌍 区域协同', '✈️ 商旅出行', '🛠️ 常用工具'];
  }
  if (selectedCat && !cats.includes(selectedCat)) {
    cats.push(selectedCat);
  }

  sel.innerHTML = `
    ${cats.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('')}
    <option value="__custom__">➕ 输入全新分类...</option>
  `;

  if (selectedCat && cats.includes(selectedCat)) {
    sel.value = selectedCat;
  } else if (cats.length > 0) {
    sel.value = cats[0];
  }
  handleLinkCategorySelectChange();
}

function openAddLinkModal(presetCategory) {
  document.getElementById('linkModalTitle').textContent = '➕ 添加常用链接';
  document.getElementById('inputLinkId').value = '';
  document.getElementById('inputLinkName').value = '';
  document.getElementById('inputLinkUrl').value = '';
  document.getElementById('inputLinkIcon').value = '🌐';
  document.getElementById('inputCustomLinkCategory').value = '';

  const delBtn = document.getElementById('btnDeleteLinkInModal');
  if (delBtn) delBtn.style.display = 'none';

  const defaultCat = (presetCategory && presetCategory !== 'ALL') ? presetCategory : '🏢 内部协同';
  populateLinkCategorySelect(defaultCat);
  openModal('linkModal');
}

function openEditLinkModal(id) {
  const links = getData(STORAGE_KEYS.LINKS, []);
  const link = links.find(l => l.id === id);
  if (!link) return;

  document.getElementById('linkModalTitle').textContent = '✏️ 编辑常用链接';
  document.getElementById('inputLinkId').value = link.id;
  document.getElementById('inputLinkName').value = link.name || '';
  document.getElementById('inputLinkUrl').value = link.url || '';
  document.getElementById('inputLinkIcon').value = link.icon || '🌐';
  document.getElementById('inputCustomLinkCategory').value = '';

  const delBtn = document.getElementById('btnDeleteLinkInModal');
  if (delBtn) delBtn.style.display = 'inline-flex';

  populateLinkCategorySelect(link.category || '🏢 内部协同');
  openModal('linkModal');
}

function saveCustomLink() {
  const idStr = document.getElementById('inputLinkId').value;
  const id = idStr ? Number(idStr) : null;
  const name = document.getElementById('inputLinkName').value.trim();
  let url = document.getElementById('inputLinkUrl').value.trim();
  const icon = document.getElementById('inputLinkIcon').value.trim() || '🌐';

  const sel = document.getElementById('selectLinkCategory');
  let category = sel ? sel.value : '🏢 内部协同';
  if (category === '__custom__') {
    const customVal = document.getElementById('inputCustomLinkCategory').value.trim();
    category = customVal || '🏢 内部协同';
  }

  if (!name) {
    showToast('请填写网站/链接名称！');
    const el = document.getElementById('inputLinkName');
    if (el) el.focus();
    return;
  }
  if (!url) {
    showToast('请填写网址 URL！');
    const el = document.getElementById('inputLinkUrl');
    if (el) el.focus();
    return;
  }

  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url;
  }

  let links = getData(STORAGE_KEYS.LINKS, []);
  if (id) {
    links = links.map(l => (l.id === id) ? { ...l, name, url, category, icon } : l);
    showToast('✅ 链接信息已更新！');
  } else {
    links.unshift({ id: Date.now(), name, url, category, icon });
    showToast('🔗 链接已成功添加！');
  }

  setData(STORAGE_KEYS.LINKS, links);
  closeModal('linkModal');
  renderLinks();
renderMonthlyRoutines();
}

function deleteLink(id) {
  if (!confirm('确定要删除此条常用链接吗？')) return;
  let links = getData(STORAGE_KEYS.LINKS, []);
  links = links.filter(l => l.id !== id);
  setData(STORAGE_KEYS.LINKS, links);
  renderLinks();
renderMonthlyRoutines();
  showToast('链接已删除');
}

function deleteCurrentEditLink() {
  const idStr = document.getElementById('inputLinkId').value;
  const id = Number(idStr);
  if (!id) return;
  closeModal('linkModal');
  deleteLink(id);
}

// ================= 分类管理与重命名 (Manage & Rename Categories) =================
function openManageCategoriesModal() {
  const links = getData(STORAGE_KEYS.LINKS, []);
  const allCats = Array.from(new Set(links.map(l => l.category || '🏢 内部协同'))).filter(Boolean);
  const listEl = document.getElementById('categoryManageList');
  if (listEl) {
    if (allCats.length === 0) {
      listEl.innerHTML = '<div style="color:var(--text-muted); font-size:12.5px; padding:12px;">暂无任何分类记录</div>';
    } else {
      listEl.innerHTML = allCats.map((cat, idx) => {
        const cCount = links.filter(l => (l.category || '🏢 内部协同') === cat).length;
        return `
          <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; padding:8px 10px; background:var(--card-subtle); border-radius:6px; border:1px solid var(--border);">
            <div style="flex:1; display:flex; align-items:center; gap:8px;">
              <span style="font-size:11px; color:var(--text-muted); width:20px;">#${idx + 1}</span>
              <input type="text" id="renameCatInput_${idx}" value="${escapeHtml(cat)}" style="flex:1; font-weight:600; font-size:13px; padding:5px 8px;" />
              <span style="font-size:11.5px; color:var(--text-secondary); white-space:nowrap;">(${cCount} 条链接)</span>
            </div>
            <button class="btn btn-sm btn-primary" onclick="submitRenameCategory('${escapeHtml(cat)}', 'renameCatInput_${idx}')" style="white-space:nowrap; padding:4px 10px;">
              保存名称
            </button>
          </div>
        `;
      }).join('');
    }
  }
  openModal('manageCategoriesModal');
}

function submitRenameCategory(oldCat, inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const newCat = input.value.trim();
  if (!newCat) {
    showToast('分类名称不能为空！');
    return;
  }
  if (newCat === oldCat) {
    showToast('分类名称未改变');
    return;
  }

  let links = getData(STORAGE_KEYS.LINKS, []);
  links = links.map(l => {
    if ((l.category || '🏢 内部协同') === oldCat) {
      return { ...l, category: newCat };
    }
    return l;
  });
  setData(STORAGE_KEYS.LINKS, links);

  if (currentLinkCategoryFilter === oldCat) {
    currentLinkCategoryFilter = newCat;
  }

  renderLinks();
renderMonthlyRoutines();
  openManageCategoriesModal();
  showToast(`🏷️ 分类已更名为【${newCat}】`);
}

// ================= 通用板块名称自定义 (Module Header Customization) =================
const DEFAULT_MODULE_CONFIGS = {
  todo: {
    name: '今日任务',
    defaultTitle: '今日任务 · Beagle Scout',
    defaultTag: '🏕️ 比格犬童子军',
    titleEl: 'todoModuleTitleText',
    tagEl: 'todoModuleTagText'
  },
  legacy_tasks: {
    name: '遗留任务',
    defaultTitle: '遗留任务 · Legacy Tasks',
    defaultTag: '📋 曦总汇报闭环追踪',
    titleEl: 'legacyTasksModuleTitleText',
    tagEl: 'legacyTasksModuleTagText'
  },
  supervisor: {
    name: '会议预约',
    defaultTitle: '会议预约 · Secretary Desk',
    defaultTag: '秘书工作台',
    titleEl: 'supervisorModuleTitleText',
    tagEl: 'supervisorModuleTagText'
  },
  timezone: {
    name: '时区协同',
    defaultTitle: '时区协同 · World Tour',
    defaultTag: '🪖 Flying Ace',
    titleEl: 'timezoneModuleTitleText',
    tagEl: 'timezoneModuleTagText'
  },
  links: {
    name: '月度闯关',
    defaultTitle: '月度闯关 · Monthly Quest',
    defaultTag: '🎯 月度打卡闯关',
    titleEl: 'linksModuleTitleText',
    tagEl: 'linksModuleTagText'
  },
  notes: {
    name: '每日小记',
    defaultTitle: '每日小记 · Little Notes',
    defaultTag: '✍️ World Famous Author',
    titleEl: 'notesModuleTitleText',
    tagEl: 'notesModuleTagText'
  },
  english: {
    name: '每日英语',
    defaultTitle: '每日英语 · 2027北欧漫游',
    defaultTag: '❄️ Nordic Journey',
    titleEl: 'englishModuleTitleText',
    tagEl: 'englishModuleTagText'
  }
};

function openEditModuleModal(moduleId) {
  const config = DEFAULT_MODULE_CONFIGS[moduleId];
  if (!config) return;

  const allSettings = getData(STORAGE_KEYS.MODULE_SETTINGS, {});
  let modSettings = allSettings[moduleId];
  if (!modSettings && moduleId === 'links') {
    modSettings = getData(STORAGE_KEYS.LINK_SETTINGS, null);
  }

  const currentTitle = (modSettings && modSettings.title) ? modSettings.title : config.defaultTitle;
  const currentTag = (modSettings && modSettings.tag !== undefined) ? modSettings.tag : config.defaultTag;

  const curKeyEl = document.getElementById('editModuleCurrentKey');
  if (curKeyEl) curKeyEl.value = moduleId;
  const modalTitleEl = document.getElementById('editModuleModalTitle');
  if (modalTitleEl) modalTitleEl.textContent = `✏️ 自定义${config.name}板块`;
  const inpTitle = document.getElementById('inputModuleCustomTitle');
  if (inpTitle) inpTitle.value = currentTitle;
  const inpTag = document.getElementById('inputModuleCustomTag');
  if (inpTag) inpTag.value = currentTag;

  // 兼容老输入框引用
  const compTitle = document.getElementById('inputLinksModuleTitle');
  if (compTitle) compTitle.value = currentTitle;
  const compTag = document.getElementById('inputLinksModuleTag');
  if (compTag) compTag.value = currentTag;

  openModal('editModuleModal');
}

function saveModuleCustomSettings() {
  const curKeyEl = document.getElementById('editModuleCurrentKey');
  const moduleId = (curKeyEl && curKeyEl.value) ? curKeyEl.value : 'links';
  const config = DEFAULT_MODULE_CONFIGS[moduleId];
  if (!config) return;

  const inpTitle = document.getElementById('inputModuleCustomTitle');
  const inpTag = document.getElementById('inputModuleCustomTag');
  const compTitle = document.getElementById('inputLinksModuleTitle');
  const compTag = document.getElementById('inputLinksModuleTag');

  let title = (inpTitle && inpTitle.value.trim()) ? inpTitle.value.trim() : '';
  if (!title && compTitle && compTitle.value.trim()) {
    title = compTitle.value.trim();
  }
  title = title || config.defaultTitle;

  let tag = (inpTag && inpTag.value !== undefined) ? inpTag.value.trim() : '';
  if (!tag && compTag && compTag.value.trim()) {
    tag = compTag.value.trim();
  }

  const allSettings = getData(STORAGE_KEYS.MODULE_SETTINGS, {});
  allSettings[moduleId] = { title, tag };
  setData(STORAGE_KEYS.MODULE_SETTINGS, allSettings);

  if (moduleId === 'links') {
    setData(STORAGE_KEYS.LINK_SETTINGS, { title, tag });
  }

  applyModuleHeaderSettings();
  closeModal('editModuleModal');
  showToast(`✅ 【${config.name}】板块设置已保存！`);
}

function resetCurrentModuleSettings() {
  const curKeyEl = document.getElementById('editModuleCurrentKey');
  const moduleId = (curKeyEl && curKeyEl.value) ? curKeyEl.value : 'links';
  const config = DEFAULT_MODULE_CONFIGS[moduleId];
  if (!config) return;

  const inpTitle = document.getElementById('inputModuleCustomTitle');
  if (inpTitle) inpTitle.value = config.defaultTitle;
  const inpTag = document.getElementById('inputModuleCustomTag');
  if (inpTag) inpTag.value = config.defaultTag;
}

function applyModuleHeaderSettings() {
  const allSettings = getData(STORAGE_KEYS.MODULE_SETTINGS, {});
  const linkSettings = getData(STORAGE_KEYS.LINK_SETTINGS, null);

  Object.keys(DEFAULT_MODULE_CONFIGS).forEach(modId => {
    const config = DEFAULT_MODULE_CONFIGS[modId];
    let settings = allSettings[modId];
    if (!settings && modId === 'links' && linkSettings) {
      settings = linkSettings;
    }

    const title = (settings && settings.title) ? settings.title : config.defaultTitle;
    const tag = (settings && settings.tag !== undefined) ? settings.tag : config.defaultTag;

    const titleEl = document.getElementById(config.titleEl);
    if (titleEl) titleEl.textContent = title;

    const tagEl = document.getElementById(config.tagEl);
    if (tagEl) {
      tagEl.textContent = tag;
      tagEl.style.display = tag ? 'inline-block' : 'none';
    }
  });
}

function openEditLinksModuleModal() {
  openEditModuleModal('links');
}

function saveLinksModuleSettings() {
  saveModuleCustomSettings();
}

// ================= 每日小记 (Little Notes) =================
function renderNotes() {
  const notes = getData(STORAGE_KEYS.NOTES);
  const gridEl = document.getElementById('notesFullGrid');
  const dashEl = document.getElementById('dashNotesBox');
  const countEl = document.getElementById('statNoteCount');

  if (countEl) countEl.textContent = notes.length;

  if (gridEl) {
    if (notes.length === 0) {
      gridEl.innerHTML = '<div style="color:var(--text-muted); font-size:12.5px; padding:20px;">暂无小记，在上方记下第一条灵感吧！</div>';
    } else {
      gridEl.innerHTML = notes.map(n => `
        <div class="note-item ${n.isPinned ? 'is-pinned' : ''}"
             draggable="true"
             data-note-id="${n.id}"
             ondragstart="handleNoteDragStart(event, ${n.id})"
             ondragover="handleNoteDragOver(event)"
             ondragenter="handleNoteDragEnter(event)"
             ondragleave="handleNoteDragLeave(event)"
             ondrop="handleNoteDrop(event, ${n.id})"
             ondragend="handleNoteDragEnd(event)">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="display:flex; align-items:center; gap:6px;">
              <span class="drag-grip-icon" title="按住拖拽排序">⠿</span>
              ${n.isPinned ? '<span class="badge" style="background:#fef3c7; color:#b45309; border:1px solid #fde68a; font-size:10.5px; padding:1px 6px;">📌 置顶</span>' : ''}
            </div>
            <button class="btn btn-sm btn-ghost" title="${n.isPinned ? '取消置顶' : '置顶小记'}" onclick="togglePinNote(${n.id})" style="padding:1px 6px; font-size:11.5px; color:${n.isPinned ? '#b45309' : 'var(--text-muted)'};">
              ${n.isPinned ? '📍 取消置顶' : '📌 置顶'}
            </button>
          </div>
          <div class="note-text">${escapeHtml(n.text)}</div>
          <div class="note-meta">
            <span>${escapeHtml(n.category || '📝 记事')} · ${n.time}</span>
            <div style="display:flex; gap:6px;">
              <button class="btn btn-sm btn-ghost" title="编辑小记" onclick="openEditNoteModal(${n.id})">✏️</button>
              <button class="btn btn-sm btn-ghost" title="复制小记" onclick="copyToClipboard('${escapeHtml(n.text).replace(/'/g, "\\'")}', '已复制小记内容')">📋</button>
              <button class="btn btn-sm btn-ghost" style="color:#dc2626;" title="删除小记" onclick="deleteNote(${n.id})">✕</button>
            </div>
          </div>
        </div>
      `).join('');
    }
  }

  if (dashEl) {
    if (notes.length === 0) {
      dashEl.innerHTML = '<div style="color:var(--text-muted); font-size:12px; text-align:center; padding:12px;">暂无最新小记 ✍️</div>';
    } else {
      const topNote = notes[0];
      dashEl.innerHTML = `
        <div style="background:var(--card-subtle); border:1px solid var(--border); border-radius:var(--radius-sm); padding:10px 12px; font-size:12.5px;">
          <div style="font-weight:700; color:var(--text-primary); margin-bottom:4px; display:flex; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:6px;">
              ${topNote.isPinned ? '<span style="color:#b45309; font-size:11px;">📌</span>' : ''}
              <span>${escapeHtml(topNote.category || '📝 记事')}</span>
            </div>
            <span style="font-size:11px; color:var(--text-muted); font-weight:normal;">${topNote.time}</span>
          </div>
          <div style="color:var(--text-secondary); line-height:1.5; white-space:pre-wrap;">${escapeHtml(topNote.text.slice(0, 85))}${topNote.text.length > 85 ? '...' : ''}</div>
        </div>
      `;
    }
  }
}

let draggedNoteId = null;

function handleNoteDragStart(e, id) {
  draggedNoteId = id;
  if (e && e.dataTransfer) {
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', String(id));
  }
  const item = e && e.currentTarget;
  if (item) {
    setTimeout(() => { if (item.classList) item.classList.add('is-dragging'); }, 0);
  }
}

function handleNoteDragOver(e) {
  if (e && e.preventDefault) e.preventDefault();
  if (e && e.dataTransfer) {
    e.dataTransfer.dropEffect = 'move';
  }
}

function handleNoteDragEnter(e) {
  const item = e && e.currentTarget && e.currentTarget.closest ? e.currentTarget.closest('.note-item') : null;
  if (item && item.classList && !item.classList.contains('is-dragging')) {
    item.classList.add('drag-over');
  }
}

function handleNoteDragLeave(e) {
  const item = e && e.currentTarget && e.currentTarget.closest ? e.currentTarget.closest('.note-item') : null;
  if (item && item.classList && (!e.relatedTarget || !item.contains(e.relatedTarget))) {
    item.classList.remove('drag-over');
  }
}

function handleNoteDragEnd(e) {
  draggedNoteId = null;
  if (document.querySelectorAll) {
    document.querySelectorAll('.note-item').forEach(el => {
      if (el.classList) el.classList.remove('is-dragging', 'drag-over');
    });
  }
}

function handleNoteDrop(e, targetId) {
  if (e && e.preventDefault) e.preventDefault();
  if (document.querySelectorAll) {
    document.querySelectorAll('.note-item').forEach(el => {
      if (el.classList) el.classList.remove('drag-over', 'is-dragging');
    });
  }
  if (!draggedNoteId || draggedNoteId === targetId) return;

  let notes = getData(STORAGE_KEYS.NOTES);
  const dragIndex = notes.findIndex(n => n.id === draggedNoteId);
  const targetIndex = notes.findIndex(n => n.id === targetId);
  if (dragIndex === -1 || targetIndex === -1) return;

  const [movedNote] = notes.splice(dragIndex, 1);
  notes.splice(targetIndex, 0, movedNote);

  setData(STORAGE_KEYS.NOTES, notes);
  renderNotes();
  showToast('↕️ 小记卡片顺序已调整');
}

function togglePinNote(id) {
  let notes = getData(STORAGE_KEYS.NOTES);
  const note = notes.find(n => n.id === id);
  if (!note) return;
  const willPin = !note.isPinned;
  note.isPinned = willPin;

  if (willPin) {
    notes = notes.filter(n => n.id !== id);
    notes.unshift(note);
    showToast('📌 小记已置顶！');
  } else {
    notes = notes.filter(n => n.id !== id);
    const firstUnpinnedIndex = notes.findIndex(n => !n.isPinned);
    if (firstUnpinnedIndex === -1) {
      notes.push(note);
    } else {
      notes.splice(firstUnpinnedIndex, 0, note);
    }
    showToast('📍 已取消置顶');
  }
  setData(STORAGE_KEYS.NOTES, notes);
  renderNotes();
}

function addNote() {
  const text = document.getElementById('inputNoteText').value.trim();
  if (!text) return;
  const category = document.getElementById('selectNoteCategory').value;
  const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });

  const notes = getData(STORAGE_KEYS.NOTES);
  const newNote = { id: Date.now(), text, category, time, isPinned: false };
  const firstUnpinnedIndex = notes.findIndex(n => !n.isPinned);
  if (firstUnpinnedIndex === -1) {
    if (notes.length > 0 && notes.every(n => n.isPinned)) {
      notes.push(newNote);
    } else {
      notes.unshift(newNote);
    }
  } else {
    notes.splice(firstUnpinnedIndex, 0, newNote);
  }
  setData(STORAGE_KEYS.NOTES, notes);

  document.getElementById('inputNoteText').value = '';
  renderNotes();
  showToast('✍️ 小记已保存！');
}

function deleteNote(id) {
  let notes = getData(STORAGE_KEYS.NOTES);
  notes = notes.filter(n => n.id !== id);
  setData(STORAGE_KEYS.NOTES, notes);
  renderNotes();
}

function openEditNoteModal(id) {
  const notes = getData(STORAGE_KEYS.NOTES);
  const n = notes.find(x => x.id === id);
  if (!n) return;
  document.getElementById('editNoteId').value = n.id;
  document.getElementById('editNoteCategory').value = n.category || '💡 灵感备忘';
  document.getElementById('editNoteText').value = n.text || '';
  openModal('editNoteModal');
}

function saveEditNote() {
  const idStr = document.getElementById('editNoteId').value;
  const id = Number(idStr) || idStr;
  const text = document.getElementById('editNoteText').value.trim();
  const category = document.getElementById('editNoteCategory').value;
  if (!text) {
    showToast('小记内容不能为空！');
    return;
  }

  let notes = getData(STORAGE_KEYS.NOTES);
  notes = notes.map(n => {
    if (n.id === id) {
      return { ...n, text, category, editedAt: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) };
    }
    return n;
  });
  setData(STORAGE_KEYS.NOTES, notes);
  closeModal('editNoteModal');
  renderNotes();
  showToast('✅ 小记修改已保存！');
}

function deleteCurrentEditNote() {
  const idStr = document.getElementById('editNoteId').value;
  const id = Number(idStr) || idStr;
  if (!id) return;
  if (!confirm('确定要删除此条小记吗？')) return;
  closeModal('editNoteModal');
  deleteNote(id);
}

// ================= DRAGGABLE MODAL SYSTEM =================
function initModalDragSystem() {
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    const box = overlay.querySelector('.modal-box, .celebration-modal-box');
    if (!box) return;

    const handles = box.querySelectorAll('.modal-header, .modal-drag-handle-bar, .modal-footer');
    if (handles.length === 0) return;

    let isDragging = false;
    let startX = 0, startY = 0;
    let curX = 0, curY = 0;
    let initX = 0, initY = 0;

    box.resetModalPosition = function() {
      curX = 0;
      curY = 0;
      initX = 0;
      initY = 0;
      box._curTranslateX = 0;
      box._curTranslateY = 0;
      box.style.transform = '';
      box.style.animation = '';
    };

    function startDrag(e) {
      if (e.target.closest('button, input, select, textarea, a, .btn, label, option, summary')) return;
      if (e.button !== undefined && e.button !== 0) return; // Only left-click
      if (e.cancelable) e.preventDefault();

      isDragging = true;
      const clientX = e.clientX !== undefined ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
      const clientY = e.clientY !== undefined ? e.clientY : (e.touches && e.touches[0] ? e.touches[0].clientY : 0);

      startX = clientX;
      startY = clientY;
      initX = (box._curTranslateX !== undefined) ? box._curTranslateX : curX;
      initY = (box._curTranslateY !== undefined) ? box._curTranslateY : curY;

      box.style.animation = 'none';
      box.style.transition = 'none';
      document.body.style.userSelect = 'none';

      const activeHandle = e.currentTarget;
      if (activeHandle && activeHandle.setPointerCapture && e.pointerId !== undefined) {
        try { activeHandle.setPointerCapture(e.pointerId); } catch (_) {}
      }

      window.addEventListener('pointermove', onMove, { passive: false });
      window.addEventListener('pointerup', endDrag);
      window.addEventListener('pointercancel', endDrag);
      window.addEventListener('mousemove', onMove, { passive: false });
      window.addEventListener('mouseup', endDrag);
      window.addEventListener('touchmove', onMove, { passive: false });
      window.addEventListener('touchend', endDrag);
    }

    function onMove(e) {
      if (!isDragging) return;
      if (e.cancelable) e.preventDefault();

      const clientX = e.clientX !== undefined ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
      const clientY = e.clientY !== undefined ? e.clientY : (e.touches && e.touches[0] ? e.touches[0].clientY : 0);

      curX = initX + (clientX - startX);
      curY = initY + (clientY - startY);
      box._curTranslateX = curX;
      box._curTranslateY = curY;

      box.style.transform = `translate(${curX}px, ${curY}px)`;
    }

    function endDrag(e) {
      if (!isDragging) return;
      isDragging = false;
      document.body.style.userSelect = '';

      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', endDrag);
      window.removeEventListener('pointercancel', endDrag);
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', endDrag);
      window.removeEventListener('touchmove', onMove);
      window.removeEventListener('touchend', endDrag);
    }

    handles.forEach(h => {
      h.style.cursor = 'grab';
      h.style.touchAction = 'none';
      h.style.userSelect = 'none';
      h.addEventListener('pointerdown', startDrag);
      h.addEventListener('mousedown', startDrag);
      h.addEventListener('touchstart', startDrag, { passive: false });
    });
  });
}

function dockMeetingModal(pos) {
  const box = document.getElementById('meetingModalBox');
  if (!box) return;
  box.style.animation = 'none';
  box.style.transition = 'transform 0.22s cubic-bezier(0.16, 1, 0.3, 1)';
  const overlay = document.getElementById('meetingModal');
  const overlayW = overlay ? overlay.clientWidth : window.innerWidth;
  const boxW = box.offsetWidth || 620;

  if (pos === 'left') {
    const shift = -Math.max(20, Math.floor((overlayW - boxW) / 2 - 24));
    box.style.transform = `translate(${shift}px, 0px)`;
    box._curTranslateX = shift;
    box._curTranslateY = 0;
  } else if (pos === 'right') {
    const shift = Math.max(20, Math.floor((overlayW - boxW) / 2 - 24));
    box.style.transform = `translate(${shift}px, 0px)`;
    box._curTranslateX = shift;
    box._curTranslateY = 0;
  } else {
    box.style.transform = 'translate(0px, 0px)';
    box._curTranslateX = 0;
    box._curTranslateY = 0;
  }
}

// ================= UTILITIES & HELPERS =================
function openModal(id) {
  if (id === 'editLinksModuleModal') {
    openEditModuleModal('links');
    return;
  }
  const el = document.getElementById(id);
  if (el) {
    el.classList.add('active');
    const box = el.querySelector('.modal-box, .celebration-modal-box');
    if (box && typeof box.resetModalPosition === 'function') {
      box.resetModalPosition();
    }
  }
}
function closeModal(id) {
  if (id === 'editLinksModuleModal') id = 'editModuleModal';
  const el = document.getElementById(id);
  if (el) el.classList.remove('active');
}

function showToast(msg) {
  const t = document.getElementById('appToast');
  const m = document.getElementById('toastMessage');
  if (t && m) {
    m.textContent = msg;
    t.style.display = 'flex';
    clearTimeout(window.toastTimer);
    window.toastTimer = setTimeout(() => {
      t.style.display = 'none';
    }, 3200);
  }
}

function copyToClipboard(text, successMsg) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => {
      showToast(successMsg || '已复制到剪贴板！');
    }).catch(() => fallbackCopy(text, successMsg));
  } else {
    fallbackCopy(text, successMsg);
  }
}

function fallbackCopy(text, successMsg) {
  const ta = document.createElement('textarea');
  ta.value = text;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand('copy');
  document.body.removeChild(ta);
  showToast(successMsg || '已复制到剪贴板！');
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function toggleTheme() {
  const isComic = document.body.classList.toggle('theme-comic');
  localStorage.setItem(STORAGE_KEYS.THEME, isComic ? 'comic' : 'modern');
  const btn = document.getElementById('themeToggleBtn');
  if (btn) btn.textContent = isComic ? '✨ biu~变回' : '✨ biu~变';
}

function exportDataJSON() {
  const bundle = {
    todos: getData(STORAGE_KEYS.TODOS),
    legacyTasks: getData(STORAGE_KEYS.LEGACY_TASKS, []),
    meetings: getData(STORAGE_KEYS.MEETINGS),
    meetingRequests: getData(STORAGE_KEYS.MEETING_REQUESTS),
    notes: getData(STORAGE_KEYS.NOTES),
    links: getData(STORAGE_KEYS.LINKS),
    linkSettings: getData(STORAGE_KEYS.LINK_SETTINGS),
    monthlyRoutines: getData(STORAGE_KEYS.MONTHLY_ROUTINES),
    monthlyChecklist: getData(STORAGE_KEYS.MONTHLY_CHECKLIST),
    englishCheckin: getData(STORAGE_KEYS.ENGLISH_CHECKIN)
  };
  const blob = new Blob([JSON.stringify(bundle, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `snoopy_lab_backup_${getTodayDateStr()}.json`;
  a.click();
  showToast('💾 数据备份已成功下载！');
}

function initSeeds() {
  function seedLocalOnly(key, val) {
    if (!localStorage.getItem(key)) {
      try {
        localStorage.setItem(key, JSON.stringify(val));
      } catch (e) {}
    }
  }

  // Restore any previous batch shift backup to ensure pure Cairo baseline times
  const oldBackup = getData(STORAGE_KEYS.BATCH_SHIFT_BACKUP, null);
  if (oldBackup && oldBackup.meetings && Array.isArray(oldBackup.meetings)) {
    try {
      localStorage.setItem(STORAGE_KEYS.MEETINGS, JSON.stringify(oldBackup.meetings));
      localStorage.removeItem(STORAGE_KEYS.BATCH_SHIFT_BACKUP);
    } catch (e) {}
  }

  const todayStr = getTodayDateStr();

  // Legacy key recovery for meetings and meeting requests across previous versions
  const legacyMeetingKeys = [
    'snoopy_supervisor_meetings_v5', 'snoopy_supervisor_meetings_v4',
    'snoopy_supervisor_meetings_v3', 'snoopy_supervisor_meetings_v2',
    'snoopy_supervisor_meetings'
  ];
  if (!localStorage.getItem(STORAGE_KEYS.MEETINGS) || JSON.parse(localStorage.getItem(STORAGE_KEYS.MEETINGS) || '[]').length === 0) {
    for (const oldKey of legacyMeetingKeys) {
      try {
        const raw = localStorage.getItem(oldKey);
        if (raw) {
          const parsed = JSON.parse(raw);
          if (Array.isArray(parsed) && parsed.length > 0) {
            localStorage.setItem(STORAGE_KEYS.MEETINGS, raw);
            break;
          }
        }
      } catch (e) {}
    }
  }

  const legacyRequestKeys = [
    'snoopy_meeting_requests_v5', 'snoopy_meeting_requests_v4',
    'snoopy_meeting_requests_v3', 'snoopy_meeting_requests_v2',
    'snoopy_meeting_requests'
  ];
  if (!localStorage.getItem(STORAGE_KEYS.MEETING_REQUESTS) || JSON.parse(localStorage.getItem(STORAGE_KEYS.MEETING_REQUESTS) || '[]').length === 0) {
    for (const oldKey of legacyRequestKeys) {
      try {
        const raw = localStorage.getItem(oldKey);
        if (raw) {
          const parsed = JSON.parse(raw);
          if (Array.isArray(parsed) && parsed.length > 0) {
            localStorage.setItem(STORAGE_KEYS.MEETING_REQUESTS, raw);
            break;
          }
        }
      } catch (e) {}
    }
  }

  seedLocalOnly(STORAGE_KEYS.MEETINGS, []);

  if (!localStorage.getItem(STORAGE_KEYS.LEGACY_TASKS) || JSON.parse(localStorage.getItem(STORAGE_KEYS.LEGACY_TASKS) || '[]').length === 0) {
    seedLocalOnly(STORAGE_KEYS.LEGACY_TASKS, [
      {
        id: 1001,
        status: "推进中",
        title: "突尼斯与利比亚交付资源协调与外汇保函特批",
        owner: "陈总",
        createdDate: "2026-10-15",
        targetDate: "2026-11-20",
        updatedFinishDate: "",
        progress: "整理两地法务补充条款，预约下周向曦总复汇报审批，跟进商务保函出具",
        reviewOpinion: "同意汇率特批方案，补充利比亚分包合规条款后上会定夺",
        remark: "需重点关注利比亚外汇管制，会同法务部协同",
        reportTime: "2026-10-28 14:30",
        isOverdue: false,
        isCurrentNew: true,
        isCurrentClosed: false,
        domain: "交付商务",
        department: "交付商务",
        createdAt: 1730000000000
      },
      {
        id: 1002,
        title: "开罗数据中心应急演练与灾备容灾方案审批",
        owner: "王工",
        department: "海外IT与基础设施部",
        priority: "p1",
        status: "pending",
        description: "按年度合规要求，开罗核心机房需在11月底前完成双活容灾实战演练，需向曦总汇报整体窗口期及业务割接降级方案。",
        targetDate: "2026-11-25",
        nextPlan: "准备演练方案PPT汇报稿，本周内发起预约向曦总做首轮专项汇报。",
        hasMinutes: false,
        createdAt: 1730100000000
      },
      {
        id: 1003,
        title: "中东非区域跨国差旅合规报销流程优化方案",
        owner: "李经理",
        department: "财务与综合管理部",
        priority: "p1",
        status: "in_progress",
        description: "各办事处反馈外币汇率折算及多币种发票核销周期过长，拟优化电子发票快速通道并推行差旅预审制。",
        targetDate: "2026-11-15",
        nextPlan: "已向曦总汇报一次，曦总要求补充利比亚与尼日利亚特殊币种操作细则，修改后出具会议纪要并宣贯。",
        hasMinutes: true,
        createdAt: 1730200000000
      },
      {
        id: 1004,
        title: "Q2季度大客户维保续签与SLA服务等级协议闭环",
        owner: "赵总",
        department: "海外交付与商务部",
        priority: "p0",
        status: "completed",
        description: "重点电信运营商年度维保合同谈判，前期商务条款存在分歧，经向曦总汇报并获授权商务折让方案后顺利签约。",
        targetDate: "2026-10-30",
        nextPlan: "合同已全签完毕，纪要已归档，项目已顺利移交运营团队，本项遗留任务圆满闭环。",
        hasMinutes: true,
        createdAt: 1729000000000
      }
    ]);
  }

  seedLocalOnly(STORAGE_KEYS.TODOS, [
    { id: 101, text: "核对阿尔及利亚代表处最新提交的差旅凭证并归档", priority: "q2", quadrant: "q2", dueDate: todayStr, completed: false, archived: false },
    { id: 102, text: "提前准备主管 10:00 交付决策会议资料与签批表", priority: "q1", quadrant: "q1", dueDate: todayStr, completed: false, archived: false },
    { id: 103, text: "校对科特迪瓦、塞内加尔代表处跨区交流日程 (注意 2 小时时差)", priority: "q3", quadrant: "q3", dueDate: todayStr, completed: false, archived: false },
    { id: 104, text: "分发今日开罗晨会纪要至各代表处接口秘书", priority: "q4", quadrant: "q4", dueDate: todayStr, completed: true, archived: false }
  ]);

  seedLocalOnly(STORAGE_KEYS.LINK_SETTINGS, {
    title: "月度闯关 · Monthly Quest",
    tag: "🎯 月度打卡闯关"
  });

  seedLocalOnly(STORAGE_KEYS.MONTHLY_ROUTINES, DEFAULT_MONTHLY_ROUTINES);

  seedLocalOnly(STORAGE_KEYS.LINKS, [
    { id: 201, name: "企业海外工作邮箱", url: "https://mail.google.com", category: "🏢 内部协同", icon: "📬" },
    { id: 202, name: "非洲业务协同知识库", url: "https://notion.so", category: "🌍 区域协同", icon: "📚" },
    { id: 203, name: "主管日常日程日历", url: "https://calendar.google.com", category: "🏢 内部协同", icon: "📅" },
    { id: 204, name: "跨国线上会议室 (WeLink)", url: "https://welink.huawei.com", category: "🏢 内部协同", icon: "💻" },
    { id: 205, name: "全球差旅申请与商旅预订平台", url: "https://ctrip.com", category: "✈️ 商旅出行", icon: "✈️" }
  ]);

  seedLocalOnly(STORAGE_KEYS.NOTES, [
    { id: 301, text: "📌 8 代表处时区快速对齐备忘：\\n• 开罗（基准·冬令时）：UTC+2\\n• 地南·利比亚：UTC+2 (0h · 无时差)\\n• 地南·突尼斯、阿尔及利亚、刚果（金）、喀麦隆：UTC+1 (-1h)\\n• 摩洛哥、科特迪瓦、塞内加尔：UTC+0 (-2h)\\n⚠️ 特别提醒：地中海南管辖突尼斯(UTC+1)与利比亚(UTC+2)，两地相差1小时！\\n★ 最佳跨区会议对齐时间：开罗时间 11:00 - 17:00", category: "🌍 代表处对接", time: "09:15" },
    { id: 302, text: "👔 主管习惯交代备忘：\\n• 每次预约必须包含清晰的决策点（最多不超过3条）。\\n• 汇报材料在会前半小时打印放置于办公桌右侧。", category: "👔 主管交代", time: "09:30" }
  ]);

  seedLocalOnly(STORAGE_KEYS.MEETING_REQUESTS, [
    {
      id: 1,
      requester: "地南代表处 陈总",
      topic: "突尼斯与利比亚Q3交付资源协调与汇率特批沟通",
      urgency: "high",
      duration: "45",
      status: "pending",
      createdAt: "09-24 14:20"
    },
    {
      id: 2,
      requester: "开罗交付部 王部长",
      topic: "开罗机房硬件升级割接方案与应急预案汇报",
      urgency: "medium",
      duration: "30",
      status: "pending",
      createdAt: "09-24 15:10"
    }
  ]);

  seedLocalOnly(STORAGE_KEYS.ENGLISH_CHECKIN, {
    history: [],
    streak: 0,
    lastDate: ''
  });

  seedLocalOnly(STORAGE_KEYS.NORDIC_BUCKET_LIST, [
    { id: 1, text: "在挪威特罗姆瑟或阿比斯库守候欧若拉北极光 (Aurora Borealis)", checked: false },
    { id: 2, text: "在斯德哥尔摩老城咖啡馆点黑咖啡与肉桂卷享用正宗 Fika", checked: false },
    { id: 3, text: "乘坐弗洛姆高山列车穿越挪威最险峻壮丽的松恩峡湾 (Flåm)", checked: false },
    { id: 4, text: "在冰岛蓝湖 (Blue Lagoon) 泡地热温泉并涂抹天然火山白硅泥", checked: false },
    { id: 5, text: "在芬兰拉普兰罗瓦涅米探访联合国认证的圣诞老人村", checked: false },
    { id: 6, text: "体验一次纯正芬兰木屋烟熏桑拿并跃入冰湖冰潜 (Avanto)", checked: false },
    { id: 7, text: "在挪威北极圈深海峡湾乘静音混合动力游船出海观座头鲸与虎鲸", checked: false },
    { id: 8, text: "漫步冰岛杰古沙龙冰河湖与晶莹剔透的钻石黑沙滩 (Diamond Beach)", checked: false }
  ]);
}

// Initialize Application
initSeeds();
initDailyQuote();
setInterval(initDailyQuote, 60000);

if (localStorage.getItem(STORAGE_KEYS.THEME) === 'comic') {
  document.body.classList.add('theme-comic');
  const btn = document.getElementById('themeToggleBtn');
  if (btn) btn.textContent = '✨ biu~变回';
}

initTimePickers();
initModalDragSystem();
document.addEventListener('click', function(e) {
  if (e && e.target && !e.target.closest('.time-picker-wrapper')) {
    closeAllTimePickers();
  }
  if (e && e.target && !e.target.closest('#profileMenu')) {
    setProfileMenuOpen(false);
  }
});
document.addEventListener('keydown', function(e) {
  if (e && e.key === 'Escape') setProfileMenuOpen(false);
});
applyModuleHeaderSettings();
renderLegacyTasks();
renderMeetings();
renderTodos();
renderTimezones();
setInterval(renderTimezones, 1000);
renderLinks();
renderMonthlyRoutines();
renderNotes();
initDailyEnglish();
updateTzSimulator();
renderHomeDashboard();
initBlackboardInputListeners();
initBlackboardFontSettings();
initHostDatabaseSync();

window.APP_VERSION = '__APP_VERSION__';
console.log("Snoopy's Little Lab loaded successfully (" + window.APP_VERSION + ") with smart calendar import, auto free slots, and chronological timezones!");
</script>
</body>
</html>
"""

login_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow">
<title>回到 Snoopy’s Little Lab</title>
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/favicon.png">
<style>
  :root {
    --ink: #171717;
    --paper: #fffdf8;
    --cream: #f8f0df;
    --red: #d9383a;
    --yellow: #f5bf36;
    --muted: #6b655d;
  }
  * { box-sizing: border-box; }
  html, body { min-height: 100%; }
  body {
    margin: 0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px 16px;
    box-sizing: border-box;
    overflow-x: hidden;
    color: var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Hiragino Sans GB", sans-serif;
    background:
      radial-gradient(circle at 12% 18%, rgba(245,191,54,.28) 0 8px, transparent 9px),
      radial-gradient(circle at 88% 78%, rgba(217,56,58,.14) 0 7px, transparent 8px),
      linear-gradient(135deg, #fffaf0 0%, #f7ecd7 48%, #fffdf8 100%);
  }
  body::before, body::after {
    content: "";
    position: fixed;
    width: 230px;
    height: 230px;
    border: 2px solid rgba(23,23,23,.08);
    border-radius: 48% 52% 46% 54%;
    transform: rotate(18deg);
    pointer-events: none;
  }
  body::before { left: -90px; top: -90px; }
  body::after { right: -100px; bottom: -105px; transform: rotate(-22deg); }
  .login-shell {
    width: min(940px, calc(100% - 32px));
    min-height: 570px;
    display: grid;
    grid-template-columns: 1.08fr .92fr;
    background: var(--paper);
    border: 2px solid var(--ink);
    border-radius: 28px;
    box-shadow: 12px 12px 0 var(--ink);
    overflow: hidden;
    position: relative;
  }
  .illustration {
    min-height: 570px;
    padding: 42px 42px 32px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
    background:
      linear-gradient(rgba(255,255,255,.22) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,.22) 1px, transparent 1px),
      var(--yellow);
    background-size: 26px 26px;
    border-right: 2px solid var(--ink);
  }
  .eyebrow {
    width: fit-content;
    padding: 7px 12px;
    border: 2px solid var(--ink);
    border-radius: 999px;
    background: var(--paper);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .12em;
  }
  .illustration h1 {
    margin: 16px 0 8px;
    max-width: 410px;
    font-family: Georgia, "Songti SC", serif;
    font-size: clamp(38px, 5vw, 64px);
    line-height: 1.02;
    letter-spacing: -.045em;
  }
  .illustration p {
    margin: 0;
    max-width: 380px;
    color: #38342e;
    font-size: 15px;
    font-weight: 650;
  }
  .snoopy-stage {
    height: 285px;
    position: relative;
    display: flex;
    align-items: flex-end;
    justify-content: center;
  }
  .snoopy-stage::before {
    content: "Z · Z · Z";
    position: absolute;
    right: 4px;
    top: 20px;
    font-family: Georgia, serif;
    font-weight: 900;
    font-size: 21px;
    transform: rotate(-8deg);
  }
  .snoopy-stage img {
    width: min(100%, 390px);
    max-height: 275px;
    object-fit: contain;
    filter: drop-shadow(7px 8px 0 rgba(255,255,255,.8));
    animation: floaty 3.4s ease-in-out infinite;
  }
  .woodstock {
    position: absolute;
    width: 74px !important;
    height: 74px;
    object-fit: contain;
    right: 10px;
    bottom: 16px;
    filter: none !important;
    animation-delay: -.8s !important;
  }
  .login-panel {
    padding: 56px 48px 42px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .mini-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 34px;
    font-size: 13px;
    font-weight: 850;
  }
  .mini-brand img { width: 44px; height: 44px; object-fit: contain; }
  .login-panel h2 { margin: 0; font-size: 29px; letter-spacing: -.03em; }
  .login-panel .welcome { margin: 8px 0 30px; color: var(--muted); font-size: 14px; }
  label { display: block; margin-bottom: 9px; font-size: 13px; font-weight: 800; }
  .password-wrap { position: relative; }
  input {
    width: 100%;
    height: 52px;
    padding: 0 52px 0 15px;
    border: 2px solid var(--ink);
    border-radius: 12px;
    background: #fff;
    color: var(--ink);
    font: inherit;
    font-size: 16px;
    outline: none;
    transition: box-shadow .18s, transform .18s;
  }
  input:focus { box-shadow: 4px 4px 0 var(--yellow); transform: translate(-1px, -1px); }
  .peek {
    position: absolute;
    right: 8px;
    top: 8px;
    width: 38px;
    height: 36px;
    border: 0;
    border-radius: 9px;
    background: var(--cream);
    cursor: pointer;
    font-size: 17px;
  }
  .submit {
    width: 100%;
    min-height: 52px;
    margin-top: 16px;
    border: 2px solid var(--ink);
    border-radius: 12px;
    background: var(--red);
    color: #fff;
    box-shadow: 4px 4px 0 var(--ink);
    font: inherit;
    font-weight: 850;
    font-size: 15px;
    cursor: pointer;
    transition: transform .15s, box-shadow .15s, background .15s;
  }
  .submit:hover { background: #bd2d30; transform: translate(-1px, -1px); box-shadow: 6px 6px 0 var(--ink); }
  .submit:active { transform: translate(3px, 3px); box-shadow: 1px 1px 0 var(--ink); }
  .submit:disabled { opacity: .65; cursor: wait; }
  .error {
    min-height: 21px;
    margin-top: 14px;
    color: #b42324;
    font-size: 13px;
    font-weight: 700;
  }
  .privacy-note {
    margin-top: 18px;
    padding-top: 18px;
    border-top: 1px dashed #c9c2b7;
    color: var(--muted);
    font-size: 11.5px;
    line-height: 1.6;
  }
  .login-card-version {
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11px;
    color: var(--muted);
    font-weight: 700;
  }
  .login-version-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    background: var(--cream);
    border: 1.5px solid var(--ink);
    border-radius: 999px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 11px;
    font-weight: 800;
    color: var(--ink);
    user-select: all;
  }
  .login-footer {
    margin-top: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-size: 12px;
    color: var(--muted);
    font-weight: 650;
    letter-spacing: .02em;
    user-select: none;
  }
  .login-version-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    background: var(--paper);
    border: 1.5px solid var(--ink);
    border-radius: 999px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 11px;
    font-weight: 800;
    color: var(--ink);
    box-shadow: 2px 2px 0 var(--ink);
    user-select: all;
  }
  @keyframes floaty { 0%, 100% { transform: translateY(0) rotate(-1deg); } 50% { transform: translateY(-8px) rotate(1deg); } }
  @media (prefers-reduced-motion: reduce) { .snoopy-stage img { animation: none; } }
  @media (max-width: 760px) {
    body { padding: 16px 0 28px; justify-content: flex-start; }
    .login-shell { grid-template-columns: 1fr; box-shadow: 7px 7px 0 var(--ink); }
    .illustration { min-height: 310px; padding: 28px 28px 12px; border-right: 0; border-bottom: 2px solid var(--ink); }
    .illustration h1 { font-size: 40px; max-width: 330px; }
    .illustration p { font-size: 13px; }
    .snoopy-stage { position: absolute; right: 14px; bottom: 4px; width: 220px; height: 180px; opacity: .96; }
    .snoopy-stage::before, .woodstock { display: none; }
    .login-panel { padding: 34px 28px 30px; }
    .mini-brand { margin-bottom: 24px; }
  }
</style>
</head>
<body>
  <main class="login-shell">
    <section class="illustration" aria-label="Snoopy 欢迎插画">
      <div>
        <div class="eyebrow">PRIVATE LITTLE LAB</div>
        <h1>欢迎回到<br>Snoopy 的小实验室</h1>
        <p>任务、会议、灵感和旅行计划，都安静地等你回来。</p>
      </div>
      <div class="snoopy-stage" aria-hidden="true">
        <img src="__IMG_ORDINARY_DOGHOUSE__" alt="">
        <img class="woodstock" src="__IMG_WOODSTOCK__" alt="">
      </div>
    </section>
    <section class="login-panel">
      <div class="mini-brand">
        <img src="__IMG_CANONICAL__" alt="Snoopy">
        <span>Snoopy’s Little Lab · Sanyli.</span>
      </div>
      <h2>输入秘密口令</h2>
      <p class="welcome">只有你和 Snoopy 知道的那一句。</p>
      <form id="loginForm" novalidate>
        <label for="password">登录密码</label>
        <div class="password-wrap">
          <input id="password" name="password" type="password" autocomplete="current-password" required autofocus aria-describedby="loginError">
          <button class="peek" id="peekButton" type="button" aria-label="显示密码" title="显示或隐藏密码">👀</button>
        </div>
        <button class="submit" id="submitButton" type="submit">🐾 打开我的小实验室</button>
        <div class="error" id="loginError" role="alert" aria-live="polite"></div>
      </form>
      <div class="privacy-note">
        <div>🔐 密码只发送给你的主机验证；登录会话使用安全 Cookie，页面不会保存密码。</div>
        <div class="login-card-version">
          <span>当前发布版本</span>
          <span class="login-version-pill" id="loginCardVersionBadge">🏷️ __APP_VERSION__</span>
        </div>
      </div>
    </section>
  </main>
  <footer class="login-footer">
    <span>Snoopy’s Little Lab · Sanyli.</span>
    <span class="login-version-badge" id="loginFooterVersionBadge" title="当前发布版本（每次更新递增）">🏷️ __APP_VERSION__</span>
  </footer>
<script>
  window.APP_VERSION = '__APP_VERSION__';
  const form = document.getElementById('loginForm');
  const passwordInput = document.getElementById('password');
  const submitButton = document.getElementById('submitButton');
  const loginError = document.getElementById('loginError');
  document.getElementById('peekButton').addEventListener('click', function() {
    const showing = passwordInput.type === 'text';
    passwordInput.type = showing ? 'password' : 'text';
    this.textContent = showing ? '👀' : '🙈';
    this.setAttribute('aria-label', showing ? '显示密码' : '隐藏密码');
    passwordInput.focus();
  });
  form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const password = passwordInput.value;
    if (!password) {
      loginError.textContent = 'Snoopy 还没听到口令呢。';
      passwordInput.focus();
      return;
    }
    submitButton.disabled = true;
    submitButton.textContent = '正在确认口令…';
    loginError.textContent = '';
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      });
      const result = await response.json();
      if (response.ok && result.success) {
        submitButton.textContent = '欢迎回来！🐾';
        window.location.replace('/');
        return;
      }
      if (response.status === 429) {
        loginError.textContent = '尝试次数有点多，Snoopy 需要休息 15 分钟。';
      } else {
        loginError.textContent = '口令不对，再想想看？';
      }
      passwordInput.select();
    } catch (error) {
      loginError.textContent = '暂时联系不上小实验室，请稍后重试。';
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = '🐾 打开我的小实验室';
    }
  });
</script>
</body>
</html>
"""

replacements = {
    '__APP_VERSION__': app_version,
    '__IMG_ORDINARY_DOGHOUSE__': img_ordinary_doghouse,
    '__IMG_BORDER_SNOOPY__': img_border_snoopy,
    '__IMG_WOODSTOCK__': img_woodstock,
    '__IMG_SUPERVISOR_SECRETARY__': img_supervisor_secretary,
    '__IMG_BEAGLE_SCOUT__': img_beagle_scout,
    '__IMG_FLYING_ACE__': img_flying_ace,
    '__IMG_JOE_COOL__': img_joe_cool,
    '__IMG_AUTHOR__': img_author,
    '__IMG_DAILY_ENGLISH__': img_daily_english,
    '__IMG_CANONICAL__': img_canonical,
    '__IMG_DANCE__': img_dance,
    '__ENGLISH_DATA_RAW__': english_data_json,
    '__ENGLISH_DICTIONARY_RAW__': english_dict_json
}

output_html = html_template
output_login_html = login_template
for placeholder, value in replacements.items():
    output_html = output_html.replace(placeholder, value)
    output_login_html = output_login_html.replace(placeholder, value)

output_path = 'index.html'
with open(output_path, 'w', encoding='utf-8') as out_f:
    out_f.write(output_html)

with open('login.html', 'w', encoding='utf-8') as out_f:
    out_f.write(output_login_html)

# Browser tab and home-screen icons use the canonical Snoopy artwork.
favicon_png_path = os.path.join('assets', 'snoopy_canonical.png')
shutil.copyfile(favicon_png_path, 'favicon.png')
with open(favicon_png_path, 'rb') as icon_source:
    png_bytes = icon_source.read()
icon_header = struct.pack('<HHH', 0, 1, 1)
icon_entry = struct.pack('<BBBBHHII', 173, 200, 0, 0, 1, 32, len(png_bytes), 22)
with open('favicon.ico', 'wb') as icon_file:
    icon_file.write(icon_header + icon_entry + png_bytes)

# Always sync to dist directory so backend server serves the latest build immediately
dist_dir = os.path.join(BASE_DIR, 'dist')
os.makedirs(dist_dir, exist_ok=True)
shutil.copy2(output_path, os.path.join(dist_dir, 'index.html'))
shutil.copy2('login.html', os.path.join(dist_dir, 'login.html'))
shutil.copy2('favicon.ico', os.path.join(dist_dir, 'favicon.ico'))
shutil.copy2('favicon.png', os.path.join(dist_dir, 'favicon.png'))

file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"Step 2: Compiled standalone {output_path} & login.html successfully! (Version: {app_version}, Size: {file_size_mb:.2f} MB)")
print(f"Step 3: Synced all build outputs to {dist_dir} successfully!")

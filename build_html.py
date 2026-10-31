import json

with open('assets_b64.json', 'r') as f:
    assets = json.load(f)

# Assign personas
img_ordinary_doghouse = assets['ordinary_doghouse']
img_author = assets['author_typewriter']
img_flying_ace = assets['flying_ace']
img_joe_cool = assets['joe_cool_lean']
img_beagle_scout = assets['beagle_scout']
img_head_beagle = assets['head_beagle']
img_artist_dream = assets['artist_dream']
img_woodstock = assets['woodstock']
img_canonical = assets['canonical']
img_dance = assets['dance']
img_sitting = assets['sitting']
img_heart = assets.get('snoopy_heart', img_canonical)
img_hug = assets.get('snoopy_hug', img_canonical)

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Snoopy’s Little Lab · 个人专属工作台</title>
<style>
  :root {{
    --bg: #f8f7f4;
    --card: #ffffff;
    --card-subtle: #fcfbf9;
    --text-primary: #18181b;
    --text-secondary: #52525b;
    --text-muted: #8e8e93;
    --border: #e8e6e1;
    --border-hover: #18181b;
    --accent-red: #d9383a;
    --accent-red-hover: #b9292b;
    --accent-red-soft: #fef2f2;
    --woodstock-yellow: #f5b041;
    --woodstock-soft: #fef9e7;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.04);
    --shadow-card: 0 2px 10px -2px rgba(0,0,0,0.05), 0 1px 4px rgba(0,0,0,0.02);
    --shadow-hover: 0 10px 25px -4px rgba(0,0,0,0.08);
    --radius-sm: 6px;
    --radius-md: 12px;
    --radius-lg: 18px;
    --font-sans: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", sans-serif;
    --font-mono: "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace;
    --font-serif: Georgia, "Songti SC", "SimSun", serif;
    --transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  }}

  /* Comic theme toggle */
  body.theme-comic {{
    --bg: #faf5eb;
    --card: #ffffff;
    --card-subtle: #f6efe1;
    --border: #18181b;
    --shadow-sm: 2px 2px 0px #18181b;
    --shadow-card: 3px 3px 0px #18181b;
    --shadow-hover: 5px 5px 0px #18181b;
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; -webkit-font-smoothing: antialiased; }}
  body {{
    font-family: var(--font-sans);
    background-color: var(--bg);
    color: var(--text-primary);
    line-height: 1.55;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }}

  ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
  ::-webkit-scrollbar-thumb {{ background: #d6d3cd; border-radius: 99px; }}
  ::-webkit-scrollbar-thumb:hover {{ background: #999; }}

  /* Header */
  .app-header {{
    background: var(--card);
    border-bottom: 2px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
  }}
  .header-inner {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 10px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    user-select: none;
  }}
  .brand-avatar {{
    width: 44px;
    height: 48px;
    object-fit: contain;
    transition: transform 0.25s ease;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.06));
  }}
  .brand:hover .brand-avatar {{
    transform: rotate(-6deg) scale(1.08);
  }}
  .brand-text h1 {{
    font-size: 19px;
    font-weight: 800;
    letter-spacing: -0.4px;
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--text-primary);
  }}
  .brand-tag {{
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 500;
    letter-spacing: 0.3px;
  }}

  .header-right {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .cairo-pill {{
    background: var(--card-subtle);
    border: 1px solid var(--border);
    padding: 6px 14px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 12px;
    box-shadow: var(--shadow-sm);
  }}
  .cairo-pill .flag {{ font-size: 16px; }}
  .cairo-pill .label {{ font-size: 11px; color: var(--text-muted); }}
  .cairo-pill .time {{
    font-family: var(--font-mono);
    font-weight: 700;
    font-size: 13.5px;
    color: var(--text-primary);
  }}

  .theme-btn {{
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
  }}
  .theme-btn:hover {{ background: var(--bg); }}

  /* Nav Tabs */
  .nav-bar {{
    background: var(--card);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 70px;
    z-index: 90;
  }}
  .nav-inner {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 28px;
    display: flex;
    gap: 6px;
    overflow-x: auto;
  }}
  .nav-tab {{
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
  }}
  .nav-tab img {{
    width: 22px;
    height: 22px;
    object-fit: contain;
    transition: transform 0.2s ease;
  }}
  .nav-tab:hover {{ color: var(--text-primary); }}
  .nav-tab:hover img {{ transform: scale(1.18); }}
  .nav-tab.active {{ color: var(--text-primary); font-weight: 700; }}
  .nav-tab.active::after {{
    content: "";
    position: absolute;
    bottom: -1px;
    left: 12px;
    right: 12px;
    height: 3px;
    background: var(--text-primary);
    border-radius: 3px;
  }}
  .badge-dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-red);
    display: inline-block;
  }}

  /* Main Container */
  .main-wrapper {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 24px 28px;
    width: 100%;
    flex: 1;
  }}
  .tab-pane {{
    display: none;
    animation: fadeIn 0.25s ease;
  }}
  .tab-pane.active {{ display: block; }}
  @keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(4px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  /* Cards */
  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-card);
    overflow: hidden;
    margin-bottom: 20px;
    transition: var(--transition);
  }}
  body.theme-comic .card {{ border: 2px solid #18181b; }}
  .card:hover {{ box-shadow: var(--shadow-hover); }}

  .card-header {{
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }}
  body.theme-comic .card-header {{ border-bottom: 2px solid #18181b; }}

  .card-title {{
    font-size: 14px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 9px;
  }}
  .card-title img {{
    width: 24px;
    height: 28px;
    object-fit: contain;
  }}
  .persona-tag {{
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    background: var(--card-subtle);
    border: 1px solid var(--border);
    padding: 2px 8px;
    border-radius: 99px;
    margin-left: 4px;
  }}
  .card-body {{ padding: 20px; }}

  /* Buttons */
  .btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 600;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background: var(--card);
    color: var(--text-primary);
    cursor: pointer;
    transition: var(--transition);
    text-decoration: none;
    font-family: inherit;
  }}
  body.theme-comic .btn {{ border: 1.5px solid #18181b; }}
  .btn:hover {{ background: var(--bg); border-color: var(--border-hover); }}

  .btn-primary {{ background: #18181b; color: #fff; border-color: #18181b; }}
  .btn-primary:hover {{ background: #333; color: #fff; }}

  .btn-red {{ background: var(--accent-red); color: #fff; border-color: var(--accent-red); }}
  .btn-red:hover {{ background: var(--accent-red-hover); color: #fff; }}

  .btn-sm {{ padding: 4px 10px; font-size: 11px; }}
  .btn-icon {{ width: 28px; height: 28px; padding: 0; border-radius: var(--radius-sm); }}
  .btn-ghost {{ background: transparent; border-color: transparent; }}
  .btn-ghost:hover {{ background: var(--bg); border-color: transparent; }}

  /* ================= EXQUISITE HERO BANNER ================= */
  .snoopy-hero-banner {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 30px 38px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow-card);
    gap: 36px;
    position: relative;
    overflow: hidden;
    background-image: radial-gradient(#eceae4 1px, transparent 1px);
    background-size: 20px 20px;
    background-position: -5px -5px;
  }}
  body.theme-comic .snoopy-hero-banner {{
    border: 2.5px solid #18181b;
    box-shadow: 4px 4px 0px #18181b;
    background-color: #fffefb;
  }}

  .hero-content {{
    flex: 1;
    max-width: 660px;
  }}
  .hero-badge-row {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
  }}
  .hero-mini-pill {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    font-family: var(--font-mono);
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }}
  .hero-greeting {{
    font-size: 23px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    letter-spacing: -0.4px;
  }}

  /* Poetic Quote Box - Schulz Natural Thought */
  .hero-quote-box {{
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(8px);
    border-left: 3.5px solid var(--accent-red);
    padding: 16px 20px;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    margin-bottom: 20px;
    border-top: 1px solid var(--border);
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
  }}
  body.theme-comic .hero-quote-box {{
    background: #fff;
    border: 1.5px solid #18181b;
    border-left: 4.5px solid var(--accent-red);
    box-shadow: 2px 2px 0px #18181b;
  }}
  .hero-quote-text {{
    font-family: var(--font-serif);
    font-size: 15px;
    color: var(--text-primary);
    font-weight: 600;
    line-height: 1.6;
    letter-spacing: 0.2px;
  }}
  .hero-quote-cn {{
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 5px;
    line-height: 1.55;
  }}
  .hero-quote-author {{
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 1px dashed var(--border);
    padding-top: 8px;
  }}
  .hero-quote-author {{
    display: flex;
    align-items: center;
    justify-content: flex-start;
    border-top: 1px dashed var(--border);
    padding-top: 8px;
    margin-top: 4px;
    font-family: var(--font-serif);
    font-size: 12px;
    color: var(--text-muted);
  }}

  .hero-actions {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }}

  /* Exquisite Canonical Snoopy & Woodstock Doghouse Vignette Stage */
  .hero-stage {{
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    padding: 12px 24px;
    background: linear-gradient(180deg, rgba(254, 249, 231, 0.45) 0%, rgba(254, 242, 242, 0.45) 100%);
    border-radius: var(--radius-lg);
    border: 1px dashed var(--border);
    user-select: none;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
  }}
  body.theme-comic .hero-stage {{
    border: 2px dashed #18181b;
    background: #fff8e8;
  }}
  .hero-stage:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
  }}
  .hero-doghouse {{
    max-width: 215px;
    height: auto;
    object-fit: contain;
    filter: drop-shadow(0 6px 16px rgba(0,0,0,0.09));
    transition: transform 0.25s ease;
  }}
  .hero-stage:hover .hero-doghouse {{
    transform: scale(1.02);
  }}
  .hero-bubble {{
    position: absolute;
    top: -12px;
    right: 20px;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 99px;
    padding: 3px 10px;
    font-size: 10.5px;
    font-weight: 700;
    color: var(--text-secondary);
    box-shadow: var(--shadow-sm);
    animation: bubbleFloat 2.5s ease-in-out infinite;
    pointer-events: none;
  }}
  body.theme-comic .hero-bubble {{
    border: 1.5px solid #18181b;
    box-shadow: 2px 2px 0px #18181b;
  }}
  @keyframes gentleBob {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-5px); }}
  }}
  @keyframes bubbleFloat {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-3px); }}
  }}

  /* 2 Column Layout */
  .grid-2col {{
    display: grid;
    grid-template-columns: 1.25fr 0.75fr;
    gap: 20px;
  }}

  /* Timezone World Clocks */
  .tz-base-banner {{
    background: #18181b;
    color: #ffffff;
    border-radius: var(--radius-md);
    padding: 22px 26px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  body.theme-comic .tz-base-banner {{ border: 2px solid #18181b; box-shadow: 4px 4px 0px #18181b; }}

  .tz-base-title {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .tz-base-title h3 {{ font-size: 18px; font-weight: 700; }}
  .tz-base-badge {{
    background: var(--accent-red);
    color: white;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 99px;
  }}
  .tz-base-time {{
    font-family: var(--font-mono);
    font-size: 34px;
    font-weight: 400;
  }}

  .tz-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 14px;
  }}
  .tz-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px;
    transition: var(--transition);
  }}
  body.theme-comic .tz-card {{ border: 1.5px solid #18181b; }}
  .tz-card:hover {{
    border-color: var(--border-hover);
    transform: translateY(-2px);
  }}
  .tz-card-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }}
  .tz-card-name {{ font-size: 13px; font-weight: 700; }}
  .tz-pill {{
    font-size: 11px;
    font-family: var(--font-mono);
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
    background: var(--bg);
    border: 1px solid var(--border);
  }}
  .tz-pill.same {{ background: #e8f5e9; color: #2e7d32; border-color: #c8e6c9; }}
  .tz-time {{
    font-size: 26px;
    font-weight: 700;
    font-family: var(--font-mono);
    margin: 4px 0;
  }}
  .tz-card-bottom {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: var(--text-muted);
    border-top: 1px dashed var(--border);
    padding-top: 8px;
    margin-top: 8px;
  }}
  .work-status {{
    font-size: 10.5px;
    padding: 1px 6px;
    border-radius: 4px;
    font-weight: 600;
  }}
  .ws-work {{ background: #e8f5e9; color: #2e7d32; }}
  .ws-off {{ background: #f5f5f5; color: #757575; }}
  .ws-lunch {{ background: #fff8e1; color: #f57f17; }}

  /* Directives (主管要求) */
  .req-item {{
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px;
    margin-bottom: 12px;
    background: var(--card);
    border-left: 3.5px solid #18181b;
    transition: var(--transition);
  }}
  body.theme-comic .req-item {{ border: 1.5px solid #18181b; border-left: 4px solid var(--accent-red); }}
  .req-item.done {{
    opacity: 0.65;
    border-left-color: #a1a1aa;
    background: var(--card-subtle);
  }}
  .req-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }}
  .req-status-tag {{
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
  }}
  .rst-pending {{ background: #fff3e0; color: #e65100; }}
  .rst-progress {{ background: #e3f2fd; color: #1565c0; }}
  .rst-done {{ background: #e8f5e9; color: #2e7d32; }}
  .req-body {{
    font-size: 13.5px;
    font-weight: 600;
    margin-bottom: 10px;
    line-height: 1.5;
  }}
  .req-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11.5px;
    color: var(--text-muted);
  }}

  /* Todos */
  .todo-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    margin-bottom: 8px;
    background: var(--card);
    transition: var(--transition);
  }}
  body.theme-comic .todo-item {{ border: 1.5px solid #18181b; }}
  .todo-item:hover {{ border-color: var(--border-hover); }}
  .todo-item.completed {{
    opacity: 0.55;
    background: var(--card-subtle);
  }}
  .todo-item.completed .todo-text {{
    text-decoration: line-through;
    color: var(--text-muted);
  }}
  .todo-chk {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1.5px solid #18181b;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: var(--transition);
  }}
  .todo-item.completed .todo-chk {{
    background: #18181b;
    border-color: #18181b;
  }}
  .todo-item.completed .todo-chk::after {{
    content: "✓";
    color: white;
    font-size: 11px;
    font-weight: 800;
  }}
  .todo-content {{ flex: 1; min-width: 0; }}
  .todo-text {{ font-size: 13px; font-weight: 500; word-break: break-word; }}
  .todo-meta {{
    display: flex;
    gap: 8px;
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 3px;
    align-items: center;
  }}
  .prio-pill {{
    font-size: 10px;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 3px;
  }}
  .prio-high {{ background: #ffebee; color: #c62828; }}
  .prio-medium {{ background: #fff8e1; color: #f57f17; }}
  .prio-low {{ background: #f5f5f5; color: #757575; }}

  /* Notes */
  .notes-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
  }}
  .note-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 150px;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    white-space: pre-wrap;
  }}
  body.theme-comic .note-card {{ border: 1.5px solid #18181b; }}
  .note-card:hover {{ box-shadow: var(--shadow-hover); border-color: var(--border-hover); }}
  .note-text {{ font-size: 13px; line-height: 1.6; flex: 1; }}
  .note-foot {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 14px;
    border-top: 1px dashed var(--border);
    padding-top: 8px;
  }}

  /* Pomodoro */
  .pomo-container {{
    max-width: 480px;
    margin: 30px auto;
    text-align: center;
    padding: 30px;
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    background: var(--card);
    box-shadow: var(--shadow-card);
  }}
  body.theme-comic .pomo-container {{ border: 2.5px solid #18181b; box-shadow: 4px 4px 0px #18181b; }}
  .pomo-illustration {{
    width: 120px;
    height: 120px;
    margin: 0 auto 16px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .pomo-illustration img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    transition: transform 0.3s ease;
  }}
  .pomo-illustration:hover img {{ transform: rotate(5deg) scale(1.05); }}
  .pomo-time {{
    font-size: 64px;
    font-weight: 800;
    font-family: var(--font-mono);
    letter-spacing: -2px;
    margin: 10px 0 20px;
  }}
  .pomo-quote-bubble {{
    margin-top: 20px;
    font-size: 12.5px;
    color: var(--text-secondary);
    background: var(--card-subtle);
    padding: 10px 16px;
    border-radius: var(--radius-sm);
    border: 1px dashed var(--border);
  }}

  /* Quick Links */
  .links-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 14px;
  }}
  .link-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: var(--transition);
  }}
  body.theme-comic .link-card {{ border: 1.5px solid #18181b; }}
  .link-card:hover {{
    border-color: var(--border-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
  }}

  /* Modals */
  .modal-overlay {{
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.45);
    backdrop-filter: blur(4px);
    z-index: 1000;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }}
  .modal-overlay.active {{ display: flex; }}
  .modal-box {{
    background: var(--card);
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    box-shadow: 0 20px 40px rgba(0,0,0,0.18);
    width: 100%;
    max-width: 480px;
    overflow: hidden;
    animation: modalPop 0.2s ease;
  }}
  body.theme-comic .modal-box {{ border: 2.5px solid #18181b; box-shadow: 6px 6px 0px #18181b; }}
  @keyframes modalPop {{
    from {{ transform: scale(0.96); opacity: 0; }}
    to {{ transform: scale(1); opacity: 1; }}
  }}
  .modal-header {{
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .modal-body {{ padding: 20px; display: flex; flex-direction: column; gap: 14px; }}
  .modal-footer {{
    padding: 12px 20px;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    background: var(--card-subtle);
  }}
  .form-control {{
    width: 100%;
    padding: 9px 12px;
    font-size: 13px;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    background: var(--card);
    color: var(--text-primary);
    font-family: inherit;
    outline: none;
    transition: var(--transition);
  }}
  .form-control:focus {{
    border-color: #18181b;
  }}
  textarea.form-control {{ min-height: 90px; resize: vertical; }}

  /* Footer */
  .app-footer {{
    border-top: 1px solid var(--border);
    background: var(--card);
    margin-top: auto;
  }}
  .footer-inner {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 16px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: var(--text-muted);
  }}

  /* Responsive */
  @media (max-width: 960px) {{
    .grid-2col {{ grid-template-columns: 1fr; }}
    .snoopy-hero-banner {{ flex-direction: column; text-align: center; }}
    .hero-greeting {{ justify-content: center; }}
    .hero-actions {{ justify-content: center; }}
    .hero-stage {{ justify-content: center; width: 100%; }}
  }}
</style>
</head>
<body>

  <!-- Header -->
  <header class="app-header">
    <div class="header-inner">
      <div class="brand" onclick="switchTab('dashboard')">
        <!-- Canonical Snoopy Artwork -->
        <img src="{img_canonical}" alt="Snoopy" class="brand-avatar" />
        <div class="brand-text">
          <h1>Snoopy’s Little Lab</h1>
          <p class="brand-tag">Personal Workspace · Est. 2026</p>
        </div>
      </div>

      <div class="header-right">
        <!-- Cairo Clock -->
        <div class="cairo-pill">
          <span class="flag">🇪🇬</span>
          <div>
            <span class="label">开罗时间 (UTC+2)</span>
            <span class="time" id="headerCairoClock">00:00:00</span>
          </div>
        </div>

        <!-- Theme Toggle -->
        <button class="theme-btn" id="themeToggleBtn" onclick="toggleTheme()">🎨 切换漫画模式</button>
        <button class="btn btn-red btn-sm" onclick="openTodoModal()">+ 新建事项</button>
      </div>
    </div>
  </header>

  <!-- Navigation Bar with Authentic 7 Snoopy Personas Icons -->
  <nav class="nav-bar">
    <div class="nav-inner">
      <button class="nav-tab active" data-tab="dashboard" onclick="switchTab('dashboard')">
        <img src="{img_ordinary_doghouse}" alt="综合工作台" />
        <span>综合工作台</span>
      </button>
      <button class="nav-tab" data-tab="todo" onclick="switchTab('todo')">
        <img src="{img_beagle_scout}" alt="待办事项" />
        <span>待办事项</span>
        <span class="badge-dot" id="todoDot" style="display:none;"></span>
      </button>
      <button class="nav-tab" data-tab="supervisor" onclick="switchTab('supervisor')">
        <img src="{img_head_beagle}" alt="主管要求" />
        <span>主管要求</span>
        <span class="badge-dot" id="reqDot" style="display:none;"></span>
      </button>
      <button class="nav-tab" data-tab="timezone" onclick="switchTab('timezone')">
        <img src="{img_flying_ace}" alt="8代表处时钟" />
        <span>8代表处时钟</span>
      </button>
      <button class="nav-tab" data-tab="notes" onclick="switchTab('notes')">
        <img src="{img_author}" alt="每日笔记" />
        <span>每日笔记</span>
      </button>
      <button class="nav-tab" data-tab="pomodoro" onclick="switchTab('pomodoro')">
        <img src="{img_joe_cool}" alt="专注番茄钟" />
        <span>专注番茄钟</span>
      </button>
      <button class="nav-tab" data-tab="links" onclick="switchTab('links')">
        <img src="{img_artist_dream}" alt="常用链接" />
        <span>常用链接</span>
      </button>
    </div>
  </nav>

  <!-- Main Content -->
  <main class="main-wrapper">

    <!-- ================= 1. DASHBOARD (🥱 普通 Snoopy · 躺在红色狗屋上) ================= -->
    <div class="tab-pane active" id="pane-dashboard">

      <!-- Exquisite Snoopy & Woodstock Hero Banner -->
      <div class="snoopy-hero-banner">
        <div class="hero-content">
          <div class="hero-badge-row">
            <span class="hero-mini-pill" id="heroDailyDatePill">✦ Snoopy’s Little Lab · 每日哲思</span>
          </div>

          <h2 class="hero-greeting" id="heroGreeting">
            <span>今天也是充实从容的一天！</span>
          </h2>

          <div class="hero-quote-box">
            <div class="hero-quote-text" id="heroQuoteText">“Keep looking up... that's the secret of life.”</div>
            <div class="hero-quote-cn" id="heroQuoteCn">「永远抬头向上看…… 这便是生活的秘诀。」</div>
            <div class="hero-quote-author">
              <span id="heroQuoteAuthor">—— Charles M. Schulz ·《Peanuts》</span>
            </div>
          </div>

          <div class="hero-actions">
            <button class="btn btn-primary btn-sm" onclick="switchTab('todo')">🏕️ 管理今日待办 →</button>
            <button class="btn btn-sm" onclick="switchTab('supervisor')">🕵️ 查看主管要求</button>
            <button class="btn btn-sm" onclick="switchTab('timezone')">🪖 跨时区大屏</button>
            <button class="btn btn-sm" onclick="switchTab('pomodoro')">😎 开启专注番茄</button>
          </div>
        </div>

        <div class="hero-stage" title="Snoopy 趴在红色狗屋上休息 · Woodstock 陪伴在身旁">
          <span class="hero-bubble" id="heroBubbleTip">Zzz... 💭</span>
          <!-- Canonical Snoopy lying on Red Doghouse with Woodstock -->
          <img src="{img_ordinary_doghouse}" id="heroDoghouseImg" alt="Snoopy on Doghouse with Woodstock" class="hero-doghouse" />
        </div>
      </div>

      <!-- 2-Column Dashboard Content -->
      <div class="grid-2col">

        <!-- Left Column: Directives & Tasks -->
        <div>
          <!-- Quick Directives (🕵️ Head Beagle) -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">
                <img src="{img_head_beagle}" alt="Head Beagle" />
                <span>主管要求 · 最新跟踪</span>
                <span class="persona-tag">🕵️ Head Beagle</span>
              </span>
              <button class="btn btn-sm btn-ghost" onclick="switchTab('supervisor')">全部指示 →</button>
            </div>
            <div class="card-body" id="dashReqList"></div>
          </div>

          <!-- Quick Todos (🏕️ Beagle Scout) -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">
                <img src="{img_beagle_scout}" alt="Beagle Scout" />
                <span>今日待办事项</span>
                <span class="persona-tag">🏕️ Beagle Scout</span>
              </span>
              <div style="display:flex; gap:6px;">
                <button class="btn btn-sm" onclick="openTodoModal()">+ 新建待办</button>
                <button class="btn btn-sm btn-ghost" onclick="switchTab('todo')">完整清单 →</button>
              </div>
            </div>
            <div class="card-body" id="dashTodoList"></div>
          </div>
        </div>

        <!-- Right Column: Timezone Mini & Sitting Companion -->
        <div>
          <!-- 8 Offices Mini Glance (🪖 Flying Ace) -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">
                <img src="{img_flying_ace}" alt="Flying Ace" />
                <span>8 代表处当地时间与时差</span>
                <span class="persona-tag">🪖 Flying Ace</span>
              </span>
              <button class="btn btn-sm btn-ghost" onclick="switchTab('timezone')">时区大屏 →</button>
            </div>
            <div class="card-body" style="padding:12px 18px;" id="dashTimeList"></div>
          </div>

          <!-- Snoopy Warm Companion Box -->
          <div class="card" style="background:var(--card-subtle);">
            <div class="card-body" style="display:flex; align-items:center; gap:16px;">
              <img src="{img_joe_cool}" alt="Joe Cool" style="width: 58px; height: 80px; object-fit: contain; flex-shrink: 0;" />
              <div>
                <div style="font-size:13.5px; font-weight:700; color:var(--text-primary);">Snoopy’s Lab 每日专注提醒 🐾</div>
                <div style="font-size:12px; color:var(--text-secondary); margin-top:4px; line-height:1.55;">
                  “无论身在哪个时区，保持沉着与条理，每一步都踏实从容。”
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>


    <!-- ================= 2. TODOS (🏕️ Beagle Scout · 比格犬童子军) ================= -->
    <div class="tab-pane" id="pane-todo">
      <div class="card">
        <div class="card-header">
          <div style="display:flex; align-items:center; gap:9px;">
            <img src="{img_beagle_scout}" alt="Beagle Scout" style="width: 28px; height: 32px; object-fit: contain;" />
            <span class="card-title">我的待办清单 · To-Do List</span>
            <span class="persona-tag">🏕️ Beagle Scout · 探索与前行</span>
          </div>
          <button class="btn btn-primary" onclick="openTodoModal()">+ 新建待办事项</button>
        </div>
        <div class="card-body">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; flex-wrap:wrap; gap:8px;">
            <div style="display:flex; gap:6px;">
              <button class="btn btn-sm" onclick="filterTodos('all', this)" id="todoTabAll" style="font-weight:700;">全部</button>
              <button class="btn btn-sm" onclick="filterTodos('pending', this)">进行中</button>
              <button class="btn btn-sm" onclick="filterTodos('completed', this)">已完成</button>
              <button class="btn btn-sm" onclick="filterTodos('high', this)">🔴 加急高优</button>
            </div>
            <div style="font-size:12px; color:var(--text-muted);" id="todoStatsText">0 项任务</div>
          </div>
          <div id="fullTodoList"></div>
        </div>
      </div>
    </div>


    <!-- ================= 3. SUPERVISOR REQUIREMENTS (🕵️ Head Beagle · “比格犬长官”) ================= -->
    <div class="tab-pane" id="pane-supervisor">
      <div class="card">
        <div class="card-header">
          <div style="display:flex; align-items:center; gap:9px;">
            <img src="{img_head_beagle}" alt="Head Beagle" style="width: 26px; height: 34px; object-fit: contain;" />
            <span class="card-title">主管要求与核心指示追踪</span>
            <span class="persona-tag">🕵️ Head Beagle · 严谨跟进与落实</span>
          </div>
          <button class="btn btn-primary" onclick="openReqModal()">+ 录入新指示</button>
        </div>
        <div class="card-body">
          <div style="display:flex; gap:6px; margin-bottom:16px; flex-wrap:wrap;">
            <button class="btn btn-sm" onclick="filterReqs('all', this)" id="reqTabAll" style="font-weight:700;">全部指示</button>
            <button class="btn btn-sm" onclick="filterReqs('pending', this)">待处理</button>
            <button class="btn btn-sm" onclick="filterReqs('progress', this)">推进中</button>
            <button class="btn btn-sm" onclick="filterReqs('done', this)">已完成 / 已汇报</button>
          </div>
          <div id="fullReqList"></div>
        </div>
      </div>
    </div>


    <!-- ================= 4. TIMEZONES (🪖 Flying Ace · 一战飞行王牌) ================= -->
    <div class="tab-pane" id="pane-timezone">

      <!-- Egypt Base Banner with Flying Ace -->
      <div class="tz-base-banner">
        <div>
          <div class="tz-base-title">
            <span>🇪🇬 开罗 · 埃及代表处</span>
            <span class="tz-base-badge">基准时区 UTC+2</span>
            <span class="persona-tag" style="background:rgba(255,255,255,0.15); color:#fff; border-color:rgba(255,255,255,0.2);">🪖 Flying Ace 领航</span>
          </div>
          <p style="font-size:12px; color:#a1a1aa; margin-top:4px;">
            精准校准非洲 8 个代表处与开罗基准时差，高效统筹跨区协作
          </p>
        </div>

        <div style="display:flex; align-items:center; gap:20px;">
          <div style="text-align:right;">
            <div class="tz-base-time" id="cairoBigTime">00:00:00</div>
            <div style="font-size:11px; color:#a1a1aa;" id="cairoBigDate">--</div>
          </div>
          <img src="{img_flying_ace}" alt="Flying Ace Snoopy" style="width: 58px; height: 50px; object-fit: contain; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.5));" />
        </div>
      </div>

      <!-- 8 Offices Timezone Cards -->
      <div class="tz-grid" id="fullTimezoneGrid"></div>

      <!-- Meeting Planner -->
      <div class="card" style="margin-top:20px; background:var(--card-subtle);">
        <div class="card-body" style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
          <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:20px;">🕒</span>
            <div>
              <div style="font-size:13px; font-weight:700;">跨区例会时间推演换算器</div>
              <div style="font-size:11px; color:var(--text-muted);">选择开罗开会时间，实时计算各代表处的对应本地时刻</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:12px; font-weight:600;">开罗开会时间：</span>
            <select id="meetingHourSelect" class="form-control" style="width:130px;" onchange="renderTimezones()">
              <option value="9">09:00</option>
              <option value="10" selected>10:00 (上午例会)</option>
              <option value="11">11:00</option>
              <option value="14">14:00 (下午例会)</option>
              <option value="15">15:00</option>
              <option value="16">16:00</option>
            </select>
          </div>
        </div>
      </div>

    </div>


    <!-- ================= 5. DAILY NOTES (✍️ World Famous Author · 世界著名作家) ================= -->
    <div class="tab-pane" id="pane-notes">
      <div class="card">
        <div class="card-header">
          <div style="display:flex; align-items:center; gap:9px;">
            <img src="{img_author}" alt="World Famous Author" style="width: 28px; height: 32px; object-fit: contain;" />
            <span class="card-title">每日笔记 · 工作纪要与闪光灵感</span>
            <span class="persona-tag">✍️ World Famous Author</span>
          </div>
        </div>
        <div class="card-body">
          <textarea id="noteInput" class="form-control" placeholder="“It was a dark and stormy night...” 敲下今天的工作纪要、电话备忘、或灵感想法... (支持换行)"></textarea>
          <div style="display:flex; justify-content:flex-end; margin-top:10px;">
            <button class="btn btn-primary" onclick="addNote()">保存笔记 ✍️</button>
          </div>
        </div>
      </div>

      <div class="notes-grid" id="fullNotesGrid"></div>
    </div>


    <!-- ================= 6. POMODORO (😎 Joe Cool · 戴墨镜的酷狗) ================= -->
    <div class="tab-pane" id="pane-pomodoro">
      <div class="card">
        <div class="card-body">
          <div class="pomo-container">
            <div class="pomo-illustration" id="pomoIllustrationBox">
              <img id="pomoImg" src="{img_joe_cool}" alt="Joe Cool" />
            </div>

            <div style="font-size:12px; letter-spacing:2px; font-weight:700; color:var(--text-muted);" id="pomoLabel">
              😎 JOE COOL FOCUS TIME · 沉稳专注
            </div>

            <div class="pomo-time" id="pomoTimeText">25:00</div>

            <div style="display:flex; justify-content:center; gap:8px; margin-bottom:18px; flex-wrap:wrap;">
              <button class="btn btn-sm" onclick="setPomoMinutes(25)">25 分钟 (经典专注)</button>
              <button class="btn btn-sm" onclick="setPomoMinutes(15)">15 分钟 (轻度推进)</button>
              <button class="btn btn-sm" onclick="setPomoMinutes(5)">5 分钟 (小憩休整)</button>
            </div>

            <div style="display:flex; justify-content:center; gap:10px;">
              <button class="btn btn-red" id="pomoStartBtn" onclick="togglePomo()" style="min-width:120px;">
                ▶ 开始专注
              </button>
              <button class="btn" onclick="resetPomo()">↻ 重置</button>
            </div>

            <div class="pomo-quote-bubble" id="pomoQuote">
              “保持冷静与从容，像 Joe Cool 一样泰然自若地攻克每一个挑战。” 😎
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- ================= 7. QUICK LINKS (🎨 艺术家 / 幻想中的 Snoopy) ================= -->
    <div class="tab-pane" id="pane-links">
      <div class="card">
        <div class="card-header">
          <div style="display:flex; align-items:center; gap:9px;">
            <img src="{img_artist_dream}" alt="Artist Snoopy" style="width: 32px; height: 26px; object-fit: contain;" />
            <span class="card-title">常用工作链接与资源导航</span>
            <span class="persona-tag">🎨 Daydreamer · 漫游与连接</span>
          </div>
          <button class="btn btn-primary" onclick="openLinkModal()">+ 添加新链接</button>
        </div>
        <div class="card-body">
          <div class="links-grid" id="fullLinksGrid"></div>
        </div>
      </div>
    </div>

  </main>


  <!-- Footer -->
  <footer class="app-footer">
    <div class="footer-inner">
      <div style="display:flex; align-items:center; gap:12px;">
        <img src="{img_ordinary_doghouse}" alt="Snoopy" style="height: 24px; width: auto; object-fit: contain; opacity: 0.9;" />
        <span>Snoopy’s Little Lab · Happiness is a productive day.</span>
      </div>
      <div>
        <button class="btn btn-ghost btn-sm" onclick="exportDataJSON()">📦 备份所有数据 (JSON)</button>
      </div>
    </div>
  </footer>


  <!-- ================= MODALS ================= -->

  <!-- Todo Modal -->
  <div class="modal-overlay" id="todoModal">
    <div class="modal-box">
      <div class="modal-header">
        <h3 style="font-size:15px; font-weight:700; display:flex; align-items:center; gap:8px;">
          <img src="{img_beagle_scout}" alt="Beagle Scout" style="width:24px;height:24px;object-fit:contain;" />
          <span>新建待办事项</span>
        </h3>
        <button class="btn btn-icon btn-ghost" onclick="closeModal('todoModal')">✕</button>
      </div>
      <div class="modal-body">
        <div>
          <label style="font-size:12px; font-weight:600; margin-bottom:4px; display:block;">任务内容 *</label>
          <input type="text" id="inputTodoText" class="form-control" placeholder="例如：给刚果（金）代表处发送财务复核表..." />
        </div>
        <div>
          <label style="font-size:12px; font-weight:600; margin-bottom:4px; display:block;">优先级</label>
          <select id="inputTodoPriority" class="form-control">
            <option value="medium">🟡 中等优先级</option>
            <option value="high">🔴 高优先级 (加急)</option>
            <option value="low">⚪ 低优先级</option>
          </select>
        </div>
        <div>
          <label style="font-size:12px; font-weight:600; margin-bottom:4px; display:block;">截止日期 (可选)</label>
          <input type="date" id="inputTodoDueDate" class="form-control" />
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn" onclick="closeModal('todoModal')">取消</button>
        <button class="btn btn-primary" onclick="addTodo()">确认保存</button>
      </div>
    </div>
  </div>

  <!-- Supervisor Requirement Modal -->
  <div class="modal-overlay" id="reqModal">
    <div class="modal-box">
      <div class="modal-header">
        <h3 style="font-size:15px; font-weight:700; display:flex; align-items:center; gap:8px;">
          <img src="{img_head_beagle}" alt="Head Beagle" style="width:22px;height:28px;object-fit:contain;" />
          <span>记录主管要求与指示</span>
        </h3>
        <button class="btn btn-icon btn-ghost" onclick="closeModal('reqModal')">✕</button>
      </div>
      <div class="modal-body">
        <div>
          <label style="font-size:12px; font-weight:600; margin-bottom:4px; display:block;">要求内容 *</label>
          <textarea id="inputReqContent" class="form-control" placeholder="详细记录主管的交付要求、具体指标与重点事项..."></textarea>
        </div>
        <div>
          <label style="font-size:12px; font-weight:600; margin-bottom:4px; display:block;">提出主管 / 负责人</label>
          <input type="text" id="inputReqSource" class="form-control" placeholder="例如：区域总监 / 张总" />
        </div>
        <div>
          <label style="font-size:12px; font-weight:600; margin-bottom:4px; display:block;">当前状态</label>
          <select id="inputReqStatus" class="form-control">
            <option value="progress">推进中</option>
            <option value="pending">待处理</option>
            <option value="done">已完成 / 已汇报</option>
          </select>
        </div>
        <div>
          <label style="font-size:12px; font-weight:600; margin-bottom:4px; display:block;">截止期限 (可选)</label>
          <input type="date" id="inputReqDueDate" class="form-control" />
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn" onclick="closeModal('reqModal')">取消</button>
        <button class="btn btn-primary" onclick="addReq()">确认保存</button>
      </div>
    </div>
  </div>

  <!-- Link Modal -->
  <div class="modal-overlay" id="linkModal">
    <div class="modal-box">
      <div class="modal-header">
        <h3 style="font-size:15px; font-weight:700; display:flex; align-items:center; gap:8px;">
          <img src="{img_artist_dream}" alt="Artist Snoopy" style="width:24px;height:24px;object-fit:contain;" />
          <span>添加常用链接</span>
        </h3>
        <button class="btn btn-icon btn-ghost" onclick="closeModal('linkModal')">✕</button>
      </div>
      <div class="modal-body">
        <div>
          <label style="font-size:12px; font-weight:600; margin-bottom:4px; display:block;">链接名称 *</label>
          <input type="text" id="inputLinkName" class="form-control" placeholder="例如：区域工作邮箱" />
        </div>
        <div>
          <label style="font-size:12px; font-weight:600; margin-bottom:4px; display:block;">网址 URL *</label>
          <input type="text" id="inputLinkUrl" class="form-control" placeholder="https://..." />
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn" onclick="closeModal('linkModal')">取消</button>
        <button class="btn btn-primary" onclick="addLink()">确认添加</button>
      </div>
    </div>
  </div>


<!-- ================= JAVASCRIPT ================= -->
<script>
const SNOOPY_ASSETS = {{
  ordinary_doghouse: "{img_ordinary_doghouse}",
  author: "{img_author}",
  flying_ace: "{img_flying_ace}",
  joe_cool: "{img_joe_cool}",
  beagle_scout: "{img_beagle_scout}",
  head_beagle: "{img_head_beagle}",
  artist_dream: "{img_artist_dream}",
  woodstock: "{img_woodstock}",
  dance: "{img_dance}",
  canonical: "{img_canonical}"
}};

const STORAGE_KEYS = {{
  TODOS: 'snoopy_todos_v5',
  REQS: 'snoopy_reqs_v5',
  NOTES: 'snoopy_notes_v5',
  LINKS: 'snoopy_links_v5',
  THEME: 'snoopy_theme_v5'
}};

// Charles M. Schulz Quotations (31 Daily Literary & Philosophical Quotes, automatically updated once per day)
const SNOOPY_PHILOSOPHIES = [
  {{
    en: "“Keep looking up... that's the secret of life.”",
    cn: "「永远抬头向上看…… 这便是生活的秘诀。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Happiness is a warm puppy.”",
    cn: "「幸福，就是一只温暖的小狗。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Learn from yesterday, live for today, look to tomorrow, rest this afternoon.”",
    cn: "「汲取昨天的经验，活在今天的当下，憧憬明天的美好，今天下午先小憩一下。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“In the book of life, the answers aren't in the back.”",
    cn: "「在人生的这一本书里，答案从不写在最后一页。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Be yourself. No one can say you're doing it wrong.”",
    cn: "「做真实的自己。没有人能对你的热爱指手画脚。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“It does not matter where you go in life, it is who you have beside you.”",
    cn: "「漫漫旅途中去往何方并不重要，重要的是同行于身侧的人。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Each morning is a clean sheet of paper, ready for new stories.”",
    cn: "「每一个清晨都是一张崭新的稿纸，正等待书写新的故事。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“My life has no direction, no aim, no meaning, and yet I'm happy.”",
    cn: "「我的生活没有既定的刻板航向，但我依然快乐而满足。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“All you need is love. But a little chocolate now and then doesn't hurt.”",
    cn: "「人人都需要爱，但偶尔来一点巧克力也绝不是坏事。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“A day without a nap is like a cupcake without frosting.”",
    cn: "「没有午休的一天，就像没有糖霜的纸杯蛋糕。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“You can't think about anything on an empty stomach.”",
    cn: "「不能空着肚子思考问题，从容享受一顿美餐吧。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Just remember, when you're over the hill, you begin to pick up speed.”",
    cn: "「翻过山巅之后，步伐便会愈加轻快从容。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Keep your face to the sunshine and you cannot see a shadow.”",
    cn: "「让脸庞向着阳光，阴影便会自然落到身后。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Don't worry about today. Tomorrow is already starting somewhere bright.”",
    cn: "「别为今日琐事忧虑，世界的某个角落早已迎来了崭新的朝阳。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Life is like an ice cream cone, you have to lick it one day at a time.”",
    cn: "「生活就像甜筒冰淇淋，需要一天一口细细品味。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Focus on today's breeze; let tomorrow's clouds take care of themselves.”",
    cn: "「专注感受今日的微风；明天的云彩自有其安放之处。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Good advice doesn't cost anything, but following it makes all the difference.”",
    cn: "「倾听善意的指引，脚踏实地，步步生花。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Small steps each day lead to grand adventures over time.”",
    cn: "「每日跨出的一小步，日积月累终将汇聚成壮阔的冒险。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Rest when you're weary. Refresh and renew yourself, your body, your mind.”",
    cn: "「感到疲惫时就安心休憩，蓄满能量后再轻盈出发。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Sometimes it’s nice just to lie on the roof and think of peaceful skies.”",
    cn: "「有时，只是静静趴在屋顶上凝望晴空，也是莫大的惬意。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Clarity in thought brings ease in every stride.”",
    cn: "「思绪清晰，落笔从容，每一步都能走得轻快坚定。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“There is nothing more attractive than a warm smile and a calm heart.”",
    cn: "「没有什么比真挚的微笑与笃定的内心更有力量。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“To live is to dance, to dance is to celebrate every little joy.”",
    cn: "「热爱生活，保持律动，就像在青草地上轻快起舞。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Big journeys begin with a steady heart and a loyal companion.”",
    cn: "「远大航程始于沉稳的内心，以及身旁值得信赖的伙伴。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“The world is full of possibilities when you greet it with kindness.”",
    cn: "「以善意与温情拥抱清晨，世界便处处皆是无限可能。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Take a deep breath. Every knot has a way of undoing itself.”",
    cn: "「遇事先深呼吸，放平心态，繁杂的谜团自会迎刃而解。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Nothing clears the mind like a fresh gentle breeze upon the roof.”",
    cn: "「没有什么比屋顶的一缕清风更能抚平心中的喧嚣。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“A little curiosity keeps an ordinary workday sparkling.”",
    cn: "「保持一点纯真的好奇心，能让平淡的工作日闪闪发光。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“To love your craft and find delight in quiet focus is pure joy.”",
    cn: "「沉浸于眼前的专注，在静谧中收获踏实的从容与喜悦。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Count your joys as you would the stars on a clear night.”",
    cn: "「像数清朗夜空的繁星那样，细数身边的每一份微小确幸。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }},
  {{
    en: "“Tomorrow is waiting with open arms; finish today with pride.”",
    cn: "「明天正敞开怀抱等待，带着今日的从容与收获安心入眠。」",
    author: "—— Charles M. Schulz ·《Peanuts》"
  }}
];

// Automatically update daily quote deterministically based on date (每天自动根据日期更新)
function initDailyQuote() {{
  const now = new Date();
  const m = now.getMonth() + 1;
  const d = now.getDate();
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  const wk = weekdays[now.getDay()];

  // Calculate day of the year for deterministic daily quote rotation
  const startOfYear = new Date(now.getFullYear(), 0, 0);
  const diff = now - startOfYear;
  const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24));
  const quoteIndex = dayOfYear % SNOOPY_PHILOSOPHIES.length;
  const item = SNOOPY_PHILOSOPHIES[quoteIndex];

  const qEl = document.getElementById('heroQuoteText');
  const cnEl = document.getElementById('heroQuoteCn');
  const aEl = document.getElementById('heroQuoteAuthor');
  const pillEl = document.getElementById('heroDailyDatePill');

  if (qEl) qEl.textContent = item.en;
  if (cnEl) cnEl.textContent = item.cn;
  if (aEl) aEl.textContent = item.author;
  if (pillEl) pillEl.textContent = '✦ Snoopy’s Little Lab · ' + m + '月' + d + '日 ' + wk + ' · 每日哲思';
}}

function getData(k, fallback = []) {{
  try {{ return JSON.parse(localStorage.getItem(k)) || fallback; }}
  catch {{ return fallback; }}
}}

function setData(k, d) {{
  localStorage.setItem(k, JSON.stringify(d));
}}

// 8 Regional Offices (Africa) + Cairo Base
const OFFICES = [
  {{ city: '阿尔及尔', country: '阿尔及利亚代表处 🇩🇿', tz: 'Africa/Algiers' }},
  {{ city: '的黎波里', country: '地中海南代表处 🇱🇾', tz: 'Africa/Tripoli' }},
  {{ city: '金沙萨', country: '刚果（金）代表处 🇨🇩', tz: 'Africa/Kinshasa' }},
  {{ city: '杜阿拉', country: '喀麦隆代表处 🇨🇲', tz: 'Africa/Douala' }},
  {{ city: '阿比让', country: '科特迪瓦代表处 🇨🇮', tz: 'Africa/Abidjan' }},
  {{ city: '卡萨布兰卡', country: '摩洛哥代表处 🇲🇦', tz: 'Africa/Casablanca' }},
  {{ city: '达喀尔', country: '塞内加尔代表处 🇸🇳', tz: 'Africa/Dakar' }}
];

function getOffsetMinutes(tz, date) {{
  try {{
    const parts = new Intl.DateTimeFormat('en-US', {{
      timeZone: tz,
      timeZoneName: 'longOffset'
    }}).formatToParts(date);
    const offsetPart = parts.find(p => p.type === 'timeZoneName');
    if (!offsetPart) return 0;
    const match = offsetPart.value.match(/GMT([+-]?)(\\d{{1,2}}):?(\\d{{2}})?/);
    if (!match) return 0;
    const sign = match[1] === '-' ? -1 : 1;
    const hours = parseInt(match[2]) || 0;
    const minutes = parseInt(match[3]) || 0;
    return sign * (hours * 60 + minutes);
  }} catch {{ return 0; }}
}}

function getDiffAgainstCairo(tz) {{
  const now = new Date();
  const cairoOffset = getOffsetMinutes('Africa/Cairo', now);
  const targetOffset = getOffsetMinutes(tz, now);
  return (targetOffset - cairoOffset) / 60;
}}

function getWorkStatus(tzDate) {{
  const hour = tzDate.getHours();
  const min = tzDate.getMinutes();
  const timeVal = hour + min / 60;
  const day = tzDate.getDay();
  if (day === 0 || day === 6) return {{ text: '周末休息', cls: 'ws-off' }};
  if (timeVal >= 8.5 && timeVal < 12.5) return {{ text: '工作中 🟢', cls: 'ws-work' }};
  if (timeVal >= 12.5 && timeVal < 14) return {{ text: '午休中 ☕', cls: 'ws-lunch' }};
  if (timeVal >= 14 && timeVal <= 17.5) return {{ text: '工作中 🟢', cls: 'ws-work' }};
  if (timeVal < 8.5) return {{ text: '未上班 🌙', cls: 'ws-off' }};
  return {{ text: '已下班 🏠', cls: 'ws-off' }};
}}

// Tab Switching
function switchTab(tab) {{
  document.querySelectorAll('.nav-tab').forEach(b => b.classList.toggle('active', b.dataset.tab === tab));
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.toggle('active', p.id === `pane-${{tab}}`));
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

// Clocks & Timezones
function renderTimezones() {{
  const now = new Date();

  // Cairo Base
  const cairoTime = now.toLocaleTimeString('zh-CN', {{ timeZone: 'Africa/Cairo', hour12: false }});
  const cairoDate = now.toLocaleDateString('zh-CN', {{ timeZone: 'Africa/Cairo', year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }});

  const headerClock = document.getElementById('headerCairoClock');
  if (headerClock) headerClock.textContent = cairoTime;
  const bigTime = document.getElementById('cairoBigTime');
  const bigDate = document.getElementById('cairoBigDate');
  if (bigTime) bigTime.textContent = cairoTime;
  if (bigDate) bigDate.textContent = cairoDate;

  const simSelect = document.getElementById('meetingHourSelect');
  const simCairoHour = simSelect ? parseInt(simSelect.value) : 10;

  // Full Grid
  const grid = document.getElementById('fullTimezoneGrid');
  if (grid) {{
    grid.innerHTML = OFFICES.map(o => {{
      const diff = getDiffAgainstCairo(o.tz);
      const diffText = diff === 0 ? '同区 0h' : (diff > 0 ? `+${{diff}}h` : `${{diff}}h`);
      const oDate = new Date(now.toLocaleString('en-US', {{ timeZone: o.tz }}));
      const timeStr = now.toLocaleTimeString('zh-CN', {{ timeZone: o.tz, hour: '2-digit', minute: '2-digit', hour12: false }});
      const status = getWorkStatus(oDate);
      const simHour = (simCairoHour + diff + 24) % 24;

      return `
        <div class="tz-card">
          <div class="tz-card-top">
            <span class="tz-card-name">${{o.country}}</span>
            <span class="tz-pill ${{diff === 0 ? 'same' : ''}}">${{diffText}}</span>
          </div>
          <div style="font-size:11px; color:var(--text-muted);">${{o.city}} · ${{o.tz}}</div>
          <div class="tz-time">${{timeStr}}</div>
          <div class="tz-card-bottom">
            <span class="work-status ${{status.cls}}">${{status.text}}</span>
            <span style="color:var(--text-secondary);">例会对齐: ${{String(simHour).padStart(2,'0')}}:00</span>
          </div>
        </div>
      `;
    }}).join('');
  }}

  // Dashboard Mini List
  const dashList = document.getElementById('dashTimeList');
  if (dashList) {{
    dashList.innerHTML = OFFICES.map(o => {{
      const diff = getDiffAgainstCairo(o.tz);
      const diffText = diff === 0 ? '同区' : (diff > 0 ? `+${{diff}}h` : `${{diff}}h`);
      const timeStr = now.toLocaleTimeString('zh-CN', {{ timeZone: o.tz, hour: '2-digit', minute: '2-digit', hour12: false }});
      return `
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; padding:6px 0; border-bottom:1px solid var(--border);">
          <span style="font-weight:600;">${{o.country}}</span>
          <div style="display:flex; gap:10px; font-family:var(--font-mono);">
            <span style="color:var(--text-muted); font-size:11px;">${{diffText}}</span>
            <strong>${{timeStr}}</strong>
          </div>
        </div>
      `;
    }}).join('');
  }}
}}

// Todos (🏕️ Beagle Scout)
let currentTodoFilter = 'all';

function filterTodos(f, btn) {{
  currentTodoFilter = f;
  renderTodos();
}}

function renderTodos() {{
  const todos = getData(STORAGE_KEYS.TODOS);
  let filtered = [...todos];
  if (currentTodoFilter === 'pending') filtered = filtered.filter(t => !t.completed);
  else if (currentTodoFilter === 'completed') filtered = filtered.filter(t => t.completed);
  else if (currentTodoFilter === 'high') filtered = filtered.filter(t => t.priority === 'high');

  const pending = todos.filter(t => !t.completed).length;
  document.getElementById('todoDot').style.display = pending > 0 ? 'inline-block' : 'none';
  document.getElementById('todoStatsText').textContent = `共 ${{todos.length}} 项 (进行中 ${{pending}})`;

  const list = document.getElementById('fullTodoList');
  if (list) {{
    if (filtered.length === 0) {{
      list.innerHTML = `
        <div style="text-align:center; padding:36px; color:var(--text-muted); font-size:13px;">
          <img src="${{SNOOPY_ASSETS.beagle_scout}}" alt="Beagle Scout" style="width: 70px; height: 90px; object-fit: contain; margin-bottom: 8px; opacity: 0.9;" />
          <p>全部任务已搞定！Beagle Scout 正在整理行囊，准备下一次探险~</p>
        </div>
      `;
    }} else {{
      const prioNames = {{ high: '加急高优', medium: '普通', low: '低优' }};
      list.innerHTML = filtered.map(t => `
        <div class="todo-item ${{t.completed ? 'completed' : ''}}">
          <div class="todo-chk" onclick="toggleTodo(${{t.id}})"></div>
          <div class="todo-content">
            <div class="todo-text">${{escapeHtml(t.text)}}</div>
            <div class="todo-meta">
              <span class="prio-pill prio-${{t.priority}}">${{prioNames[t.priority] || '普通'}}</span>
              ${{t.dueDate ? `<span>📅 截止: ${{t.dueDate}}</span>` : ''}}
            </div>
          </div>
          <button class="btn btn-icon btn-ghost btn-sm" onclick="deleteTodo(${{t.id}})">🗑</button>
        </div>
      `).join('');
    }}
  }}

  // Dashboard preview
  const dashList = document.getElementById('dashTodoList');
  if (dashList) {{
    const uncompleted = todos.filter(t => !t.completed).slice(0, 4);
    if (uncompleted.length === 0) {{
      dashList.innerHTML = `
        <div style="text-align:center; padding:20px; color:var(--text-muted); font-size:12px;">
          <img src="${{SNOOPY_ASSETS.dance}}" alt="Snoopy" style="width: 50px; height: 50px; object-fit: contain; margin-bottom: 4px;" />
          <p>今日待办全部完成，太棒了！</p>
        </div>
      `;
    }} else {{
      dashList.innerHTML = uncompleted.map(t => `
        <div class="todo-item" style="margin-bottom:6px; padding:8px 10px;">
          <div class="todo-chk" onclick="toggleTodo(${{t.id}})"></div>
          <div class="todo-content">
            <div class="todo-text" style="font-size:12.5px;">${{escapeHtml(t.text)}}</div>
          </div>
        </div>
      `).join('');
    }}
  }}
}}

function openTodoModal() {{
  document.getElementById('inputTodoText').value = '';
  document.getElementById('inputTodoPriority').value = 'medium';
  document.getElementById('inputTodoDueDate').value = '';
  openModal('todoModal');
  setTimeout(() => document.getElementById('inputTodoText').focus(), 50);
}}

function addTodo() {{
  const text = document.getElementById('inputTodoText').value.trim();
  if (!text) return;
  const todos = getData(STORAGE_KEYS.TODOS);
  todos.unshift({{
    id: Date.now(),
    text,
    priority: document.getElementById('inputTodoPriority').value,
    dueDate: document.getElementById('inputTodoDueDate').value,
    completed: false
  }});
  setData(STORAGE_KEYS.TODOS, todos);
  closeModal('todoModal');
  renderTodos();
}}

function toggleTodo(id) {{
  const todos = getData(STORAGE_KEYS.TODOS);
  const t = todos.find(item => item.id === id);
  if (t) t.completed = !t.completed;
  setData(STORAGE_KEYS.TODOS, todos);
  renderTodos();
}}

function deleteTodo(id) {{
  let todos = getData(STORAGE_KEYS.TODOS);
  todos = todos.filter(t => t.id !== id);
  setData(STORAGE_KEYS.TODOS, todos);
  renderTodos();
}}

// Supervisor Requirements (🕵️ Head Beagle)
let currentReqFilter = 'all';

function filterReqs(f, btn) {{
  currentReqFilter = f;
  renderReqs();
}}

function renderReqs() {{
  const reqs = getData(STORAGE_KEYS.REQS);
  let filtered = [...reqs];
  if (currentReqFilter !== 'all') filtered = filtered.filter(r => r.status === currentReqFilter);

  const active = reqs.filter(r => r.status !== 'done').length;
  document.getElementById('reqDot').style.display = active > 0 ? 'inline-block' : 'none';

  const statusMap = {{
    pending: {{ label: '待处理', cls: 'rst-pending' }},
    progress: {{ label: '推进中', cls: 'rst-progress' }},
    done: {{ label: '已完成 / 已汇报', cls: 'rst-done' }}
  }};

  const list = document.getElementById('fullReqList');
  if (list) {{
    if (filtered.length === 0) {{
      list.innerHTML = `
        <div style="text-align:center; padding:36px; color:var(--text-muted); font-size:13px;">
          <img src="${{SNOOPY_ASSETS.head_beagle}}" alt="Head Beagle" style="width: 54px; height: 75px; object-fit: contain; margin-bottom: 8px; opacity: 0.9;" />
          <p>暂无主管指示记录。Head Beagle 视察完毕，一切井然有序！</p>
        </div>
      `;
    }} else {{
      list.innerHTML = filtered.map(r => {{
        const s = statusMap[r.status] || statusMap.pending;
        return `
          <div class="req-item ${{r.status === 'done' ? 'done' : ''}}">
            <div class="req-header">
              <span class="req-status-tag ${{s.cls}}">${{s.label}}</span>
              <div style="display:flex; gap:6px;">
                <select class="form-control" style="font-size:11px; padding:2px 6px; width:auto;" onchange="updateReqStatus(${{r.id}}, this.value)">
                  <option value="progress" ${{r.status === 'progress' ? 'selected' : ''}}>推进中</option>
                  <option value="pending" ${{r.status === 'pending' ? 'selected' : ''}}>待处理</option>
                  <option value="done" ${{r.status === 'done' ? 'selected' : ''}}>已完成</option>
                </select>
                <button class="btn btn-icon btn-ghost btn-sm" onclick="deleteReq(${{r.id}})">🗑</button>
              </div>
            </div>
            <div class="req-body">${{escapeHtml(r.content)}}</div>
            <div class="req-footer">
              <span>👤 提出人: <strong>${{escapeHtml(r.source || '主管')}}</strong></span>
              ${{r.dueDate ? `<span style="color:var(--accent-red); font-weight:700;">⏰ 截止: ${{r.dueDate}}</span>` : ''}}
            </div>
          </div>
        `;
      }}).join('');
    }}
  }}

  // Dashboard preview
  const dashReq = document.getElementById('dashReqList');
  if (dashReq) {{
    const actives = reqs.filter(r => r.status !== 'done').slice(0, 2);
    if (actives.length === 0) {{
      dashReq.innerHTML = `<div style="text-align:center; padding:18px; color:var(--text-muted); font-size:12px;">各项指示均已落实汇报完毕！</div>`;
    }} else {{
      dashReq.innerHTML = actives.map(r => {{
        const s = statusMap[r.status] || statusMap.pending;
        return `
          <div class="req-item" style="margin-bottom:8px; padding:10px 12px;">
            <div class="req-header" style="margin-bottom:4px;">
              <span class="req-status-tag ${{s.cls}}" style="font-size:10px;">${{s.label}}</span>
              <span style="font-size:11px; color:var(--text-muted);">👤 ${{escapeHtml(r.source)}}</span>
            </div>
            <div style="font-size:13px; font-weight:500;">${{escapeHtml(r.content)}}</div>
          </div>
        `;
      }}).join('');
    }}
  }}
}}

function openReqModal() {{
  document.getElementById('inputReqContent').value = '';
  document.getElementById('inputReqSource').value = '';
  document.getElementById('inputReqStatus').value = 'progress';
  document.getElementById('inputReqDueDate').value = '';
  openModal('reqModal');
  setTimeout(() => document.getElementById('inputReqContent').focus(), 50);
}}

function addReq() {{
  const content = document.getElementById('inputReqContent').value.trim();
  if (!content) return;
  const reqs = getData(STORAGE_KEYS.REQS);
  reqs.unshift({{
    id: Date.now(),
    content,
    source: document.getElementById('inputReqSource').value.trim() || '主管',
    status: document.getElementById('inputReqStatus').value,
    dueDate: document.getElementById('inputReqDueDate').value
  }});
  setData(STORAGE_KEYS.REQS, reqs);
  closeModal('reqModal');
  renderReqs();
}}

function updateReqStatus(id, st) {{
  const reqs = getData(STORAGE_KEYS.REQS);
  const r = reqs.find(item => item.id === id);
  if (r) r.status = st;
  setData(STORAGE_KEYS.REQS, reqs);
  renderReqs();
}}

function deleteReq(id) {{
  let reqs = getData(STORAGE_KEYS.REQS);
  reqs = reqs.filter(r => r.id !== id);
  setData(STORAGE_KEYS.REQS, reqs);
  renderReqs();
}}

// Notes (✍️ World Famous Author)
function renderNotes() {{
  const notes = getData(STORAGE_KEYS.NOTES);
  const grid = document.getElementById('fullNotesGrid');
  if (!grid) return;
  if (notes.length === 0) {{
    grid.innerHTML = `
      <div style="grid-column:1/-1; text-align:center; padding:36px; color:var(--text-muted);">
        <img src="${{SNOOPY_ASSETS.author}}" alt="Author Snoopy" style="width: 60px; height: 70px; object-fit: contain; margin-bottom: 8px; opacity: 0.9;" />
        <p>还没有记录笔记，打字机已经就绪，敲下今天的第一条灵感吧~</p>
      </div>
    `;
    return;
  }}
  grid.innerHTML = notes.map(n => `
    <div class="note-card">
      <div class="note-text">${{escapeHtml(n.text)}}</div>
      <div class="note-foot">
        <span>🕒 ${{n.time}}</span>
        <button class="btn btn-icon btn-ghost btn-sm" onclick="deleteNote(${{n.id}})">🗑</button>
      </div>
    </div>
  `).join('');
}}

function addNote() {{
  const input = document.getElementById('noteInput');
  const text = input.value.trim();
  if (!text) return;
  const notes = getData(STORAGE_KEYS.NOTES);
  notes.unshift({{
    id: Date.now(),
    text,
    time: new Date().toLocaleTimeString('zh-CN', {{ hour: '2-digit', minute: '2-digit' }})
  }});
  setData(STORAGE_KEYS.NOTES, notes);
  input.value = '';
  renderNotes();
}}

function deleteNote(id) {{
  let notes = getData(STORAGE_KEYS.NOTES);
  notes = notes.filter(n => n.id !== id);
  setData(STORAGE_KEYS.NOTES, notes);
  renderNotes();
}}

// Pomodoro Focus Timer (😎 Joe Cool)
let pomoSecs = 25 * 60;
let pomoRunning = false;
let pomoTimer = null;

function playChime() {{
  try {{
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
    osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.3); // A5
    gain.gain.setValueAtTime(0.3, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.8);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.8);
  }} catch(e) {{}}
}}

function setPomoMinutes(mins) {{
  pomoSecs = mins * 60;
  pomoRunning = false;
  clearInterval(pomoTimer);
  document.getElementById('pomoStartBtn').innerHTML = '▶ 开始专注';
  document.getElementById('pomoLabel').textContent = mins <= 5 ? 'REST TIME · 稍事休息' : '😎 JOE COOL FOCUS TIME · 沉稳专注';
  document.getElementById('pomoImg').src = SNOOPY_ASSETS.joe_cool;
  updatePomo();
}}

function togglePomo() {{
  const btn = document.getElementById('pomoStartBtn');
  if (pomoRunning) {{
    pomoRunning = false;
    clearInterval(pomoTimer);
    btn.innerHTML = '▶ 继续专注';
  }} else {{
    pomoRunning = true;
    btn.innerHTML = '⏸ 暂停';
    pomoTimer = setInterval(() => {{
      pomoSecs--;
      if (pomoSecs <= 0) {{
        clearInterval(pomoTimer);
        pomoRunning = false;
        pomoSecs = 0;
        btn.innerHTML = '▶ 开始专注';
        document.getElementById('pomoImg').src = SNOOPY_ASSETS.dance;
        playChime();
        alert('🐾 叮！专注时钟已圆满完成！Snoopy 在为你跳舞喝彩，站起来伸个懒腰吧！');
      }}
      updatePomo();
    }}, 1000);
  }}
}}

function resetPomo() {{
  pomoSecs = 25 * 60;
  pomoRunning = false;
  clearInterval(pomoTimer);
  document.getElementById('pomoStartBtn').innerHTML = '▶ 开始专注';
  document.getElementById('pomoImg').src = SNOOPY_ASSETS.joe_cool;
  updatePomo();
}}

function updatePomo() {{
  const m = Math.floor(pomoSecs / 60);
  const s = pomoSecs % 60;
  document.getElementById('pomoTimeText').textContent =
    `${{String(m).padStart(2,'0')}}:${{String(s).padStart(2,'0')}}`;
}}

// Links (🎨 Artist / Daydreamer)
function renderLinks() {{
  const links = getData(STORAGE_KEYS.LINKS);
  const grid = document.getElementById('fullLinksGrid');
  if (!grid) return;
  if (links.length === 0) {{
    grid.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:36px; color:var(--text-muted);">🔗 还没有添加链接，点击上方按钮添加！</div>`;
    return;
  }}
  grid.innerHTML = links.map(l => `
    <div class="link-card">
      <img src="${{SNOOPY_ASSETS.artist_dream}}" alt="Link" style="width:28px;height:24px;object-fit:contain;" />
      <div style="flex:1; min-width:0;">
        <a href="${{escapeHtml(l.url)}}" target="_blank" style="text-decoration:none; color:inherit;">
          <div style="font-size:13px; font-weight:700;">${{escapeHtml(l.name)}}</div>
          <div style="font-size:11px; color:var(--text-muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${{escapeHtml(l.url)}}</div>
        </a>
      </div>
      <button class="btn btn-icon btn-ghost btn-sm" onclick="deleteLink(${{l.id}})">✕</button>
    </div>
  `).join('');
}}

function openLinkModal() {{
  document.getElementById('inputLinkName').value = '';
  document.getElementById('inputLinkUrl').value = '';
  openModal('linkModal');
}}

function addLink() {{
  const name = document.getElementById('inputLinkName').value.trim();
  let url = document.getElementById('inputLinkUrl').value.trim();
  if (!name || !url) return;
  if (!url.startsWith('http://') && !url.startsWith('https://')) url = 'https://' + url;
  const links = getData(STORAGE_KEYS.LINKS);
  links.push({{ id: Date.now(), name, url }});
  setData(STORAGE_KEYS.LINKS, links);
  closeModal('linkModal');
  renderLinks();
}}

function deleteLink(id) {{
  let links = getData(STORAGE_KEYS.LINKS);
  links = links.filter(l => l.id !== id);
  setData(STORAGE_KEYS.LINKS, links);
  renderLinks();
}}

// Modals
function openModal(id) {{ document.getElementById(id).classList.add('active'); }}
function closeModal(id) {{ document.getElementById(id).classList.remove('active'); }}

// Theme
function toggleTheme() {{
  const isComic = document.body.classList.toggle('theme-comic');
  localStorage.setItem(STORAGE_KEYS.THEME, isComic ? 'comic' : 'modern');
  document.getElementById('themeToggleBtn').textContent = isComic ? '🎨 切换现代极简' : '🎨 切换经典漫画';
}}

function exportDataJSON() {{
  const bundle = {{
    todos: getData(STORAGE_KEYS.TODOS),
    reqs: getData(STORAGE_KEYS.REQS),
    notes: getData(STORAGE_KEYS.NOTES),
    links: getData(STORAGE_KEYS.LINKS)
  }};
  const blob = new Blob([JSON.stringify(bundle, null, 2)], {{ type: 'application/json' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `snoopy_lab_backup_${{new Date().toISOString().slice(0,10)}}.json`;
  a.click();
}}

function escapeHtml(s) {{
  if (!s) return '';
  const div = document.createElement('div');
  div.textContent = s;
  return div.innerHTML;
}}

// Seed initial sample data if empty
function initSeeds() {{
  if (!localStorage.getItem(STORAGE_KEYS.REQS)) {{
    setData(STORAGE_KEYS.REQS, [
      {{ id: 1, content: "整理刚果（金）及地中海南代表处业务周报，周五开罗例会统一汇报。", source: "区域总监", status: "progress", dueDate: "2026-09-25" }},
      {{ id: 2, content: "与科特迪瓦、塞内加尔代表处对齐下季度协作计划（注意 2 小时时差）。", source: "综合运营部", status: "pending", dueDate: "2026-09-24" }}
    ]);
  }}
  if (!localStorage.getItem(STORAGE_KEYS.TODOS)) {{
    setData(STORAGE_KEYS.TODOS, [
      {{ id: 101, text: "核对阿尔及利亚代表处最新提交的报销凭证", priority: "medium", dueDate: "2026-09-23", completed: false }},
      {{ id: 102, text: "拆解并校准喀麦隆、摩洛哥代表处 Q3 关键业务指标", priority: "high", dueDate: "2026-09-24", completed: false }},
      {{ id: 103, text: "分发今日开罗晨会要点及备忘给各代表处接口人", priority: "low", dueDate: "", completed: true }}
    ]);
  }}
  if (!localStorage.getItem(STORAGE_KEYS.LINKS)) {{
    setData(STORAGE_KEYS.LINKS, [
      {{ id: 201, name: "企业海外工作邮箱", url: "https://mail.google.com" }},
      {{ id: 202, name: "非洲业务协同知识库", url: "https://notion.so" }}
    ]);
  }}
  if (!localStorage.getItem(STORAGE_KEYS.NOTES)) {{
    setData(STORAGE_KEYS.NOTES, [
      {{ id: 301, text: "📌 8 代表处时区快速备忘：\\n• 开罗（基准）、地中海南：UTC+2\\n• 阿尔及利亚、刚果（金）、喀麦隆、摩洛哥：UTC+1 (-1h)\\n• 科特迪瓦、塞内加尔：UTC+0 (-2h)", time: "09:30" }}
    ]);
  }}
}}

// Start
initSeeds();
initDailyQuote();
setInterval(initDailyQuote, 60000);
if (localStorage.getItem(STORAGE_KEYS.THEME) === 'comic') {{
  document.body.classList.add('theme-comic');
  const btn = document.getElementById('themeToggleBtn');
  if (btn) btn.textContent = '🎨 切换现代极简';
}}
renderTodos();
renderReqs();
renderNotes();
renderLinks();
renderTimezones();
setInterval(renderTimezones, 1000);
</script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as out_f:
    out_f.write(html_content)

print('Compiled index.html successfully with all authentic Peanuts persona logos!')

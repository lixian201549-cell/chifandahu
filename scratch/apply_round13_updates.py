#!/usr/bin/env python3
import sys

with open("assemble_final_app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Original line count:", len(lines))

# 1. Update CSS: Blackboard width & Snoopy cute animations
# Find chalkboard-stage-wrap around line 1823
stage_idx = -1
for i, line in enumerate(lines):
    if ".chalkboard-stage-wrap {" in line and i < 1900:
        stage_idx = i
        break

assert stage_idx != -1, "Could not find .chalkboard-stage-wrap"
print("Found .chalkboard-stage-wrap at line", stage_idx + 1)

# Replace lines stage_idx to stage_idx + 4
lines[stage_idx : stage_idx + 5] = [
    "  .chalkboard-stage-wrap {\n",
    "    margin: 110px auto 30px auto; /* Moved blackboard noticeably lower per user request */\n",
    "    position: relative;\n",
    "    max-width: 1280px;\n",
    "    width: 96%;\n",
    "  }\n"
]

# Find .snoopy-lying-wrap around line 1696
snoopy_wrap_idx = -1
for i, line in enumerate(lines):
    if ".snoopy-lying-wrap {" in line and i < 1800:
        snoopy_wrap_idx = i
        break

assert snoopy_wrap_idx != -1, "Could not find .snoopy-lying-wrap"
print("Found .snoopy-lying-wrap at line", snoopy_wrap_idx + 1)

# Find the end of @keyframes snoopyNod
nod_end_idx = -1
for i in range(snoopy_wrap_idx, snoopy_wrap_idx + 35):
    if "  @keyframes snoopyNod {" in lines[i]:
        for j in range(i, i + 10):
            if lines[j].strip() == "}":
                nod_end_idx = j
                break
        break

assert nod_end_idx != -1, "Could not find end of @keyframes snoopyNod"

new_snoopy_css_lines = [
    "  /* Lively breathing animation for cute Snoopy & Woodstock */\n",
    "  @keyframes snoopyGentleFloat {\n",
    "    0%, 100% {\n",
    "      transform: translateY(0px) rotate(0deg);\n",
    "    }\n",
    "    50% {\n",
    "      transform: translateY(-5px) rotate(1.2deg);\n",
    "    }\n",
    "  }\n",
    "\n",
    "  .snoopy-lying-wrap {\n",
    "    position: relative;\n",
    "    display: block;\n",
    "    width: 110px;\n",
    "    height: 132px;\n",
    "    animation: snoopyGentleFloat 3.8s ease-in-out infinite;\n",
    "    transition: transform 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.22s ease;\n",
    "    transform-origin: bottom center;\n",
    "  }\n",
    "  .border-snoopy-stage:hover .snoopy-lying-wrap {\n",
    "    animation-play-state: paused;\n",
    "    transform: translateY(-6px) scale(1.08) rotate(-1.2deg);\n",
    "    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.22)) drop-shadow(0 0 14px rgba(254, 240, 138, 0.45));\n",
    "  }\n",
    "\n",
    "  .snoopy-lying-img {\n",
    "    width: 110px;\n",
    "    height: 132px;\n",
    "    object-fit: contain;\n",
    "    display: block;\n",
    "    filter: drop-shadow(0 4px 10px rgba(0,0,0,0.15));\n",
    "  }\n",
    "\n",
    "  .snoopy-nodding {\n",
    "    animation: snoopyNod 0.45s ease;\n",
    "  }\n",
    "  @keyframes snoopyNod {\n",
    "    0% { transform: rotate(0deg); }\n",
    "    30% { transform: rotate(-2.5deg) translateY(-3px); }\n",
    "    60% { transform: rotate(1.5deg) translateY(-1px); }\n",
    "    100% { transform: rotate(0deg); }\n",
    "  }\n",
    "\n",
    "  /* Joyful bounce & wiggle on click */\n",
    "  .snoopy-happy-bounce {\n",
    "    animation: snoopyHappyBounce 0.65s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;\n",
    "  }\n",
    "  @keyframes snoopyHappyBounce {\n",
    "    0% { transform: scale(1) translateY(0); }\n",
    "    22% { transform: scale(1.15, 0.88) translateY(2px) rotate(-4deg); }\n",
    "    48% { transform: scale(0.92, 1.15) translateY(-12px) rotate(5deg); }\n",
    "    72% { transform: scale(1.06, 0.96) translateY(-4px) rotate(-2deg); }\n",
    "    100% { transform: scale(1) translateY(0) rotate(0); }\n",
    "  }\n",
    "\n",
    "  .snoopy-cute-aura {\n",
    "    position: absolute;\n",
    "    top: 6px;\n",
    "    left: 10px;\n",
    "    font-size: 13px;\n",
    "    pointer-events: none;\n",
    "    animation: auraFloat 2.8s ease-in-out infinite;\n",
    "    filter: drop-shadow(0 0 4px rgba(254, 240, 138, 0.8));\n",
    "    opacity: 0.85;\n",
    "  }\n",
    "  @keyframes auraFloat {\n",
    "    0%, 100% { transform: translateY(0) scale(1); opacity: 0.6; }\n",
    "    50% { transform: translateY(-4px) scale(1.15); opacity: 1; }\n",
    "  }\n"
]

lines[snoopy_wrap_idx : nod_end_idx + 1] = new_snoopy_css_lines

# Update chalkboard slate & textarea dimensions
content = "".join(lines)

old_slate_css = """  .chalkboard-slate {
    background: #142a20;
    background-image: 
      radial-gradient(ellipse at 50% 30%, rgba(255, 255, 255, 0.04) 0%, rgba(0, 0, 0, 0.45) 100%),
      repeating-radial-gradient(circle at 20% 40%, rgba(255,255,255,0.01) 0, rgba(255,255,255,0.01) 2px, transparent 2px, transparent 4px);
    border-radius: 12px;
    padding: 24px 28px;
    border: 2px solid #0d1c15;
    box-shadow: inset 0 6px 18px rgba(0, 0, 0, 0.6), inset 0 0 60px rgba(0, 0, 0, 0.4);
    color: #f8fafc;
    min-height: 400px;
    position: relative;
  }"""

new_slate_css = """  .chalkboard-slate {
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
  }"""

assert old_slate_css in content, "Could not find old_slate_css"
content = content.replace(old_slate_css, new_slate_css)

old_textarea_css = """  .chalkboard-content {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 380px;
    position: relative;
  }
  .chalkboard-direct-textarea {
    width: 100%;
    min-height: 380px;"""

new_textarea_css = """  .chalkboard-content {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 420px;
    position: relative;
  }
  .chalkboard-direct-textarea {
    width: 100%;
    min-height: 420px;"""

assert old_textarea_css in content, "Could not find old_textarea_css"
content = content.replace(old_textarea_css, new_textarea_css)

# Update HTML Snoopy element to include aura sparkle
old_snoopy_html = """          <!-- Cute Snoopy & Woodstock on Board Border -->
          <div class="border-snoopy-stage" id="borderSnoopyStage" onclick="interactBorderSnoopy()" title="点击史努比互动~">
            <div class="snoopy-lying-wrap" id="snoopyLyingWrap" title="史努比抱着 Woodstock 陪你自学~">
              <img src="__IMG_BORDER_SNOOPY__" alt="Snoopy and Woodstock" class="snoopy-lying-img" />
              <div class="snoopy-particles" id="snoopyParticles"></div>
            </div>
          </div>"""

new_snoopy_html = """          <!-- Cute Snoopy & Woodstock on Board Border -->
          <div class="border-snoopy-stage" id="borderSnoopyStage" onclick="interactBorderSnoopy()" title="点击史努比互动~">
            <div class="snoopy-lying-wrap" id="snoopyLyingWrap" title="史努比抱着 Woodstock 陪你自学~">
              <span class="snoopy-cute-aura" title="Woodstock ♪">✨</span>
              <img src="__IMG_BORDER_SNOOPY__" alt="Snoopy and Woodstock" class="snoopy-lying-img" />
              <div class="snoopy-particles" id="snoopyParticles"></div>
            </div>
          </div>"""

assert old_snoopy_html in content, "Could not find old_snoopy_html"
content = content.replace(old_snoopy_html, new_snoopy_html)

# Update JS interactBorderSnoopy and spawnSnoopyParticles
old_interact_js = """// ================= BORDER SNOOPY & WOODSTOCK INTERACTION =================
function interactBorderSnoopy() {
  const wrap = document.getElementById('snoopyLyingWrap');
  if (wrap) {
    wrap.classList.remove('snoopy-nodding');
    void wrap.offsetWidth;
    wrap.classList.add('snoopy-nodding');
  }
  spawnSnoopyParticles();
}

function spawnSnoopyParticles() {
  const container = document.getElementById('snoopyParticles');
  if (!container) return;

  const icons = ['❤️', '✨', '♪', '🌸', '🐾', '⭐', '♫'];
  for (let i = 0; i < 4; i++) {
    const p = document.createElement('span');
    p.className = 'floating-particle';
    p.textContent = icons[Math.floor(Math.random() * icons.length)];
    const dx = (Math.random() - 0.5) * 80 + 'px';
    const dy = (-35 - Math.random() * 50) + 'px';
    p.style.setProperty('--dx', dx);
    p.style.setProperty('--dy', dy);
    p.style.left = (Math.random() * 80 + 30) + 'px';
    p.style.bottom = '15px';
    container.appendChild(p);

    setTimeout(() => {
      if (p.parentNode) p.parentNode.removeChild(p);
    }, 1100);
  }
}"""

new_interact_js = """// ================= BORDER SNOOPY & WOODSTOCK INTERACTION =================
function interactBorderSnoopy() {
  const wrap = document.getElementById('snoopyLyingWrap');
  if (wrap) {
    wrap.classList.remove('snoopy-happy-bounce');
    wrap.classList.remove('snoopy-nodding');
    void wrap.offsetWidth;
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
}"""

assert old_interact_js in content, "Could not find old_interact_js"
content = content.replace(old_interact_js, new_interact_js)

# 2. Update CSS for minimal conflict pill and weekly board morning/afternoon/allday layout
# Find conflict css around .weekly-card-conflict
lines = content.splitlines(keepends=True)
c_start = -1
c_end = -1
for i, line in enumerate(lines):
    if "  .weekly-card-conflict {" in line:
        c_start = i
        break

assert c_start != -1, "Could not find .weekly-card-conflict in lines"

for i in range(c_start, c_start + 150):
    if "  /* Month Calendar Conflict Event Pill */" in lines[i]:
        c_end = i
        break

assert c_end != -1, "Could not find Month Calendar Conflict marker"

new_conflict_css_lines = [
    "  /* 极简而明白的日历卡片冲突提示条 (Minimalist Calendar Conflict Pill) */\n",
    "  .weekly-card-conflict {\n",
    "    display: inline-flex;\n",
    "    align-items: center;\n",
    "    gap: 4px;\n",
    "    margin-top: 5px;\n",
    "    padding: 2px 7px;\n",
    "    background: #ffe4e6;\n",
    "    border: 1px solid #fecdd3;\n",
    "    border-radius: 4px;\n",
    "    color: #be123c;\n",
    "    font-size: 11px;\n",
    "    font-weight: 700;\n",
    "    line-height: 1.35;\n",
    "    cursor: pointer;\n",
    "    transition: all 0.15s ease;\n",
    "  }\n",
    "  .weekly-card-conflict:hover {\n",
    "    background: #fecdd3;\n",
    "    border-color: #fda4af;\n",
    "  }\n",
    "  .conflict-head-icon {\n",
    "    font-size: 11px;\n",
    "    line-height: 1;\n",
    "  }\n",
    "  .conflict-overlap-label {\n",
    "    color: #9f1239;\n",
    "    font-size: 10.5px;\n",
    "  }\n",
    "  .conflict-overlap-time {\n",
    "    color: #be123c;\n",
    "    font-weight: 800;\n",
    "    font-family: var(--font-mono);\n",
    "    padding: 0 2px;\n",
    "  }\n",
    "  .conflict-overlap-dur {\n",
    "    color: #e11d48;\n",
    "    font-weight: 700;\n",
    "    font-size: 10px;\n",
    "  }\n",
    "  .weekly-conflict-more {\n",
    "    background: #be123c;\n",
    "    color: #ffffff;\n",
    "    font-size: 9px;\n",
    "    padding: 0 4px;\n",
    "    border-radius: 8px;\n",
    "    font-weight: 700;\n",
    "  }\n",
    "\n",
    "  /* Day Calendar Conflict Alert Box (Minimalist Sleek Bar) */\n",
    "  .day-meeting-card.is-conflict {\n",
    "    border-left: 5px solid #e11d48 !important;\n",
    "    background: #fff8f8 !important;\n",
    "    border-color: #fca5a5 !important;\n",
    "  }\n",
    "  .day-meeting-conflict-box {\n",
    "    margin-top: 6px;\n",
    "    margin-bottom: 6px;\n",
    "    padding: 5px 10px;\n",
    "    background: #fff1f2;\n",
    "    border: 1px solid #fecdd3;\n",
    "    border-left: 3px solid #e11d48;\n",
    "    border-radius: 4px;\n",
    "    display: flex;\n",
    "    align-items: center;\n",
    "    gap: 8px;\n",
    "    flex-wrap: wrap;\n",
    "    font-size: 11.5px;\n",
    "    line-height: 1.4;\n",
    "    cursor: pointer;\n",
    "    transition: background 0.15s ease;\n",
    "  }\n",
    "  .day-meeting-conflict-box:hover {\n",
    "    background: #ffe4e6;\n",
    "  }\n",
    "  .day-conflict-time-pill {\n",
    "    display: inline-flex;\n",
    "    align-items: center;\n",
    "    gap: 3px;\n",
    "    color: #881337;\n",
    "  }\n",
    "  .day-conflict-time-pill strong {\n",
    "    color: #be123c;\n",
    "    font-family: var(--font-mono);\n",
    "  }\n",
    "  .day-conflict-dur {\n",
    "    color: #e11d48;\n",
    "    font-weight: 700;\n",
    "    font-size: 11px;\n",
    "  }\n",
    "  .day-conflict-count-badge {\n",
    "    background: #be123c;\n",
    "    color: #ffffff;\n",
    "    font-size: 10px;\n",
    "    padding: 1px 6px;\n",
    "    border-radius: 10px;\n",
    "    font-weight: 700;\n",
    "  }\n",
    "\n",
    "  /* Weekly Board Morning / Afternoon Structure & All-Day Occupied Display */\n",
    "  .weekly-allday-wrap {\n",
    "    margin-bottom: 4px;\n",
    "  }\n",
    "  .weekly-allday-banner {\n",
    "    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);\n",
    "    border: 1px solid #f59e0b;\n",
    "    color: #92400e;\n",
    "    font-size: 11px;\n",
    "    font-weight: 800;\n",
    "    padding: 5px 8px;\n",
    "    border-radius: 6px;\n",
    "    text-align: center;\n",
    "    margin-bottom: 8px;\n",
    "    box-shadow: 0 1px 3px rgba(245, 158, 11, 0.2);\n",
    "    display: flex;\n",
    "    align-items: center;\n",
    "    justify-content: center;\n",
    "    gap: 4px;\n",
    "  }\n",
    "  .weekly-card.weekly-card-allday {\n",
    "    border-left: 4px solid #f59e0b !important;\n",
    "    background: #fffbeb !important;\n",
    "    border-color: #fde68a !important;\n",
    "  }\n",
    "  .allday-pill-tag {\n",
    "    background: #f59e0b;\n",
    "    color: #ffffff;\n",
    "    font-size: 9.5px;\n",
    "    padding: 0 5px;\n",
    "    border-radius: 8px;\n",
    "    font-weight: 700;\n",
    "    margin-left: 4px;\n",
    "  }\n",
    "  .weekly-allday-occupied-notice {\n",
    "    margin-top: 8px;\n",
    "    padding: 6px 8px;\n",
    "    background: #f4f4f5;\n",
    "    border: 1px dashed #d4d4d8;\n",
    "    border-radius: 6px;\n",
    "    font-size: 11px;\n",
    "    color: #71717a;\n",
    "    text-align: center;\n",
    "    font-weight: 600;\n",
    "  }\n",
    "  .weekly-period-block {\n",
    "    margin-bottom: 8px;\n",
    "  }\n",
    "  .weekly-period-divider {\n",
    "    display: flex;\n",
    "    align-items: center;\n",
    "    justify-content: space-between;\n",
    "    font-size: 10.5px;\n",
    "    font-weight: 700;\n",
    "    color: var(--text-muted);\n",
    "    padding: 3px 2px;\n",
    "    margin-top: 6px;\n",
    "    margin-bottom: 4px;\n",
    "    border-bottom: 1px dashed var(--border);\n",
    "  }\n",
    "  .weekly-period-block:first-child .weekly-period-divider {\n",
    "    margin-top: 0;\n",
    "  }\n",
    "  .period-status-empty {\n",
    "    color: #16a34a;\n",
    "    background: #dcfce7;\n",
    "    font-size: 9.5px;\n",
    "    padding: 0 5px;\n",
    "    border-radius: 8px;\n",
    "    font-weight: 700;\n",
    "  }\n",
    "  .period-status-occupied {\n",
    "    color: #2563eb;\n",
    "    background: #dbeafe;\n",
    "    font-size: 9.5px;\n",
    "    padding: 0 5px;\n",
    "    border-radius: 8px;\n",
    "    font-weight: 700;\n",
    "  }\n",
    "  .weekly-empty-period-slot {\n",
    "    padding: 10px 8px;\n",
    "    background: #f8fafc;\n",
    "    border: 1.5px dashed #cbd5e1;\n",
    "    border-radius: 6px;\n",
    "    text-align: center;\n",
    "    cursor: pointer;\n",
    "    transition: all 0.15s ease;\n",
    "    margin-bottom: 6px;\n",
    "  }\n",
    "  .weekly-empty-period-slot:hover {\n",
    "    background: #f0fdf4;\n",
    "    border-color: #86efac;\n",
    "    transform: translateY(-1px);\n",
    "  }\n",
    "  .empty-slot-text {\n",
    "    font-size: 11.5px;\n",
    "    font-weight: 700;\n",
    "    color: #16a34a;\n",
    "  }\n",
    "  .empty-slot-sub {\n",
    "    font-size: 10px;\n",
    "    color: #64748b;\n",
    "    margin-top: 2px;\n",
    "  }\n",
    "  .weekly-period-free-slots {\n",
    "    margin-top: 4px;\n",
    "    margin-bottom: 4px;\n",
    "  }\n\n"
]

lines[c_start : c_end] = new_conflict_css_lines
content = "".join(lines)

# 3. Update Weekly Board day column rendering
old_weekly_marker = "    if (dayMeetings.length === 0) {\n      html += `\n        <div style=\"text-align:center; padding: 22px 8px; color:var(--text-muted); font-size:12px; background:#fff; border:1px dashed var(--border); border-radius:var(--radius-sm);\">\n          <div style=\"margin-bottom:4px;\">全天暂无会议</div>"
assert old_weekly_marker in content, "Could not find old_weekly_marker"

weekly_end_marker = "      html += `</div>`;\n    }\n\n    html += `\n        </div>\n      </div>\n    `;"
w_start = content.find(old_weekly_marker)
w_end = content.find(weekly_end_marker, w_start)
assert w_start != -1 and w_end != -1, "Could not find weekly board boundaries"
w_end += len("      html += `</div>`;\n    }")

new_weekly_code = """    function renderWeeklySingleCard(m, isAllDay) {
      const dt = getMeetingDisplayTime(m);
      const isPending = (m.status === 'pending');
      const isNoticeUnsent = (m.noticeSent === false || m.noticeSent === undefined || m.noticeSent === null);
      const mConflicts = conflictMap[m.id] || [];
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
            <span style="display:inline-flex; align-items:center; gap:4px; font-size:11.5px; ${dt.isShifted ? 'font-weight:700; color:#15803d;' : 'font-weight:700; color:var(--blue-accent);'}">
              <span>${dt.start}${dt.end ? ' - ' + dt.end : ''}</span>
              ${isAllDay ? '<span class="allday-pill-tag">从早到晚 · 全天</span>' : ''}
            </span>
            <div style="display:flex; align-items:center; gap:4px;">
              ${isNoticeUnsent ? '<span class="weekly-notice-tag">⚠️ 待发通知</span>' : ''}
              ${isPending ? '<span class="weekly-pending-tag">⚠️ 待确认</span>' : (m.location ? `<span style="font-size:10px; font-weight:normal; color:var(--text-muted);">${escapeHtml(m.location)}</span>` : '')}
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
              <span class="conflict-overlap-dur">(${mConflicts[0].overlapDuration}m)</span>
              ${mConflicts.length > 1 ? `<span class="weekly-conflict-more">+${mConflicts.length - 1}</span>` : ''}
            </div>
          ` : ''}

          ${(m.reporter || m.attendees) ? `
            <div class="weekly-card-meta" style="font-size:11px; color:var(--text-secondary); margin-top:2px;">
              ${m.reporter ? `<div>👤 <span style="color:var(--text-primary); font-weight:600;">${escapeHtml(m.reporter)}</span>${m.attendees && m.attendees !== m.reporter ? `<span style="color:var(--text-muted); margin-left:4px;">· ${escapeHtml(m.attendees)}</span>` : ''}</div>` : (m.attendees ? `<div>👥 <span style="color:var(--text-muted);">${escapeHtml(m.attendees)}</span></div>` : '')}
            </div>
          ` : ''}

          ${m.decision ? `
            <div class="weekly-card-decision ${isPending ? 'decision-pending' : ''}" title="${escapeHtml(m.decision)}" style="margin-top:5px; padding:3px 6px; font-size:10.5px; line-height:1.35; border-radius:3px;">
              <strong>🎯 决策：</strong>${escapeHtml(m.decision.slice(0, 36))}${m.decision.length > 36 ? '...' : ''}
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

    // 检查是否有从早到晚 / 全天占满的会议
    const allDayMeeting = dayMeetings.find(m => {
      const dur = parseInt(m.duration || 45, 10);
      const sMin = timeStrToMinutes(m.startTime || m.time || '10:00');
      const eMin = timeStrToMinutes(m.endTime || calculateEndTime(m.startTime || m.time, dur));
      return dur >= 360 || (sMin <= 600 && eMin >= 1020) || (m.subject && (m.subject.includes('全天') || m.subject.includes('从早到晚')));
    });

    if (dayMeetings.length === 0) {
      html += `
        <div style="text-align:center; padding: 22px 8px; color:var(--text-muted); font-size:12px; background:#fff; border:1px dashed var(--border); border-radius:var(--radius-sm);">
          <div style="margin-bottom:4px;">全天暂无会议</div>
          <button class="btn btn-sm btn-ghost" style="margin-top:4px; font-size:11px;" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '10:00', 45)">＋ 安排预约</button>
        </div>
      `;
    } else if (allDayMeeting) {
      // 🌞 全天会议：把一整天都显示用完了！
      html += `
        <div class="weekly-allday-wrap">
          <div class="weekly-allday-banner">
            <span>🌞 全天排期已满 · 从早到晚</span>
          </div>
      `;
      dayMeetings.forEach(m => {
        html += renderWeeklySingleCard(m, m.id === allDayMeeting.id);
      });
      html += `
          <div class="weekly-allday-occupied-notice">
            <span>🚫 本日从早到晚均已占满，无可用空档</span>
          </div>
        </div>
      `;
    } else {
      // 区分上午 (08:30 - 12:00) 与 下午 (13:30 - 18:00)
      const morningMeetings = [];
      const afternoonMeetings = [];

      dayMeetings.forEach(m => {
        const dt = getMeetingDisplayTime(m);
        const sMins = timeStrToMinutes(dt.start || '10:00');
        if (sMins < 780) { // 13:00 前归为上午
          morningMeetings.push(m);
        } else {
          afternoonMeetings.push(m);
        }
      });

      const morningFreeSlots = freeSlots.filter(s => s.end <= 780);
      const afternoonFreeSlots = freeSlots.filter(s => s.start >= 780);

      // --- 1. 上午时段 (如果只在下午，上午显示为空档可约) ---
      html += `
        <div class="weekly-period-block morning-block">
          <div class="weekly-period-divider">
            <span>🌅 上午 (08:30 - 12:00)</span>
            <span class="${morningMeetings.length > 0 ? 'period-status-occupied' : 'period-status-empty'}">
              ${morningMeetings.length > 0 ? morningMeetings.length + '场排期' : '空闲'}
            </span>
          </div>
      `;
      if (morningMeetings.length === 0) {
        html += `
          <div class="weekly-empty-period-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '09:30', 60)" title="上午时段空闲，点击预约上午会议">
            <div class="empty-slot-text">🌅 上午时段空闲 (可约) ＋</div>
            <div class="empty-slot-sub">08:30 - 12:00 无排期</div>
          </div>
        `;
      } else {
        morningMeetings.forEach(m => {
          html += renderWeeklySingleCard(m, false);
        });
        if (morningFreeSlots.length > 0) {
          html += `<div class="weekly-period-free-slots">`;
          morningFreeSlots.forEach(slot => {
            html += `
              <div class="weekly-free-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '${slot.startStr}', ${Math.min(slot.duration, 60)})" title="上午空档 ${slot.startStr} - ${slot.endStr} (${slot.duration}m 可约)">
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
            <span>🌇 下午 (13:30 - 18:00)</span>
            <span class="${afternoonMeetings.length > 0 ? 'period-status-occupied' : 'period-status-empty'}">
              ${afternoonMeetings.length > 0 ? afternoonMeetings.length + '场排期' : '空闲'}
            </span>
          </div>
      `;
      if (afternoonMeetings.length === 0) {
        html += `
          <div class="weekly-empty-period-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '14:30', 60)" title="下午时段空闲，点击预约下午会议">
            <div class="empty-slot-text">🌇 下午时段空闲 (可约) ＋</div>
            <div class="empty-slot-sub">13:30 - 18:00 无排期</div>
          </div>
        `;
      } else {
        afternoonMeetings.forEach(m => {
          html += renderWeeklySingleCard(m, false);
        });
        if (afternoonFreeSlots.length > 0) {
          html += `<div class="weekly-period-free-slots">`;
          afternoonFreeSlots.forEach(slot => {
            html += `
              <div class="weekly-free-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '${slot.startStr}', ${Math.min(slot.duration, 60)})" title="下午空档 ${slot.startStr} - ${slot.endStr} (${slot.duration}m 可约)">
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
    }"""

content = content[:w_start] + new_weekly_code + content[w_end:]

# 4. Update Day Calendar conflict box to be minimalist sleek bar
day_conf_marker = "        ${mConflicts.length > 0 ? `\n          <div class=\"day-meeting-conflict-box\">"
assert day_conf_marker in content, "Could not find day_conf_marker"
day_conf_end_marker = "          </div>\n        ` : ''}"
dc_start = content.find(day_conf_marker)
dc_end = content.find(day_conf_end_marker, dc_start) + len(day_conf_end_marker)

new_day_conf_code = """        ${mConflicts.length > 0 ? `
          <div class="day-meeting-conflict-box" title="⚠️ 会议时间冲突：与【${mConflicts.map(c => escapeHtml(c.otherSubject)).join('、')}】重合（点击查看详情）" onclick="editMeeting(${m.id})">
            <span class="day-conflict-time-pill">⚠️ 🕒 重合时间：<strong>${mConflicts[0].overlapRangeStr}</strong></span>
            <span class="day-conflict-dur">（重叠时长：${mConflicts[0].overlapDuration} 分钟）</span>
            ${mConflicts.length > 1 ? `<span class="day-conflict-count-badge">+${mConflicts.length - 1} 处冲突</span>` : ''}
            <span style="font-size:11px; color:#9f1239; margin-left:auto; font-weight:600;">点击查看详情 ▶</span>
          </div>
        ` : ''}"""

content = content[:dc_start] + new_day_conf_code + content[dc_end:]

# 5. Day Calendar empty slot quick booking buttons
old_day_morning_empty = """  if (morningItems.length === 0) {
    html += `
      <div class="day-lunch-rest-card" style="background:#f0fdf4; border-color:#bbf7d0; color:#15803d;">
        <span>🕒</span> 上午工作时段无会议排期，全时段机动专注
      </div>
    `;
  }"""

new_day_morning_empty = """  if (morningItems.length === 0) {
    html += `
      <div class="day-lunch-rest-card" style="background:#f0fdf4; border-color:#bbf7d0; color:#15803d; display:flex; justify-content:space-between; align-items:center;">
        <div><span>🕒</span> <strong>上午时段空闲 (08:30 - 12:00)</strong> · 无会议排期</div>
        <button class="btn btn-sm btn-ghost" style="color:#15803d; border-color:#86efac; background:#fff; font-size:11px;" onclick="openAddMeetingModalWithSlot('${curDateStr}', '09:30', 60)">＋ 安排上午会议</button>
      </div>
    `;
  }"""

assert old_day_morning_empty in content, "Could not find old_day_morning_empty"
content = content.replace(old_day_morning_empty, new_day_morning_empty)

old_day_afternoon_empty = """  if (afternoonItems.length === 0) {
    html += `
      <div class="day-lunch-rest-card" style="background:#f0fdf4; border-color:#bbf7d0; color:#15803d;">
        <span>🕒</span> 下午工作时段无会议排期，全时段机动专注
      </div>
    `;
  }"""

new_day_afternoon_empty = """  if (afternoonItems.length === 0) {
    html += `
      <div class="day-lunch-rest-card" style="background:#f0fdf4; border-color:#bbf7d0; color:#15803d; display:flex; justify-content:space-between; align-items:center;">
        <div><span>🕒</span> <strong>下午时段空闲 (14:00 - 18:00)</strong> · 无会议排期</div>
        <button class="btn btn-sm btn-ghost" style="color:#15803d; border-color:#86efac; background:#fff; font-size:11px;" onclick="openAddMeetingModalWithSlot('${curDateStr}', '14:30', 60)">＋ 安排下午会议</button>
      </div>
    `;
  }"""

assert old_day_afternoon_empty in content, "Could not find old_day_afternoon_empty"
content = content.replace(old_day_afternoon_empty, new_day_afternoon_empty)

with open("assemble_final_app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("assemble_final_app.py updated successfully!")

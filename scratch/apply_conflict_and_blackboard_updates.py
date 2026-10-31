import re

with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update chalkboard margin and border snoopy styling
old_css_snoopy = """  /* Border-Lying Snoopy Stage */
  .border-snoopy-stage {
    position: absolute;
    right: 48px;
    bottom: calc(100% - 2px);
    z-index: 30;
    cursor: pointer;
    user-select: none;
    display: flex;
    align-items: flex-end;
  }

  .snoopy-lying-wrap {
    position: relative;
    display: block;
    width: 165px;
    height: 67px;
    transition: transform 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  .border-snoopy-stage:hover .snoopy-lying-wrap {
    transform: translateY(-2px) scale(1.02);
  }

  .snoopy-lying-img {
    width: 165px;
    height: auto;
    display: block;
    filter: drop-shadow(0 2px 5px rgba(0,0,0,0.08));
  }"""

new_css_snoopy = """  /* Border Snoopy Stage (Cute Snoopy cuddling Woodstock sitting on board) */
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

  .snoopy-lying-wrap {
    position: relative;
    display: block;
    width: 105px;
    height: 126px;
    transition: transform 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  .border-snoopy-stage:hover .snoopy-lying-wrap {
    transform: translateY(-2px) scale(1.03);
  }

  .snoopy-lying-img {
    width: 105px;
    height: 126px;
    object-fit: contain;
    display: block;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.12));
  }"""

assert old_css_snoopy in code, "Could not find old_css_snoopy"
code = code.replace(old_css_snoopy, new_css_snoopy)

# 2. Lower the chalkboard (黑板再低一点)
old_board_margin = """  .chalkboard-stage-wrap {
    margin: 75px auto 25px auto; /* Moved blackboard down to give generous room for Snoopy & Woodstock */
    position: relative;
    max-width: 1040px;
  }"""

new_board_margin = """  .chalkboard-stage-wrap {
    margin: 115px auto 30px auto; /* Moved blackboard noticeably lower per user request */
    position: relative;
    max-width: 1040px;
  }"""

assert old_board_margin in code, "Could not find old_board_margin"
code = code.replace(old_board_margin, new_board_margin)

# 3. Mobile responsiveness for snoopy and board margin
old_media = """  @media (max-width: 768px) {
    .chalkboard-stage-wrap {
      margin-top: 55px;
    }
    .border-snoopy-stage {
      right: 18px;
    }
    .snoopy-lying-wrap {
      width: 125px;
      height: 51px;
    }
    .snoopy-lying-img {
      width: 125px;
    }
    .woodstock-avatar {
      width: 34px;
      height: 38px;
    }
  }"""

new_media = """  @media (max-width: 768px) {
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
  }"""

assert old_media in code, "Could not find old_media"
code = code.replace(old_media, new_media)

# 4. Add Calendar Conflict CSS Classes
conflict_css = """
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
  .weekly-card-conflict {
    margin-top: 6px;
    padding: 4px 6px;
    background: #ffe4e6;
    border: 1px solid #fecdd3;
    border-radius: 4px;
    font-size: 10.5px;
    line-height: 1.35;
  }
  .weekly-card-conflict-head {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-bottom: 2px;
  }
  .conflict-head-icon {
    font-size: 11px;
  }
  .conflict-head-text {
    font-weight: 800;
    color: #be123c;
  }
  .conflict-head-count {
    font-size: 9.5px;
    background: #be123c;
    color: #ffffff;
    padding: 0 4px;
    border-radius: 8px;
    font-weight: 700;
  }
  .weekly-card-conflict-row {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 3px;
    font-size: 10.5px;
    color: #881337;
    margin-top: 2px;
  }
  .conflict-overlap-label {
    color: #9f1239;
    font-weight: 600;
  }
  .conflict-overlap-time {
    color: #be123c;
    font-weight: 800;
    font-family: var(--font-mono);
    background: rgba(255, 255, 255, 0.75);
    padding: 0 3px;
    border-radius: 2px;
  }
  .conflict-overlap-dur {
    color: #e11d48;
    font-weight: 700;
    font-size: 10px;
  }
  .conflict-overlap-with {
    color: #52525b;
    font-size: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 110px;
  }

  /* Day Calendar Conflict Alert Box */
  .day-meeting-card.is-conflict {
    border-left: 5px solid #e11d48 !important;
    background: #fff8f8 !important;
    border-color: #fca5a5 !important;
  }
  .day-meeting-conflict-box {
    margin-top: 6px;
    margin-bottom: 8px;
    padding: 8px 12px;
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-left: 4px solid #e11d48;
    border-radius: 6px;
  }
  .day-conflict-title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
  }
  .day-conflict-badge {
    font-weight: 800;
    color: #be123c;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .day-conflict-count-badge {
    background: #be123c;
    color: #ffffff;
    font-size: 10px;
    padding: 1px 6px;
    border-radius: 10px;
    font-weight: 700;
  }
  .day-conflict-hint {
    font-size: 11px;
    color: #9f1239;
    font-weight: 600;
  }
  .day-conflict-detail-row {
    font-size: 12px;
    color: #881337;
    margin-top: 3px;
    line-height: 1.45;
  }
  .day-conflict-time-pill {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    background: #ffe4e6;
    border: 1px solid #fecdd3;
    padding: 1px 6px;
    border-radius: 4px;
    color: #be123c;
    font-weight: 700;
    font-family: var(--font-mono);
    margin-left: 2px;
  }
  .day-conflict-dur {
    color: #e11d48;
    font-weight: 700;
    font-size: 11px;
    margin-left: 3px;
  }
  .day-conflict-reporter {
    color: var(--text-secondary);
    font-size: 11px;
    margin-left: 4px;
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
"""

anchor_css_end = "  /* ================= 2. 今日任务 (🏕️ Beagle Scout) ================= */"
assert anchor_css_end in code, "Could not find anchor_css_end"
code = code.replace(anchor_css_end, conflict_css + "\n" + anchor_css_end)

# 5. Update HTML: remove woodstock speech bubble and update Snoopy stage
old_html_snoopy = """          <!-- Classic Snoopy (Original Size 165px) & Woodstock on Board Border -->
          <div class="border-snoopy-stage" id="borderSnoopyStage" onclick="interactBorderSnoopy()" title="点击与史努比、Woodstock互动">
            <div class="woodstock-float-box" id="woodstockFloatBox">
              <div class="woodstock-speech-bubble" id="woodstockSpeechText">
                “♪ 啾啾！今天也要开开心心自学呀！”
              </div>
            </div>

            <!-- Visible Woodstock perching on the board border -->
            <div class="woodstock-perch-wrap" title="Woodstock 助教">
              <img src="__IMG_WOODSTOCK__" alt="Woodstock" class="woodstock-avatar" />
            </div>

            <!-- Classic 165px Snoopy lying on the board border -->
            <div class="snoopy-lying-wrap" id="snoopyLyingWrap" title="史努比趴在黑板上陪你自学~">
              <img src="__IMG_BORDER_SNOOPY__" alt="Snoopy Lying" class="snoopy-lying-img" />
              <div class="snoopy-particles" id="snoopyParticles"></div>
            </div>
          </div>"""

new_html_snoopy = """          <!-- Cute Snoopy & Woodstock on Board Border -->
          <div class="border-snoopy-stage" id="borderSnoopyStage" onclick="interactBorderSnoopy()" title="点击史努比互动~">
            <div class="snoopy-lying-wrap" id="snoopyLyingWrap" title="史努比抱着 Woodstock 陪你自学~">
              <img src="__IMG_BORDER_SNOOPY__" alt="Snoopy and Woodstock" class="snoopy-lying-img" />
              <div class="snoopy-particles" id="snoopyParticles"></div>
            </div>
          </div>"""

assert old_html_snoopy in code, "Could not find old_html_snoopy"
code = code.replace(old_html_snoopy, new_html_snoopy)

# 6. Update interactBorderSnoopy: silent, cute nod & particles only (no speech bubble per user request)
old_interact = """let woodstockWhisperIdx = 0;
let woodstockTimeout = null;

function interactBorderSnoopy() {
  const wrap = document.getElementById('snoopyLyingWrap');
  if (wrap) {
    wrap.classList.remove('snoopy-nodding');
    void wrap.offsetWidth;
    wrap.classList.add('snoopy-nodding');
  }

  const textEl = document.getElementById('woodstockSpeechText');
  const whisper = WOODSTOCK_WHISPERS[woodstockWhisperIdx % WOODSTOCK_WHISPERS.length];
  woodstockWhisperIdx++;
  if (textEl) textEl.textContent = whisper;

  const box = document.getElementById('woodstockFloatBox');
  if (box) {
    box.classList.add('active');
    clearTimeout(woodstockTimeout);
    woodstockTimeout = setTimeout(() => {
      box.classList.remove('active');
    }, 5500);
  }

  spawnSnoopyParticles();
}"""

new_interact = """function interactBorderSnoopy() {
  const wrap = document.getElementById('snoopyLyingWrap');
  if (wrap) {
    wrap.classList.remove('snoopy-nodding');
    void wrap.offsetWidth;
    wrap.classList.add('snoopy-nodding');
  }
  spawnSnoopyParticles();
}"""

assert old_interact in code, "Could not find old_interact"
code = code.replace(old_interact, new_interact)

# 7. Add core Conflict and Overlapping Time calculation functions
old_conflict_funcs = """// ================= 会议时间冲突检测 (Meeting Conflict Detection) =================
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
    const listHtml = conflicts.map(c => {
      const dt = getMeetingDisplayTime(c);
      const displayRange = (dt.start && dt.end) ? `${dt.start} - ${dt.end}` : dt.start;
      const cTimeNote = (tzBase !== 'cairo') ? ` (开罗 ${c.startTime || c.time})` : '';
      const reporterText = c.reporter ? ` · 汇报人: ${escapeHtml(c.reporter)}` : '';
      return `
        <div style="margin-top: 4px; padding: 5px 9px; background: rgba(225,29,72,0.06); border-radius: 4px; display: flex; justify-content: space-between; align-items: center; gap: 8px;">
          <div>
            <strong>【${escapeHtml(c.subject || '未命名会议')}】</strong>
            <span style="color: #be123c; font-weight: 700; margin-left: 4px;">🕒 ${escapeHtml(displayRange)}${cTimeNote}</span>
            <span style="color: var(--text-secondary); font-size: 11px;">${reporterText}</span>
          </div>
          <span style="font-size: 11px; color: #be123c; background: #ffe4e6; padding: 1px 6px; border-radius: 3px; font-weight: 600;">已排期</span>
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
}"""

new_conflict_funcs = """// ================= 会议时间冲突与重合时段检测引擎 (Meeting Conflict & Overlapping Time Engine) =================
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
              <span style="color: #9f1239; font-weight: 700; font-size: 11px;">(重叠 ${oDur} 分钟)</span>
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
}"""

assert old_conflict_funcs in code, "Could not find old_conflict_funcs"
code = code.replace(old_conflict_funcs, new_conflict_funcs)

# 8. Update saveMeetingForm confirm message to include exact overlapping time
old_save_conflict = """  // Conflict detection and confirmation prompt against Cairo baseline
  const conflicts = getMeetingConflicts(date, cairoStartTime, cairoEndTime, id);
  if (conflicts.length > 0) {
    const conflictList = conflicts.map(c => {
      const cdt = getMeetingDisplayTime(c);
      return `• 【${c.subject || '未命名会议'}】(${cdt.start} - ${cdt.end}${c.reporter ? ' / 汇报人: ' + c.reporter : ''}${cdt.isShifted ? ' [开罗 ' + cdt.cairoStart + ']' : ''})`;
    }).join('\\n');
    const confirmMsg = `⚠️ 会议时间冲突提醒：\\n\\n您安排的会议时间（${date} ${startTime} - ${endTime}${effectiveTzBase !== 'cairo' ? `，对应开罗时间 ${cairoStartTime} - ${cairoEndTime}` : ''}）与以下已有日程存在重叠冲突：\\n\\n${conflictList}\\n\\n是否确认仍要保存该会议？`;
    if (!confirm(confirmMsg)) {
      return;
    }
  }"""

new_save_conflict = """  // Conflict detection and confirmation prompt against Cairo baseline with exact overlapping times
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
  }"""

assert old_save_conflict in code, "Could not find old_save_conflict"
code = code.replace(old_save_conflict, new_save_conflict)

# 9. Update renderSupervisorWeeklyBoard to display conflict tag & exact overlapping time on cards & day header
old_weekly_start = """function renderSupervisorWeeklyBoard() {
  const boardContainer = document.getElementById('supervisorWeeklyBoardContainer');
  if (!boardContainer) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);"""

new_weekly_start = """function renderSupervisorWeeklyBoard() {
  const boardContainer = document.getElementById('supervisorWeeklyBoardContainer');
  if (!boardContainer) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const conflictMap = getAllMeetingConflicts(meetings);"""

assert old_weekly_start in code, "Could not find old_weekly_start"
code = code.replace(old_weekly_start, new_weekly_start)

# Day column header conflict badge in weekly board
old_weekly_col_header = """        <div class="weekly-col-header">
          <div class="weekly-col-header-main" style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
            <span class="weekly-col-day">${day.name}</span>
            <span class="weekly-col-date">${day.month}月${day.day}日</span>
            ${dayTrip ? `<span class="badge" style="background:#dcfce7; color:#15803d; border:1px solid #86efac; font-size:9.5px; padding:1px 6px; border-radius:10px; font-weight:700;" title="领导出差目的地：${dayTrip.tzName} (比开罗${dayTrip.diffText}) · 本日日程全按当地时间安排">✈️ ${dayTrip.tzName}</span>` : ''}
          </div>
          ${day.isToday ? '<span class="cal-today-badge">今日</span>' : (day.isWeekend ? '<span class="weekly-weekend-badge">周末</span>' : '')}
        </div>"""

new_weekly_col_header = """        <div class="weekly-col-header">
          <div class="weekly-col-header-main" style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
            <span class="weekly-col-day">${day.name}</span>
            <span class="weekly-col-date">${day.month}月${day.day}日</span>
            ${dayTrip ? `<span class="badge" style="background:#dcfce7; color:#15803d; border:1px solid #86efac; font-size:9.5px; padding:1px 6px; border-radius:10px; font-weight:700;" title="领导出差目的地：${dayTrip.tzName} (比开罗${dayTrip.diffText}) · 本日日程全按当地时间安排">✈️ ${dayTrip.tzName}</span>` : ''}
            ${dayMeetings.some(m => conflictMap[m.id] && conflictMap[m.id].length > 0) ? `<span class="badge weekly-conflict-header-badge" title="本日存在会议时间冲突！">⚠️ 时间冲突</span>` : ''}
          </div>
          ${day.isToday ? '<span class="cal-today-badge">今日</span>' : (day.isWeekend ? '<span class="weekly-weekend-badge">周末</span>' : '')}
        </div>"""

assert old_weekly_col_header in code, "Could not find old_weekly_col_header"
code = code.replace(old_weekly_col_header, new_weekly_col_header)

# Meeting card in weekly board: add is-conflict class and render overlapping time block
old_weekly_card_iter = """      dayMeetings.forEach(m => {
        const dt = getMeetingDisplayTime(m);
        const isPending = (m.status === 'pending');
        const isNoticeUnsent = (m.noticeSent === false || m.noticeSent === undefined || m.noticeSent === null);
        let cardCls = 'weekly-card';
        if (isPending) {
          cardCls += ' is-pending';
        } else if (m.priority === 'high') {
          cardCls += ' priority-high';
        }
        if (isNoticeUnsent) {
          cardCls += ' notice-unsent';
        }

        html += `
          <div class="${cardCls}" onclick="editMeeting(${m.id})" title="${isPending ? '【待领导确认】点击核准或调整排期' : (isNoticeUnsent ? '【尚未发送会议通知】点击可编辑并更新通知状态' : '点击查看/编辑详情')}">"""

new_weekly_card_iter = """      dayMeetings.forEach(m => {
        const dt = getMeetingDisplayTime(m);
        const isPending = (m.status === 'pending');
        const isNoticeUnsent = (m.noticeSent === false || m.noticeSent === undefined || m.noticeSent === null);
        const mConflicts = conflictMap[m.id] || [];
        const hasConflict = mConflicts.length > 0;

        let cardCls = 'weekly-card';
        if (isPending) {
          cardCls += ' is-pending';
        } else if (m.priority === 'high') {
          cardCls += ' priority-high';
        }
        if (isNoticeUnsent) {
          cardCls += ' notice-unsent';
        }
        if (hasConflict) {
          cardCls += ' is-conflict';
        }

        const conflictTooltip = hasConflict ? `【⚠️时间冲突警告：与${mConflicts.map(c => '【' + c.otherSubject + '】').join('、')}存在时段重叠】` : '';

        html += `
          <div class="${cardCls}" onclick="editMeeting(${m.id})" title="${conflictTooltip}${isPending ? '【待领导确认】点击核准或调整排期' : (isNoticeUnsent ? '【尚未发送会议通知】点击可编辑并更新通知状态' : '点击查看/编辑详情')}">"""

assert old_weekly_card_iter in code, "Could not find old_weekly_card_iter"
code = code.replace(old_weekly_card_iter, new_weekly_card_iter)

# Insert the conflict display block inside the weekly card
old_weekly_card_meta = """            ${(m.reporter || m.attendees) ? `
              <div class="weekly-card-meta" style="font-size:11px; color:var(--text-secondary); margin-top:2px;">"""

new_weekly_card_meta = """            ${mConflicts.length > 0 ? `
              <div class="weekly-card-conflict" title="⚠️ 会议时间冲突：与【${mConflicts.map(c => escapeHtml(c.otherSubject)).join('、')}】重合">
                <div class="weekly-card-conflict-head">
                  <span class="conflict-head-icon">⚠️</span>
                  <span class="conflict-head-text">时间冲突</span>
                  <span class="conflict-head-count">${mConflicts.length}处重叠</span>
                </div>
                ${mConflicts.map(c => `
                  <div class="weekly-card-conflict-row">
                    <span class="conflict-overlap-label">重合时间：</span>
                    <strong class="conflict-overlap-time">${c.overlapRangeStr}</strong>
                    <span class="conflict-overlap-dur">(${c.overlapDuration}m)</span>
                    <span class="conflict-overlap-with" title="与【${escapeHtml(c.otherSubject)}】重叠">与【${escapeHtml(c.otherSubject.length > 9 ? c.otherSubject.slice(0, 9) + '...' : c.otherSubject)}】</span>
                  </div>
                `).join('')}
              </div>
            ` : ''}

            ${(m.reporter || m.attendees) ? `
              <div class="weekly-card-meta" style="font-size:11px; color:var(--text-secondary); margin-top:2px;">"""

assert old_weekly_card_meta in code, "Could not find old_weekly_card_meta"
code = code.replace(old_weekly_card_meta, new_weekly_card_meta)

# 10. Update renderSupervisorDayCalendar to display conflict details & overlapping time
old_day_cal_start = """function renderSupervisorDayCalendar() {
  const container = document.getElementById('supervisorDayCalendarContainer');
  if (!container) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);"""

new_day_cal_start = """function renderSupervisorDayCalendar() {
  const container = document.getElementById('supervisorDayCalendarContainer');
  if (!container) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const conflictMap = getAllMeetingConflicts(meetings);"""

assert old_day_cal_start in code, "Could not find old_day_cal_start"
code = code.replace(old_day_cal_start, new_day_cal_start)

# Day event card in day calendar
old_day_card_iter = """  function renderDayEventCard(m) {
    const durHours = m.durationHours || (parseInt(m.duration || 45, 10) / 60).toFixed(2);
    const isHigh = (m.priority === 'high');
    const isPending = (m.status === 'pending');
    const isNoticeUnsent = (m.noticeSent === false || m.noticeSent === undefined || m.noticeSent === null);
    const dt = getMeetingDisplayTime(m);"""

new_day_card_iter = """  function renderDayEventCard(m) {
    const durHours = m.durationHours || (parseInt(m.duration || 45, 10) / 60).toFixed(2);
    const isHigh = (m.priority === 'high');
    const isPending = (m.status === 'pending');
    const isNoticeUnsent = (m.noticeSent === false || m.noticeSent === undefined || m.noticeSent === null);
    const dt = getMeetingDisplayTime(m);
    const mConflicts = conflictMap[m.id] || [];
    const hasConflict = mConflicts.length > 0;"""

assert old_day_card_iter in code, "Could not find old_day_card_iter"
code = code.replace(old_day_card_iter, new_day_card_iter)

old_day_card_top = """    return `
      <div class="day-meeting-card ${isPending ? 'is-pending' : (isHigh ? 'priority-high' : '')} ${isNoticeUnsent ? 'notice-unsent' : ''}">"""

new_day_card_top = """    return `
      <div class="day-meeting-card ${isPending ? 'is-pending' : (isHigh ? 'priority-high' : '')} ${isNoticeUnsent ? 'notice-unsent' : ''} ${hasConflict ? 'is-conflict' : ''}">"""

assert old_day_card_top in code, "Could not find old_day_card_top"
code = code.replace(old_day_card_top, new_day_card_top)

# Insert day conflict alert box before decision in day calendar
old_day_card_decision = """        ${m.decision ? `
          <div class="day-meeting-decision ${isPending ? 'decision-pending' : ''}">"""

new_day_card_decision = """        ${mConflicts.length > 0 ? `
          <div class="day-meeting-conflict-box">
            <div class="day-conflict-title-row">
              <div class="day-conflict-badge">
                <span>⚠️ 会议时间冲突警告</span>
                <span class="day-conflict-count-badge">${mConflicts.length} 处重合</span>
              </div>
              <span class="day-conflict-hint">请协调避免时段重合</span>
            </div>
            ${mConflicts.map(c => `
              <div class="day-conflict-detail-row">
                • 与【<strong>${escapeHtml(c.otherSubject)}</strong>】存在时间冲突：
                <span class="day-conflict-time-pill">
                  🕒 重合时间：<strong>${c.overlapRangeStr}</strong>
                </span>
                <span class="day-conflict-dur">（重叠时长：${c.overlapDuration} 分钟）</span>
                ${c.otherReporter ? `<span class="day-conflict-reporter">· 汇报人: ${escapeHtml(c.otherReporter)}</span>` : ''}
              </div>
            `).join('')}
          </div>
        ` : ''}

        ${m.decision ? `
          <div class="day-meeting-decision ${isPending ? 'decision-pending' : ''}">"""

assert old_day_card_decision in code, "Could not find old_day_card_decision"
code = code.replace(old_day_card_decision, new_day_card_decision)

# Day header badge in day calendar
old_day_header_badge = """          ${isToday ? '<span class="cal-today-badge">今日</span>' : ''}
          ${isWeekend ? '<span class="weekly-weekend-badge">周末</span>' : ''}
        </div>"""

new_day_header_badge = """          ${isToday ? '<span class="cal-today-badge">今日</span>' : ''}
          ${isWeekend ? '<span class="weekly-weekend-badge">周末</span>' : ''}
          ${dayMeetings.some(m => conflictMap[m.id] && conflictMap[m.id].length > 0) ? `<span class="badge" style="background:#fee2e2; color:#be123c; border:1px solid #fecdd3; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:700; margin-left:8px;" title="本日存在会议时间冲突">⚠️ 存在时间冲突</span>` : ''}
        </div>"""

assert old_day_header_badge in code, "Could not find old_day_header_badge"
code = code.replace(old_day_header_badge, new_day_header_badge)

# 11. Update renderSupervisorMonthCalendar to show conflict icon and event overlap tag
old_month_cal_start = """function renderSupervisorMonthCalendar() {
  const calContainer = document.getElementById('supervisorMonthCalendarContainer');
  if (!calContainer) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);"""

new_month_cal_start = """function renderSupervisorMonthCalendar() {
  const calContainer = document.getElementById('supervisorMonthCalendarContainer');
  if (!calContainer) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const conflictMap = getAllMeetingConflicts(meetings);"""

assert old_month_cal_start in code, "Could not find old_month_cal_start"
code = code.replace(old_month_cal_start, new_month_cal_start)

# Month day header conflict icon
old_month_day_header = """            <div class="cal-day-header">
              <span class="cal-day-num">${dayCounter}</span>
              ${(() => {
                const curDayTrip = getTripForDate(curDateStr);
                return curDayTrip ? `<span class="badge" style="background:#dcfce7; color:#15803d; border:1px solid #86efac; font-size:9px; padding:0 4px; border-radius:8px; font-weight:700;" title="领导出差目的地：${curDayTrip.tzName} (比开罗${curDayTrip.diffText}) · 全天为当地时间">✈️ ${curDayTrip.tzName}</span>` : '';
              })()}
              ${isToday ? '<span class="cal-today-badge">今天</span>' : ''}
            </div>"""

new_month_day_header = """            <div class="cal-day-header">
              <span class="cal-day-num">${dayCounter}</span>
              ${(() => {
                const curDayTrip = getTripForDate(curDateStr);
                return curDayTrip ? `<span class="badge" style="background:#dcfce7; color:#15803d; border:1px solid #86efac; font-size:9px; padding:0 4px; border-radius:8px; font-weight:700;" title="领导出差目的地：${curDayTrip.tzName} (比开罗${curDayTrip.diffText}) · 全天为当地时间">✈️ ${curDayTrip.tzName}</span>` : '';
              })()}
              ${dayMeetingsList.some(m => conflictMap[m.id] && conflictMap[m.id].length > 0) ? `<span class="cal-day-conflict-icon" title="本日存在会议时间冲突！">⚠️</span>` : ''}
              ${isToday ? '<span class="cal-today-badge">今天</span>' : ''}
            </div>"""

assert old_month_day_header in code, "Could not find old_month_day_header"
code = code.replace(old_month_day_header, new_month_day_header)

# Month day event pills
old_month_events = """            <div class="cal-day-events">
              ${dayMeetingsList.slice(0, 2).map(m => {
                const stCls = m.status === 'scheduled' ? 'status-scheduled' : (m.status === 'completed' ? 'status-completed' : 'status-pending');
                const dt = getMeetingDisplayTime(m);
                return `<div class="cal-event-pill ${stCls}" title="${dt.start} ${escapeHtml(m.subject)}">${dt.start} ${escapeHtml(m.subject)}</div>`;
              }).join('')}
              ${dayMeetingsList.length > 2 ? `<div class="cal-event-more">+${dayMeetingsList.length - 2} 更多...</div>` : ''}
            </div>"""

new_month_events = """            <div class="cal-day-events">
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
            </div>"""

assert old_month_events in code, "Could not find old_month_events"
code = code.replace(old_month_events, new_month_events)

# 12. Update renderMeetings (Cards List view) to display conflict banner
old_cards_list_render = """        return `
          <div class="meeting-card">
            <div class="meeting-card-top">
              <div class="meeting-title-area">
                <h3>
                  <span>${escapeHtml(m.subject)}</span>
                  ${pr}
                  <span class="status-badge ${st.cls}">${st.text}</span>
                </h3>"""

new_cards_list_render = """        const mConflicts = conflictMap[m.id] || [];
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
                ` : ''}"""

assert old_cards_list_render in code, "Could not find old_cards_list_render"
code = code.replace(old_cards_list_render, new_cards_list_render)

old_render_meetings_start = """function renderMeetings() {
  const meetings = getData(STORAGE_KEYS.MEETINGS);"""

new_render_meetings_start = """function renderMeetings() {
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const conflictMap = getAllMeetingConflicts(meetings);"""

assert old_render_meetings_start in code, "Could not find old_render_meetings_start"
code = code.replace(old_render_meetings_start, new_render_meetings_start)

with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully applied conflict detection & blackboard updates to assemble_final_app.py!")

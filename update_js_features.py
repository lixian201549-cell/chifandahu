import re

print("Reading assemble_final_app.py to update JS...")
with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Target start: // ================= 会议预约 (6 Key Secretary Fields) =================
# Target end: right before // Modal Form Actions function openAddMeetingModal()
# Let's locate the region
start_marker = "// ================= 会议预约 (6 Key Secretary Fields) ================="
end_marker = "// Modal Form Actions\nfunction openAddMeetingModal()"

if start_marker not in code or end_marker not in code:
    print("ERROR: Markers not found!")
    exit(1)

pre_part = code[:code.index(start_marker)]
post_part = code[code.index(end_marker):]

new_js = r"""// ================= 会议预约 (Secretary Desk & Dual View: Calendar + Cards) =================
let currentMeetingFilter = 'all';
let supervisorViewMode = 'cal_cards'; // 'cal_cards' | 'all_cards' | 'timeline_only'
let selectedTimelineDate = '';
let currentCalendarYearMonth = { year: 2026, month: 8 }; // 0-indexed month (8 = September)
let importPreviewTab = 'cal'; // 'cal' | 'card'

function setSupervisorViewMode(mode) {
  supervisorViewMode = mode;
  const btnCalCards = document.getElementById('btnViewCalCards');
  const btnAllCards = document.getElementById('btnViewAllCards');
  const btnTimeline = document.getElementById('btnViewTimeline');
  const modeTag = document.getElementById('currentViewModeTag');

  if (btnCalCards) btnCalCards.classList.toggle('active', mode === 'cal_cards');
  if (btnAllCards) btnAllCards.classList.toggle('active', mode === 'all_cards');
  if (btnTimeline) btnTimeline.classList.toggle('active', mode === 'timeline_only');

  if (modeTag) {
    if (mode === 'cal_cards') modeTag.textContent = '📅 月度日历 + 卡片视图';
    else if (mode === 'all_cards') modeTag.textContent = '🃏 全部日程卡片清单';
    else modeTag.textContent = '🕒 每日时间轴与空档';
  }

  renderMeetings();
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
  const todayStr = today.toISOString().slice(0, 10);
  currentCalendarYearMonth.year = today.getFullYear();
  currentCalendarYearMonth.month = today.getMonth();
  selectedTimelineDate = todayStr;
  const inputEl = document.getElementById('timelineDateSelector');
  if (inputEl) inputEl.value = todayStr;
  renderMeetings();
}

// ----------------- 月度日历渲染引擎 (Month Calendar Renderer) -----------------
function renderSupervisorMonthCalendar() {
  const calContainer = document.getElementById('supervisorMonthCalendarContainer');
  if (!calContainer) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const year = currentCalendarYearMonth.year;
  const month = currentCalendarYearMonth.month; // 0-indexed
  const todayStr = new Date().toISOString().slice(0, 10);

  if (!selectedTimelineDate) {
    selectedTimelineDate = todayStr;
  }

  // Count meetings in this month
  const monthPrefix = `${year}-${String(month + 1).padStart(2, '0')}`;
  const monthMeetings = meetings.filter(m => m.date && m.date.startsWith(monthPrefix) && m.status !== 'cancelled');
  let monthMins = 0;
  monthMeetings.forEach(m => { monthMins += parseInt(m.duration || 45, 10); });

  // Map meetings by date
  const meetingsByDate = {};
  meetings.forEach(m => {
    if (!m.date || m.status === 'cancelled') return;
    if (!meetingsByDate[m.date]) meetingsByDate[m.date] = [];
    meetingsByDate[m.date].push(m);
  });

  // Calculate grid dates
  const firstDay = new Date(year, month, 1);
  let startDayOfWeek = firstDay.getDay(); // 0 is Sunday
  if (startDayOfWeek === 0) startDayOfWeek = 7; // Convert to Mon=1..Sun=7
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
        <span>📅 本月排期会议：<strong style="color:var(--blue-accent);">${monthMeetings.length}</strong> 场</span>
        <span>⏱️ 累计排期时长：<strong>${(monthMins / 60).toFixed(1)}</strong> 小时</span>
      </div>
    </div>

    <table class="cal-grid-table">
      <thead>
        <tr>
          <th>周一</th>
          <th>周二</th>
          <th>周三</th>
          <th>周四</th>
          <th>周五</th>
          <th class="weekend">周六</th>
          <th class="weekend">周日</th>
        </tr>
      </thead>
      <tbody>
  `;

  let dayCounter = 1;
  let nextMonthDay = 1;

  for (let row = 0; row < 6; row++) {
    html += '<tr>';
    for (let col = 1; col <= 7; col++) {
      if (row === 0 && col < startDayOfWeek) {
        // Prev month days
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
        // Next month days
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
        // Current month day
        const curDateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(dayCounter).padStart(2, '0')}`;
        const isToday = curDateStr === todayStr;
        const isSelected = curDateStr === selectedTimelineDate;
        const dayMeetingsList = meetingsByDate[curDateStr] || [];

        let cellClasses = ['cal-day-cell'];
        if (isToday) cellClasses.push('today');
        if (isSelected) cellClasses.push('selected');

        html += `
          <td class="${cellClasses.join(' ')}" onclick="selectCalendarDate('${curDateStr}')">
            <div class="cal-day-header">
              <span class="cal-day-num">${dayCounter}</span>
              <div>
                ${isToday ? '<span class="cal-today-badge">今天</span>' : ''}
                ${dayMeetingsList.length > 0 ? `<span class="cal-meeting-count-badge">${dayMeetingsList.length}场</span>` : ''}
              </div>
            </div>
            <div class="cal-day-events">
              ${dayMeetingsList.slice(0, 2).map(m => {
                const stCls = m.status === 'scheduled' ? 'status-scheduled' : (m.status === 'completed' ? 'status-completed' : 'status-pending');
                return `<div class="cal-event-pill ${stCls}" title="${m.time} ${escapeHtml(m.subject)}">🕒 ${m.time} ${escapeHtml(m.subject)}</div>`;
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
function renderMeetings() {
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const listEl = document.getElementById('meetingCardsList');
  const dashListEl = document.getElementById('dashMeetingList');
  const calContainer = document.getElementById('supervisorMonthCalendarContainer');
  const timelineWrap = document.getElementById('supervisorTimelineWrap');
  const cardsToolbar = document.getElementById('cardsSectionToolbar');
  const cardsTitle = document.getElementById('cardsSectionTitle');
  const todayStr = new Date().toISOString().slice(0, 10);

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

  const pEl = document.getElementById('statPendingCount');
  const sEl = document.getElementById('statScheduledCount');
  const dEl = document.getElementById('statDurationSum');
  if (pEl) pEl.textContent = pendingCount;
  if (sEl) sEl.textContent = scheduledCount;
  if (dEl) dEl.textContent = (todayDurationMins / 60).toFixed(1) + 'h';

  // Toggle view elements based on supervisorViewMode
  if (supervisorViewMode === 'cal_cards') {
    if (calContainer) calContainer.style.display = 'block';
    if (timelineWrap) timelineWrap.style.display = 'block';
    if (cardsToolbar) cardsToolbar.style.display = 'flex';
    if (listEl) listEl.style.display = 'block';
    if (cardsTitle) cardsTitle.innerHTML = `🃏 选定日期【<strong>${selectedTimelineDate}</strong>】日程卡片详情`;
  } else if (supervisorViewMode === 'all_cards') {
    if (calContainer) calContainer.style.display = 'none';
    if (timelineWrap) timelineWrap.style.display = 'none';
    if (cardsToolbar) cardsToolbar.style.display = 'flex';
    if (listEl) listEl.style.display = 'block';
    if (cardsTitle) cardsTitle.innerHTML = `🃏 全部会议日程卡片清单 (按排期时间顺排)`;
  } else if (supervisorViewMode === 'timeline_only') {
    if (calContainer) calContainer.style.display = 'none';
    if (timelineWrap) timelineWrap.style.display = 'block';
    if (cardsToolbar) cardsToolbar.style.display = 'none';
    if (listEl) listEl.style.display = 'none';
  }

  // Render Month Calendar
  if (supervisorViewMode === 'cal_cards') {
    renderSupervisorMonthCalendar();
  }

  // Filter meetings for Cards View
  let filtered = meetings;
  if (supervisorViewMode === 'cal_cards') {
    filtered = meetings.filter(m => m.date === selectedTimelineDate);
  }

  if (currentMeetingFilter !== 'all') {
    filtered = filtered.filter(m => m.status === currentMeetingFilter);
  }

  filtered.sort((a, b) => {
    const da = (a.date || '') + ' ' + (a.time || '');
    const db = (b.date || '') + ' ' + (b.time || '');
    return da.localeCompare(db);
  });

  if (listEl && supervisorViewMode !== 'timeline_only') {
    if (filtered.length === 0) {
      listEl.innerHTML = `
        <div style="text-align:center; padding: 36px 20px; color: var(--text-muted); background:var(--card); border:1px dashed var(--border); border-radius:var(--radius-md);">
          <img src="${SNOOPY_ASSETS.supervisor_secretary}" style="width:48px; opacity:0.65; margin-bottom:8px;" alt="" />
          <p style="font-size:13.5px; font-weight:600; color:var(--text-secondary);">
            ${supervisorViewMode === 'cal_cards' ? `该日 (${selectedTimelineDate}) 暂无已安排的会议，全天空闲可随时预约！☕` : '暂无符合筛选条件的会议记录'}
          </p>
          <div style="margin-top:12px; display:flex; justify-content:center; gap:8px;">
            <button class="btn btn-sm btn-primary" onclick="openAddMeetingModalWithSlot('${selectedTimelineDate}', '10:00', 45)">➕ 为该日安排预约</button>
            <button class="btn btn-sm" onclick="openImportCalendarModal()">📥 智能导入表格/日历</button>
          </div>
        </div>`;
    } else {
      listEl.innerHTML = filtered.map(m => {
        const statusMap = {
          pending: { text: '🟡 待安排预约', cls: 'status-pending' },
          scheduled: { text: '🔵 已排期待开', cls: 'status-scheduled' },
          completed: { text: '🟢 会议已完成', cls: 'status-completed' },
          cancelled: { text: '⚪ 已取消/延期', cls: 'status-cancelled' }
        };
        const st = statusMap[m.status] || statusMap.pending;

        const priorityMap = {
          high: '<span class="priority-badge priority-high">🔴 紧急决议</span>',
          medium: '<span class="priority-badge priority-medium">🟡 常规业务</span>',
          routine: '<span class="priority-badge priority-low">🟢 例行汇报</span>'
        };
        const pr = priorityMap[m.priority] || priorityMap.medium;

        return `
          <div class="meeting-card">
            <div class="meeting-card-top">
              <div class="meeting-title-area">
                <h3>
                  <span>${escapeHtml(m.subject)}</span>
                  ${pr}
                  <span class="status-badge ${st.cls}">${st.text}</span>
                </h3>
                <div class="meeting-meta-row">
                  <span class="meta-chip">🕒 <strong>时间：</strong>${m.date} ${m.time}</span>
                  <span class="meta-chip">⏱️ <strong>时长：</strong>${m.duration || 45} 分钟</span>
                  <span class="meta-chip">📍 <strong>地点：</strong>${escapeHtml(m.location || '主管办公室')}</span>
                  <span class="meta-chip">👥 <strong>与会人/汇报人：</strong>${escapeHtml(m.attendees)}</span>
                </div>
              </div>

              <button class="btn btn-sm" onclick="copySingleMeetingNotice(${m.id})" title="复制该会议的完整通知格式至剪贴板">📋 复制通知</button>
            </div>

            <div class="meeting-card-body">
              <div class="field-block">
                <div class="field-label">📖 会议背景 (Background & Context)</div>
                <div class="field-val">${escapeHtml(m.background)}</div>
              </div>

              <div class="field-block">
                <div class="field-label">🎯 核心决策点 (Decision Points - 待主管定夺)</div>
                <div class="field-val decision-val">${escapeHtml(m.decision)}</div>
              </div>
            </div>

            <div class="meeting-card-footer">
              <div class="requester-info">
                <span>👤 预约人/汇报人：${escapeHtml(m.requester || '未注明')}</span>
                ${m.notes ? ` · <span style="color:#d97706;">💡 秘书备忘：${escapeHtml(m.notes)}</span>` : ''}
              </div>

              <div class="meeting-actions">
                ${m.status !== 'completed' ? `<button class="btn btn-sm btn-ghost" onclick="updateMeetingStatus(${m.id}, 'completed')">✅ 标记完成</button>` : ''}
                ${m.status === 'pending' ? `<button class="btn btn-sm btn-primary" onclick="updateMeetingStatus(${m.id}, 'scheduled')">🔵 确认排期</button>` : ''}
                <button class="btn btn-sm btn-ghost" onclick="editMeeting(${m.id})">✏️ 编辑</button>
                <button class="btn btn-sm btn-ghost" style="color:#dc2626;" onclick="deleteMeeting(${m.id})">🗑️ 删除</button>
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
      dashListEl.innerHTML = '<div style="color:var(--text-muted); font-size:12px; text-align:center; padding:12px;">今日暂无待开会议，日程轻松从容 ☕</div>';
    } else {
      dashListEl.innerHTML = upcoming.map(m => `
        <div style="padding:9px 12px; background:var(--card-subtle); border:1px solid var(--border); border-radius:var(--radius-sm); margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-size:13px; font-weight:700; color:var(--text-primary);">${escapeHtml(m.subject)}</div>
            <div style="font-size:11.5px; color:var(--text-secondary); margin-top:2px;">
              🕒 ${m.date} ${m.time} (${m.duration}分) · 👥 ${escapeHtml(m.attendees)}
            </div>
          </div>
          <button class="btn btn-sm" onclick="copySingleMeetingNotice(${m.id})">📋 复制</button>
        </div>
      `).join('');
    }
  }

  renderSupervisorTimeline(meetings);
}

function filterMeetings(type) {
  currentMeetingFilter = type;
  document.querySelectorAll('#cardStatusFilters .filter-btn').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-filter') === type);
  });
  renderMeetings();
}

// ================= TIMELINE & AUTOMATIC FREE-SLOT DETECTION =================
function calculateDayFreeSlots(meetings, dateStr) {
  const dayStart = 8 * 60 + 30; // 08:30 = 510
  const lunchStart = 12 * 60;   // 12:00 = 720
  const lunchEnd = 14 * 60;     // 14:00 = 840
  const dayEnd = 18 * 60;       // 18:00 = 1080

  const dayMeetings = meetings.filter(m => m.date === dateStr && m.status !== 'cancelled');

  const busyIntervals = [];
  dayMeetings.forEach(m => {
    const parts = (m.time || '10:00').split(':').map(Number);
    const start = parts[0] * 60 + parts[1];
    const dur = parseInt(m.duration || 45, 10);
    const end = start + dur;
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

  return { dayMeetings, busyIntervals, freeSlots };
}

function minutesToTimeStr(mins) {
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return (h < 10 ? '0' + h : '' + h) + ':' + (m < 10 ? '0' + m : '' + m);
}

function renderSupervisorTimeline(meetings) {
  const track = document.getElementById('supervisorTimelineTrack');
  const pillsEl = document.getElementById('timelineFreeSlotsPills');
  const badgeEl = document.getElementById('timelineFreeCountBadge');
  if (!track) return;

  const todayStr = new Date().toISOString().slice(0, 10);
  if (!selectedTimelineDate) selectedTimelineDate = todayStr;

  const { dayMeetings, freeSlots } = calculateDayFreeSlots(meetings, selectedTimelineDate);

  if (badgeEl) {
    badgeEl.innerHTML = `<span style="color:#16a34a; font-weight:700;">🟢 自动识别 ${freeSlots.length} 处可排期空档</span> · 当日已安排 ${dayMeetings.length} 场会议`;
  }

  // Render Visual Timeline Graphic
  const slots = [
    { label: '08:30', hour: 8.5 },
    { label: '09:00', hour: 9 },
    { label: '10:00', hour: 10 },
    { label: '11:00', hour: 11 },
    { label: '12:00', hour: 12, isLunch: true },
    { label: '13:00', hour: 13, isLunch: true },
    { label: '14:00', hour: 14 },
    { label: '15:00', hour: 15 },
    { label: '16:00', hour: 16 },
    { label: '17:00', hour: 17 },
    { label: '18:00', hour: 18 }
  ];

  track.innerHTML = slots.map(s => {
    if (s.isLunch) {
      return `<div class="time-slot slot-lunch" style="flex:1;" title="${s.label} 约定午休与充能时段">${s.label} 午休</div>`;
    }
    const busy = dayMeetings.find(m => {
      const parts = (m.time || '00:00').split(':').map(Number);
      const startH = parts[0] + parts[1] / 60;
      const endH = startH + (parseInt(m.duration || 45, 10) / 60);
      return s.hour >= startH && s.hour < endH;
    });

    if (busy) {
      return `<div class="time-slot slot-busy" style="flex:1;" onclick="editMeeting(${busy.id})" title="【已排期】${busy.time} ${escapeHtml(busy.subject)} (${busy.duration}分) · 点击查看">${s.label} ${escapeHtml(busy.subject.slice(0, 5))}</div>`;
    }

    const free = freeSlots.find(f => {
      const st = f.start / 60;
      const et = f.end / 60;
      return s.hour >= st && s.hour < et;
    });

    if (free) {
      return `<div class="time-slot slot-free" style="flex:1;" onclick="openAddMeetingModalWithSlot('${selectedTimelineDate}', '${free.startStr}', ${Math.min(free.duration, 45)})" title="【空档时间】${free.startStr} - ${free.endStr} (${free.duration}分钟可用) · 点击直接排期">${s.label} 可排期</div>`;
    }

    return `<div class="time-slot slot-free" style="flex:1;" onclick="openAddMeetingModalWithSlot('${selectedTimelineDate}', '${s.label}', 45)" title="${s.label} 空档 · 点击直接排期">${s.label} 空闲</div>`;
  }).join('');

  // Render Free-slot Action Chips
  if (pillsEl) {
    if (freeSlots.length === 0) {
      pillsEl.innerHTML = '<span style="font-size:11.5px; color:var(--text-muted);">今日各时段均已排满，暂无可调度的大块空档</span>';
    } else {
      pillsEl.innerHTML = `
        <span style="font-size:11.5px; font-weight:700; color:var(--text-secondary);">💡 推荐可排期空档（点击快速预约）：</span>
        ${freeSlots.map(f => `
          <button class="free-pill-btn" onclick="openAddMeetingModalWithSlot('${selectedTimelineDate}', '${f.startStr}', ${Math.min(f.duration, 45)})" title="点击直接预定该时段预约 (${f.startStr} - ${f.endStr})">
            <span>🟢 ${f.startStr} - ${f.endStr}</span>
            <span style="font-size:10px; opacity:0.8;">(${f.duration}m)</span>
            <span style="font-weight:normal;">＋</span>
          </button>
        `).join('')}
      `;
    }
  }
}

function openAddMeetingModalWithSlot(date, startTime, duration) {
  openAddMeetingModal();
  if (date) document.getElementById('inputMeetingDate').value = date;
  if (startTime) document.getElementById('inputMeetingTime').value = startTime;
  if (duration) setMeetingDuration(duration);
  showToast(`已为您自动填入推荐空档：${date} ${startTime} (${duration}分钟)`);
}

// ================= UNIVERSAL SMART CALENDAR & TABLE IMPORT ENGINE =================
let parsedImportMeetings = [];

function openImportCalendarModal() {
  const todayStr = new Date().toISOString().slice(0, 10);
  document.getElementById('importTargetDate').value = selectedTimelineDate || todayStr;
  document.getElementById('inputImportTableText').value = '';
  document.getElementById('importLivePreviewArea').style.display = 'none';
  document.getElementById('btnConfirmImport').disabled = true;
  parsedImportMeetings = [];
  openModal('importCalendarModal');
}

// In-browser XLSX ZIP Reader supporting Excel .xlsx files
async function readXlsxFile(file) {
  try {
    const arrayBuffer = await file.arrayBuffer();
    const bytes = new Uint8Array(arrayBuffer);

    // Scan ZIP entries
    const entries = {};
    let pos = 0;
    while (pos + 30 <= bytes.length) {
      if (bytes[pos] !== 0x50 || bytes[pos+1] !== 0x4b || bytes[pos+2] !== 0x03 || bytes[pos+3] !== 0x04) break;
      const method = bytes[pos+8] | (bytes[pos+9] << 8);
      const compSize = bytes[pos+18] | (bytes[pos+19] << 8) | (bytes[pos+20] << 16) | (bytes[pos+21] << 24);
      const fnameLen = bytes[pos+26] | (bytes[pos+27] << 8);
      const extraLen = bytes[pos+28] | (bytes[pos+29] << 8);
      const fnameBytes = bytes.slice(pos + 30, pos + 30 + fnameLen);
      const fname = new TextDecoder('utf-8').decode(fnameBytes);
      const dataStart = pos + 30 + fnameLen + extraLen;
      const compData = bytes.slice(dataStart, dataStart + compSize);
      entries[fname] = { method, data: compData };
      pos = dataStart + compSize;
    }

    async function decompress(entry) {
      if (!entry) return '';
      if (entry.method === 0) return new TextDecoder('utf-8').decode(entry.data);
      if (entry.method === 8 && typeof DecompressionStream !== 'undefined') {
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
      }
      return '';
    }

    const sstXml = await decompress(entries['xl/sharedStrings.xml']);
    const sheetEntry = entries['xl/worksheets/sheet1.xml'] || entries['xl/worksheets/sheet.xml'] || Object.entries(entries).find(([k]) => k.startsWith('xl/worksheets/'))?.[1];
    const sheetXml = await decompress(sheetEntry);

    const strings = [];
    if (sstXml) {
      const siMatches = sstXml.match(/<si>[\s\S]*?<\/si>/g) || [];
      for (const si of siMatches) {
        const tMatches = si.match(/<t[^>]*>([\s\S]*?)<\/t>/g) || [];
        const text = tMatches.map(m => m.replace(/<[^>]+>/g, '')).join('');
        strings.push(text);
      }
    }

    const rows = [];
    if (sheetXml) {
      const rowMatches = sheetXml.match(/<row[^>]*>[\s\S]*?<\/row>/g) || [];
      for (const r of rowMatches) {
        const cellMatches = r.match(/<c[^>]*>[\s\S]*?<\/c>/g) || [];
        const rowVals = [];
        for (const c of cellMatches) {
          const isString = /t="s"/.test(c);
          const valMatch = c.match(/<v>([^<]*)<\/v>/);
          if (valMatch) {
            const val = valMatch[1];
            rowVals.push(isString ? (strings[parseInt(val, 10)] || '') : val);
          } else {
            const inlineMatch = c.match(/<t[^>]*>([\s\S]*?)<\/t>/);
            if (inlineMatch) rowVals.push(inlineMatch[1]);
          }
        }
        if (rowVals.length > 0) rows.push(rowVals.join('\t'));
      }
    }
    return rows.join('\n');
  } catch (err) {
    console.warn('XLSX native extraction error, falling back to text:', err);
    return null;
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

  // General text reading fallback
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
    "【2026-09-24】",
    "09:30 - 10:15\t中东北非区域 Q3 交付资源评审\t张总(地南代)\t审批重点交付架构师驻场支持",
    "11:00 - 11:45\t喀麦隆重点交付工程方案终审\t李总(开罗交付部)\t终审喀麦隆大客户交付方案",
    "【2026-09-25】",
    "14:30 - 15:15\t阿尔及利亚代表处外汇与回款复盘\t王总(阿尔及尔)\t特批账期与外汇风险收敛",
    "16:30 - 17:15\t8代表处跨区行政响应与协同机制\t区域综合秘书处\t明确紧急调度通道",
    "【微信通知样例】",
    "明天下午15:00在1号会议室召开刚果金代表处业务对齐会，请陈部长汇报业务进展，预计时长45分钟，需审批工程预算。"
  ].join('\n');

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

// Universal Schedule Text Parser (Handles Tables, Chat Notifications, Mixed Bullets, Free Text)
function parseUniversalScheduleText(rawText, defaultDate) {
  if (!rawText || !rawText.trim()) return [];
  const lines = rawText.trim().split(/\r?\n/);
  const results = [];
  let currentDate = defaultDate || new Date().toISOString().slice(0, 10);
  const curYear = new Date().getFullYear();

  for (let originalLine of lines) {
    let line = originalLine.trim();
    if (!line) continue;

    // Check if line is a date section header, e.g. 【2026-09-25】 or 9月25日日程
    const headerDateMatch = line.match(/(?:【|\[)?(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|(?:\d{1,2}月\d{1,2}[日号]?))(?:日程|安排|会议|】|\]|:)?/);
    if (headerDateMatch && line.length <= 25 && !/\d{1,2}:\d{2}/.test(line)) {
      const dStr = headerDateMatch[1];
      if (dStr.includes('月')) {
        const md = dStr.match(/\d+/g);
        currentDate = `${curYear}-${md[0].padStart(2, '0')}-${md[1].padStart(2, '0')}`;
      } else {
        const parts = dStr.split(/[-/.]/);
        currentDate = `${parts[0]}-${parts[1].padStart(2, '0')}-${parts[2].padStart(2, '0')}`;
      }
      continue;
    }

    // Skip table column header lines
    if (/^(序号|时间|日期|主题|会议|汇报|与会|Time|Date|Subject|Presenter)/i.test(line)) {
      continue;
    }

    let itemDate = currentDate;

    // Check inline date in the line
    const inlineDateMatch = line.match(/(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})/);
    if (inlineDateMatch) {
      const parts = inlineDateMatch[1].split(/[-/.]/);
      itemDate = `${parts[0]}-${parts[1].padStart(2, '0')}-${parts[2].padStart(2, '0')}`;
      line = line.replace(inlineDateMatch[0], ' ');
    } else {
      const mdMatch = line.match(/(\d{1,2})月(\d{1,2})[日号]?/);
      if (mdMatch) {
        itemDate = `${curYear}-${mdMatch[1].padStart(2, '0')}-${mdMatch[2].padStart(2, '0')}`;
        line = line.replace(mdMatch[0], ' ');
      } else if (line.includes('明天')) {
        const d = new Date(); d.setDate(d.getDate() + 1);
        itemDate = d.toISOString().slice(0, 10);
        line = line.replace('明天', ' ');
      } else if (line.includes('后天')) {
        const d = new Date(); d.setDate(d.getDate() + 2);
        itemDate = d.toISOString().slice(0, 10);
        line = line.replace('后天', ' ');
      } else if (line.includes('今天')) {
        itemDate = new Date().toISOString().slice(0, 10);
        line = line.replace('今天', ' ');
      }
    }

    // Time & Duration extraction
    let startTime = '10:00';
    let duration = 45;

    // Match Range: 10:00 - 10:45
    const rangeMatch = line.match(/(\d{1,2}:\d{2})\s*[-~至到与]\s*(\d{1,2}:\d{2})/);
    if (rangeMatch) {
      startTime = padTime(rangeMatch[1]);
      const endTime = padTime(rangeMatch[2]);
      const [sh, sm] = startTime.split(':').map(Number);
      const [eh, em] = endTime.split(':').map(Number);
      const diff = (eh * 60 + em) - (sh * 60 + sm);
      if (diff > 0 && diff <= 480) duration = diff;
      line = line.replace(rangeMatch[0], ' ');
    } else {
      // Chinese clock range: 下午2点半至3点15分
      const cnRange = line.match(/(上午|下午|晚上)?\s*(\d{1,2})(?:点|时)(半|\d{1,2}分)?\s*[-~至到]\s*(上午|下午|晚上)?\s*(\d{1,2})(?:点|时)(半|\d{1,2}分)?/);
      if (cnRange) {
        const p1 = cnRange[1], h1 = cnRange[2], m1 = cnRange[3];
        const p2 = cnRange[4], h2 = cnRange[5], m2 = cnRange[6];
        let hour1 = parseInt(h1, 10) + ((p1 === '下午' || p1 === '晚上') && parseInt(h1, 10) < 12 ? 12 : 0);
        let min1 = m1 === '半' ? 30 : (m1 ? parseInt(m1.match(/\d+/)[0], 10) : 0);
        let hour2 = parseInt(h2, 10) + (((p2 || p1) === '下午' || (p2 || p1) === '晚上') && parseInt(h2, 10) < 12 ? 12 : 0);
        let min2 = m2 === '半' ? 30 : (m2 ? parseInt(m2.match(/\d+/)[0], 10) : 0);
        startTime = `${String(hour1).padStart(2, '0')}:${String(min1).padStart(2, '0')}`;
        const diff = (hour2 * 60 + min2) - (hour1 * 60 + min1);
        if (diff > 0 && diff <= 480) duration = diff;
        line = line.replace(cnRange[0], ' ');
      } else {
        // Single clock time: 14:30
        const singleMatch = line.match(/(?:上午|下午|晚上)?\s*(\d{1,2}:\d{2})/);
        if (singleMatch) {
          let [h, m] = singleMatch[1].split(':').map(Number);
          if (singleMatch[0].includes('下午') && h < 12) h += 12;
          startTime = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
          line = line.replace(singleMatch[0], ' ');
        } else {
          // Chinese single: 上午10点 or 下午3点半
          const cnSingle = line.match(/(上午|下午|晚上)?\s*(\d{1,2})(?:点|时)(半|\d{1,2}分)?/);
          if (cnSingle) {
            let hour = parseInt(cnSingle[2], 10) + ((cnSingle[1] === '下午' || cnSingle[1] === '晚上') && parseInt(cnSingle[2], 10) < 12 ? 12 : 0);
            let min = cnSingle[3] === '半' ? 30 : (cnSingle[3] ? parseInt(cnSingle[3].match(/\d+/)[0], 10) : 0);
            startTime = `${String(hour).padStart(2, '0')}:${String(min).padStart(2, '0')}`;
            line = line.replace(cnSingle[0], ' ');
          }
        }
      }
    }

    // Explicit duration: 45分钟, 1小时, 1.5小时
    const hourDurMatch = line.match(/(\d+(?:\.\d+)?)\s*(?:小时|h)/i);
    if (hourDurMatch) {
      duration = Math.round(parseFloat(hourDurMatch[1]) * 60);
      line = line.replace(hourDurMatch[0], ' ');
    } else {
      const minDurMatch = line.match(/(\d{1,3})\s*(?:分钟|min|m)/i);
      if (minDurMatch) {
        duration = parseInt(minDurMatch[1], 10);
        line = line.replace(minDurMatch[0], ' ');
      }
    }

    // Location extraction: 在1号会议室
    let location = '主管办公室';
    const locMatch = line.match(/(?:在|地点[：:\s]*)([\w\u4e00-\u9fa5]+(?:会议室|办公室|大厅|楼|座))/);
    if (locMatch) {
      location = locMatch[1];
      line = line.replace(locMatch[0], ' ');
    }

    // Reporter extraction
    let reporter = '';
    const repMatch = line.match(/(?:汇报人|汇报专家|主讲人|发言人|主讲|对接人|发起人)[：:\s]*([^\s,，。；;\t]+)/);
    if (repMatch) {
      reporter = repMatch[1];
      line = line.replace(repMatch[0], ' ');
    } else {
      const verbMatch = line.match(/([^\s,，。；;\t]{2,6})(?:汇报|发言|主讲)/);
      if (verbMatch) {
        reporter = verbMatch[1].replace(/^请/, '');
        line = line.replace(verbMatch[0], ' ');
      }
    }

    // Decision point extraction
    let decision = '';
    const decMatch = line.match(/(?:决策点|决策事项|核心决策|议题|目标)[：:\s]*([^\n。；;]+)/);
    if (decMatch) {
      decision = decMatch[1].trim();
      line = line.replace(decMatch[0], ' ');
    }

    // Clean remaining words to form Subject
    line = line.replace(/请[^\s,，。；;\t]{2,6}(?=汇报|发言)/g, '');
    for (const w of ['召开', '进行', '讨论', '沟通', '业务进展', '会议通知', '各位同事', '预计时长', '时间', '地点']) {
      line = line.split(w).join(' ');
    }

    // Split by tabs or commas if tabular
    let parts = line.split(/[\t,;|]+|\s{2,}/).map(s => s.trim()).filter(Boolean);
    if (!reporter && parts.length >= 2) {
      for (let i = 0; i < parts.length; i++) {
        const p = parts[i];
        if (/(总|部长|经理|主任|处长|专家|秘书|HR|VP|代|办)/.test(p) && p.length <= 8) {
          reporter = p;
          parts.splice(i, 1);
          break;
        }
      }
    }

    let subject = parts.join(' ');
    subject = subject.replace(/^[0-9一二三四五六七八九十]+[、.\s]+/, ''); // remove leading 1. 2.
    subject = subject.replace(/[\s,，。；;]+$/, '').trim();
    if (!subject || subject.length < 2) {
      subject = '主管业务交流与议程对齐';
    }

    if (!decision) {
      decision = `1. 审议《${subject}》关键诉求，明确后续落地步骤与资源支持。`;
    }

    const attendees = reporter ? (reporter.includes('主管') ? reporter : '主管、' + reporter) : '主管、相关参会人';

    results.push({
      id: Date.now() + Math.floor(Math.random() * 1000000),
      date: itemDate,
      time: startTime,
      duration: duration,
      subject: subject,
      background: `由智能日程引擎自动识别规整：${subject}。需根据汇报人材料跟进具体业务背景。`,
      decision: decision,
      attendees: attendees,
      requester: reporter || '智能导入',
      location: location,
      status: 'scheduled',
      priority: 'medium',
      notes: '由自由格式智能识别规整生成'
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
  const targetDate = document.getElementById('importTargetDate').value || new Date().toISOString().slice(0, 10);
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

    // Collect dates
    const datesSet = new Set(parsedImportMeetings.map(m => m.date));
    statusText.textContent = `🟢 智能识别成功：已规整 ${parsedImportMeetings.length} 场会议，涉及 ${datesSet.size} 个日期`;

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
              <th style="width:110px;">时间与时长</th>
              <th>会议主题</th>
              <th style="width:140px;">汇报人 / 与会人</th>
            </tr>
          </thead>
          <tbody>
            ${list.map(m => `
              <tr>
                <td><strong>${m.time}</strong> (${m.duration}分)</td>
                <td>${escapeHtml(m.subject)}</td>
                <td>${escapeHtml(m.attendees)}</td>
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
          <div style="font-size:13px; font-weight:700; color:var(--text-primary);">${escapeHtml(m.subject)}</div>
          <span class="status-badge status-scheduled">已识别排期</span>
        </div>
        <div style="font-size:11.5px; color:var(--text-secondary); display:flex; flex-wrap:wrap; gap:10px; margin-bottom:4px;">
          <span>📅 ${m.date}</span>
          <span>🕒 ${m.time} (${m.duration}分钟)</span>
          <span>👥 ${escapeHtml(m.attendees)}</span>
          <span>📍 ${escapeHtml(m.location)}</span>
        </div>
        <div style="font-size:11.5px; color:var(--text-muted); background:#f4f4f5; padding:4px 8px; border-radius:4px;">
          <strong>🎯 决策点：</strong>${escapeHtml(m.decision)}
        </div>
      </div>
    `).join('');
  }
}

function confirmImportCalendar() {
  if (parsedImportMeetings.length === 0) return;

  let existing = getData(STORAGE_KEYS.MEETINGS);
  // Merge imported meetings
  const updated = [...parsedImportMeetings, ...existing];
  setData(STORAGE_KEYS.MEETINGS, updated);

  // Jump to first imported meeting date
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
  showToast(`🎉 成功导入并规整 ${parsedImportMeetings.length} 场会议！日历与卡片已自动更新！`);
}

"""

# Combine parts
updated_code = pre_part + new_js + post_part

# Now let's enrich initSeeds with multi-day seed meetings for September 2026
seeds_target = """  if (!localStorage.getItem(STORAGE_KEYS.MEETINGS)) {
    setData(STORAGE_KEYS.MEETINGS, [
      {
        id: 1,
        date: todayStr,
        time: "10:00",
        duration: 45,
        subject: "中东北非区域 Q3 交付资源倾斜及关键决策评审",
        background: "喀麦隆与科特迪瓦代表处重点工程交付进入攻坚期，一线技术专家面临紧缺，需主管定夺是否从地区部统一调配高级技术专家现场支援并追加差旅额度。",
        decision: "1. 是否同意科特迪瓦代表处追加2名资深交付架构师驻场？\\n2. 喀麦隆大客户合同备件本地采购预算审批通过与否？",
        attendees: "主管、李总(开罗交付部)、张总(科特迪瓦代)、财务BP、HRG",
        requester: "地区部交付与服务部 · 王秘书",
        location: "主管办公室 / 线上 WeLink 889-201",
        status: "scheduled",
        priority: "high",
        notes: "已提前打印现场风险排查表与两代表处人员盘点清单"
      },
      {
        id: 2,
        date: todayStr,
        time: "14:30",
        duration: 30,
        subject: "刚果（金）及阿尔及利亚代表处月度经营例行汇报",
        background: "阿尔及利亚代表处受当地外汇管制影响，部分重点客户回款面临超期风险，特向主管当面汇报风险收敛措施并申请政策特批。",
        decision: "1. 阿尔及利亚客户付款账期延长申请是否特批？\\n2. 刚果（金）办事处新安保防护方案终审确认。",
        attendees: "主管、阿尔及利亚代代表、刚果代代表、法务BP",
        requester: "刚果代表处秘书处",
        location: "1号会议室",
        status: "scheduled",
        priority: "medium",
        notes: "提醒主管会前签字授权委托书"
      },
      {
        id: 3,
        date: todayStr,
        time: "16:30",
        duration: 45,
        subject: "8 代表处跨区协同机制与行政支持新规范汇报",
        background: "梳理跨开罗(UTC+2)、阿尔及尔(UTC+1)、阿比让(UTC+0)等不同时区的行政响应标准，建立秘书处跨时区紧急调度绿色通道。",
        decision: "1. 跨时区通用会议窗口是否固定为开罗时间 11:00 - 17:00？\\n2. 统一差旅紧急代订与商务接待标准确认。",
        attendees: "主管、区域行政总监、各代表处综合行政主管",
        requester: "区域综合秘书处",
        location: "主管办公室",
        status: "pending",
        priority: "routine",
        notes: "需提前准备各代表处时差对比对照表"
      }
    ]);
  }"""

seeds_replacement = """  if (!localStorage.getItem(STORAGE_KEYS.MEETINGS)) {
    const d1 = new Date(); d1.setDate(d1.getDate() + 1);
    const dateTomorrow = d1.toISOString().slice(0, 10);
    const d2 = new Date(); d2.setDate(d2.getDate() + 2);
    const dateDayAfter = d2.toISOString().slice(0, 10);
    const d3 = new Date(); d3.setDate(d3.getDate() + 5);
    const dateNextWeek = d3.toISOString().slice(0, 10);

    setData(STORAGE_KEYS.MEETINGS, [
      {
        id: 1,
        date: todayStr,
        time: "10:00",
        duration: 45,
        subject: "中东北非区域 Q3 交付资源倾斜及关键决策评审",
        background: "喀麦隆与科特迪瓦代表处重点工程交付进入攻坚期，一线技术专家面临紧缺，需主管定夺是否从地区部统一调配高级技术专家现场支援并追加差旅额度。",
        decision: "1. 是否同意科特迪瓦代表处追加2名资深交付架构师驻场？\\n2. 喀麦隆大客户合同备件本地采购预算审批通过与否？",
        attendees: "主管、李总(开罗交付部)、张总(科特迪瓦代)、财务BP、HRG",
        requester: "地区部交付与服务部 · 王秘书",
        location: "主管办公室 / 线上 WeLink 889-201",
        status: "scheduled",
        priority: "high",
        notes: "已提前打印现场风险排查表与两代表处人员盘点清单"
      },
      {
        id: 2,
        date: todayStr,
        time: "14:30",
        duration: 30,
        subject: "刚果（金）及阿尔及利亚代表处月度经营例行汇报",
        background: "阿尔及利亚代表处受当地外汇管制影响，部分重点客户回款面临超期风险，特向主管当面汇报风险收敛措施并申请政策特批。",
        decision: "1. 阿尔及利亚客户付款账期延长申请是否特批？\\n2. 刚果（金）办事处新安保防护方案终审确认。",
        attendees: "主管、阿尔及利亚代代表、刚果代代表、法务BP",
        requester: "刚果代表处秘书处",
        location: "1号会议室",
        status: "scheduled",
        priority: "medium",
        notes: "提醒主管会前签字授权委托书"
      },
      {
        id: 3,
        date: todayStr,
        time: "16:30",
        duration: 45,
        subject: "8 代表处跨区协同机制与行政支持新规范汇报",
        background: "梳理跨开罗(UTC+2)、阿尔及尔(UTC+1)、阿比让(UTC+0)等不同时区的行政响应标准，建立秘书处跨时区紧急调度绿色通道。",
        decision: "1. 跨时区通用会议窗口是否固定为开罗时间 11:00 - 17:00？\\n2. 统一差旅紧急代订与商务接待标准确认。",
        attendees: "主管、区域行政总监、各代表处综合行政主管",
        requester: "区域综合秘书处",
        location: "主管办公室",
        status: "pending",
        priority: "routine",
        notes: "需提前准备各代表处时差对比对照表"
      },
      {
        id: 4,
        date: dateTomorrow,
        time: "11:00",
        duration: 45,
        subject: "摩洛哥代表处高层客户来访接待与商机定夺",
        background: "摩洛哥大客户代表团将于开罗中转，特申请主管当面会见并敲定战略合作备忘录。",
        decision: "1. 敲定联合实验室共建框架；\\n2. 审批定制化交付条款让利权限。",
        attendees: "主管、摩洛哥总代表、商务专家",
        requester: "摩洛哥代表处总办",
        location: "贵宾会客室",
        status: "scheduled",
        priority: "high",
        notes: "已确认阿拉伯语与法语同声传译就位"
      },
      {
        id: 5,
        date: dateTomorrow,
        time: "15:00",
        duration: 60,
        subject: "塞内加尔达喀尔港口工程回款攻坚专题会",
        background: "塞内加尔达喀尔重点港口工程进入整体验收阶段，梳理回款时间表并部署防范风险预案。",
        decision: "1. 确定下阶段付款节点追讨策略；\\n2. 批准补充备件保修函签署。",
        attendees: "主管、塞内加尔总代表、交付总监、法务部",
        requester: "西非项目群经理",
        location: "2号会议室",
        status: "scheduled",
        priority: "medium",
        notes: "需准备西非法郎外汇对冲分析表"
      },
      {
        id: 6,
        date: dateDayAfter,
        time: "10:30",
        duration: 45,
        subject: "埃及代表处本地化人才梯队建设汇报",
        background: "深化埃及与北非本地技术专家招聘与培养，建立开罗中枢培训基地。",
        decision: "1. 审批2026-2027年度本地大学联合培养计划预算。",
        attendees: "主管、区域人力资源总监、开罗培训中心负责人",
        requester: "地区部HRBP",
        location: "主管办公室",
        status: "pending",
        priority: "routine",
        notes: "会前准备开罗大学合作协议草案"
      }
    ]);
  }"""

if seeds_target in updated_code:
    updated_code = updated_code.replace(seeds_target, seeds_replacement, 1)
    print("Seeds updated successfully.")
else:
    print("WARNING: seeds_target not found!")

with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
    f.write(updated_code)

print("Assemble script part 2 (JS logic) written successfully.")

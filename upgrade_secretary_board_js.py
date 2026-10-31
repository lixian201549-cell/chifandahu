import re

print("Reading assemble_final_app.py...")
with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Locate the meeting JS section
start_marker = "// ================= 会议预约 (Secretary Desk & Dual View: Calendar + Cards) ================="
end_marker = "function editMeeting(id) {"

if start_marker not in code or end_marker not in code:
    print("ERROR: Markers not found!")
    exit(1)

pre_part = code[:code.index(start_marker)]
post_part = code[code.index(end_marker):]

new_js = r"""// ================= 会议预约 (Secretary Desk & Executive Weekly/Monthly Board) =================
let currentMeetingFilter = 'all';
let supervisorViewMode = 'week_board'; // 'week_board' | 'month_cal' | 'card_list'
let selectedTimelineDate = '';
let currentWeekOffset = 0; // 0 = current week, -1 = last week, +1 = next week
let currentCalendarYearMonth = { year: 2026, month: 8 }; // 0-indexed month (8 = September)
let importPreviewTab = 'cal'; // 'cal' | 'card'

function setSupervisorViewMode(mode) {
  supervisorViewMode = mode;
  const btnWeekBoard = document.getElementById('btnViewWeekBoard');
  const btnMonthCal = document.getElementById('btnViewMonthCal');
  const btnCardList = document.getElementById('btnViewCardList');
  const modeTag = document.getElementById('currentViewModeTag');

  if (btnWeekBoard) btnWeekBoard.classList.toggle('active', mode === 'week_board');
  if (btnMonthCal) btnMonthCal.classList.toggle('active', mode === 'month_cal');
  if (btnCardList) btnCardList.classList.toggle('active', mode === 'card_list');

  if (modeTag) {
    if (mode === 'week_board') modeTag.textContent = '📅 本周日历看板 · 领导一眼看懂';
    else if (mode === 'month_cal') modeTag.textContent = '🗓️ 月度全景日历 · 宏观统筹';
    else modeTag.textContent = '🃏 决策卡片清单 · 细节跟进';
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
  selectedTimelineDate = new Date().toISOString().slice(0, 10);
  renderSupervisorWeeklyBoard();
}

// ----------------- 领导本周日历看板渲染引擎 (Executive Weekly Board) -----------------
function renderSupervisorWeeklyBoard() {
  const boardContainer = document.getElementById('supervisorWeeklyBoardContainer');
  if (!boardContainer) return;

  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const today = new Date();
  const todayStr = today.toISOString().slice(0, 10);

  // Compute Monday of the displayed week
  let dayOfWeek = today.getDay();
  if (dayOfWeek === 0) dayOfWeek = 7;
  const monDate = new Date(today);
  monDate.setDate(today.getDate() - (dayOfWeek - 1) + (currentWeekOffset * 7));

  const weekDays = [];
  const weekdayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];

  for (let i = 0; i < 7; i++) {
    const d = new Date(monDate);
    d.setDate(monDate.getDate() + i);
    const dStr = d.toISOString().slice(0, 10);
    weekDays.push({
      dateStr: dStr,
      month: d.getMonth() + 1,
      day: d.getDate(),
      name: weekdayNames[i],
      isToday: (dStr === todayStr),
      isWeekend: (i >= 5)
    });
  }

  // Check if weekend has meetings
  const hasWeekendMeetings = meetings.some(m => {
    return (m.date === weekDays[5].dateStr || m.date === weekDays[6].dateStr) && m.status !== 'cancelled';
  });

  const displayDays = hasWeekendMeetings ? weekDays : weekDays.slice(0, 5);

  // Calculate week stats
  const weekStartStr = weekDays[0].dateStr;
  const weekEndStr = weekDays[4].dateStr;
  const weekMeetings = meetings.filter(m => m.date >= weekStartStr && m.date <= weekDays[6].dateStr && m.status !== 'cancelled');
  let totalWeekMins = 0;
  weekMeetings.forEach(m => { totalWeekMins += parseInt(m.duration || 45, 10); });

  let html = `
    <div class="weekly-board-header">
      <div class="weekly-nav-group">
        <button class="btn btn-sm" onclick="changeWeekOffset(-1)" title="上一周">◀ 上周</button>
        <div class="weekly-title">
          <span>📅 本周日程看板 · ${weekDays[0].month}月${weekDays[0].day}日 - ${displayDays[displayDays.length-1].month}月${displayDays[displayDays.length-1].day}日</span>
          ${currentWeekOffset === 0 ? '<span class="cal-today-badge" style="margin-left:6px;">本周</span>' : ''}
        </div>
        <button class="btn btn-sm" onclick="changeWeekOffset(1)" title="下一周">下周 ▶</button>
        <button class="btn btn-sm btn-ghost" onclick="jumpToCurrentWeek()">回到本周</button>
      </div>

      <div style="font-size:12px; color:var(--text-secondary); display:flex; align-items:center; gap:12px;">
        <span>本周重点会议：<strong style="color:var(--blue-accent); font-size:14px;">${weekMeetings.length}</strong> 场</span>
        <span>排期总时长：<strong style="color:var(--text-primary); font-size:14px;">${(totalWeekMins/60).toFixed(1)}</strong> H</span>
        <button class="btn btn-sm btn-ghost" onclick="exportExecutiveScheduleBriefing()" title="复制本周完整会议通知文本发给领导/工作群">📋 复制周日程简报</button>
      </div>
    </div>

    <div class="weekly-grid" style="grid-template-columns: repeat(${displayDays.length}, 1fr);">
  `;

  displayDays.forEach(day => {
    const dayMeetings = meetings.filter(m => m.date === day.dateStr && m.status !== 'cancelled');
    dayMeetings.sort((a, b) => (a.time || '10:00').localeCompare(b.time || '10:00'));

    let dayDurationMins = 0;
    dayMeetings.forEach(m => { dayDurationMins += parseInt(m.duration || 45, 10); });

    const { freeSlots } = calculateDayFreeSlots(meetings, day.dateStr);

    html += `
      <div class="weekly-col ${day.isToday ? 'is-today' : ''}">
        <div class="weekly-col-header">
          <div>
            <span class="weekly-col-day">${day.name}</span>
            <span class="weekly-col-date">${day.month}月${day.day}日</span>
            ${day.isToday ? '<span class="cal-today-badge">今天</span>' : ''}
          </div>
          <span class="weekly-col-badge">${dayMeetings.length} 场 · ${(dayDurationMins/60).toFixed(1)}H</span>
        </div>

        <div class="weekly-col-events">
    `;

    if (dayMeetings.length === 0) {
      html += `
        <div style="text-align:center; padding: 24px 8px; color:var(--text-muted); font-size:12px; background:#fff; border:1px dashed var(--border); border-radius:var(--radius-sm);">
          <div style="font-size:18px; margin-bottom:4px;">☕</div>
          <div>全天暂无会议</div>
          <button class="btn btn-sm btn-ghost" style="margin-top:6px; font-size:11px;" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '10:00', 45)">＋ 安排预约</button>
        </div>
      `;
    } else {
      dayMeetings.forEach(m => {
        const durHours = m.durationHours || (parseInt(m.duration || 45, 10) / 60).toFixed(2);
        const priorityCls = m.priority === 'high' ? 'priority-high' : '';

        html += `
          <div class="weekly-card ${priorityCls}" onclick="editMeeting(${m.id})" title="点击查看/编辑详情">
            <div class="weekly-card-time">
              <span>🕒 ${m.time} (${durHours}H)</span>
              <span style="font-size:10px; font-weight:normal; color:var(--text-muted);">${escapeHtml(m.location || '主管办公室')}</span>
            </div>

            <div class="weekly-card-title">
              ${escapeHtml(m.subject)}
            </div>

            <div class="weekly-card-meta">
              <div><strong>👔 汇报人：</strong>${escapeHtml(m.reporter || m.attendees.split('、')[1] || '未注明')}</div>
              <div><strong>👥 参会人：</strong>${escapeHtml(m.attendees)}</div>
              ${m.minuter ? `<div><strong>📝 纪要人：</strong><span style="color:#2563eb; font-weight:600;">${escapeHtml(m.minuter)}</span></div>` : ''}
            </div>

            ${m.decision ? `
              <div class="weekly-card-decision" title="${escapeHtml(m.decision)}">
                <strong>🎯 决策要点：</strong>${escapeHtml(m.decision.slice(0, 45))}${m.decision.length > 45 ? '...' : ''}
              </div>
            ` : ''}
          </div>
        `;
      });
    }

    // Free slots indicators
    if (freeSlots.length > 0) {
      const topFree = freeSlots[0];
      html += `
        <div class="weekly-free-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '${topFree.startStr}', ${Math.min(topFree.duration, 45)})" title="点击一键在空档时段预约新会议">
          🟢 推荐空档：${topFree.startStr} - ${topFree.endStr} (${topFree.duration}m) ＋
        </div>
      `;
    }

    html += `
        </div>
      </div>
    `;
  });

  html += `
    </div>
  `;

  boardContainer.innerHTML = html;
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
  let startDayOfWeek = firstDay.getDay();
  if (startDayOfWeek === 0) startDayOfWeek = 7;
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
  const weekBoardEl = document.getElementById('supervisorWeeklyBoardContainer');
  const monthCalEl = document.getElementById('supervisorMonthCalendarContainer');
  const cardsToolbar = document.getElementById('cardsSectionToolbar');
  const listEl = document.getElementById('meetingCardsList');
  const dashListEl = document.getElementById('dashMeetingList');
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

  // Show/Hide view modes
  if (supervisorViewMode === 'week_board') {
    if (weekBoardEl) weekBoardEl.style.display = 'block';
    if (monthCalEl) monthCalEl.style.display = 'none';
    if (cardsToolbar) cardsToolbar.style.display = 'none';
    if (listEl) listEl.style.display = 'none';
    renderSupervisorWeeklyBoard();
  } else if (supervisorViewMode === 'month_cal') {
    if (weekBoardEl) weekBoardEl.style.display = 'none';
    if (monthCalEl) monthCalEl.style.display = 'block';
    if (cardsToolbar) cardsToolbar.style.display = 'none';
    if (listEl) listEl.style.display = 'none';
    renderSupervisorMonthCalendar();
  } else if (supervisorViewMode === 'card_list') {
    if (weekBoardEl) weekBoardEl.style.display = 'none';
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
          <img src="${SNOOPY_ASSETS.supervisor_secretary}" style="width:48px; opacity:0.65; margin-bottom:8px;" alt="" />
          <p style="font-size:13.5px; font-weight:600; color:var(--text-secondary);">暂无符合筛选条件的会议记录</p>
          <div style="margin-top:12px; display:flex; justify-content:center; gap:8px;">
            <button class="btn btn-sm btn-primary" onclick="openAddMeetingModal()">➕ 登记新预约</button>
            <button class="btn btn-sm" onclick="openImportCalendarModal()">📥 导入表格 / 日历</button>
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
        const durHours = m.durationHours || (parseInt(m.duration || 45, 10) / 60).toFixed(2);

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
                  <span class="meta-chip">⏱️ <strong>时长：</strong>${durHours}H (${m.duration || 45}分钟)</span>
                  <span class="meta-chip">📍 <strong>地点：</strong>${escapeHtml(m.location || '主管办公室')}</span>
                  <span class="meta-chip">👔 <strong>汇报人：</strong>${escapeHtml(m.reporter || '未注明')}</span>
                  ${m.minuter ? `<span class="meta-chip">📝 <strong>纪要人：</strong>${escapeHtml(m.minuter)}</span>` : ''}
                </div>
              </div>

              <button class="btn btn-sm" onclick="copySingleMeetingNotice(${m.id})" title="复制该会议的完整通知格式至剪贴板">📋 复制通知</button>
            </div>

            <div class="meeting-card-body">
              ${m.background ? `
                <div class="field-block">
                  <div class="field-label">📖 议题背景 (Background / Context)</div>
                  <div class="field-val">${escapeHtml(m.background)}</div>
                </div>
              ` : ''}

              <div class="field-block">
                <div class="field-label">🎯 决策要点说明 (Decision Points - 待主管定夺)</div>
                <div class="field-val decision-val">${escapeHtml(m.decision || '审议相关事项并定夺')}</div>
              </div>

              <div class="field-block">
                <div class="field-label">👥 参会人员 (Attendees)</div>
                <div class="field-val">${escapeHtml(m.attendees)}</div>
              </div>
            </div>

            <div class="meeting-card-footer">
              <div class="requester-info">
                <span>👤 预约人：${escapeHtml(m.requester || '日历导入')}</span>
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
              🕒 ${m.date} ${m.time} (${m.duration}分) · 👔 ${escapeHtml(m.reporter || m.attendees)}
            </div>
          </div>
          <button class="btn btn-sm" onclick="copySingleMeetingNotice(${m.id})">📋 复制</button>
        </div>
      `).join('');
    }
  }
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

function openAddMeetingModalWithSlot(date, startTime, duration) {
  openAddMeetingModal();
  if (date) document.getElementById('inputMeetingDate').value = date;
  if (startTime) document.getElementById('inputMeetingTime').value = startTime;
  if (duration) setMeetingDuration(duration);
  showToast(`已自动填入排期时段：${date} ${startTime} (${duration}分钟)`);
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

function copyStandardExcelHeader() {
  const header = "*会议主题（关键任务）\\t*议题背景/决策要点说明\\t*汇报人\\t*参会人\\t*纪要人\\t*预约时长（H）\\t排期日期\\t开始时间";
  copyToClipboard(header, "📋 标准表头已复制！可直接粘贴至 Excel 第一行。");
}

function downloadStandardExcelTemplate() {
  const csvContent = "\uFEFF*会议主题（关键任务）,*议题背景/决策要点说明,*汇报人,*参会人,*纪要人,*预约时长（H）,排期日期,开始时间\n" +
    "中东北非区域Q3交付资源评审,审批重点交付架构师驻场与预算特批,张总(地南代),\"主管、李总、财务BP\",王秘书,0.75,2026-09-24,10:00\n" +
    "阿尔及利亚代表处外汇与回款复盘,特批客户付款账期与汇率对冲,王总,\"主管、法务部、商务部\",李秘书,1.0,2026-09-25,14:30\n" +
    "刚果金代表处工程进展对齐,审批新安保防护与施工里程碑,陈部长,\"主管、交付部\",赵秘书,0.5,2026-09-25,16:00\n";

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
        if (rowVals.length > 0) rows.push(rowVals.join('\\t'));
      }
    }
    return rows.join('\\n');
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

// Universal Schedule Text Parser with Fixed Header Alignment & Weekday Row Filter
function parseUniversalScheduleText(rawText, defaultDate) {
  if (!rawText || !rawText.trim()) return [];
  const lines = rawText.trim().split(/\\r?\\n/).map(s => s.trim()).filter(Boolean);
  const results = [];

  const baseDate = new Date(defaultDate || new Date().toISOString().slice(0, 10));
  let dayOfWeek = baseDate.getDay();
  if (dayOfWeek === 0) dayOfWeek = 7;
  const monDate = new Date(baseDate);
  monDate.setDate(baseDate.getDate() - (dayOfWeek - 1));

  const weekdayMap = {
    '一': 0, '1': 0,
    '二': 1, '2': 1,
    '三': 2, '3': 2,
    '四': 3, '4': 3,
    '五': 4, '5': 4,
    '六': 5, '6': 5,
    '日': 6, '天': 6, '7': 6
  };

  let colMap = null;
  let currentDate = defaultDate || baseDate.toISOString().slice(0, 10);
  let currentSlotIdx = 0;
  const defaultSlots = ['09:30', '10:30', '14:30', '15:30', '16:30', '17:15'];

  let isGridCalendar = false;
  const gridDayCols = {};

  for (let line of lines) {
    // 1. Weekday Header check: e.g. 星期一, 星期二, 周三, 【星期四】
    // NEVER treat weekday headers as meeting subjects!
    const wkMatch = line.match(/^(?:【|\[)?(?:星期|周|礼拜)([一二三四五六日天1-7])(?:】|\])?$/);
    if (wkMatch) {
      const offset = weekdayMap[wkMatch[1]];
      const targetD = new Date(monDate);
      targetD.setDate(monDate.getDate() + offset);
      currentDate = targetD.toISOString().slice(0, 10);
      currentSlotIdx = 0;
      continue;
    }

    // Split line
    const parts = line.split(/[\\t,;|]+|\\s{2,}/).map(s => s.trim());

    // 2. Grid calendar header check: e.g. 时间 \t 星期一 \t 星期二 \t 星期三 ...
    const hasMultipleWeekdays = parts.filter(p => /(?:星期|周)[一二三四五六日天]/.test(p)).length >= 2;
    if (hasMultipleWeekdays) {
      isGridCalendar = true;
      parts.forEach((p, idx) => {
        const m = p.match(/(?:星期|周)([一二三四五六日天])/);
        if (m) {
          const targetD = new Date(monDate);
          targetD.setDate(monDate.getDate() + weekdayMap[m[1]]);
          gridDayCols[idx] = targetD.toISOString().slice(0, 10);
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
          if (!['-', '/', '无', '空'].includes(val)) {
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
    const cleanHeaderCheck = parts.map(p => p.toLowerCase().replace(/[*（）()\\s]/g, ''));
    if (cleanHeaderCheck.some(p => p.includes('会议主题') || p.includes('关键任务') || p.includes('主题'))) {
      colMap = {};
      parts.forEach((p, idx) => {
        const clean = p.replace(/[*（）()\\s]/g, '').toLowerCase();
        if (clean.includes('会议主题') || clean.includes('关键任务') || clean.includes('主题')) {
          colMap['subject'] = idx;
        } else if (clean.includes('议题背景') || clean.includes('决策要点') || clean.includes('决策')) {
          colMap['decision'] = idx;
        } else if (clean.includes('汇报人') || clean.includes('汇报') || clean.includes('主讲')) {
          colMap['reporter'] = idx;
        } else if (clean.includes('参会人') || clean.includes('与会')) {
          colMap['attendees'] = idx;
        } else if (clean.includes('纪要人') || clean.includes('记录') || clean.includes('纪要')) {
          colMap['minuter'] = idx;
        } else if (clean.includes('预约时长') || clean.includes('时长') || clean.includes('duration')) {
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
      const sub = parts[colMap['subject']] || '';
      if (!sub) continue;

      // Filter out weekday row if pasted
      if (/^(?:星期|周)[一二三四五六日天]$/.test(sub)) {
        continue;
      }

      const dec = colMap['decision'] !== undefined ? (parts[colMap['decision']] || '') : '';
      const rep = colMap['reporter'] !== undefined ? (parts[colMap['reporter']] || '') : '';
      let att = colMap['attendees'] !== undefined ? (parts[colMap['attendees']] || '') : '';
      const minu = colMap['minuter'] !== undefined ? (parts[colMap['minuter']] || '') : '';
      const durStr = colMap['durationHours'] !== undefined ? (parts[colMap['durationHours']] || '') : '';
      const dateVal = colMap['date'] !== undefined ? (parts[colMap['date']] || '') : '';
      const timeVal = colMap['time'] !== undefined ? (parts[colMap['time']] || '') : '';

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

    // 5. Fallback: Universal NLP / Free Form extractor
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
  showToast(`🎉 成功导入并规整 ${parsedImportMeetings.length} 场会议！周历看板与月历已自动更新！`);
}

function exportExecutiveScheduleBriefing() {
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const today = new Date();
  let dayOfWeek = today.getDay();
  if (dayOfWeek === 0) dayOfWeek = 7;
  const monDate = new Date(today);
  monDate.setDate(today.getDate() - (dayOfWeek - 1) + (currentWeekOffset * 7));

  const weekStartStr = monDate.toISOString().slice(0, 10);
  const sunDate = new Date(monDate);
  sunDate.setDate(monDate.getDate() + 6);
  const weekEndStr = sunDate.toISOString().slice(0, 10);

  const weekMeetings = meetings.filter(m => m.date >= weekStartStr && m.date <= weekEndStr && m.status !== 'cancelled');
  weekMeetings.sort((a, b) => (a.date + ' ' + a.time).localeCompare(b.date + ' ' + b.time));

  const lines = [
    '【主管本周日程安排 · 秘书处通报】',
    `排期周期：${weekStartStr} 至 ${weekEndStr} · 共 ${weekMeetings.length} 场重点会议`,
    '══════════════════════════════════════════════'
  ];

  const weekdayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
  for (let i = 0; i < 7; i++) {
    const curD = new Date(monDate);
    curD.setDate(monDate.getDate() + i);
    const curDStr = curD.toISOString().slice(0, 10);
    const dayM = weekMeetings.filter(m => m.date === curDStr);

    if (dayM.length > 0) {
      lines.push(`\\n📅 ${weekdayNames[i]} (${curDStr}) · ${dayM.length} 场会议:`);
      dayM.forEach(m => {
        const durHours = m.durationHours || (parseInt(m.duration || 45, 10) / 60).toFixed(2);
        lines.push(`  ▪ ${m.time} (${durHours}H) 《${m.subject}》`);
        lines.push(`    - 汇报人：${m.reporter || '未注明'} | 纪要人：${m.minuter || '秘书处'}`);
        lines.push(`    - 参会人：${m.attendees}`);
        lines.push(`    - 决策要点：${m.decision}`);
      });
    }
  }

  lines.push('\\n══════════════════════════════════════════════');
  lines.push('💡 秘书处提醒：请各汇报人提前5分钟就座，精简汇报，直奔决策要点。');

  copyToClipboard(lines.join('\\n'), '📋 领导周日程通报已复制到剪贴板！可直接发送微信/邮件/工作群。');
}

"""

# Reconstruct code
updated_code = pre_part + new_js + post_part

# Update openAddMeetingModal to populate minuter and reporter
add_meeting_old = """function openAddMeetingModal() {
  document.getElementById('meetingModalTitle').textContent = '➕ 登记主管会议预约';
  document.getElementById('inputMeetingId').value = '';
  document.getElementById('inputMeetingDate').value = selectedTimelineDate || new Date().toISOString().slice(0, 10);
  document.getElementById('inputMeetingTime').value = '10:00';
  document.getElementById('inputMeetingDuration').value = '45';
  document.getElementById('inputMeetingSubject').value = '';
  document.getElementById('inputMeetingBackground').value = '';
  document.getElementById('inputMeetingDecision').value = '1. \\n2. ';
  document.getElementById('inputMeetingAttendees').value = '主管、';
  document.getElementById('inputMeetingRequester').value = '';
  document.getElementById('inputMeetingLocation').value = '主管办公室';
  document.getElementById('selectMeetingStatus').value = 'scheduled';
  document.getElementById('selectMeetingPriority').value = 'medium';
  document.getElementById('inputMeetingNotes').value = '';
  openModal('meetingModal');
}"""

add_meeting_new = """function openAddMeetingModal() {
  document.getElementById('meetingModalTitle').textContent = '➕ 登记主管会议预约';
  document.getElementById('inputMeetingId').value = '';
  document.getElementById('inputMeetingDate').value = selectedTimelineDate || new Date().toISOString().slice(0, 10);
  document.getElementById('inputMeetingTime').value = '10:00';
  document.getElementById('inputMeetingDuration').value = '45';
  document.getElementById('inputMeetingSubject').value = '';
  document.getElementById('inputMeetingBackground').value = '';
  document.getElementById('inputMeetingDecision').value = '1. \\n2. ';
  document.getElementById('inputMeetingReporter').value = '';
  document.getElementById('inputMeetingMinuter').value = '王秘书';
  document.getElementById('inputMeetingAttendees').value = '主管、';
  document.getElementById('inputMeetingRequester').value = '';
  document.getElementById('inputMeetingLocation').value = '主管办公室';
  document.getElementById('selectMeetingStatus').value = 'scheduled';
  document.getElementById('selectMeetingPriority').value = 'medium';
  document.getElementById('inputMeetingNotes').value = '';
  openModal('meetingModal');
}"""

if add_meeting_old in updated_code:
    updated_code = updated_code.replace(add_meeting_old, add_meeting_new, 1)
    print("openAddMeetingModal updated.")
else:
    print("WARNING: add_meeting_old not found!")

# Update saveMeeting to save minuter and reporter
save_meeting_old = """  const id = document.getElementById('inputMeetingId').value;
  const date = document.getElementById('inputMeetingDate').value;
  const time = document.getElementById('inputMeetingTime').value;
  const duration = document.getElementById('inputMeetingDuration').value;
  const subject = document.getElementById('inputMeetingSubject').value.trim();
  const background = document.getElementById('inputMeetingBackground').value.trim();
  const decision = document.getElementById('inputMeetingDecision').value.trim();
  const attendees = document.getElementById('inputMeetingAttendees').value.trim();
  const requester = document.getElementById('inputMeetingRequester').value.trim();
  const location = document.getElementById('inputMeetingLocation').value.trim();
  const status = document.getElementById('selectMeetingStatus').value;
  const priority = document.getElementById('selectMeetingPriority').value;
  const notes = document.getElementById('inputMeetingNotes').value.trim();"""

save_meeting_new = """  const id = document.getElementById('inputMeetingId').value;
  const date = document.getElementById('inputMeetingDate').value;
  const time = document.getElementById('inputMeetingTime').value;
  const duration = document.getElementById('inputMeetingDuration').value;
  const subject = document.getElementById('inputMeetingSubject').value.trim();
  const background = document.getElementById('inputMeetingBackground').value.trim();
  const decision = document.getElementById('inputMeetingDecision').value.trim();
  const reporter = (document.getElementById('inputMeetingReporter') ? document.getElementById('inputMeetingReporter').value.trim() : '');
  const minuter = (document.getElementById('inputMeetingMinuter') ? document.getElementById('inputMeetingMinuter').value.trim() : '秘书处');
  const attendees = document.getElementById('inputMeetingAttendees').value.trim();
  const requester = document.getElementById('inputMeetingRequester').value.trim();
  const location = document.getElementById('inputMeetingLocation').value.trim();
  const status = document.getElementById('selectMeetingStatus').value;
  const priority = document.getElementById('selectMeetingPriority').value;
  const notes = document.getElementById('inputMeetingNotes').value.trim();"""

if save_meeting_old in updated_code:
    updated_code = updated_code.replace(save_meeting_old, save_meeting_new, 1)
    # Also update meeting object construction
    updated_code = updated_code.replace("attendees, requester,", "reporter, minuter, attendees, requester, durationHours: (parseInt(duration,10)/60).toFixed(2),")
    print("saveMeeting updated with minuter.")
else:
    print("WARNING: save_meeting_old not found!")

# Update editMeeting to populate minuter and reporter
edit_meeting_target = """  document.getElementById('inputMeetingDecision').value = m.decision;
  document.getElementById('inputMeetingAttendees').value = m.attendees;"""

edit_meeting_replacement = """  document.getElementById('inputMeetingDecision').value = m.decision;
  if (document.getElementById('inputMeetingReporter')) document.getElementById('inputMeetingReporter').value = m.reporter || '';
  if (document.getElementById('inputMeetingMinuter')) document.getElementById('inputMeetingMinuter').value = m.minuter || '秘书处';
  document.getElementById('inputMeetingAttendees').value = m.attendees;"""

if edit_meeting_target in updated_code:
    updated_code = updated_code.replace(edit_meeting_target, edit_meeting_replacement, 1)
    print("editMeeting updated with minuter and reporter.")
else:
    print("WARNING: edit_meeting_target not found!")

with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
    f.write(updated_code)

print("Part 2 (JS logic) done.")

# update_round10.py
# Applies all 4 points from user request 10 to assemble_final_app.py

import re

with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS: avatar sizes, weekly-col header, is-resting
old_css_needle = """  .module-banner-avatar {
    width: 72px;
    height: 76px;
    object-fit: contain;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));
    flex-shrink: 0;
    transition: transform 0.2s ease;
  }
  /* Enlarge logos for 常用链接, 每日小记, 每日英语 to match the first banners */
  .theme-links .module-banner-avatar {
    width: 92px;
    height: 96px;
  }
  .theme-notes .module-banner-avatar {
    width: 92px;
    height: 96px;
  }
  .theme-english .module-banner-avatar {
    width: 88px;
    height: 92px;
  }"""

new_css_banner = """  .module-header-banner {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 24px;
    min-height: 112px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
  }
  .module-banner-avatar {
    width: 84px;
    height: 88px;
    object-fit: contain;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));
    flex-shrink: 0;
    transition: transform 0.2s ease;
  }
  /* Enlarge logos for 常用链接, 每日小记, 每日英语 to match the first banners */
  .theme-links .module-banner-avatar {
    width: 96px;
    height: 98px;
  }
  .theme-notes .module-banner-avatar {
    width: 96px;
    height: 98px;
  }
  .theme-english .module-banner-avatar {
    width: 92px;
    height: 94px;
  }"""

if old_css_needle in content:
    content = content.replace(old_css_needle, new_css_banner)
    print("✓ Updated module avatar CSS")
else:
    print("! Could not find old_css_needle")

# Update weekly column CSS to avoid wrapping
old_col_css = """  .weekly-col-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    border-bottom: 1px dashed var(--border);
  }
  .weekly-col-day {
    font-size: 13.5px;
    font-weight: 800;
    color: var(--text-primary);
  }
  .weekly-col-date {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: normal;
  }
  .weekly-col-badge {
    font-size: 10.5px;
    background: #e0e7ff;
    color: #3730a3;
    padding: 2px 6px;
    border-radius: 10px;
    font-weight: 600;
  }"""

new_col_css = """  .weekly-col-header {
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
  }"""

if old_col_css in content:
    content = content.replace(old_col_css, new_col_css)
    print("✓ Updated weekly col header CSS")
else:
    print("! Could not find old_col_css")

# 2. Update toggleFullWeekDisplay helper variable and function before renderSupervisorWeeklyBoard
toggle_helper = """let showFullWeekCalendar = false;
function toggleFullWeekDisplay(showFull) {
  showFullWeekCalendar = showFull;
  renderSupervisorWeeklyBoard();
}

// ----------------- 领导本周日历看板渲染引擎 (Executive Weekly Board) -----------------
function renderSupervisorWeeklyBoard() {"""

content = content.replace("// ----------------- 领导本周日历看板渲染引擎 (Executive Weekly Board) -----------------\nfunction renderSupervisorWeeklyBoard() {", toggle_helper)

# 3. Replace renderSupervisorWeeklyBoard implementation
old_weekly_start = """  const meetings = getData(STORAGE_KEYS.MEETINGS);
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
          <span>本周日程看板 · ${weekDays[0].month}月${weekDays[0].day}日 - ${displayDays[displayDays.length-1].month}月${displayDays[displayDays.length-1].day}日</span>
          ${currentWeekOffset === 0 ? '<span class="cal-today-badge" style="margin-left:6px;">本周</span>' : ''}
        </div>
        <button class="btn btn-sm" onclick="changeWeekOffset(1)" title="下一周">下周 ▶</button>
        <button class="btn btn-sm btn-ghost" onclick="jumpToCurrentWeek()">回到本周</button>
      </div>

      <div style="font-size:12px; color:var(--text-secondary); display:flex; align-items:center; gap:12px;">
        <span>重点会议：<strong style="color:var(--blue-accent); font-size:14px;">${weekMeetings.length}</strong> 场</span>
        <span>排期时长：<strong style="color:var(--text-primary); font-size:14px;">${(totalWeekMins/60).toFixed(1)}</strong> H</span>
        <button class="btn btn-sm btn-ghost" onclick="exportExecutiveScheduleBriefing()" title="复制本周完整会议通知文本发给领导/工作群">复制周日程简报</button>
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
        </div>"""

new_weekly_start = """  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const today = new Date();
  const todayStr = today.toISOString().slice(0, 10);

  // Compute Sunday of the displayed week (周日到周四工作日，周五周六周末)
  const sunDate = new Date(today);
  sunDate.setDate(today.getDate() - today.getDay() + (currentWeekOffset * 7));

  const weekDays = [];
  const weekdayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];

  for (let i = 0; i < 7; i++) {
    const d = new Date(sunDate);
    d.setDate(sunDate.getDate() + i);
    const dStr = d.toISOString().slice(0, 10);
    weekDays.push({
      dateStr: dStr,
      month: d.getMonth() + 1,
      day: d.getDate(),
      name: weekdayNames[i],
      isToday: (dStr === todayStr),
      isWeekend: (i === 5 || i === 6) // 周五与周六为周末
    });
  }

  // Check if weekend has meetings or if today falls on the weekend
  const hasWeekendMeetings = meetings.some(m => {
    return (m.date === weekDays[5].dateStr || m.date === weekDays[6].dateStr) && m.status !== 'cancelled';
  });
  const todayIsWeekend = (todayStr === weekDays[5].dateStr || todayStr === weekDays[6].dateStr);
  const shouldShowFull = showFullWeekCalendar || hasWeekendMeetings || todayIsWeekend;
  const displayDays = shouldShowFull ? weekDays : weekDays.slice(0, 5);

  // Calculate week stats (Sunday to Saturday)
  const weekStartStr = weekDays[0].dateStr;
  const weekEndStr = weekDays[6].dateStr;
  const weekMeetings = meetings.filter(m => m.date >= weekStartStr && m.date <= weekEndStr && m.status !== 'cancelled');
  let totalWeekMins = 0;
  weekMeetings.forEach(m => { totalWeekMins += parseInt(m.duration || 45, 10); });

  let html = `
    <div class="weekly-board-header">
      <div class="weekly-nav-group">
        <button class="btn btn-sm" onclick="changeWeekOffset(-1)" title="上一周">◀ 上周</button>
        <div class="weekly-title">
          <span>本周日程看板 · ${weekDays[0].month}月${weekDays[0].day}日 - ${displayDays[displayDays.length-1].month}月${displayDays[displayDays.length-1].day}日</span>
          ${currentWeekOffset === 0 ? '<span class="cal-today-badge" style="margin-left:6px;">本周</span>' : ''}
        </div>
        <button class="btn btn-sm" onclick="changeWeekOffset(1)" title="下一周">下周 ▶</button>
        <button class="btn btn-sm btn-ghost" onclick="jumpToCurrentWeek()">回到本周</button>
        <button class="btn btn-sm btn-ghost" onclick="toggleFullWeekDisplay(${!shouldShowFull})" style="font-size:11.5px; margin-left:4px;" title="切换5天工作日与7天全周视图">
          ${shouldShowFull ? '仅看工作日 (周日-周四)' : '完整周历 (含周五六)'}
        </button>
      </div>

      <div style="font-size:12px; color:var(--text-secondary); display:flex; align-items:center; gap:12px;">
        <span>重点会议：<strong style="color:var(--blue-accent); font-size:14px;">${weekMeetings.length}</strong> 场</span>
        <span>排期时长：<strong style="color:var(--text-primary); font-size:14px;">${(totalWeekMins/60).toFixed(1)}</strong> H</span>
        <button class="btn btn-sm btn-ghost" onclick="exportExecutiveScheduleBriefing()" title="复制本周完整会议通知文本发给领导/工作群">复制周日程简报</button>
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
      <div class="weekly-col ${day.isToday ? 'is-today' : ''} ${day.isWeekend ? 'is-weekend' : ''}">
        <div class="weekly-col-header">
          <div class="weekly-col-header-main">
            <span class="weekly-col-day">${day.name}</span>
            <span class="weekly-col-date">${day.month}月${day.day}日</span>
          </div>
          ${day.isToday ? '<span class="cal-today-badge">今日</span>' : (day.isWeekend ? '<span class="weekly-weekend-badge">周末</span>' : '')}
        </div>"""

if old_weekly_start in content:
    content = content.replace(old_weekly_start, new_weekly_start)
    print("✓ Updated renderSupervisorWeeklyBoard to Sunday-first without meeting count badge")
else:
    print("! Could not find old_weekly_start")

# 4. Update Month Calendar: start Sunday, Friday-Saturday weekends, remove X场 badge
old_month_cal = """  const firstDay = new Date(year, month, 1);
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
        <span>本月排期会议：<strong style="color:var(--blue-accent);">${monthMeetings.length}</strong> 场</span>
        <span>累计排期时长：<strong>${(monthMins / 60).toFixed(1)}</strong> 小时</span>
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
            </div>"""

new_month_cal = """  const firstDay = new Date(year, month, 1);
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
              ${isToday ? '<span class="cal-today-badge">今天</span>' : ''}
            </div>"""

if old_month_cal in content:
    content = content.replace(old_month_cal, new_month_cal)
    print("✓ Updated renderSupervisorMonthCalendar to Sunday-first without meeting count badge")
else:
    print("! Could not find old_month_cal")

# 5. Update parseUniversalScheduleText Sunday-first baseDate
old_parse_base = """  const baseDate = new Date(defaultDate || new Date().toISOString().slice(0, 10));
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
  };"""

new_parse_base = """  const baseDate = new Date(defaultDate || new Date().toISOString().slice(0, 10));
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
  };"""

if old_parse_base in content:
    content = content.replace(old_parse_base, new_parse_base)
    # Also replace monDate with sunDate in parseUniversalScheduleText
    content = content.replace("targetD = new Date(monDate);", "targetD = new Date(sunDate);")
    content = content.replace("targetD.setDate(monDate.getDate() + offset);", "targetD.setDate(sunDate.getDate() + offset);")
    content = content.replace("targetD.setDate(monDate.getDate() + weekdayMap[m[1]]);", "targetD.setDate(sunDate.getDate() + weekdayMap[m[1]]);")
    print("✓ Updated parseUniversalScheduleText to Sunday-first")
else:
    print("! Could not find old_parse_base")

# 6. Update exportExecutiveScheduleBriefing to Sunday-first
old_briefing = """function exportExecutiveScheduleBriefing() {
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
      lines.push(`\\n【${weekdayNames[i]} ${curDStr}】· ${dayM.length} 场会议:`);"""

new_briefing = """function exportExecutiveScheduleBriefing() {
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const today = new Date();
  const sunDate = new Date(today);
  sunDate.setDate(today.getDate() - today.getDay() + (currentWeekOffset * 7));

  const weekStartStr = sunDate.toISOString().slice(0, 10);
  const satDate = new Date(sunDate);
  satDate.setDate(sunDate.getDate() + 6);
  const weekEndStr = satDate.toISOString().slice(0, 10);

  const weekMeetings = meetings.filter(m => m.date >= weekStartStr && m.date <= weekEndStr && m.status !== 'cancelled');
  weekMeetings.sort((a, b) => (a.date + ' ' + a.time).localeCompare(b.date + ' ' + b.time));

  const lines = [
    '【主管本周日程安排 · 秘书处通报】',
    `排期周期：${weekStartStr} 至 ${weekEndStr} · 共 ${weekMeetings.length} 场重点会议`,
    '══════════════════════════════════════════════'
  ];

  const weekdayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  for (let i = 0; i < 7; i++) {
    const curD = new Date(sunDate);
    curD.setDate(sunDate.getDate() + i);
    const curDStr = curD.toISOString().slice(0, 10);
    const dayM = weekMeetings.filter(m => m.date === curDStr);

    if (dayM.length > 0) {
      lines.push(`\\n【${weekdayNames[i]} ${curDStr}】:`);"""

if old_briefing in content:
    content = content.replace(old_briefing, new_briefing)
    print("✓ Updated exportExecutiveScheduleBriefing to Sunday-first")
else:
    print("! Could not find old_briefing")

# 7. Update resetMeetingsToDefault: clean slate without examples
old_reset = """function resetMeetingsToDefault() {
  const ok = confirm('确定要重置主管会议日程为初始状态吗？\\n当前自定义导入或修改的会议记录将被清空，并恢复为默认的精选排期示例。');
  if (!ok) return;

  localStorage.removeItem(STORAGE_KEYS.MEETINGS);
  initSeeds();
  renderMeetings();
  if (typeof updateHomeBadge === 'function') updateHomeBadge();
  showToast('已成功重置为初始会议日程');
}"""

new_reset = """function resetMeetingsToDefault() {
  const ok = confirm('确定要重置主管会议日程为空白初始状态吗？\\n当前所有会议记录将被清空，恢复为空白日程表，方便全新导入或登记。');
  if (!ok) return;

  setData(STORAGE_KEYS.MEETINGS, []);
  renderMeetings();
  if (typeof updateHomeBadge === 'function') updateHomeBadge();
  showToast('已清空所有日程，恢复为空白初始状态');
}"""

if old_reset in content:
    content = content.replace(old_reset, new_reset)
    print("✓ Updated resetMeetingsToDefault to empty clean slate")
else:
    print("! Could not find old_reset")

# 8. Update initSeeds: initialize empty meetings
content = re.sub(
    r'if \(!localStorage\.getItem\(STORAGE_KEYS\.MEETINGS\)\) \{[\s\S]*?setData\(STORAGE_KEYS\.MEETINGS, \[[\s\S]*?\]\);\s*\}',
    'if (!localStorage.getItem(STORAGE_KEYS.MEETINGS)) {\n    setData(STORAGE_KEYS.MEETINGS, []);\n  }',
    content
)
print("✓ Updated initSeeds to initialize empty meetings array")

# 9. Update renderTimezones: 09:00 - 18:00, lunch 12:00 - 13:30, weekend resting, light-gray .is-resting
old_tz_render = """    gridEl.innerHTML = sortedReps.map(rep => {
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

      let statusDot = '<span class="tz-status-dot"><span class="dot-green"></span> 正常办公中</span>';
      let progressPct = 0;
      if (hourVal < 8.5 || hourVal >= 18) {
        statusDot = '<span class="tz-status-dot"><span class="dot-grey"></span> 🌙 休息蓄能中</span>';
        progressPct = hourVal >= 18 ? 100 : 0;
      } else if (hourVal >= 12.5 && hourVal < 14) {
        statusDot = '<span class="tz-status-dot"><span class="dot-yellow"></span> ☕ 午休小憩</span>';
        progressPct = ((hourVal - 8.5) / 9.5) * 100;
      } else {
        progressPct = Math.min(100, Math.max(0, ((hourVal - 8.5) / 9.5) * 100));
      }

      const offsetStr = rep.utcOffset >= 0 ? 'UTC+' + rep.utcOffset : 'UTC' + rep.utcOffset;
      const diffLabel = rep.isBaseline ? '<span style="color:var(--accent-red); font-weight:700;">★ 开罗基准时区</span>' : rep.diffText;

      return `
        <div class="tz-card ${rep.isBaseline ? 'baseline' : ''}">
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

            <div class="tz-progress-bar" title="工作日作息进度 (08:30 - 18:00)">
              <div class="tz-progress-fill" style="width: ${progressPct}%;"></div>
            </div>
          </div>

          <div class="tz-diff-row">
            <div>${diffLabel}</div>
            <div>${statusDot}</div>
          </div>
        </div>
      `;
    }).join('');"""

new_tz_render = """    gridEl.innerHTML = sortedReps.map(rep => {
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
      // In Cairo, Algeria, Med South (North Africa/MENA): Friday and Saturday are official weekend
      // In Congo DRC, Cameroon, Ivory Coast, Senegal, Morocco: Saturday and Sunday are weekend
      let isWeekend = false;
      if (rep.id === 'cairo' || rep.id === 'algeria' || rep.id === 'med_south') {
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
    }).join('');"""

if old_tz_render in content:
    content = content.replace(old_tz_render, new_tz_render)
    print("✓ Updated renderTimezones with 09:00-18:00, lunch break, and .is-resting class")
else:
    print("! Could not find old_tz_render")

with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("assemble_final_app.py updated successfully.")

with open('assemble_final_app.py') as f:
    code = f.read()

checks = [
    '/* Border-Lying Snoopy Stage */',
    'margin: 75px auto 25px auto;',
    'margin-top: 55px;',
    '/* ================= 2. 今日任务 (🏕️ Beagle Scout) ================= */',
    '<!-- Classic Snoopy (Original Size 165px) & Woodstock on Board Border -->',
    'let woodstockWhisperIdx = 0;',
    '// ================= 会议时间冲突检测 (Meeting Conflict Detection) =================',
    '// Conflict detection and confirmation prompt against Cairo baseline',
    'function renderSupervisorWeeklyBoard() {',
    "day.isToday ? '<span class=\"cal-today-badge\">今日</span>'",
    'dayMeetings.forEach(m => {',
    '${(m.reporter || m.attendees) ? `',
    'function renderSupervisorDayCalendar() {',
    'function renderDayEventCard(m) {',
    '${m.decision ? `',
    'function renderSupervisorMonthCalendar() {',
    '${dayCounter}</span>',
    'dayMeetingsList.slice(0, 2).map(m => {',
    'function renderMeetings() {',
    '<h3>\n                  <span>${escapeHtml(m.subject)}</span>'
]

for ch in checks:
    print(f'Found {ch[:40]}:', ch in code)

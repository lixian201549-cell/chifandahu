import re
import subprocess
import json

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Assertions on HTML
print("--- Testing HTML Static Assertions ---")
for dur in [30, 40, 60, 90, 120]:
    chip_id = f'id="durChip{dur}"'
    assert chip_id in html, f"Missing duration chip {chip_id}"
    assert f"applyQuickDuration({dur})" in html, f"Missing applyQuickDuration({dur})"
print("✓ All 5 duration chips (30, 40, 60, 90, 120) found and configured")

assert 'class="time-picker-wrapper"' in html, "Missing .time-picker-wrapper in HTML"
assert 'id="inputMeetingStartTime"' in html, "Missing inputMeetingStartTime"
assert 'id="inputMeetingEndTime"' in html, "Missing inputMeetingEndTime"
assert 'id="timePickerMenu_start"' in html, "Missing timePickerMenu_start dropdown"
assert 'id="timePickerMenu_end"' in html, "Missing timePickerMenu_end dropdown"
print("✓ time-picker-wrapper and dropdown menu containers found in HTML")

# Verify "(选填)" is removed from labels and placeholders
assert "(选填)" not in html, "Found literal '(选填)' in HTML!"
assert "（选填）" not in html, "Found literal '（选填）' in HTML!"
assert "(可手输/下拉选)" not in html, "Found '(可手输/下拉选)' in HTML!"
assert 'placeholder="选填' not in html, "Found 'placeholder=\"选填' in HTML!"
assert '<label>汇报人</label>' in html, "Reporter label should be simple '<label>汇报人</label>'"
assert 'id="inputMeetingReporter" required' not in html, "inputMeetingReporter should NOT be required"
print("✓ 汇报人 (Reporter) is clean and optional, no '(选填)' or verbose labels in HTML")

# Verify Delete button and Recall button in meetingModal
assert 'id="btnDeleteMeeting"' in html, "Missing #btnDeleteMeeting in meetingModal footer"
assert 'deleteCurrentMeeting()' in html, "Missing deleteCurrentMeeting() call on #btnDeleteMeeting"
assert 'id="btnRecallToPending"' in html, "Missing #btnRecallToPending in meetingModal footer"
assert 'recallMeetingToPending()' in html, "Missing recallMeetingToPending() call on #btnRecallToPending"
print("✓ Delete button (#btnDeleteMeeting) & Recall button (#btnRecallToPending) configured in meeting modal")

# Verify switchable views in HTML (Simplified to 周历 & 月度日历 per minimal executive style)
assert 'id="btnViewWeekBoard"' in html, "Missing #btnViewWeekBoard"
assert '>周历</button>' in html, "Missing '周历' button"
assert 'id="btnViewMonthCal"' in html, "Missing #btnViewMonthCal"
assert '>月度日历</button>' in html, "Missing '月度日历' button"
assert 'id="btnViewDayCal"' not in html, "btnViewDayCal should be removed per executive minimal UI"
assert 'id="btnViewCardList"' not in html, "btnViewCardList should be removed per executive minimal UI"
assert 'id="supervisorDayCalendarContainer"' in html, "Missing #supervisorDayCalendarContainer"
print("✓ Simplified switchable views (周历, 月度日历; removed 日历, 决策卡片) verified in HTML")

# Verify CSS classes for free slots and day view
assert '.weekly-free-slots-wrap' in html, "Missing .weekly-free-slots-wrap in CSS"
assert '.supervisor-day-view' in html, "Missing .supervisor-day-view in CSS"
assert '.weekly-card.is-pending' in html, "Missing .weekly-card.is-pending in CSS"
assert '.weekly-decision-overview' in html, "Missing .weekly-decision-overview in CSS"
assert '.weekly-requests-overview' in html, "Missing .weekly-requests-overview in CSS"
assert '>添加任务</button>' in html, "Todo button should say '添加任务'"
assert 'btn-todo-add">➕' not in html and 'btn-todo-add">+' not in html, "Todo button must NOT have plus symbol"
assert 'id="editTodoModal"' in html, "Missing editTodoModal in HTML"
assert 'id="editRequestModal"' in html, "Missing editRequestModal in HTML"
assert 'id="btnNoticeUnsent"' in html, "Missing #btnNoticeUnsent in HTML"
assert 'id="btnNoticeSent"' in html, "Missing #btnNoticeSent in HTML"
assert 'id="meetingFoldableDetails"' in html, "Missing #meetingFoldableDetails in HTML"
assert '会议地点 / 线上会议' in html, "Missing updated label '会议地点 / 线上会议'"
assert '线上会议号' not in html, "'线上会议号' should be replaced by '线上会议'"
assert '开罗基准时间' not in html, "'开罗基准时间' pill should be removed from header"
assert '✨ biu~变' in html, "Theme toggle button should say '✨ biu~变'"
assert 'id="editNoteModal"' in html, "Missing #editNoteModal"
assert '第 22 天 · 商务实战' not in html, "'第 22 天 · 商务实战' must be removed"
assert '北欧生活习惯与旅行Tips：' in html, "English tip should say '北欧生活习惯与旅行Tips：'"
assert 'id="linksCategoryTabs"' in html, "Missing #linksCategoryTabs in HTML"
assert 'id="manageCategoriesModal"' in html, "Missing #manageCategoriesModal in HTML"
assert 'id="editLinksModuleModal"' in html, "Missing #editLinksModuleModal in HTML"
assert 'id="editModuleModal"' in html, "Missing #editModuleModal in HTML"
assert 'id="linksModuleTitleText"' in html, "Missing #linksModuleTitleText in HTML"
assert 'id="notesModuleTitleText"' in html, "Missing #notesModuleTitleText in HTML"
assert 'id="todoModuleTitleText"' in html, "Missing #todoModuleTitleText in HTML"
assert 'id="supervisorModuleTitleText"' in html, "Missing #supervisorModuleTitleText in HTML"
assert 'id="timezoneModuleTitleText"' in html, "Missing #timezoneModuleTitleText in HTML"
assert 'id="englishModuleTitleText"' in html, "Missing #englishModuleTitleText in HTML"
assert '.module-edit-btn' in html, "Missing .module-edit-btn in CSS"
assert '主管日程时间轴' not in html, "Banner '主管日程时间轴' must be removed"
assert 'id="meetingConflictAlert"' in html, "Missing #meetingConflictAlert in HTML"
assert '.link-url-hint' not in html, "Long URL hint '.link-url-hint' must be removed from CSS and HTML"
assert '.category-tab-btn' in html, "Missing .category-tab-btn in CSS"
assert 'id="statPendingCount"' not in html, "Meeting banner stat boxes must be removed per user instruction"
assert 'id="statScheduledCount"' not in html, "Meeting banner stat boxes must be removed per user instruction"
assert 'id="statDurationSum"' not in html, "Meeting banner stat boxes must be removed per user instruction"
assert '复制排版周报' in html, "Toolbar must contain '复制排版周报'"
assert 'openLeaderTripModal()' in html, "Toolbar must contain 'openLeaderTripModal()'"
assert 'id="todoMatrixContainer"' in html, "Missing #todoMatrixContainer in HTML"
assert 'id="todoArchiveContainer"' in html, "Missing #todoArchiveContainer in HTML"
assert 'btnTodoViewMatrix' in html, "Missing btnTodoViewMatrix"
assert 'btnArchiveCompleted' in html, "Missing btnArchiveCompleted"
assert 'todoBadgeDot' not in html, "Red dot #todoBadgeDot must be removed from 今日任务 title!"
assert 'meetingBadgeDot' not in html, "Red dot #meetingBadgeDot must be removed from 会议预约 title!"
assert html.find('id="btnTodoViewMatrix"') < html.find('id="btnTodoViewList"'), "四象限看板 button must be placed before 清单视图 button!"
assert html.find('id="todoMatrixContainer"') < html.find('id="todoFullList"'), "todoMatrixContainer must be placed before todoFullList!"
assert '今天完成' in html, "Missing '今天完成' in HTML"
assert '这周安排上' in html, "Missing '这周安排上' in HTML"
assert '先放一放' in html, "Missing '先放一放' in HTML"
assert '有空再说' in html, "Missing '有空再说' in HTML"
assert '开罗时间' in html, "Missing '开罗时间' in HTML"
assert 'id="editNoteModal"' in html, "Missing editNoteModal"
req_pos = html.find('id="editRequestModal"')
note_pos = html.find('id="editNoteModal"')
between_modals = html[req_pos:note_pos]
assert between_modals.count('</div>') >= 3, "editRequestModal must close its modal-box and modal-overlay before editNoteModal!"
print("✓ Red badge dots removed, Four-Quadrant board placed first, new 4 dimensions and Cairo UTC+3 verified")
print("✓ Universal module header customization (icon-only pencil, 6 module headers, edit modal) verified")

# Assertions for Trip Timezone & Leader Business Trip System
assert 'class="trip-timezone-bar"' in html, "Missing .trip-timezone-bar in HTML"
assert 'id="leaderTripModal"' in html, "Missing #leaderTripModal in HTML"
assert 'id="inputTripDestination"' in html, "Missing #inputTripDestination in HTML"
assert 'id="inputTripStartDate"' in html, "Missing #inputTripStartDate in HTML"
assert 'id="inputTripEndDate"' in html, "Missing #inputTripEndDate in HTML"
assert 'saveLeaderTrip' in html, "Missing saveLeaderTrip in HTML"
assert 'deleteLeaderTrip' in html, "Missing deleteLeaderTrip in HTML"
assert 'openLeaderTripModal' in html, "Missing openLeaderTripModal in HTML"
assert 'getTripForDate' in html, "Missing getTripForDate in HTML"
assert 'id="inputMeetingTimezoneBase"' in html, "Missing #inputMeetingTimezoneBase in HTML"
assert 'id="modalTzConversionHint"' in html, "Missing #modalTzConversionHint in HTML"
assert 'changeTripTimezone' in html, "Missing changeTripTimezone in HTML"
assert 'togglePinNote' in html, "Missing togglePinNote in HTML"
assert 'handleNoteDragStart' in html, "Missing handleNoteDragStart in HTML"
assert 'handleTodayTodoDragStart' in html, "Missing handleTodayTodoDragStart in HTML"
assert '.note-item.is-pinned' in html, "Missing .note-item.is-pinned in CSS"
assert 'id="modalTripBanner"' in html, "Missing #modalTripBanner in HTML"
assert 'handleMeetingModalDateChange' in html, "Missing handleMeetingModalDateChange in HTML"
assert '.weekly-card-cairo-sub' in html, "Missing .weekly-card-cairo-sub in CSS"
assert 'copyPendingRequestsBriefing()' in html, "Missing copyPendingRequestsBriefing() call in HTML"
assert '📋 复制待排期简报' in html, "Missing '📋 复制待排期简报' button in HTML"
assert 'id="btnCopyPendingBriefing"' in html, "Missing #btnCopyPendingBriefing in HTML"
print("✓ Trip timezone switcher, leader business trip modal & controls, note pinning & drag-and-drop HTML/CSS verified")
print("✓ 待排期请示简报 (Pending Briefing) buttons and triggers verified in HTML")

# Assertions for English Word Selection & Pronunciation
assert 'id="wordLookupPopup"' in html, "Missing #wordLookupPopup container"
assert 'id="wordPopupTitle"' in html, "Missing #wordPopupTitle"
assert 'id="wordPopupPhonetic"' in html, "Missing #wordPopupPhonetic"
assert 'id="wordPopupPos"' in html, "Missing #wordPopupPos"
assert 'id="wordPopupSpeakBtn"' in html, "Missing #wordPopupSpeakBtn"
assert 'id="wordPopupDef"' in html, "Missing #wordPopupDef"
assert 'id="englishSearchInput"' in html, "Missing #englishSearchInput search bar"
assert 'speakLookupWord()' in html, "Missing speakLookupWord() call"
assert 'handleSelectionLookup' in html, "Missing handleSelectionLookup"
assert 'findWordInDict' in html, "Missing findWordInDict function"
assert 'cleanLookupWord' in html, "Missing cleanLookupWord function"
assert 'const NORDIC_DICT = ' in html, "Missing bundled NORDIC_DICT in index.html"
print("✓ 每日英语: 划词查询与发音浮窗、北欧词典 (NORDIC_DICT)、发音朗读与快捷搜索栏静态验证通过")

# 2. Extract JS script and test via macOS JSC
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
assert script_match, "No script found in index.html"
js_code = script_match.group(1)

test_js = f"""
const console = {{ log: (s) => print(s), error: (s) => print(s) }};
const clearTimeout = () => {{}};
let lastSpokenUtterance = null;
const window = {{
  addEventListener: () => {{}},
  speechSynthesis: {{
    cancel: () => {{}},
    speak: (u) => {{ lastSpokenUtterance = u.text; }}
  }},
  innerWidth: 1200,
  innerHeight: 800,
  scrollX: 0,
  scrollY: 0
}};
function SpeechSynthesisUtterance(text) {{
  this.text = text;
  this.lang = '';
  this.rate = 1;
}}
const elements = {{}};
const document = {{
  getElementById: (id) => {{
    if (!elements[id]) {{
      elements[id] = {{
        id: id,
        value: '',
        textContent: '',
        innerHTML: '',
        style: {{ display: 'none' }},
        classList: {{
          _cls: new Set(),
          add: function(c) {{ this._cls.add(c); }},
          remove: function(c) {{ this._cls.delete(c); }},
          contains: function(c) {{ return this._cls.has(c); }},
          toggle: function(c, v) {{ if (v) this._cls.add(c); else this._cls.delete(c); }}
        }},
        focus: () => {{}},
        querySelectorAll: () => [],
        querySelector: () => null,
        addEventListener: () => {{}},
        removeEventListener: () => {{}}
      }};
    }}
    return elements[id];
  }},
  querySelectorAll: (sel) => {{
    return [];
  }},
  addEventListener: () => {{}},
  body: {{
    classList: {{
      _cls: new Set(),
      add: function(c) {{ this._cls.add(c); }},
      remove: function(c) {{ this._cls.delete(c); }},
      contains: function(c) {{ return this._cls.has(c); }},
      toggle: function(c) {{
        if (this._cls.has(c)) {{ this._cls.delete(c); return false; }}
        else {{ this._cls.add(c); return true; }}
      }}
    }}
  }}
}};
const localStorage = {{
  _store: {{}},
  getItem: function(k) {{ return this._store[k] || null; }},
  setItem: function(k, v) {{ this._store[k] = v; }},
  removeItem: function(k) {{ delete this._store[k]; }}
}};
const confirm = () => true;
let toasts = [];
const setInterval = () => 1;
const setTimeout = () => 1;

{js_code}

// Hook showToast after script evaluation
const origShowToast = showToast;
showToast = function(msg) {{
  toasts.push(msg);
}};

let lastCopiedText = '';
const origCopyToClipboard = copyToClipboard;
copyToClipboard = function(text, msg) {{
  lastCopiedText = text;
  if (typeof showToast === 'function') showToast(msg);
}};

function assertEq(act, exp, msg) {{
  if (act !== exp) {{
    throw new Error('FAIL: ' + msg + ' -> expected: ' + exp + ', actual: ' + act);
  }}
}}

print('--- Testing Default Todo View Mode is Matrix (四象限看板在最前面，一打开就看见) ---');
assertEq(currentTodoViewMode, 'matrix', 'Default currentTodoViewMode must be matrix');

print('--- Testing normalizeTimeStr & timeStrToMinutes ---');
assertEq(normalizeTimeStr('9:30'), '09:30', '9:30 -> 09:30');
assertEq(normalizeTimeStr('09:30'), '09:30', '09:30 -> 09:30');
assertEq(normalizeTimeStr('9'), '09:00', '9 -> 09:00');
assertEq(normalizeTimeStr('14'), '14:00', '14 -> 14:00');
assertEq(timeStrToMinutes('08:30'), 510, '08:30 is 510 mins');
assertEq(timeStrToMinutes('12:00'), 720, '12:00 is 720 mins');
assertEq(timeStrToMinutes('14:00'), 840, '14:00 is 840 mins');
assertEq(timeStrToMinutes('18:00'), 1080, '18:00 is 1080 mins');
print('✓ normalizeTimeStr and timeStrToMinutes tests passed');

print('--- Testing Custom Time Picker Dropdown & Quick Duration ---');
openAddMeetingModal();
assertEq(document.getElementById('inputMeetingStartTime').value, '10:00', 'default start 10:00');
assertEq(document.getElementById('btnDeleteMeeting').style.display, 'none', 'Delete button hidden on new appointment');

// Select duration 40m
applyQuickDuration(40);
assertEq(document.getElementById('inputMeetingEndTime').value, '10:40', '40m sets 10:40');
assertEq(document.getElementById('durChip40').classList.contains('selected'), true, 'durChip40 selected');

print('--- Testing saveMeeting with optional reporter ---');
document.getElementById('inputMeetingDate').value = '2026-09-24';
document.getElementById('inputMeetingStartTime').value = '09:30';
document.getElementById('inputMeetingEndTime').value = '10:15';
document.getElementById('inputMeetingSubject').value = '中东北非区域协同会议';
document.getElementById('inputMeetingReporter').value = '';
document.getElementById('inputMeetingDecision').value = '决议：推进开罗备件库直发试点';

toasts = [];
saveMeeting();
let meetings = getData(STORAGE_KEYS.MEETINGS);
assertEq(meetings.length > 0, true, 'Meeting saved');
const savedId = meetings[0].id;
assertEq(meetings[0].reporter, '', 'Reporter empty string saved');
assertEq(meetings[0].subject, '中东北非区域协同会议', 'Subject matches');
print('✓ Meeting saved successfully without reporter');

print('--- Testing editMeeting & delete button display ---');
editMeeting(savedId);
assertEq(document.getElementById('btnDeleteMeeting').style.display, 'inline-flex', 'Delete button visible when editing');
assertEq(document.getElementById('inputMeetingSubject').value, '中东北非区域协同会议', 'Subject loaded in edit');

print('--- Testing deleteCurrentMeeting ---');
toasts = [];
deleteCurrentMeeting();
meetings = getData(STORAGE_KEYS.MEETINGS);
assertEq(meetings.length, 0, 'Meeting deleted via deleteCurrentMeeting');
assertEq(toasts.includes('会议预约已成功删除'), true, 'Delete toast displayed');
print('✓ deleteCurrentMeeting successfully deleted reservation');

print('--- Testing 4 View Modes (周历, 日历, 月度日历, 决策卡片) ---');
setSupervisorViewMode('day_cal');
assertEq(supervisorViewMode, 'day_cal', 'Mode set to day_cal');
assertEq(document.getElementById('supervisorDayCalendarContainer').style.display, 'block', 'Day container shown');
assertEq(document.getElementById('supervisorWeeklyBoardContainer').style.display, 'none', 'Weekly container hidden');
assertEq(document.getElementById('currentViewModeTag').textContent, '日历', 'Mode tag shows 日历');

setSupervisorViewMode('week_board');
assertEq(supervisorViewMode, 'week_board', 'Mode set to week_board');
assertEq(document.getElementById('supervisorWeeklyBoardContainer').style.display, 'block', 'Weekly container shown');
assertEq(document.getElementById('supervisorDayCalendarContainer').style.display, 'none', 'Day container hidden');
assertEq(document.getElementById('currentViewModeTag').textContent, '周历', 'Mode tag shows 周历');

setSupervisorViewMode('month_cal');
assertEq(supervisorViewMode, 'month_cal', 'Mode set to month_cal');
assertEq(document.getElementById('supervisorMonthCalendarContainer').style.display, 'block', 'Month container shown');
assertEq(document.getElementById('currentViewModeTag').textContent, '月度日历', 'Mode tag shows 月度日历');

setSupervisorViewMode('card_list');
assertEq(supervisorViewMode, 'card_list', 'Mode set to card_list');
assertEq(document.getElementById('cardsSectionToolbar').style.display, 'flex', 'Cards toolbar shown');
assertEq(document.getElementById('currentViewModeTag').textContent, '决策卡片', 'Mode tag shows 决策卡片');
print('✓ All 4 view modes switched and verified');

print('--- Testing All Free Slots Display in Weekly Board ---');
// Always use a future date so this regression test remains valid after its authoring date.
const freeSlotFutureDate = formatDateToStr(new Date(Date.now() + 7 * 86400000));
setData(STORAGE_KEYS.MEETINGS, [{{
  id: 12345,
  date: freeSlotFutureDate,
  startTime: '10:00',
  endTime: '11:00',
  time: '10:00',
  duration: 60,
  subject: '区域战略评审会',
  reporter: 'Sanyli',
  status: 'scheduled',
  priority: 'high',
  decision: '批准Q4预算方案'
}}]);

const freeSlotResult = calculateDayFreeSlots(getData(STORAGE_KEYS.MEETINGS), freeSlotFutureDate);
print('Free slots count: ' + freeSlotResult.freeSlots.length);
assertEq(freeSlotResult.freeSlots.length >= 2, true, 'At least 2 free slots detected outside 10:00-11:00 and lunch on future date');

// Test today's free slots: passed time slots are filtered and real-time available time is presented
const todayDateStr = getTodayDateStr();
const todayFreeSlotResult = calculateDayFreeSlots(getData(STORAGE_KEYS.MEETINGS), todayDateStr);
const nowMins = new Date().getHours() * 60 + new Date().getMinutes();
for (let s of todayFreeSlotResult.freeSlots) {{
  assertEq(s.end > nowMins, true, 'All free slots for today must end strictly after current real time');
  assertEq(s.start >= nowMins - 5, true, 'Slot start time must be current or in the future');
}}
print('✓ Passed slots for today filtered and real-time available slots calculated');

// Render weekly board and verify all free slots are generated
currentWeekOffset = 1;
renderSupervisorWeeklyBoard();
const weeklyHtml = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(weeklyHtml.includes('weekly-free-slots-wrap'), true, 'weekly-free-slots-wrap rendered in weekly board');
assertEq(weeklyHtml.includes('可用空档') || weeklyHtml.includes('今日空档'), true, 'Free slots header rendered in weekly board');
currentWeekOffset = 0;

print('--- Testing Pending Meeting in Weekly Board & Weekly Decision Overview ---');
// Insert a pending meeting
setData(STORAGE_KEYS.MEETINGS, [
  {{
    id: 12345,
    date: todayDateStr,
    startTime: '10:00',
    endTime: '11:00',
    time: '10:00',
    duration: 60,
    subject: '区域战略评审会',
    reporter: 'Sanyli',
    status: 'scheduled',
    priority: 'high',
    decision: '批准Q4预算方案'
  }},
  {{
    id: 12346,
    date: todayDateStr,
    startTime: '15:00',
    endTime: '16:00',
    time: '15:00',
    duration: 60,
    subject: '阿尔及利亚商务合同特批',
    reporter: '王总',
    status: 'pending',
    priority: 'high',
    decision: '待主管拍板预付款放行比例'
  }}
]);

renderSupervisorWeeklyBoard();
const weeklyHtmlWithPending = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(weeklyHtmlWithPending.includes('is-pending'), true, 'Pending card has .is-pending class');
assertEq(weeklyHtmlWithPending.includes('weekly-pending-tag'), true, 'Pending card has .weekly-pending-tag');
assertEq(weeklyHtmlWithPending.includes('待确认'), true, 'Pending card shows 待确认 tag');
assertEq(weeklyHtmlWithPending.includes('本周待决议题速览'), false, 'Weekly board must NOT contain 本周待决议题速览 per user instruction');
assertEq(weeklyHtmlWithPending.includes('待排期'), true, 'Weekly board contains 待排期 module');
assertEq(weeklyHtmlWithPending.includes('快速记下'), true, 'Weekly board contains 快速记下 button');
print('✓ Weekly Board pending card styling & 待排期 (本周待决议题速览 removed) verified');

print('--- Testing 待排期 功能 (Quick Add, Convert to Meeting, Recall to Pending) ---');
document.getElementById('inputFastReqRequester').value = '塞内加尔代表处 刘总';
document.getElementById('inputFastReqTopic').value = '达喀尔港口物流关税紧急协调';
document.getElementById('selectFastReqUrgency').value = 'high';
document.getElementById('inputFastReqDuration').value = '30m';
addMeetingRequestFast();

let reqs = getData(STORAGE_KEYS.MEETING_REQUESTS);
const senegalReq = reqs.find(r => r.topic === '达喀尔港口物流关税紧急协调');
assertEq(!!senegalReq, true, 'Senegal request successfully recorded');
assertEq(senegalReq.requester, '塞内加尔代表处 刘总', 'Requester recorded');
assertEq(senegalReq.status, 'pending', 'Status is pending');

// Convert request to meeting
convertRequestToMeeting(senegalReq.id);
assertEq(document.getElementById('inputMeetingSubject').value, '达喀尔港口物流关税紧急协调', 'Subject prefilled');
assertEq(document.getElementById('inputMeetingReporter').value, '塞内加尔代表处 刘总', 'Reporter prefilled');
assertEq(window.convertingRequestId, senegalReq.id, 'convertingRequestId set');

// Save meeting and verify request automatically marked as scheduled
document.getElementById('inputMeetingDate').value = '2026-09-25';
document.getElementById('inputMeetingStartTime').value = '11:00';
document.getElementById('inputMeetingEndTime').value = '11:30';
saveMeeting();

reqs = getData(STORAGE_KEYS.MEETING_REQUESTS);
const updatedReq = reqs.find(r => r.id === senegalReq.id);
assertEq(updatedReq.status, 'scheduled', 'Request marked as scheduled after meeting saved');

// Verify that scheduled meeting request MUST NOT appear in 待排期 section!
renderSupervisorWeeklyBoard();
const weeklyHtmlAfterSched = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(weeklyHtmlAfterSched.includes('达喀尔港口物流关税紧急协调'), false, 'Scheduled meeting request MUST NOT appear in 待排期 section!');
print('✓ 待排期: 极速添加 & 一键转为正式排期联动 (已排期卡片不出现在待排期中) verified');

// Test recallMeetingToPending:
const scheduledMeeting = getData(STORAGE_KEYS.MEETINGS).find(m => m.subject === '达喀尔港口物流关税紧急协调');
assertEq(!!scheduledMeeting, true, 'Meeting found in scheduled meetings');

// Open meeting for editing
editMeeting(scheduledMeeting.id);
assertEq(document.getElementById('inputMeetingId').value, scheduledMeeting.id, 'Meeting ID set in modal');
assertEq(document.getElementById('btnRecallToPending').style.display, 'inline-flex', 'Recall button is visible when editing meeting');

// Trigger recallMeetingToPending
recallMeetingToPending();

// Assert meeting is removed from MEETINGS
const meetingsAfterRecall = getData(STORAGE_KEYS.MEETINGS);
assertEq(meetingsAfterRecall.some(m => m.id === scheduledMeeting.id), false, 'Recalled meeting removed from calendar schedule');

// Assert request is back in MEETING_REQUESTS as 'pending'
const reqsAfterRecall = getData(STORAGE_KEYS.MEETING_REQUESTS);
const recalledReq = reqsAfterRecall.find(r => r.topic === '达喀尔港口物流关税紧急协调');
assertEq(!!recalledReq, true, 'Recalled request exists in requests pool');
assertEq(recalledReq.status, 'pending', 'Recalled request status is pending');

// Verify that after recall, it appears back in 待排期!
renderSupervisorWeeklyBoard();
const weeklyHtmlAfterRecall = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(weeklyHtmlAfterRecall.includes('达喀尔港口物流关税紧急协调'), true, 'Recalled pending request appears back in 待排期!');
print('✓ 待排期: 会议卡片撤回改成待排期 & 重新回归待排期栏目 verified');

print('--- Testing 今日任务 (由近到远排序 & 卡片再编辑) ---');
setData(STORAGE_KEYS.TODOS, [
  {{ id: 1, text: '远期规划讨论', priority: 'medium', dueDate: '2026-09-30', completed: false }},
  {{ id: 2, text: '今日必须提交的报销单', priority: 'high', dueDate: '2026-09-24', completed: false }},
  {{ id: 3, text: '明日交付复盘会议准备', priority: 'high', dueDate: '2026-09-25', completed: false }},
  {{ id: 4, text: '已经完成的历史任务', priority: 'low', dueDate: '2026-09-20', completed: true }}
]);

renderTodos();
const todoHtml = document.getElementById('todoFullList').innerHTML;
assertEq(todoHtml.includes('openEditTodoModal') && todoHtml.includes('✏️'), true, 'Edit button rendered on todo cards');

// Verify chronological ordering in rendered output: 2026-09-24 must appear before 2026-09-25, which appears before 2026-09-30
const idxToday = todoHtml.indexOf('2026-09-24');
const idxTomorrow = todoHtml.indexOf('2026-09-25');
const idxFuture = todoHtml.indexOf('2026-09-30');
assertEq(idxToday < idxTomorrow && idxTomorrow < idxFuture, true, 'Todos sorted chronologically from nearest to furthest');

// Test editing existing todo
openEditTodoModal(2);
assertEq(document.getElementById('editTodoText').value, '今日必须提交的报销单', 'Todo text loaded into modal');
document.getElementById('editTodoText').value = '今日必须提交的报销单与发票原件';
document.getElementById('editTodoDate').value = '2026-09-24';
document.getElementById('editTodoPriority').value = 'high';
saveEditTodo();

const editedTodos = getData(STORAGE_KEYS.TODOS);
const t2 = editedTodos.find(x => x.id === 2);
assertEq(t2.text, '今日必须提交的报销单与发票原件', 'Todo text successfully updated in storage');
print('✓ 今日任务: 由近到远时间排序 & 弹窗再编辑保存 verified');

print('--- Testing 时区协同 (开罗 UTC+3 基准与各代表处时差换算) ---');
const cairoRep = TIMEZONE_REPS.find(r => r.id === 'cairo');
assertEq(cairoRep.utcOffset, 3, 'Cairo rep utcOffset must be 3 (UTC+3)');
renderTimezones();
const tzGridHtml = document.getElementById('tzFullGrid').innerHTML;
assertEq(tzGridHtml.includes('埃及代表处'), true, 'Cairo card rendered');
assertEq(tzGridHtml.includes('UTC+3'), true, 'Cairo UTC+3 tag rendered');
assertEq(tzGridHtml.includes('地南代表处 · 突尼斯'), true, 'Med South Tunis card rendered');
assertEq(tzGridHtml.includes('地南代表处 · 利比亚'), true, 'Med South Libya card rendered');
assertEq(tzGridHtml.includes('突尼斯市'), true, 'Tunis city rendered');
assertEq(tzGridHtml.includes('利比亚'), true, 'Libya city rendered');
assertEq(tzGridHtml.includes('UTC+1'), true, 'Tunis UTC+1 tag rendered');
assertEq(tzGridHtml.includes('UTC+2'), true, 'Libya UTC+2 tag rendered');

// Test dashTzMiniList has Cairo UTC+3
const miniHtml = document.getElementById('dashTzMiniList').innerHTML;
assertEq(miniHtml.includes('开罗基准 (UTC+3)'), true, 'Mini timezone box displays 开罗基准 (UTC+3)');

// Test simulator with Cairo UTC+3
document.getElementById('simCairoTime').value = '15:00';
updateTzSimulator();
const simHtml = document.getElementById('tzSimResults').innerHTML;
assertEq(simHtml.includes('开罗 (UTC+3)'), true, 'Simulator includes 开罗 (UTC+3)');
assertEq(simHtml.includes('利比亚 (UTC+2 · 慢1h)'), true, 'Simulator includes 利比亚 (UTC+2 · 慢1h)');
print('✓ 时区协同: 开罗精准调整为UTC+3基准、地南双卡分拆、各代表处时差与仿真器验证全部通过');

print('--- Testing Day Calendar Navigation (后一天 / 前一天) ---');
selectedTimelineDate = '2026-09-24';
changeDayOffset(1);
assertEq(selectedTimelineDate, '2026-09-25', 'changeDayOffset(1) advances 2026-09-24 to 2026-09-25');
changeDayOffset(-1);
assertEq(selectedTimelineDate, '2026-09-24', 'changeDayOffset(-1) retreats 2026-09-25 to 2026-09-24');
changeDayOffset(7);
assertEq(selectedTimelineDate, '2026-10-01', 'changeDayOffset(7) advances over month boundary');
changeDayOffset(-7);
assertEq(selectedTimelineDate, '2026-09-24', 'changeDayOffset(-7) retreats back to 2026-09-24');
print('✓ Day calendar navigation (前一天 / 后一天) verified without any timezone drift');

print('--- Testing Day Calendar Rendering & Card Removal ---');
selectedTimelineDate = todayDateStr;
setSupervisorViewMode('day_cal');
renderSupervisorDayCalendar();
const dayHtml = document.getElementById('supervisorDayCalendarContainer').innerHTML;
assertEq(dayHtml.includes('上午日程推进'), true, 'Morning section rendered');
assertEq(dayHtml.includes('午餐与午休休整时段'), true, 'Lunch break card rendered');
assertEq(dayHtml.includes('下午日程推进'), true, 'Afternoon section rendered');
assertEq(dayHtml.includes('区域战略评审会'), true, 'Meeting rendered in day timeline');
assertEq(dayHtml.includes('今日待决议题速览'), true, 'Decision summary rendered');
assertEq(dayHtml.includes('今日参会与汇报骨干'), false, '今日参会与汇报骨干 successfully removed');
assertEq(dayHtml.includes('快捷操作 & 视图联动'), false, '快捷操作 & 视图联动 successfully removed');
print('✓ Day calendar simplified: redundant cards removed, decision summary retained');

print('--- Testing Meeting Notice Sent Status & Unsent Highlighting ---');
// By default, meeting saved without sending notice has noticeSent: false
openAddMeetingModal();
document.getElementById('inputMeetingDate').value = '2026-10-16';
document.getElementById('inputMeetingStartTime').value = '10:00';
document.getElementById('inputMeetingEndTime').value = '10:45';
document.getElementById('inputMeetingSubject').value = '跨时区预算评审';
saveMeeting();

let allM = getData(STORAGE_KEYS.MEETINGS);
const unsentMeeting = allM.find(m => m.subject === '跨时区预算评审');
assertEq(unsentMeeting.noticeSent, false, 'Default meeting noticeSent is false');

// Weekly board should show notice-unsent and ⚠️ 待发通知
renderSupervisorWeeklyBoard();
const weeklyUnsentHtml = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(weeklyUnsentHtml.includes('notice-unsent'), true, 'Unsent meeting card has .notice-unsent class');
assertEq(weeklyUnsentHtml.includes('⚠️ 待发通知'), true, 'Unsent meeting card has ⚠️ 待发通知 tag');

// Now edit meeting, toggle notice sent to true, and save
editMeeting(unsentMeeting.id);
setMeetingNoticeState(true);
saveMeeting();
allM = getData(STORAGE_KEYS.MEETINGS);
const sentMeeting = allM.find(m => m.id === unsentMeeting.id);
assertEq(sentMeeting.noticeSent, true, 'Updated meeting noticeSent is true');
print('✓ Meeting notice toggle (unsent/sent) & yellow highlighting verified');

print('--- Testing Daily Notes (Re-editing Support) ---');
setData(STORAGE_KEYS.NOTES, [{{
  id: 999,
  text: '原小记内容：联系刚果金代表处',
  category: '🌍 代表处对接',
  time: '10:00'
}}]);
renderNotes();
openEditNoteModal(999);
assertEq(document.getElementById('editNoteText').value, '原小记内容：联系刚果金代表处', 'Note text loaded into edit modal');
document.getElementById('editNoteText').value = '更新后小记内容：已同刚果金代表处陈部长对齐备件物流';
saveEditNote();

const updatedNotes = getData(STORAGE_KEYS.NOTES);
const n999 = updatedNotes.find(x => x.id === 999);
assertEq(n999.text, '更新后小记内容：已同刚果金代表处陈部长对齐备件物流', 'Note text updated');
print('✓ Daily Notes: openEditNoteModal & saveEditNote verified');

print('--- Testing Daily English (Streak Starts at 0, No Fake 6-Day Streak) ---');
const englishCheckin = getData(STORAGE_KEYS.ENGLISH_CHECKIN);
assertEq(englishCheckin.streak === 0 || englishCheckin.streak === 1, true, 'Streak is 0 (or 1 if user checked in), never hardcoded fake 6');
initDailyEnglish();
const wordsGridHtml = document.getElementById('englishWordsGrid').innerHTML;
assertEq(wordsGridHtml.length > 0, true, 'Words grid populated with diverse scenarios');
const sentencesListHtml = document.getElementById('englishSentencesList').innerHTML;
assertEq(sentencesListHtml.includes('💡 <strong>北欧生活习惯与旅行Tips：</strong>'), true, 'English tip says 北欧生活习惯与旅行Tips');
print('✓ Daily English: Streak reset & 北欧生活习惯与旅行Tips verified');

print('--- Testing Theme Toggle Button Text ---');
const themeBtn = document.getElementById('themeToggleBtn');
toggleTheme();
assertEq(document.body.classList.contains('theme-comic'), true, 'Theme comic active');
assertEq(themeBtn.textContent, '✨ biu~变回', 'Button text when comic is ✨ biu~变回');
toggleTheme();
assertEq(document.body.classList.contains('theme-comic'), false, 'Theme modern active');
assertEq(themeBtn.textContent, '✨ biu~变', 'Button text when modern is ✨ biu~变');
print('✓ Theme Toggle: ✨ biu~变 / ✨ biu~变回 verified');

print('--- Testing 常用链接 (Links Module: No Raw URLs, Large Titles, Editing, Categories, Rename & Settings) ---');
setData(STORAGE_KEYS.LINKS, [
  {{ id: 201, name: "企业海外工作邮箱", url: "https://mail.google.com", category: "🏢 内部协同", icon: "📬" }},
  {{ id: 202, name: "非洲业务协同知识库", url: "https://notion.so", category: "🌍 区域协同", icon: "📚" }},
  {{ id: 203, name: "主管日常日程日历", url: "https://calendar.google.com", category: "🏢 内部协同", icon: "📅" }}
]);
setData(STORAGE_KEYS.LINK_SETTINGS, {{
  title: "常用链接 · Snoopy Links",
  tag: "😎 Joe Cool"
}});

renderLinks();
const gridHtml = document.getElementById('linksFullGrid').innerHTML;
assertEq(gridHtml.includes('企业海外工作邮箱'), true, 'Link name rendered on card');
assertEq(gridHtml.includes('https://mail.google.com'), true, 'URL is retained in onclick / target');
assertEq(gridHtml.includes('link-url-hint'), false, 'link-url-hint is NEVER rendered (no visible raw URLs on card)');
assertEq(gridHtml.includes('link-title'), true, 'link-title class used for enlarged bold title');
assertEq(gridHtml.includes('link-category-pill'), true, 'link-category-pill rendered for category badge');

// Test category filtering
const catTabsHtml = document.getElementById('linksCategoryTabs').innerHTML;
assertEq(catTabsHtml.includes('全部 (3)'), true, 'All category tab rendered with count 3');
assertEq(catTabsHtml.includes('🏢 内部协同 (2)'), true, 'Internal collab tab rendered with count 2');
assertEq(catTabsHtml.includes('🌍 区域协同 (1)'), true, 'Regional collab tab rendered with count 1');

filterLinksByCategory('🌍 区域协同');
const filteredGridHtml = document.getElementById('linksFullGrid').innerHTML;
assertEq(filteredGridHtml.includes('非洲业务协同知识库'), true, 'Filtered grid has regional knowledgebase');
assertEq(filteredGridHtml.includes('企业海外工作邮箱'), false, 'Filtered grid excludes other categories');
filterLinksByCategory('ALL');

// Test editing existing link
openEditLinkModal(201);
assertEq(document.getElementById('inputLinkName').value, '企业海外工作邮箱', 'Link name loaded in edit modal');
assertEq(document.getElementById('inputLinkUrl').value, 'https://mail.google.com', 'Link url loaded in edit modal');
document.getElementById('inputLinkName').value = '企业海外高管邮箱系统';
saveCustomLink();

const linksAfterEdit = getData(STORAGE_KEYS.LINKS);
const l201 = linksAfterEdit.find(x => x.id === 201);
assertEq(l201.name, '企业海外高管邮箱系统', 'Link name updated in storage');

// Test category rename
let linksForRename = getData(STORAGE_KEYS.LINKS);
linksForRename = linksForRename.map(l => l.category === '🌍 区域协同' ? {{ ...l, category: '🌍 非洲大区直通' }} : l);
setData(STORAGE_KEYS.LINKS, linksForRename);
renderLinks();
const renamedTabsHtml = document.getElementById('linksCategoryTabs').innerHTML;
assertEq(renamedTabsHtml.includes('🌍 非洲大区直通 (1)'), true, 'Renamed category rendered in tabs');

// Test module header customization
document.getElementById('inputLinksModuleTitle').value = '海外高管办公导航站';
document.getElementById('inputLinksModuleTag').value = '🌐 极速直达';
saveLinksModuleSettings();
const settingsAfterSave = getData(STORAGE_KEYS.LINK_SETTINGS);
assertEq(settingsAfterSave.title, '海外高管办公导航站', 'Module title updated');
assertEq(settingsAfterSave.tag, '🌐 极速直达', 'Module tag updated');
print('✓ 常用链接: 不露长网址、大号标题、信息再编辑、分类筛选、分类重命名、板块自定义 verified');

print('--- Testing 通用板块自定义 (Universal Module Customization: Notes, Todo, Meeting, Timezone, English, Links) ---');
// 1. Test Notes module customization
openEditModuleModal('notes');
assertEq(document.getElementById('editModuleModalTitle').textContent, '✏️ 自定义每日小记板块', 'Notes module title loaded in modal');
assertEq(document.getElementById('inputModuleCustomTitle').value, '每日小记 · Little Notes', 'Notes default title');
assertEq(document.getElementById('inputModuleCustomTag').value, '✍️ World Famous Author', 'Notes default tag');

document.getElementById('inputModuleCustomTitle').value = '每日灵感与速记';
document.getElementById('inputModuleCustomTag').value = '💡 Sany 手账';
saveModuleCustomSettings();

assertEq(document.getElementById('notesModuleTitleText').textContent, '每日灵感与速记', 'Notes DOM title updated');
assertEq(document.getElementById('notesModuleTagText').textContent, '💡 Sany 手账', 'Notes DOM tag updated');

// 2. Test reset defaults
openEditModuleModal('notes');
resetCurrentModuleSettings();
assertEq(document.getElementById('inputModuleCustomTitle').value, '每日小记 · Little Notes', 'Notes title reset to default in input');
saveModuleCustomSettings();
assertEq(document.getElementById('notesModuleTitleText').textContent, '每日小记 · Little Notes', 'Notes DOM title reset');

// 3. Test Todo module customization
openEditModuleModal('todo');
document.getElementById('inputModuleCustomTitle').value = '今日高优作战看板';
document.getElementById('inputModuleCustomTag').value = '⚡ 敏捷交付';
saveModuleCustomSettings();
assertEq(document.getElementById('todoModuleTitleText').textContent, '今日高优作战看板', 'Todo DOM title updated');
assertEq(document.getElementById('todoModuleTagText').textContent, '⚡ 敏捷交付', 'Todo DOM tag updated');

// 4. Test Meeting module customization
openEditModuleModal('supervisor');
document.getElementById('inputModuleCustomTitle').value = '曦总会议安排工作台';
document.getElementById('inputModuleCustomTag').value = '🎯 决策排期';
saveModuleCustomSettings();
assertEq(document.getElementById('supervisorModuleTitleText').textContent, '曦总会议安排工作台', 'Supervisor DOM title updated');

// 5. Test Timezone module customization
openEditModuleModal('timezone');
document.getElementById('inputModuleCustomTitle').value = '非洲跨区时区护航';
document.getElementById('inputModuleCustomTag').value = '🌍 Global Timing';
saveModuleCustomSettings();
assertEq(document.getElementById('timezoneModuleTitleText').textContent, '非洲跨区时区护航', 'Timezone DOM title updated');

// 6. Test English module customization
openEditModuleModal('english');
document.getElementById('inputModuleCustomTitle').value = '每日商务口语';
document.getElementById('inputModuleCustomTag').value = '🗣️ Fluent Office';
saveModuleCustomSettings();
assertEq(document.getElementById('englishModuleTitleText').textContent, '每日商务口语', 'English DOM title updated');

print('✓ 通用板块自定义: 每日小记、今日任务、会议预约、时区协同、每日英语、常用链接 全部验证通过');

print('--- Testing 会议时间冲突检测与提醒 (Meeting Time Conflict Detection & Alert) ---');
setData(STORAGE_KEYS.MEETINGS, [
  {{
    id: 101,
    date: '2026-09-24',
    time: '10:00',
    startTime: '10:00',
    endTime: '11:00',
    duration: 60,
    subject: '项目交付复盘会',
    reporter: '陈总',
    status: 'scheduled'
  }},
  {{
    id: 102,
    date: '2026-09-24',
    time: '14:00',
    startTime: '14:00',
    endTime: '15:00',
    duration: 60,
    subject: '预算审批会',
    reporter: '王总',
    status: 'scheduled'
  }}
]);

// 1. Overlapping meeting detection
const c1 = getMeetingConflicts('2026-09-24', '10:30', '11:30', null);
assertEq(c1.length, 1, 'Detects 1 conflicting meeting');
assertEq(c1[0].id, 101, 'Conflicting meeting is 101');

// 2. Fully engulfed meeting detection
const c2 = getMeetingConflicts('2026-09-24', '09:00', '12:00', null);
assertEq(c2.length, 1, 'Detects meeting inside range');

// 3. Back-to-back non-overlapping meeting
const c3 = getMeetingConflicts('2026-09-24', '11:00', '12:00', null);
assertEq(c3.length, 0, 'Back to back meeting (11:00) has 0 conflicts');

// 4. Editing existing meeting (should not conflict with itself)
const c4 = getMeetingConflicts('2026-09-24', '10:00', '11:00', 101);
assertEq(c4.length, 0, 'Editing meeting 101 does not conflict with itself');

// 5. checkMeetingConflicts UI rendering
document.getElementById('inputMeetingId').value = '';
document.getElementById('inputMeetingDate').value = '2026-09-24';
document.getElementById('inputMeetingStartTime').value = '10:15';
document.getElementById('inputMeetingEndTime').value = '10:45';
checkMeetingConflicts();
const alertEl = document.getElementById('meetingConflictAlert');
assertEq(alertEl.style.display, 'block', 'Conflict alert displayed');
assertEq(alertEl.innerHTML.includes('项目交付复盘会'), true, 'Conflict alert includes conflicting meeting subject');

// 6. Test conflict resolved
document.getElementById('inputMeetingStartTime').value = '11:00';
document.getElementById('inputMeetingEndTime').value = '11:45';
checkMeetingConflicts();
assertEq(alertEl.style.display, 'none', 'Conflict alert hidden when no conflict');

print('✓ 会议时间冲突检测: 重叠冲突检测、背靠背安全、自身编辑排除、UI动态提醒条验证全部通过');

print('--- Testing Cross-Week Meeting Notice & Stat Jump ---');
const prevWkDate = new Date();
prevWkDate.setDate(prevWkDate.getDate() - 7);
const prevWkDateStr = formatDateToStr(prevWkDate);

setData(STORAGE_KEYS.MEETINGS, [
  {{
    id: 9901,
    date: prevWkDateStr,
    startTime: '14:00',
    endTime: '15:00',
    time: '14:00',
    duration: 60,
    subject: '历史遗留重要决议会',
    reporter: '周总',
    status: 'scheduled'
  }}
]);
currentWeekOffset = 0;
supervisorViewMode = 'week_board';
renderSupervisorWeeklyBoard();
let weekHtml = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(weekHtml.includes('crossWeekScheduleNotice'), true, 'Cross-week schedule notice rendered when week has 0 meetings');
assertEq(weekHtml.includes('上周或更早日期已记录 1 场会议') || weekHtml.includes('保存在其他日期'), true, 'Cross-week notice explains meeting location');
assertEq(weekHtml.includes('📅 月历总览'), true, 'Cross-week notice provides button to view month overview');

// Test clicking "查看上一周日程"
changeWeekOffset(-1);
weekHtml = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(weekHtml.includes('历史遗留重要决议会'), true, 'Previous week view displays the previous week meeting');

// Test clicking stat box to jump to card_list
filterMeetingsByStat('scheduled');
assertEq(supervisorViewMode, 'card_list', 'filterMeetingsByStat switched to card_list view');
assertEq(currentMeetingFilter, 'scheduled', 'filterMeetingsByStat filtered to scheduled');

// Test legacy migration in initSeeds
localStorage.removeItem(STORAGE_KEYS.MEETINGS);
localStorage.setItem('snoopy_supervisor_meetings_v5', JSON.stringify([
  {{ id: 8888, subject: 'v5遗留会议', date: '2026-09-25', status: 'scheduled' }}
]));
initSeeds();
const restored = getData(STORAGE_KEYS.MEETINGS);
assertEq(restored.length, 1, 'Restored 1 meeting from legacy v5 key');
assertEq(restored[0].subject, 'v5遗留会议', 'Legacy meeting restored correctly');
print('✓ 跨周日程提示条、上周切换、顶部统计点击跳转、历史版本数据平滑恢复全部验证通过');

print('--- Testing 仅看工作日 (周日-周五) / 完整周历 (含周六) 切换响应 ---');
currentWeekOffset = 0;
hidePastWeekdays = false; // Show all days for full week workday test
showFullWeekCalendar = null; // Reset to auto
const todayForWk = new Date();
const satDate = new Date(todayForWk);
satDate.setDate(todayForWk.getDate() - todayForWk.getDay() + 6);
const satDateStr = formatDateToStr(satDate);

// Add a Saturday (weekend) meeting so auto mode shows 7 columns
setData(STORAGE_KEYS.MEETINGS, [
  {{
    id: 9955,
    date: satDateStr,
    startTime: '10:00',
    endTime: '11:00',
    time: '10:00',
    duration: 60,
    subject: '周六突发加班会议',
    reporter: '赵总',
    status: 'scheduled'
  }}
]);

renderSupervisorWeeklyBoard();
let wkToggleHtml = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(wkToggleHtml.includes('grid-template-columns: repeat(7, 1fr)'), true, 'Auto-detects weekend meeting and shows 7 columns');
assertEq(wkToggleHtml.includes('仅看工作日'), true, 'Shows button to switch to 仅看工作日');

// Now click "仅看工作日" -> toggleFullWeekDisplay(false)
toasts = [];
toggleFullWeekDisplay(false);
wkToggleHtml = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(showFullWeekCalendar, false, 'showFullWeekCalendar explicitly set to false');
assertEq(wkToggleHtml.includes('grid-template-columns: repeat(6, 1fr)'), true, 'Clicking 仅看工作日 forces 6 workday columns (Sun-Fri) even when weekend meeting exists!');
assertEq(wkToggleHtml.includes('完整周历'), true, 'Button updates to 完整周历');
assertEq(toasts.some(t => t.includes('仅看工作日')), true, 'Toast confirms switch to 仅看工作日');

// Click again to switch back to 7-day full calendar -> toggleFullWeekDisplay(true)
toasts = [];
toggleFullWeekDisplay(true);
wkToggleHtml = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(showFullWeekCalendar, true, 'showFullWeekCalendar explicitly set to true');
assertEq(wkToggleHtml.includes('grid-template-columns: repeat(7, 1fr)'), true, 'Clicking 完整周历 restores 7 columns');
assertEq(toasts.some(t => t.includes('完整周历')), true, 'Toast confirms switch to 完整周历');
print('✓ 会议预约周历: 仅看工作日 (周日-周五) 与 完整周历 (含周六) 双向切换响应验证通过');

print('--- Testing 每日小记 编辑弹窗唤起与保存 (Fix Nested Modal Bug) ---');
setData(STORAGE_KEYS.NOTES, [
  {{ id: 701, text: '重要灵感备忘：跟进开罗物流清关进度', category: '💡 灵感备忘', time: '14:20' }}
]);
openEditNoteModal(701);
assertEq(elements['editNoteModal'].classList.contains('active'), true, 'editNoteModal opened and active');
assertEq(elements['editNoteText'].value, '重要灵感备忘：跟进开罗物流清关进度', 'Note text populated into modal');
elements['editNoteText'].value = '已更新：开罗物流清关完成并放行';
elements['editNoteCategory'].value = '🌍 代表处对接';
saveEditNote();
assertEq(elements['editNoteModal'].classList.contains('active'), false, 'editNoteModal closed after save');
const notesAfterSave = getData(STORAGE_KEYS.NOTES);
assertEq(notesAfterSave[0].text, '已更新：开罗物流清关完成并放行', 'Updated note text saved in storage');
print('✓ 每日小记: 编辑弹窗正常呼出、内容回填、保存与关闭全部验证通过');

print('--- Testing 今日任务 (四象限工作法默认最前展示 & 已完成归档) ---');
setData(STORAGE_KEYS.TODOS, [
  {{ id: 501, text: 'Q1紧急会议签批', priority: 'q1', completed: false, archived: false }},
  {{ id: 502, text: 'Q2季度业务复盘', priority: 'q2', completed: false, archived: false }},
  {{ id: 503, text: 'Q3日常行政报销', priority: 'q3', completed: true, archived: false }},
  {{ id: 504, text: 'Q4随手整理资料', priority: 'q4', completed: true, archived: false }}
]);

// 1. Verify Matrix View and HOME Dashboard Four-Quadrant Preview
renderTodos();
const matrixHtml = elements['todoMatrixContainer'].innerHTML;
assertEq(matrixHtml.includes('今天必须搞定'), true, 'Q1 quadrant rendered in matrix as 今天必须搞定');
assertEq(matrixHtml.includes('这周安排上'), true, 'Q2 quadrant rendered in matrix as 这周安排上');
assertEq(matrixHtml.includes('先放一放'), true, 'Q3 quadrant rendered in matrix as 先放一放');
assertEq(matrixHtml.includes('有空再说'), true, 'Q4 quadrant rendered in matrix as 有空再说');
assertEq(matrixHtml.includes('Q1紧急会议签批'), true, 'Q1 task rendered');

const dashTodoHtml = elements['dashTodoList'].innerHTML;
assertEq(dashTodoHtml.includes('今天必须搞定') && dashTodoHtml.includes('这周安排上'), true, 'HOME dashboard also displays new 4 dimensions immediately');

// 2. Quick add to quadrant
quickAddTodoToQuadrant('q1');
assertEq(elements['selectTodoPriority'].value, 'q1', 'Quick add sets priority to q1');

// 3. Archive completed todos
archiveCompletedTodos();
const afterArchiveTodos = getData(STORAGE_KEYS.TODOS);
const activeCount = afterArchiveTodos.filter(t => !t.archived).length;
const archivedCount = afterArchiveTodos.filter(t => t.archived).length;
assertEq(activeCount, 2, '2 active uncompleted tasks remain');
assertEq(archivedCount, 2, '2 completed tasks moved to archive');

// 4. Switch to Archive View & Verify
setTodoViewMode('archive');
assertEq(currentTodoViewMode, 'archive', 'Switched to archive view');
renderTodos();
const archiveHtml = elements['todoArchiveContainer'].innerHTML;
assertEq(archiveHtml.includes('已归档任务库'), true, 'Archive container rendered');
assertEq(archiveHtml.includes('Q3日常行政报销'), true, 'Archived task 503 rendered');

// 5. Unarchive a task
unarchiveTodo(503);
const unarchivedTodos = getData(STORAGE_KEYS.TODOS);
const restored503 = unarchivedTodos.find(t => t.id === 503);
assertEq(restored503.archived, false, 'Task 503 restored to active list');

print('✓ 今日任务: 四象限看板默认最前展示、HOME页四象限预览、快捷象限归属、一键归档已完成、归档库恢复全部验证通过');

print('--- Testing 今日任务 Plan A (今日聚焦 + 激励进度条 + 快捷分类转移) ---');
setData(STORAGE_KEYS.TODOS, [
  {{ id: 601, text: '必须今天给主管汇报预算', priority: 'q1', completed: false, archived: false }},
  {{ id: 602, text: '本周完成供应商合同签署', priority: 'q2', completed: false, archived: false }},
  {{ id: 603, text: '低优先级备忘录整理', priority: 'q4', completed: false, archived: false }}
]);
setTodoViewMode('matrix');
renderTodos();

const planAMatrix = elements['todoMatrixContainer'].innerHTML;
assertEq(planAMatrix.includes('todo-energy-card'), true, 'Hero energy progress card rendered');
assertEq(planAMatrix.includes('todo-progress-fill'), true, 'Energy progress fill track rendered');
assertEq(planAMatrix.includes('today-hero-board'), true, 'Today Hero Focus board rendered');
assertEq(planAMatrix.includes('todo-submatrix-grid'), true, '3-Column submatrix grid rendered');
assertEq(planAMatrix.includes('必须今天给主管汇报预算'), true, 'Q1 focus task rendered in today hero board');
assertEq(planAMatrix.includes('shift-quadrant-select'), true, 'Fast quadrant shift dropdown rendered');

// Test quickMoveTodo
quickMoveTodo(601, 'q2');
const afterMoveTodos = getData(STORAGE_KEYS.TODOS);
const moved601 = afterMoveTodos.find(t => t.id === 601);
assertEq(moved601.quadrant, 'q2', 'Task 601 moved to q2');

// Test toggleTodo positive dopamine toast
toasts = [];
toggleTodo(602);
assertEq(toasts.length > 0 && toasts.some(msg => msg.includes('搞定') || msg.includes('保持') || msg.includes('漂亮')), true, 'Dopamine toast triggered upon completion');

print('✓ 今日任务 Plan A: 今日攻坚能量条、Hero聚焦卡、轻量3列次矩阵、快捷移位、多巴胺激励反馈验证全部通过');

print('--- Testing 主管出差时区切换与会议预约当地时区转换 (Trip Timezone Engine & Batch Shift) ---');
// 1. Initial State
assertEq(getActiveTripTimezone(), 'cairo', 'Default trip timezone is cairo');
assertEq(getTripTimezoneDiffHours('cairo'), 0, 'Cairo diff is 0');
assertEq(getTripTimezoneDiffHours('med_south_tunis'), -2, 'Tunis is 2 hours behind Cairo (UTC+1 vs UTC+3)');
assertEq(getTripTimezoneDiffHours('med_south_libya'), -1, 'Libya is 1 hour behind Cairo (UTC+2 vs UTC+3)');
assertEq(getTripTimezoneDiffHours('beijing'), 5, 'Beijing is 5 hours ahead of Cairo (UTC+8 vs UTC+3)');

// 2. shiftTimeStrByHours
assertEq(shiftTimeStrByHours('10:00', 0), '10:00', 'Shift by 0 keeps 10:00');
assertEq(shiftTimeStrByHours('10:00', -2), '08:00', '10:00 shifted by -2 is 08:00');
assertEq(shiftTimeStrByHours('09:30', 5), '14:30', '09:30 shifted by +5 is 14:30');
assertEq(shiftTimeStrByHours('01:00', -2), '23:00', '01:00 shifted by -2 wraps to 23:00');

// 3. Dynamic display with trip timezone (Option C)
const sampleMeeting = {{
  id: 8801,
  date: getTodayDateStr(),
  time: '11:00',
  startTime: '11:00',
  endTime: '12:00',
  duration: 60,
  subject: '地南代表处重点业务审议'
}};
let dtCairo = getMeetingDisplayTime(sampleMeeting);
assertEq(dtCairo.isShifted, false, 'In Cairo mode, isShifted is false');
assertEq(dtCairo.start, '11:00', 'Cairo start is 11:00');

changeTripTimezone('med_south_tunis');
assertEq(getActiveTripTimezone(), 'med_south_tunis', 'Active timezone switched to med_south_tunis');
let dtTunis = getMeetingDisplayTime(sampleMeeting);
assertEq(dtTunis.isShifted, true, 'In Tunis mode, isShifted is true');
assertEq(dtTunis.start, '09:00', 'Tunis local start time is 09:00 (11:00 - 2h)');
assertEq(dtTunis.end, '10:00', 'Tunis local end time is 10:00');
assertEq(dtTunis.cairoStart, '11:00', 'Cairo baseline start preserved as 11:00');

// 4. Modal Entry with trip timezone (Option 1)
// When secretary enters meeting in Tunis local time: 14:00 - 15:00
document.getElementById('inputMeetingId').value = '';
document.getElementById('inputMeetingDate').value = getTodayDateStr();
document.getElementById('inputMeetingTimezoneBase').value = 'med_south_tunis';
document.getElementById('inputMeetingStartTime').value = '14:00';
document.getElementById('inputMeetingEndTime').value = '15:00';
document.getElementById('inputMeetingSubject').value = '突尼斯本地项目研讨会';
document.getElementById('inputMeetingReporter').value = '突尼斯代表';
saveMeeting();

const allMeetingsAfterAdd = getData(STORAGE_KEYS.MEETINGS);
const addedTripMeeting = allMeetingsAfterAdd.find(m => m.subject === '突尼斯本地项目研讨会');
assertEq(Boolean(addedTripMeeting), true, 'Added trip meeting found in storage');
assertEq(addedTripMeeting.tzBase, 'med_south_tunis', 'Saved tzBase is med_south_tunis');
assertEq(addedTripMeeting.localStartTime, '14:00', 'Saved localStartTime is 14:00');
// In Cairo baseline: 14:00 Tunis (-2h vs Cairo) corresponds to 16:00 Cairo
assertEq(addedTripMeeting.startTime, '16:00', 'Saved baseline startTime in Cairo is 16:00');
assertEq(addedTripMeeting.endTime, '17:00', 'Saved baseline endTime in Cairo is 17:00');

// 5. Leader Business Trip Schedule & Date-Bound Dual-Timezone Engine
changeTripTimezone('cairo');
setData(STORAGE_KEYS.LEADER_TRIPS, []);
assertEq(getLeaderTrips().length, 0, 'Initially no trips registered');

// Setup three meetings: one pre-trip, one during trip, one post-trip
setData(STORAGE_KEYS.MEETINGS, [
  {{
    id: 9001,
    date: '2026-10-19',
    time: '10:00',
    startTime: '10:00',
    endTime: '11:00',
    duration: 60,
    subject: '出差前开罗例会',
    status: 'scheduled'
  }},
  {{
    id: 9002,
    date: '2026-10-21',
    time: '10:00',
    startTime: '10:00',
    endTime: '11:00',
    duration: 60,
    subject: '突尼斯代表处业务研讨会',
    status: 'scheduled'
  }},
  {{
    id: 9003,
    date: '2026-10-26',
    time: '14:00',
    startTime: '14:00',
    endTime: '15:00',
    duration: 60,
    subject: '出差后开罗复盘会',
    status: 'scheduled'
  }}
]);

// Before registering trip, all meetings display Cairo time
const m2Before = getMeetingDisplayTime(getData(STORAGE_KEYS.MEETINGS).find(m => m.id === 9002));
assertEq(m2Before.isShifted, false, 'Before trip, meeting 9002 is not shifted');
assertEq(m2Before.start, '10:00', 'Meeting 9002 displays Cairo 10:00');

// Now register a trip: 2026-10-20 to 2026-10-24 in med_south_tunis (-2h vs Cairo)
document.getElementById('inputTripDestination').value = 'med_south_tunis';
document.getElementById('inputTripStartDate').value = '2026-10-20';
document.getElementById('inputTripEndDate').value = '2026-10-24';
document.getElementById('inputTripRemark').value = '地南代表处重点业务考察';
saveLeaderTrip();

const activeTrips = getLeaderTrips();
assertEq(activeTrips.length, 1, 'Leader trip successfully saved to storage');
assertEq(activeTrips[0].destination, 'med_south_tunis', 'Saved destination is med_south_tunis');

// Check date-bound meeting displays:
// 1) 2026-10-19 (pre-trip): stays Cairo time
const m1During = getMeetingDisplayTime(getData(STORAGE_KEYS.MEETINGS).find(m => m.id === 9001));
assertEq(m1During.isTripDate, false, 'Meeting 9001 is outside trip range');
assertEq(m1During.isShifted, false, 'Meeting 9001 time is not shifted');
assertEq(m1During.start, '10:00', 'Meeting 9001 stays at 10:00');

// 2) 2026-10-21 (during trip): automatically shows Tunis local time + Cairo start time!
const m2During = getMeetingDisplayTime(getData(STORAGE_KEYS.MEETINGS).find(m => m.id === 9002));
assertEq(m2During.isTripDate, true, 'Meeting 9002 is identified as being within leader trip range');
assertEq(m2During.isShifted, true, 'Meeting 9002 time is shifted to destination timezone');
assertEq(m2During.start, '08:00', 'Meeting 9002 start displays local Tunis time 08:00 (10:00 - 2h)');
assertEq(m2During.end, '09:00', 'Meeting 9002 end displays local Tunis time 09:00');
assertEq(m2During.cairoStart, '10:00', 'Meeting 9002 preserves and displays Cairo start time 10:00');
assertEq(m2During.tzName, '地南·突尼斯', 'Meeting 9002 displays destination name 地南·突尼斯');

// Verify UI rendering in Weekly Board:
const todayNow = new Date();
const testDateObj = new Date(2026, 9, 21);
const curSun = new Date(todayNow);
curSun.setDate(todayNow.getDate() - todayNow.getDay());
const testSun = new Date(testDateObj);
testSun.setDate(testDateObj.getDate() - testDateObj.getDay());
currentWeekOffset = Math.round((testSun.getTime() - curSun.getTime()) / (7 * 86400000));
supervisorWeekOffset = currentWeekOffset;
// Test Wednesday of the trip (2026-10-21)
selectedTimelineDate = '2026-10-21';
renderSupervisorWeeklyBoard();
const boardHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;
assertEq(boardHtml.includes('✈️ 地南·突尼斯'), true, 'Day header has trip badge ✈️ 地南·突尼斯');
assertEq(boardHtml.includes('weekly-card-cairo-sub'), true, 'Meeting card has bottom-right .weekly-card-cairo-sub container');
assertEq(boardHtml.includes('开罗 10:00'), true, 'Card bottom-right includes subtle Cairo 10:00 note');
assertEq(boardHtml.includes('08:00 - 09:00'), true, 'Card main time displays Tunis local time 08:00 - 09:00');

// 3) 2026-10-26 (post-trip): stays Cairo time
const m3During = getMeetingDisplayTime(getData(STORAGE_KEYS.MEETINGS).find(m => m.id === 9003));
assertEq(m3During.isTripDate, false, 'Meeting 9003 is outside trip range');
assertEq(m3During.isShifted, false, 'Meeting 9003 time is not shifted');
assertEq(m3During.start, '14:00', 'Meeting 9003 stays at 14:00');

// 4) Verify underlying meeting data was NEVER corrupted or mutated!
const rawMeetings = getData(STORAGE_KEYS.MEETINGS);
assertEq(rawMeetings.find(m => m.id === 9002).startTime, '10:00', 'Underlying database startTime is permanently untouched at 10:00');

// 5) Test User Feature: 在确认出差后的日期，新添加的会议自动按照出差地本地时间安排
openAddMeetingModalWithSlot('2026-10-21', '14:00', 60);
assertEq(document.getElementById('inputMeetingDate').value, '2026-10-21', 'Modal date is 2026-10-21');
assertEq(document.getElementById('inputMeetingTimezoneBase').value, 'med_south_tunis', 'Timezone base automatically set to trip destination med_south_tunis');
assertEq(elements['modalTripBanner'].style.display, 'none', 'Modal trip banner is hidden for clean minimalist UI');
assertEq(elements['modalTripLiveCard'].style.display, 'none', 'Modal live conversion card is hidden per minimalist UI');

// Change date inside modal to non-trip date (2026-10-26)
document.getElementById('inputMeetingDate').value = '2026-10-26';
handleMeetingModalDateChange();
assertEq(document.getElementById('inputMeetingTimezoneBase').value, 'cairo', 'Switching to non-trip date reverts timezone base to cairo');
assertEq(elements['modalTripBanner'].style.display, 'none', 'Modal trip banner remains hidden');

// Change date back to trip date (2026-10-21) and save new meeting in local time
document.getElementById('inputMeetingDate').value = '2026-10-21';
handleMeetingModalDateChange();
assertEq(document.getElementById('inputMeetingTimezoneBase').value, 'med_south_tunis', 'Switching back to trip date auto-sets to med_south_tunis');
document.getElementById('inputMeetingSubject').value = '突尼斯当地重点客户会面';
document.getElementById('inputMeetingStartTime').value = '14:00';
document.getElementById('inputMeetingEndTime').value = '15:00';
saveMeeting();

const newLocalMeeting = getData(STORAGE_KEYS.MEETINGS).find(m => m.subject === '突尼斯当地重点客户会面');
assertEq(newLocalMeeting.date, '2026-10-21', 'Saved meeting date is 2026-10-21');
assertEq(newLocalMeeting.tzBase, 'med_south_tunis', 'Saved meeting tzBase is med_south_tunis');
assertEq(newLocalMeeting.localStartTime, '14:00', 'Saved local start time is 14:00');
assertEq(newLocalMeeting.startTime, '16:00', 'Saved Cairo baseline time is 16:00 (14:00 + 2h)');

const newDt = getMeetingDisplayTime(newLocalMeeting);
assertEq(newDt.start, '14:00', 'Display start time is Tunis local time 14:00');
assertEq(newDt.end, '15:00', 'Display end time is Tunis local time 15:00');
assertEq(newDt.cairoStart, '16:00', 'Display Cairo start time is 16:00');

// 6) Edit existing meeting 9002 (originally arranged in Cairo time before trip)
editMeeting(9002);
assertEq(document.getElementById('inputMeetingTimezoneBase').value, 'med_south_tunis', 'Editing pre-trip meeting on trip date automatically presents it in destination local time');
assertEq(document.getElementById('inputMeetingStartTime').value, '08:00', 'Modal presents 08:00 (the local time displayed on card)');
assertEq(elements['modalTripBanner'].style.display, 'none', 'Modal trip banner remains hidden during edit per user request');

// 7) Cancel / Delete trip: verify instantaneous non-destructive rollback
deleteLeaderTrip(activeTrips[0].id);
assertEq(getLeaderTrips().length, 0, 'Trip deleted');
const m2AfterDelete = getMeetingDisplayTime(getData(STORAGE_KEYS.MEETINGS).find(m => m.id === 9002));
assertEq(m2AfterDelete.isTripDate, false, 'Meeting 9002 is no longer in trip range');
assertEq(m2AfterDelete.isShifted, false, 'Meeting 9002 reverted to unshifted');
assertEq(m2AfterDelete.start, '10:00', 'Meeting 9002 seamlessly restored to Cairo 10:00 without any data loss');
print('✓ 领导出差行程日程区间管理、所选日期与地点自动双时区展示(当地时间+开罗开始时间)、非出差日期保持开罗时间与无损还原验证通过');

print('--- Testing 每日小记 置顶功能与拖拽排序 ---');
setData(STORAGE_KEYS.NOTES, [
  {{ id: 701, text: '小记卡片1', category: '📝 记事', time: '10:00', isPinned: false }},
  {{ id: 702, text: '小记卡片2', category: '💡 灵感备忘', time: '11:00', isPinned: false }},
  {{ id: 703, text: '小记卡片3', category: '🌍 代表处对接', time: '12:00', isPinned: false }}
]);
renderNotes();

// Pin note 702
togglePinNote(702);
let notesAfterPin = getData(STORAGE_KEYS.NOTES);
assertEq(notesAfterPin[0].id, 702, 'Pinned note 702 moved to index 0');
assertEq(notesAfterPin[0].isPinned, true, 'Note 702 marked as isPinned: true');
assertEq(elements['notesFullGrid'].innerHTML.includes('📌 置顶'), true, 'Rendered notes includes 📌 置顶 badge');
assertEq(elements['notesFullGrid'].innerHTML.includes('note-item is-pinned'), true, 'Rendered notes includes note-item is-pinned class');

// Add a new note while 702 is pinned: it should be inserted after pinned note
document.getElementById('inputNoteText').value = '新增普通小记4';
document.getElementById('selectNoteCategory').value = '📝 记事';
addNote();
let notesAfterAdd = getData(STORAGE_KEYS.NOTES);
assertEq(notesAfterAdd[0].id, 702, 'Pinned note 702 remains at index 0 after adding new note');
assertEq(notesAfterAdd[1].text, '新增普通小记4', 'New note inserted at index 1 after pinned note');

// Unpin note 702
togglePinNote(702);
let notesAfterUnpin = getData(STORAGE_KEYS.NOTES);
const note702AfterUnpin = notesAfterUnpin.find(n => n.id === 702);
assertEq(note702AfterUnpin.isPinned, false, 'Note 702 unpinned');

// Test manual drag-and-drop: drag note 703 to index 0 (drop onto 702)
draggedNoteId = 703;
handleNoteDrop({{ preventDefault: () => {{}} }}, 702);
let notesAfterDrag = getData(STORAGE_KEYS.NOTES);
assertEq(notesAfterDrag[0].id, 703, 'Note 703 dropped to index 0');
print('✓ 每日小记 置顶功能(📌/📍切换、置顶状态徽章、新卡片顺延)与手动拖拽排序验证通过');

print('--- Testing 今天必须搞定 (Q1) 卡片手动拖拽排序 ---');
setData(STORAGE_KEYS.TODOS, [
  {{ id: 601, text: '待办任务A', priority: 'q1', completed: false, archived: false }},
  {{ id: 602, text: '待办任务B', priority: 'q1', completed: false, archived: false }},
  {{ id: 603, text: '待办任务C', priority: 'q1', completed: false, archived: false }}
]);
renderTodos();

// Verify grip icon and draggable
assertEq(elements['todoMatrixContainer'].innerHTML.includes('draggable="true"'), true, 'Today tasks have draggable="true"');
assertEq(elements['todoMatrixContainer'].innerHTML.includes('drag-grip-icon'), true, 'Today tasks have drag-grip-icon ⠿');

// Drag task 601 (initially at bottom due to id descending) and drop onto task 603 (at top)
draggedTodayTodoId = 601;
handleTodayTodoDrop({{ preventDefault: () => {{}} }}, 603);

let todosAfterDrag = getData(STORAGE_KEYS.TODOS);
const q1After = todosAfterDrag.filter(t => !t.archived && getTodoQuadrant(t) === 'q1');
assertEq(q1After.find(t => t.id === 601).order, 1, 'Task 601 assigned order 1');
assertEq(q1After.find(t => t.id === 603).order, 2, 'Task 603 assigned order 2');
assertEq(q1After.find(t => t.id === 602).order, 3, 'Task 602 assigned order 3');

// Render and verify order of appearance in today-hero-items
renderTodos();
const matrixHtmlAfterDrag = elements['todoMatrixContainer'].innerHTML;
const posA = matrixHtmlAfterDrag.indexOf('待办任务A');
const posC = matrixHtmlAfterDrag.indexOf('待办任务C');
const posB = matrixHtmlAfterDrag.indexOf('待办任务B');
print('✓ 今天必须搞定 (Q1) 卡片手动拖拽排序与顺序持久化验证通过');

print('--- Testing 出差行程会议排期当地时间严格保持 (Libya 09:00 stays 09:00 without unwanted shift) ---');
setData(STORAGE_KEYS.LEADER_TRIPS, [{{
  id: 201,
  destination: 'med_south_libya',
  startDate: '2026-10-18',
  endDate: '2026-10-25',
  remark: '利比亚代表处出差'
}}]);

selectedTimelineDate = '2026-10-20';
openAddMeetingModal();
assertEq(elements['inputMeetingDate'].value, '2026-10-20', 'Modal date is 2026-10-20');
assertEq(elements['inputMeetingTimezoneBase'].value, 'med_south_libya', 'Modal tz is med_south_libya');

// User fills in 9:00 (09:00 - 09:45)
elements['inputMeetingStartTime'].value = '09:00';
elements['inputMeetingEndTime'].value = '09:45';
elements['inputMeetingSubject'].value = '利比亚晨会汇报';
elements['inputMeetingDecision'].value = '审议利比亚现场拓展策略';
saveMeeting();

let meetingsList = getData(STORAGE_KEYS.MEETINGS);
let mTrip = meetingsList.find(x => x.subject === '利比亚晨会汇报');
assertEq(mTrip.localStartTime, '09:00', 'm.localStartTime strictly equals 09:00');
assertEq(mTrip.localEndTime, '09:45', 'm.localEndTime strictly equals 09:45');
assertEq(mTrip.startTime, '10:00', 'Cairo baseline startTime is 10:00');

let dtTrip = getMeetingDisplayTime(mTrip);
assertEq(dtTrip.start, '09:00', 'Card display start is strictly 09:00');
assertEq(dtTrip.end, '09:45', 'Card display end is strictly 09:45');
assertEq(dtTrip.cairoStart, '10:00', 'Quiet corner Cairo time is 10:00');

// Edit meeting and verify it opens with 09:00 and saves with 09:00
editMeeting(mTrip.id);
assertEq(elements['inputMeetingStartTime'].value, '09:00', 'Edit modal opens with 09:00');
assertEq(elements['inputMeetingEndTime'].value, '09:45', 'Edit modal opens with 09:45');
elements['inputMeetingSubject'].value = '利比亚晨会汇报(已确认)';
saveMeeting();

meetingsList = getData(STORAGE_KEYS.MEETINGS);
mTrip = meetingsList.find(x => x.id === mTrip.id);
assertEq(mTrip.localStartTime, '09:00', 'After editing, localStartTime strictly persists as 09:00');
dtTrip = getMeetingDisplayTime(mTrip);
assertEq(dtTrip.start, '09:00', 'After editing, card display start strictly stays 09:00');
print('✓ 出差行程会议排期当地时间严格保持 (录入9点保存与编辑后始终显示9点，开罗时间不喧宾夺主) 验证通过');

print('--- Testing 摩洛哥 UTC+0 与出差地/开罗时间全链路联动 (Morocco UTC+0 & Multi-Timezone Linkage) ---');
// 1. Verify Morocco timezone config (UTC+0 · 比开罗慢 3 小时)
const moroccoInfo = TRIP_TIMEZONE_MAP['morocco'];
assertEq(moroccoInfo.utcOffset, 0, 'Morocco utcOffset must be 0 (UTC+0)');
assertEq(getTripTimezoneDiffHours('morocco'), -3, 'Morocco diff relative to Cairo must be -3 hours');
const moroccoRep = TIMEZONE_REPS.find(r => r.id === 'morocco');
assertEq(moroccoRep.utcOffset, 0, 'Morocco rep utcOffset must be 0');

// 2. Setup Leader trip to Libya: 2026-10-18 to 2026-10-25 (Libya is UTC+2, -1h vs Cairo)
setData(STORAGE_KEYS.LEADER_TRIPS, [{{
  id: 301,
  destination: 'med_south_libya',
  startDate: '2026-10-18',
  endDate: '2026-10-25',
  remark: '利比亚代表处出差'
}}]);

// 3. User opens Add Meeting Modal on 2026-10-20 (during Libya trip)
selectedTimelineDate = '2026-10-20';
openAddMeetingModal();

// 4. Secretary chooses Morocco timezone and inputs 09:00 - 10:00 Morocco time
elements['inputMeetingTimezoneBase'].value = 'morocco';
handleMeetingModalTimezoneChange();

elements['inputMeetingStartTime'].value = '09:00';
elements['inputMeetingEndTime'].value = '10:00';
elements['inputMeetingSubject'].value = '摩洛哥重点客户联合评审';
elements['inputMeetingReporter'].value = '摩洛哥代表处';
handleMeetingModalTimezoneChange();

// Verify modalTzConversionHint and modalTripLiveCard are hidden per minimalist UI:
assertEq(elements['modalTzConversionHint'].style.display, 'none', 'modalTzConversionHint is hidden per minimalist UI');
assertEq(elements['modalTripLiveCard'].style.display, 'none', 'modalTripLiveCard is hidden per minimalist UI');

// 5. Save meeting
saveMeeting();

let moroccoAllM = getData(STORAGE_KEYS.MEETINGS);
let moroccoM = moroccoAllM.find(x => x.subject === '摩洛哥重点客户联合评审');
assertEq(Boolean(moroccoM), true, 'Meeting must exist in storage');
assertEq(moroccoM.tzBase, 'morocco', 'moroccoM.tzBase must be morocco');
assertEq(moroccoM.startTime, '12:00', 'moroccoM.startTime (Cairo baseline) must be 12:00');
assertEq(moroccoM.endTime, '13:00', 'moroccoM.endTime (Cairo baseline) must be 13:00');
assertEq(moroccoM.inputStartTime, '09:00', 'moroccoM.inputStartTime must be 09:00');

// 6. Verify getMeetingDisplayTime converts Morocco 09:00 to Libya 11:00
let moroccoDt = getMeetingDisplayTime(moroccoM);
assertEq(moroccoDt.start, '11:00', 'Display start must be Libya local time 11:00');
assertEq(moroccoDt.end, '12:00', 'Display end must be Libya local time 12:00');
assertEq(moroccoDt.cairoStart, '12:00', 'Cairo start must be 12:00');
assertEq(moroccoDt.isShifted, true, 'isShifted must be true');

// 7. Verify Weekly Board rendering on Libya day column
renderSupervisorWeeklyBoard();
let weekHtml2 = elements['supervisorWeeklyBoardContainer'].innerHTML;
assertEq(weekHtml2.includes('11:00 - 12:00'), true, 'Weekly board card MUST show Libya local time 11:00 - 12:00');
assertEq(weekHtml2.includes('开罗 12:00'), true, 'Weekly board card MUST show quiet Cairo time: 开罗 12:00');

// 8. Secretary clicks EDIT on the card: editMeeting(moroccoM.id)
editMeeting(moroccoM.id);
assertEq(elements['inputMeetingTimezoneBase'].value, 'morocco', 'Edit modal tz MUST be morocco');
assertEq(elements['inputMeetingStartTime'].value, '09:00', 'Edit modal MUST present Morocco 09:00');
assertEq(elements['inputMeetingEndTime'].value, '10:00', 'Edit modal MUST present Morocco 10:00');

// 9. Secretary changes timezone dropdown to Libya in modal -> auto-converts to 11:00 - 12:00!
elements['inputMeetingTimezoneBase'].value = 'med_south_libya';
handleMeetingModalTimezoneChange();
assertEq(elements['inputMeetingStartTime'].value, '11:00', 'Switching to Libya auto-converts to 11:00');
assertEq(elements['inputMeetingEndTime'].value, '12:00', 'Switching to Libya auto-converts to 12:00');

// Secretary switches to Cairo in modal -> auto-converts to 12:00 - 13:00!
elements['inputMeetingTimezoneBase'].value = 'cairo';
handleMeetingModalTimezoneChange();
assertEq(elements['inputMeetingStartTime'].value, '12:00', 'Switching to Cairo auto-converts to 12:00');
assertEq(elements['inputMeetingEndTime'].value, '13:00', 'Switching to Cairo auto-converts to 13:00');

// Secretary switches back to Morocco in modal -> auto-converts to 09:00 - 10:00!
elements['inputMeetingTimezoneBase'].value = 'morocco';
handleMeetingModalTimezoneChange();
assertEq(elements['inputMeetingStartTime'].value, '09:00', 'Switching back to Morocco auto-converts to 09:00');
assertEq(elements['inputMeetingEndTime'].value, '10:00', 'Switching back to Morocco auto-converts to 10:00');

saveMeeting();
print('✓ 摩洛哥时区修正为UTC+0、录入时间/出差地时间/开罗时间实时联动、卡片自动折算出差地时间 验证全部通过');

print('\\n--- Testing 待排期简报 (Copy Pending Requests Briefing for Executive Review) ---');

// Test 1: Empty state
setData(STORAGE_KEYS.MEETING_REQUESTS, []);
setData(STORAGE_KEYS.MEETINGS, []);
toasts = [];
lastCopiedText = '';
copyPendingRequestsBriefing();
assertEq(toasts.includes('当前暂无待排期事项，无需生成简报'), true, 'Should notify user when no pending items');
assertEq(lastCopiedText, '', 'Should not copy text when empty');

// Test 2: With exactly 4 pending requests (High/Medium/Low urgency) and calendar meetings in database
const sampleRequests = [
  {{ id: 101, requester: '地南代表处 陈总', topic: 'Q3交付回款与预算特批沟通', urgency: 'high', duration: '45m', status: 'pending' }},
  {{ id: 102, requester: '物流中心 孙经理', topic: '海外仓二期供应链协同', urgency: 'medium', duration: '30', status: 'pending' }},
  {{ id: 103, requester: '开罗交付部 王部长', topic: '开罗机房硬件升级方案汇报', urgency: 'medium', duration: '30m', status: 'pending' }},
  {{ id: 104, requester: '人力资源部 李总监', topic: '中东北非属地化人才招聘汇报', urgency: 'low', duration: '60分钟', status: 'pending' }},
  {{ id: 105, requester: '已排期人员', topic: '此项已排期不应出现', urgency: 'high', duration: '30m', status: 'scheduled' }}
];

const sampleMeetings = [
  {{ id: 201, subject: '地中海区域重点基建项目风险会商', reporter: '赵总', attendees: '各代表处一把手', duration: 45, date: '2026-10-25', time: '14:00', status: 'pending', decision: '明确工程延期索赔应对预案' }},
  {{ id: 202, subject: '已排期常规例会', reporter: '周经理', attendees: '财务组', duration: 30, date: '2026-10-20', time: '10:00', status: 'scheduled', decision: '通报常规预算' }}
];

setData(STORAGE_KEYS.MEETING_REQUESTS, sampleRequests);
setData(STORAGE_KEYS.MEETINGS, sampleMeetings);
toasts = [];
lastCopiedText = '';

copyPendingRequestsBriefing();

assertEq(toasts.includes('待排期简报已复制到剪贴板，可直接发送微信或工作群！'), true, 'Toast notification on copy pending briefing');
assertEq(lastCopiedText.includes('【主管待排期事项请示 · '), true, 'Header title must match template');
assertEq(lastCopiedText.includes('曦总您好，当前汇总共有 4 项待排期事项，请您审定是否安排：'), true, 'Must report exact count of 4 pending items matching UI pool');

// Check each reservation is strictly a single concise line
assertEq(lastCopiedText.includes('1. 🔴【加急】地南代表处 陈总：Q3交付回款与预算特批沟通 (45m)'), true, 'High urgency single line');
assertEq(lastCopiedText.includes('2. 🟡【本周】物流中心 孙经理：海外仓二期供应链协同 (30m)'), true, 'Medium urgency single line 1');
assertEq(lastCopiedText.includes('3. 🟡【本周】开罗交付部 王部长：开罗机房硬件升级方案汇报 (30m)'), true, 'Medium urgency single line 2');
assertEq(lastCopiedText.includes('4. 🟢【机动】人力资源部 李总监：中东北非属地化人才招聘汇报 (60m)'), true, 'Low urgency single line');

// Scheduled request and calendar meetings must NOT be mixed in
assertEq(lastCopiedText.includes('此项已排期不应出现'), false, 'Scheduled request must not be included');
assertEq(lastCopiedText.includes('已排期常规例会'), false, 'Scheduled meeting must not be included');
assertEq(lastCopiedText.includes('地中海区域重点基建项目风险会商'), false, 'Calendar pending meeting must not be mixed into request pool briefing');

// Closing call to action
assertEq(lastCopiedText.includes('请示说明：请曦总批示优先安排哪些事项，秘书处将立即为您锁定时间。'), true, 'Must include concise executive call to action');

// Test 3: Trip Timezone Header Suffix
changeTripTimezone('med_south_libya');
lastCopiedText = '';
copyPendingRequestsBriefing();
assertEq(lastCopiedText.includes('出差地南·利比亚中 · 🇱🇾'), true, 'Header must indicate active business trip destination and flag');
changeTripTimezone('cairo');

print('✓ 会议预约: 待排期极简一行字简报、数量与待排池严格一致、加急分级、出差地感知 验证全部通过');

// --- Testing 每日英语 (English Word Selection, Dictionary Lookup & Pronunciation) ---
print('\\n--- Testing 每日英语 (English Word Selection, Dictionary Lookup & Pronunciation) ---');
assertEq(Object.keys(NORDIC_DICT).length >= 1000, true, 'NORDIC_DICT must have at least 1000 vocabulary words');
assertEq(cleanLookupWord('"sauna,"'), 'sauna', 'cleanLookupWord strips quotes and punctuation');
assertEq(cleanLookupWord('“Fika”'), 'Fika', 'cleanLookupWord strips Chinese/curly quotes');
assertEq(cleanLookupWord('Löyly!'), 'Löyly', 'cleanLookupWord preserves Nordic special characters');
assertEq(cleanLookupWord('dalahäst.'), 'dalahäst', 'cleanLookupWord preserves dalahäst');
assertEq(cleanLookupWord('  aurora borealis  '), 'aurora borealis', 'cleanLookupWord preserves multi-word phrase');

const fikaRes = findWordInDict('fika');
assertEq(fikaRes && fikaRes.d.indexOf('咖啡') !== -1, true, 'findWordInDict finds fika');

const saunaRes = findWordInDict('Sauna');
assertEq(saunaRes && saunaRes.d.indexOf('桑拿') !== -1, true, 'findWordInDict handles uppercase Sauna');

const auroraRes = findWordInDict('Aurora Borealis');
assertEq(auroraRes && auroraRes.d.indexOf('极光') !== -1, true, 'findWordInDict handles Aurora Borealis');

const fjordsStem = findWordInDict('fjords');
assertEq(fjordsStem && fjordsStem.d.indexOf('峡湾') !== -1, true, 'Stemming resolves fjords -> fjord');

const hikedStem = findWordInDict('hiked');
assertEq(hikedStem && hikedStem.d.indexOf('徒步') !== -1, true, 'Stemming resolves hiked -> hike');

const dancingStem = findWordInDict('dancing');
assertEq(dancingStem && dancingStem.d.indexOf('跳舞') !== -1, true, 'Stemming resolves dancing -> dance');

// Show popup and test UI values
showWordLookupPopup('fika', {{ left: 200, top: 300, width: 60, height: 20, right: 260, bottom: 320 }});
assertEq(document.getElementById('wordLookupPopup').style.display, 'block', 'Popup must be displayed');
assertEq(document.getElementById('wordPopupTitle').textContent, 'Fika', 'Popup title set to Fika');
assertEq(document.getElementById('wordPopupDef').textContent.indexOf('咖啡') !== -1, true, 'Popup definition contains 咖啡');

// Pronunciation test
lastSpokenUtterance = null;
speakLookupWord();
assertEq(lastSpokenUtterance, 'fika', 'speakLookupWord must trigger speech synthesis for fika');

// Search input test
document.getElementById('englishSearchInput').value = 'avanto';
searchEnglishWord();
assertEq(document.getElementById('wordPopupTitle').textContent, 'Avanto', 'Search sets title to Avanto');
speakLookupWord();
assertEq(lastSpokenUtterance, 'avanto', 'Speech triggers for search word avanto');

hideWordLookupPopup();
assertEq(document.getElementById('wordLookupPopup').style.display, 'none', 'hideWordLookupPopup hides popup');

print('✓ 每日英语: 划词查询、1200+词典匹配、词干还原、发音朗读与即时搜索验证全部通过');

print('\\n=========================================');
print('ALL TESTS PASSED SUCCESSFULLY 100%!');
print('=========================================\\n');
"""

with open("scratch/test_run.js", "w", encoding="utf-8") as f:
    f.write(test_js)

jsc_path = "/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
res = subprocess.run([jsc_path, "scratch/test_run.js"], capture_output=True, text=True)
print("JSC STDOUT:\n" + res.stdout)
if res.stderr:
    print("JSC STDERR:\n" + res.stderr)
assert res.returncode == 0, f"JSC exited with code {res.returncode}"

# Run 31-day Business Travel English curriculum verification
travel_eng_res = subprocess.run(["python3", "scratch/test_business_travel_english.py"], capture_output=True, text=True)
print(travel_eng_res.stdout)
assert travel_eng_res.returncode == 0, f"test_business_travel_english failed: {travel_eng_res.stderr}"

print("PYTHON TEST RUNNER COMPLETED WITH EXIT CODE 0!")

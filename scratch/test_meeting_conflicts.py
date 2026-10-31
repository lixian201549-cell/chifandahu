import subprocess
import os

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("--- 1. Testing HTML & CSS Static Assertions for Meeting Conflict Overlap Display ---")
# Check CSS classes
assert '.weekly-card.is-conflict' in html, "Missing .weekly-card.is-conflict in CSS"
assert '.weekly-card-conflict' in html, "Missing .weekly-card-conflict in CSS"
assert '.conflict-overlap-time' in html, "Missing .conflict-overlap-time in CSS"
assert '.weekly-conflict-header-badge' in html, "Missing .weekly-conflict-header-badge in CSS"
assert '.day-meeting-card.is-conflict' in html, "Missing .day-meeting-card.is-conflict in CSS"
assert '.day-meeting-conflict-box' in html, "Missing .day-meeting-conflict-box in CSS"
assert '.day-conflict-time-pill' in html, "Missing .day-conflict-time-pill in CSS"
assert '.cal-event-pill.cal-event-conflict' in html, "Missing .cal-event-pill.cal-event-conflict in CSS"
assert '.cal-conflict-overlap-tag' in html, "Missing .cal-conflict-overlap-tag in CSS"
assert '.meeting-card-conflict-notice' in html, "Missing .meeting-card-conflict-notice in CSS"

print("✓ All CSS conflict classes verified in index.html!")

# Extract JS code
script_start = html.find('<script>') + len('<script>')
script_end = html.rfind('</script>')
js_code = html[script_start:script_end]

jsc_header = """
const console = { log: print, error: print, warn: print };
const setTimeout = (fn) => 0;
const clearTimeout = () => {};
const setInterval = (fn) => 0;
const clearInterval = () => {};
const window = {
  scrollTo: () => {},
  addEventListener: () => {},
  removeEventListener: () => {},
  location: { search: '' },
  navigator: { clipboard: { writeText: () => Promise.resolve() } },
  innerWidth: 1200, innerHeight: 800, scrollX: 0, scrollY: 0
};
function SpeechSynthesisUtterance(text) { this.text = text; }
const speechSynthesis = { speak: () => {}, cancel: () => {} };
const localStorage = {
  _store: {},
  getItem: function(k) { return this._store[k] || null; },
  setItem: function(k, v) { this._store[k] = String(v); },
  removeItem: function(k) { delete this._store[k]; },
  clear: function() { this._store = {}; }
};
const elements = {};
const document = {
  getElementById: (id) => {
    if (!elements[id]) {
      elements[id] = {
        id, value: '', textContent: '', innerHTML: '', style: {},
        classList: {
          _cls: new Set(),
          add: function(c) { this._cls.add(c); },
          remove: function(c) { this._cls.delete(c); },
          contains: function(c) { return this._cls.has(c); },
          toggle: function(c, v) { if (v) this._cls.add(c); else this._cls.delete(c); }
        },
        focus: () => {}, querySelectorAll: () => [], appendChild: () => {}
      };
    }
    return elements[id];
  },
  querySelectorAll: () => [], addEventListener: () => {},
  createElement: (tag) => ({
    tagName: tag, style: { setProperty: () => {} },
    classList: { _cls: new Set(), add: function(c) { this._cls.add(c); }, remove: function(c) { this._cls.delete(c); }, contains: function(c) { return this._cls.has(c); } },
    appendChild: () => {}, remove: () => {}
  })
};
function alert(m) { print('[ALERT] ' + m); }
function confirm(m) { print('[CONFIRM] ' + m); return true; }
function prompt(m, d) { return d; }
function assertEq(act, exp, msg) {
  if (act !== exp) {
    throw new Error('FAIL: ' + msg + ' | Expected [' + exp + '], got [' + act + ']');
  }
  print('  ✓ ' + msg);
}
"""

test_js = """
print("--- 2. Testing Meeting Conflict & Overlapping Time in JSC ---");

const testDate = getTodayDateStr();
selectedTimelineDate = testDate;

// Setup test meetings with intentional overlaps on 2026-10-25:
// Meeting 1: 10:00 - 11:00 (60m)
// Meeting 2: 10:30 - 11:30 (60m) -> Overlaps with M1 from 10:30 to 11:00 (30m)
// Meeting 3: 11:15 - 12:00 (45m) -> Overlaps with M2 from 11:15 to 11:30 (15m)
// Meeting 4: 14:00 - 15:00 (60m) -> No overlap with anything
// Meeting 5: 15:00 - 16:00 (60m) -> Back to back with M4, NO overlap!
const sampleMeetings = [
  { id: 801, date: testDate, startTime: '10:00', endTime: '11:00', time: '10:00', duration: 60, subject: '季度预算审议会', reporter: '张财务', status: 'scheduled' },
  { id: 802, date: testDate, startTime: '10:30', endTime: '11:30', time: '10:30', duration: 60, subject: '重点交付项目协调', reporter: '李项目', status: 'scheduled' },
  { id: 803, date: testDate, startTime: '11:15', endTime: '12:00', time: '11:15', duration: 45, subject: '突尼斯代表处周会', reporter: '王突尼斯', status: 'scheduled' },
  { id: 804, date: testDate, startTime: '14:00', endTime: '15:00', time: '14:00', duration: 60, subject: '新员工座谈', reporter: '赵人力', status: 'scheduled' },
  { id: 805, date: testDate, startTime: '15:00', endTime: '16:00', time: '15:00', duration: 60, subject: '安全例会', reporter: '钱安全', status: 'scheduled' },
];

setData(STORAGE_KEYS.MEETINGS, sampleMeetings);

// A. Test getMeetingConflictDetails
const m1Conflicts = getMeetingConflictDetails(sampleMeetings[0], sampleMeetings);
assertEq(m1Conflicts.length, 1, 'Meeting 801 has exactly 1 conflict (with Meeting 802)');
assertEq(m1Conflicts[0].conflictId, 802, 'Meeting 801 conflicts with ID 802');
assertEq(m1Conflicts[0].overlapRangeStr, '10:30 - 11:00', 'Meeting 801 overlap range is exactly 10:30 - 11:00');
assertEq(m1Conflicts[0].overlapDuration, 30, 'Meeting 801 overlap duration is exactly 30 minutes');

const m2Conflicts = getMeetingConflictDetails(sampleMeetings[1], sampleMeetings);
assertEq(m2Conflicts.length, 2, 'Meeting 802 has 2 conflicts (with 801 and 803)');
assertEq(m2Conflicts[0].overlapRangeStr, '10:30 - 11:00', 'M2 first overlap range is 10:30 - 11:00');
assertEq(m2Conflicts[0].overlapDuration, 30, 'M2 first overlap is 30 mins');
assertEq(m2Conflicts[1].overlapRangeStr, '11:15 - 11:30', 'M2 second overlap range is 11:15 - 11:30');
assertEq(m2Conflicts[1].overlapDuration, 15, 'M2 second overlap is 15 mins');

const m4Conflicts = getMeetingConflictDetails(sampleMeetings[3], sampleMeetings);
assertEq(m4Conflicts.length, 0, 'Meeting 804 (14:00-15:00) has NO conflicts (back-to-back with 15:00-16:00 is safe)');

const m5Conflicts = getMeetingConflictDetails(sampleMeetings[4], sampleMeetings);
assertEq(m5Conflicts.length, 0, 'Meeting 805 (15:00-16:00) has NO conflicts');

// B. Test Weekly Board Rendering with Conflict Display
currentWeekOffset = 0;
renderSupervisorWeeklyBoard();
const weekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;

assertEq(weekHtml.indexOf('weekly-conflict-header-badge" style="display:none;"') !== -1, true, 'Weekly column header conflict badge is hidden from view per user request');
assertEq(weekHtml.indexOf('is-conflict') !== -1, true, 'Weekly card has is-conflict class');
assertEq(weekHtml.indexOf('weekly-card-conflict') !== -1, true, 'Weekly card contains .weekly-card-conflict block');
assertEq(weekHtml.indexOf('10:30 - 11:00') !== -1, true, 'Weekly card explicitly shows overlapping time range 10:30 - 11:00');
assertEq(weekHtml.indexOf('重合') !== -1, true, 'Weekly card explicitly shows 重合');
assertEq(weekHtml.indexOf('conflict-overlap-dur') === -1, true, 'Weekly card does NOT show redundant duration (90min/30m) per user request');

// C. Test Day Calendar Rendering with Conflict Display
renderSupervisorDayCalendar();
const dayHtml = elements['supervisorDayCalendarContainer'].innerHTML;

assertEq(dayHtml.indexOf('day-meeting-conflict-box') !== -1, true, 'Day calendar contains .day-meeting-conflict-box');
assertEq(dayHtml.indexOf('🕒 重合：<strong>10:30 - 11:00</strong>') !== -1, true, 'Day calendar explicitly displays highlighted overlap time 10:30 - 11:00');
assertEq(dayHtml.indexOf('重叠时长') === -1, true, 'Day calendar does NOT show redundant 重叠时长 per user request');
assertEq(dayHtml.indexOf('style="display:none;" title="本日存在会议时间冲突"') !== -1, true, 'Day top header conflict badge is hidden from view per user request');

// D. Test Month Calendar Rendering with Conflict Display
currentCalendarYearMonth = { year: 2026, month: 9 }; // Oct 2026 (0-indexed 9)
renderSupervisorMonthCalendar();
const monthHtml = elements['supervisorMonthCalendarContainer'].innerHTML;

assertEq(monthHtml.indexOf('cal-day-conflict-icon') !== -1, true, 'Month calendar day header displays ⚠️ conflict icon');
assertEq(monthHtml.indexOf('cal-event-conflict') !== -1, true, 'Month calendar event pill has cal-event-conflict class');
assertEq(monthHtml.indexOf('重合 10:30 - 11:00') !== -1, true, 'Month calendar event pill shows [重合 10:30 - 11:00]');

// E. Test Card List View Rendering with Conflict Display
supervisorViewMode = 'card_list';
renderMeetings();
const cardListHtml = elements['meetingCardsList'].innerHTML;

assertEq(cardListHtml.indexOf('meeting-card-conflict-notice') !== -1, true, 'Cards list displays .meeting-card-conflict-notice');
assertEq(cardListHtml.indexOf('10:30 - 11:00') !== -1, true, 'Cards list explicitly displays overlapping time 10:30 - 11:00');
assertEq(cardListHtml.indexOf('重叠 30 分钟') !== -1, true, 'Cards list explicitly displays 30 mins overlap');

// F. Test Modal Live Conflict Checking
document.getElementById('inputMeetingDate').value = testDate;
document.getElementById('inputMeetingStartTime').value = '10:15';
document.getElementById('inputMeetingEndTime').value = '10:45';
document.getElementById('inputMeetingId').value = '';
checkMeetingConflicts();
const modalAlertHtml = elements['meetingConflictAlert'].innerHTML;

assertEq(elements['meetingConflictAlert'].style.display, 'block', 'Modal conflict alert is visible');
assertEq(modalAlertHtml.indexOf('💥 重合时间') !== -1, true, 'Modal conflict alert highlights 💥 重合时间');
assertEq(modalAlertHtml.indexOf('10:30 - 10:45') !== -1, true, 'Modal detects overlap with 10:30-11:30 is 10:30 - 10:45');
assertEq(modalAlertHtml.indexOf('15 分钟') !== -1, true, 'Modal displays overlap duration 15分钟');

print('✓ ALL meeting conflict & overlapping time display tests passed 100%!');
"""

full_test_js = jsc_header + "\n" + js_code + "\n" + test_js
with open("scratch/test_meeting_conflicts_runner.js", "w", encoding="utf-8") as f:
    f.write(full_test_js)

jsc_path = "/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
res = subprocess.run([jsc_path, "scratch/test_meeting_conflicts_runner.js"], capture_output=True, text=True)
print("JSC STDOUT:\n" + res.stdout)
if res.stderr:
    print("JSC STDERR:\n" + res.stderr)
assert res.returncode == 0, f"JSC exited with code {res.returncode}"
print("ALL MEETING CONFLICT TESTS PASSED SUCCESSFULLY 100%!")

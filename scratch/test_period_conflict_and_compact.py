import subprocess
import os

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("--- 1. Testing CSS & HTML Static Assertions for Period Conflict & Compact Card ---")
# 1. Check CSS for compactness and non-wrapping
assert '.weekly-card-time-text' in html, "Missing .weekly-card-time-text in CSS"
assert 'white-space: nowrap !important' in html, "Missing white-space: nowrap !important for card time"
assert 'padding: 3px 5px' in html, "Missing compact padding: 3px 5px in .weekly-card CSS"
assert '.weekly-card-time-badges' in html, "Missing .weekly-card-time-badges"
assert '-webkit-line-clamp: 2' in html, "Missing line-clamp for weekly-card-title"
assert 'text-overflow: ellipsis' in html, "Missing text-overflow: ellipsis for compact decision snippet"

print("✓ CSS compactness and nowrap rules successfully verified in index.html!")

# 2. Extract JavaScript
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
print("--- 2. Testing Period-Specific Conflict Display (上午无冲突不标红，仅下午标红) ---");

const testDate = getTodayDateStr();
selectedTimelineDate = testDate;

// Setup User Scenario:
// Meeting 901: 09:00 - 19:00 (All-day meeting spanning morning and afternoon)
// Meeting 902: 16:00 - 18:00 (Afternoon conflict with Meeting 901)
const testMeetings = [
  {
    id: 901,
    date: testDate,
    startTime: '09:00',
    endTime: '19:00',
    time: '09:00',
    duration: 600,
    subject: '全天战略发展与经营分析闭门会',
    reporter: '赵战略',
    status: 'scheduled',
    decision: '原则同意下季度经营目标，深化全区资源联动并优化业务流'
  },
  {
    id: 902,
    date: testDate,
    startTime: '16:00',
    endTime: '18:00',
    time: '16:00',
    duration: 120,
    subject: '西非油气项目紧急协调会',
    reporter: '钱商务',
    status: 'scheduled'
  }
];

setData(STORAGE_KEYS.MEETINGS, testMeetings);

// A. Test Weekly Board Rendering
currentWeekOffset = 0;
renderSupervisorWeeklyBoard();
const weekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;

// Extract Morning Block and Afternoon Block for testDate
const morningDividerIdx = weekHtml.indexOf('class="weekly-period-block morning-block"');
const afternoonDividerIdx = weekHtml.indexOf('class="weekly-period-block afternoon-block"');
assertEq(morningDividerIdx !== -1, true, 'Weekly board has morning block');
assertEq(afternoonDividerIdx !== -1, true, 'Weekly board has afternoon block');

const morningSub = weekHtml.substring(morningDividerIdx, afternoonDividerIdx);
const afternoonSub = weekHtml.substring(afternoonDividerIdx);

// In morning block:
// 1. Meeting 901 is displayed
assertEq(morningSub.indexOf('全天战略发展与经营分析闭门会') !== -1, true, 'Morning block contains Meeting 901');
// 2. Morning block MUST NOT have is-conflict styling!
assertEq(morningSub.indexOf('is-conflict') === -1, true, 'Morning block card is NOT marked as conflicted (is-conflict absent)');
// 3. Morning block MUST NOT show .weekly-card-conflict warning pill
assertEq(morningSub.indexOf('weekly-card-conflict') === -1, true, 'Morning block does NOT display weekly-card-conflict pill');

// In afternoon block:
// 1. Meeting 901 is displayed
assertEq(afternoonSub.indexOf('全天战略发展与经营分析闭门会') !== -1, true, 'Afternoon block contains Meeting 901');
// 2. Afternoon block MUST have is-conflict styling!
assertEq(afternoonSub.indexOf('is-conflict') !== -1, true, 'Afternoon block card is correctly marked as conflicted (is-conflict present)');
// 3. Afternoon block MUST show .weekly-card-conflict warning pill with 16:00 - 18:00
assertEq(afternoonSub.indexOf('weekly-card-conflict') !== -1, true, 'Afternoon block displays weekly-card-conflict pill');
assertEq(afternoonSub.indexOf('16:00 - 18:00') !== -1, true, 'Afternoon block displays exact overlap time 16:00 - 18:00');

// B. Test Day Calendar Rendering
renderSupervisorDayCalendar();
const dayHtml = elements['supervisorDayCalendarContainer'].innerHTML;

const dayMornIdx = dayHtml.indexOf('上午日程推进');
const dayAftIdx = dayHtml.indexOf('下午日程推进');
const dayMornSub = dayHtml.substring(dayMornIdx, dayAftIdx);
const dayAftSub = dayHtml.substring(dayAftIdx);

// Day morning:
assertEq(dayMornSub.indexOf('全天战略发展与经营分析闭门会') !== -1, true, 'Day morning contains Meeting 901');
assertEq(dayMornSub.indexOf('day-meeting-card is-conflict') === -1, true, 'Day morning card is NOT marked as is-conflict');
assertEq(dayMornSub.indexOf('day-meeting-conflict-box') === -1, true, 'Day morning does NOT show conflict alert box');

// Day afternoon:
assertEq(dayAftSub.indexOf('全天战略发展与经营分析闭门会') !== -1, true, 'Day afternoon contains Meeting 901');
assertEq(dayAftSub.indexOf('is-conflict') !== -1, true, 'Day afternoon card IS marked as is-conflict');
assertEq(dayAftSub.indexOf('day-meeting-conflict-box') !== -1, true, 'Day afternoon shows conflict alert box with 16:00 - 18:00');
assertEq(dayAftSub.indexOf('16:00 - 18:00') !== -1, true, 'Day afternoon shows exact overlap 16:00 - 18:00');

// C. Test Time Display Format on Card (保持时间在一行，9:00-19:00)
assertEq(morningSub.indexOf('weekly-card-time-text') !== -1, true, 'Card time has dedicated weekly-card-time-text container');
assertEq(morningSub.indexOf('09:00 - 19:00') !== -1 || morningSub.indexOf('09:00-19:00') !== -1 || morningSub.indexOf('9:00 - 19:00') !== -1, true, 'Card time formatted within nowrap container');

print('✓ ALL PERIOD-AWARE CONFLICT & COMPACT CARD TESTS PASSED 100%!');
"""

full_test_js = jsc_header + "\n" + js_code + "\n" + test_js
with open("scratch/test_period_conflict_runner.js", "w", encoding="utf-8") as f:
    f.write(full_test_js)

jsc_path = "/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
res = subprocess.run([jsc_path, "scratch/test_period_conflict_runner.js"], capture_output=True, text=True)
print("JSC STDOUT:\n" + res.stdout)
if res.stderr:
    print("JSC STDERR:\n" + res.stderr)
assert res.returncode == 0, f"JSC exited with code {res.returncode}"
print("=== ALL TEST ASSERTIONS PASSED WITH ZERO ERRORS! ===")

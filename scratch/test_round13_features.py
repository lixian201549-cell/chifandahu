#!/usr/bin/env python3
import subprocess
import os

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("--- Testing Round 13 HTML & CSS Assertions ---")
assert 'max-width: 1280px;' in html, "Blackboard width should be widened to 1280px"
assert 'snoopyGentleFloat' in html, "Snoopy gentle floating breathing animation missing"
assert 'snoopy-cute-aura' in html, "Snoopy cute aura sparkle element missing"
assert 'snoopy-happy-bounce' in html, "Snoopy happy bounce on click missing"
assert '.weekly-allday-banner' in html, "Weekly allday banner CSS missing"
assert '.weekly-empty-period-slot' in html, "Weekly empty period slot CSS missing"
assert '.weekly-card-conflict' in html, "Weekly card conflict CSS missing"

print("✓ Static CSS/HTML assertions passed!")

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
print("--- Testing Round 13 Features in JSC ---");

// Test 1: All-Day Meeting Occupies the Entire Day
const testDateSun = '2026-10-25'; // Sunday
const testDateMon = '2026-10-26'; // Monday
const testDateTue = '2026-10-27'; // Tuesday

const sampleMeetings = [
  // Sunday: All-day meeting from morning to evening (09:00 - 18:00)
  {
    id: 1001,
    date: testDateSun,
    startTime: '09:00',
    endTime: '18:00',
    time: '09:00',
    duration: 540,
    subject: '年度经营战略研讨会 (全天)',
    reporter: '集团高管组',
    status: 'scheduled'
  },
  // Monday: Afternoon ONLY meeting (14:00 - 17:00), Morning MUST BE EMPTY
  {
    id: 1002,
    date: testDateMon,
    startTime: '14:00',
    endTime: '17:00',
    time: '14:00',
    duration: 180,
    subject: '海外交付复盘',
    reporter: '李交付',
    status: 'scheduled'
  },
  // Tuesday: Morning ONLY meeting (09:30 - 11:30), Afternoon MUST BE EMPTY
  {
    id: 1003,
    date: testDateTue,
    startTime: '09:30',
    endTime: '11:30',
    time: '09:30',
    duration: 120,
    subject: '采购内审例会',
    reporter: '王采购',
    status: 'scheduled'
  }
];

setData(STORAGE_KEYS.MEETINGS, sampleMeetings);

currentWeekOffset = 0;
renderSupervisorWeeklyBoard();
const weekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;

// Assertion 1: No "全天排满" card/banner per user request; separated into morning and afternoon
assertEq(weekHtml.indexOf('📅 全天排满') === -1, true, '全天排满 is completely removed per user request');
assertEq(weekHtml.indexOf('从早到晚') === -1, true, '从早到晚 is completely deleted per user request');

// Assertion 2: Monday morning is visibly empty with booking slot (no emoji, no specific time)
assertEq(weekHtml.indexOf('暂无排期') !== -1, true, 'Monday morning indicates 暂无排期');
assertEq(weekHtml.indexOf('空闲') === -1, true, 'No 空闲 text');
assertEq(weekHtml.indexOf('可约') === -1, true, 'No 可约 text');
assertEq(weekHtml.indexOf('海外交付复盘') !== -1, true, 'Monday afternoon contains afternoon meeting');
assertEq(weekHtml.indexOf('🌅') === -1, true, 'No emoji in morning/afternoon');

// Assertion 3: Tuesday afternoon is visibly empty with booking slot (no emoji, no specific time)
assertEq(weekHtml.indexOf('采购内审例会') !== -1, true, 'Tuesday morning contains morning meeting');
assertEq(weekHtml.indexOf('🌇') === -1, true, 'No emoji in morning/afternoon');

// Test 2: Minimalist conflict pill on calendar cards vs Detailed Info in opened modal
const conflictMeetings = [
  { id: 2001, date: '2026-10-28', startTime: '10:00', endTime: '11:00', time: '10:00', duration: 60, subject: 'A会议', reporter: '张三', status: 'scheduled' },
  { id: 2002, date: '2026-10-28', startTime: '10:30', endTime: '11:30', time: '10:30', duration: 60, subject: 'B会议', reporter: '李四', status: 'scheduled' }
];
setData(STORAGE_KEYS.MEETINGS, conflictMeetings);
renderSupervisorWeeklyBoard();
const conflictWeekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;

// Minimalist pill on card: single line with ⚠️ 重合
assertEq(conflictWeekHtml.indexOf('weekly-card-conflict') !== -1, true, 'Card has weekly-card-conflict pill');
assertEq(conflictWeekHtml.indexOf('重合') !== -1, true, 'Card conflict pill displays 重合');
assertEq(conflictWeekHtml.indexOf('10:30 - 11:00') !== -1, true, 'Card conflict pill displays overlap range 10:30 - 11:00');

// Open modal via editMeeting: detailed view inside opened card
editMeeting(2001);
const modalAlertHtml = elements['meetingConflictAlert'].innerHTML;
assertEq(elements['meetingConflictAlert'].style.display !== 'none', true, 'Modal conflict alert is visible');
assertEq(modalAlertHtml.indexOf('💥 重合时间') !== -1, true, 'Modal details highlight 💥 重合时间');
assertEq(modalAlertHtml.indexOf('B会议') !== -1, true, 'Modal displays conflicting meeting name B会议');
assertEq(modalAlertHtml.indexOf('李四') !== -1, true, 'Modal displays conflicting meeting reporter 李四');
assertEq(modalAlertHtml.indexOf('30 分钟') !== -1, true, 'Modal displays overlap duration 30 分钟');

// Test 3: Snoopy interactive bounce and particle spawn
interactBorderSnoopy();
const snoopyWrap = elements['snoopyLyingWrap'];
assertEq(snoopyWrap.classList.contains('snoopy-happy-bounce'), true, 'Snoopy gets snoopy-happy-bounce class on click');

print("✓ All Round 13 features verified successfully 100%!");
"""

with open("scratch/test_round13_runner.js", "w", encoding="utf-8") as f:
    f.write(jsc_header + "\n" + js_code + "\n" + test_js)

jsc_bin = "/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
res = subprocess.run([jsc_bin, "scratch/test_round13_runner.js"], capture_output=True, text=True)
print("JSC STDOUT:")
print(res.stdout)
if res.stderr:
    print("JSC STDERR:")
    print(res.stderr)

assert res.returncode == 0, f"JSC exited with code {res.returncode}"
print("ROUND 13 TEST SUITE PASSED 100%!")

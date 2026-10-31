#!/usr/bin/env python3
import subprocess

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("--- Testing Round 15 HTML & CSS Assertions ---")
# 1. Check Snoopy avatars enlarged by 1.5x
assert 'width: 78px;' in html, "module-banner-avatar width should be 78px"
assert 'height: 84px;' in html, "module-banner-avatar height should be 84px"
assert 'width: 66px;' in html, "brand-avatar width should be 66px"
assert 'height: 72px;' in html, "brand-avatar height should be 72px"
assert 'width: 32px;' in html, "nav-tab img width should be 32px"
assert 'height: 32px;' in html, "nav-tab img height should be 32px"
assert 'width: 100px;' in html, "snoopy-lying-wrap width should be 100px (shrunk to avoid blocking)"
assert 'height: 120px;' in html, "snoopy-lying-wrap height should be 120px (shrunk to avoid blocking)"

print("✓ All module Snoopys remain enlarged (1.5x) and HOME Snoopy comfortably shrunk (100x120px) verified in CSS!")

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
print("--- Testing Precise Thursday Recognition in JSC ---");

// Sunday 2026-10-25 to Saturday 2026-10-31
// Thursday is 2026-10-29
const thuDate = '2026-10-29';
const sunDate = '2026-10-25';

const meetings = [
  // Sunday: Truly fully booked (09:00 - 18:00)
  {
    id: 901,
    date: sunDate,
    startTime: '09:00',
    endTime: '18:00',
    time: '09:00',
    duration: 540,
    subject: '集团高管年度研讨会',
    status: 'scheduled'
  },
  // Thursday Case A: Afternoon meeting ONLY (14:00 - 18:00). Morning MUST HAVE FREE TIME!
  {
    id: 902,
    date: thuDate,
    startTime: '14:00',
    endTime: '18:00',
    time: '14:00',
    duration: 240,
    subject: '周四下午经营复盘',
    status: 'scheduled'
  }
];

setData(STORAGE_KEYS.MEETINGS, meetings);
currentWeekOffset = 0;
renderSupervisorWeeklyBoard();
let weekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;

// 1. Verify "全天排满" card is completely removed
assertEq(weekHtml.indexOf('📅 全天排满') === -1, true, 'No 全天排满 card/banner per user request');

// 2. Verify Thursday shows separated morning and afternoon without emoji or time range
const thuIdx = weekHtml.indexOf('10月29日');
assertEq(thuIdx !== -1, true, 'Thursday column found in week board');

const nextColIdx = weekHtml.indexOf('10月30日', thuIdx);
const thuColHtml = weekHtml.substring(thuIdx, nextColIdx);

assertEq(thuColHtml.indexOf('📅 全天排满') === -1, true, 'Thursday is NOT 全天排满!');
assertEq(thuColHtml.indexOf('暂无排期') !== -1, true, 'Thursday morning shows 暂无排期');
assertEq(thuColHtml.indexOf('空闲') === -1, true, 'No 空闲 on Thursday morning');
assertEq(thuColHtml.indexOf('可约') === -1, true, 'No 可约 on Thursday morning');
assertEq(thuColHtml.indexOf('🌅') === -1, true, 'No emoji on Thursday morning');
assertEq(thuColHtml.indexOf('周四下午经营复盘') !== -1, true, 'Thursday afternoon shows afternoon meeting');

// Thursday Case B: Meeting 10:00 - 17:00. Morning still has 09:00 - 10:00 free slot!
meetings[1] = {
  id: 902,
  date: thuDate,
  startTime: '10:00',
  endTime: '17:00',
  time: '10:00',
  duration: 420,
  subject: '跨部门协作会',
  status: 'scheduled'
};
setData(STORAGE_KEYS.MEETINGS, meetings);
renderSupervisorWeeklyBoard();
weekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;
const thuColHtml2 = weekHtml.substring(weekHtml.indexOf('10月29日'), weekHtml.indexOf('10月30日'));

assertEq(thuColHtml2.indexOf('📅 全天排满') === -1, true, 'Thursday with 10:00-17:00 is NOT 全天排满!');
assertEq(thuColHtml2.indexOf('09:00 - 10:00') !== -1, true, 'Thursday morning shows 09:00 - 10:00 free slot');

print("✓ Thursday morning free time precision recognition 100% verified!");
"""

with open("scratch/test_round15_runner.js", "w", encoding="utf-8") as f:
    f.write(jsc_header + "\n" + js_code + "\n" + test_js)

jsc_bin = "/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
res = subprocess.run([jsc_bin, "scratch/test_round15_runner.js"], capture_output=True, text=True)
print("JSC STDOUT:")
print(res.stdout)
if res.stderr:
    print("JSC STDERR:")
    print(res.stderr)

assert res.returncode == 0, f"JSC exited with code {res.returncode}"
print("ROUND 15 TEST SUITE PASSED 100%!")

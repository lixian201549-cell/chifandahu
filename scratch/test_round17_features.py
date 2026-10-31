#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os

print("--- Testing Round 17: No '全天排满' Card, Clean Morning/Afternoon Split Without Emojis or Specific Times ---")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Static HTML Assertions
assert '全天排满' not in html, "全天排满 must not appear in HTML"
assert '🌅' not in html, "🌅 emoji must not appear in HTML"
assert '🌇' not in html, "🌇 emoji must not appear in HTML"
assert '09:00 - 12:00' not in html, "Specific time 09:00 - 12:00 must not appear in HTML"
assert '14:00 - 18:00' not in html, "Specific time 14:00 - 18:00 must not appear in HTML"
print("✓ Static assertions passed: No '全天排满', no 🌅/🌇 emojis, no hardcoded time ranges in HTML")

# 2. Functional JS execution via macOS JSC
script_start = html.find('<script>') + len('<script>')
script_end = html.rfind('</script>')
js_code = html[script_start:script_end]

jsc_code = f"""
const console = {{ log: (s) => print(s), error: (s) => print(s), warn: (s) => print(s) }};
const window = {{ addEventListener: () => {{}}, speechSynthesis: {{ cancel: () => {{}}, speak: () => {{}} }} }};
const setInterval = () => 1;
const clearInterval = () => {{}};
const setTimeout = (fn) => {{ if (typeof fn === 'function') fn(); return 1; }};
const clearTimeout = () => {{}};
const elements = {{}};
function createMockEl(id) {{
  return {{
    id: id,
    value: '',
    textContent: '',
    innerHTML: '',
    className: '',
    classList: {{
      _classes: new Set(),
      add: function(c) {{ this._classes.add(c); }},
      remove: function(c) {{ this._classes.delete(c); }},
      contains: function(c) {{ return this._classes.has(c); }}
    }},
    style: {{ display: 'none' }},
    querySelectorAll: () => []
  }};
}}
const document = {{
  getElementById: (id) => {{
    if (!elements[id]) elements[id] = createMockEl(id);
    return elements[id];
  }},
  querySelectorAll: () => [],
  addEventListener: () => {{}}
}};
const localStorage = {{
  _store: {{}},
  getItem: (k) => localStorage._store[k] || null,
  setItem: (k, v) => {{ localStorage._store[k] = String(v); }},
  removeItem: (k) => {{ delete localStorage._store[k]; }}
}};
function showToast(msg) {{}}
function openModal(id) {{}}

{js_code}

function assertEq(actual, expected, msg) {{
  if (actual !== expected) {{
    throw new Error('FAIL: ' + msg + ' -> expected: ' + expected + ', actual: ' + actual);
  }}
  print('  ✓ ' + msg);
}}

// Setup a fully booked day (packed morning + packed afternoon) on today's date
const todayTestDate = getTodayDateStr();
const fullDayMeetings = [
  {{
    id: 501,
    date: todayTestDate,
    startTime: '09:00',
    endTime: '12:00',
    time: '09:00',
    duration: 180,
    subject: '上午战略会议',
    status: 'scheduled'
  }},
  {{
    id: 502,
    date: todayTestDate,
    startTime: '14:00',
    endTime: '18:00',
    time: '14:00',
    duration: 240,
    subject: '下午运营研讨会',
    status: 'scheduled'
  }}
];
setData(STORAGE_KEYS.MEETINGS, fullDayMeetings);
currentWeekOffset = 0;
renderSupervisorWeeklyBoard();
const weekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;

// 1. Must NOT show 全天排满 card
assertEq(weekHtml.indexOf('全天排满') === -1, true, 'Fully booked day NEVER renders 全天排满 card');
assertEq(weekHtml.indexOf('allday') === -1, true, 'No allday card tags rendered');

// 2. Morning and afternoon must be cleanly separated
assertEq(weekHtml.indexOf('<span>上午</span>') !== -1, true, 'Shows clean <span>上午</span> without emoji or time');
assertEq(weekHtml.indexOf('<span>下午</span>') !== -1, true, 'Shows clean <span>下午</span> without emoji or time');

// 3. No emojis in morning / afternoon
assertEq(weekHtml.indexOf('🌅') === -1, true, 'No 🌅 emoji in weekly board');
assertEq(weekHtml.indexOf('🌇') === -1, true, 'No 🌇 emoji in weekly board');
assertEq(weekHtml.indexOf('☀️') === -1, true, 'No ☀️ emoji in weekly board');

// 4. No specific times (09:00 - 12:00 or 14:00 - 18:00) on dividers or slots
assertEq(weekHtml.indexOf('上午 (09:00 - 12:00)') === -1, true, 'No 09:00 - 12:00 in morning divider');
assertEq(weekHtml.indexOf('09:00 - 12:00 无排期') === -1, true, 'No 09:00 - 12:00 in morning empty slot');
assertEq(weekHtml.indexOf('下午 (14:00 - 18:00)') === -1, true, 'No 14:00 - 18:00 in afternoon divider');
assertEq(weekHtml.indexOf('14:00 - 18:00 无排期') === -1, true, 'No 14:00 - 18:00 in afternoon empty slot');

// 5. Test empty morning and empty afternoon display on upcoming days
const tomorrowDate = formatDateToStr(new Date(Date.now() + 86400000));
const dayAfterDate = formatDateToStr(new Date(Date.now() + 86400000 * 2));
const partialMeetings = [
  {{
    id: 601,
    date: tomorrowDate,
    startTime: '14:30',
    endTime: '16:00',
    time: '14:30',
    duration: 90,
    subject: '下午例会',
    status: 'scheduled'
  }},
  {{
    id: 602,
    date: dayAfterDate,
    startTime: '10:00',
    endTime: '11:30',
    time: '10:00',
    duration: 90,
    subject: '上午例会',
    status: 'scheduled'
  }}
];
setData(STORAGE_KEYS.MEETINGS, partialMeetings);
renderSupervisorWeeklyBoard();
const partialWeekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;

assertEq(partialWeekHtml.indexOf('暂无排期') !== -1, true, 'Clean 暂无排期 slot');
assertEq(partialWeekHtml.indexOf('场排期') === -1, true, 'No 场排期 badge');
assertEq(partialWeekHtml.indexOf('空闲') === -1, true, 'No 空闲 text');
assertEq(partialWeekHtml.indexOf('可约') === -1, true, 'No 可约 text');

print('✓ All Round 17 & Round 18 requirements verified successfully in JSC!');
"""

jsc_path = '/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
temp_file = 'scratch/test_round17_jsc.js'
with open(temp_file, 'w', encoding='utf-8') as f:
    f.write(jsc_code)

proc = subprocess.run([jsc_path, temp_file], capture_output=True, text=True)
print(proc.stdout)
if proc.returncode != 0:
    print(proc.stderr)
    raise AssertionError(f"JSC execution failed with code {proc.returncode}")

print("==========================================================")
print("ALL ROUND 17 MEETING SCHEDULE TESTS PASSED 100%!")
print("==========================================================")

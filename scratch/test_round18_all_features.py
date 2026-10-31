#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os
import re

print("--- Testing Round 18: 5 Core Meeting Reservation Minimalist Requirements ---")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

assert ('padding: 3px 5px;' in html or 'padding: 4px 6px;' in html), ".weekly-card must have compact padding"
assert 'padding: 8px 12px;' in html, ".day-meeting-card must have compact 8px 12px padding"
assert 'margin-bottom: 8px;' in html, ".meeting-card must have compact 8px margin-bottom"
print("✓ Requirement 1 Static: Compact card CSS verified")

# 2. Requirement 3 & 5: Banner and Live Card Hidden from Modal
assert 'id="modalTripBanner" style="display:none !important;"' in html, "#modalTripBanner must be hidden with display:none !important;"
assert 'id="modalTripLiveCard" style="display:none !important;"' in html, "#modalTripLiveCard must be hidden with display:none !important;"
assert 'id="modalTzConversionHint" style="display:none !important;"' in html, "#modalTzConversionHint must be hidden with display:none !important;"
print("✓ Requirements 3 & 5 Static: Banners, live conversion cards, and hint boxes hidden from UI")

# 3. Requirement 4: Simplified Timezone Select Menu
assert '<option value="cameroon">喀麦隆 (UTC+1)</option>' in html, "Select option must be simplified: 喀麦隆 (UTC+1)"
assert '<option value="cairo" selected>埃及·开罗 (UTC+3)</option>' in html, "Select option must be simplified: 埃及·开罗 (UTC+3)"
assert '<option value="med_south_libya">利比亚 (UTC+2)</option>' in html, "Select option must be simplified: 利比亚 (UTC+2)"
assert '<option value="beijing">北京 (UTC+8)</option>' in html, "Select option must be simplified: 北京 (UTC+8)"
assert '🇨🇲 喀麦隆当地时间' not in html, "Complex emoji/descriptions must be removed from select options"
print("✓ Requirement 4 Static: Timezone select menu is simplified to 喀麦隆 (UTC+1) format")

# 4. Functional JS execution via macOS JSC
script_start = html.find('<script>') + len('<script>')
script_end = html.rfind('</script>')
js_code = html[script_start:script_end]

jsc_script = f"""
const console = {{ log: (s) => print(s), error: (s) => print(s), warn: (s) => print(s) }};
const window = {{ addEventListener: () => {{}}, speechSynthesis: {{ cancel: () => {{}}, speak: () => {{}} }} }};
const setInterval = () => 1;
const clearInterval = () => {{}};
const setTimeout = (fn) => {{ if (typeof fn === 'function') fn(); return 1; }};
const clearTimeout = () => {{}};
const confirm = () => true;

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
    focus: () => {{}},
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
function closeModal(id) {{}}

{js_code}

function assertEq(actual, expected, msg) {{
  if (actual !== expected) {{
    throw new Error('FAIL: ' + msg + ' -> expected: ' + expected + ', actual: ' + actual);
  }}
  print('  ✓ ' + msg);
}}

// ==========================================
// Test Req 2: Past Days Hiding in Current Week
// ==========================================
print('--- Testing Req 2: Past Days Hiding in Current Week ---');
assertEq(hidePastWeekdays, true, 'hidePastWeekdays is enabled (true) by default');

currentWeekOffset = 0;
renderSupervisorWeeklyBoard();
let weekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;
assertEq(weekHtml.indexOf('已隐藏过去日期') !== -1, true, 'Toolbar displays 已隐藏过去日期 button');

// Verify that yesterday or earlier dates in the current week are NOT rendered in columns
const today = new Date();
const todayStr = getTodayDateStr();
const sunDate = new Date(today);
sunDate.setDate(today.getDate() - today.getDay());
const sunDateStr = formatDateToStr(sunDate);

if (todayStr > sunDateStr) {{
  // Today is after Sunday, so Sunday is past and must be filtered out
  assertEq(weekHtml.indexOf(sunDateStr) === -1, true, 'Past date (Sunday ' + sunDateStr + ') is hidden from weekly columns');
}}

// Toggle show past days
toggleHidePastDays(false);
assertEq(hidePastWeekdays, false, 'hidePastWeekdays is now false');
renderSupervisorWeeklyBoard();
let fullWeekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;
assertEq(fullWeekHtml.indexOf('显示过去日期') !== -1, true, 'Toolbar button displays 显示过去日期');
if (todayStr > sunDateStr) {{
  assertEq(fullWeekHtml.indexOf(sunDateStr) !== -1, true, 'Sunday ' + sunDateStr + ' is restored and visible');
}}

// Restore default hidePastWeekdays = true
toggleHidePastDays(true);
assertEq(hidePastWeekdays, true, 'Restored hidePastWeekdays = true');

// ==========================================
// Test Req 3, 4, 5: Modal Silence & Accurate Dual-Timezone Auto-Conversion
// ==========================================
print('--- Testing Req 3, 4, 5: Modal Silence & Background Dual-Timezone Conversion ---');
// Setup Leader trip to Cameroon: 2026-10-26 to 2026-10-31 (Cameroon UTC+1, -2h vs Cairo UTC+3)
setData(STORAGE_KEYS.LEADER_TRIPS, [{{
  id: 701,
  destination: 'cameroon',
  startDate: '2026-10-26',
  endDate: '2026-10-31',
  remark: '喀麦隆商务考察'
}}]);

// User creates meeting on 2026-10-28 (Trip date)
openAddMeetingModalWithSlot('2026-10-28', '14:00', 60);

// Check that top trip banner and live conversion cards remain strictly hidden
assertEq(elements['modalTripBanner'].style.display, 'none', 'Modal trip banner is strictly hidden');
assertEq(elements['modalTripLiveCard'].style.display, 'none', 'Modal trip live card is strictly hidden');
assertEq(elements['modalTzConversionHint'].style.display, 'none', 'Modal hint is strictly hidden');
assertEq(elements['lblMeetingStartTime'].innerHTML, '开始时间 *', 'Start time label is minimal without noise');
assertEq(elements['lblMeetingEndTime'].innerHTML, '结束时间 *', 'End time label is minimal without noise');

// Case A: User chooses Cairo timezone (cairo, UTC+3) and inputs 14:00 - 15:00
elements['inputMeetingTimezoneBase'].value = 'cairo';
elements['inputMeetingStartTime'].value = '14:00';
elements['inputMeetingEndTime'].value = '15:00';
elements['inputMeetingSubject'].value = '埃及开罗输入测试会';
saveMeeting();

let mList = getData(STORAGE_KEYS.MEETINGS);
let mA = mList.find(m => m.subject === '埃及开罗输入测试会');
assertEq(Boolean(mA), true, 'Meeting A saved successfully');
assertEq(mA.tzBase, 'cairo', 'Meeting A tzBase is cairo');
assertEq(mA.startTime, '14:00', 'Cairo baseline start is 14:00');
assertEq(mA.localStartTime, '12:00', 'Silently converted to Cameroon local 12:00');
assertEq(mA.localEndTime, '13:00', 'Silently converted to Cameroon local 13:00');

let dtA = getMeetingDisplayTime(mA);
assertEq(dtA.start, '12:00', 'Card displays Cameroon local start 12:00');
assertEq(dtA.end, '13:00', 'Card displays Cameroon local end 13:00');
assertEq(dtA.cairoStart, '14:00', 'Sub-note displays Cairo 14:00');

// Case B: User chooses Cameroon timezone (cameroon, UTC+1) and inputs 10:00 - 11:30
openAddMeetingModalWithSlot('2026-10-28', '10:00', 90);
elements['inputMeetingTimezoneBase'].value = 'cameroon';
elements['inputMeetingStartTime'].value = '10:00';
elements['inputMeetingEndTime'].value = '11:30';
elements['inputMeetingSubject'].value = '喀麦隆当地时间输入测试会';
saveMeeting();

mList = getData(STORAGE_KEYS.MEETINGS);
let mB = mList.find(m => m.subject === '喀麦隆当地时间输入测试会');
assertEq(Boolean(mB), true, 'Meeting B saved successfully');
assertEq(mB.tzBase, 'cameroon', 'Meeting B tzBase is cameroon');
assertEq(mB.startTime, '12:00', 'Cairo baseline start is 12:00 (10:00 + 2h)');
assertEq(mB.localStartTime, '10:00', 'Cameroon local start is 10:00');
assertEq(mB.localEndTime, '11:30', 'Cameroon local end is 11:30');

let dtB = getMeetingDisplayTime(mB);
assertEq(dtB.start, '10:00', 'Card displays Cameroon local start 10:00');
assertEq(dtB.end, '11:30', 'Card displays Cameroon local end 11:30');
assertEq(dtB.cairoStart, '12:00', 'Sub-note displays Cairo 12:00');

print('✓ All 5 Round 18 requirements verified 100% in JavaScriptCore!');
"""

jsc_path = '/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
temp_file = 'scratch/test_round18_jsc.js'
with open(temp_file, 'w', encoding='utf-8') as f:
    f.write(jsc_script)

res = subprocess.run([jsc_path, temp_file], capture_output=True, text=True)
print("JSC STDOUT:")
print(res.stdout)
if res.stderr:
    print("JSC STDERR:")
    print(res.stderr)

assert res.returncode == 0, f"JSC execution failed with code {res.returncode}"
print("==========================================================")
print("ALL ROUND 18 REQUIREMENTS VERIFIED AND PASSED 100%!")
print("==========================================================")

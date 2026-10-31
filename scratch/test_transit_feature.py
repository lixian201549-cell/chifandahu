import subprocess
import os
import re

print("--- Testing Cross-Timezone In-Transit Feature (🛫 登记在途) ---")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Static HTML Checks
assert 'id="btnRegisterTransit"' in html, "Missing #btnRegisterTransit button in HTML"
assert '登记在途' in html, "Button must have text '登记在途'"
assert 'openTransitModal()' in html, "Button must call openTransitModal()"
assert 'id="transitModal"' in html, "Missing #transitModal in HTML"
assert 'id="inputTransitTitle"' in html, "Missing #inputTransitTitle in HTML"
assert 'id="inputTransitDepDate"' in html, "Missing #inputTransitDepDate in HTML"
assert 'id="inputTransitDepTime"' in html, "Missing #inputTransitDepTime in HTML"
assert 'id="inputTransitDepTz"' in html, "Missing #inputTransitDepTz in HTML"
assert 'id="inputTransitArrDate"' in html, "Missing #inputTransitArrDate in HTML"
assert 'id="inputTransitArrTime"' in html, "Missing #inputTransitArrTime in HTML"
assert 'id="inputTransitArrTz"' in html, "Missing #inputTransitArrTz in HTML"
assert 'id="transitDurationLiveHint"' in html, "Missing #transitDurationLiveHint in HTML"
assert 'id="inputTransitFlightNo"' in html, "Missing #inputTransitFlightNo in HTML"
assert 'id="inputTransitRemark"' in html, "Missing #inputTransitRemark in HTML"
assert 'id="transitExistingListArea"' in html, "Missing #transitExistingListArea in HTML"
assert 'saveLeaderTransit()' in html, "Missing saveLeaderTransit() call in HTML"
assert 'weekly-card-transit' in html, "Missing .weekly-card-transit CSS in HTML"
assert 'day-transit-card' in html, "Missing .day-transit-card CSS in HTML"

# Layout check: User requested "但我不想它单独呈现在版面上"
# Ensure there is NO standalone section or panel for in-transit on page body
body_parts = html.split('<body')[1].split('</body>')[0]
# Check that there is no independent section like <section id="leaderTransitSection"> or dedicated dashboard panel
assert 'id="leaderTransitSection"' not in body_parts, "Must not create a standalone section for in-transit on layout"
assert 'class="transit-panel"' not in body_parts, "Must not create a standalone panel for in-transit on layout"

print("✓ Static verification passed: Register button, modal, controls, and layout integration verified")

# 2. Extract JS from index.html
js_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if not js_match:
    raise AssertionError("Script tag not found in index.html")
js_code = js_match.group(1)

test_script = f"""
const console = {{ log: (s) => print(s), error: (s) => print(s) }};
const clearTimeout = () => {{}};
const clearInterval = () => {{}};
const setInterval = () => 1;
const setTimeout = () => 1;
const confirm = () => true;
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
        querySelectorAll: () => []
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

{js_code}

function assertEq(a, b, msg) {{
  if (a !== b) {{
    throw new Error('FAIL: ' + msg + ' -> expected: ' + b + ', actual: ' + a);
  }}
}}

function assertTrue(cond, msg) {{
  if (!cond) {{
    throw new Error('FAIL: ' + msg);
  }}
}}

print("--- Step A: Testing Cross-Timezone Transit Math ---");
// Cairo (UTC+3) 09:30 -> Cameroon (UTC+1) 14:45
// Cairo 09:30 (UTC+3) is 06:30 UTC
// Cameroon 14:45 (UTC+1) is 13:45 UTC
// Diff = 13:45 - 06:30 = 7 hours 15 minutes = 435 minutes
const cairoToCameroon = calculateTransitDuration('2026-10-28', '09:30', 'cairo', '2026-10-28', '14:45', 'cameroon');
assertEq(cairoToCameroon.isValid, true, "Transit Cairo->Cameroon should be valid");
assertEq(cairoToCameroon.diffMins, 435, "Cairo 09:30 to Cameroon 14:45 must be exactly 435 mins (7h 15m)");
assertEq(cairoToCameroon.text, "7小时15分", "Duration text should be 7小时15分");
print("✓ Test A1 Passed: Cairo (UTC+3) 09:30 to Cameroon (UTC+1) 14:45 = 7h 15m");

// Cameroon (UTC+1) 10:00 -> Cairo (UTC+3) 17:00
// Cameroon 10:00 (UTC+1) is 09:00 UTC
// Cairo 17:00 (UTC+3) is 14:00 UTC
// Diff = 14:00 - 09:00 = 5 hours = 300 minutes
const cameroonToCairo = calculateTransitDuration('2026-10-30', '10:00', 'cameroon', '2026-10-30', '17:00', 'cairo');
assertEq(cameroonToCairo.isValid, true, "Cameroon->Cairo should be valid");
assertEq(cameroonToCairo.diffMins, 300, "Cameroon 10:00 to Cairo 17:00 must be 300 mins (5h)");
assertEq(cameroonToCairo.text, "5小时", "Duration text should be 5小时");
print("✓ Test A2 Passed: Cameroon (UTC+1) 10:00 to Cairo (UTC+3) 17:00 = 5h");

// Invalid flight: lands earlier than departs
const invalidFlight = calculateTransitDuration('2026-10-28', '14:00', 'cairo', '2026-10-28', '11:00', 'cameroon');
// Cairo 14:00 UTC+3 = 11:00 UTC. Cameroon 11:00 UTC+1 = 10:00 UTC. (Arrives 1 hour before departure in UTC)
assertEq(invalidFlight.isValid, false, "Invalid flight should have isValid = false");
print("✓ Test A3 Passed: Detects invalid landing time earlier than departure");

print("--- Step B: Testing In-Transit Form & Live Hint ---");
document.getElementById('inputTransitDepDate').value = '2026-10-28';
document.getElementById('inputTransitDepTime').value = '09:30';
document.getElementById('inputTransitDepTz').value = 'cairo';
document.getElementById('inputTransitArrDate').value = '2026-10-28';
document.getElementById('inputTransitArrTime').value = '14:45';
document.getElementById('inputTransitArrTz').value = 'cameroon';
handleTransitFormChange();
const hintHtml = document.getElementById('transitDurationLiveHint').innerHTML;
assertTrue(hintHtml.includes('7小时15分'), "Live hint should show calculated duration 7小时15分");
print("✓ Test B Passed: Live calculation hint correctly updates in form");

print("--- Step C: Testing In-Transit Registration & Storage ---");
document.getElementById('inputTransitId').value = '';
document.getElementById('inputTransitTitle').value = '开罗 ✈ 喀麦隆';
document.getElementById('inputTransitFlightNo').value = 'MS887';
document.getElementById('inputTransitRemark').value = '机上免打扰';
saveLeaderTransit();

const savedTransits = getLeaderTransits();
assertEq(savedTransits.length, 1, "Should have 1 transit saved in storage");
assertEq(savedTransits[0].title, '开罗 ✈ 喀麦隆', "Saved title check");
assertEq(savedTransits[0].flightNo, 'MS887', "Saved flightNo check");
assertEq(savedTransits[0].durationMins, 435, "Saved durationMins check");
assertEq(savedTransits[0].durationText, '7小时15分', "Saved durationText check");
print("✓ Test C Passed: Transit saved successfully into LEADER_TRANSITS");

print("--- Step D: Testing Weekly Board & Day Calendar Integration (不单独呈现在版面上) ---");
// Render weekly board
hidePastWeekdays = false;
renderSupervisorWeeklyBoard();
const weeklyHtml = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertTrue(weeklyHtml.includes('weekly-card-transit'), "Weekly board must include .weekly-card-transit card");
assertTrue(weeklyHtml.includes('MS887'), "Weekly board must display flight number MS887");
assertTrue(weeklyHtml.includes('7小时15分'), "Weekly board must display transit duration 7小时15分");
assertTrue(weeklyHtml.includes('🛫 在途'), "Weekly board day header must display 🛫 在途 badge");
print("✓ Test D1 Passed: In-transit card and header badge seamlessly integrated into Weekly Board");

// Render day calendar for 2026-10-28
selectedTimelineDate = '2026-10-28';
renderSupervisorDayCalendar();
const dayHtml = document.getElementById('supervisorDayCalendarContainer').innerHTML;
assertTrue(dayHtml.includes('day-transit-card'), "Day calendar must include .day-transit-card");
assertTrue(dayHtml.includes('开罗 ✈ 喀麦隆'), "Day calendar must include transit title");
assertTrue(dayHtml.includes('7小时15分'), "Day calendar must include transit duration");
print("✓ Test D2 Passed: In-transit card seamlessly integrated into Day Calendar timeline");

// Chalkboard executive bar
updateChalkboardExecutiveBar();
const tripText = document.getElementById('execBarTripText').textContent;
// If today matches, it shows in-transit
print("Chalkboard bar text: " + tripText);

print("--- Step E: Testing Deletion ---");
deleteLeaderTransit(savedTransits[0].id);
assertEq(getLeaderTransits().length, 0, "Transits should be empty after deletion");
print("✓ Test E Passed: Deletion restores normal state cleanly");

print("ALL TRANSIT FEATURE TESTS COMPLETED WITH 100% SUCCESS!");
"""

with open('scratch/test_transit_script.js', 'w', encoding='utf-8') as f:
    f.write(test_script)

res = subprocess.run(
    ['/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc', 'scratch/test_transit_script.js'],
    capture_output=True,
    text=True
)

print(res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)

assert res.returncode == 0, f"jsc test failed with code {res.returncode}"
print("=== All Test Suites Passed Successfully! ===")

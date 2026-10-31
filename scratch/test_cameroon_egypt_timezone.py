import subprocess
import os
import re

print("--- Testing Cameroon Trip Timezone Auto-Conversion (Egypt Cairo UTC+3 vs Cameroon UTC+1) ---")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Static checks
assert 'id="modalTripLiveCard"' in html, "Missing #modalTripLiveCard in HTML"
assert 'id="lblMeetingStartTime"' in html, "Missing #lblMeetingStartTime in HTML"
assert 'id="lblMeetingEndTime"' in html, "Missing #lblMeetingEndTime in HTML"
assert 'setMeetingModalTzMode' in html, "Missing setMeetingModalTzMode in HTML"
assert '喀麦隆 (UTC+1)' in html, "Simplified select option 喀麦隆 (UTC+1) must be in HTML"
print("✓ Static HTML and JS elements verified")

# Extract JS from index.html
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
  print('  ✓ ' + msg);
}}

// 1. Setup Leader trip to Cameroon: 2026-10-26 to 2026-10-31 (Cameroon is UTC+1, -2h vs Cairo UTC+3)
setData(STORAGE_KEYS.LEADER_TRIPS, [{{
  id: 401,
  destination: 'cameroon',
  startDate: '2026-10-26',
  endDate: '2026-10-31',
  remark: '喀麦隆代表处出差'
}}]);

selectedTimelineDate = '2026-10-28';
openAddMeetingModal();

assertEq(elements['inputMeetingDate'].value, '2026-10-28', 'Modal date is 2026-10-28');
const trip = getTripForDate('2026-10-28');
assertEq(Boolean(trip), true, 'Trip to Cameroon found');
assertEq(trip.diffHours, -2, 'Cameroon diffHours is -2 hours vs Cairo');

// 2. User switches to Cairo mode (录入埃及·开罗时间)
setMeetingModalTzMode('cairo');
assertEq(elements['inputMeetingTimezoneBase'].value, 'cairo', 'Timezone base is set to cairo');

// User inputs 14:00 - 15:00 in Egypt time
elements['inputMeetingStartTime'].value = '14:00';
elements['inputMeetingEndTime'].value = '15:00';
elements['inputMeetingSubject'].value = '喀麦隆交付战略评审会';
elements['inputMeetingReporter'].value = '海外交付部';
handleMeetingModalTimezoneChange();

// 3. Verify Live Conversion Card and Trip Banner are hidden per user minimalist UI request
assertEq(elements['modalTripLiveCard'].style.display, 'none', 'modalTripLiveCard is hidden');
assertEq(elements['modalTripBanner'].style.display, 'none', 'modalTripBanner is hidden');

// 4. Save meeting
saveMeeting();

let meetingsList = getData(STORAGE_KEYS.MEETINGS);
let m = meetingsList.find(x => x.subject === '喀麦隆交付战略评审会');
assertEq(Boolean(m), true, 'Meeting must exist in storage');
assertEq(m.tzBase, 'cairo', 'Meeting tzBase is strictly cairo');
assertEq(m.startTime, '14:00', 'Cairo baseline startTime is 14:00');
assertEq(m.endTime, '15:00', 'Cairo baseline endTime is 15:00');
assertEq(m.localStartTime, '12:00', 'Cameroon localStartTime is automatically converted to 12:00');
assertEq(m.localEndTime, '13:00', 'Cameroon localEndTime is automatically converted to 13:00');

// 5. Verify getMeetingDisplayTime returns Cameroon local time 12:00 - 13:00 with Cairo 14:00
let dt = getMeetingDisplayTime(m);
assertEq(dt.start, '12:00', 'Display start is Cameroon local time 12:00');
assertEq(dt.end, '13:00', 'Display end is Cameroon local time 13:00');
assertEq(dt.cairoStart, '14:00', 'Cairo start is 14:00');
assertEq(dt.cairoEnd, '15:00', 'Cairo end is 15:00');
assertEq(dt.isShifted, true, 'isShifted is true');

// 6. Verify Weekly Board rendering on Cameroon column
hidePastWeekdays = false;
renderSupervisorWeeklyBoard();
let weekHtml = elements['supervisorWeeklyBoardContainer'].innerHTML;
assertEq(weekHtml.indexOf('12:00 - 13:00') !== -1, true, 'Weekly card displays 12:00 - 13:00');
assertEq(weekHtml.indexOf('开罗 14:00') !== -1, true, 'Weekly card displays [开罗 14:00]');

// 7. Secretary edits the meeting: verify it opens in Cairo mode with 14:00 - 15:00
editMeeting(m.id);
assertEq(elements['inputMeetingTimezoneBase'].value, 'cairo', 'Edit modal opens with cairo tzBase');
assertEq(elements['inputMeetingStartTime'].value, '14:00', 'Edit modal inputs show Egypt time 14:00');
assertEq(elements['inputMeetingEndTime'].value, '15:00', 'Edit modal inputs show Egypt time 15:00');

// 8. Secretary switches modal to Cameroon mode: verify auto-conversion to 12:00 - 13:00
setMeetingModalTzMode('cameroon');
assertEq(elements['inputMeetingStartTime'].value, '12:00', 'Switching to Cameroon mode converts start to 12:00');
assertEq(elements['inputMeetingEndTime'].value, '13:00', 'Switching to Cameroon mode converts end to 13:00');

print('✓ Cameroon & Egypt dual-timezone auto-conversion verified 100% successfully!');
"""

jsc_path = '/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
temp_file = 'scratch/test_cameroon_jsc.js'
with open(temp_file, 'w', encoding='utf-8') as f:
    f.write(test_script)

proc = subprocess.run([jsc_path, temp_file], capture_output=True, text=True)
print(proc.stdout)
if proc.returncode != 0:
    print(proc.stderr)
    raise AssertionError(f"JSC execution failed with code {proc.returncode}")

print("=================================================================")
print("ALL CAMEROON & EGYPT TIMEZONE CONVERSION TESTS PASSED 100%!")
print("=================================================================")

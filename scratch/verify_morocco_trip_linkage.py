import re
import subprocess

# 1. Run run_tests.py
print("Running run_tests.py...")
res = subprocess.run(["python3", "scratch/run_tests.py"], capture_output=True, text=True)
if res.returncode != 0:
    print(res.stdout)
    print(res.stderr)
    exit(1)
print("run_tests.py passed successfully!")

# 2. Run Morocco trip linkage verification test
jsc_test = """
// 1. Verify Morocco timezone config (UTC+0 · 比开罗慢 3 小时)
const moroccoInfo = TRIP_TIMEZONE_MAP['morocco'];
assertEq(moroccoInfo.utcOffset, 0, 'Morocco utcOffset must be 0 (UTC+0)');
assertEq(getTripTimezoneDiffHours('morocco'), -3, 'Morocco diff relative to Cairo must be -3 hours');
const moroccoRep = TIMEZONE_REPS.find(r => r.id === 'morocco');
assertEq(moroccoRep.utcOffset, 0, 'Morocco rep utcOffset must be 0');

// 2. Setup Leader trip to Libya: 2026-10-18 to 2026-10-25 (Libya is UTC+2, -1h vs Cairo)
setData(STORAGE_KEYS.LEADER_TRIPS, [{
  id: 301,
  destination: 'med_south_libya',
  startDate: '2026-10-18',
  endDate: '2026-10-25',
  remark: '利比亚代表处现场出差'
}]);

// 3. User opens Add Meeting Modal on 2026-10-20 (during Libya trip)
selectedTimelineDate = '2026-10-20';
openAddMeetingModal();

assertEq(document.getElementById('inputMeetingDate').value, '2026-10-20', 'Modal date should be 2026-10-20');
assertEq(document.getElementById('inputMeetingTimezoneBase').value, 'med_south_libya', 'Modal tz defaults to trip destination Libya');

// 4. Secretary chooses Morocco timezone and inputs 09:00 - 10:00 Morocco time
document.getElementById('inputMeetingTimezoneBase').value = 'morocco';
handleMeetingModalTimezoneChange(); // Dropdown onchange event fires

document.getElementById('inputMeetingStartTime').value = '09:00'; // User enters 09:00
document.getElementById('inputMeetingEndTime').value = '10:00';   // User enters 10:00
document.getElementById('inputMeetingSubject').value = '摩洛哥重点客户联合评审';
document.getElementById('inputMeetingReporter').value = '摩洛哥代表处';
handleMeetingModalTimezoneChange(); // Input oninput/blur updates hint

// Check real-time conversion hint in modal:
const hintText = document.getElementById('modalTzConversionHint').innerHTML;
assertEq(hintText.includes('11:00 - 12:00'), true, 'Hint must calculate Libya time 11:00 - 12:00, got: ' + hintText);
assertEq(hintText.includes('12:00 - 13:00'), true, 'Hint must calculate Cairo time 12:00 - 13:00, got: ' + hintText);

// 5. Save meeting
saveMeeting();

let meetings = getData(STORAGE_KEYS.MEETINGS);
let m = meetings.find(x => x.subject === '摩洛哥重点客户联合评审');
assertEq(Boolean(m), true, 'Meeting must exist in storage');
assertEq(m.tzBase, 'morocco', 'm.tzBase must be morocco');
assertEq(m.startTime, '12:00', 'm.startTime (Cairo baseline) must be 12:00, got: ' + m.startTime);
assertEq(m.endTime, '13:00', 'm.endTime (Cairo baseline) must be 13:00, got: ' + m.endTime);
assertEq(m.inputStartTime, '09:00', 'm.inputStartTime must be 09:00');

// 6. Verify getMeetingDisplayTime converts Morocco 09:00 to Libya 11:00
let dt = getMeetingDisplayTime(m);
assertEq(dt.start, '11:00', 'Display start must be Libya local time 11:00, got: ' + dt.start);
assertEq(dt.end, '12:00', 'Display end must be Libya local time 12:00, got: ' + dt.end);
assertEq(dt.cairoStart, '12:00', 'Cairo start must be 12:00, got: ' + dt.cairoStart);
assertEq(dt.isShifted, true, 'isShifted must be true');

// 7. Verify Weekly Board rendering on Libya day column
renderSupervisorWeeklyBoard();
let weekHtml = document.getElementById('supervisorWeeklyBoardContainer').innerHTML;
assertEq(weekHtml.includes('11:00 - 12:00'), true, 'Weekly board card MUST show Libya local time 11:00 - 12:00');
assertEq(weekHtml.includes('开罗 12:00'), true, 'Weekly board card MUST show quiet Cairo time: 开罗 12:00');

// 8. Secretary clicks EDIT on the card: editMeeting(m.id)
editMeeting(m.id);
assertEq(document.getElementById('inputMeetingTimezoneBase').value, 'morocco', 'Edit modal tz MUST be morocco');
assertEq(document.getElementById('inputMeetingStartTime').value, '09:00', 'Edit modal MUST present Morocco 09:00, got: ' + document.getElementById('inputMeetingStartTime').value);
assertEq(document.getElementById('inputMeetingEndTime').value, '10:00', 'Edit modal MUST present Morocco 10:00, got: ' + document.getElementById('inputMeetingEndTime').value);

// 9. Secretary changes timezone dropdown to Libya in modal -> auto-converts to 11:00 - 12:00!
document.getElementById('inputMeetingTimezoneBase').value = 'med_south_libya';
handleMeetingModalTimezoneChange();
assertEq(document.getElementById('inputMeetingStartTime').value, '11:00', 'Switching to Libya auto-converts to 11:00, got: ' + document.getElementById('inputMeetingStartTime').value);
assertEq(document.getElementById('inputMeetingEndTime').value, '12:00', 'Switching to Libya auto-converts to 12:00, got: ' + document.getElementById('inputMeetingEndTime').value);

// Secretary switches to Cairo in modal -> auto-converts to 12:00 - 13:00!
document.getElementById('inputMeetingTimezoneBase').value = 'cairo';
handleMeetingModalTimezoneChange();
assertEq(document.getElementById('inputMeetingStartTime').value, '12:00', 'Switching to Cairo auto-converts to 12:00');
assertEq(document.getElementById('inputMeetingEndTime').value, '13:00', 'Switching to Cairo auto-converts to 13:00');

// Secretary switches back to Morocco in modal -> auto-converts to 09:00 - 10:00!
document.getElementById('inputMeetingTimezoneBase').value = 'morocco';
handleMeetingModalTimezoneChange();
assertEq(document.getElementById('inputMeetingStartTime').value, '09:00', 'Switching back to Morocco auto-converts to 09:00');
assertEq(document.getElementById('inputMeetingEndTime').value, '10:00', 'Switching back to Morocco auto-converts to 10:00');

// 10. Re-save and verify
saveMeeting();
meetings = getData(STORAGE_KEYS.MEETINGS);
m = meetings.find(x => x.id === m.id);
assertEq(m.startTime, '12:00', 'Cairo baseline startTime stays 12:00');
dt = getMeetingDisplayTime(m);
assertEq(dt.start, '11:00', 'Display start stays Libya 11:00');

print('SUCCESS: Morocco UTC+0 and full multi-timezone linkage across modal & calendar verified 100%!');
"""

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
assert m, "Script tag not found in index.html"
js_code = m.group(1)

test_runner_js = f"""
const elements = {{}};
function getEl(id) {{
  if (!elements[id]) {{
    elements[id] = {{
      id: id,
      value: '',
      innerHTML: '',
      textContent: '',
      style: {{ display: 'block' }},
      classList: {{
        classes: [],
        add: function(c) {{ if (!this.classes.includes(c)) this.classes.push(c); }},
        remove: function(c) {{ this.classes = this.classes.filter(x => x !== c); }},
        toggle: function(c, force) {{
          if (force !== undefined) {{
            if (force) this.add(c); else this.remove(c);
          }} else {{
            if (this.contains(c)) this.remove(c); else this.add(c);
          }}
        }},
        contains: function(c) {{ return this.classes.includes(c); }}
      }},
      focus: function() {{}},
      setAttribute: function(k, v) {{ this[k] = v; }},
      getAttribute: function(k) {{ return this[k] || ''; }},
      querySelectorAll: function() {{ return []; }},
      appendChild: function() {{}}
    }};
  }}
  return elements[id];
}}

const document = {{
  getElementById: getEl,
  querySelector: function(sel) {{ return getEl(sel.replace(/^[#.]/, '')); }},
  querySelectorAll: function(sel) {{ return []; }},
  body: {{ classList: getEl('body').classList }},
  createElement: function(tag) {{ return getEl(tag + '_' + Math.random()); }},
  addEventListener: function() {{}}
}};
const window = {{
  scrollTo: function() {{}},
  convertingRequestId: null
}};
const confirm = () => true;
let toasts = [];
const setInterval = () => 1;
const setTimeout = () => 1;
const clearInterval = () => {{}};
const clearTimeout = () => {{}};
const localStorage = {{
  store: {{}},
  getItem: function(k) {{ return this.store[k] || null; }},
  setItem: function(k, v) {{ this.store[k] = String(v); }},
  removeItem: function(k) {{ delete this.store[k]; }}
}};
const console = {{ log: print, error: print, warn: print }};

function assertEq(act, exp, msg) {{
  if (act !== exp) {{
    throw new Error('FAIL: ' + msg + ' -> expected: ' + exp + ', actual: ' + act);
  }}
}}

{js_code}

{jsc_test}
"""

with open("scratch/test_morocco_linkage.js", "w", encoding="utf-8") as f:
    f.write(test_runner_js)

res = subprocess.run(["/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc", "scratch/test_morocco_linkage.js"], capture_output=True, text=True)
print("JSC output:")
print(res.stdout)
if res.returncode != 0:
    print("JSC error:")
    print(res.stderr)
    exit(1)

print("ALL MOROCCO LINKAGE TESTS PASSED 100%!")

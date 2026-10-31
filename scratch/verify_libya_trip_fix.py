import re
import subprocess

# 1. Run run_tests.py
print("Running run_tests.py...")
res = subprocess.run(["python3", "scratch/run_tests.py"], capture_output=True, text=True)
print("run_tests.py exit code:", res.returncode)
if res.returncode != 0:
    print(res.stdout)
    print(res.stderr)
    exit(1)
print(res.stdout[-300:])

# 2. Now run specialized JSC test verifying the Libya 9:00 -> 10:00 bug is completely fixed
jsc_test = """
// 1. Setup Leader trip to Libya: 2026-10-18 to 2026-10-25
setData(STORAGE_KEYS.LEADER_TRIPS, [{
  id: 201,
  destination: 'med_south_libya',
  startDate: '2026-10-18',
  endDate: '2026-10-25',
  remark: '利比亚代表处出差'
}]);

// 2. Add new meeting on 2026-10-20 starting at 9:00 local time
selectedTimelineDate = '2026-10-20';
openAddMeetingModal();

// Check modal values
assert(getEl('inputMeetingDate').value === '2026-10-20', 'Modal date should be 2026-10-20');
assert(getEl('inputMeetingTimezoneBase').value === 'med_south_libya', 'Modal tz should be med_south_libya');

// User inputs 9点 (09:00 - 09:45)
getEl('inputMeetingStartTime').value = '09:00';
getEl('inputMeetingEndTime').value = '09:45';
getEl('inputMeetingSubject').value = '利比亚重点业务现场汇报';
getEl('inputMeetingDecision').value = '审议利比亚现场拓展策略';
saveMeeting();

let meetings = getData(STORAGE_KEYS.MEETINGS);
let m = meetings.find(x => x.subject === '利比亚重点业务现场汇报');
assert(m, 'Meeting must exist in storage');
assert(m.localStartTime === '09:00', 'm.localStartTime must be 09:00, got: ' + m.localStartTime);
assert(m.localEndTime === '09:45', 'm.localEndTime must be 09:45, got: ' + m.localEndTime);
assert(m.startTime === '10:00', 'm.startTime (Cairo baseline) must be 10:00, got: ' + m.startTime);

// 3. Verify getMeetingDisplayTime returns 09:00
let dt = getMeetingDisplayTime(m);
assert(dt.start === '09:00', 'Display start must be 09:00, got: ' + dt.start);
assert(dt.end === '09:45', 'Display end must be 09:45, got: ' + dt.end);
assert(dt.cairoStart === '10:00', 'Cairo start must be 10:00, got: ' + dt.cairoStart);
assert(dt.isShifted === true, 'isShifted must be true');

// 4. Verify Weekly Board rendering
renderSupervisorWeeklyBoard();
let weekHtml = getEl('supervisorWeeklyBoardContainer').innerHTML;
assert(weekHtml.indexOf('09:00 - 09:45') !== -1, 'Weekly board card MUST show 09:00 - 09:45');
assert(weekHtml.indexOf('开罗 10:00') !== -1, 'Weekly board card MUST show quiet Cairo time: 开罗 10:00');

// 5. Verify Day Calendar rendering
renderSupervisorDayCalendar();
let dayHtml = getEl('supervisorDayCalendarContainer').innerHTML;
assert(dayHtml.indexOf('09:00 - 09:45') !== -1, 'Day view card MUST show 09:00 - 09:45');
assert(dayHtml.indexOf('开罗 10:00') !== -1, 'Day view card MUST show 开罗 10:00');

// 6. User clicks EDIT on the card: editMeeting(m.id)
editMeeting(m.id);
assert(getEl('inputMeetingStartTime').value === '09:00', 'Edit modal MUST open with local time 09:00, got: ' + getEl('inputMeetingStartTime').value);
assert(getEl('inputMeetingEndTime').value === '09:45', 'Edit modal MUST open with local time 09:45, got: ' + getEl('inputMeetingEndTime').value);
assert(getEl('inputMeetingTimezoneBase').value === 'med_south_libya', 'Edit modal tz MUST be med_south_libya');

// User finishes editing (updates subject / notes) and saves
getEl('inputMeetingSubject').value = '利比亚重点业务现场汇报(已审阅)';
saveMeeting();

// Re-check storage & display
meetings = getData(STORAGE_KEYS.MEETINGS);
m = meetings.find(x => x.id === m.id);
assert(m.subject === '利比亚重点业务现场汇报(已审阅)', 'Subject updated');
assert(m.localStartTime === '09:00', 'After editing, localStartTime MUST still be 09:00');
assert(m.startTime === '10:00', 'After editing, Cairo baseline startTime MUST still be 10:00');

dt = getMeetingDisplayTime(m);
assert(dt.start === '09:00', 'After editing, display start MUST stay 09:00');

// Verify copy notice format
let copiedText = '';
const originalCopyToClipboard = copyToClipboard;
copyToClipboard = function(txt) { copiedText = txt; };
copySingleMeetingNotice(m.id);
assert(copiedText.indexOf('09:00 - 09:45 (当地时间 | 对应开罗时间 10:00 - 10:45)') !== -1, 'Copied notice must show 09:00 - 09:45 local time, got: ' + copiedText);

print('SUCCESS: Libya 09:00 input strictly persists as 09:00 across all views and edit operations!');
"""

# Extract JS from index.html and append jsc_test
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
js_content = m.group(1)

# Build jsc test bundle
test_js = f"""
const console = {{ log: print, error: print }};
const localStorage = {{ 
  _s: {{}}, 
  getItem: k => localStorage._s[k] || null, 
  setItem: (k,v) => localStorage._s[k] = v 
}};
const elements = {{}};
function getEl(id) {{
  if (!elements[id]) {{
    elements[id] = {{ 
      id, 
      value: '', 
      style: {{}}, 
      classList: {{ add: ()=>{{}}, remove: ()=>{{}}, contains: ()=>false, toggle: ()=>false }}, 
      innerHTML: '', 
      textContent: '', 
      querySelectorAll: () => [],
      focus: () => {{}}
    }};
  }}
  return elements[id];
}}
const document = {{ 
  getElementById: getEl,
  querySelectorAll: () => [],
  addEventListener: () => {{}},
  body: {{ classList: {{ add: ()=>{{}}, remove: ()=>{{}}, toggle: ()=>false, contains: ()=>false }} }}
}};
const confirm = () => true;
const setInterval = () => 1;
const setTimeout = () => 1;
const clearTimeout = () => {{}};
const window = {{ addEventListener: () => {{}} }};
function assert(cond, msg) {{
  if (!cond) throw new Error("Assertion failed: " + msg);
}}

{js_content}

{jsc_test}
"""

with open("scratch/test_libya_verification.js", "w", encoding="utf-8") as f:
    f.write(test_js)

res2 = subprocess.run(["/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc", "scratch/test_libya_verification.js"], capture_output=True, text=True)
print("JSC verification test output:")
print(res2.stdout)
if res2.stderr:
    print("JSC test stderr:", res2.stderr)
assert res2.returncode == 0, "JSC verification failed!"
print("ALL VERIFICATION CHECKS PASSED 100%!")

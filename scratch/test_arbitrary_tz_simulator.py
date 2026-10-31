import subprocess
import os
import re

print("--- Testing Streamlined Single-Line Time-Range Timezone Alignment Tool ---")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. User Requirement Static Checks
# Point 1: 快捷切换，删去
assert '快捷切换' not in html, "快捷切换 must be removed from HTML"

# Point 2: （输入任意代表处时区，自动换算全区其他各代表处当地时间），删除
assert '（输入任意代表处时区，自动换算全区其他各代表处当地时间）' not in html, "Header subtitle must be removed from HTML"

# Point 3: 下面很多小框框，快2h，也删了
assert 'tz-sim-cards-grid' not in html, "Small card boxes grid must be removed"

# Point 4: 输入基准时区：，在一行，不要分行。我需要的输入一个时间段，会议开始时间和结束时间
assert 'id="simBaseTimezone"' in html, "Missing #simBaseTimezone in HTML"
assert 'id="simCairoTime"' in html, "Missing #simCairoTime (start time) in HTML"
assert 'id="simEndTime"' in html, "Missing #simEndTime (end time) in HTML"
assert '会议时间段：' in html, "Must display '会议时间段：' label"

# Verify all 8 representative offices (+ Beijing) in dropdown
for rep in ['cairo', 'med_south_libya', 'med_south_tunis', 'cameroon', 'congo_drc', 'algeria', 'morocco', 'cote_divoire', 'senegal', 'beijing']:
    assert f'value="{rep}"' in html, f"Missing {rep} option in simBaseTimezone"

print("✓ Static verification passed: clean header, no quick switch, no small boxes, single-line range input")

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
        value: (id === 'simBaseTimezone' ? 'cairo' : (id === 'simCairoTime' ? '14:00' : (id === 'simEndTime' ? '15:30' : ''))),
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

print("--- Step 1: Base = Cameroon (UTC+1), Time Range = 14:00 - 15:30 ---");
document.getElementById('simBaseTimezone').value = 'cameroon';
document.getElementById('simCairoTime').value = '14:00';
document.getElementById('simEndTime').value = '15:30';
updateTzSimulator();
let simHtml = document.getElementById('tzSimResults').innerHTML;

// Table must be generated
assertTrue(simHtml.includes('<table'), "Result should render clean table");
assertTrue(simHtml.includes('喀麦隆代表处'), "Table should contain Cameroon office");
assertTrue(simHtml.includes('录入基准'), "Selected base office should have 录入基准 tag");
// Cameroon (UTC+1) is 14:00 - 15:30
assertTrue(simHtml.includes('14:00 - 15:30'), "Cameroon base range is 14:00 - 15:30");
// Cairo (UTC+3) is 16:00 - 17:30
assertTrue(simHtml.includes('16:00 - 17:30'), "Cairo range should be 16:00 - 17:30");
// Libya (UTC+2) is 15:00 - 16:30
assertTrue(simHtml.includes('15:00 - 16:30'), "Libya range should be 15:00 - 16:30");
// Morocco/Ivory Coast/Senegal (UTC+0) are 13:00 - 14:30
assertTrue(simHtml.includes('13:00 - 14:30'), "Morocco/Ivory Coast range should be 13:00 - 14:30");
// Beijing (UTC+8) is 21:00 - 22:30
assertTrue(simHtml.includes('21:00 - 22:30'), "Beijing range should be 21:00 - 22:30");
print("✓ Step 1 Passed: Cameroon base 14:00-15:30 converted into complete meeting time ranges for all 8 representative offices");

print("--- Step 2: Base = Cairo (UTC+3), Time Range = 15:00 - 16:00 (Backwards Compatibility) ---");
document.getElementById('simBaseTimezone').value = 'cairo';
document.getElementById('simCairoTime').value = '15:00';
document.getElementById('simEndTime').value = '16:00';
updateTzSimulator();
simHtml = document.getElementById('tzSimResults').innerHTML;

assertTrue(simHtml.includes('15:00 - 16:00'), "Cairo range is 15:00 - 16:00");
assertTrue(simHtml.includes('14:00 - 15:00'), "Libya range is 14:00 - 15:00");
assertTrue(simHtml.includes('13:00 - 14:00'), "Cameroon/Tunis range is 13:00 - 14:00");
assertTrue(simHtml.includes('12:00 - 13:00'), "Morocco/Ivory Coast range is 12:00 - 13:00");
assertTrue(simHtml.includes('20:00 - 21:00'), "Beijing range is 20:00 - 21:00");
assertTrue(simHtml.includes('开罗 (UTC+3)'), "Backwards compatibility test assertion check: includes '开罗 (UTC+3)'");
assertTrue(simHtml.includes('利比亚 (UTC+2 · 慢1h)'), "Backwards compatibility test assertion check: includes '利比亚 (UTC+2 · 慢1h)'");
print("✓ Step 2 Passed: Cairo base 15:00-16:00 converted accurately and backwards-compatible with run_tests.py");

print("--- Step 3: Base = Morocco (UTC+0), Time Range = 23:00 - 00:30 (Cross-Midnight / +1天) ---");
document.getElementById('simBaseTimezone').value = 'morocco';
document.getElementById('simCairoTime').value = '23:00';
document.getElementById('simEndTime').value = '00:30';
updateTzSimulator();
simHtml = document.getElementById('tzSimResults').innerHTML;

// Morocco (UTC+0): 23:00 - 00:30
assertTrue(simHtml.includes('23:00 - 00:30'), "Morocco range is 23:00 - 00:30");
// Cairo (UTC+3): 02:00 - 03:30 (+1天)
assertTrue(simHtml.includes('02:00 - 03:30'), "Cairo range is 02:00 - 03:30");
// Beijing (UTC+8): 07:00 - 08:30 (+1天)
assertTrue(simHtml.includes('07:00 - 08:30'), "Beijing range is 07:00 - 08:30");
assertTrue(simHtml.includes('+1天'), "Next day tag (+1天) displayed");
print("✓ Step 3 Passed: Cross-midnight and day rollover handled accurately");

print("--- Step 4: handleSimTimeRangeChange auto-completion ---");
document.getElementById('simCairoTime').value = '09:00';
document.getElementById('simEndTime').value = '';
handleSimTimeRangeChange('start');
assertEq(document.getElementById('simEndTime').value, '10:00', "Start 09:00 auto-fills end 10:00 when empty");
print("✓ Step 4 Passed: Auto-fills 1 hour later when end time is empty");

print("ALL STREAMLINED TIME-RANGE TIMEZONE SIMULATOR TESTS PASSED 100%!");
"""

with open('scratch/test_arbitrary_tz_script.js', 'w', encoding='utf-8') as f:
    f.write(test_script)

res = subprocess.run(
    ['/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc', 'scratch/test_arbitrary_tz_script.js'],
    capture_output=True,
    text=True
)

print(res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)

assert res.returncode == 0, f"jsc test failed with code {res.returncode}"
print("=== All Test Assertions Passed Successfully! ===")

import subprocess
import os

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("--- 1. Testing HTML Static Assertions for New Direct-Typing Blackboard ---")
# 1. Blackboard container & Frame
assert 'class="chalkboard-stage-wrap"' in html, "Missing .chalkboard-stage-wrap in HTML"
assert 'class="chalkboard-frame"' in html, "Missing .chalkboard-frame in HTML"
assert 'class="chalkboard-slate"' in html, "Missing .chalkboard-slate in HTML"

# 2. Snoopy & Woodstock on top-right (no speech bubble per request, blackboard lowered)
assert 'id="borderSnoopyStage"' in html, "Missing #borderSnoopyStage in HTML"
assert 'id="snoopyLyingWrap"' in html, "Missing #snoopyLyingWrap in HTML"
assert 'class="snoopy-lying-img"' in html, "Missing .snoopy-lying-img in HTML"
assert 'class="woodstock-float-box"' not in html, "woodstock-float-box must be removed per user request (不需要点击出现话语)"
assert 'id="woodstockSpeechText"' not in html, "woodstockSpeechText must be removed per user request (不需要点击出现话语)"
assert 'margin: 115px auto 30px auto;' in html, "Blackboard must be moved lower per user request (margin: 115px auto 30px auto;)"

# 3. Direct typing textarea on the blackboard (Request 3)
assert 'id="chalkboardDirectInput"' in html, "Missing #chalkboardDirectInput in HTML"
assert 'class="chalkboard-direct-textarea"' in html, "Missing .chalkboard-direct-textarea in HTML"

# 4. Eraser at bottom-right corner of tray (Request 3/4)
assert 'class="chalkboard-tray"' in html, "Missing .chalkboard-tray in HTML"
assert 'class="chalk-tray-eraser-btn"' in html, "Missing .chalk-tray-eraser-btn in HTML"
assert 'id="btnChalkEraser"' in html, "Missing #btnChalkEraser in HTML"
assert '擦黑板' in html, "Missing '擦黑板' in HTML"

# 5. Clean board: removed clutter requested by user
assert 'class="teacher-bubble"' not in html, "Dialogue bubble (.teacher-bubble) must be removed per user request"
assert 'teacherSpeechText' not in html, "teacherSpeechText must be removed per user request"
assert '✦ 史努比小讲堂 · 每日自学黑板报 ✦' not in html, "Title banner must be removed per user request"
assert 'class="chalk-actions-group"' not in html, "Top-right 4 action boxes must be removed per user request"
assert 'class="chalkboard-executive-bar"' not in html, "Bottom executive bar under board must be removed per user request"

print("✓ All static HTML assertions (clean blackboard, direct typing, border snoopy, bottom-right eraser, removals) verified!")

# JSC Functional Tests
script_start = html.find('<script>') + len('<script>')
script_end = html.rfind('</script>')
js_code = html[script_start:script_end]

jsc_header = """
const console = {
  log: print,
  error: print,
  warn: print
};
const window = {
  scrollTo: () => {},
  addEventListener: () => {},
  removeEventListener: () => {},
  location: { search: '' },
  navigator: {
    clipboard: {
      writeText: () => Promise.resolve()
    }
  },
  innerWidth: 1200,
  innerHeight: 800,
  scrollX: 0,
  scrollY: 0
};
function SpeechSynthesisUtterance(text) {
  this.text = text;
  this.lang = '';
  this.rate = 1;
}
const elements = {};
const document = {
  getElementById: (id) => {
    if (!elements[id]) {
      elements[id] = {
        id: id,
        value: '',
        textContent: '',
        innerHTML: '',
        style: { display: 'none' },
        classList: {
          _cls: new Set(),
          add: function(c) { this._cls.add(c); },
          remove: function(c) { this._cls.delete(c); },
          contains: function(c) { return this._cls.has(c); },
          toggle: function(c, v) { if (v) this._cls.add(c); else this._cls.delete(c); }
        },
        focus: () => {},
        querySelectorAll: () => [],
        appendChild: () => {}
      };
    }
    return elements[id];
  },
  querySelectorAll: (sel) => [],
  addEventListener: () => {},
  createElement: (tag) => {
    return {
      tagName: tag,
      style: {
        setProperty: () => {}
      },
      classList: {
        _cls: new Set(),
        add: function(c) { this._cls.add(c); },
        remove: function(c) { this._cls.delete(c); },
        contains: function(c) { return this._cls.has(c); }
      },
      appendChild: () => {},
      remove: () => {}
    };
  },
  body: {
    appendChild: () => {},
    classList: {
      _cls: new Set(),
      add: function(c) { this._cls.add(c); },
      remove: function(c) { this._cls.delete(c); },
      contains: function(c) { return this._cls.has(c); },
      toggle: function(c) {
        if (this._cls.has(c)) { this._cls.delete(c); return false; }
        else { this._cls.add(c); return true; }
      }
    }
  }
};
const localStorage = {
  _store: {},
  getItem: function(k) { return this._store[k] !== undefined ? this._store[k] : null; },
  setItem: function(k, v) { this._store[k] = String(v); },
  removeItem: function(k) { delete this._store[k]; },
  clear: function() { this._store = {}; }
};
const setTimeout = (fn, ms) => { if (!ms || ms <= 100) fn(); return 1; };
const clearTimeout = () => {};
const setInterval = (fn, ms) => 1;
const clearInterval = () => {};
const alert = (msg) => { print('ALERT: ' + msg); };
const confirm = (msg) => true;

function assertEq(actual, expected, msg) {
  if (actual !== expected) {
    throw new Error(`FAIL: ${msg} | Expected [${expected}], got [${actual}]`);
  }
}
"""

test_chalkboard_script = """
print('\\n--- 2. Testing Direct-Typing Chalkboard Engine in JSC ---');

// 1. Initial Render & Auto-seed
renderChalkboard();
const records = getData(STORAGE_KEYS.BLACKBOARD_RECORDS, {});
const todayStr = getTodayDateStr();
assertEq(!!records[todayStr], true, 'Today record should be automatically seeded if blank');

const textarea = document.getElementById('chalkboardDirectInput');
assertEq(textarea.value.indexOf('涉外排期要点') !== -1, true, 'Direct chalkboard textarea pre-populated with initial content');

// 2. Direct Typing on Blackboard
textarea.value = '• 今日英语单词：Nordic, Lagom, Fika\\n• 重点事项：跨时区会议对齐\\n“保持从容与好奇心！”';
handleDirectBlackboardInput();

const updatedRecords = getData(STORAGE_KEYS.BLACKBOARD_RECORDS, {});
assertEq(updatedRecords[todayStr].content.indexOf('Nordic') !== -1, true, 'Direct input saved directly to storage');
assertEq(updatedRecords[todayStr].notes.indexOf('Fika') !== -1, true, 'Notes field kept in sync');

// 3. Date Navigation (Yesterday / Tomorrow / Today)
changeBlackboardDayOffset(-1);
assertEq(currentBlackboardDate !== todayStr, true, 'Offset -1 should change blackboard date to yesterday');
assertEq(document.getElementById('btnChalkToday').style.display, 'inline-block', 'Today button visible when viewing past date');

jumpToTodayBlackboard();
assertEq(currentBlackboardDate, todayStr, 'jumpToToday returns to today');
assertEq(document.getElementById('btnChalkToday').style.display, 'none', 'Today button hidden when already on today');
assertEq(textarea.value.indexOf('Nordic') !== -1, true, 'Today board text restored on jump to today');

// 4. Border Snoopy Interaction (No speech bubble per user request "不需要点击出现话语")
interactBorderSnoopy();
assertEq(document.getElementById('snoopyLyingWrap').classList.contains('snoopy-nodding'), true, 'Nodding animation added to snoopy');

// 5. Erase Blackboard
eraseCurrentBlackboard();
const recordsAfterErase = getData(STORAGE_KEYS.BLACKBOARD_RECORDS, {});
assertEq(recordsAfterErase[todayStr].content, '', 'Erase clears today content string');
assertEq(textarea.value, '', 'Erase clears direct textarea value');

print('✓ Direct-typing Chalkboard all functional tests passed successfully 100%!');
"""

full_test_js = jsc_header + "\n" + js_code + "\n" + test_chalkboard_script
with open("scratch/test_chalkboard_runner.js", "w", encoding="utf-8") as f:
    f.write(full_test_js)

jsc_path = "/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
res = subprocess.run([jsc_path, "scratch/test_chalkboard_runner.js"], capture_output=True, text=True)
print("JSC STDOUT:\n" + res.stdout)
if res.stderr:
    print("JSC STDERR:\n" + res.stderr)
assert res.returncode == 0, f"JSC exited with code {res.returncode}"

print("ALL CHALKBOARD TESTS PASSED SUCCESSFULLY 100%!")

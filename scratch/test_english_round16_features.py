#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os

print("--- Testing Round 16: Daily English UI Streamlining & Snoopy Checkin Pill ---")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 划词即查 tip deleted per Request 1
assert '划词即查：在下方选中任意英文单词' not in html, "划词即查 tip must be deleted per Request 1"
print("✓ Request 1: '划词即查' prompt text successfully deleted")

# 2. English search input placeholder deleted per Request 2
assert 'placeholder="输入任意英文单词' not in html, "Search input placeholder must be deleted per Request 2"
assert 'id="englishSearchInput"' in html, "Missing #englishSearchInput in HTML"
print("✓ Request 2: English search box placeholder text successfully deleted")

# 3. Fire icon deleted from Daily English per Request 3
english_pane = html[html.find('id="pane-english"'):html.find('</main>')]
assert '🔥' not in english_pane, "Fire icon (🔥) must be deleted from Daily English pane per Request 3"
checkin_fn_js = html[html.find('function renderEnglishCheckinState'):html.find('function doEnglishCheckin')]
assert '🔥' not in checkin_fn_js, "Fire icon (🔥) must be deleted from checkin JS logic"
print("✓ Request 3: Fire icon (🔥) deleted from Daily English, replaced by Snoopy avatar/face")

# 4. Old separate checkin button deleted per Request 4
assert '🏆 今日学习完成 · 立即打卡' not in html, "Old separate checkin button must be deleted per Request 4"
print("✓ Request 4: Old '立即打卡' separate button successfully deleted")

# 5. Combined Snoopy checkin pill button per Request 5
assert 'class="snoopy-checkin-pill-btn"' in html, "Missing .snoopy-checkin-pill-btn in HTML"
assert 'id="btnEnglishCheckin"' in html, "Missing #btnEnglishCheckin in HTML"
assert 'id="snoopyCheckinAvatar"' in html, "Missing #snoopyCheckinAvatar in HTML"
assert 'id="englishStreakNum"' in html, "Missing #englishStreakNum in HTML"
assert 'id="englishCheckinActionText"' in html, "Missing #englishCheckinActionText in HTML"
print("✓ Request 5: Combined Snoopy streak & checkin pill button present in HTML")

# JSC Functional Test
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
    style: {{}},
    setAttribute: () => {{}},
    appendChild: () => {{}},
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
function showToast(msg) {{ print('Toast: ' + msg); }}
function openModal(id) {{ print('Modal opened: ' + id); }}

{js_code}

// Test initial unchecked state
localStorage.removeItem(STORAGE_KEYS.ENGLISH_CHECKIN);
renderEnglishCheckinState();
const streakEl = document.getElementById('englishStreakNum');
const actionEl = document.getElementById('englishCheckinActionText');
const btnEl = document.getElementById('btnEnglishCheckin');
const avatarEl = document.getElementById('snoopyCheckinAvatar');

if (streakEl.textContent !== '0 天') {{
  throw new Error('Initial streak should be 0 天, got: ' + streakEl.textContent);
}}
if (streakEl.textContent.includes('🔥')) {{
  throw new Error('Streak should NOT contain fire icon');
}}
const actionContent = actionEl.innerHTML || actionEl.textContent;
if (!actionContent.includes('点击打卡')) {{
  throw new Error('Action text should invite user to check in, got: ' + actionContent);
}}
if (btnEl.classList.contains('is-checked')) {{
  throw new Error('Button should not be is-checked initially');
}}
print('✓ Initial unchecked state verified: 0 天, no fire, calls for check in');

// Test performing check in
doEnglishCheckin();
if (streakEl.textContent !== '1 天') {{
  throw new Error('Streak after checkin should be 1 天, got: ' + streakEl.textContent);
}}
if (!btnEl.classList.contains('is-checked')) {{
  throw new Error('Button should have is-checked class after checkin');
}}
const checkedActionContent = actionEl.innerHTML || actionEl.textContent;
if (!checkedActionContent.includes('已打卡')) {{
  throw new Error('Action text should say 已打卡, got: ' + checkedActionContent);
}}
print('✓ Checked-in state verified: 1 天, is-checked active, action text shows 已打卡');

// Test duplicate check in on same day
doEnglishCheckin();
if (streakEl.textContent !== '1 天') {{
  throw new Error('Duplicate checkin should not increment streak further');
}}
print('✓ Duplicate check-in gracefully prevented');
"""

jsc_path = '/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
temp_file = 'scratch/test_round16_jsc.js'
with open(temp_file, 'w', encoding='utf-8') as f:
    f.write(jsc_code)

proc = subprocess.run([jsc_path, temp_file], capture_output=True, text=True)
print(proc.stdout)
if proc.returncode != 0:
    print(proc.stderr)
    raise AssertionError(f"JSC execution failed with code {proc.returncode}")

print("==========================================================")
print("ALL ROUND 16 DAILY ENGLISH STREAMLINING TESTS PASSED 100%!")
print("==========================================================")

# -*- coding: utf-8 -*-
import json
import re
import subprocess
import os

print("--- Testing English Word Selection & Pronunciation Module ---")

# 1. Static HTML verification
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

assert 'id="wordLookupPopup"' in html, "Missing #wordLookupPopup container"
assert 'id="wordPopupTitle"' in html, "Missing #wordPopupTitle"
assert 'id="wordPopupPhonetic"' in html, "Missing #wordPopupPhonetic"
assert 'id="wordPopupPos"' in html, "Missing #wordPopupPos"
assert 'id="wordPopupSpeakBtn"' in html, "Missing #wordPopupSpeakBtn"
assert 'id="wordPopupDef"' in html, "Missing #wordPopupDef"
assert 'id="englishSearchInput"' in html, "Missing #englishSearchInput search bar"
assert 'speakLookupWord()' in html, "Missing speakLookupWord() call"
assert 'handleSelectionLookup' in html, "Missing handleSelectionLookup"
assert 'findWordInDict' in html, "Missing findWordInDict function"
assert 'cleanLookupWord' in html, "Missing cleanLookupWord function"
assert 'const NORDIC_DICT = ' in html, "Missing bundled NORDIC_DICT in index.html"

print("✓ Static HTML and CSS assertions for English Word Selection & Lookup passed!")

# 2. Functional JS execution via macOS JSC
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
assert script_match, "No script found in index.html"
js_code = script_match.group(1)

test_jsc = f"""
const console = {{ log: (s) => print(s), error: (s) => print(s), warn: (s) => print(s) }};
let speakCalledWith = null;
const window = {{
  addEventListener: () => {{}},
  speechSynthesis: {{
    cancel: () => {{}},
    speak: (u) => {{ speakCalledWith = u.text; }}
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
        offsetWidth: 260,
        offsetHeight: 90,
        focus: () => {{}},
        querySelectorAll: () => [],
        getBoundingClientRect: () => ({{ left: 100, top: 200, width: 80, height: 20, right: 180, bottom: 220 }})
      }};
    }}
    return elements[id];
  }},
  addEventListener: () => {{}}
}};
const localStorage = {{
  _store: {{}},
  getItem: (k) => localStorage._store[k] || null,
  setItem: (k, v) => {{ localStorage._store[k] = String(v); }},
  removeItem: (k) => {{ delete localStorage._store[k]; }}
}};
function showToast(msg) {{}}
const setInterval = () => 1;
const clearInterval = () => {{}};
const setTimeout = (fn) => {{ if (typeof fn === 'function') fn(); return 1; }};
const clearTimeout = () => {{}};

{js_code}

function assert(condition, message) {{
  if (!condition) throw new Error('ASSERTION FAILED: ' + message);
}}

print('Testing NORDIC_DICT entries count...');
const dictKeys = Object.keys(NORDIC_DICT);
print('NORDIC_DICT keys length: ' + dictKeys.length);
assert(dictKeys.length >= 1000, 'Expected at least 1000 words in NORDIC_DICT, found: ' + dictKeys.length);

print('Testing cleanLookupWord...');
assert(cleanLookupWord('"sauna,"') === 'sauna', 'cleanLookupWord failed for punctuation');
assert(cleanLookupWord('“Fika”') === 'Fika', 'cleanLookupWord failed for curly quotes');
assert(cleanLookupWord('Löyly!') === 'Löyly', 'cleanLookupWord failed for Nordic chars');
assert(cleanLookupWord('dalahäst.') === 'dalahäst', 'cleanLookupWord failed for dalahäst');
assert(cleanLookupWord('  aurora borealis  ') === 'aurora borealis', 'cleanLookupWord failed for phrase');

print('Testing findWordInDict...');
const fikaEntry = findWordInDict('fika');
assert(fikaEntry && fikaEntry.d.indexOf('咖啡') !== -1, 'findWordInDict failed for fika');

const saunaEntry = findWordInDict('Sauna');
assert(saunaEntry && saunaEntry.d.indexOf('桑拿') !== -1, 'findWordInDict failed for uppercase Sauna');

const auroraEntry = findWordInDict('Aurora Borealis');
assert(auroraEntry && auroraEntry.d.indexOf('极光') !== -1, 'findWordInDict failed for Aurora Borealis');

// Stemming tests
const fjordPlural = findWordInDict('fjords');
assert(fjordPlural && fjordPlural.d.indexOf('峡湾') !== -1, 'Lemmatization failed for fjords');

const hikedPast = findWordInDict('hiked');
assert(hikedPast && hikedPast.d.indexOf('徒步') !== -1, 'Lemmatization failed for hiked');

const dancingCont = findWordInDict('dancing');
assert(dancingCont && dancingCont.d.indexOf('跳舞') !== -1, 'Lemmatization failed for dancing');

print('Testing showWordLookupPopup and speech playback...');
const mockRect = {{ left: 200, top: 300, width: 60, height: 20, right: 260, bottom: 320 }};
showWordLookupPopup('fika', mockRect);

const popup = document.getElementById('wordLookupPopup');
assert(popup.style.display === 'block', 'Popup did not display');
assert(document.getElementById('wordPopupTitle').textContent === 'Fika', 'Popup title not set correctly');
assert(document.getElementById('wordPopupDef').textContent.indexOf('咖啡') !== -1, 'Popup def not set correctly');

// Test speakLookupWord
speakLookupWord();
assert(speakCalledWith === 'fika', 'speakLookupWord failed to call speechSynthesis with fika, got: ' + speakCalledWith);

// Test searchEnglishWord
const searchInput = document.getElementById('englishSearchInput');
searchInput.value = 'avanto';
searchEnglishWord();
assert(document.getElementById('wordPopupTitle').textContent === 'Avanto', 'Search did not show Avanto');
speakLookupWord();
assert(speakCalledWith === 'avanto', 'Speech failed after search for avanto');

print('✓ All JSC unit tests for Word Selection, Dictionary & Speech passed 100%!');
"""

with open("scratch/test_word_lookup_jsc.js", "w", encoding="utf-8") as f:
    f.write(test_jsc)

jsc_path = "/System/Volumes/Preboot/Cryptexes/OS/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
res = subprocess.run([jsc_path, "scratch/test_word_lookup_jsc.js"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
assert res.returncode == 0, f"JSC test runner failed with code {res.returncode}"

print("=================================================================")
print("ALL ENGLISH WORD SELECTION & PRONUNCIATION TESTS PASSED 100%!")
print("=================================================================")

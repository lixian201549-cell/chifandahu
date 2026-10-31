import subprocess
import os

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("--- Testing HTML Static Assertions for New Home Cockpit ---")
assert 'class="home-cockpit-grid"' in html, "Missing .home-cockpit-grid in HTML"
assert 'id="homeLeaderTripCard"' in html, "Missing #homeLeaderTripCard in HTML"
assert 'id="homeLeaderTripBody"' in html, "Missing #homeLeaderTripBody in HTML"
assert 'id="homeTodayAgendaCard"' in html, "Missing #homeTodayAgendaCard in HTML"
assert 'id="homeTodayAgendaList"' in html, "Missing #homeTodayAgendaList in HTML"
assert 'id="homeTodayAgendaBadge"' in html, "Missing #homeTodayAgendaBadge in HTML"
assert 'id="homeTodayFocusCard"' in html, "Missing #homeTodayFocusCard in HTML"
assert 'id="homeTodayFocusList"' in html, "Missing #homeTodayFocusList in HTML"

assert 'id="homeNordicCountdownCard"' in html, "Missing #homeNordicCountdownCard in HTML"
assert 'id="homeNordicCountdownBody"' in html, "Missing #homeNordicCountdownBody in HTML"
assert 'id="homeNordicBucketCard"' in html, "Missing #homeNordicBucketCard in HTML"
assert 'id="homeBucketList"' in html, "Missing #homeBucketList in HTML"
assert 'id="homeBucketProgressBadge"' in html, "Missing #homeBucketProgressBadge in HTML"
assert 'id="homeBucketProgressBar"' in html, "Missing #homeBucketProgressBar in HTML"
assert 'id="homeNordicTipsCard"' in html, "Missing #homeNordicTipsCard in HTML"
assert 'id="homeNordicTipsBody"' in html, "Missing #homeNordicTipsBody in HTML"
assert 'id="addBucketItemModal"' in html, "Missing #addBucketItemModal in HTML"
assert 'id="inputBucketItemText"' in html, "Missing #inputBucketItemText in HTML"

print("✓ All static Home Cockpit containers, cards, and modal found!")

# JSC Unit Tests for Home Cockpit
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
        querySelectorAll: () => []
      };
    }
    return elements[id];
  },
  querySelectorAll: (sel) => [],
  addEventListener: () => {},
  body: {
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
  getItem: function(k) { return this._store[k] || null; },
  setItem: function(k, v) { this._store[k] = v; },
  removeItem: function(k) { delete this._store[k]; }
};
const confirm = () => true;
let toasts = [];
const setInterval = () => 1;
const setTimeout = () => 1;
const clearTimeout = () => {};
"""

jsc_footer = """
function assertEq(act, exp, msg) {
  if (act !== exp) {
    throw new Error('FAIL: ' + msg + ' -> expected: ' + exp + ', actual: ' + act);
  }
}

print("--- Testing Home Dashboard Rendering ---");
renderHomeDashboard();

// 1. Leader Trip Card
const leaderBodyHtml = elements['homeLeaderTripBody'].innerHTML;
assertEq(leaderBodyHtml.includes('开罗常驻总部') || leaderBodyHtml.includes('领导出差中'), true, 'Leader status rendered');
print("✓ Leader status rendered successfully: " + (leaderBodyHtml.includes('开罗常驻总部') ? '开罗常驻' : '出差中'));

// 2. Today Agenda Timeline
const agendaHtml = elements['homeTodayAgendaList'].innerHTML;
assertEq(agendaHtml.length > 0, true, 'Today agenda timeline rendered');
print("✓ Today agenda timeline rendered");

// 3. Today Focus Q1
const focusHtml = elements['homeTodayFocusList'].innerHTML;
assertEq(focusHtml.includes('Q1 必须搞定') || focusHtml.includes('已达成'), true, 'Today Q1 focus rendered');
print("✓ Today Q1 focus rendered");

// 4. 2027 Nordic Countdown
const countdownHtml = elements['homeNordicCountdownBody'].innerHTML;
assertEq(countdownHtml.includes('DAYS') && countdownHtml.includes('2027'), true, '2027 countdown rendered');
print("✓ 2027 Nordic countdown rendered");

// 5. Nordic Bucket List
const bucketListHtml = elements['homeBucketList'].innerHTML;
assertEq(bucketListHtml.includes('欧若拉北极光'), true, 'Aurora borealis bucket item rendered');
assertEq(bucketListHtml.includes('Fika'), true, 'Fika bucket item rendered');
const progressText = elements['homeBucketProgressBadge'].textContent;
assertEq(progressText.includes('已点亮'), true, 'Bucket progress badge rendered');
print("✓ Nordic bucket list rendered with progress: " + progressText);

// 6. Test Bucket List Toggle & Add & Delete
const curItems = getData(STORAGE_KEYS.NORDIC_BUCKET_LIST);
assertEq(curItems.length, 8, '8 initial Nordic bucket list items');
toggleBucketItem(1);
const toggledItems = getData(STORAGE_KEYS.NORDIC_BUCKET_LIST);
assertEq(toggledItems[0].checked, true, 'Item 1 checked after toggle');
assertEq(elements['homeBucketProgressBadge'].textContent, '1 / 8 已点亮', 'Progress updated to 1 / 8');

// Add item
document.getElementById('inputBucketItemText').value = '在冰岛看玄武岩黑沙滩海浪';
saveNewBucketItem();
const afterAddItems = getData(STORAGE_KEYS.NORDIC_BUCKET_LIST);
assertEq(afterAddItems.length, 9, '9 items after adding new wish');
assertEq(elements['homeBucketProgressBadge'].textContent, '1 / 9 已点亮', 'Progress updated to 1 / 9');

// Delete item
deleteBucketItem(afterAddItems[8].id);
const afterDelItems = getData(STORAGE_KEYS.NORDIC_BUCKET_LIST);
assertEq(afterDelItems.length, 8, '8 items after deletion');
print("✓ Bucket list interactive toggle, add, and delete operations verified 100%!");

// 7. Nordic Tips
const tipHtml = elements['homeNordicTipsBody'].innerHTML;
assertEq(tipHtml.includes('极地三层穿衣法则') || tipHtml.includes('北欧'), true, 'Nordic travel tip rendered');
cycleNordicTip();
const nextTipHtml = elements['homeNordicTipsBody'].innerHTML;
assertEq(nextTipHtml.length > 0, true, 'Cycled to next tip');
print("✓ Nordic travel tips and cycling verified!");

print("==================================================");
print("ALL HOME COCKPIT TESTS PASSED 100%!");
print("==================================================");
"""

full_code = jsc_header + "\n" + js_code + "\n" + jsc_footer
with open("scratch/test_home_cockpit.js", "w", encoding="utf-8") as f:
    f.write(full_code)

res = subprocess.run(["/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc", "scratch/test_home_cockpit.js"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)
assert res.returncode == 0, "JSC tests failed!"
print("ALL NEW HOME COCKPIT TESTS PASSED!")

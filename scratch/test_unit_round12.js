// Unit test suite for Round 12 requirements:
// 1. Quick duration chips (30, 40, 60, 90, 120) restored and functional
// 2. Reporter (汇报人) is optional (not required)
// 3. Start time & End time support both manual typing and dropdown selection

const fs = require('fs');

// Simple DOM Mock for jsc / node
class ClassList {
  constructor() { this.classes = new Set(); }
  add(c) { this.classes.add(c); }
  remove(c) { this.classes.delete(c); }
  contains(c) { return this.classes.has(c); }
  toggle(c, force) {
    if (force !== undefined) {
      if (force) this.classes.add(c);
      else this.classes.delete(c);
      return force;
    }
    if (this.classes.has(c)) { this.classes.delete(c); return false; }
    this.classes.add(c); return true;
  }
}

class MockElement {
  constructor(id, tag = 'div') {
    this.id = id;
    this.tagName = tag.toUpperCase();
    this.value = '';
    this.textContent = '';
    this.innerHTML = '';
    this.classList = new ClassList();
    this.children = [];
    this.options = [];
    this.style = {};
    this.required = false;
  }
  focus() { this.focused = true; }
  getAttribute(a) { return this[a] || null; }
  setAttribute(a, v) { this[a] = v; }
}

const elements = {};
function getEl(id) {
  if (!elements[id]) {
    elements[id] = new MockElement(id);
  }
  return elements[id];
}

globalThis.document = {
  getElementById: (id) => getEl(id),
  querySelectorAll: (sel) => {
    if (sel === '.time-dropdown-select') {
      return [getEl('sel1'), getEl('sel2')];
    }
    if (sel.includes('.filter-btn')) return [];
    return [];
  },
  body: new MockElement('body')
};

globalThis.window = {
  addEventListener: () => {}
};

let toasts = [];
globalThis.showToast = (msg) => { toasts.push(msg); };

let storage = {};
globalThis.localStorage = {
  getItem: (k) => storage[k] || null,
  setItem: (k, v) => { storage[k] = v; }
};

globalThis.STORAGE_KEYS = {
  MEETINGS: 'meetings',
  THEME: 'theme'
};

globalThis.getData = (k) => JSON.parse(storage[k] || '[]');
globalThis.setData = (k, v) => { storage[k] = JSON.stringify(v); };
globalThis.selectedTimelineDate = '2026-09-24';
globalThis.openModal = () => {};
globalThis.closeModal = () => {};
globalThis.renderMeetings = () => {};

// Read and extract functions from assemble_final_app.py or index.html
const html = fs.readFileSync('index.html', 'utf8');

// Verify DOM structure in index.html
console.log('--- Testing HTML static assertions ---');
if (!html.includes('id="durChip30"') || !html.includes('id="durChip40"') || 
    !html.includes('id="durChip60"') || !html.includes('id="durChip90"') || 
    !html.includes('id="durChip120"')) {
  throw new Error('Duration chip buttons (30/40/60/90/120) missing in HTML!');
}
console.log('✓ All 5 duration chips (30, 40, 60, 90, 120) present in HTML');

if (html.includes('id="inputMeetingReporter" placeholder="请填写汇报人" required') ||
    html.includes('id="inputMeetingReporter" placeholder="选填，如：张总、李部长、王经理..." required')) {
  throw new Error('Reporter field should NOT be marked required!');
}
console.log('✓ 汇报人 (Reporter) input is not marked required');

if (!html.includes('class="time-combobox"')) {
  throw new Error('time-combobox wrapper missing in HTML!');
}
console.log('✓ time-combobox present for start and end time');

// Extract script content
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) throw new Error('No script block found in index.html');
const script = scriptMatch[1];

// Evaluate the script functions in our environment
eval(script);

console.log('--- Testing normalizeTimeStr ---');
assertEq(normalizeTimeStr('9:30'), '09:30', '9:30 -> 09:30');
assertEq(normalizeTimeStr('09:30'), '09:30', '09:30 -> 09:30');
assertEq(normalizeTimeStr('9'), '09:00', '9 -> 09:00');
assertEq(normalizeTimeStr('14'), '14:00', '14 -> 14:00');
assertEq(normalizeTimeStr('930'), '09:30', '930 -> 09:30');
assertEq(normalizeTimeStr('1015'), '10:15', '1015 -> 10:15');
assertEq(normalizeTimeStr('9：30'), '09:30', '9：30 (Chinese colon) -> 09:30');
assertEq(normalizeTimeStr('9.30'), '09:30', '9.30 -> 09:30');
console.log('✓ All time string normalizations passed');

console.log('--- Testing Quick Duration Options ---');
openAddMeetingModal();
// Default start is 10:00
assertEq(getEl('inputMeetingStartTime').value, '10:00', 'Default start time is 10:00');

applyQuickDuration(30);
assertEq(getEl('inputMeetingEndTime').value, '10:30', 'Duration 30 sets 10:30');
assertEq(getEl('durChip30').classList.contains('selected'), true, 'durChip30 is selected');
assertEq(getEl('durChip40').classList.contains('selected'), false, 'durChip40 is NOT selected');

applyQuickDuration(40);
assertEq(getEl('inputMeetingEndTime').value, '10:40', 'Duration 40 sets 10:40');
assertEq(getEl('durChip40').classList.contains('selected'), true, 'durChip40 is selected');
assertEq(getEl('durChip30').classList.contains('selected'), false, 'durChip30 is NOT selected');

applyQuickDuration(60);
assertEq(getEl('inputMeetingEndTime').value, '11:00', 'Duration 60 sets 11:00');
assertEq(getEl('durChip60').classList.contains('selected'), true, 'durChip60 is selected');

applyQuickDuration(90);
assertEq(getEl('inputMeetingEndTime').value, '11:30', 'Duration 90 sets 11:30');
assertEq(getEl('durChip90').classList.contains('selected'), true, 'durChip90 is selected');

applyQuickDuration(120);
assertEq(getEl('inputMeetingEndTime').value, '12:00', 'Duration 120 sets 12:00');
assertEq(getEl('durChip120').classList.contains('selected'), true, 'durChip120 is selected');
console.log('✓ Quick duration 30, 40, 60, 90, 120 all passed');

console.log('--- Testing Dropdown selection (applyTimeSelect) ---');
applyTimeSelect('start', '14:30');
assertEq(getEl('inputMeetingStartTime').value, '14:30', 'Start time updated from dropdown');
applyQuickDuration(30);
assertEq(getEl('inputMeetingEndTime').value, '15:00', 'End time 15:00 based on 14:30 + 30');
console.log('✓ Dropdown selection test passed');

console.log('--- Testing saveMeeting with empty 汇报人 (Reporter optional) ---');
openAddMeetingModal();
getEl('inputMeetingDate').value = '2026-09-24';
getEl('inputMeetingStartTime').value = '10:00';
getEl('inputMeetingEndTime').value = '10:45';
getEl('inputMeetingSubject').value = '中东北非区域例会';
getEl('inputMeetingReporter').value = ''; // LEFT EMPTY INTENTIONALLY!

toasts = [];
saveMeeting();
const savedMeetings = getData(STORAGE_KEYS.MEETINGS);
if (savedMeetings.length === 0) {
  throw new Error('Meeting failed to save when reporter is empty! Toast: ' + toasts.join(', '));
}
assertEq(savedMeetings[0].subject, '中东北非区域例会', 'Meeting subject matches');
assertEq(savedMeetings[0].reporter, '', 'Reporter saved as empty string');
assertEq(toasts.includes('会议预约已成功登记'), true, 'Success toast displayed');
console.log('✓ Successfully saved meeting without reporter (reporter is optional)');

console.log('--- Testing saveMeeting mandatory subject check ---');
openAddMeetingModal();
getEl('inputMeetingDate').value = '2026-09-24';
getEl('inputMeetingStartTime').value = '10:00';
getEl('inputMeetingEndTime').value = '10:45';
getEl('inputMeetingSubject').value = ''; // EMPTY SUBJECT
toasts = [];
saveMeeting();
assertEq(toasts.includes('请填写会议主题'), true, 'Subject is still mandatory');
console.log('✓ Subject remains properly mandatory');

console.log('\n=========================================');
console.log('ALL ROUND 12 TESTS PASSED PERFECTLY!');
console.log('=========================================\n');

function assertEq(actual, expected, msg) {
  if (actual !== expected) {
    throw new Error(`FAIL: ${msg} -> expected "${expected}", got "${actual}"`);
  }
}

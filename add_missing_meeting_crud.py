with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = "function editMeeting(id) {"
crud_code = """function openAddMeetingModal() {
  document.getElementById('meetingModalTitle').textContent = '➕ 登记主管会议预约';
  document.getElementById('inputMeetingId').value = '';
  document.getElementById('inputMeetingDate').value = selectedTimelineDate || new Date().toISOString().slice(0, 10);
  document.getElementById('inputMeetingTime').value = '10:00';
  document.getElementById('inputMeetingDuration').value = '45';
  document.getElementById('inputMeetingSubject').value = '';
  document.getElementById('inputMeetingBackground').value = '';
  document.getElementById('inputMeetingDecision').value = '1. \\\\n2. ';
  if (document.getElementById('inputMeetingReporter')) document.getElementById('inputMeetingReporter').value = '';
  if (document.getElementById('inputMeetingMinuter')) document.getElementById('inputMeetingMinuter').value = '王秘书';
  document.getElementById('inputMeetingAttendees').value = '主管、';
  document.getElementById('inputMeetingRequester').value = '';
  document.getElementById('inputMeetingLocation').value = '主管办公室';
  document.getElementById('selectMeetingStatus').value = 'scheduled';
  document.getElementById('selectMeetingPriority').value = 'medium';
  document.getElementById('inputMeetingNotes').value = '';
  setMeetingDuration(45);
  openModal('meetingModal');
}

function setMeetingDuration(mins) {
  document.getElementById('inputMeetingDuration').value = mins;
  document.querySelectorAll('.duration-chips .chip-btn').forEach(b => {
    b.classList.toggle('selected', b.textContent.includes(mins + '分'));
  });
}

function saveMeeting() {
  const id = document.getElementById('inputMeetingId').value;
  const date = document.getElementById('inputMeetingDate').value;
  const time = document.getElementById('inputMeetingTime').value;
  const duration = parseInt(document.getElementById('inputMeetingDuration').value, 10) || 45;
  const subject = document.getElementById('inputMeetingSubject').value.trim();
  const background = document.getElementById('inputMeetingBackground').value.trim();
  const decision = document.getElementById('inputMeetingDecision').value.trim();
  const reporter = document.getElementById('inputMeetingReporter') ? document.getElementById('inputMeetingReporter').value.trim() : '';
  const minuter = document.getElementById('inputMeetingMinuter') ? document.getElementById('inputMeetingMinuter').value.trim() : '秘书处';
  const attendees = document.getElementById('inputMeetingAttendees').value.trim();
  const requester = document.getElementById('inputMeetingRequester').value.trim();
  const location = document.getElementById('inputMeetingLocation').value.trim();
  const status = document.getElementById('selectMeetingStatus').value;
  const priority = document.getElementById('selectMeetingPriority').value;
  const notes = document.getElementById('inputMeetingNotes').value.trim();

  let meetings = getData(STORAGE_KEYS.MEETINGS);
  const durHours = (duration / 60).toFixed(2);

  if (id) {
    meetings = meetings.map(m => m.id == id ? {
      ...m,
      date, time, duration, durationHours: durHours,
      subject, background, decision,
      reporter, minuter, attendees, requester, location,
      status, priority, notes
    } : m);
    showToast('✏️ 会议预约已更新！');
  } else {
    meetings.unshift({
      id: Date.now(),
      date, time, duration, durationHours: durHours,
      subject, background, decision,
      reporter, minuter, attendees, requester, location,
      status, priority, notes
    });
    showToast('➕ 会议预约已成功登记！');
  }

  setData(STORAGE_KEYS.MEETINGS, meetings);
  closeModal('meetingModal');
  renderMeetings();
}

"""

if target in text:
    text = text.replace(target, crud_code + target, 1)
    with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("CRUD functions added successfully.")
else:
    print("WARNING: target not found!")

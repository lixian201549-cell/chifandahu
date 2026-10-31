# update_round11_safe.py
# Applies all requested form updates safely using string find and replace

with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for .quick-suggest-chips, .suggest-chip if not already present
chip_css = """  .quick-suggest-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 6px;
  }
  .suggest-chip {
    display: inline-flex;
    align-items: center;
    border: 1px dashed var(--border);
    background: #fafaf9;
    padding: 2px 8px;
    font-size: 11px;
    color: var(--text-secondary);
    border-radius: 4px;
    cursor: pointer;
    user-select: none;
    transition: all 0.15s ease;
  }
  .suggest-chip:hover {
    background: #eff6ff;
    border-color: var(--blue-accent);
    color: var(--blue-accent);
    border-style: solid;
    transform: translateY(-1px);
  }
  .suggest-chip:active {
    transform: translateY(0);
  }"""

if ".quick-suggest-chips {" not in content:
    content = content.replace("  .duration-chips {", chip_css + "\n  .duration-chips {")
    print("✓ Added quick-suggest-chips CSS")

# 2. Check if meeting form was already replaced or needs replacing
form_needle = '<form id="meetingForm"'
if 'id="inputMeetingStartTime"' not in content:
    idx_start = content.find('<form id="meetingForm"')
    idx_end = content.find('</form>', idx_start) + len('</form>')
    if idx_start != -1 and idx_end != -1:
        new_form_html = """<form id="meetingForm" onsubmit="event.preventDefault(); saveMeeting();">
          <input type="hidden" id="inputMeetingId" value="" />

          <!-- 1. 会议时间: 日期、开始时间、结束时间 (必须) -->
          <div class="form-row">
            <div class="form-group" style="flex: 1.2;">
              <label>会议日期 *</label>
              <input type="date" id="inputMeetingDate" required />
            </div>
            <div class="form-group" style="flex: 1;">
              <label>开始时间 *</label>
              <input type="time" id="inputMeetingStartTime" onchange="handleMeetingTimeChange('start')" required />
            </div>
            <div class="form-group" style="flex: 1;">
              <label>结束时间 *</label>
              <input type="time" id="inputMeetingEndTime" onchange="handleMeetingTimeChange('end')" required />
            </div>
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:-4px; margin-bottom:14px; flex-wrap:wrap; gap:8px;">
            <div class="duration-quick-chips" style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
              <span style="font-size:11.5px; color:var(--text-muted);">快捷时长：</span>
              <span class="chip-btn" onclick="applyQuickDuration(15)">15分</span>
              <span class="chip-btn" onclick="applyQuickDuration(30)">30分</span>
              <span class="chip-btn selected" id="chipDur45" onclick="applyQuickDuration(45)">45分</span>
              <span class="chip-btn" onclick="applyQuickDuration(60)">1小时</span>
              <span class="chip-btn" onclick="applyQuickDuration(90)">1.5小时</span>
              <span class="chip-btn" onclick="applyQuickDuration(120)">2小时</span>
            </div>
            <div id="meetingDurationBadge" style="font-size:12px; font-weight:700; color:var(--blue-accent); background:var(--blue-soft); padding:3px 10px; border-radius:12px;">
              时长：45 分钟 (0.75H)
            </div>
          </div>

          <!-- 2. 会议主题 (必须) -->
          <div class="form-group">
            <label>会议主题 *</label>
            <input type="text" id="inputMeetingSubject" placeholder="请填写会议主题 / 关键任务..." required />
          </div>

          <!-- 3. 汇报人 (必须) -->
          <div class="form-group">
            <label>汇报人 *</label>
            <input type="text" id="inputMeetingReporter" placeholder="请填写汇报人（如：张总、李部长、王经理...）" required />
          </div>

          <!-- 4. 会议地点 (选填，提供快捷选项) -->
          <div class="form-group">
            <label>会议地点 / 线上会议号</label>
            <input type="text" id="inputMeetingLocation" placeholder="选填，可直接手动输入或点击下方常用地点快速填入" />
            <div class="quick-suggest-chips">
              <span class="suggest-chip" onclick="quickFillLocation('主管办公室')">主管办公室</span>
              <span class="suggest-chip" onclick="quickFillLocation('1号会议室')">1号会议室</span>
              <span class="suggest-chip" onclick="quickFillLocation('2号会议室')">2号会议室</span>
              <span class="suggest-chip" onclick="quickFillLocation('线上 WeLink')">线上 WeLink</span>
              <span class="suggest-chip" onclick="quickFillLocation('客户现场')">客户现场</span>
            </div>
          </div>

          <!-- 5. 纪要人 (选填，提供快捷选项) -->
          <div class="form-group">
            <label>纪要人</label>
            <input type="text" id="inputMeetingMinuter" placeholder="选填，负责会后输出纪要的人员" />
            <div class="quick-suggest-chips">
              <span class="suggest-chip" onclick="quickFillMinuter('王秘书')">王秘书</span>
              <span class="suggest-chip" onclick="quickFillMinuter('李秘书')">李秘书</span>
              <span class="suggest-chip" onclick="quickFillMinuter('汇报人自记')">汇报人自记</span>
            </div>
          </div>

          <!-- 6. 参会人 (选填，提供快捷选项) -->
          <div class="form-group">
            <label>参会人</label>
            <input type="text" id="inputMeetingAttendees" placeholder="选填，多参会人以顿号分隔" />
            <div class="quick-suggest-chips">
              <span class="suggest-chip" onclick="appendAttendee('主管')">+ 主管</span>
              <span class="suggest-chip" onclick="appendAttendee('财务BP')">+ 财务BP</span>
              <span class="suggest-chip" onclick="appendAttendee('HRG')">+ HRG</span>
              <span class="suggest-chip" onclick="appendAttendee('法务BP')">+ 法务BP</span>
              <span class="suggest-chip" onclick="appendAttendee('交付部')">+ 交付部</span>
              <span class="suggest-chip" onclick="appendAttendee('商务部')">+ 商务部</span>
            </div>
          </div>

          <!-- 7. 会议背景 (选填) -->
          <div class="form-group">
            <label>会议背景</label>
            <textarea id="inputMeetingBackground" rows="2" placeholder="选填，简述会议的触发背景、当前现状或关键信息..."></textarea>
          </div>

          <!-- 8. 核心决策点 (选填) -->
          <div class="form-group">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <label>核心决策点 (待主管定夺事项)</label>
              <button type="button" class="btn btn-sm btn-ghost" style="font-size:11px; padding:1px 6px;" onclick="insertDecisionTemplate()">+ 插入 1. 2. 序号模板</button>
            </div>
            <textarea id="inputMeetingDecision" rows="2" placeholder="选填，待主管拍板定夺的核心决议事项..."></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>预约人 / 部门</label>
              <input type="text" id="inputMeetingRequester" placeholder="选填，发起预约的人员或部门" />
            </div>
            <div class="form-group">
              <label>预约状态</label>
              <select id="selectMeetingStatus">
                <option value="scheduled" selected>已排期 (时间已敲定)</option>
                <option value="pending">待安排 (待主管确认时间)</option>
                <option value="completed">会议已完成</option>
                <option value="cancelled">已取消 / 延期</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>紧急程度</label>
              <select id="selectMeetingPriority">
                <option value="medium" selected>常规业务 (日常协同)</option>
                <option value="high">紧急决议 (重大事项/风险)</option>
                <option value="routine">例行汇报 (例会/周期进展)</option>
              </select>
            </div>
            <div class="form-group">
              <label>秘书工作备忘 (仅秘书可见)</label>
              <input type="text" id="inputMeetingNotes" placeholder="选填，如：提前10分钟打印材料..." />
            </div>
          </div>
        </form>"""
        content = content[:idx_start] + new_form_html + content[idx_end:]
        print("✓ Replaced meeting form HTML safely")
else:
    print("✓ meeting form HTML already updated")

# 3. Replace openAddMeetingModal, saveMeeting, editMeeting, setMeetingDuration
idx_func_start = content.find('function openAddMeetingModal() {')
idx_func_end_marker = "openModal('meetingModal');\n}"
idx_func_end = content.find(idx_func_end_marker, idx_func_start)
if idx_func_start != -1 and idx_func_end != -1:
    idx_func_end += len(idx_func_end_marker)
    new_modal_funcs = """// Time & Duration Calculation Helpers
function calculateEndTime(startTimeStr, durationMins) {
  if (!startTimeStr) return '';
  const [h, m] = startTimeStr.split(':').map(Number);
  const totalMins = h * 60 + m + parseInt(durationMins || 45, 10);
  const eh = Math.floor(totalMins / 60) % 24;
  const em = totalMins % 60;
  return `${String(eh).padStart(2, '0')}:${String(em).padStart(2, '0')}`;
}

function calculateDurationFromRange(startTimeStr, endTimeStr) {
  if (!startTimeStr || !endTimeStr) return 45;
  const [sh, sm] = startTimeStr.split(':').map(Number);
  const [eh, em] = endTimeStr.split(':').map(Number);
  let diff = (eh * 60 + em) - (sh * 60 + sm);
  if (diff <= 0) diff += 24 * 60; // if spans midnight
  return diff;
}

function handleMeetingTimeChange(type) {
  const startVal = document.getElementById('inputMeetingStartTime').value;
  const endVal = document.getElementById('inputMeetingEndTime').value;
  if (!startVal) return;

  if (type === 'start') {
    if (!endVal || endVal <= startVal) {
      document.getElementById('inputMeetingEndTime').value = calculateEndTime(startVal, 45);
    }
  }
  updateMeetingDurationBadge();
}

function applyQuickDuration(mins) {
  const startVal = document.getElementById('inputMeetingStartTime').value || '10:00';
  document.getElementById('inputMeetingStartTime').value = startVal;
  document.getElementById('inputMeetingEndTime').value = calculateEndTime(startVal, mins);
  updateMeetingDurationBadge();
}

function updateMeetingDurationBadge() {
  const startVal = document.getElementById('inputMeetingStartTime') ? document.getElementById('inputMeetingStartTime').value : '';
  const endVal = document.getElementById('inputMeetingEndTime') ? document.getElementById('inputMeetingEndTime').value : '';
  const badge = document.getElementById('meetingDurationBadge');
  if (!badge) return;

  if (!startVal || !endVal) {
    badge.textContent = '请选择起止时间';
    return;
  }

  const dur = calculateDurationFromRange(startVal, endVal);
  const hours = (dur / 60).toFixed(2);
  badge.textContent = `时长：${dur} 分钟 (${hours}H)`;

  document.querySelectorAll('.duration-quick-chips .chip-btn').forEach(b => {
    const t = b.textContent;
    const match = (dur === 15 && t.includes('15')) ||
                  (dur === 30 && t.includes('30')) ||
                  (dur === 45 && t.includes('45')) ||
                  (dur === 60 && t.includes('1小时')) ||
                  (dur === 90 && t.includes('1.5')) ||
                  (dur === 120 && t.includes('2小时'));
    b.classList.toggle('selected', match);
  });
}

function quickFillLocation(loc) {
  const el = document.getElementById('inputMeetingLocation');
  if (el) el.value = loc;
}

function quickFillMinuter(name) {
  const el = document.getElementById('inputMeetingMinuter');
  if (el) el.value = name;
}

function appendAttendee(name) {
  const input = document.getElementById('inputMeetingAttendees');
  if (!input) return;
  const current = input.value.trim();
  if (!current) {
    input.value = name;
  } else {
    const list = current.split(/[、,，\\s]+/).filter(Boolean);
    if (!list.includes(name)) {
      input.value = current + '、' + name;
    }
  }
}

function insertDecisionTemplate() {
  const input = document.getElementById('inputMeetingDecision');
  if (!input) return;
  if (!input.value.trim()) {
    input.value = '1. \\n2. ';
    input.focus();
  }
}

function openAddMeetingModal() {
  document.getElementById('meetingModalTitle').textContent = '登记主管会议预约';
  document.getElementById('inputMeetingId').value = '';
  document.getElementById('inputMeetingDate').value = selectedTimelineDate || new Date().toISOString().slice(0, 10);
  document.getElementById('inputMeetingStartTime').value = '10:00';
  document.getElementById('inputMeetingEndTime').value = '10:45';

  // Mandatory fields: subject & reporter are empty
  document.getElementById('inputMeetingSubject').value = '';
  document.getElementById('inputMeetingReporter').value = '';

  // Optional fields: ALL COMPLETELY EMPTY by default per user request
  document.getElementById('inputMeetingLocation').value = '';
  document.getElementById('inputMeetingMinuter').value = '';
  document.getElementById('inputMeetingAttendees').value = '';
  document.getElementById('inputMeetingBackground').value = '';
  document.getElementById('inputMeetingDecision').value = '';
  document.getElementById('inputMeetingRequester').value = '';
  document.getElementById('inputMeetingNotes').value = '';

  document.getElementById('selectMeetingStatus').value = 'scheduled';
  document.getElementById('selectMeetingPriority').value = 'medium';

  updateMeetingDurationBadge();
  openModal('meetingModal');
}

function saveMeeting() {
  const id = document.getElementById('inputMeetingId').value;
  const date = document.getElementById('inputMeetingDate').value;
  const startTime = document.getElementById('inputMeetingStartTime').value;
  const endTime = document.getElementById('inputMeetingEndTime').value;
  const subject = document.getElementById('inputMeetingSubject').value.trim();
  const reporter = document.getElementById('inputMeetingReporter').value.trim();

  // Mandatory checks
  if (!date) {
    showToast('请选择会议日期');
    document.getElementById('inputMeetingDate').focus();
    return;
  }
  if (!startTime) {
    showToast('请选择开始时间');
    document.getElementById('inputMeetingStartTime').focus();
    return;
  }
  if (!endTime) {
    showToast('请选择结束时间');
    document.getElementById('inputMeetingEndTime').focus();
    return;
  }
  if (!subject) {
    showToast('请填写会议主题');
    document.getElementById('inputMeetingSubject').focus();
    return;
  }
  if (!reporter) {
    showToast('请填写汇报人');
    document.getElementById('inputMeetingReporter').focus();
    return;
  }

  // Duration
  const duration = calculateDurationFromRange(startTime, endTime);
  const durationHours = (duration / 60).toFixed(2);

  // Optional fields (empty string if blank)
  const location = document.getElementById('inputMeetingLocation').value.trim();
  const minuter = document.getElementById('inputMeetingMinuter').value.trim();
  const attendees = document.getElementById('inputMeetingAttendees').value.trim();
  const background = document.getElementById('inputMeetingBackground').value.trim();
  const decision = document.getElementById('inputMeetingDecision').value.trim();
  const requester = document.getElementById('inputMeetingRequester').value.trim();
  const status = document.getElementById('selectMeetingStatus').value || 'scheduled';
  const priority = document.getElementById('selectMeetingPriority').value || 'medium';
  const notes = document.getElementById('inputMeetingNotes').value.trim();

  let meetings = getData(STORAGE_KEYS.MEETINGS);

  const meetingData = {
    date,
    time: startTime,
    startTime,
    endTime,
    duration,
    durationHours,
    subject,
    reporter,
    location,
    minuter,
    attendees,
    background,
    decision,
    requester,
    status,
    priority,
    notes
  };

  if (id) {
    meetings = meetings.map(m => m.id == id ? { ...m, ...meetingData, id: m.id } : m);
    showToast('会议预约已更新');
  } else {
    meetings.unshift({
      id: Date.now(),
      ...meetingData
    });
    showToast('会议预约已成功登记');
  }

  setData(STORAGE_KEYS.MEETINGS, meetings);
  closeModal('meetingModal');
  renderMeetings();
}

function editMeeting(id) {
  const meetings = getData(STORAGE_KEYS.MEETINGS);
  const m = meetings.find(x => x.id === id);
  if (!m) return;

  document.getElementById('meetingModalTitle').textContent = '编辑主管会议预约';
  document.getElementById('inputMeetingId').value = m.id;
  document.getElementById('inputMeetingDate').value = m.date;

  const sTime = m.startTime || m.time || '10:00';
  const eTime = m.endTime || calculateEndTime(sTime, m.duration || 45);
  document.getElementById('inputMeetingStartTime').value = sTime;
  document.getElementById('inputMeetingEndTime').value = eTime;

  document.getElementById('inputMeetingSubject').value = m.subject || '';
  document.getElementById('inputMeetingReporter').value = m.reporter || '';
  document.getElementById('inputMeetingLocation').value = m.location || '';
  document.getElementById('inputMeetingMinuter').value = m.minuter || '';
  document.getElementById('inputMeetingAttendees').value = m.attendees || '';
  document.getElementById('inputMeetingBackground').value = m.background || '';
  document.getElementById('inputMeetingDecision').value = m.decision || '';
  document.getElementById('inputMeetingRequester').value = m.requester || '';
  document.getElementById('selectMeetingStatus').value = m.status || 'scheduled';
  document.getElementById('selectMeetingPriority').value = m.priority || 'medium';
  document.getElementById('inputMeetingNotes').value = m.notes || '';

  updateMeetingDurationBadge();
  openModal('meetingModal');
}"""
    content = content[:idx_func_start] + new_modal_funcs + content[idx_func_end:]
    print("✓ Replaced modal functions safely")
else:
    print("! Could not locate openAddMeetingModal function block")

# 4. Update openAddMeetingModalWithSlot
old_slot_func = """function openAddMeetingModalWithSlot(date, startTime, duration) {
  openAddMeetingModal();
  if (date) document.getElementById('inputMeetingDate').value = date;
  if (startTime) document.getElementById('inputMeetingTime').value = startTime;
  if (duration) setMeetingDuration(duration);
  showToast(`已自动填入排期时段：${date} ${startTime} (${duration}分钟)`);
}"""

new_slot_func = """function openAddMeetingModalWithSlot(date, startTime, duration) {
  openAddMeetingModal();
  if (date) document.getElementById('inputMeetingDate').value = date;
  if (startTime) {
    document.getElementById('inputMeetingStartTime').value = startTime;
    const dur = parseInt(duration || 45, 10);
    document.getElementById('inputMeetingEndTime').value = calculateEndTime(startTime, dur);
  }
  updateMeetingDurationBadge();
  const eTime = document.getElementById('inputMeetingEndTime').value;
  showToast(`已自动填入推荐空档：${date} ${startTime} - ${eTime}`);
}"""

if old_slot_func in content:
    content = content.replace(old_slot_func, new_slot_func)
    print("✓ Updated openAddMeetingModalWithSlot")

# 5. Update Weekly Card Time display to show Start Time - End Time
old_weekly_time_str = """            <div class="weekly-card-time">
              <span>${m.time} (${durHours}H)</span>
              <span style="font-size:10.5px; font-weight:normal; color:var(--text-muted);">${escapeHtml(m.location || '主管办公室')}</span>
            </div>

            <div class="weekly-card-title">
              ${escapeHtml(m.subject)}
            </div>

            <div class="weekly-card-meta">
              <div><strong>汇报人：</strong>${escapeHtml(m.reporter || m.attendees.split('、')[1] || '未注明')}</div>
              <div><strong>参会人：</strong>${escapeHtml(m.attendees)}</div>
              ${m.minuter ? `<div><strong>纪要人：</strong><span style="color:#2563eb; font-weight:600;">${escapeHtml(m.minuter)}</span></div>` : ''}
            </div>"""

new_weekly_time_str = """            <div class="weekly-card-time">
              <span>${m.startTime || m.time}${m.endTime ? ' - ' + m.endTime : ''} (${durHours}H)</span>
              ${m.location ? `<span style="font-size:10.5px; font-weight:normal; color:var(--text-muted);">${escapeHtml(m.location)}</span>` : ''}
            </div>

            <div class="weekly-card-title">
              ${escapeHtml(m.subject)}
            </div>

            <div class="weekly-card-meta">
              <div><strong>汇报人：</strong>${escapeHtml(m.reporter || (m.attendees ? m.attendees.split('、')[1] : '') || '未注明')}</div>
              ${m.attendees ? `<div><strong>参会人：</strong>${escapeHtml(m.attendees)}</div>` : ''}
              ${m.minuter ? `<div><strong>纪要人：</strong><span style="color:#2563eb; font-weight:600;">${escapeHtml(m.minuter)}</span></div>` : ''}
            </div>"""

if old_weekly_time_str in content:
    content = content.replace(old_weekly_time_str, new_weekly_time_str)
    print("✓ Updated weekly-card time and meta rendering")

# 6. Update copySingleMeetingNotice with start and end time
old_copy_single = """  const text = [
    '【主管会议安排通知】' + m.subject,
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    '会议时间：' + m.date + ' ' + m.time + ' (' + (m.duration || 45) + '分钟)',
    '会议地点：' + (m.location || '主管办公室'),
    '汇报人：' + (m.reporter || '未注明'),
    '与会人员：' + m.attendees,
    (m.minuter ? '纪要人：' + m.minuter : ''),
    (m.background ? '会议背景：' + m.background : ''),
    '决策要点：\\n' + m.decision,
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    '秘书处提示：请参会人员提前5分钟就座，精简汇报，直奔决策要点。'
  ].filter(Boolean).join('\\n');"""

new_copy_single = """  const sTime = m.startTime || m.time;
  const eTime = m.endTime || calculateEndTime(sTime, m.duration || 45);

  const text = [
    '【主管会议安排通知】' + m.subject,
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    '会议时间：' + m.date + ' ' + sTime + ' - ' + eTime + ' (' + (m.duration || 45) + '分钟)',
    m.location ? ('会议地点：' + m.location) : '',
    '汇报人：' + (m.reporter || '未注明'),
    m.attendees ? ('与会人员：' + m.attendees) : '',
    m.minuter ? ('会议纪要：' + m.minuter) : '',
    m.decision ? ('决策要点：' + m.decision) : '',
    m.background ? ('议题背景：' + m.background) : '',
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    '秘书处提醒：请汇报人准时参会，精炼汇报，直奔决策要点。'
  ].filter(Boolean).join('\\n');"""

if old_copy_single in content:
    content = content.replace(old_copy_single, new_copy_single)
    print("✓ Updated copySingleMeetingNotice with start & end time")

with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("assemble_final_app.py updated successfully for round 11.")

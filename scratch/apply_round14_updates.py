#!/usr/bin/env python3
import re

with open("assemble_final_app.py", "r", encoding="utf-8") as f:
    content = f.read()

print("Original content length:", len(content))

# 1. Point 1: Remove top header conflict alerts
# Weekly Board column header: remove visible badge
old_col_header_badge = """            ${dayTrip ? `<span class="badge" style="background:#dcfce7; color:#15803d; border:1px solid #86efac; font-size:9.5px; padding:1px 6px; border-radius:10px; font-weight:700;" title="领导出差目的地：${dayTrip.tzName} (比开罗${dayTrip.diffText}) · 本日日程全按当地时间安排">✈️ ${dayTrip.tzName}</span>` : ''}
            ${dayMeetings.some(m => conflictMap[m.id] && conflictMap[m.id].length > 0) ? `<span class="badge weekly-conflict-header-badge" title="本日存在会议时间冲突！">⚠️ 时间冲突</span>` : ''}"""

new_col_header_badge = """            ${dayTrip ? `<span class="badge" style="background:#dcfce7; color:#15803d; border:1px solid #86efac; font-size:9.5px; padding:1px 6px; border-radius:10px; font-weight:700;" title="领导出差目的地：${dayTrip.tzName} (比开罗${dayTrip.diffText}) · 本日日程全按当地时间安排">✈️ ${dayTrip.tzName}</span>` : ''}
            ${dayMeetings.some(m => conflictMap[m.id] && conflictMap[m.id].length > 0) ? `<span class="badge weekly-conflict-header-badge" style="display:none;" title="本日存在会议时间冲突！">⚠️ 时间冲突</span>` : ''}"""

assert old_col_header_badge in content, "Could not find old_col_header_badge"
content = content.replace(old_col_header_badge, new_col_header_badge)

# Day Calendar top title: remove visible badge
old_day_top_badge = """          ${isToday ? '<span class="cal-today-badge">今日</span>' : ''}
          ${isWeekend ? '<span class="weekly-weekend-badge">周末</span>' : ''}
          ${dayMeetings.some(m => conflictMap[m.id] && conflictMap[m.id].length > 0) ? `<span class="badge" style="background:#fee2e2; color:#be123c; border:1px solid #fecdd3; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:700; margin-left:8px;" title="本日存在会议时间冲突">⚠️ 存在时间冲突</span>` : ''}"""

new_day_top_badge = """          ${isToday ? '<span class="cal-today-badge">今日</span>' : ''}
          ${isWeekend ? '<span class="weekly-weekend-badge">周末</span>' : ''}
          ${dayMeetings.some(m => conflictMap[m.id] && conflictMap[m.id].length > 0) ? `<span class="badge" style="display:none;" title="本日存在会议时间冲突">⚠️ 存在时间冲突</span>` : ''}"""

assert old_day_top_badge in content, "Could not find old_day_top_badge"
content = content.replace(old_day_top_badge, new_day_top_badge)

# 2. Point 2: Card conflict pill: only "重合" + 重合时间, no "(30m)" or "(90min)" or "（重叠时长：xx分钟）"
old_weekly_conflict_pill = """          ${hasConflict ? `
            <div class="weekly-card-conflict" title="⚠️ 会议时间冲突：与【${mConflicts.map(c => escapeHtml(c.otherSubject)).join('、')}】重合 ${mConflicts.map(c => c.overlapRangeStr).join('、')}（点击查看详情）">
              <span class="conflict-head-icon">⚠️</span>
              <span class="conflict-overlap-label">重合</span>
              <strong class="conflict-overlap-time">${mConflicts[0].overlapRangeStr}</strong>
              <span class="conflict-overlap-dur">(${mConflicts[0].overlapDuration}m)</span>
              ${mConflicts.length > 1 ? `<span class="weekly-conflict-more">+${mConflicts.length - 1}</span>` : ''}
            </div>
          ` : ''}"""

new_weekly_conflict_pill = """          ${hasConflict ? `
            <div class="weekly-card-conflict" title="⚠️ 会议时间冲突：与【${mConflicts.map(c => escapeHtml(c.otherSubject)).join('、')}】重合 ${mConflicts.map(c => c.overlapRangeStr).join('、')}（点击查看详情）">
              <span class="conflict-head-icon">⚠️</span>
              <span class="conflict-overlap-label">重合</span>
              <strong class="conflict-overlap-time">${mConflicts[0].overlapRangeStr}</strong>
              ${mConflicts.length > 1 ? `<span class="weekly-conflict-more">+${mConflicts.length - 1}</span>` : ''}
            </div>
          ` : ''}"""

assert old_weekly_conflict_pill in content, "Could not find old_weekly_conflict_pill"
content = content.replace(old_weekly_conflict_pill, new_weekly_conflict_pill)

# In Day Calendar card:
old_day_card_conflict = """        ${mConflicts.length > 0 ? `
          <div class="day-meeting-conflict-box" title="⚠️ 会议时间冲突：与【${mConflicts.map(c => escapeHtml(c.otherSubject)).join('、')}】重合（点击查看详情）" onclick="editMeeting(${m.id})">
            <span class="day-conflict-time-pill">⚠️ 🕒 重合时间：<strong>${mConflicts[0].overlapRangeStr}</strong></span>
            <span class="day-conflict-dur">（重叠时长：${mConflicts[0].overlapDuration} 分钟）</span>
            ${mConflicts.length > 1 ? `<span class="day-conflict-count-badge">+${mConflicts.length - 1} 处冲突</span>` : ''}
            <span style="font-size:11px; color:#9f1239; margin-left:auto; font-weight:600;">点击查看详情 ▶</span>
          </div>
        ` : ''}"""

new_day_card_conflict = """        ${mConflicts.length > 0 ? `
          <div class="day-meeting-conflict-box" title="⚠️ 会议时间冲突：与【${mConflicts.map(c => escapeHtml(c.otherSubject)).join('、')}】重合（点击查看详情）" onclick="editMeeting(${m.id})">
            <span class="day-conflict-time-pill">⚠️ 🕒 重合：<strong>${mConflicts[0].overlapRangeStr}</strong></span>
            ${mConflicts.length > 1 ? `<span class="day-conflict-count-badge">+${mConflicts.length - 1} 处冲突</span>` : ''}
            <span style="font-size:11px; color:#9f1239; margin-left:auto; font-weight:600;">点击查看详情 ▶</span>
          </div>
        ` : ''}"""

assert old_day_card_conflict in content, "Could not find old_day_card_conflict"
content = content.replace(old_day_card_conflict, new_day_card_conflict)

# 3. Point 3: Morning 09:00 - 12:00, Afternoon 14:00 - 18:00
# Update calculateDayFreeSlots
old_calc_slots = """function calculateDayFreeSlots(meetings, dateStr) {
  const dayStart = 8 * 60 + 30; // 08:30 = 510
  const lunchStart = 12 * 60;   // 12:00 = 720
  const lunchEnd = 14 * 60;     // 14:00 = 840
  const dayEnd = 18 * 60;       // 18:00 = 1080"""

new_calc_slots = """function calculateDayFreeSlots(meetings, dateStr) {
  const dayStart = 9 * 60;      // 09:00 = 540 (上午9点开始-12点)
  const lunchStart = 12 * 60;   // 12:00 = 720
  const lunchEnd = 14 * 60;     // 14:00 = 840
  const dayEnd = 18 * 60;       // 18:00 = 1080 (下午14点-18点)"""

assert old_calc_slots in content, "Could not find old_calc_slots"
content = content.replace(old_calc_slots, new_calc_slots)

# Update Weekly Board morning & afternoon split & wording
old_weekly_split = """      // 区分上午 (08:30 - 12:00) 与 下午 (13:30 - 18:00)
      const morningMeetings = [];
      const afternoonMeetings = [];

      dayMeetings.forEach(m => {
        const dt = getMeetingDisplayTime(m);
        const sMins = timeStrToMinutes(dt.start || '10:00');
        if (sMins < 780) { // 13:00 前归为上午
          morningMeetings.push(m);
        } else {
          afternoonMeetings.push(m);
        }
      });

      const morningFreeSlots = freeSlots.filter(s => s.end <= 780);
      const afternoonFreeSlots = freeSlots.filter(s => s.start >= 780);

      // --- 1. 上午时段 (如果只在下午，上午显示为空档可约) ---
      html += `
        <div class="weekly-period-block morning-block">
          <div class="weekly-period-divider">
            <span>🌅 上午 (08:30 - 12:00)</span>
            <span class="${morningMeetings.length > 0 ? 'period-status-occupied' : 'period-status-empty'}">
              ${morningMeetings.length > 0 ? morningMeetings.length + '场排期' : '空闲'}
            </span>
          </div>
      `;
      if (morningMeetings.length === 0) {
        html += `
          <div class="weekly-empty-period-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '09:30', 60)" title="上午时段空闲，点击预约上午会议">
            <div class="empty-slot-text">🌅 上午时段空闲 (可约) ＋</div>
            <div class="empty-slot-sub">08:30 - 12:00 无排期</div>
          </div>
        `;
      } else {
        morningMeetings.forEach(m => {
          html += renderWeeklySingleCard(m, false);
        });
        if (morningFreeSlots.length > 0) {
          html += `<div class="weekly-period-free-slots">`;
          morningFreeSlots.forEach(slot => {
            html += `
              <div class="weekly-free-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '${slot.startStr}', ${Math.min(slot.duration, 60)})" title="上午空档 ${slot.startStr} - ${slot.endStr} (${slot.duration}m 可约)">
                <span class="slot-time">${slot.startStr} - ${slot.endStr}</span>
                <span class="slot-dur-tag">${slot.duration}m ＋</span>
              </div>
            `;
          });
          html += `</div>`;
        }
      }
      html += `</div>`; // end morning-block

      // --- 2. 下午时段 ---
      html += `
        <div class="weekly-period-block afternoon-block">
          <div class="weekly-period-divider">
            <span>🌇 下午 (13:30 - 18:00)</span>
            <span class="${afternoonMeetings.length > 0 ? 'period-status-occupied' : 'period-status-empty'}">
              ${afternoonMeetings.length > 0 ? afternoonMeetings.length + '场排期' : '空闲'}
            </span>
          </div>
      `;
      if (afternoonMeetings.length === 0) {
        html += `
          <div class="weekly-empty-period-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '14:30', 60)" title="下午时段空闲，点击预约下午会议">
            <div class="empty-slot-text">🌇 下午时段空闲 (可约) ＋</div>
            <div class="empty-slot-sub">13:30 - 18:00 无排期</div>
          </div>
        `;"""

new_weekly_split = """      // 区分上午 (09:00 - 12:00) 与 下午 (14:00 - 18:00)
      const morningMeetings = [];
      const afternoonMeetings = [];

      dayMeetings.forEach(m => {
        const dt = getMeetingDisplayTime(m);
        const sMins = timeStrToMinutes(dt.start || '09:00');
        if (sMins < 720) { // 12:00 前归为上午
          morningMeetings.push(m);
        } else {
          afternoonMeetings.push(m);
        }
      });

      const morningFreeSlots = freeSlots.filter(s => s.end <= 720);
      const afternoonFreeSlots = freeSlots.filter(s => s.start >= 840);

      // --- 1. 上午时段 (09:00 - 12:00) ---
      html += `
        <div class="weekly-period-block morning-block">
          <div class="weekly-period-divider">
            <span>🌅 上午 (09:00 - 12:00)</span>
            <span class="${morningMeetings.length > 0 ? 'period-status-occupied' : 'period-status-empty'}">
              ${morningMeetings.length > 0 ? morningMeetings.length + '场排期' : '空闲'}
            </span>
          </div>
      `;
      if (morningMeetings.length === 0) {
        html += `
          <div class="weekly-empty-period-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '09:00', 60)" title="上午时段空闲，点击预约上午会议">
            <div class="empty-slot-text">🌅 上午空闲 (可约) ＋</div>
            <div class="empty-slot-sub">09:00 - 12:00 无排期</div>
          </div>
        `;
      } else {
        morningMeetings.forEach(m => {
          html += renderWeeklySingleCard(m, false);
        });
        if (morningFreeSlots.length > 0) {
          html += `<div class="weekly-period-free-slots">`;
          morningFreeSlots.forEach(slot => {
            html += `
              <div class="weekly-free-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '${slot.startStr}', ${Math.min(slot.duration, 60)})" title="上午空档 ${slot.startStr} - ${slot.endStr} (${slot.duration}m 可约)">
                <span class="slot-time">${slot.startStr} - ${slot.endStr}</span>
                <span class="slot-dur-tag">${slot.duration}m ＋</span>
              </div>
            `;
          });
          html += `</div>`;
        }
      }
      html += `</div>`; // end morning-block

      // --- 2. 下午时段 (14:00 - 18:00) ---
      html += `
        <div class="weekly-period-block afternoon-block">
          <div class="weekly-period-divider">
            <span>🌇 下午 (14:00 - 18:00)</span>
            <span class="${afternoonMeetings.length > 0 ? 'period-status-occupied' : 'period-status-empty'}">
              ${afternoonMeetings.length > 0 ? afternoonMeetings.length + '场排期' : '空闲'}
            </span>
          </div>
      `;
      if (afternoonMeetings.length === 0) {
        html += `
          <div class="weekly-empty-period-slot" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '14:00', 60)" title="下午时段空闲，点击预约下午会议">
            <div class="empty-slot-text">🌇 下午空闲 (可约) ＋</div>
            <div class="empty-slot-sub">14:00 - 18:00 无排期</div>
          </div>
        `;"""

assert old_weekly_split in content, "Could not find old_weekly_split"
content = content.replace(old_weekly_split, new_weekly_split)

# Update Day Calendar dividers & empty slots
old_day_morning_div = '<div class="day-section-divider">🌅 上午日程推进 (08:30 - 12:00)</div>'
new_day_morning_div = '<div class="day-section-divider">🌅 上午日程推进 (09:00 - 12:00)</div>'
assert old_day_morning_div in content, "Could not find old_day_morning_div"
content = content.replace(old_day_morning_div, new_day_morning_div)

old_day_morning_card = """        <div><span>🕒</span> <strong>上午时段空闲 (08:30 - 12:00)</strong> · 无会议排期</div>
        <button class="btn btn-sm btn-ghost" style="color:#15803d; border-color:#86efac; background:#fff; font-size:11px;" onclick="openAddMeetingModalWithSlot('${curDateStr}', '09:30', 60)">＋ 安排上午会议</button>"""

new_day_morning_card = """        <div><span>🕒</span> <strong>上午时段空闲 (09:00 - 12:00)</strong> · 无会议排期</div>
        <button class="btn btn-sm btn-ghost" style="color:#15803d; border-color:#86efac; background:#fff; font-size:11px;" onclick="openAddMeetingModalWithSlot('${curDateStr}', '09:00', 60)">＋ 安排上午会议</button>"""

assert old_day_morning_card in content, "Could not find old_day_morning_card"
content = content.replace(old_day_morning_card, new_day_morning_card)

# 4. Point 4: "全天排满，删去从早到晚"
# Card pill tag
old_pill_tag = "${isAllDay ? '<span class=\"allday-pill-tag\">从早到晚 · 全天</span>' : ''}"
new_pill_tag = "${isAllDay ? '<span class=\"allday-pill-tag\">全天</span>' : ''}"
assert old_pill_tag in content, "Could not find old_pill_tag"
content = content.replace(old_pill_tag, new_pill_tag)

# All day banner in Weekly Board: minimalist "全天排满", delete bottom redundant notice
old_allday_weekly = """    } else if (allDayMeeting) {
      // 🌞 全天会议：把一整天都显示用完了！
      html += `
        <div class="weekly-allday-wrap">
          <div class="weekly-allday-banner">
            <span>🌞 全天排期已满 · 从早到晚</span>
          </div>
      `;
      dayMeetings.forEach(m => {
        html += renderWeeklySingleCard(m, m.id === allDayMeeting.id);
      });
      html += `
          <div class="weekly-allday-occupied-notice">
            <span>🚫 本日从早到晚均已占满，无可用空档</span>
          </div>
        </div>
      `;
    }"""

new_allday_weekly = """    } else if (allDayMeeting) {
      // 📅 全天排满 (极简清晰，删去从早到晚)
      html += `
        <div class="weekly-allday-wrap">
          <div class="weekly-allday-banner">
            <span>📅 全天排满</span>
          </div>
      `;
      dayMeetings.forEach(m => {
        html += renderWeeklySingleCard(m, m.id === allDayMeeting.id);
      });
      html += `
        </div>
      `;
    }"""

assert old_allday_weekly in content, "Could not find old_allday_weekly"
content = content.replace(old_allday_weekly, new_allday_weekly)

with open("assemble_final_app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("assemble_final_app.py updated successfully for round 14!")

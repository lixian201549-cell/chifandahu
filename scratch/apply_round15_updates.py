#!/usr/bin/env python3
import sys

with open("assemble_final_app.py", "r", encoding="utf-8") as f:
    content = f.read()

print("Original content length:", len(content))

# 1. Scale up Snoopy in every module proportionally by 1/2 (1.5x)
# A. Module banner avatar in every module (今日任务, 会议预约, 时区协同, 常用链接, 每日小记, 每日英语)
old_banner_avatar_css = """  .module-banner-avatar {
    width: 52px;
    height: 56px;
    object-fit: contain;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.06));
    flex-shrink: 0;
    transition: transform 0.2s ease;
  }
  .theme-links .module-banner-avatar {
    width: 56px;
    height: 58px;
  }
  .theme-notes .module-banner-avatar {
    width: 56px;
    height: 58px;
  }
  .theme-english .module-banner-avatar {
    width: 54px;
    height: 56px;
  }"""

new_banner_avatar_css = """  /* Module Header Banner Snoopy Avatars: Scaled up proportionally by 1/2 (+50%, 1.5x) */
  .module-banner-avatar {
    width: 78px;
    height: 84px;
    object-fit: contain;
    filter: drop-shadow(0 3px 6px rgba(0,0,0,0.08));
    flex-shrink: 0;
    transition: transform 0.2s ease;
  }
  .theme-links .module-banner-avatar {
    width: 84px;
    height: 87px;
  }
  .theme-notes .module-banner-avatar {
    width: 84px;
    height: 87px;
  }
  .theme-english .module-banner-avatar {
    width: 81px;
    height: 84px;
  }"""

assert old_banner_avatar_css in content, "Could not find old_banner_avatar_css"
content = content.replace(old_banner_avatar_css, new_banner_avatar_css)

# B. Brand avatar in top header
old_brand_avatar_css = """  .brand-avatar {
    width: 44px;
    height: 48px;
    object-fit: contain;
    transition: transform 0.25s ease;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.06));
  }"""

new_brand_avatar_css = """  .brand-avatar {
    width: 66px;
    height: 72px;
    object-fit: contain;
    transition: transform 0.25s ease;
    filter: drop-shadow(0 2px 5px rgba(0,0,0,0.08));
  }"""

assert old_brand_avatar_css in content, "Could not find old_brand_avatar_css"
content = content.replace(old_brand_avatar_css, new_brand_avatar_css)

# C. Nav Tab Snoopy icons (22px -> 33px)
old_nav_tab_css = """  .nav-tab img {
    width: 22px;
    height: 22px;
    object-fit: contain;
    transition: transform 0.2s ease;
  }"""

new_nav_tab_css = """  .nav-tab img {
    width: 32px;
    height: 32px;
    object-fit: contain;
    transition: transform 0.2s ease;
  }"""

assert old_nav_tab_css in content, "Could not find old_nav_tab_css"
content = content.replace(old_nav_tab_css, new_nav_tab_css)

# D. HOME Blackboard Snoopy (110px x 132px -> 165px x 198px)
old_snoopy_lying_css = """  .snoopy-lying-wrap {
    position: relative;
    display: block;
    width: 110px;
    height: 132px;
    animation: snoopyGentleFloat 3.8s ease-in-out infinite;
    transition: transform 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.22s ease;
    transform-origin: bottom center;
  }
  .border-snoopy-stage:hover .snoopy-lying-wrap {
    animation-play-state: paused;
    transform: translateY(-6px) scale(1.08) rotate(-1.2deg);
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.22)) drop-shadow(0 0 14px rgba(254, 240, 138, 0.45));
  }

  .snoopy-lying-img {
    width: 110px;
    height: 132px;
    object-fit: contain;
    display: block;
    filter: drop-shadow(0 4px 10px rgba(0,0,0,0.15));
  }"""

new_snoopy_lying_css = """  .snoopy-lying-wrap {
    position: relative;
    display: block;
    width: 165px;
    height: 198px;
    animation: snoopyGentleFloat 3.8s ease-in-out infinite;
    transition: transform 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.22s ease;
    transform-origin: bottom center;
  }
  .border-snoopy-stage:hover .snoopy-lying-wrap {
    animation-play-state: paused;
    transform: translateY(-6px) scale(1.08) rotate(-1.2deg);
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.22)) drop-shadow(0 0 14px rgba(254, 240, 138, 0.45));
  }

  .snoopy-lying-img {
    width: 165px;
    height: 198px;
    object-fit: contain;
    display: block;
    filter: drop-shadow(0 4px 10px rgba(0,0,0,0.15));
  }"""

assert old_snoopy_lying_css in content, "Could not find old_snoopy_lying_css"
content = content.replace(old_snoopy_lying_css, new_snoopy_lying_css)

# E. Empty state card image in card list
old_empty_img = 'style="width:48px; opacity:0.65; margin-bottom:8px;"'
new_empty_img = 'style="width:72px; opacity:0.65; margin-bottom:8px;"'
if old_empty_img in content:
    content = content.replace(old_empty_img, new_empty_img)

# 2. Precise detection for Thursday and all days:
# If morning has no meetings or morning has free slots, morning HAS free time!
# It must NEVER be falsely identified as 全天排满!
old_weekly_board_decision_block = """    // 检查是否有从早到晚 / 全天占满的会议
    const allDayMeeting = dayMeetings.find(m => {
      const dur = parseInt(m.duration || 45, 10);
      const sMin = timeStrToMinutes(m.startTime || m.time || '10:00');
      const eMin = timeStrToMinutes(m.endTime || calculateEndTime(m.startTime || m.time, dur));
      return dur >= 360 || (sMin <= 600 && eMin >= 1020) || (m.subject && (m.subject.includes('全天') || m.subject.includes('从早到晚')));
    });

    if (dayMeetings.length === 0) {
      html += `
        <div style="text-align:center; padding: 22px 8px; color:var(--text-muted); font-size:12px; background:#fff; border:1px dashed var(--border); border-radius:var(--radius-sm);">
          <div style="margin-bottom:4px;">全天暂无会议</div>
          <button class="btn btn-sm btn-ghost" style="margin-top:4px; font-size:11px;" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '10:00', 45)">＋ 安排预约</button>
        </div>
      `;
    } else if (allDayMeeting) {
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
    } else {
      // 区分上午 (09:00 - 12:00) 与 下午 (14:00 - 18:00)
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
      const afternoonFreeSlots = freeSlots.filter(s => s.start >= 840);"""

new_weekly_board_decision_block = """    // 区分上午 (09:00 - 12:00) 与 下午 (14:00 - 18:00)
    const morningMeetings = [];
    const afternoonMeetings = [];

    dayMeetings.forEach(m => {
      const dt = getMeetingDisplayTime(m);
      const sMins = timeStrToMinutes(dt.start || '09:00');
      const dur = parseInt(m.duration || 45, 10);
      const eMins = dt.end ? timeStrToMinutes(dt.end) : (sMins + dur);
      if (sMins < 720) { // 12:00 前有排期
        morningMeetings.push(m);
      }
      if (eMins > 840 || sMins >= 720) { // 14:00 之后有排期
        afternoonMeetings.push(m);
      }
    });

    const morningFreeSlots = freeSlots.filter(s => s.end <= 720);
    const afternoonFreeSlots = freeSlots.filter(s => s.start >= 840);

    // 精准识别：只要上午没有会议，或者上午存在可用空档，上午就是有空闲的，绝不是全天排满！
    const hasMorningFreeTime = (morningMeetings.length === 0) || (morningFreeSlots.length > 0);
    const hasAfternoonFreeTime = (afternoonMeetings.length === 0) || (afternoonFreeSlots.length > 0);

    // 只有在全天确实无任何可用空档，且上午和下午均已被会议完全占满时，才判定为全天排满
    const isDayFullyBooked = dayMeetings.length > 0 && !hasMorningFreeTime && !hasAfternoonFreeTime && freeSlots.length === 0;

    if (dayMeetings.length === 0) {
      html += `
        <div style="text-align:center; padding: 22px 8px; color:var(--text-muted); font-size:12px; background:#fff; border:1px dashed var(--border); border-radius:var(--radius-sm);">
          <div style="margin-bottom:4px;">全天暂无会议</div>
          <button class="btn btn-sm btn-ghost" style="margin-top:4px; font-size:11px;" onclick="openAddMeetingModalWithSlot('${day.dateStr}', '09:00', 60)">＋ 安排预约</button>
        </div>
      `;
    } else if (isDayFullyBooked) {
      // 📅 全天排满 (极简清晰，删去从早到晚)
      html += `
        <div class="weekly-allday-wrap">
          <div class="weekly-allday-banner">
            <span>📅 全天排满</span>
          </div>
      `;
      dayMeetings.forEach(m => {
        html += renderWeeklySingleCard(m, true);
      });
      html += `
        </div>
      `;
    } else {"""

assert old_weekly_board_decision_block in content, "Could not find old_weekly_board_decision_block"
content = content.replace(old_weekly_board_decision_block, new_weekly_board_decision_block)

with open("assemble_final_app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("assemble_final_app.py updated successfully for round 15!")

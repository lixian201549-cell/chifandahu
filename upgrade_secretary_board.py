import re

print("Reading assemble_final_app.py...")
with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for Weekly Board
css_marker = "/* Supervisor Month Calendar & Cards Dual View Styles */"
weekly_css = """  /* Executive Weekly Board Styles (领导周历看板) */
  .weekly-board-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
  }
  .weekly-board-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 12px;
  }
  .weekly-nav-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .weekly-title {
    font-size: 16px;
    font-weight: 800;
    color: var(--text-primary);
    min-width: 220px;
    text-align: center;
  }
  .weekly-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    align-items: start;
  }
  @media (max-width: 1200px) {
    .weekly-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  @media (max-width: 768px) {
    .weekly-grid {
      grid-template-columns: 1fr;
    }
  }
  .weekly-col {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: all 0.2s ease;
    min-height: 420px;
  }
  .weekly-col.is-today {
    background: #f0f7ff;
    border: 2px solid var(--blue-accent);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
  }
  .weekly-col-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    border-bottom: 1px dashed var(--border);
  }
  .weekly-col-day {
    font-size: 13.5px;
    font-weight: 800;
    color: var(--text-primary);
  }
  .weekly-col-date {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: normal;
  }
  .weekly-col-badge {
    font-size: 10.5px;
    background: #e0e7ff;
    color: #3730a3;
    padding: 2px 6px;
    border-radius: 10px;
    font-weight: 600;
  }
  .weekly-col-events {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .weekly-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-left: 4px solid var(--blue-accent);
    border-radius: var(--radius-sm);
    padding: 10px 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    cursor: pointer;
  }
  .weekly-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border-color: var(--blue-accent);
  }
  .weekly-card.priority-high {
    border-left-color: var(--accent-red);
  }
  .weekly-card-time {
    font-size: 11px;
    font-weight: 700;
    color: var(--blue-accent);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }
  .weekly-card-title {
    font-size: 12.5px;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.4;
    margin-bottom: 6px;
  }
  .weekly-card-meta {
    font-size: 11px;
    color: var(--text-secondary);
    display: flex;
    flex-direction: column;
    gap: 3px;
    line-height: 1.4;
  }
  .weekly-card-decision {
    margin-top: 6px;
    padding: 5px 7px;
    background: #f8fafc;
    border-radius: 4px;
    font-size: 10.5px;
    color: var(--text-secondary);
    line-height: 1.35;
    border-left: 2px solid #cbd5e1;
  }
  .weekly-free-slot {
    background: rgba(22, 163, 74, 0.08);
    border: 1px dashed #16a34a;
    border-radius: var(--radius-sm);
    padding: 5px 8px;
    text-align: center;
    font-size: 10.5px;
    color: #15803d;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .weekly-free-slot:hover {
    background: rgba(22, 163, 74, 0.18);
  }

  """

if css_marker in content:
    content = content.replace(css_marker, weekly_css + css_marker, 1)
    print("Weekly Board CSS added successfully.")
else:
    print("WARNING: css_marker not found!")

# 2. Update HTML of pane-supervisor
html_pane_target = """      <!-- Main Supervisor Schedule Management Toolbar (View Switcher & Actions) -->
      <div class="meeting-toolbar" style="margin-bottom: 16px;">
        <div class="filter-tabs">
          <button class="filter-btn active" id="btnViewCalCards" onclick="setSupervisorViewMode('cal_cards')">📅 月度日历 + 卡片视图</button>
          <button class="filter-btn" id="btnViewAllCards" onclick="setSupervisorViewMode('all_cards')">🃏 全部日程卡片清单</button>
          <button class="filter-btn" id="btnViewTimeline" onclick="setSupervisorViewMode('timeline_only')">🕒 每日时间轴与空档</button>
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
          <button class="btn btn-primary" onclick="openImportCalendarModal()" title="支持任意自由文本、微信通知、Excel/WPS表格导入，自动规整为日历和卡片">
            📥 智能导入日程（自由格式/Excel）
          </button>
          <button class="btn" onclick="openAddMeetingModal()">
            ➕ 登记单场预约
          </button>
          <button class="btn" onclick="exportTodayMeetingBriefing()" title="一键生成当前选定日期的会议通报文本，方便发到微信/邮件/工作群">
            📋 复制当日会议通知
          </button>
        </div>
      </div>

      <!-- Section Title: 主管日程时间轴 (Requirement 1) -->
      <div class="selected-date-banner" id="supervisorSectionHeader">
        <div class="selected-date-title">
          <span>🕒 主管日程时间轴</span>
          <span class="persona-tag" id="currentViewModeTag">📅 月度日历 + 卡片视图</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <label style="font-size:12px; color:var(--text-secondary); font-weight:600;">当前选定日期：</label>
          <input type="date" id="timelineDateSelector" style="width:130px; padding:3px 8px; font-size:12px;" onchange="handleTimelineDateChange()" />
        </div>
      </div>

      <!-- 1. Month Calendar Section (月度日历板块) -->
      <div id="supervisorMonthCalendarContainer" class="supervisor-month-view"></div>

      <!-- 2. Daily Timeline & Auto-Detected Free Slots Section -->
      <div class="timeline-bar-wrap" id="supervisorTimelineWrap">
        <div class="timeline-header">
          <div>
            <span style="font-weight:700; font-size:13px;">🕒 当日时间轴占用（08:30 - 18:00）</span>
            <span style="font-size:11px; font-weight:normal; color:var(--text-muted); margin-left:8px;" id="timelineFreeCountBadge">（智能识别可排期空档中...）</span>
          </div>
          <button class="btn btn-sm btn-ghost" onclick="jumpToTodayCalendar()">回到今天</button>
        </div>

        <!-- Timeline Graphic Track -->
        <div class="timeline-track" id="supervisorTimelineTrack"></div>

        <!-- Interactive Quick Free Slot Chips -->
        <div class="timeline-free-pills" id="timelineFreeSlotsPills"></div>
      </div>

      <!-- 3. Selected Date Header & Filter Toolbar for Cards -->
      <div id="cardsSectionToolbar" style="margin-top: 18px; margin-bottom: 12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div style="font-size:13.5px; font-weight:700; color:var(--text-primary);" id="cardsSectionTitle">
          🃏 当日日程卡片详情
        </div>
        <div class="filter-tabs" id="cardStatusFilters">
          <button class="filter-btn active" data-filter="all" onclick="filterMeetings('all')">全部</button>
          <button class="filter-btn" data-filter="scheduled" onclick="filterMeetings('scheduled')">🔵 已排期</button>
          <button class="filter-btn" data-filter="pending" onclick="filterMeetings('pending')">🟡 待安排</button>
          <button class="filter-btn" data-filter="completed" onclick="filterMeetings('completed')">🟢 已完成</button>
        </div>
      </div>

      <!-- 4. Meeting Cards List Container -->
      <div id="meetingCardsList"></div>"""

html_pane_replacement = """      <!-- Main Supervisor Schedule Management Toolbar (View Switcher & Actions) -->
      <div class="meeting-toolbar" style="margin-bottom: 16px;">
        <div class="filter-tabs">
          <button class="filter-btn active" id="btnViewWeekBoard" onclick="setSupervisorViewMode('week_board')">📅 本周日历看板 (领导一览)</button>
          <button class="filter-btn" id="btnViewMonthCal" onclick="setSupervisorViewMode('month_cal')">🗓️ 月度全景日历</button>
          <button class="filter-btn" id="btnViewCardList" onclick="setSupervisorViewMode('card_list')">🃏 决策卡片清单</button>
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
          <button class="btn btn-primary" onclick="openImportCalendarModal()" title="支持固定标准表头导入或自由格式，智能识别星期一到星期五与预约时长">
            📥 智能导入日程（支持固定表头/自由格式）
          </button>
          <button class="btn" onclick="exportExecutiveScheduleBriefing()" title="一键生成本周/今日给领导的汇报通报文本，可直接发送微信/邮件/工作群">
            📋 复制领导日程通报
          </button>
          <button class="btn" onclick="openAddMeetingModal()">
            ➕ 登记单场预约
          </button>
        </div>
      </div>

      <!-- Section Title: 主管日程时间轴 (Requirement 1) -->
      <div class="selected-date-banner" id="supervisorSectionHeader">
        <div class="selected-date-title">
          <span>🕒 主管日程时间轴</span>
          <span class="persona-tag" id="currentViewModeTag">📅 本周日历看板 · 领导一眼看懂</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <label style="font-size:12px; color:var(--text-secondary); font-weight:600;">快速跳转日期：</label>
          <input type="date" id="timelineDateSelector" style="width:130px; padding:3px 8px; font-size:12px;" onchange="handleTimelineDateChange()" />
        </div>
      </div>

      <!-- 1. Executive Weekly Board (本周日历看板·领导一眼看懂周一到周五) -->
      <div id="supervisorWeeklyBoardContainer" class="weekly-board-wrap"></div>

      <!-- 2. Month Calendar Section (月度日历板块) -->
      <div id="supervisorMonthCalendarContainer" class="supervisor-month-view" style="display:none;"></div>

      <!-- 3. Cards Section Toolbar & List -->
      <div id="cardsSectionToolbar" style="display:none; margin-top: 18px; margin-bottom: 12px; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div style="font-size:13.5px; font-weight:700; color:var(--text-primary);" id="cardsSectionTitle">
          🃏 主管会议决策卡片清单
        </div>
        <div class="filter-tabs" id="cardStatusFilters">
          <button class="filter-btn active" data-filter="all" onclick="filterMeetings('all')">全部</button>
          <button class="filter-btn" data-filter="scheduled" onclick="filterMeetings('scheduled')">🔵 已排期</button>
          <button class="filter-btn" data-filter="pending" onclick="filterMeetings('pending')">🟡 待安排</button>
          <button class="filter-btn" data-filter="completed" onclick="filterMeetings('completed')">🟢 已完成</button>
        </div>
      </div>

      <!-- 4. Meeting Cards List Container -->
      <div id="meetingCardsList" style="display:none;"></div>"""

if html_pane_target in content:
    content = content.replace(html_pane_target, html_pane_replacement, 1)
    print("Supervisor pane HTML updated successfully.")
else:
    print("WARNING: html_pane_target not found!")

# 3. Update HTML of importCalendarModal: Add standard headers box, copy button, download template
html_modal_old = """      <div class="modal-body">
        <div style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.55;">
          支持<strong>任意自由格式</strong>：直接粘贴 Excel/WPS 表格、微信/企微通知、邮件、自然语言日程，或上传电脑文档（<code>.xlsx / .xls / .csv / .txt</code>）。系统将自动智能识别并规整为<strong>日历版本</strong>与<strong>卡片版本</strong>！
        </div>"""

html_modal_new = """      <div class="modal-body">
        <!-- Standard Header Box per User Request -->
        <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:6px; padding:10px 14px; margin-bottom:12px; font-size:12px;">
          <div style="font-weight:700; color:#0369a1; margin-bottom:5px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
            <span>📋 推荐标准 Excel 导入表头（支持自动对齐）：</span>
            <div style="display:flex; gap:6px;">
              <button type="button" class="btn btn-sm btn-ghost" onclick="copyStandardExcelHeader()" title="点击复制整行表头至剪贴板，可直接粘贴到您的Excel第一行">📋 复制标准表头</button>
              <button type="button" class="btn btn-sm btn-ghost" onclick="downloadStandardExcelTemplate()" title="下载预设好列名的标准 Excel CSV 模板">📥 下载示例模板</button>
            </div>
          </div>
          <code style="display:block; background:#fff; padding:6px 10px; border-radius:4px; border:1px solid #e0f2fe; color:#0c4a6e; font-size:11.5px; overflow-x:auto; white-space:nowrap; font-family:var(--font-mono);">
            *会议主题（关键任务）	*议题背景/决策要点说明	*汇报人	*参会人	*纪要人	*预约时长（H）
          </code>
          <div style="color:#0284c7; font-size:11px; margin-top:5px; line-height:1.45;">
            ★ <strong>智能容错识别</strong>：非强制填满所有列，核心信息仅需<strong>【会议主题】、【汇报人】、【预约时长（H）】</strong>即可排期！“星期一到星期五”等字样将自动识别为排期日期，绝不误认为会议主题。
          </div>
        </div>"""

if html_modal_old in content:
    content = content.replace(html_modal_old, html_modal_new, 1)
    print("Import modal HTML updated with standard headers.")
else:
    print("WARNING: html_modal_old not found!")

# 4. Update meetingModal form to include 纪要人 (Minuter)
meeting_form_old = """          <!-- 5. 与会人 (Mandatory) -->
          <div class="form-group">
            <label>👥 与会人 / 汇报人 (Attendees) *</label>
            <input type="text" id="inputMeetingAttendees" placeholder="例：主管、张总(地南代)、李总(开罗)、财务BP、HRG" required />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>👤 预约人 / 代表处部门</label>
              <input type="text" id="inputMeetingRequester" placeholder="例：地中海南代表处 · 张明" />
            </div>
            <div class="form-group">
              <label>📍 会议地点 / 线上会议号</label>
              <input type="text" id="inputMeetingLocation" placeholder="例：主管办公室 / WeLink 889-201" />
            </div>
          </div>"""

meeting_form_new = """          <!-- 4. 汇报人与参会人 (Mandatory) -->
          <div class="form-row">
            <div class="form-group">
              <label>👔 *汇报人 (Presenter) *</label>
              <input type="text" id="inputMeetingReporter" placeholder="例：张总(地南代) 或 李总" required />
            </div>
            <div class="form-group">
              <label>📝 *纪要人 (Minuter)</label>
              <input type="text" id="inputMeetingMinuter" placeholder="例：王秘书 (负责会后输出纪要)" />
            </div>
          </div>

          <!-- 5. 与会人 (Mandatory) -->
          <div class="form-group">
            <label>👥 *参会人 (Attendees) *</label>
            <input type="text" id="inputMeetingAttendees" placeholder="例：主管、李总(开罗)、财务BP、HRG" required />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>👤 预约人 / 代表处部门</label>
              <input type="text" id="inputMeetingRequester" placeholder="例：地中海南代表处 · 张明" />
            </div>
            <div class="form-group">
              <label>📍 会议地点 / 线上会议号</label>
              <input type="text" id="inputMeetingLocation" placeholder="例：主管办公室 / WeLink 889-201" />
            </div>
          </div>"""

if meeting_form_old in content:
    content = content.replace(meeting_form_old, meeting_form_new, 1)
    print("Meeting form updated with minuter.")
else:
    print("WARNING: meeting_form_old not found!")

with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Part 1 (HTML/CSS) done.")

import re

print("Reading assemble_final_app.py...")
with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS: Banner Avatar sizing and add Month Calendar / Dual-View / Import Preview styles
css_target = """  .module-banner-avatar {
    width: 60px;
    height: 64px;
    object-fit: contain;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));
    flex-shrink: 0;
  }"""

css_replacement = """  .module-banner-avatar {
    width: 72px;
    height: 76px;
    object-fit: contain;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));
    flex-shrink: 0;
    transition: transform 0.2s ease;
  }
  /* Enlarge logos for 常用链接, 每日小记, 每日英语 to match the first banners */
  .theme-links .module-banner-avatar {
    width: 82px;
    height: 84px;
    transform: scale(1.15);
  }
  .theme-notes .module-banner-avatar {
    width: 82px;
    height: 84px;
    transform: scale(1.18);
  }
  .theme-english .module-banner-avatar {
    width: 80px;
    height: 84px;
    transform: scale(1.15);
  }

  /* Supervisor Month Calendar & Cards Dual View Styles */
  .supervisor-month-view {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
  }
  .cal-top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 12px;
  }
  .cal-month-nav {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .cal-current-month-title {
    font-size: 16px;
    font-weight: 800;
    color: var(--text-primary);
    min-width: 130px;
    text-align: center;
  }
  .cal-grid-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
  }
  .cal-grid-table th {
    text-align: center;
    padding: 8px 4px;
    font-size: 12px;
    font-weight: 700;
    color: var(--text-secondary);
    background: var(--bg);
    border: 1px solid var(--border);
  }
  .cal-grid-table th.weekend {
    color: var(--accent-red);
  }
  .cal-day-cell {
    height: 86px;
    vertical-align: top;
    padding: 6px;
    border: 1px solid var(--border);
    background: var(--card);
    cursor: pointer;
    transition: all 0.15s ease;
    position: relative;
  }
  .cal-day-cell:hover {
    background: #fdfdfd;
    border-color: var(--blue-accent);
  }
  .cal-day-cell.other-month {
    background: #fafafa;
    color: #a1a1aa;
    opacity: 0.55;
  }
  .cal-day-cell.today {
    background: #eff6ff;
  }
  .cal-day-cell.selected {
    outline: 2px solid var(--blue-accent);
    background: #f0f7ff;
    z-index: 2;
  }
  .cal-day-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }
  .cal-day-num {
    font-size: 13px;
    font-weight: 700;
  }
  .cal-today-badge {
    font-size: 10px;
    background: var(--accent-red);
    color: #fff;
    padding: 1px 5px;
    border-radius: 10px;
    font-weight: bold;
  }
  .cal-meeting-count-badge {
    font-size: 10.5px;
    background: #e0e7ff;
    color: #3730a3;
    padding: 1px 5px;
    border-radius: 8px;
    font-weight: 600;
  }
  .cal-day-events {
    display: flex;
    flex-direction: column;
    gap: 3px;
    overflow: hidden;
    max-height: 54px;
  }
  .cal-event-pill {
    font-size: 10px;
    padding: 2px 4px;
    border-radius: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.3;
    display: block;
    text-align: left;
  }
  .cal-event-pill.status-scheduled {
    background: #dbeafe;
    color: #1e40af;
    border-left: 2px solid #2563eb;
  }
  .cal-event-pill.status-pending {
    background: #fef3c7;
    color: #92400e;
    border-left: 2px solid #d97706;
  }
  .cal-event-pill.status-completed {
    background: #dcfce7;
    color: #166534;
    border-left: 2px solid #16a34a;
  }
  .cal-event-more {
    font-size: 10px;
    color: var(--text-muted);
    padding-left: 2px;
  }

  .selected-date-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 5px solid var(--blue-accent);
    padding: 12px 18px;
    border-radius: var(--radius-sm);
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 10px;
  }
  .selected-date-title {
    font-size: 14.5px;
    font-weight: 800;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* Import Live Preview Styles */
  .preview-tab-btn {
    padding: 4px 12px;
    font-size: 11.5px;
    font-weight: 600;
    border: 1px solid var(--border);
    background: var(--card);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .preview-tab-btn.active {
    background: var(--blue-accent);
    color: #fff;
    border-color: var(--blue-accent);
  }
  .import-cal-group {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    margin-bottom: 8px;
  }
  .import-cal-group-header {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .import-card-item {
    background: #ffffff;
    border: 1px solid var(--border);
    border-left: 4px solid var(--blue-accent);
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    margin-bottom: 8px;
  }"""

if css_target in content:
    content = content.replace(css_target, css_replacement, 1)
    print("CSS updated successfully.")
else:
    print("WARNING: css_target not found!")

# 2. Update HTML of pane-supervisor:
# Change title to '主管日程时间轴', add View Mode Switcher, Month Calendar Container, Selected Date Header
html_supervisor_target = """      <!-- Supervisor Daily Timeline with Auto-Detected Free Slots -->
      <div class="timeline-bar-wrap">
        <div class="timeline-header">
          <div>
            <span>🕒 主管日程时间轴 · 槽位占用与空档一览</span>
            <span style="font-size:11px; font-weight:normal; color:var(--text-muted); margin-left:8px;" id="timelineFreeCountBadge">（智能识别可排期空档中...）</span>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <label style="font-size:11.5px; color:var(--text-muted);">排期日期：</label>
            <input type="date" id="timelineDateSelector" style="width:130px; padding:3px 6px; font-size:11.5px;" onchange="handleTimelineDateChange()" />
          </div>
        </div>

        <!-- Timeline Graphic Track -->
        <div class="timeline-track" id="supervisorTimelineTrack">
          <!-- Dynamically populated 08:30 - 18:00 blocks (Busy / Free / Lunch) -->
        </div>

        <!-- Interactive Quick Free Slot Chips -->
        <div class="timeline-free-pills" id="timelineFreeSlotsPills">
          <!-- Populated via JS with free slot recommendation chips -->
        </div>
      </div>

      <!-- Toolbar: Filter & Actions (Featuring Calendar/Table Import Button) -->
      <div class="meeting-toolbar">
        <div class="filter-tabs">
          <button class="filter-btn active" data-filter="all" onclick="filterMeetings('all')">全部会议</button>
          <button class="filter-btn" data-filter="pending" onclick="filterMeetings('pending')">🟡 待安排预约</button>
          <button class="filter-btn" data-filter="scheduled" onclick="filterMeetings('scheduled')">🔵 已排期待开</button>
          <button class="filter-btn" data-filter="completed" onclick="filterMeetings('completed')">🟢 会议已完成</button>
        </div>

        <div style="display: flex; gap: 8px;">
          <!-- Smart Table / Calendar Import Button (Point 2) -->
          <button class="btn btn-primary" onclick="openImportCalendarModal()" title="支持从 Excel、WPS 或日历直接复制表格导入，自动识别时间、主题、汇报人">
            📥 导入表格 / 日历
          </button>
          <button class="btn" onclick="openAddMeetingModal()">
            ➕ 登记单场预约
          </button>
          <button class="btn" onclick="exportTodayMeetingBriefing()" title="一键生成今日会议通报文本，方便发到微信/邮件/工作群">
            📋 复制今日会议通知
          </button>
        </div>
      </div>

      <!-- Meeting Cards List -->
      <div id="meetingCardsList"></div>"""

html_supervisor_replacement = """      <!-- Main Supervisor Schedule Management Toolbar (View Switcher & Actions) -->
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

if html_supervisor_target in content:
    content = content.replace(html_supervisor_target, html_supervisor_replacement, 1)
    print("Supervisor HTML updated successfully.")
else:
    print("WARNING: html_supervisor_target not found!")

# 3. Update HTML of importCalendarModal: accept="*", free format, dual normalization preview
html_modal_target = """  <!-- ================= MODAL: SMART CALENDAR & TABLE IMPORT (Point 2) ================= -->
  <div class="modal-overlay" id="importCalendarModal">
    <div class="modal-box" style="max-width: 660px;">
      <div class="modal-header">
        <div class="modal-title">📥 导入会议日程表格 / 日历（智能自动识别）</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('importCalendarModal')">✕</button>
      </div>
      <div class="modal-body">
        <div style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.55;">
          请在下方文本框中直接粘贴从 <strong>Excel、WPS、Outlook 或聊天记录</strong> 中复制的日程内容，或上传 <code>.csv / .tsv / .txt</code> 表格文件。系统将自动智能提取<strong>【时间】、【会议主题】、【汇报人/与会人】</strong>并自动刷新空档！
        </div>

        <div class="form-row" style="margin-bottom: 12px;">
          <div class="form-group" style="margin-bottom: 0;">
            <label>📅 导入目标排期日期：</label>
            <input type="date" id="importTargetDate" onchange="runCalendarLivePreview()" />
          </div>
          <div style="display:flex; align-items:flex-end; gap:8px;">
            <button class="btn btn-sm" onclick="document.getElementById('calendarFileInput').click()">📁 选择文件导入...</button>
            <input type="file" id="calendarFileInput" accept=".csv,.tsv,.txt" style="display:none;" onchange="handleCalendarFileUpload(event)" />
            <button class="btn btn-sm btn-ghost" onclick="fillSampleCalendarData()">📋 填入示例表格</button>
          </div>
        </div>

        <div class="form-group">
          <label>📋 粘贴表格或日程文本：</label>
          <textarea id="inputImportTableText" style="min-height: 130px; font-family: var(--font-mono); font-size: 12px;" placeholder="支持多列制表符或逗号分隔，例如：&#10;时间&#9;会议主题&#9;汇报人&#10;10:00 - 10:45&#9;中东北非区域Q3预算评审&#9;张总(地南代)&#10;11:00 - 11:30&#9;喀麦隆交付专家定夺&#9;李总(开罗)&#10;14:30 - 15:15&#9;阿尔及利亚大客户合同让利&#9;王总" oninput="runCalendarLivePreview()"></textarea>
        </div>

        <!-- Recognition Status & Live Preview -->
        <div id="importLivePreviewArea" style="display:none; margin-top: 14px;">
          <div style="font-size: 12px; font-weight: 700; color: #16a34a; display:flex; justify-content:space-between; align-items:center;">
            <span id="importPreviewStatusText">🟢 识别成功：共解析出 0 场会议</span>
            <span style="font-weight:normal; color:var(--text-muted); font-size:11px;">确认无误后点击下方按钮导入</span>
          </div>
          <div style="max-height: 160px; overflow-y: auto; border: 1px solid var(--border); border-radius: 4px; margin-top: 6px;">
            <table class="import-preview-table" id="importPreviewTable">
              <thead>
                <tr>
                  <th>时间与时长</th>
                  <th>会议主题</th>
                  <th>汇报人 / 与会人</th>
                </tr>
              </thead>
              <tbody id="importPreviewTableBody"></tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn" onclick="closeModal('importCalendarModal')">取消</button>
        <button type="button" class="btn btn-primary" id="btnConfirmImport" onclick="confirmImportCalendar()" disabled>
          ✅ 确认导入至主管日程
        </button>
      </div>
    </div>
  </div>"""

html_modal_replacement = """  <!-- ================= MODAL: UNIVERSAL SMART CALENDAR & TABLE IMPORT ================= -->
  <div class="modal-overlay" id="importCalendarModal">
    <div class="modal-box" style="max-width: 680px;">
      <div class="modal-header">
        <div class="modal-title">📥 智能识别导入会议日程（自由格式 / Excel / 微信邮件）</div>
        <button class="btn btn-sm btn-ghost" onclick="closeModal('importCalendarModal')">✕</button>
      </div>
      <div class="modal-body">
        <div style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.55;">
          支持<strong>任意自由格式</strong>：直接粘贴 Excel/WPS 表格、微信/企微通知、邮件、自然语言日程，或上传电脑文档（<code>.xlsx / .xls / .csv / .txt</code>）。系统将自动智能识别并规整为<strong>日历版本</strong>与<strong>卡片版本</strong>！
        </div>

        <div class="form-row" style="margin-bottom: 12px;">
          <div class="form-group" style="margin-bottom: 0;">
            <label>📅 默认排期日期（如文本未注明日期的默认归属）：</label>
            <input type="date" id="importTargetDate" onchange="runCalendarLivePreview()" />
          </div>
          <div style="display:flex; align-items:flex-end; gap:8px;">
            <!-- accept="*" allows selecting ANY document from computer without macOS Finder filtering -->
            <button class="btn btn-sm" onclick="document.getElementById('calendarFileInput').click()">📁 选择电脑文档导入...</button>
            <input type="file" id="calendarFileInput" accept="*" style="display:none;" onchange="handleCalendarFileUpload(event)" />
            <button class="btn btn-sm btn-ghost" onclick="fillSampleCalendarData()">📋 填入示例数据</button>
          </div>
        </div>

        <div class="form-group">
          <label>📋 自由文本粘贴框（支持表格多列、自然语言、段落、微信通知等任意形式）：</label>
          <textarea id="inputImportTableText" style="min-height: 120px; font-family: var(--font-mono); font-size: 12px;" placeholder="支持自由输入任何格式，例如：&#10;1. 表格复制：10:00 - 10:45&#9;中东北非区域Q3预算评审&#9;张总(地南代)&#10;2. 自然语言：9月25日下午2点半至3点15分 刚果金代表处业务对齐 汇报人：陈部长 决策点：审批工程预算&#10;3. 会议通知：明天上午10点在1号会议室召开非洲8代表处协同例会，请李总汇报业务进展，预计时长60分钟" oninput="runCalendarLivePreview()"></textarea>
        </div>

        <!-- Recognition Status & Dual Normalization Live Preview (日历规整版本 / 卡片规整版本) -->
        <div id="importLivePreviewArea" style="display:none; margin-top: 14px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:8px;">
            <span id="importPreviewStatusText" style="font-size: 12px; font-weight: 700; color: #16a34a;">🟢 智能识别成功：已规整 0 场会议</span>
            <div style="display:flex; gap:6px;">
              <button type="button" class="preview-tab-btn active" id="btnPreviewTabCal" onclick="switchImportPreviewTab('cal')">📅 规整日历版本</button>
              <button type="button" class="preview-tab-btn" id="btnPreviewTabCard" onclick="switchImportPreviewTab('card')">🃏 规整卡片版本</button>
            </div>
          </div>

          <!-- Calendar Formatted Version Wrap -->
          <div id="importCalPreviewWrap" style="max-height: 200px; overflow-y: auto; border: 1px solid var(--border); border-radius: 6px; padding: 10px; background: #fafafa;">
            <!-- Rendered by runCalendarLivePreview() -->
          </div>

          <!-- Card Formatted Version Wrap -->
          <div id="importCardPreviewWrap" style="display:none; max-height: 200px; overflow-y: auto; border: 1px solid var(--border); border-radius: 6px; padding: 10px; background: #fafafa;">
            <!-- Rendered by runCalendarLivePreview() -->
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn" onclick="closeModal('importCalendarModal')">取消</button>
        <button type="button" class="btn btn-primary" id="btnConfirmImport" onclick="confirmImportCalendar()" disabled>
          ✅ 确认导入并规整至主管日程
        </button>
      </div>
    </div>
  </div>"""

if html_modal_target in content:
    content = content.replace(html_modal_target, html_modal_replacement, 1)
    print("Modal HTML updated successfully.")
else:
    print("WARNING: html_modal_target not found!")

with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Assemble script part 1 (HTML/CSS) written successfully.")

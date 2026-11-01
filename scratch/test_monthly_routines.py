#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(BASE_DIR, "index.html")
DIST_INDEX_HTML = os.path.join(BASE_DIR, "dist", "index.html")

def test_monthly_routines():
    print("Testing Monthly Routine Timeline...")
    for path, name in [(INDEX_HTML, "index.html"), (DIST_INDEX_HTML, "dist/index.html")]:
        assert os.path.exists(path), f"{name} does not exist"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check DOM elements
        required_elements = [
            'id="pane-links"',
            'id="monthlyTimelineContainer"',
            'id="currentRoutineMonthDisplay"',
            'id="statMonthlyProgress"',
            'id="statMonthlyNextDate"',
            'id="routineProgressFill"',
            'id="monthlyRoutineModal"',
            'id="linksCollapseBody"',
            'id="linksCategoryTabs"',
            'id="linksFullGrid"',
            'id="btnRemindTomorrowMeetings"',
            'id="tomorrowReminderModal"',
            'id="inputReminderDate"',
            'id="reminderMessagePreview"',
        ]
        for elem in required_elements:
            assert elem in content, f"Missing {elem} in {name}"

        # Check required user content keywords
        keywords = [
            "开部门例会（内部）",
            "发送技术运营月报 + 遗留任务双周报",
            "开NIS部门例会",
            "发送遗留任务双周报",
            "每月 9 号",
            "每月第二周",
            "每月 20 号",
            "每月第四周",
            "月度闯关",
            "计划时间：",
            "提醒领导明日会议",
        ]
        for kw in keywords:
            assert kw in content, f"Missing keyword '{kw}' in {name}"

        # Check JS function names
        js_functions = [
            "renderMonthlyRoutines",
            "toggleMonthlyRoutineComplete",
            "changeRoutineMonth",
            "resetRoutineMonthToCurrent",
            "getRoutineDateDetails",
            "toggleLinksCollapse",
            "openAddMonthlyRoutineModal",
            "openEditMonthlyRoutineModal",
            "saveMonthlyRoutineItem",
            "deleteMonthlyRoutine",
            "openTomorrowMeetingReminderModal",
            "setReminderDateTomorrow",
            "updateTomorrowReminderPreview",
            "copyTomorrowReminderContent",
        ]
        for fn in js_functions:
            assert fn in content, f"Missing JS function {fn} in {name}"

        # Check JavaScript syntax execution via Node
        import subprocess
        res = subprocess.run([
            "node", "-e",
            f"""
            const fs = require('fs');
            const html = fs.readFileSync('{path}', 'utf8');
            const scripts = html.match(/<script>([\\s\\S]*?)<\\/script>/g) || [];
            for (let i = 0; i < scripts.length; i++) {{
              const code = scripts[i].replace(/<\\/?script>/g, '');
              new Function(code);
            }}
            """
        ], capture_output=True, text=True)
        assert res.returncode == 0, f"JS Syntax error in {name}: {res.stderr}"

        print(f"✓ All checks & JS syntax passed for {name}!")

    print("✨ All Monthly Routine tests passed successfully!")

if __name__ == "__main__":
    test_monthly_routines()

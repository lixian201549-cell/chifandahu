import re

with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Update initSeeds with minuter and reporter
seeds_target = """    setData(STORAGE_KEYS.MEETINGS, [
      {
        id: 1,
        date: todayStr,
        time: "10:00",
        duration: 45,
        subject: "中东北非区域 Q3 交付资源倾斜及关键决策评审",
        background: "喀麦隆与科特迪瓦代表处重点工程交付进入攻坚期，一线技术专家面临紧缺，需主管定夺是否从地区部统一调配高级技术专家现场支援并追加差旅额度。",
        decision: "1. 是否同意科特迪瓦代表处追加2名资深交付架构师驻场？\\\\n2. 喀麦隆大客户合同备件本地采购预算审批通过与否？",
        attendees: "主管、李总(开罗交付部)、张总(科特迪瓦代)、财务BP、HRG",
        requester: "地区部交付与服务部 · 王秘书",
        location: "主管办公室 / 线上 WeLink 889-201",
        status: "scheduled",
        priority: "high",
        notes: "已提前打印现场风险排查表与两代表处人员盘点清单"
      },
      {
        id: 2,
        date: todayStr,
        time: "14:30",
        duration: 30,
        subject: "刚果（金）及阿尔及利亚代表处月度经营例行汇报",
        background: "阿尔及利亚代表处受当地外汇管制影响，部分重点客户回款面临超期风险，特向主管当面汇报风险收敛措施并申请政策特批。",
        decision: "1. 阿尔及利亚客户付款账期延长申请是否特批？\\\\n2. 刚果（金）办事处新安保防护方案终审确认。",
        attendees: "主管、阿尔及利亚代代表、刚果代代表、法务BP",
        requester: "刚果代表处秘书处",
        location: "1号会议室",
        status: "scheduled",
        priority: "medium",
        notes: "提醒主管会前签字授权委托书"
      },
      {
        id: 3,
        date: todayStr,
        time: "16:30",
        duration: 45,
        subject: "8 代表处跨区协同机制与行政支持新规范汇报",
        background: "梳理跨开罗(UTC+2)、阿尔及尔(UTC+1)、阿比让(UTC+0)等不同时区的行政响应标准，建立秘书处跨时区紧急调度绿色通道。",
        decision: "1. 跨时区通用会议窗口是否固定为开罗时间 11:00 - 17:00？\\\\n2. 统一差旅紧急代订与商务接待标准确认。",
        attendees: "主管、区域行政总监、各代表处综合行政主管",
        requester: "区域综合秘书处",
        location: "主管办公室",
        status: "pending",
        priority: "routine",
        notes: "需提前准备各代表处时差对比对照表"
      },
      {
        id: 4,
        date: dateTomorrow,
        time: "11:00",
        duration: 45,
        subject: "摩洛哥代表处高层客户来访接待与商机定夺",
        background: "摩洛哥大客户代表团将于开罗中转，特申请主管当面会见并敲定战略合作备忘录。",
        decision: "1. 敲定联合实验室共建框架；\\\\n2. 审批定制化交付条款让利权限。",
        attendees: "主管、摩洛哥总代表、商务专家",
        requester: "摩洛哥代表处总办",
        location: "贵宾会客室",
        status: "scheduled",
        priority: "high",
        notes: "已确认阿拉伯语与法语同声传译就位"
      },
      {
        id: 5,
        date: dateTomorrow,
        time: "15:00",
        duration: 60,
        subject: "塞内加尔达喀尔港口工程回款攻坚专题会",
        background: "塞内加尔达喀尔重点港口工程进入整体验收阶段，梳理回款时间表并部署防范风险预案。",
        decision: "1. 确定下阶段付款节点追讨策略；\\\\n2. 批准补充备件保修函签署。",
        attendees: "主管、塞内加尔总代表、交付总监、法务部",
        requester: "西非项目群经理",
        location: "2号会议室",
        status: "scheduled",
        priority: "medium",
        notes: "需准备西非法郎外汇对冲分析表"
      },
      {
        id: 6,
        date: dateDayAfter,
        time: "10:30",
        duration: 45,
        subject: "埃及代表处本地化人才梯队建设汇报",
        background: "深化埃及与北非本地技术专家招聘与培养，建立开罗中枢培训基地。",
        decision: "1. 审批2026-2027年度本地大学联合培养计划预算。",
        attendees: "主管、区域人力资源总监、开罗培训中心负责人",
        requester: "地区部HRBP",
        location: "主管办公室",
        status: "pending",
        priority: "routine",
        notes: "会前准备开罗大学合作协议草案"
      }
    ]);"""

seeds_replacement = """    setData(STORAGE_KEYS.MEETINGS, [
      {
        id: 1,
        date: todayStr,
        time: "10:00",
        duration: 45,
        durationHours: "0.75",
        subject: "中东北非区域 Q3 交付资源倾斜及关键决策评审",
        background: "喀麦隆与科特迪瓦代表处重点工程交付进入攻坚期，一线技术专家面临紧缺，需主管定夺是否从地区部统一调配高级技术专家现场支援并追加差旅额度。",
        decision: "1. 是否同意科特迪瓦代表处追加2名资深交付架构师驻场？\\\\n2. 喀麦隆大客户合同备件本地采购预算审批通过与否？",
        reporter: "李总(开罗交付部)",
        minuter: "王秘书",
        attendees: "主管、李总(开罗交付部)、张总(科特迪瓦代)、财务BP、HRG",
        requester: "地区部交付与服务部 · 王秘书",
        location: "主管办公室 / 线上 WeLink 889-201",
        status: "scheduled",
        priority: "high",
        notes: "已提前打印现场风险排查表与两代表处人员盘点清单"
      },
      {
        id: 2,
        date: todayStr,
        time: "14:30",
        duration: 30,
        durationHours: "0.50",
        subject: "刚果（金）及阿尔及利亚代表处月度经营例行汇报",
        background: "阿尔及利亚代表处受当地外汇管制影响，部分重点客户回款面临超期风险，特向主管当面汇报风险收敛措施并申请政策特批。",
        decision: "1. 阿尔及利亚客户付款账期延长申请是否特批？\\\\n2. 刚果（金）办事处新安保防护方案终审确认。",
        reporter: "阿尔及利亚代代表",
        minuter: "李秘书",
        attendees: "主管、阿尔及利亚代代表、刚果代代表、法务BP",
        requester: "刚果代表处秘书处",
        location: "1号会议室",
        status: "scheduled",
        priority: "medium",
        notes: "提醒主管会前签字授权委托书"
      },
      {
        id: 3,
        date: todayStr,
        time: "16:30",
        duration: 45,
        durationHours: "0.75",
        subject: "8 代表处跨区协同机制与行政支持新规范汇报",
        background: "梳理跨开罗(UTC+2)、阿尔及尔(UTC+1)、阿比让(UTC+0)等不同时区的行政响应标准，建立秘书处跨时区紧急调度绿色通道。",
        decision: "1. 跨时区通用会议窗口是否固定为开罗时间 11:00 - 17:00？\\\\n2. 统一差旅紧急代订与商务接待标准确认。",
        reporter: "区域综合秘书处",
        minuter: "王秘书",
        attendees: "主管、区域行政总监、各代表处综合行政主管",
        requester: "区域综合秘书处",
        location: "主管办公室",
        status: "pending",
        priority: "routine",
        notes: "需提前准备各代表处时差对比对照表"
      },
      {
        id: 4,
        date: dateTomorrow,
        time: "11:00",
        duration: 45,
        durationHours: "0.75",
        subject: "摩洛哥代表处高层客户来访接待与商机定夺",
        background: "摩洛哥大客户代表团将于开罗中转，特申请主管当面会见并敲定战略合作备忘录。",
        decision: "1. 敲定联合实验室共建框架；\\\\n2. 审批定制化交付条款让利权限。",
        reporter: "摩洛哥总代表",
        minuter: "陈秘书",
        attendees: "主管、摩洛哥总代表、商务专家",
        requester: "摩洛哥代表处总办",
        location: "贵宾会客室",
        status: "scheduled",
        priority: "high",
        notes: "已确认阿拉伯语与法语同声传译就位"
      },
      {
        id: 5,
        date: dateTomorrow,
        time: "15:00",
        duration: 60,
        durationHours: "1.00",
        subject: "塞内加尔达喀尔港口工程回款攻坚专题会",
        background: "塞内加尔达喀尔重点港口工程进入整体验收阶段，梳理回款时间表并部署防范风险预案。",
        decision: "1. 确定下阶段付款节点追讨策略；\\\\n2. 批准补充备件保修函签署。",
        reporter: "塞内加尔总代表",
        minuter: "赵秘书",
        attendees: "主管、塞内加尔总代表、交付总监、法务部",
        requester: "西非项目群经理",
        location: "2号会议室",
        status: "scheduled",
        priority: "medium",
        notes: "需准备西非法郎外汇对冲分析表"
      },
      {
        id: 6,
        date: dateDayAfter,
        time: "10:30",
        duration: 45,
        durationHours: "0.75",
        subject: "埃及代表处本地化人才梯队建设汇报",
        background: "深化埃及与北非本地技术专家招聘与培养，建立开罗中枢培训基地。",
        decision: "1. 审批2026-2027年度本地大学联合培养计划预算。",
        reporter: "开罗培训中心负责人",
        minuter: "王秘书",
        attendees: "主管、区域人力资源总监、开罗培训中心负责人",
        requester: "地区部HRBP",
        location: "主管办公室",
        status: "pending",
        priority: "routine",
        notes: "会前准备开罗大学合作协议草案"
      }
    ]);"""

if seeds_target in text:
    text = text.replace(seeds_target, seeds_replacement, 1)
    print("Seeds successfully updated with reporter and minuter.")
else:
    print("WARNING: seeds_target not found in exact form!")

# Add intelligent tabular classifier into parseUniversalScheduleText
# Replace the fallback section with the tabular classifier
heuristic_target = """    // 5. Fallback: Universal NLP / Free Form extractor
    let itemDate = currentDate;"""

heuristic_replacement = """    // 5. Intelligent Tabular Classifier (Handles unlabelled rows like: 10:00 - 10:45 \\t 主题 \\t 汇报人 \\t 参会人 \\t 纪要人 \\t 0.75)
    if (parts.length >= 3 && !colMap) {
      let tVal = '', sVal = '', rVal = '', aVal = '', mVal = '', dVal = '';

      for (let p of parts) {
        if (/\\d{1,2}:\\d{2}/.test(p) && !tVal) {
          tVal = p;
        } else if (/^[0-9.]+\\s*(?:h|小时|m|分钟)?$/i.test(p) && !dVal) {
          dVal = p;
        } else if (/(?:秘书|纪要)/.test(p) && !mVal && p.length <= 10) {
          mVal = p;
        } else if (/(?:主管|交付部|财务|HR|BP|法务)/.test(p) || p.includes('、') || p.includes(',')) {
          if (!aVal) aVal = p;
        } else if (/(?:总|部长|经理|主任|专家|代表)/.test(p) && p.length <= 12 && !rVal) {
          rVal = p;
        } else if (!sVal) {
          sVal = p;
        }
      }

      if (sVal && !/^(?:星期|周)[一二三四五六日天]$/.test(sVal)) {
        let durMins = 45;
        if (dVal) {
          const num = parseFloat(dVal.replace(/[^0-9.]/g, ''));
          if (!isNaN(num) && num > 0) {
            durMins = num <= 5 ? Math.round(num * 60) : Math.round(num);
          }
        }

        let startTime = '10:00';
        if (tVal) {
          const rangeM = tVal.match(/(\\d{1,2}:\\d{2})(?:\\s*[-~至到]\\s*(\\d{1,2}:\\d{2}))?/);
          if (rangeM) {
            startTime = padTime(rangeM[1]);
            if (rangeM[2]) {
              const [sh, sm] = rangeM[1].split(':').map(Number);
              const [eh, em] = rangeM[2].split(':').map(Number);
              const diff = (eh * 60 + em) - (sh * 60 + sm);
              if (diff > 0 && diff <= 480) durMins = diff;
            }
          }
        } else {
          startTime = defaultSlots[currentSlotIdx % defaultSlots.length];
          currentSlotIdx++;
        }

        results.push({
          id: Date.now() + Math.floor(Math.random() * 1000000),
          date: currentDate,
          time: startTime,
          duration: durMins,
          durationHours: (durMins / 60).toFixed(2),
          subject: sVal,
          decision: `1. 审议《${sVal}》关键决策要点，确定推进方案。`,
          reporter: rVal || '待确定汇报人',
          attendees: aVal || (rVal ? '主管、' + rVal : '主管、相关参会人'),
          minuter: mVal || '秘书处',
          requester: rVal || '表格导入',
          location: '主管办公室 / 线上会议室',
          status: 'scheduled',
          priority: 'medium',
          notes: '由无表头表格智能分类识别导入'
        });
        continue;
      }
    }

    // 6. Fallback: Universal NLP / Free Form extractor
    let itemDate = currentDate;"""

if heuristic_target in text:
    text = text.replace(heuristic_target, heuristic_replacement, 1)
    print("Intelligent tabular classifier added successfully.")
else:
    print("WARNING: heuristic_target not found!")

with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("assemble_final_app.py updated.")

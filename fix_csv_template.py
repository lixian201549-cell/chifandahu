with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx_start = text.find('function downloadStandardExcelTemplate() {')
idx_end = text.find('showToast("📥 标准 Excel CSV 模板已下载！");\n}') + len('showToast("📥 标准 Excel CSV 模板已下载！");\n}')

clean_func = """function downloadStandardExcelTemplate() {
  const rows = [
    "*会议主题（关键任务）,*议题背景/决策要点说明,*汇报人,*参会人,*纪要人,*预约时长（H）,排期日期,开始时间",
    "中东北非区域Q3交付资源评审,审批重点交付架构师驻场与预算特批,张总(地南代),主管、李总、财务BP,王秘书,0.75,2026-09-24,10:00",
    "阿尔及利亚代表处外汇与回款复盘,特批客户付款账期与汇率对冲,王总,主管、法务部、商务部,李秘书,1.0,2026-09-25,14:30",
    "刚果金代表处工程进展对齐,审批新安保防护与施工里程碑,陈部长,主管、交付部,赵秘书,0.5,2026-09-25,16:00"
  ];
  const csvContent = '\\uFEFF' + rows.join('\\\\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', '主管日程标准导入模板.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  showToast("📥 标准 Excel CSV 模板已下载！");
}"""

if idx_start != -1 and idx_end != -1:
    text = text[:idx_start] + clean_func + text[idx_end:]
    with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("CSV template function fixed.")
else:
    print("Indices not found:", idx_start, idx_end)

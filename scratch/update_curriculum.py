import json

scenarios_pool = [
    # Day 1
    {
        "day": 1,
        "words": [
            {"word": "Prioritize", "phonetic": "/praɪˈɒrətaɪz/", "pos": "v. 动词", "def": "按优先顺序处理；优先考虑", "exampleEn": "Let's prioritize these action items before the team sync.", "exampleCn": "在团队同步会之前，我们先理清这几项任务的优先级。"},
            {"word": "Deliverable", "phonetic": "/dɪˈlɪvərəbl/", "pos": "n. 名词", "def": "可交付成果；阶段性成果", "exampleEn": "The team committed to submitting all deliverables by Friday afternoon.", "exampleCn": "团队承诺在周五下午前提交所有的交付成果。"},
            {"word": "Alignment", "phonetic": "/əˈlaɪnmənt/", "pos": "n. 名词", "def": "对齐；达成共识", "exampleEn": "We need cross-functional alignment before rolling out the plan.", "exampleCn": "在推出方案之前，我们需要跨部门达成共识。"}
        ],
        "sentences": [
            {"scenario": "跨部门协作推进", "en": "Let's set up a quick 15-minute touchpoint to ensure we're all on the same page regarding the project timeline.", "cn": "我们开一个15分钟的简短碰头会，确保大家对项目排期达成完全共识。", "tip": "on the same page 是职场中表示‘意见达成一致/步调协同’的地道表达。"},
            {"scenario": "办公室茶歇寒暄", "en": "I'm heading to the pantry for a coffee refill—would anyone like me to grab them one?", "cn": "我正要去茶水间续杯咖啡，有人需要我顺便带一杯吗？", "tip": "在茶水间主动询问同事是否需要咖啡，是增进职场人际关系的好习惯。"},
            {"scenario": "线上会议与屏幕共享", "en": "Kevin, you're currently on mute—could you unmute yourself and share your screen?", "cn": "凯文，你现在静音了——能打开麦克风并共享一下你的屏幕吗？", "tip": "You're on mute 是现代线上办公出镜率极高的经典口语。"}
        ]
    },
    # Day 2
    {
        "day": 2,
        "words": [
            {"word": "Consolidate", "phonetic": "/kənˈsɒlɪdeɪt/", "pos": "v. 动词", "def": "汇总；合并；巩固", "exampleEn": "I will consolidate feedback from all departments into a single report.", "exampleCn": "我将把各部门的反馈意见汇总成一份统一报告。"},
            {"word": "Feasibility", "phonetic": "/ˌfiːzəˈbɪləti/", "pos": "n. 名词", "def": "可行性；可实施度", "exampleEn": "We conducted a feasibility study before purchasing the new software.", "exampleCn": "在采购新软件系统之前，我们进行了详尽的可行性评估。"},
            {"word": "Contingency", "phonetic": "/kənˈtɪndʒənsi/", "pos": "n. 名词", "def": "应急预案；突发应对", "exampleEn": "We need a contingency plan in case the supply chain experiences delays.", "exampleCn": "我们需要一份应急预案，以防供应链环节发生延误。"}
        ],
        "sentences": [
            {"scenario": "项目进度与工期协调", "en": "Could you provide a ballpark estimate on when the revised data model will be ready?", "cn": "你能大概预估一下修改后的数据模型什么时候能准备好吗？", "tip": "ballpark estimate 指‘大致估算、粗略预估’，极为口语常用。"},
            {"scenario": "办公设备与IT求助", "en": "The shared printer on the 3rd floor is showing a paper jam error again; I've just logged an IT ticket.", "cn": "三楼的共享打印机又提示卡纸了，我刚在系统里提交了IT维修工单。", "tip": "log a ticket 指在公司内部服务台‘提报运维工单’。"},
            {"scenario": "工作交接与下班问候", "en": "I've wrapped up all urgent items for today and sent you the handover notes by email. Have a great evening!", "cn": "我今天的所有紧急事项都已处理完毕，交接清单已发你邮箱。祝今晚愉快！", "tip": "下班前简短告知交接进度，彰显专业有交代的工作作风。"}
        ]
    },
    # Day 3
    {
        "day": 3,
        "words": [
            {"word": "Facilitate", "phonetic": "/fəˈsɪlɪteɪt/", "pos": "v. 动词", "def": "协助；促进；使便利", "exampleEn": "Our team will facilitate the cross-departmental workshop tomorrow.", "exampleCn": "我们团队明天将协助主持跨部门研讨会。"},
            {"word": "Stakeholder", "phonetic": "/ˈsteɪkhəʊldə(r)/", "pos": "n. 名词", "def": "利益相关方；关键业务干系人", "exampleEn": "All key stakeholders agreed on the proposed timeline adjustments.", "exampleCn": "所有关键干系人均已同意提出的时间表调整。"},
            {"word": "Discrepancy", "phonetic": "/dɪˈskrepənsi/", "pos": "n. 名词", "def": "差异；不符之处", "exampleEn": "We noticed a slight discrepancy between the invoice and the purchase order.", "exampleCn": "我们注意到发票和采购订单之间存在细微差异。"}
        ],
        "sentences": [
            {"scenario": "差旅报销与财务沟通", "en": "Please ensure you upload all digital VAT receipts before the monthly expense submission cutoff.", "cn": "请务必在月度报销截止日前上传所有增值税电子发票。", "tip": "submission cutoff 指‘截止提交时间节点’。"},
            {"scenario": "头脑风暴与创意讨论", "en": "There are no bad ideas here—let's think outside the box to streamline our user onboarding.", "cn": "咱们畅所欲言没有坏想法——跳出固有思维，看看怎么精简用户上手流程。", "tip": "think outside the box 表示‘跳出思维定势、打破常规’。"},
            {"scenario": "客户来访接待", "en": "Welcome to our office! May I take your coat, and would you prefer still or sparkling water?", "cn": "欢迎莅临我们办公室！我帮您挂外套，请问您喝纯净水还是气泡水？", "tip": "接待外宾时的优雅职业开场白。"}
        ]
    }
]

# We will load the full 31 days and update scenarios and tips to be broad workplace office dialogues
with open('english_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Topic scenarios pool to cycle through for all 31 days
office_scenarios = [
    ("跨部门协作与项目排期", "Could we block out 30 minutes next Tuesday to review the quarterly milestone deliverables?", "我们下周二能预留30分钟对齐一下季度里程碑交付成果吗？", "block out time 表示‘在日历中预留/锁定时间’。"),
    ("办公室茶水间闲聊", "How was your weekend? Did you do anything fun in the nice weather?", "周末过得怎么样？天气这么好，有没有去哪儿玩玩？", "周一早晨茶水间的经典破冰寒暄，快速拉近同事关系。"),
    ("IT设备与网络支持", "My laptop won't connect to the guest Wi-Fi; could you check if my VPN certificate expired?", "我的电脑连不上访客Wi-Fi了，能帮我看看是不是VPN证书过期了吗？", "跨国公司办公中遇到网络与VPN故障时的标准描述。"),
    ("会议室预定与协调", "Excuse me, we booked Conference Room B starting at 2:00 PM; are you almost wrapped up here?", "不好意思打扰一下，我们预定了下午两点开始的B会议室，请问你们快结束了吗？", "礼貌提醒前一场会议超时的得体句型。"),
    ("出差审批与财务报销", "The finance team requires approval from the department head before processing overseas flight expenses.", "财务部门要求在报销国际机票费用前，必须先获得部门负责人的审批。", "财务流程沟通中的清晰陈述句。"),
    ("新员工入职引导", "Feel free to ping me on Slack anytime if you have any questions about our internal wiki or workflow.", "如果你对内部知识库或工作流有任何疑问，随时在办公软件上找我！", "ping me 是互联网与现代办公室中‘私信我/联系我’的超高频口语。"),
    ("客户接待与商务拜访", "Our meeting room is ready on the 8th floor. Please follow me, and we'll get started right away.", "我们8楼的会议室已准备就绪。请随我来，我们马上开始。", "商务接待引导访客时的标准职业礼仪。"),
    ("紧急交付与互相支援", "I'm currently swamped with the Q3 review deck; could you help cover the weekly status update call?", "我现在被Q3评审材料搞得抽不开身，能帮我代开一下周例会吗？", "swamped with 表示‘手头事情堆积如山、忙得不可开交’。"),
    ("供应商谈判与订单核对", "We need to clarify the warranty terms and shipment lead time before signing off on the agreement.", "在最终签署协议之前，我们需要先确认质保条款和发货交付周期。", "lead time 指‘从下订单到交货的生产交付周期’。"),
    ("团队午餐与订餐破冰", "A few of us are ordering Thai food for lunch today—do you want to join in?", "我们几个人今天中午准备点泰国菜外卖，你想一起拼单吗？", "午餐邀请同事拼单的自然表达。"),
    ("线上会议音画调试", "Could everyone please turn on their cameras for a quick team group photo before we wrap up?", "在散会前，大家能打开摄像头我们一起截个合影吗？", "跨国远程会议收尾时常用的暖心互动句。"),
    ("休假通知与工作交接", "I'll be out of office with limited access to email next week; please reach out to Sarah for urgent matters.", "我下周休假外出且邮件查收受限，如有紧急事项请直接联系莎拉。", "经典标准的职场自动回复与交接文案。"),
    ("头脑风暴与方案讨论", "Let's put a pin in that topic for now and circle back once we have the customer survey data.", "我们先把这个议题搁置一下，等拿到客户问卷数据后再回过头来讨论。", "put a pin in it 是职场中‘暂时搁置、稍后讨论’的地道成语。"),
    ("季度复盘与表扬认可", "Shout-out to the delivery team for going the extra mile to hit our launch target on schedule!", "向交付团队致敬，感谢大家全力以赴让我们如期达成上线目标！", "going the extra mile 表示‘额外付出努力、加倍尽责’。")
]

for i, day_obj in enumerate(data):
    s_list = []
    # Pick 3 varied scenarios for each day
    base_idx = (i * 3) % len(office_scenarios)
    for k in range(3):
        item = office_scenarios[(base_idx + k) % len(office_scenarios)]
        s_list.append({
            "scenario": item[0],
            "en": item[1],
            "cn": item[2],
            "tip": item[3]
        })
    day_obj["sentences"] = s_list

with open('english_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Successfully updated english_data.json with diverse office situations!')

# -*- coding: utf-8 -*-
"""
Script to generate 31 days of professional Business Travel English curriculum for Snoopy's Little Lab.
Tailored for executive assistants, overseas rep office coordinators, and traveling leaders.
"""

import json

curriculum = [
    {
        "day": 1,
        "topic": "✈️ 航班行程单与电子客票",
        "words": [
            {
                "word": "Itinerary",
                "phonetic": "/aɪˈtɪnərəri/",
                "pos": "n. 名词",
                "def": "行程安排；详细旅行路线单",
                "exampleEn": "I have forwarded the director's flight itinerary for the Cairo-Casablanca trip to your inbox.",
                "exampleCn": "我已将领导前往开罗和卡萨布兰卡的航班行程单发送至您的邮箱。"
            },
            {
                "word": "Layover",
                "phonetic": "/ˈleɪoʊvər/",
                "pos": "n. 名词",
                "def": "中途停留；转机等待时间",
                "exampleEn": "There is a brief two-hour layover in Dubai before connecting to our onward flight to Rabat.",
                "exampleCn": "在转乘前往拉巴特的后续航班之前，我们在迪拜有两小时的短暂中转停留。"
            },
            {
                "word": "Concourse",
                "phonetic": "/ˈkɒnkɔːs/",
                "pos": "n. 名词",
                "def": "机场候机大厅；中央大厅",
                "exampleEn": "Our departure gate has been moved to Concourse B, right next to the executive lounge.",
                "exampleCn": "我们的登机口已改至B候机大厅，就在行政贵宾休息室正隔壁。"
            }
        ],
        "sentences": [
            {
                "scenario": "确认领导联程航班行程",
                "en": "Could you please double-check the connection window during our transit in Istanbul to ensure luggage through-check?",
                "cn": "能否麻烦您核实一下我们在伊斯坦布尔中转的接驳时间，并确认行李能否直接直挂？",
                "tip": "through-check 指‘行李直挂’，国际多程中转时必须向值机地勤核对的黄金术语。"
            },
            {
                "scenario": "向海外代表处通报航班时刻",
                "en": "The delegation is scheduled to touch down at Terminal 3 at 18:45 local time tomorrow evening.",
                "cn": "代表团预计将于明晚当地时间18点45分降落于3号航站楼。",
                "tip": "touch down 比 arrive 更具商务差旅报告质感，意为‘客机落地进港’。"
            },
            {
                "scenario": "向领导汇报行程备忘",
                "en": "All e-tickets and boarding passes have been saved to your digital wallet for seamless offline access.",
                "cn": "所有电子客票和登机牌均已同步保存至您的手机卡包，方便离线快速调取查看。",
                "tip": "seamless offline access 体现细致入微的秘书差旅支持专业度。"
            }
        ]
    },
    {
        "day": 2,
        "topic": "🎫 机场值机与行李托运",
        "words": [
            {
                "word": "Baggage Allowance",
                "phonetic": "/ˈbæɡɪdʒ əˈlaʊəns/",
                "pos": "n. 短语",
                "def": "免费行李额度",
                "exampleEn": "Our business class booking includes two pieces of checked baggage allowance up to 32kg each.",
                "exampleCn": "我们的商务舱机票包含两件每件上限32公斤的托运行李额度。"
            },
            {
                "word": "Fragile",
                "phonetic": "/ˈfrædʒaɪl/",
                "pos": "adj. 形容词",
                "def": "易碎的；需轻拿轻放的",
                "exampleEn": "Please attach a fragile sticker to this suitcase, as it contains sensitive electronic demo units.",
                "exampleCn": "请在这个行李箱上贴上易碎品标签，里面装有精密的电子样机设备。"
            },
            {
                "word": "Aisle Seat",
                "phonetic": "/aɪl siːt/",
                "pos": "n. 短语",
                "def": "靠过道座位",
                "exampleEn": "The director prefers an aisle seat in row 5 for easier movement during long-haul flights.",
                "exampleCn": "领导偏好第5排靠过道的座位，以便在长途飞行期间方便起身出入。"
            }
        ],
        "sentences": [
            {
                "scenario": "在机场值机柜台办理手续",
                "en": "Good morning, we have two passengers checking in for Flight MS778 to Cairo with two pieces of luggage.",
                "cn": "早上好，我们有两位旅客办理前往开罗的MS778次航班值机，共两件托运行李。",
                "tip": "标准干练的机场柜台值机开场句，清晰交代人数、航班号与行李件数。"
            },
            {
                "scenario": "询问超重行李政策",
                "en": "Is it possible to purchase extra luggage weight online now to avoid excess baggage fees at the gate?",
                "cn": "请问现在可以在线上增购行李额度吗，以避免在登机口产生高额的超重费？",
                "tip": "excess baggage fees 是国际航线托运常见的‘行李超重罚款’。"
            },
            {
                "scenario": "申请提前打印返程登机牌",
                "en": "Could you issue both boarding passes now so we won't need to re-check our bags in transit?",
                "cn": "请问能否一并打印两段航程的登机牌，这样中转时我们就无需重新提取托运行李了？",
                "tip": "在中转联程票务中，提前打齐登机牌可大幅节省过站安检与跑登机口时间。"
            }
        ]
    },
    {
        "day": 3,
        "topic": "🛂 快速安检与优先登机",
        "words": [
            {
                "word": "Fast Track",
                "phonetic": "/fɑːst træk/",
                "pos": "n. 短语",
                "def": "快速通行通道；贵宾优先安检口",
                "exampleEn": "Business class passengers can use the Fast Track lane to clear security within minutes.",
                "exampleCn": "商务舱旅客可走Fast Track快速通道，数分钟内便可完成安检。"
            },
            {
                "word": "Carry-on",
                "phonetic": "/ˈkæri ɒn/",
                "pos": "n./adj.",
                "def": "手提登机行李（的）",
                "exampleEn": "Please ensure all portable lithium battery power banks remain in your carry-on bag.",
                "exampleCn": "请确保所有便携式锂电池充电宝均放置于手提登机包内，严禁托运。"
            },
            {
                "word": "Priority Boarding",
                "phonetic": "/praɪˈɒrəti ˈbɔːdɪŋ/",
                "pos": "n. 短语",
                "def": "优先登机特权",
                "exampleEn": "Priority boarding is now being called for Zone 1 and SkyTeam elite tier members.",
                "exampleCn": "现在广播通知第1登机区旅客及天合联盟精英会员开始优先登机。"
            }
        ],
        "sentences": [
            {
                "scenario": "引导领导前往快速安检通道",
                "en": "The general security queue is backed up, but our tickets qualify for the VIP Fast Track lane on the left.",
                "cn": "普通安检通道排队较长，但我们的机票可以走左侧的VIP快速安检专道。",
                "tip": "backed up 在口语中表示‘排长队积压/堵塞’，地道生动。"
            },
            {
                "scenario": "在机舱内协调行李舱位",
                "en": "Excuse me, flight attendant, could you assist in finding overhead bin space near seat 3A?",
                "cn": "打扰一下乘务员，能否协助在3A座位附近找一个行李架空位放手提包？",
                "tip": "overhead bin 是机舱头顶‘行李置物仓’的标准航空英文表达。"
            },
            {
                "scenario": "商务舱机舱餐饮要求",
                "en": "Could we request hot tea with lemon instead of coffee before take-off, please?",
                "cn": "请问起飞前能帮我们倒一杯热柠檬水替代咖啡吗？非常感谢。",
                "tip": "商务舱起飞前迎宾饮品沟通时的客气礼貌表达。"
            }
        ]
    },
    {
        "day": 4,
        "topic": "🛃 出入境边检与签证申报",
        "words": [
            {
                "word": "Immigration",
                "phonetic": "/ˌɪmɪˈɡreɪʃn/",
                "pos": "n. 名词",
                "def": "出入境边检；移民海关事务处",
                "exampleEn": "Please have your passport, return flight confirmation, and business invitation letter ready for immigration.",
                "exampleCn": "请备好护照、返程机票确认单和商务邀请函，以便边检官员核验。"
            },
            {
                "word": "Entry Visa",
                "phonetic": "/ˈentri ˈviːzə/",
                "pos": "n. 短语",
                "def": "入境签证",
                "exampleEn": "Our multi-entry business visa allows a continuous stay of up to 30 days per visit.",
                "exampleCn": "我们办理的多次入境商务签证允许单次最长停留30天。"
            },
            {
                "word": "Landing Card",
                "phonetic": "/ˈlændɪŋ kɑːd/",
                "pos": "n. 短语",
                "def": "入境登记卡",
                "exampleEn": "The flight crew distributed the Moroccan landing cards shortly before initial descent.",
                "exampleCn": "航班机组在客机开始下降前向旅客分发了摩洛哥入境卡。"
            }
        ],
        "sentences": [
            {
                "scenario": "回答海外边检官员的入境目的询问",
                "en": "We are visiting Cairo for five days of executive commercial meetings with our local representative office.",
                "cn": "我们前往开罗停留五天，将与当地代表处举行商务高层商谈。",
                "tip": "入境问询务必简明扼要，直接说明商务目的（commercial meetings）和天数。"
            },
            {
                "scenario": "出示商务邀请函与住宿地址",
                "en": "Here is the official invitation letter from our Egyptian partner, along with our confirmed hotel reservation.",
                "cn": "这是我们埃及合作方出具的官方邀请函，附有已确认的酒店入住凭单。",
                "tip": "入境过关时主动附上 hotel reservation 可显著加快通关盖章速度。"
            },
            {
                "scenario": "协助领导核验入境章日期",
                "en": "Let's check the ink stamp in the passport to make sure the allowed duration of stay matches our itinerary.",
                "cn": "我们核对一下护照上的验讫章，确保官员盖注的准许逗留期限与我们的行程一致。",
                "tip": "涉外差旅必查细节：防范部分口岸官员误盖短于行程期限的停留天数。"
            }
        ]
    },
    {
        "day": 5,
        "topic": "📦 海关清关与行李提取",
        "words": [
            {
                "word": "Customs Declaration",
                "phonetic": "/ˈkʌstəmz ˌdekləˈreɪʃn/",
                "pos": "n. 短语",
                "def": "海关申报（单）",
                "exampleEn": "Goods intended for exhibition display must be declared on the customs declaration form.",
                "exampleCn": "用于展会样品陈列的展品必须在海关申报单上如实注明申报。"
            },
            {
                "word": "Carousel",
                "phonetic": "/ˌkærəˈsel/",
                "pos": "n. 名词",
                "def": "行李提取转盘",
                "exampleEn": "Bags from our flight are arriving on baggage carousel 4 in the international arrivals hall.",
                "exampleCn": "我们航班的托运行李正在国际到达大厅的4号转盘上陆续送达。"
            },
            {
                "word": "Duty-Free",
                "phonetic": "/ˌdjuːti ˈfriː/",
                "pos": "adj./n.",
                "def": "免税的；免税商品",
                "exampleEn": "Corporate gifts purchased at the airport duty-free store comply with standard customs allowance.",
                "exampleCn": "在机场免税店购买的商务伴手礼符合标准的旅客免税限额。"
            }
        ],
        "sentences": [
            {
                "scenario": "在行李转盘旁指引领导",
                "en": "Our priority-tagged luggage should be among the first batch out on Carousel 3 shortly.",
                "cn": "贴有优先标签的行李应该很快就会随第一批次在3号转盘送出。",
                "tip": "priority-tagged 指商务舱或金卡会员托运时栓挂的‘优先行李标牌’。"
            },
            {
                "scenario": "遇到行李延误或破损",
                "en": "One of our equipment cases did not arrive; we need to file a Property Irregularity Report at the lost baggage desk.",
                "cn": "我们的一件设备箱未运达，需要立即前往行李查询处填写《行李运输事故记录单（PIR）》。",
                "tip": "Property Irregularity Report（PIR单）是航司索赔和追踪迟到行李的唯一法定凭据。"
            },
            {
                "scenario": "海关抽检样品与样机说明",
                "en": "These items are non-commercial exhibition samples for demonstration purposes only, not for local resale.",
                "cn": "这些物品是仅供技术展示演示的非贸易样品，绝不在当地市场转售。",
                "tip": "海外通关样机设备的黄金免税抗辩金句，消除海关转售疑虑。"
            }
        ]
    },
    {
        "day": 6,
        "topic": "🔄 航班延误与航变改签",
        "words": [
            {
                "word": "Reschedule",
                "phonetic": "/ˌriːˈskedʒuːl/",
                "pos": "v. 动词",
                "def": "改签；重新安排日程时刻",
                "exampleEn": "Due to technical maintenance, the airline offered to reschedule our departure to an earlier flight.",
                "exampleCn": "由于机械故障检修，航空公司主动提出将我们的出发时间改签至更早的航班。"
            },
            {
                "word": "Compensation",
                "phonetic": "/ˌkɒmpenˈseɪʃn/",
                "pos": "n. 名词",
                "def": "航变延误补偿；赔偿金",
                "exampleEn": "Passengers delayed for over four hours on international routes are entitled to meal vouchers and hotel compensation.",
                "exampleCn": "在国际航线上延误超过四小时的旅客有权获得餐券及航司提供的酒店住宿补偿。"
            },
            {
                "word": "Reroute",
                "phonetic": "/ˌriːˈruːt/",
                "pos": "v. 动词",
                "def": "改道；变更中转路线",
                "exampleEn": "If the direct flight is cancelled, the ticketing agent can reroute us through Paris or Frankfurt.",
                "exampleCn": "如果直飞航班取消，票务代表可以为我们改签经由巴黎或法兰克福中转的航线。"
            }
        ],
        "sentences": [
            {
                "scenario": "在航司柜台紧急申请改签",
                "en": "Our incoming connection was delayed; could you endorse our tickets to the next available Star Alliance flight?",
                "cn": "我们前段接驳航班延误了，请问能否帮我们将客票签转至下一班最早起飞的星空联盟航班？",
                "tip": "endorse tickets 指‘签转机票至他航’，紧急保会期时的专业术语。"
            },
            {
                "scenario": "向领导汇报航变与备选方案",
                "en": "The original flight is delayed by two hours; I have already placed us on standby for the 16:30 express flight.",
                "cn": "原航班延误了两小时，我已经帮我们登记了16:30快线航班的候补名单。",
                "tip": "on standby 指‘排队候补登机’，展现前瞻高效的改签动作。"
            },
            {
                "scenario": "通知接机方推迟接机时间",
                "en": "Due to air traffic control, our estimated arrival time has slipped to 21:15; please adjust the driver pick-up accordingly.",
                "cn": "受航空管制影响，我们预计到达时间推迟至21:15，烦请同步调整接机司机的到达时间。",
                "tip": "air traffic control（ATC航管）是国际航班推迟最常见的官方表述。"
            }
        ]
    },
    {
        "day": 7,
        "topic": "🚖 机场接机与专车接送",
        "words": [
            {
                "word": "Chauffeur",
                "phonetic": "/ˈʃoʊfər/",
                "pos": "n. 名词",
                "def": "商务专车司机；专职司导",
                "exampleEn": "The local representative office arranged a bilingual chauffeur holding a nameplate at Exit 2.",
                "exampleCn": "当地代表处安排了一位手持接机牌的双语专车司机在2号出口处等候。"
            },
            {
                "word": "Curbside",
                "phonetic": "/ˈkɜːbsaɪd/",
                "pos": "n./adv.",
                "def": "路边落客/乘车区",
                "exampleEn": "The limousine is staged at the VIP curbside pickup zone right outside Pillar 5.",
                "exampleCn": "接待礼宾车正停靠在航站楼5号立柱正对面的VIP路侧乘车区。"
            },
            {
                "word": "Van",
                "phonetic": "/væn/",
                "pos": "n. 名词",
                "def": "商务车（如埃尔法/奔驰V-Class）",
                "exampleEn": "We booked a 7-seater executive van to accommodate the six delegates and all their luggage.",
                "exampleCn": "我们预定了一辆7座商务车，以便舒适容纳六位代表及其全部行李。"
            }
        ],
        "sentences": [
            {
                "scenario": "出海关后联络接机司机",
                "en": "Hello Ahmed, we have just cleared customs and are heading towards International Arrival Gate 3.",
                "cn": "你好艾哈迈德，我们刚刚完成出关，正朝国际到达3号门走出来。",
                "tip": "出关后第一条简讯，精准报出所在的大门号（Gate 3）。"
            },
            {
                "scenario": "确认车辆型号与车牌号码",
                "en": "Could you send me the driver's direct mobile number and the vehicle license plate for quick identification?",
                "cn": "能否将司机的直接联系电话和车牌号发送给我，以便快速确认接应？",
                "tip": "接机前锁定 vehicle license plate 是确保高管出差安全与对接顺畅的关键。"
            },
            {
                "scenario": "指引领导上车并前往酒店",
                "en": "The driver has loaded our luggage; the journey to the Four Seasons Cairo takes roughly 45 minutes in current traffic.",
                "cn": "司机已帮我们装好行李，按当前路况前往开罗四季酒店大约需要45分钟车程。",
                "tip": "上车后主动向领导通报抵达酒店所需路程时间，展现贴心预期管理。"
            }
        ]
    },
    {
        "day": 8,
        "topic": "🏨 酒店入住与房型确认",
        "words": [
            {
                "word": "Reservation",
                "phonetic": "/ˌrezəˈveɪʃn/",
                "pos": "n. 名词",
                "def": "预订；订房预订单",
                "exampleEn": "Here is our booking voucher confirming three nights under the corporate rate.",
                "exampleCn": "这是我们的订房凭证，确认以协议公司价入住三晚。"
            },
            {
                "word": "Early Check-in",
                "phonetic": "/ˈɜːli tʃek ɪn/",
                "pos": "n. 短语",
                "def": "提前入住办理",
                "exampleEn": "Since our red-eye flight landed at dawn, we requested guaranteed early check-in at 8:00 AM.",
                "exampleCn": "由于我们的红眼航班在黎明降落，我们提前申请了早上8点的保证提前入住。"
            },
            {
                "word": "Upgrade",
                "phonetic": "/ˌʌpˈɡreɪd/",
                "pos": "v./n.",
                "def": "升级（房型/舱位）",
                "exampleEn": "As a loyalty titanium member, the director received a complimentary upgrade to an Executive Nile Suite.",
                "exampleCn": "作为常旅客钛金会员，领导获得了免费升至行政尼罗河套房的礼遇待遇。"
            }
        ],
        "sentences": [
            {
                "scenario": "在前台办理入住登记",
                "en": "Good afternoon, we have a reservation for Mr. Zhang; here are our passports and credit card for incidentals.",
                "cn": "下午好，我们预订了张先生的房间，这是我们的护照和用于杂费预授权的信用卡。",
                "tip": "incidentals 指‘客房杂费/押金’，国际五星级酒店入住标配用词。"
            },
            {
                "scenario": "要求安静且高楼层的无烟房型",
                "en": "Could you please assign a non-smoking room on a higher floor facing away from street traffic noise?",
                "cn": "请问能否安排一间高楼层、背向街道马路噪音的无烟客房？",
                "tip": "facing away from traffic noise 是保障领导长途出差睡眠质量的精准诉求。"
            },
            {
                "scenario": "询问酒店早餐时间与行政待遇",
                "en": "What time does breakfast start tomorrow, and does our booking include access to the Executive Lounge on the 18th floor?",
                "cn": "请问明天早餐几点开始，我们的房型是否包含18楼行政酒廊的进出使用权益？",
                "tip": "Executive Lounge access 是高管差旅处理公务、轻商务会面的核心场所。"
            }
        ]
    },
    {
        "day": 9,
        "topic": "🛎️ 行政酒廊与礼宾服务",
        "words": [
            {
                "word": "Concierge",
                "phonetic": "/kɒnˈsjeəʒ/",
                "pos": "n. 名词",
                "def": "礼宾部主管；酒店礼宾接待员",
                "exampleEn": "The concierge helped us secure a private dining room for tonight's client banquet.",
                "exampleCn": "酒店礼宾部协助我们为今晚的客户晚宴预定了一间私密包厢。"
            },
            {
                "word": "Amenities",
                "phonetic": "/əˈmiːnətiz/",
                "pos": "n. 复数",
                "def": "客房便利设施；配套用品",
                "exampleEn": "The executive suite amenities include high-speed fiber Wi-Fi, an ironing board, and a Nespresso machine.",
                "exampleCn": "行政套房的配套设施包括高速光纤Wi-Fi、熨衣板和奈斯派索胶囊咖啡机。"
            },
            {
                "word": "Pressing Service",
                "phonetic": "/ˈpresɪŋ ˈsɜːvɪs/",
                "pos": "n. 短语",
                "def": "衣物熨烫服务",
                "exampleEn": "Please send someone for express pressing service; the director needs this business suit pressed before 14:00.",
                "exampleCn": "请派员来取急件熨烫，领导需要在下午两点前将这套商务西装熨好送回。"
            }
        ],
        "sentences": [
            {
                "scenario": "联系礼宾部打印会议机密文件",
                "en": "Could the business center print ten bound copies of this bilingual presentation deck by 10:00 AM?",
                "cn": "请问商务中心能在上午10点前帮我们装订打印10份双语演示讲稿吗？",
                "tip": "bound copies 指‘装订成册的副本’，彰显严谨的会务准备水准。"
            },
            {
                "scenario": "向客房服务申请电源转换插头",
                "en": "Could housekeeping send up two Type-C European standard travel adapters and an extension cord?",
                "cn": "能否请客房服务送两个欧标C型转换插头和一条电源接线板到房间？",
                "tip": "travel adapter（转换插头）与 extension cord（插线板）是涉外出差高频必备物资。"
            },
            {
                "scenario": "在行政酒廊预定小型私密会客角",
                "en": "We are hosting an informal 30-minute discussion with an overseas partner; is there a quiet corner available?",
                "cn": "我们将与一位海外合作伙伴进行30分钟的非正式会谈，酒廊里有安静的角落可以使用吗？",
                "tip": "informal discussion 结合 quiet corner，是高管在酒廊碰头的高级得体说法。"
            }
        ]
    },
    {
        "day": 10,
        "topic": "🍽️ 酒店退房与账单核对",
        "words": [
            {
                "word": "Folio",
                "phonetic": "/ˈfoʊlioʊ/",
                "pos": "n. 名词",
                "def": "酒店结账明细单；消费账册",
                "exampleEn": "Please print an itemized folio detailing room charges, laundry, and dining for company expense filing.",
                "exampleCn": "请打印一份列明房费、洗衣费和餐饮开销的消费账单明细，供公司财务报销审核。"
            },
            {
                "word": "Late Check-out",
                "phonetic": "/leɪt tʃek aʊt/",
                "pos": "n. 短语",
                "def": "延迟退房服务",
                "exampleEn": "Because our flight departs at 22:00, we arranged late check-out until 16:00 to allow the leader to rest.",
                "exampleCn": "由于我们的航班晚上10点起飞，我们协商了延迟退房至下午4点，以便领导休整。"
            },
            {
                "word": "Discrepancy",
                "phonetic": "/dɪˈskrepənsi/",
                "pos": "n. 名词",
                "def": "出入；账目差异；不一致",
                "exampleEn": "There is a minor discrepancy on the mini-bar charge that needs to be clarified before signing.",
                "exampleCn": "账单上的迷你吧消费项有一点出入，签字刷卡前需要先核实澄清一下。"
            }
        ],
        "sentences": [
            {
                "scenario": "前台办理快速结账退房",
                "en": "We are ready to check out of Rooms 1802 and 1806; could we settle the room charges together on one master bill?",
                "cn": "我们准备办理1802和1806房的退房手续，能否将两间房的费用统一合并在一张总账单上结算？",
                "tip": "master bill 指‘统一结算主账单’，多房间统一企业报销时的关键术语。"
            },
            {
                "scenario": "寄存行李以便开展下午商务拜访",
                "en": "Could the bell desk store our four suitcases until 17:00? We will collect them right before heading to the airport.",
                "cn": "能否麻烦礼宾行李房代存我们四件行李箱到下午5点？我们去机场前会统一取件。",
                "tip": "bell desk 是五星级酒店‘行李服务台’的标准名称。"
            },
            {
                "scenario": "索要符合财务报销格式的增值税发票/水单",
                "en": "Please ensure our company's full legal entity name and tax number are clearly printed on the final invoice.",
                "cn": "请确保我们公司的完整法人实体全称和纳税识别号清晰打印在最终结账发票上。",
                "tip": "legal entity name 是避免财务被打回重开票的专业英文用词。"
            }
        ]
    },
    {
        "day": 11,
        "topic": "🏢 涉外会务场地预订与布置",
        "words": [
            {
                "word": "Boardroom",
                "phonetic": "/ˈbɔːdruːm/",
                "pos": "n. 名词",
                "def": "董事会会议室；高规格闭门会议室",
                "exampleEn": "We reserved the executive boardroom equipped with video conferencing for the bilateral summit.",
                "exampleCn": "我们预定了配备远程视频会议系统的行政董事会厅，用于双边高级别峰会。"
            },
            {
                "word": "Audio-Visual (AV)",
                "phonetic": "/ˌɔːdiəʊ ˈvɪʒuəl/",
                "pos": "adj./n.",
                "def": "音视频多媒体设备",
                "exampleEn": "The hotel AV technician is running a soundcheck for the lapel microphones and projector.",
                "exampleCn": "酒店音视频工程师正在对领夹无线麦克风和高清投影仪进行现场试音试屏。"
            },
            {
                "word": "U-Shape",
                "phonetic": "/ˈjuː ʃeɪp/",
                "pos": "n./adj.",
                "def": "U型会议台型桌席布置",
                "exampleEn": "The bilateral discussion requires a U-shape seating layout to foster direct interaction across delegations.",
                "exampleCn": "双边洽谈会议需要布置为U型桌席，以促进两个代表团成员之间更直接的交流。"
            }
        ],
        "sentences": [
            {
                "scenario": "与酒店宴会销售经理核对会场设备",
                "en": "We will need a wireless clicker, HDMI adapter for MacBooks, and high-speed dedicated bandwidth in the meeting room.",
                "cn": "会议室里我们需要翻页激光笔、苹果电脑HDMI转接头以及一条高速专享网络带宽。",
                "tip": "dedicated bandwidth（专享带宽）能有效防止因酒店公共Wi-Fi卡顿导致视频汇报中断。"
            },
            {
                "scenario": "检查会场名牌与资料摆放",
                "en": "Let's align the desk nameplates in English and French according to the finalized VIP protocol hierarchy.",
                "cn": "让我们依照最终确认的VIP外事礼宾排位顺序，对齐摆放英法双语桌签席卡。",
                "tip": "protocol hierarchy（礼宾层级排位）是重大国际涉外会晤的核心考究细节。"
            },
            {
                "scenario": "协调会中即时茶歇补给",
                "en": "Please ensure coffee, mineral water, and light refreshments are replenished quietly at the rear table at 10:30.",
                "cn": "请确保在10点30分轻声在会场后侧长桌上添补热咖啡、矿泉水及精美茶点。",
                "tip": "replenished quietly 体现高标准外事会务助理的不打扰、重细节素养。"
            }
        ]
    },
    {
        "day": 12,
        "topic": "🤝 涉外高管会见礼仪与接待",
        "words": [
            {
                "word": "Protocol",
                "phonetic": "/ˈproʊtəkɒl/",
                "pos": "n. 名词",
                "def": "外事礼宾礼仪；外交规范",
                "exampleEn": "Adhering to strict international protocol ensures mutual respect between visiting foreign executives.",
                "exampleCn": "恪守严谨的国际外事礼仪规范，能够确保到访外籍高管之间展现充分的互敬互重。"
            },
            {
                "word": "Dignitary",
                "phonetic": "/ˈdɪɡnɪteri/",
                "pos": "n. 名词",
                "def": "政要；外籍贵宾；高规格领导",
                "exampleEn": "Our general manager will greet the Moroccan government dignitary in the VIP holding room.",
                "exampleCn": "我们的总经理将在贵宾休息室亲自迎接摩洛哥政府高级官员。"
            },
            {
                "word": "Bilateral",
                "phonetic": "/ˌbaɪˈlætərəl/",
                "pos": "adj. 形容词",
                "def": "双边的；双方高层的",
                "exampleEn": "Both sides concluded the bilateral closed-door talks with a joint memorandum of understanding.",
                "exampleCn": "双方在闭门双边会谈后联合签署了战略合作谅解备忘录。"
            }
        ],
        "sentences": [
            {
                "scenario": "为双方领导进行正式引见介绍",
                "en": "Allow me to introduce our Executive Vice President, Mr. Wang, who oversees our regional infrastructure initiatives.",
                "cn": "请允许我荣幸地介绍我们的常务副总裁王总，王总全面统筹我们整个区域的基础设施业务规划。",
                "tip": "Allow me to introduce... 是外事与商务接待中最为典雅稳重的引荐句型。"
            },
            {
                "scenario": "双方互赠名片与破冰开场",
                "en": "It is an absolute pleasure to meet you in person following our productive video conference last month.",
                "cn": "继上个月卓有成效的视频会议后，今天能同您在线下当面会晤，真是倍感荣幸。",
                "tip": "in person（当面/线下）是疫情后国际商旅拜访中极为加分的高情商破冰语。"
            },
            {
                "scenario": "合影留念与引领入席",
                "en": "Before we begin our formal agenda, could we invite both delegations to step forward for a commemorative photo?",
                "cn": "在正式议程开始前，能否诚邀双方代表团移步向前合影留念？",
                "tip": "commemorative photo（纪念合影）通常在刚落座或会谈签字后适时发起。"
            }
        ]
    },
    {
        "day": 13,
        "topic": "🍷 商务宴请与座次安排",
        "words": [
            {
                "word": "Seating Chart",
                "phonetic": "/ˈsiːtɪŋ tʃɑːt/",
                "pos": "n. 短语",
                "def": "宴席座次排位图",
                "exampleEn": "The host and primary VIP guest should be placed opposite each other according to the seating chart.",
                "exampleCn": "依据宴会座次图安排，主东道主与主宾领导应面朝主门按主宾对应落座。"
            },
            {
                "word": "Dietary Restriction",
                "phonetic": "/ˈdaɪətəri rɪˈstrɪkʃn/",
                "pos": "n. 短语",
                "def": "饮食忌口；清真/素食等饮食习惯",
                "exampleEn": "Please inform the head chef that our guests require certified Halal dining with no alcohol served.",
                "exampleCn": "请提前通告主厨，我们的中东贵宾要求严格遵照清真认证餐饮标准，宴席不供应酒精制品。"
            },
            {
                "word": "Toast",
                "phonetic": "/toʊst/",
                "pos": "n./v.",
                "def": "祝酒词；举杯敬酒",
                "exampleEn": "The director will propose a short toast to celebrate our fruitful collaboration across North Africa.",
                "exampleCn": "领导将在开席时发表一段简短的祝酒辞，庆祝我们在北非市场的丰硕合作成果。"
            }
        ],
        "sentences": [
            {
                "scenario": "确认外宾饮食禁忌与清真标准",
                "en": "Do any members of your delegation have specific allergies, seafood restrictions, or vegetarian requirements?",
                "cn": "请问贵方代表团成员中是否有任何过敏源禁忌、海鲜忌口或清真素食要求？",
                "tip": "宴请前主动书面核对 dietary restrictions 是专业涉外秘书的标杆动作。"
            },
            {
                "scenario": "在宴会开场时致敬酒词",
                "en": "Let's raise our glasses to our enduring partnership and to the continued prosperity of both our organizations.",
                "cn": "让我们共同举杯，为我们历久弥坚的友谊伙伴关系、以及双方机构的欣欣向荣干杯！",
                "tip": "raise our glasses to... 是国际商务晚宴中典雅、庄重且极富感染力的敬酒标配。"
            },
            {
                "scenario": "礼貌结账并要求装订水单",
                "en": "Excuse me, waiter, could you bring the bill discretely to my side table so as not to disrupt the banquet?",
                "cn": "服务员麻烦一下，能否低调将账单递到我的偏桌，避免打扰主宾席的谈话？",
                "tip": "discretely（审慎地/不张扬地）结账是高水平宴会助理服务领导的顶级细节。"
            }
        ]
    },
    {
        "day": 14,
        "topic": "🚗 当地包车与城际交通",
        "words": [
            {
                "word": "Private Charter",
                "phonetic": "/ˈpraɪvət ˈtʃɑːtər/",
                "pos": "n. 短语",
                "def": "私人包车；专车包天租赁",
                "exampleEn": "We arranged a private charter van on stand-by for 10 hours for intercity visits between Rabat and Casablanca.",
                "exampleCn": "我们包租了一辆10小时全天待命的专属商务车，用于拉巴特与卡萨布兰卡之间的城际考察。"
            },
            {
                "word": "Toll",
                "phonetic": "/toʊl/",
                "pos": "n. 名词",
                "def": "高速公路通行费；过路费",
                "exampleEn": "The daily charter rate includes all highway tolls, fuel, and parking expenses.",
                "exampleCn": "每日全包车费已涵盖所有高速通行过路费、全程油费及停车费。"
            },
            {
                "word": "Itinerary Buffer",
                "phonetic": "/aɪˈtɪnərəri ˈbʌfər/",
                "pos": "n. 短语",
                "def": "行程机动富余缓冲时间",
                "exampleEn": "Allow a 45-minute itinerary buffer to account for unforeseen traffic jams near the business district.",
                "exampleCn": "请在日程中预留45分钟的机动缓冲时间，以应对CBD商务区突发的交通拥堵状况。"
            }
        ],
        "sentences": [
            {
                "scenario": "告知包车司机今日全天考察路线",
                "en": "Good morning, driver; our route today starts at the hotel, stops at the rep office, and heads to the project site.",
                "cn": "早上好师傅；我们今天的行程从酒店出发，中途经停代表处，下午前往工程项目现场。",
                "tip": "上车前用清晰的时间轴向包车司机明确各途经点，避免走错航路。"
            },
            {
                "scenario": "要求司机在下客点原地待命随时接驾",
                "en": "Please stay parked near Building C and keep your phone on; we anticipate wrapping up in approximately one hour.",
                "cn": "请将车停泊在C座附近并保持手机畅通，我们预计约一小时后结束会谈立刻用车。",
                "tip": "anticipate wrapping up 表示‘预计大约何时收尾结束’，地道职场口语。"
            },
            {
                "scenario": "因突发修路改道向领导说明",
                "en": "Due to ongoing roadwork on the coastal highway, the navigation suggests taking the inland ring road to save 20 minutes.",
                "cn": "由于沿海主干道目前正在施工修路，导航建议改走内陆环线，可以为我们节省20分钟车程。",
                "tip": "主动向领导汇报‘为何绕路以及绕路节省多长时间’，让领导心中有数、安心舒畅。"
            }
        ]
    },
    {
        "day": 15,
        "topic": "🌐 国际漫游、网络与移动SIM卡",
        "words": [
            {
                "word": "Data Roaming",
                "phonetic": "/ˈdeɪtə ˈroʊmɪŋ/",
                "pos": "n. 短语",
                "def": "数据国际漫游",
                "exampleEn": "Please turn on data roaming on your phone after landing to connect to the local partner carrier.",
                "exampleCn": "航班落地后请在手机设置中开启数据漫游，以便自动接入当地合作运营商网络。"
            },
            {
                "word": "eSIM",
                "phonetic": "/ˈiː sɪm/",
                "pos": "n. 名词",
                "def": "嵌入式电子虚拟SIM卡",
                "exampleEn": "I pre-installed a Middle East regional eSIM profile on the executive iPad for high-speed 5G access.",
                "exampleCn": "我已在领导的iPad上预先安装了中东多国通用eSIM配置方案，实现即开即用5G高速上网。"
            },
            {
                "word": "Bandwidth",
                "phonetic": "/ˈbændwɪdθ/",
                "pos": "n. 名词",
                "def": "网络带宽；传输速率",
                "exampleEn": "The hotel meeting room has dedicated Wi-Fi bandwidth capable of seamless HD international calls.",
                "exampleCn": "酒店会议室具备专属Wi-Fi宽带，完全能够支撑无卡顿的高清国际跨国连线。"
            }
        ],
        "sentences": [
            {
                "scenario": "协助领导解决漫游无信号问题",
                "en": "If the network shows 'No Service', let's manually select the local operator Maroc Telecom in carrier settings.",
                "cn": "如果手机屏幕显示‘无服务’，我们在蜂窝网络设置里手动搜索并选中当地运营商Maroc Telecom试试。",
                "tip": "manually select carrier 是跨国出差排查漫游无网最立竿见影的技术解决手段。"
            },
            {
                "scenario": "在境外机场购买当地流量卡备用",
                "en": "Could you provide a 30-day prepaid data SIM card with at least 20 gigabytes of 5G tethering data?",
                "cn": "请问能帮我们办理一张含至少20GB高速5G热点共享流量的30天预付费电话卡吗？",
                "tip": "tethering data 指‘允许开启移动热点分享’的流量，备用应急极度实用。"
            },
            {
                "scenario": "安全提示避免连接未加密公共Wi-Fi",
                "en": "Please avoid connecting to open public Wi-Fi networks when accessing internal enterprise ERP or email servers.",
                "cn": "在访问企业内部ERP或公司邮件系统时，请尽量使用个人安全热点，避免连接未加密的公共Wi-Fi。",
                "tip": "涉外商务差旅的信息安全红线提醒，体现秘书极强的数据合规意识。"
            }
        ]
    },
    {
        "day": 16,
        "topic": "💱 外币兑换与差旅小额现金",
        "words": [
            {
                "word": "Exchange Rate",
                "phonetic": "/ɪksˈtʃeɪndʒ reɪt/",
                "pos": "n. 短语",
                "def": "货币兑换汇率",
                "exampleEn": "What is the official bank exchange rate between US Dollars and Egyptian Pounds today?",
                "exampleCn": "请问今天美元对埃及镑的官方银行买入卖出汇率是多少？"
            },
            {
                "word": "Petty Cash",
                "phonetic": "/ˈpeti kæʃ/",
                "pos": "n. 短语",
                "def": "备用零用金；差旅小额现钞",
                "exampleEn": "Keep approximately 200 dollars in local petty cash for small taxi fares and airport porter tips.",
                "exampleCn": "请随身留备大约等值200美元的当地零钱现钞，以便支付出租车及机场行李搬运小费。"
            },
            {
                "word": "Denomination",
                "phonetic": "/dɪˌnɒmɪˈneɪʃn/",
                "pos": "n. 名词",
                "def": "纸币面额",
                "exampleEn": "Could you give me smaller denominations, preferably 10 and 20 dollar bills?",
                "exampleCn": "请问能否帮我多兑换一些小面额的纸币，最好是10美元和20美元的面值？"
            }
        ],
        "sentences": [
            {
                "scenario": "在银行或机场外币兑换窗口",
                "en": "I would like to exchange 500 US Dollars into Moroccan Dirhams; here is my passport and receipt.",
                "cn": "我想将500美元兑换为摩洛哥迪拉姆；这是我的护照和兑换凭据。",
                "tip": "标准简明的货币兑换指令，同时务必索要保留好官方兑换收据（receipt）。"
            },
            {
                "scenario": "信用卡境外消费遇到刷卡失败",
                "en": "The terminal declined the transaction; could we try swiping through the alternative Visa payment gateway?",
                "cn": "POS机终端显示交易被拒，请问能否尝试改走Visa备用清算通道刷一次？",
                "tip": "terminal declined transaction 是境外刷卡时POS机吐出失败单据的标准英文提示。"
            },
            {
                "scenario": "留存所有消费小票以便财务入账",
                "en": "Be sure to retain all taxi receipts and ATM withdrawal slips to attach to our post-trip expense voucher.",
                "cn": "请务必妥善保留所有的出租车小票和ATM取款凭条，回国后需要装订在差旅报销单后。",
                "tip": "expense voucher 是大企业内部财务部门审核差旅支出的‘报销凭单’。"
            }
        ]
    },
    {
        "day": 17,
        "topic": "📋 签证延期与使领馆对接",
        "words": [
            {
                "word": "Extension",
                "phonetic": "/ɪkˈstenʃn/",
                "pos": "n. 名词",
                "def": "延期；续签许可",
                "exampleEn": "Our commercial meetings will run longer, so we need to file for a 14-day visa extension at the passport bureau.",
                "exampleCn": "由于商业谈判议程拉长，我们需要去当地出入境管理局申请为期14天的签证延期。"
            },
            {
                "word": "Consulate",
                "phonetic": "/ˈkɒnsələt/",
                "pos": "n. 名词",
                "def": "领事馆；使领馆外事办事处",
                "exampleEn": "The Chinese Embassy and Consulate General provide 24-hour emergency consular protection for overseas delegations.",
                "exampleCn": "中国驻外使领馆为海外到访商务代表团提供24小时全天候应急领事保护。"
            },
            {
                "word": "Notarize",
                "phonetic": "/ˈnoʊtəraɪz/",
                "pos": "v. 动词",
                "def": "公证；使具备法律证明力",
                "exampleEn": "The corporate power of attorney must be notarized and apostilled before submission to local authorities.",
                "exampleCn": "企业法定代表人授权委托书必须经过公证并办理海牙附加证明书后，方可递交当地官方机构。"
            }
        ],
        "sentences": [
            {
                "scenario": "向出入境机构咨询商务签延期材料",
                "en": "What supporting documents are required to extend a single-entry commercial visa for another two weeks?",
                "cn": "请问办理单次商务签证再延期两周，需要提交哪些支持性证明材料？",
                "tip": "supporting documents 包括邀请函、返程机票订单、本地代表处担保函等。"
            },
            {
                "scenario": "联络驻外使馆领事保护热线",
                "en": "We are a visiting corporate delegation from Beijing; could you advise on current entry protocols at the land border?",
                "cn": "我们是来自北京的商务访问代表团，想向贵馆咨询一下目前陆路口岸的最新通行政策？",
                "tip": "表明身份（visiting corporate delegation），迅速获得使领馆精准权威指导。"
            },
            {
                "scenario": "护照遗失紧急补办旅行证件",
                "en": "Our delegate mislaid their passport; we need to apply for an emergency travel document to ensure onward travel.",
                "cn": "我们代表团一名成员不慎遗失护照，需要紧急申领临时旅行证件，以确保后续行程正常衔接。",
                "tip": "emergency travel document（旅行证）是境外护照丢失时唯一快速回国通行证件。"
            }
        ]
    },
    {
        "day": 18,
        "topic": "⏱️ 跨时区作息与时差调整",
        "words": [
            {
                "word": "Jet Lag",
                "phonetic": "/ˈdʒet læɡ/",
                "pos": "n. 短语",
                "def": "时差综合征；跨时区疲劳反应",
                "exampleEn": "To minimize jet lag after flying from Beijing to Cairo, we kept the first afternoon schedule light.",
                "exampleCn": "为了尽量减轻从北京飞抵开罗后的时差疲劳，我们将首日下午的日程安排得相对轻松。"
            },
            {
                "word": "Time Difference",
                "phonetic": "/taɪm ˈdɪfrəns/",
                "pos": "n. 短语",
                "def": "时差",
                "exampleEn": "Morocco is currently three hours behind Cairo, so please pay close attention to meeting scheduling.",
                "exampleCn": "摩洛哥目前比开罗慢三小时，在统筹会议排期时请务必格外留心时差。"
            },
            {
                "word": "Recuperate",
                "phonetic": "/rɪˈkuːpəreɪt/",
                "pos": "v. 动词",
                "def": "修整；调理恢复体力",
                "exampleEn": "Allowing the director two hours to rest and recuperate before tonight's banquet will ensure peak energy.",
                "exampleCn": "在今晚宴请前预留两小时供领导在酒店静心修整，可确保出席活动时精力充沛。"
            }
        ],
        "sentences": [
            {
                "scenario": "向海外合作伙伴解释时差排期考虑",
                "en": "Considering our delegation just crossed six time zones, could we shift tomorrow's kickoff session from 9:00 to 10:30 AM?",
                "cn": "鉴于我们代表团刚跨越了六个时区，能否将明早的启动会从9点顺延至上午10点半召开？",
                "tip": "shift session from ... to ... 是礼貌顺延会议开始时间的极其体面的外交措辞。"
            },
            {
                "scenario": "在日历与周报中醒目标注双时区",
                "en": "All appointment invitations indicate both Cairo headquarters time and the local destination timezone.",
                "cn": "所有预约日程卡片均清晰标注了开罗代表处常驻时间以及当地出差目的地的双时区。",
                "tip": "indicate both ... time 体现秘书系统严谨、杜绝时差混淆的专业规范。"
            },
            {
                "scenario": "建议领导调整机上睡眠作息",
                "en": "I suggest setting your watch to Cairo local time upon boarding to help your internal body clock adjust.",
                "cn": "建议您登机后立即将手表时间拨至开罗当地时间，这有助于体内的生物钟提前适应节律。",
                "tip": "国际长途飞行抗时差的经典黄金技巧，高管秘书贴心建议。"
            }
        ]
    },
    {
        "day": 19,
        "topic": "💼 随行陪同与同声传译配合",
        "words": [
            {
                "word": "Interpreter",
                "phonetic": "/ɪnˈtɜːprɪtər/",
                "pos": "n. 名词",
                "def": "商务口译员；现场同传/交传人员",
                "exampleEn": "We hired an accredited Arabic-English simultaneous interpreter for the ministerial forum.",
                "exampleCn": "我们为部长级论坛聘请了一位具备官方认证的阿拉伯语-英语同声传译专家。"
            },
            {
                "word": "Briefing",
                "phonetic": "/ˈbriːfɪŋ/",
                "pos": "n. 名词",
                "def": "简要情况介绍会；预备对齐会",
                "exampleEn": "Let's organize a 15-minute briefing with the interpreter to review technical acronyms and key talking points.",
                "exampleCn": "会前我们同口译员开一个15分钟的对齐会，过一遍专业技术缩略词和发言要点。"
            },
            {
                "word": "Liaison",
                "phonetic": "/liˈeɪzɒn/",
                "pos": "n. 名词",
                "def": "外事联络官；对接协调人",
                "exampleEn": "The Ministry assigned an English-speaking liaison officer to escort our director throughout the summit.",
                "exampleCn": "部委专门指派了一名讲英语的外事联络官，在峰会期间全程随行陪同协助我方领导。"
            }
        ],
        "sentences": [
            {
                "scenario": "会前向口译员提供专业词汇表与演讲稿",
                "en": "Here is our glossed terminology sheet and the speaker's prepared remarks to help you prepare in advance.",
                "cn": "这是我们整理的专业术语对照表和主讲嘉宾的预备讲稿，方便您会前充分备课熟悉。",
                "tip": "glossed terminology sheet 是让现场同传交传发挥出顶级水准的秘密法宝。"
            },
            {
                "scenario": "在谈判桌上提醒发言语速节奏",
                "en": "Please pause briefly every couple of sentences to allow consecutive interpretation to come through accurately.",
                "cn": "发言时烦请每两句话适度停顿留白，以便交替传译能够完整精准地向外方传达。",
                "tip": "consecutive interpretation（交传）时提醒发言节奏是外事随行秘书的重要把控职责。"
            },
            {
                "scenario": "向外宾引荐随行口译人员",
                "en": "Mr. Chen will be accompanying our executive team today to facilitate smooth translation throughout the factory tour.",
                "cn": "陈翻译今天将全程随行陪同我们高管团队，协助厂区参观交流过程中的顺畅沟通。",
                "tip": "facilitate smooth translation（促进顺畅交流），高雅得体。"
            }
        ]
    },
    {
        "day": 20,
        "topic": "📑 差旅备忘录与出差纪要",
        "words": [
            {
                "word": "Debrief",
                "phonetic": "/ˌdiːˈbriːf/",
                "pos": "v./n.",
                "def": "任务复盘汇总；汇报出差总结",
                "exampleEn": "The director convened an immediate evening debrief to consolidate today's commercial takeaways.",
                "exampleCn": "领导在今晚立即召集了复盘总结会，梳理归纳今天各项商务会谈的核心成果与要点。"
            },
            {
                "word": "Action Item",
                "phonetic": "/ˈækʃn ˈaɪtəm/",
                "pos": "n. 短语",
                "def": "待办执行事项；后续落实动作",
                "exampleEn": "Each follow-up action item must have a designated point of contact and an agreed completion deadline.",
                "exampleCn": "每项后续落实执行动作都必须指派明确的第一责任人并约定明确的交付截止时间。"
            },
            {
                "word": "Takeaway",
                "phonetic": "/ˈteɪkəweɪ/",
                "pos": "n. 名词",
                "def": "核心收获；关键结论点",
                "exampleEn": "The primary takeaway from the meeting is that the local partner is eager to finalize contract signing by November.",
                "exampleCn": "本次会谈最核心的结论是，当地合作伙伴十分迫切期望在11月前敲定正式合同签署。"
            }
        ],
        "sentences": [
            {
                "scenario": "在返程航班上整理出差纪要",
                "en": "I will draft the executive trip summary report on the flight back so it's ready for the board meeting tomorrow.",
                "cn": "我将在返程飞机上起草撰写本次出差的高管总结报告，确保明天晨会能够直接呈送董事会。",
                "tip": "executive trip summary report 是展示高水平差旅闭环交付成果的王牌产物。"
            },
            {
                "scenario": "向代表处同步会议待办备忘",
                "en": "Please find attached the meeting minutes detailing agreed deliverables and next steps for both regional teams.",
                "cn": "随信附上本次会谈纪要，详细列明了双方代表处团队达成的交付目标与后续动作。",
                "tip": "meeting minutes detailing agreed deliverables 格式严整、责任清晰。"
            },
            {
                "scenario": "快速抄送核心决议给国内总部",
                "en": "A concise one-page briefing highlights the strategic agreements reached during the Casablanca negotiations.",
                "cn": "这份精炼的一页纸快报重点提炼了在卡萨布兰卡谈判期间达成的各项战略共识。",
                "tip": "one-page briefing（一页纸极简简报）是高管最欣赏的高效汇报方式。"
            }
        ]
    },
    {
        "day": 21,
        "topic": "🩺 差旅医疗应急与国际救援",
        "words": [
            {
                "word": "Travel Insurance",
                "phonetic": "/ˈtrævl ɪnˌʃʊərəns/",
                "pos": "n. 短语",
                "def": "境外商务差旅救援与意外保险",
                "exampleEn": "All delegation members are covered under our comprehensive corporate global travel insurance policy.",
                "exampleCn": "代表团所有成员均已全额投保我们公司的全球商务差旅综合救援与意外险。"
            },
            {
                "word": "SOS Hotline",
                "phonetic": "/ˌes oʊ ˈes ˈhɒtlaɪn/",
                "pos": "n. 短语",
                "def": "国际紧急救援热线",
                "exampleEn": "Save the 24/7 International SOS hotline in your phone in case any emergency medical consultation is needed.",
                "exampleCn": "请将国际SOS机构24小时全天候救援热线存入手机，以备突发紧急医疗咨询使用。"
            },
            {
                "word": "First-Aid Kit",
                "phonetic": "/ˌfɜːst ˈeɪd kɪt/",
                "pos": "n. 短语",
                "def": "急救药箱；随行常用药品包",
                "exampleEn": "The secretary carries a travel first-aid kit stocked with pain relievers, band-aids, and gastrointestinal medication.",
                "exampleCn": "随行秘书备有差旅急救药包，里面备齐了止痛药、创口贴及水土不服常用的肠胃急救药。"
            }
        ],
        "sentences": [
            {
                "scenario": "领导突发水土不服肠胃不适",
                "en": "The director is experiencing mild digestive upset; could the concierge recommend a reputable English-speaking doctor?",
                "cn": "领导感觉有些水土不服、肠胃不适，能否请礼宾部推荐一位声誉良好的全英语就诊医生？",
                "tip": "mild digestive upset 是表达‘轻微水土不服肠胃难受’的高雅委婉医学词汇。"
            },
            {
                "scenario": "联系酒店紧急就近送医或派医生上门",
                "en": "Could you request an on-call hotel physician to visit Room 1205 for a brief diagnostic consultation?",
                "cn": "能否麻烦请酒店的签约值班医生到1205房间进行一次简短的问诊？",
                "tip": "on-call hotel physician 是高档涉外酒店的标配‘随叫随到签约医生’。"
            },
            {
                "scenario": "索要全英文医疗发票与病历用于保险理赔",
                "en": "Please ensure the clinic provides an itemized medical invoice and doctor's diagnosis report in English for insurance claims.",
                "cn": "请确保诊所提供全英文的医疗收费明细发票及医生诊断证明书，以便回国办理商业保险理赔。",
                "tip": "itemized medical invoice 是商业保险理赔审核报销报账不可或缺的黄金凭证。"
            }
        ]
    },
    {
        "day": 22,
        "topic": "🧳 商务着装与商务行李准备",
        "words": [
            {
                "word": "Dress Code",
                "phonetic": "/ˈdres koʊd/",
                "pos": "n. 短语",
                "def": "着装规范；着装要求",
                "exampleEn": "The dress code for tomorrow morning's signing ceremony is strictly business formal.",
                "exampleCn": "明早签约仪式的官方着装规范严格要求为‘全套商务正装’。"
            },
            {
                "word": "Business Formal",
                "phonetic": "/ˈbɪznəs ˈfɔːml/",
                "pos": "n. 短语",
                "def": "正式商务正装（西装领带/正装套裙）",
                "exampleEn": "Dark suits and ties are required for delegates attending the ministerial banquet.",
                "exampleCn": "出席部委正式晚宴的代表团成员必须身着深色西装并系正式领带。"
            },
            {
                "word": "Business Casual",
                "phonetic": "/ˈbɪznəs ˈkæʒuəl/",
                "pos": "n. 短语",
                "def": "商务便装；雅致休闲装（无需领带）",
                "exampleEn": "The internal factory inspection allows business casual attire such as a collared polo or tailored blazer.",
                "exampleCn": "内部厂区技术视察允许穿着商务便装，例如有领Polo衫或合身单西夹克。"
            }
        ],
        "sentences": [
            {
                "scenario": "向前来接洽的使馆确认着装规格",
                "en": "Could you confirm whether the evening diplomatic reception calls for black-tie attire or standard business suits?",
                "cn": "能否向贵方核实一下，今晚的外交招待会是要求穿礼服燕尾服，还是标准商务西装即可？",
                "tip": "提前核对 black-tie 与 business suits，杜绝重大外事活动中着装失礼的尴尬局面。"
            },
            {
                "scenario": "提醒代表团成员随身携带替换衬衫",
                "en": "We advise packing one crisp dress shirt in your carry-on luggage just in case checked bags are delayed.",
                "cn": "建议大家在手提登机包里常备一件平整的换洗衬衫，以防托运行李发生延误影响次日正规会议。",
                "tip": "crisp dress shirt 指‘平整无褶皱的高级正装衬衫’，资深常旅人士的硬核经验。"
            },
            {
                "scenario": "向领导汇报当地气候与适宜衣物建议",
                "en": "Temperatures drop significantly in Casablanca at night; I suggest bringing an overcoat for the outdoor gala.",
                "cn": "卡萨布兰卡夜间气温下降明显，建议您随身带上一件薄大衣外套以备户外酒会御寒保暖。",
                "tip": "主动提示气温骤降（temperatures drop significantly），体现高水平秘书的体贴周到。"
            }
        ]
    },
    {
        "day": 23,
        "topic": "🤝 拜访海外办事处与代表处对接",
        "words": [
            {
                "word": "Representative Office",
                "phonetic": "/ˌreprɪˈzentətɪv ˈɒfɪs/",
                "pos": "n. 短语",
                "def": "驻外代表处；常驻代表机构",
                "exampleEn": "The general manager will inspect our Cairo representative office to review fourth-quarter operational milestones.",
                "exampleCn": "总经理将视察我们的开罗代表处，检视第四季度各项业务运营里程碑进展。"
            },
            {
                "word": "Local Counterpart",
                "phonetic": "/ˈloʊkl ˈkaʊntərpɑːrt/",
                "pos": "n. 短语",
                "def": "当地对口负责人；驻地业务对接人",
                "exampleEn": "Our local counterpart in Rabat has arranged all regional meetings with the port authority.",
                "exampleCn": "我们在拉巴特的驻地业务对口负责人已协调敲定了同当地港务局的所有会谈排期。"
            },
            {
                "word": "Town Hall",
                "phonetic": "/ˈtaʊn hɔːl/",
                "pos": "n. 短语",
                "def": "全员沟通会；代表处员工座谈交流会",
                "exampleEn": "The director will host a town hall session with the frontline expatriate staff tomorrow afternoon.",
                "exampleCn": "领导将于明天下午与一线外派常驻员工举办一场面对面的全员座谈沟通会。"
            }
        ],
        "sentences": [
            {
                "scenario": "抵达代表处受到全体驻外员工热烈欢迎",
                "en": "On behalf of the headquarters leadership team, we extend our heartfelt appreciation to our frontline expatriates.",
                "cn": "我谨代表总部领导班子，向坚守在海外一线扎根拼搏的所有常驻同仁致以最由衷的感谢与问候！",
                "tip": "frontline expatriates 指‘海外一线常驻外派人员’，极具温度与尊重的官方称谓。"
            },
            {
                "scenario": "与代表处总代表对齐近期重大诉求",
                "en": "Let's reserve 40 minutes for a closed-door alignment on resource bottlenecks and headquarters budget approvals.",
                "cn": "我们预留40分钟闭门对齐一下代表处目前的资源瓶颈短板及总部预算审批事项。",
                "tip": "resource bottlenecks（资源瓶颈）聚焦业务症结，务实高效推进。"
            },
            {
                "scenario": "参观代表处办公区域与文化墙",
                "en": "The representative office has established a wonderful team culture despite challenging local operating conditions.",
                "cn": "尽管当地经营环境充满挑战与艰辛，代表处依然沉淀出了极其优秀的团队凝聚力与奋斗氛围。",
                "tip": "大方得体肯定海外代表处凝聚力的经典评述赞词。"
            }
        ]
    },
    {
        "day": 24,
        "topic": "🚕 差旅交通拥堵与行程突发改道",
        "words": [
            {
                "word": "Congestion",
                "phonetic": "/kənˈdʒestʃən/",
                "pos": "n. 名词",
                "def": "交通拥挤；拥堵路况",
                "exampleEn": "Heavy rush-hour congestion on the October Bridge delayed our airport transfer by thirty minutes.",
                "exampleCn": "十月六日大桥上早高峰的严重拥堵导致我们前往机场的接驳行程延误了半小时。"
            },
            {
                "word": "Detour",
                "phonetic": "/ˈdiːtʊər/",
                "pos": "n./v.",
                "def": "绕道；改走备选公路",
                "exampleEn": "The chauffeur took a smart detour through the ring road to bypass the highway accident.",
                "exampleCn": "司机果断绕道经由城市外环线行驶，巧妙避开了高速公路上的交通事故拥堵点。"
            },
            {
                "word": "Punctuality",
                "phonetic": "/ˌpʌŋktʃuˈæləti/",
                "pos": "n. 名词",
                "def": "守时；准时准点性",
                "exampleEn": "Punctuality is regarded as a cornerstone of credibility when meeting Middle Eastern executives.",
                "exampleCn": "在拜访中东地区商界高层时，严守时间被视为建立企业信誉与尊重的基石准则。"
            }
        ],
        "sentences": [
            {
                "scenario": "因突发大堵车向会谈外方礼貌通报可能晚到",
                "en": "Due to gridlock traffic near the city center, we may arrive approximately 10 minutes past our 14:00 appointment.",
                "cn": "由于市中心附近出现大面积交通瘫痪拥堵，我们可能会比原定的14点会晤晚到大约10分钟左右。",
                "tip": "gridlock traffic 指‘完全瘫痪寸步难行的交通大塞车’，说明晚到原因极具信服力。"
            },
            {
                "scenario": "叮嘱司机提前出发预留充裕时间",
                "en": "Let's push our hotel pickup up by 30 minutes to make certain we don't cut it close before the ministerial meeting.",
                "cn": "我们把酒店接驾出发时间提前30分钟吧，确保部委重要会谈前绝不会卡点仓促入场。",
                "tip": "not cut it close 是‘别把时间卡得太死/避免仓促赶点’的极高频地道商务谚语。"
            },
            {
                "scenario": "利用乘车时间向领导口头简要过一遍议程",
                "en": "While we are en route to the venue, I can run through the bios of the three key attendees you are meeting.",
                "cn": "在乘车前往会场的路上，我可以为您简要过一遍待会儿即将接见的这三位核心外宾的个人履历背景。",
                "tip": "en route to the venue（前往会场途中），有效盘活车上碎裂时间。"
            }
        ]
    },
    {
        "day": 25,
        "topic": "🎤 国际展会/论坛入场与注册",
        "words": [
            {
                "word": "Badge",
                "phonetic": "/bædʒ/",
                "pos": "n. 名词",
                "def": "参展证；VIP嘉宾出入证胸牌",
                "exampleEn": "Please present your confirmation QR code at the registration counter to collect your VIP badge.",
                "exampleCn": "请在现场注册登记台出示确认二维码，以领取您的VIP贵宾参会胸牌。"
            },
            {
                "word": "Keynote Speaker",
                "phonetic": "/ˈkiːnoʊt ˈspiːkər/",
                "pos": "n. 短语",
                "def": "主旨演讲嘉宾",
                "exampleEn": "Our director is invited as a keynote speaker for the plenary session on green energy transition.",
                "exampleCn": "我们的领导受邀在绿色能源转型全体大会上发表重磅主旨演讲。"
            },
            {
                "word": "Lanyard",
                "phonetic": "/ˈlænjɑːd/",
                "pos": "n. 名词",
                "def": "证件挂绳；工卡挂绳",
                "exampleEn": "All summit attendees are required to wear their security badges and lanyards prominently at all times.",
                "exampleCn": "所有峰会参会人员必须时刻在胸前明显位置佩戴安保凭证及挂绳。"
            }
        ],
        "sentences": [
            {
                "scenario": "在展会VIP快速注册通道核验证件",
                "en": "Good morning, we are pre-registered VIP delegates; here are our confirmation letters and passport IDs.",
                "cn": "早上好，我们是预先登记注册的VIP贵宾代表团，这是我们的确认函及护照证件。",
                "tip": "pre-registered VIP delegates 走贵宾预先注册通道，秒速打牌通关进馆。"
            },
            {
                "scenario": "引导演讲领导前往VIP贵宾备场室",
                "en": "The organizers have reserved Speaker Holding Room 3 on the second floor where you can review your slides quietly.",
                "cn": "主办方在二楼为您预留了3号贵宾演讲人备场室，您可以在那里安静梳理演讲PPT讲稿。",
                "tip": "Speaker Holding Room 是高级国际会议中保障演讲嘉宾不受外界打扰的核心场所。"
            },
            {
                "scenario": "会前对齐技术音控台翻页笔与麦克风",
                "en": "Could the stage manager test the presentation clicker and lavalier mic before our director takes the podium?",
                "cn": "在领导登台前，能否请舞台场控老师提前试一下演讲翻页笔和无线领夹胸麦？",
                "tip": "takes the podium 表示‘正式登台演讲’，舞台会务标准用词。"
            }
        ]
    },
    {
        "day": 26,
        "topic": "☕ 商务茶歇与中场社交破冰",
        "words": [
            {
                "word": "Networking",
                "phonetic": "/ˈnetwɜːkɪŋ/",
                "pos": "n. 名词",
                "def": "人脉拓展；行业商务社交",
                "exampleEn": "The mid-morning coffee break provides an ideal networking window to connect with local prospective clients.",
                "exampleCn": "上午的茶歇时段为与当地潜在优质客户建立人脉连接提供了绝佳的社交窗口期。"
            },
            {
                "word": "Business Card",
                "phonetic": "/ˈbɪznəs kɑːrd/",
                "pos": "n. 短语",
                "def": "名片",
                "exampleEn": "Allow me to exchange business cards with you; my direct mobile and WeChat are printed on the back.",
                "exampleCn": "请允许我与您交换一下名片，我个人的直线电话和微信号均印在名片背面。"
            },
            {
                "word": "Small Talk",
                "phonetic": "/smɔːl tɔːk/",
                "pos": "n. 短语",
                "def": "闲聊；商务社交寒暄破冰",
                "exampleEn": "Engaging in pleasant small talk about local heritage helps break the ice before heavy commercial talks.",
                "exampleCn": "在深入繁重商业谈判之前，就当地历史名胜展开轻松愉悦的寒暄有助于快速破冰融洽气氛。"
            }
        ],
        "sentences": [
            {
                "scenario": "在茶歇时主动结识外籍商务高管",
                "en": "I really enjoyed your panel insights on regional infrastructure; allow me to briefly introduce our group.",
                "cn": "我非常赞赏您刚才圆桌论坛上关于区域基础设施的独到见解，请允许我简要向您介绍我们集团。",
                "tip": "以对方刚才演讲内容为切入点破冰赞美，是极高情商的人脉结识法则。"
            },
            {
                "scenario": "巧妙协助领导从中场闲聊中脱身进入下一议程",
                "en": "Excuse me, Mr. Zhang, the host has invited both delegations to move to Conference Hall A for the signing ceremony.",
                "cn": "不好意思打扰一下张总，东道主已经邀请双方代表团移步A会议厅，准备进行正式签约仪式。",
                "tip": "秘书适时而体面地介入，帮助领导礼貌告别当前交谈、精准把控议程节点。"
            },
            {
                "scenario": "建议会后建立领英或工作联络",
                "en": "Let's definitely keep in touch; I will connect with you on LinkedIn and share our corporate brochure this afternoon.",
                "cn": "我们后续保持密切常态联系，我下午会在领英上添加您为好友，并给您发送我们集团的电子宣传册。",
                "tip": "海外涉外人脉拓展中，LinkedIn（领英）是跨国企业高管最信赖的职业社交平台。"
            }
        ]
    },
    {
        "day": 27,
        "topic": "🔒 差旅物资保管与商业保密",
        "words": [
            {
                "word": "Confidential",
                "phonetic": "/ˌkɒnfɪˈdenʃl/",
                "pos": "adj. 形容词",
                "def": "机密的；需严格保密的",
                "exampleEn": "All commercial bid files and technical tender documents are strictly confidential and must not be left unattended.",
                "exampleCn": "所有商业标书文件及技术投函资料均属严格绝密级材料，切不可遗留在无人看管处。"
            },
            {
                "word": "Hotel Safe",
                "phonetic": "/hoʊˈtel seɪf/",
                "pos": "n. 短语",
                "def": "客房电子保险箱",
                "exampleEn": "Please store backup passports, corporate seals, and master contracts inside the in-room hotel safe.",
                "exampleCn": "请将备用护照正本、企业印章及母合同文本统一妥善存放在客房内的电子保险箱中。"
            },
            {
                "word": "Non-Disclosure Agreement (NDA)",
                "phonetic": "/ˌnɒn dɪsˈkloʊʒər əˈɡriːmənt/",
                "pos": "n. 短语",
                "def": "保密协议",
                "exampleEn": "Both corporate parties signed a mutual NDA prior to sharing proprietary architectural blueprints.",
                "exampleCn": "在共享专有建筑工程图纸之前，双方企业法人已正式签署了双边互惠保密协议。"
            }
        ],
        "sentences": [
            {
                "scenario": "提醒团队在外就餐时避免大声讨论核心商务数字",
                "en": "Let's refrain from discussing sensitive quotation figures or bidding strategies in open hotel lobbies and restaurants.",
                "cn": "在酒店开放式大堂及公共餐厅用餐时，请大家避免公开发声谈论敏感的报价数字及投标商业底牌。",
                "tip": "refrain from discussing sensitive figures 是高标准商务差旅纪律的铁律要求。"
            },
            {
                "scenario": "离开会议室前彻底清理现场废弃草稿纸",
                "en": "Please ensure all draft negotiation notes and whiteboard diagrams are cleared before we vacate the boardroom.",
                "cn": "在我们离开会议室之前，请务必彻底收回销毁所有手写草稿谈判纪要并擦除白板架构图。",
                "tip": "vacate the boardroom（退离会议室），防止被后续使用者窥视商业机密。"
            },
            {
                "scenario": "使用带密码保护的加密U盘传递资料",
                "en": "The financial forecast files on this USB flash drive are encrypted with a 256-bit password for transport safety.",
                "cn": "该U盘中存储的财务测算模型文件已采用256位密码加密，确保差旅随身携带过程中的绝对安全。",
                "tip": "encrypted with password 彰显数字化商务差旅的专业严谨防护规范。"
            }
        ]
    },
    {
        "day": 28,
        "topic": "🛍️ 商务伴手礼挑选与赠送礼仪",
        "words": [
            {
                "word": "Token of Appreciation",
                "phonetic": "/ˈtoʊkən əv əˌpriːʃiˈeɪʃn/",
                "pos": "n. 短语",
                "def": "纪念性伴手礼；答谢心意之礼",
                "exampleEn": "Our delegation presented a traditional handcrafted porcelain tea set as a token of appreciation to the host.",
                "exampleCn": "我们代表团向东道主馈赠了一套精美的传统手工陶瓷茶具，以此表达诚挚的答谢之意。"
            },
            {
                "word": "Souvenir",
                "phonetic": "/ˌsuːvəˈnɪər/",
                "pos": "n. 名词",
                "def": "当地特产伴手礼；旅游纪念品",
                "exampleEn": "The director selected premium Moroccan Argan oil and local artisanal leather crafts as souvenirs for headquarters.",
                "exampleCn": "领导挑选了顶级摩洛哥阿甘油及当地手工皮具工艺品，作为带回总部的伴手礼特产。"
            },
            {
                "word": "Cultural Sensitivity",
                "phonetic": "/ˈkʌltʃərəl ˌsensəˈtɪvəti/",
                "pos": "n. 短语",
                "def": "文化敏感性；跨文化礼俗尊重",
                "exampleEn": "Gift selection must demonstrate cultural sensitivity and respect for local traditions and taboos.",
                "exampleCn": "挑选商务礼品必须兼顾文化包容性，严格尊重当地的宗教习俗、礼节讲究及禁忌事项。"
            }
        ],
        "sentences": [
            {
                "scenario": "在会谈尾声正式向外宾赠送礼物",
                "en": "On behalf of our company, we would like to present this small gift to celebrate our enduring friendship.",
                "cn": "我谨代表我们公司，向贵方呈上这份心意微礼，以庆祝我们双方历久弥新的深厚友谊。",
                "tip": "present this small gift 是涉外礼宾赠礼时谦逊得体、不卑不亢的标准国际表达。"
            },
            {
                "scenario": "向外宾讲解礼品背后的东方文化寓意",
                "en": "This hand-embroidered silk artwork symbolizes longevity, prosperity, and seamless bilateral cooperation.",
                "cn": "这幅手工双面刺绣真丝艺术品蕴含着长青、繁荣昌盛以及双方精诚合作的美好寓意。",
                "tip": "向外方讲述礼品承载的文化内涵故事，能极大升华赠礼的精神价值与记忆点。"
            },
            {
                "scenario": "礼貌双手接领外方回赠的纪念礼品",
                "en": "Thank you so much for this exquisite local craftsmanship; we will display it with pride at our headquarters.",
                "cn": "非常感谢贵方赠送如此精妙的当地手工艺术杰作，回国后我们必将自豪地陈列于总部展厅中。",
                "tip": "display it with pride 是令受礼外方最为欢喜欣慰的高规格答谢赞语。"
            }
        ]
    },
    {
        "day": 29,
        "topic": "🧾 差旅发票与财务报销凭证",
        "words": [
            {
                "word": "Tax Invoice",
                "phonetic": "/tæks ˈɪnvɔɪs/",
                "pos": "n. 短语",
                "def": "正规税务发票；增值税发票",
                "exampleEn": "Please request an official stamped tax invoice showing the hotel's tax registration identification number.",
                "exampleCn": "请索要盖有官方印章并载明酒店纳税人识别号的正规税务发票。"
            },
            {
                "word": "Boarding Pass",
                "phonetic": "/ˈbɔːrdɪŋ pæs/",
                "pos": "n. 短语",
                "def": "登机牌（原件）",
                "exampleEn": "Corporate audit policies strictly require paper boarding passes as physical proof of international flight travel.",
                "exampleCn": "公司审计制度严格规定必须留存纸质登机牌原件，作为国际航班实际出行的物理审计证明。"
            },
            {
                "word": "Per Diem",
                "phonetic": "/ˌpɜːr ˈdiːem/",
                "pos": "n./adj.",
                "def": "每日出差包干伙食/零用津贴",
                "exampleEn": "Delegation members are eligible for standard overseas per diem allowances calculated by destination tier.",
                "exampleCn": "代表团成员有权依照所前往国家城市的差旅档次标准，享受标准的海外每日差旅包干伙食津贴。"
            }
        ],
        "sentences": [
            {
                "scenario": "向财务部呈交完整的差旅报销案卷",
                "en": "Here is the consolidated reimbursement dossier including flight stubs, hotel folios, and taxi receipts.",
                "cn": "这是整理好的差旅报销全套案卷，内附登机牌票根、酒店结算水单及打车小票凭据。",
                "tip": "reimbursement dossier（报销卷宗档案），条理清晰，财务一次审核通过。"
            },
            {
                "scenario": "发票丢失时的合规替代声明",
                "en": "Since the local driver could not issue a formal receipt, I have filled out an electronic expense declaration form.",
                "cn": "由于当地出租车司机无法出具正规发票，我已依规填报了小额差旅开支情况说明单附卷。",
                "tip": "expense declaration form（开支情况自述声明），解决海外某些落后地区无票痛点。"
            },
            {
                "scenario": "外币汇率折算核对",
                "en": "All Moroccan Dirham expenses have been converted into US Dollars using the official Central Bank conversion rate on the transaction date.",
                "cn": "所有摩洛哥迪拉姆开支均已按实际刷卡交易发生当日的央行官方牌价折算为美元入账核算。",
                "tip": "on transaction date 符合国际跨国公司财务严格的公允入账标准。"
            }
        ]
    },
    {
        "day": 30,
        "topic": "✈️ 返程值机与贵宾休息室",
        "words": [
            {
                "word": "Departure Lounge",
                "phonetic": "/dɪˈpɑːrtʃər laʊndʒ/",
                "pos": "n. 短语",
                "def": "国际出发贵宾候机休息室",
                "exampleEn": "We can unwind and catch up on emails in the Star Alliance departure lounge before our red-eye boarding.",
                "exampleCn": "在红眼航班登机前，我们可以先在星空联盟出发贵宾厅稍作休整并处理手头的邮件。"
            },
            {
                "word": "Gate Change",
                "phonetic": "/ɡeɪt tʃeɪndʒ/",
                "pos": "n. 短语",
                "def": "登机口临时变更",
                "exampleEn": "Keep an eye on the flight display screen in case there is a last-minute gate change announced.",
                "exampleCn": "请密切留意贵宾厅内的航班信息显示屏，以防临时通知临时变更登机口。"
            },
            {
                "word": "Duty-Free Allowance",
                "phonetic": "/ˌdjuːti ˈfriː əˈlaʊəns/",
                "pos": "n. 短语",
                "def": "回国入境免税购物限额",
                "exampleEn": "Verify your home customs duty-free allowance before purchasing cosmetics, luxury goods, or tobacco.",
                "exampleCn": "在免税店采购化妆品、奢侈品或烟酒之前，请先核实国内海关入境免税额度要求。"
            }
        ],
        "sentences": [
            {
                "scenario": "在机场贵宾室前台核验身份入场",
                "en": "Good evening, we are two business class passengers on Flight MS779 eligible for lounge access.",
                "cn": "晚上好，我们是MS779次航班的两位商务舱旅客，前来使用贵宾室候机休息。",
                "tip": "eligible for lounge access（享有使用休息室权益），干练从容。"
            },
            {
                "scenario": "留意并提醒领导登机广播",
                "en": "Our boarding gate 22 has just started boarding; it is a five-minute walk from here, so we can head over now.",
                "cn": "我们位于22号的登机口刚刚开始登机广播了；从休息室步行过去大约5分钟，我们可以启程移步了。",
                "tip": "精准把控‘步行耗时’并及时提醒动身，是高管随行秘书的典范素养。"
            },
            {
                "scenario": "确认返程航班行李直达北京目的地",
                "en": "The check-in agent confirmed our four suitcases are checked through all the way to Beijing Capital Airport.",
                "cn": "值机地勤已确认我们的四件大行李箱已经一路直挂托运至北京首都国际机场。",
                "tip": "checked through all the way to... 让长途飞行旅程彻底免除提箱中转顾虑。"
            }
        ]
    },
    {
        "day": 31,
        "topic": "🌟 出差圆满复盘与客户感谢信",
        "words": [
            {
                "word": "Follow-up",
                "phonetic": "/ˈfɒloʊ ʌp/",
                "pos": "n./adj.",
                "def": "后续跟进事项；跟踪落实邮件",
                "exampleEn": "I drafted a formal follow-up letter expressing appreciation for the warm hospitality in Cairo.",
                "exampleCn": "我已起草了一封正式的跟进感谢信，对开罗各方给予的热情周到款待表达诚挚谢意。"
            },
            {
                "word": "Deliverable",
                "phonetic": "/dɪˈlɪvərəbl/",
                "pos": "n. 名词",
                "def": "双方承诺落地的交付成果",
                "exampleEn": "We committed to delivering the detailed commercial proposal within seven business days of our return.",
                "exampleCn": "我们已向对方承诺，在代表团回国后的七个工作日内交付详尽的商业商务提案。"
            },
            {
                "word": "Hospitality",
                "phonetic": "/ˌhɒspɪˈtæləti/",
                "pos": "n. 名词",
                "def": "热情款待；周到接待礼仪",
                "exampleEn": "The generous hospitality extended by the Moroccan team established a strong foundation for future joint ventures.",
                "exampleCn": "摩洛哥团队给予的热情周到款待，为双方未来建立合资合作项目奠定了坚实的互信基础。"
            }
        ],
        "sentences": [
            {
                "scenario": "出差返程后第一时间向海外接待方发送感谢函",
                "en": "On behalf of our delegation, I wish to extend our deepest gratitude for your gracious hospitality throughout our visit.",
                "cn": "我谨代表我们代表团全体成员，对访问期间贵方给予的无微不至的热情款待致以最深切的谢意！",
                "tip": "gracious hospitality 是国际高规格商旅感谢函中规格最高、最受赞许的黄金用词。"
            },
            {
                "scenario": "在信中重申会谈达成的关键共识与下一步动作",
                "en": "We were deeply encouraged by our discussions and look forward to executing the agreed action items in the coming weeks.",
                "cn": "本次会谈的丰硕共识令我们备受鼓舞，我们热切期待在接下来的数周内高效推进各项既定落实事项。",
                "tip": "executing the agreed action items 体现雷厉风行、重信守诺的顶级商业作风。"
            },
            {
                "scenario": "热情邀请海外合作伙伴未来回访中国总部",
                "en": "We sincerely hope to have the honor of reciprocating your exceptional hospitality when you visit Beijing next spring.",
                "cn": "我们由衷期盼在明春您访问北京之际，能有幸回敬您和团队同样卓越周到的热情款待！",
                "tip": "reciprocate hospitality（回敬款待/礼尚往来），大国大司大格局的风范尽显。"
            }
        ]
    }
]

# Write to english_data.json
with open('english_data.json', 'w', encoding='utf-8') as f:
    json.dump(curriculum, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(curriculum)} days of Business Travel English curriculum!")

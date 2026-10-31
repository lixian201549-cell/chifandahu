# -*- coding: utf-8 -*-
import json

with open('english_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

assert len(data) == 31, f"Expected 31 days of English data, got {len(data)}"

for day in data:
    assert 'day' in day and isinstance(day['day'], int), "Missing day number"
    assert 'topic' in day and len(day['topic']) > 0, f"Missing topic for day {day['day']}"
    assert 'words' in day and len(day['words']) == 3, f"Expected 3 words for day {day['day']}"
    assert 'sentences' in day and len(day['sentences']) == 3, f"Expected 3 sentences for day {day['day']}"
    for w in day['words']:
        assert 'word' in w and 'phonetic' in w and 'pos' in w and 'def' in w and 'exampleEn' in w and 'exampleCn' in w, f"Incomplete word schema in day {day['day']}"
    for s in day['sentences']:
        assert 'scenario' in s and 'en' in s and 'cn' in s and 'tip' in s, f"Incomplete sentence schema in day {day['day']}"

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

assert '每日英语 · 2027北欧漫游' in html, "Missing 每日英语 · 2027北欧漫游 in index.html"
assert '❄️ Nordic Journey' in html, "Missing ❄️ Nordic Journey in index.html"
assert '今日北欧旅行核心词汇' in html, "Missing 今日北欧旅行核心词汇 in index.html"
assert 'Aurora Borealis' in html, "Missing Nordic vocabulary Aurora Borealis in compiled HTML"
assert '北欧生活习惯与旅行Tips' in html, "Missing 北欧生活习惯与旅行Tips in compiled HTML"

print("✓ All 31-day Nordic Travel & Lifestyle English curriculum checks passed successfully 100%!")

import json

with open('assets_b64.json', 'r', encoding='utf-8') as f:
    assets = json.load(f)

with open('english_data.json', 'r', encoding='utf-8') as f:
    english_data_raw = f.read()

# Load base64 assets
img_ordinary_doghouse = assets['ordinary_doghouse']
img_border_snoopy = assets['border_snoopy']
img_woodstock = assets['woodstock']
img_supervisor_secretary = assets['supervisor_secretary']
img_beagle_scout = assets['beagle_scout']
img_flying_ace = assets['flying_ace']
img_author = assets['author_typewriter']
img_artist_dream = assets['artist_dream']
img_daily_english = assets['daily_english']
img_canonical = assets['canonical']

print("Loaded all assets successfully. Now generating build_html.py...")

with open('assemble_final_app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace rows.join('\n') with rows.join('\\n')
text = text.replace("return rows.join('\\n');", "return rows.join('\\\\n');")
text = text.replace("rows.push(rowVals.join('\t'));", "rows.push(rowVals.join('\\\\t'));")
text = text.replace("].join('\n');", "].join('\\\\n');")
text = text.replace("split(/\\r?\\n/);", "split(/\\\\r?\\\\n/);")
text = text.replace("split(/[\\t,;|]+|\\s{2,}/)", "split(/[\\\\t,;|]+|\\\\s{2,}/)")
text = text.replace("replace(/^[0-9一二三四五六七八九十]+[、.\\s]+/, '')", "replace(/^[0-9一二三四五六七八九十]+[、.\\\\s]+/, '')")
text = text.replace("replace(/\\d+/g)", "replace(/\\\\d+/g)")

with open('assemble_final_app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Escaping fixed.")

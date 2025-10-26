import os
import re

INPUT_FILE = "chatlog.txt"
OUTPUT_FILE = "index.html"
ICON_FOLDER = "images"

def name_to_icon(name):
    sanitized = re.sub(r'[\\/:*?"<>|@ ]', '_', name.split('@')[0])
    return f"{ICON_FOLDER}/{sanitized}.png"

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>チャットログ</title>
    <style>
        body {{
            font-family: sans-serif;
            background-color: #778899;
            padding: 20px;
            max-width: 600px;
            margin: auto;
            font-size: 12px;
        }}
        .chat {{
            display: flex;
            align-items: flex-start;
            margin: 8px 0;
        }}
        .icon {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
            flex-shrink: 0;
        }}
        .bubble {{
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            position: relative;
            max-width: 80%;
            word-break: break-word;
            font-size: 12px;
        }}
        .bubble .meta {{
            font-size: 0.7em;
            color: #888;
            margin-bottom: 3px;
        }}
        .bubble div {{
            white-space: pre-wrap;
        }}
        .meta {{
            font-size: 0.7em;
            color: #eee;
            margin: 15px 0 5px 0;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ccc;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
{body}
</body>
</html>
'''

def parse_chat_line(line):
    return re.match(r"^(\d{4}年\d{1,2}月\d{1,2}日) (\d{1,2}:\d{2}) ([^ ]+) (.+)$", line)

def load_chat_log():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    chat_html = ""
    current_date = None
    current_message_lines = []
    current_meta = None

    def flush_message():
        nonlocal chat_html, current_message_lines, current_meta
        if not current_meta or not current_message_lines:
            return
        date, time, name = current_meta
        message = "\n".join(current_message_lines)
        icon_path = name_to_icon(name)

        # HTMLエスケープ
        message = (
            message.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
        )

        chat_html += f'''
        <div class="chat">
            <img class="icon" src="{icon_path}" alt="{name}">
            <div class="bubble">
                <div class="meta">{name}・{time}</div>
                <div>{message}</div>
            </div>
        </div>
        '''

        current_message_lines = []
        current_meta = None

    for line in lines:
        line = line.rstrip('\n')
        match = parse_chat_line(line)
        if match:
            flush_message()
            date, time, name, message = match.groups()

            if current_date != date:
                if current_date is not None:
                    chat_html += "<hr>\n"
                chat_html += f"<div class='meta'>{date}</div>\n"
                current_date = date

            current_meta = (date, time, name)
            current_message_lines = [message]
        else:
            # 追加の行とみなして蓄積
            if current_message_lines is not None:
                current_message_lines.append(line)

    flush_message()
    return chat_html

def generate_html():
    body = load_chat_log()
    html = HTML_TEMPLATE.format(body=body)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {OUTPUT_FILE} を作成しました！")

if __name__ == "__main__":
    generate_html()
    input("何かキーを押すと終了します…")
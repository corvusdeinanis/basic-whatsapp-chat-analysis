import re
import os
from collections import defaultdict

def parse_and_split_whatsapp_export(file_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'r', encoding='utf-8') as file:
        chat_lines = file.readlines()

    messages = defaultdict(list)
    current_sender = None
    current_message = []

    pattern = re.compile(r'^(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}\s?[APap][Mm]) - (.*?): (.*)$')

    for line in chat_lines:
        match = pattern.match(line)
        if match:
            if current_sender:
                messages[current_sender].append(' '.join(current_message))
            date, time, sender, message = match.groups()
            current_sender = sender
            current_message = [f"{date} {time} - {message}"]
            print(f"Matched line: {line.strip()} | Sender: {sender}")
        else:
            if current_sender:
                current_message.append(line.strip())
            else:
                print(f"No match for line: {line.strip()}")  

    if current_sender:
        messages[current_sender].append(' '.join(current_message))

    for sender, msgs in messages.items():
        sender_filename = re.sub(r'[^\w\-_\. ]', '_', sender) + '.txt'
        file_path = os.path.join(output_dir, sender_filename)
        print(f"Writing to file: {file_path}")
        with open(file_path, 'w', encoding='utf-8') as sender_file:
            for msg in msgs:
                sender_file.write(msg + '\n')

    return messages

messages = parse_and_split_whatsapp_export('whatsapp_chat.txt', 'output')

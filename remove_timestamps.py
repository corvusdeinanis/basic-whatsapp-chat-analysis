import os
import re

directory_path = 'output'

timestamp_pattern = re.compile(r'^\d{2}/\d{2}/\d{2} \d{1,2}:\d{2}\s?[APap][Mm] - ')

def remove_timestamps_from_files(directory):
    print(f"Starting to process files in directory: {directory}")
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            print(f"\nProcessing file: {file_path}")

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                print(f"Read {len(lines)} lines from {filename}")
                
                cleaned_lines = []
                for line in lines:
                    cleaned_line = timestamp_pattern.sub('', line)
                    cleaned_lines.append(cleaned_line)
                    print(f"Original line: '{line.strip()}'")
                    print(f"Cleaned line: '{cleaned_line.strip()}'")

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(cleaned_lines)
                
                print(f"Timestamps removed and file overwritten: {filename}")

            except Exception as e:
                print(f"Error processing file {filename}: {e}")
        else:
            print(f"Skipping non-text file: {filename}")

remove_timestamps_from_files(directory_path)

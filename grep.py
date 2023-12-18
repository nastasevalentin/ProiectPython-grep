import os
import re
import argparse

def grep(file_path, pattern, ignore_case=False, count=False, not_match=False):
    try:
        flags = re.IGNORECASE if ignore_case else 0
        matches = []

        with open(file_path, 'r', errors='ignore') as file:
            for line in file:
                line_matches = re.findall(pattern, line, flags=flags)
                if line_matches:
                    matches.append(line)

        if count:
            return len(matches)
        elif not matches:
            print(f"The patterns '{pattern}' was not found in the file '{file_path}'")
            return None
        else:
            return matches
    except FileNotFoundError:
        return 0

def search_string_in_file(file_path, patterns, count=False, ignore_case=False, not_match=False):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            matches = 0
            matching_lines = []
            for line_number, line in enumerate(lines, 1):
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE if ignore_case else 0):
                        matches += 1
                        matching_lines.append(line)
            if count:
                print(f"{file_path}: {matches} matches")
            for line in matching_lines:
                print(line, end='')
            if not_match and matches == 0:
                print(f"The patterns '{patterns}' were not found in the file '{file_path}'")
            elif matches == 0 and not count:
                print(f"The patterns '{patterns}' were not found in the file '{file_path}'")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def search_files(directory, patterns, ignore_case=False, count=False, not_match=False):
    matches = {}
    text_file_extensions = ['.txt', '.py', '.md', '.csv', '.json', '.xml', '.html', '.js', '.css', '.c', '.cpp', '.java']

    for root, _, files in os.walk(directory):
        if '/.' in root:
            continue
        for file in files:
            if file.startswith('.'):
                continue
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1]

            if file_extension not in text_file_extensions:
                print(f"Skipping non-text file: {file_path}")
                continue

            print(f"Processing file: {file_path}")
            for pattern in patterns:
                file_match = grep(file_path, pattern, ignore_case, count, not_match)
                if file_match:
                    if count:
                        matches[file_path] = file_match
                    else:
                        matches[file_path] = file_match
    return matches

def main():
    parser = argparse.ArgumentParser(description='A Python grep utility')
    parser.add_argument('pattern', nargs='+',  help='Pattern to search for (regular expression)')
    parser.add_argument('path', help='File or directory path')
    parser.add_argument('-ignoreCase', action='store_true', help='Ignore case in the search')
    parser.add_argument('-NOT', action='store_true', help='Invert match, i.e., select non-matching lines/files')
    parser.add_argument('-count', action='store_true', help='Print only the number of matches')

    args = parser.parse_args()

    patterns = args.pattern
    path = args.path
    ignore_case = args.ignoreCase
    count = args.count
    not_match = args.NOT

    if os.path.isfile(path):
        search_string_in_file(path, patterns, count, ignore_case, not_match)
    elif os.path.isdir(path):
        matches = search_files(path, patterns, ignore_case, count, not_match)
        for file, match in matches.items():
            if count:
                print(f"{file}: {match} matches")
            else:
                if not_match==0:
                    print(f"{file}: {match}")

if __name__ == '__main__':
    main()
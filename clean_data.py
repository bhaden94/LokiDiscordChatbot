import re
import csv

raw_file_name = "raw_loki_transcripts.txt"
stripped_file_name = "stripped_loki_transcripts.txt"
csv_file_name = "loki_transcripts.csv"


# format transcript file so we can easily create csv later
def format_file():
    raw_transcipt = open(raw_file_name, "r", encoding="utf8")
    stripped_transcript = open(stripped_file_name, "w", encoding="utf8")
    # clear contents
    stripped_transcript.truncate(0)
    stripped_lines = []

    for line in raw_transcipt:
        # remove all characters and lines we don't need
        stripped_line = re.sub(
            '\{.*\}|\[.*?\]|\=.*\=|\(.*\)|\'\'\'|\[|\]|\{|\}', '', line)
        # if line has content then write to file, otherwise it is just blank and can be ignored
        if not stripped_line.isspace():
            stripped_lines.append(stripped_line)

    # combine stripped lines so each characters dialog is on one line
    new_lines = []
    for line in stripped_lines:
        # if line contains ':', then it is a new character speaking
        line = line.replace('\n', '')
        line = line.strip()
        if ":" in line:
            new_lines.append(line)
        # if line does not containe ':', it is the same character speaking
        else:
            new_lines[-1] = new_lines[-1] + ' ' + line

    # write to new file
    for line in new_lines:
        stripped_transcript.write(line + '\n')

    raw_transcipt.close()
    stripped_transcript.close()


# take formatted text file and create csv with name and line of each character
def create_csv():
    stripped_transcript = open(stripped_file_name, "r", encoding="utf8")
    fieldnames = ['name', 'line']
    data = []

    for line in stripped_transcript:
        split_line = line.split(":")
        #print(len(split_line))
        current_line = {fieldnames[0]: split_line[0], fieldnames[1].strip(): split_line[1].strip()}
        data.append(current_line)

    with open(csv_file_name, 'w', newline='') as csv_file:
        # clear file
        csv_file.truncate(0)
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    format_file()
    create_csv()


if __name__ == "__main__":
    main()

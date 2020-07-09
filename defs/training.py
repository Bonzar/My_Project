import pyperclip


def exercise(text_by_line):
    global new_text
    for i in range(len(text_by_line)):
        if i % 2 == 0:
            new_text += '* ' + text_by_line[i] + ' / '
        else:
            values = text_by_line[i].split('rest')
            new_text += values[0].split()[0]
            if 'hold' in values[0]:
                new_text += ' hold '
            if 'seconds' in values[0]:
                new_text += ' sec '
            if 'reps' in values[0]:
                new_text += ' reps '
            if 'each' in values[0]:
                new_text += 'each '
            if len(text_by_line) - i != 1 or len(text_by_line) <= 6:
                new_text += '/ rest ' + values[1].split()[0] + ' sec'
            new_text += '\n'


text = f'''{pyperclip.paste()}'''
new_text = ''

text_by_line = text.split('\n')
lineNumber, round_count = 0, 1
numbers_line_dict = {}
for line in text_by_line:
    if 'warm-up' in line.lower():
        numbers_line_dict[f'## Warm-up x 2\n'] = lineNumber
    if 'round' in line.lower():
        for n in range(2, len(line.split())):
            if line.split()[n].isdigit():
                sets = line.split()[n]
        numbers_line_dict[f'## Round {round_count} | {sets} sets\n'] = lineNumber
        round_count += 1
    lineNumber += 1

for number_of_circle, circle in enumerate(numbers_line_dict.keys()):
    end_index = None
    start_index = numbers_line_dict[circle]
    if number_of_circle + 1 != len(numbers_line_dict.keys()):
        end_index = numbers_line_dict[list(numbers_line_dict.keys())[number_of_circle + 1]] - 1
    new_text += circle
    exercise(text_by_line[start_index + 1:end_index])
    new_text += '**rest 2 minutes**\n'

print(new_text)
pyperclip.copy(new_text)

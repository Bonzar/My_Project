import pyperclip, os, shutil

text = f'''{pyperclip.paste()}'''

new_text = ''
text_by_line = text.split('\n')
lineNumber, round_count = 0, 1
numbers_line_dict = {}
for line in text_by_line:
    print(line)
for line in text_by_line:
    if 'warm-up' in line.lower():
        text_by_line.remove(line)
    if 'rest 2 minutes' in line.lower():
        text_by_line.remove(line)
for line in text_by_line:
    if 'round' in line.lower():
        text_by_line.remove(line)
print(text_by_line)
os.chdir('C:/Users/Татьяна/iCloudDrive/Упражнения')
n = 8
i = 1
while True:
    try:
        os.mkdir(f'C:/Users/Татьяна/iCloudDrive/Упражнения/{n + i/10}')
    except FileExistsError:
        i += 1
    else:
        break
for exercise in text_by_line:
    directory = f'C:/Users/Татьяна/iCloudDrive/Упражнения/{n + i/10}'
    shutil.copy(f'C:/Users/Татьяна/iCloudDrive/Упражнения/{exercise.split(" / ")[0][2:]}.mov', directory)
print(new_text)
pyperclip.copy(new_text)

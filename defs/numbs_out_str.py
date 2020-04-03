from functools import reduce


def numbs_out_str(line_with_numbers):
    full_number_list = []
    list_numbers_inline = []
    for hours in line_with_numbers:
        if hours.isdigit():
            list_numbers_inline.append(hours)
    ind = 0
    count = 0
    numbers = [list_numbers_inline[ind]]
    for i in range(len(list_numbers_inline)):
        ind += 1
        try:
            while line_with_numbers.find(list_numbers_inline[ind - 1], line_with_numbers.find(
                    numbers[0]) + count) - line_with_numbers.find(
                list_numbers_inline[ind], line_with_numbers.find(
                    numbers[0]) + count + 1) == -1:
                numbers.append(list_numbers_inline[ind])
                ind += 1
                count += 1
            else:
                full_number_list.append(int(reduce(lambda a, b: a + b, numbers)))
                count = 0
                line_with_numbers = line_with_numbers[line_with_numbers.find(numbers[0]) + len(numbers):]
                numbers = [list_numbers_inline[ind]]
        except IndexError:
            full_number_list.append(int(reduce(lambda a, b: a + b, numbers)))
            break
    return full_number_list

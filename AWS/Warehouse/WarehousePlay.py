from json import load
from Warehouse import *

"""   Welcome to the office equipment accounting program.
    ------------------------------------------------------
    We have 4 type's of equipment:
        -Printer(P)
        -Scanner(S)
        -PrinterScanner(PS)
        -Xerox(X)
    You can add and del certain types of office equipment
    with a specific firm model and properties different
    for each type of equipment.
    ------------------------------------------------------
    Specification for models:
        First symbol(Two for PS) - abbreviation of Name office equipment
        For Scanner - after the abbreviation should be number - version of scanner
        For Printer - in the end of model should be a letter (b/c) that mean type of painting (Black&White / RGB)
        For PrinterScanner both of the top.
"""
while True:
    command = input('\n''Enter a command: ').title()
    if command == 'Add' or command == '1':
        equipment = input('Choice equipment:\n-Printer(P)\n-Scanner(S)\n-PrinterScanner(PS)\n-Xerox(X)\n:').title()
        if len(equipment) <= 2:
            equipment = short_name(equipment)
        else:
            equipment = short_name(short_name(equipment))
        if equipment == 'Back':
            continue
        adding_mode = input('Add to old model(1) or create a new?(2)\n:').lower()
        while adding_mode != 'new' and adding_mode != 'old' and adding_mode != '1' and adding_mode != '2':
            print(adding_mode)
            adding_mode = input(': ')
        if adding_mode == '1' or adding_mode == 'old':
            model = dell(equipment)
            if model is None:
                continue
        elif adding_mode == '2' or adding_mode == 'new':
            model = short_name(equipment) + input(f'Model: {short_name(equipment)}')
            firm = input('Firm: ')
            cost = input('Cost: ')
            while not cost.isdigit():
                cost = input(': ')
            cost = int(cost)
        if equipment == 'Printer':
            p = Printer(model, firm, cost)
            Printer.add_printer(p, equipment=equipment)
        elif equipment == 'Scanner':
            s = Scanner(model, firm, cost)
            Scanner.add_scanner(s, equipment=equipment)
        elif equipment == 'PrinterScanner':
            ps = PrinterScanner(model, firm, cost)
            PrinterScanner.add_printer_scanner(ps, equipment=equipment)
        elif equipment == 'Xerox':
            x = Xerox(model, firm, cost)
            Xerox.add_xerox(x, equipment=equipment)
    elif command == 'Del' or command == '2':
        equipment = input('Choice equipment:\n-Printer(P)\n-Scanner(S)\n-PrinterScanner(PS)\n-Xerox(X)\n:').title()
        if len(equipment) <= 2:
            equipment = short_name(equipment)
        else:
            equipment = short_name(short_name(equipment))
        if equipment == 'Back':
            continue
        model = dell(equipment)
        if model is None:
            continue
        if equipment == 'Printer':
            p = Printer(model)
            Printer.del_printer(p)
        elif equipment == 'Scanner':
            s = Scanner(model)
            Scanner.del_scanner(s)
        elif equipment == 'PrinterScanner':
            p = PrinterScanner(model)
            PrinterScanner.del_printer_scanner(p)
        elif equipment == 'Xerox':
            x = Xerox(model)
            Xerox.del_xerox(x)
    elif command == 'List' or command == '3':
        with open(path, 'r', encoding='utf-8') as List:
            print(List.read())
    elif command == 'Default' or command == '4':
        default()
    elif command == 'Info' or command == '5':
        info()
    elif command == 'Help' or command == '6':
        print('Available command:\n'
              '1) Add (add equipment to warehouse)\n'
              '2) Del (del equipment from warehouse)\n'
              '3) List (display the contents of the warehouse)\n'
              '4) Default (reset the contents of the warehouse)\n'
              "5) Info (available model's)\n"
              '6) Help (list of available commands)\n'
              '7) Exit (out of program)')
    elif command == 'Exit' or command == '7':
        raise SystemExit

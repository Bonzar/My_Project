import json
import re

# path = "/home/ubuntu/MyProject/AWS/Warehouse/WarehouseList.json"
path = "WarehouseList.json"


def info():
    print('List of models in Warehouse:')
    number_in_list = 1
    dict_of_models = {}
    for eqp_kind in Warehouse.list_equipment:
        for eks in Warehouse.list_equipment[eqp_kind]:
            print(f'{number_in_list}) {eks["model"]}')
            dict_of_models[number_in_list] = eks
            number_in_list += 1
    model = input('\nChoice number of model to take full info or return /back/: ')
    while (model.lower() != 'back') and (not model.isdigit() or int(model) > len(dict_of_models)):
        model = input(': ')
    if model.lower() == 'back':
        return
    else:
        f = dict_of_models[int(model)]
        for el, var in f.items():
            print(f'"{el}": {var}')
        return


def short_name(letter):
    try:
        dict_of_equipment = {'Printer': 'P', 'Scanner': 'S', 'PrinterScanner': 'PS', 'Xerox': 'X', 'P': 'Printer',
                             'S': 'Scanner', 'Ps': 'PrinterScanner', 'X': 'Xerox'}
        return dict_of_equipment[letter]
    except KeyError:
        print('Not equipment!')
        return "Back"


def dell(equipment):
    try:
        if len(Warehouse.list_equipment[equipment]):
            print('Models on warehouse:')
            dict_of_models = {}
            for i in range(len(Warehouse.list_equipment[equipment])):
                print(f'{i + 1}) {Warehouse.list_equipment[equipment][i]["model"]}')
                dict_of_models[i + 1] = Warehouse.list_equipment[equipment][i]["model"]
        else:
            raise EmptyModel
        new_model = input('Enter a model(or a number of model): ')
        while not new_model.isdigit() or int(new_model) > len(Warehouse.list_equipment[equipment]):
            new_model = input(': ')
        return dict_of_models[int(new_model)] if new_model.isdigit() else new_model
    except EmptyModel:
        return


class EmptyModel(Exception):
    def __init__(self):
        print('Nothing in list!')


class TypeOrgEquipmentError(Exception):
    def __init__(self, name, model):
        print(f'This model: {model} is not {name}')


def default():
    with open(path, 'w', encoding='utf-8') as WLj:
        list_equipment_default = {'Printer': [], 'Scanner': [], 'PrinterScanner': [], 'Xerox': []}
        json.dump(list_equipment_default, WLj, indent=4)


class Warehouse:
    try:
        with open(path, 'r', encoding='utf-8') as WLj:
            list_equipment = json.load(WLj)
    except json.decoder.JSONDecodeError and FileNotFoundError:
        default()
        with open(path, 'r', encoding='utf-8') as WLj:
            list_equipment = json.load(WLj)


def add_to_warehouse(equipment, *args):
    try:
        count = int(input(f'How many {equipment} {args[0]["firm"]} {args[0]["model"]} to add: '))
    except ValueError:
        print('Not a number was entered')
        return
    with open(path, 'w', encoding='utf-8') as WLw:
        if Warehouse.list_equipment[equipment]:
            for i in range(len(Warehouse.list_equipment[equipment])):
                if Warehouse.list_equipment[equipment][i]["model"].upper() == args[0]["model"].upper():
                    Warehouse.list_equipment[equipment][i]['count'] += count
                    json.dump(Warehouse.list_equipment, WLw, indent=4)
                    return
        Warehouse.list_equipment[equipment].append({})
        for el in args:
            Warehouse.list_equipment[equipment][-1] = {par: value for par, value in el.items()}
        Warehouse.list_equipment[equipment][-1]['count'] = count
        json.dump(Warehouse.list_equipment, WLw, indent=4)


class OrgEquipment:
    def __init__(self, model, firm=None, cost=None):
        self.firm = firm
        self.cost = cost
        self.model = model
        self._list_of_params = {'firm': firm, 'cost': cost, 'model': model}

    @classmethod
    def del_from_warehouse(cls, *args):
        try:
            count = int(input(f'How many {cls.__name__} {args[0]["model"]} to delete: '))
        except ValueError as VE:
            print('Not a number was entered')
            return
        with open(path, 'w', encoding='utf-8') as WLw:
            if Warehouse.list_equipment[cls.__name__]:
                for i in range(len(Warehouse.list_equipment[cls.__name__])):
                    if Warehouse.list_equipment[cls.__name__][i]["model"].upper() == args[0]["model"].upper():
                        if Warehouse.list_equipment[cls.__name__][i]['count'] - count <= 0:
                            del Warehouse.list_equipment[cls.__name__][i]
                        else:
                            Warehouse.list_equipment[cls.__name__][i]['count'] -= count
                        json.dump(Warehouse.list_equipment, WLw, indent=4)
                        return
            else:
                print('Nothing to delete.')


class Printer(OrgEquipment):
    def __init__(self, model, firm=None, cost=None, type_paint=None):
        super().__init__(model)
        self.type_paint = type_paint
        Printer._type_paint1(self)
        self._list_of_params = {'firm': firm, 'cost': cost, 'model': model, 'type_paint': self.type_paint}

    def _type_paint1(self):
        if self.type_paint is not None:
            pass
        elif self.model[-1].upper() == 'B':
            self.type_paint = 'Black & White'
        elif self.model[-1].upper() == 'C':
            self.type_paint = 'Colorful'

    def add_printer(self, equipment):
        add_to_warehouse(equipment, self._list_of_params)

    def del_printer(self):
        Printer.del_from_warehouse(self._list_of_params)


class Scanner(OrgEquipment):
    def __init__(self, model, firm=None, cost=None, version_scanner=None):
        super().__init__(model)
        self.version_scanner = version_scanner
        Scanner._version_scanner1(self)
        self._list_of_params = {'firm': firm, 'cost': cost, 'model': model, 'version_scanner': self.version_scanner}

    def _version_scanner1(self, number_of_version=None):
        if self.version_scanner is not None:
            pass
        elif 'PS' in self.model.split('_')[0]:
            number_of_version = self.model[2]
        else:
            number_of_version = self.model[1]
        if number_of_version.isdigit() and (1 <= int(number_of_version) <= 3):
            self.version_scanner = int(number_of_version)

    def add_scanner(self, equipment):
        add_to_warehouse(equipment, self._list_of_params)

    def del_scanner(self):
        Scanner.del_from_warehouse(self._list_of_params)


class PrinterScanner(Printer, Scanner):
    def __init__(self, model, firm=None, cost=None, version_scanner=None, type_paint=None):
        super().__init__(model)
        self.type_paint = type_paint
        Printer._type_paint1(self)
        self.version_scanner = version_scanner
        Scanner._version_scanner1(self)
        self._list_of_params = {'firm': firm, 'cost': cost, 'model': model, 'type_paint': self.type_paint,
                                'version_scanner': self.version_scanner}

    def add_printer_scanner(self, equipment):
        add_to_warehouse(equipment, self._list_of_params)

    def del_printer_scanner(self):
        PrinterScanner.del_from_warehouse(self._list_of_params)


class Xerox(OrgEquipment):
    def add_xerox(self, equipment):
        add_to_warehouse(equipment, self._list_of_params)

    def del_xerox(self):
        Xerox.del_from_warehouse(self._list_of_params)

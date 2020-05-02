import json
import re


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
            dict_of_models_to_delete = {}
            for i in range(len(Warehouse.list_equipment[equipment])):
                print(f'{i + 1}) {Warehouse.list_equipment[equipment][i]["model"]}')
                dict_of_models_to_delete[i + 1] = Warehouse.list_equipment[equipment][i]["model"]
        else:
            raise EmptyModel
        new_model = input('Enter a model(or a number of model) to delete: ')
        return dict_of_models_to_delete[int(new_model)] if new_model.isdigit() else new_model
    except EmptyModel:
        return


class EmptyModel(Exception):
    def __init__(self):
        print('Nothing to delete!')


class TypeOrgEquipmentError(Exception):
    def __init__(self, name, model):
        print(f'This model: {model} is not {name}')


def default():
    with open("WarehouseList.json", 'w', encoding='utf-8') as WLw:
        list_equipment_default = {'Printer': [], 'Scanner': [], 'PrinterScanner': [], 'Xerox': []}
        json.dump(list_equipment_default, WLw, indent=4)


class Warehouse:
    with open("WarehouseList.json", 'r', encoding='utf-8') as WL1:
        try:
            list_equipment = json.load(WL1)
        except json.decoder.JSONDecodeError:
            default()
            list_equipment = json.load(WL1)


def add_to_warehouse(equipment, *args):
    try:
        count = int(input(f'How many {equipment} {args[0]["firm"]} {args[0]["model"]} to add: '))
    except ValueError:
        print('Not a number was entered')
        return
    with open("WarehouseList.json", 'w', encoding='utf-8') as WLw:
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
        with open('WarehouseList.json', 'w', encoding='utf-8') as WLw:
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

    def _version_scanner1(self):
        if self.version_scanner is not None:
            pass
        elif 'S' in self.model:
            number_of_version = self.model[1]
            if number_of_version.isdigit() and 1 <= int(number_of_version) <= 3:
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

import json
import re


class TypeOrgEquipmentError(Exception):
    def __init__(self, name, model):
        print(f'This model: {model} is not {name}')


class Warehouse:
    with open("WarehouseList.json", 'r', encoding='utf-8') as WL1:
        list_equipment = json.load(WL1)

    @staticmethod
    def default():
        with open("WarehouseList.json", 'w', encoding='utf-8') as WLw:
            list_equipment_default = {'Printer': [], 'Scanner': [], 'PrinterScanner': [], 'Xerox': []}
            json.dump(list_equipment_default, WLw, indent=4)


class OrgEquipment:
    def __init__(self, model, firm=None, cost=None):
        self.firm = firm
        self.cost = cost
        self.model = model
        self._list_of_params = {'firm': firm, 'cost': cost, 'model': model}

    @classmethod
    def add_to_warehouse(cls, *args):
        try:
            list_words = re.findall('[A-Z][^A-Z]*', cls.__name__)
            if len(list_words) > 1:
                first_letter = ''
                for el in range(len(list_words)):
                    first_letter += list_words[el][0]
            else:
                first_letter = cls.__name__.upper()[:2]
            if args[0]["model"].upper().split('_')[0][:2] == first_letter:
                pass
            else:
                raise TypeOrgEquipmentError(cls.__name__, args[0]["model"])
        except TypeOrgEquipmentError:
            return
        try:
            count = int(input(f'How many {cls.__name__} {args[0]["firm"]} {args[0]["model"]} to add: '))
        except ValueError as VE:
            print('Not a number was entered')
            return
        with open("WarehouseList.json", 'w', encoding='utf-8') as WLw:
            if Warehouse.list_equipment[cls.__name__]:
                for i in range(len(Warehouse.list_equipment[cls.__name__])):
                    if Warehouse.list_equipment[cls.__name__][i]["model"].upper() == args[0]["model"].upper():
                        Warehouse.list_equipment[cls.__name__][i]['count'] += count
                        json.dump(Warehouse.list_equipment, WLw, indent=4)
                        return
            Warehouse.list_equipment[cls.__name__].append({})
            for el in args:
                Warehouse.list_equipment[cls.__name__][-1] = {par: value for par, value in el.items()}
            Warehouse.list_equipment[cls.__name__][-1]['count'] = count
            json.dump(Warehouse.list_equipment, WLw, indent=4)

    @classmethod
    def del_from_warehouse(cls, *args):
        try:
            count = int(input(f'How many {cls.__name__} {args[0]["model"]} to delete: '))
        except ValueError as VE:
            print('Not a number was entered')
            return
        with open('Warehouse/WarehouseList.json', 'w', encoding='utf-8') as WLw:
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

    def add_printer(self):
        Printer.add_to_warehouse(self._list_of_params)

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
            number_of_version = self.model[2]
            if number_of_version.isdigit() and 1 <= int(number_of_version) <= 3:
                self.version_scanner = int(number_of_version)

    def add_scanner(self):
        Scanner.add_to_warehouse(self._list_of_params)

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

    def add_printer_scanner(self):
        PrinterScanner.add_to_warehouse(self._list_of_params)

    def del_printer_scanner(self):
        PrinterScanner.del_from_warehouse(self._list_of_params)


class Xerox(OrgEquipment):
    def add_xerox(self):
        Xerox.add_to_warehouse(self._list_of_params)

    def del_xerox(self):
        Xerox.del_from_warehouse(self._list_of_params)

import csv
from ..home import Home
from .section import Section


class City:
    def __init__(self, model, seed, community) -> None:
        self.model = model
        self.no_houses = 0
        self.house_id = 1 # used for house unique IDs
        self.class_names =  community['class_names']

        self.class_houses = {}
        self.neighborhoods = {} # neighborhood_name : lst of streets
        self.street_lookup = {} # street_key : neighborhood_name
        self.streets = {} # street_name : {section_key : section}
        self.sections = {}
        self.class_sections = {}

        if seed['generate']:
            self.init_town(seed['number_of_houses'], community['class_distribution'])
            self.init_neighborhoods(seed['no_neighborhoods'], seed['streets_per_neighborhood'],
                                    seed['sections_per_neighborhood'], seed['houses_per_section'])
        else:
            self.import_town(seed['neighborhood_file'], seed['sections_street_file'])

    """
    INIT FUNCTIONS
    """
    def init_town(self, households, class_distr):
        """
        Initialize more or less the specified amount of houses (rounding error)
        with the correct class distribution.
        """
        for c, class_perc in enumerate(class_distr):
            self.class_houses[c] = {}
            no_class_houses = round(class_perc * households)
            for house in range(no_class_houses):
                id = house + self.no_houses
                key = f"h{id}"
                self.class_houses[c][key] = Home(key, id, self.model, (c, self.class_names[c]))
            self.no_houses += no_class_houses
        # it's possible these don't align neatly

    def init_neighborhoods(self, no_neighs, no_neighstreets, no_streetsections, 
                           houses_per_section):
        quan_class_distr = [len(self.class_houses[n]) for n in range(no_neighs)]
        class_per_neigh = [[0 for _ in range(len(self.class_houses))] for _ in range(no_neighs)]
        print(quan_class_distr)
        print(class_per_neigh)

        # Descending order
        for neigh in range(no_neighs -1, -1, -1):
            print(neigh)

    def import_town(self, neigh_file, street_file):
        self.neighborhoods = {}
        self.street_lookup = {}
        with open(neigh_file, 'r') as bfile:
            csvreader = csv.reader(bfile)
            for row in csvreader:
                self.street_lookup[row[1]] = row[0]
                if row[0] not in self.neighborhoods:
                    self.neighborhoods[row[0]] = []
                self.neighborhoods[row[0]].append(row[1])

        with open(street_file, 'r') as cfile:
            csvreader = csv.reader(cfile)
            for row in csvreader:
                self.init_street(row[0], row)

    def init_street(self, street_name, row):
        if row == [] or not row or row == '':
            print(f'Could not init street {street_name}')
            return
        self.streets[street_name] = {}

        # INPUT FILE STRUCTURE: 
        # cols = ['street', 'A', 'class', 'B', 'class',
        #         'C', 'class', 'D', 'class', 'E', 'class']
        # This loops over the provided row and inits sections and the houses 
        # within
        for i in range(1, 11, 2):
            if row[i] == '' or i >= len(row):
                break
            no_section_houses = int(row[i])
            in_class = int(row[i+1]) - 1 # -1 because input file has classes starting with 1
            section_key = f's{i}.c{in_class}'
            this_section =  Section(section_key, no_section_houses, in_class, 
                                    street_name)
            for _ in range(no_section_houses):
                house_key = f'h{self.house_id}'
                self.house_id += 1
                house = Home(house_key, self.house_id, self.model, 
                             (in_class, self.class_names[in_class]), this_section)
                this_section.add_house(house)

            self.streets[street_name][section_key] = this_section
            self.class_sections[in_class] = this_section
    
    """
    CITY MANAGEMENT
    """
    def find_empty_house(self, income_class : int):
        """
        Find house in income class
        """
        for sec in self.class_sections[income_class]:
            if sec.has_space():
                house_key = sec.get_empty_house()
                if house_key:
                    return house_key
                else:
                    print("Got wrong house_key")
        return False


"""
Though written in python for ease and & type control, this can 
easily be converted to another config format like .ini or .yaml. 
These dictionaries are never referenced directly in the code and
are fed to the model through generation.py. 
"""


simulation = {
    'number_of_years' : 100,
    'simulation_output' : False,
    'json_output' : True,
    'tests' : False
}

seed = {
    'city_mode' : 'vars', # ['vars', 'files']
    'percentage_inhabited_houses' : 0.75,
    'generate' : False,

    # generate city
    'number_of_houses' : 750, 
    'streets_per_neighborhood' : 5, 
    'sections_per_neighborhood' : 5,
    'houses_per_section': 5, 
    'input_streets' : 'input/city/streetnames.txt', 
    'input_neighborhoods' : 'input/city/neighborhoods.txt',
    'input_male_names' : 'input/names/male.names', 
    'input_female_names' : 'input/names/female.names', 
    'input_surnames' : 'input/names/genericsur.names',

    # pre-crafted city
    'sections_street_file' : 'input/preset_city/SectionStreets.csv',
    'neighborhood_file' : 'input/preset_city/Buurten.csv'
}

health_stats = {
    'bio_male_female_ratio' : 0.499, # percentage of men
    'average_health' : 0.7, # on a scale from 0-1
    'health_care_modifier' : 0.0, # increased chance for cure 
    'child_mortality' : 0.1, # yearly chance of child dying from childhood-specific illnesses (0 cancels out all childhood mortality)
    'old_age' : 50, # when is a person considered to be old in this community?

    'physical_disability_chance' : 0.1,
    'physical_disabilities' : ['blind', 'deaf', 'mute', 'missing limb', 'decreased mobility', 'cognitive'], # from birth, an accident or old age
    'physical_disabilities_distribution' : [0.2, 0.1, 0.2, 0.2, 0.2, 0.1], # given that a disability occurs, chance of each
    'physical_disabilities_health_impact' : [(False, True, False, 0), (True, False, False, -0.2), 
                                             (True, False, False, -0.2), (False, True, False, -0.2), 
                                             (False, True, False, -0.3), (True, False, True, -0.3)], 
                                             # (communication, mobility, cognitive, health_modifier)

}

aesthetic_seed = {
    'skin_color_distribution' : [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], # from dark to light
    'hair_colors' : ['black', 'dark brown', 'brown', 'red', 'blonde', 'strawberry blonde'],
    'dark_skin_hair_color_distribution' : [0.7, 0.25, 0.035, 0.005, 0.005, 0.005],
    'light_skin_hair_color_distribution' : [0.05, 0.1, 0.3, 0.05, 0.3, 0.2],
    'hair_type_seed' : ['C', 'S'], # the curly / straight hair gene seed (lenght inconsequential)
    'eye_colors' : ['blue', 'green', 'brown'], # ['brown', 'green', 'blue'],
    'dark_skin_eye_color_distribution' : [0.1, 0.2, 0.7],
    'light_skin_eye_color_distribution' : [0.5, 0.2, 0.3],
}

society = {
    'marriage' : True,
    'same_sex_marriage' : False,
    'divorce' : False,
    'marriage_age_women' : 16,
    'marriage_age_men' : 20,
    'male_meant_for_independence' :  True,
    'female_meant_for_independence' : False,
    'name_system' : 'medieval', # ['medieval', 'male-centric', 'equal']
}

community = {
    'classes' : 5,
    'class_names' : ['working class', 'lower middle class', 'middle class', 'upper middle class', 'nobility'],
    'class_distribution' : [0.45, 0.3, 0.15, 0.08, 0.02],
    'class_person_household_percentage' : [0.25, 0.15, 0.1, 0.05, 0.025], # what percentage of 1 income is needed to sustain 1 person?
    'class_mobility' : [(0.9, 0.08, 0.02, 0, 0), (), (), (), ()],
    # class distribution will only be taken into account if not specified in input

    'factions' : 3,
    'faction_names' : ['Zealots', 'Dogmatists', 'No religion'],
    'faction_distribution' : [0.35, 0.3, 0.35],
    'faction_mobility' : [(0.95, 0.01, 0.04), (0.02, 0.9, 0.8), (0.15, 0.12, 0.73)],
    # faction distribution will only be taken into account if not specified in input
}


institutions = {
    'orphanage' : True,
    'orphanage_label' : 'House of Children',
    'orphanages' : 3,
    'orphanages_names' : ['Meertens', 'Afilan', 'Luisan'],
    'orphanages_capacity' : [70, 20, 50],
    # if not specified, there will be 1 orphanage with unlimited spots
    'orphanages_factions' : {
        'Meertens': 'Zealots',
        'Afilan' : 'Dogmatists', 
        'Luisan' : 'No religion'
    }, 
    # if empty, no factions will be associated with the orphanages

    'monastery' : True,
    'monastery_label' : 'House of Worship',
    'monasteries' : 2,
    # if not specified, there will be 1 monastery with unlimited spots
    'monasteries_names' : ['Zeal', 'Dogma'],
    'monasteries_capacity' : [100, 75],
    'monasteries_factions' : {
        'Zeal' : 'Zealots',
        'Dogma' : 'Dogmatists'
    , } 
    # if empty, no factions will be associated with the monasteries
}


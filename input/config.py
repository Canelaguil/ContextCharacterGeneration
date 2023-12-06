simulation = {
    'number_of_years' : 100,
    'simulation_output' : True,
    'json_output' : True,
}

population_seed = {
    'number_of_houses' : 750, # number of houses is only taken into account if not specified in input files
    'percentage_inhabited_houses' : 0.75,
    'bio_male_female_ratio' : 0.49 # percentage of men
}

health_stats = {
    'average_health' : 0.7, # on a scale from 0-1
    'health_care_modifier' : 0.0, # increased chance for cure 
    'child_mortality' : 0.2, # yearly chance of child dying from childhood-specific illnesses (0 cancels out all childhood mortality)
    'old_age' : 40, # when is a person considered to be old in this community?

    'physical_disability_chance' : 0.1,
    'physical_disabilities' : ['blind', 'deaf', 'mute', 'missing limb', 'decreased mobility'], # from birth, an accident or old age
    'physical_disabilities_distribution' : [0.2, 0.2, 0.2, 0.2, 0.2], # given that a disability occurs, chance of each
    'physical_disabilities_health_impact' : [(False, True, 0), (True, False, -0.2), (True, False, -0.2), 
                                             (False, True, -0.2), (False, True, -0.3)], # (communication, mobility, health_modifier)

}

aesthetic_seed = {
    'skin_color_distribution' : [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], # from dark to light
    'hair_colors' : ['black', 'dark brown', 'brown', 'red', 'blonde', 'strawberry blonde'],
    'dark_skin_hair_color_distribution' : [0.7, 0.25, 0.035, 0.005, 0.005, 0.005],
    'light_skin_hair_color_distribution' : [0.05, 0.1, 0.3, 0.05, 0.3, 0.2],
    'eye_colors' : ['brown', 'green', 'blue'],
    'dark_skin_eye_color_distribution' : [0.7, 0.2, 0.1],
    'light_skin_eye_color_distribution' : [0.3, 0.2, 0.5],
}

community = {
    'marriage' : True,
    'divorce' : False,
    'marriage_age_women' : 16,
    'marriage_age_men' : 20,
    'male_meant_for_indepence' :  True,
    'female_meant_for_independece' : False,

    'classes' : 5,
    'class_names' : ['working class', 'lower middle class', 'middle class', 'upper middle class', 'nobility'],
    'class_distribution' : [0.5, 0.3, 0.15, 0.1, 0.05],
    # class distribution will only be taken into account if not specified in input

    'factions' : 3,
    'faction_names' : ['Zealots', 'Dogmatists', 'No religion'],
    'faction_distribution' : [0.35, 0.3, 0.35],
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


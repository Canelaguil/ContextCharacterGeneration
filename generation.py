from input.config import *
import math
from classes import Community

def read_names(male_file, female_file, surname_file): 
    """
    Reads the different name files and saves them as lists.
    """
    men_file = open(male_file, "r")
    women_file = open(female_file, "r")
    sur_file = open(surname_file, "r")

    m_names, w_names, s_names = [], [], []

    for mn in men_file:
        mn = mn.replace("\n", "")
        mn = mn.replace("\r", "")
        m_names.append(mn.strip())

    for wn in women_file:
        wn = wn.replace("\n", "")
        wn = wn.replace("\r", "")
        w_names.append(wn.strip())

    for sn in sur_file:
        sn = sn.replace("\n", "")
        sn = sn.replace("\r", "")
        s_names.append(sn.strip())

    return [m_names, w_names, s_names]


def check_config(): 
    """
    Checks the integrity of the provided input.
    """
    error = True

    # population 
    if simulation['number_of_years'] > 1000: 
        print(f"Warning: {simulation['number_of_years']} years is costly and does not necessarily improve much over, say, 100 years")
    if seed['number_of_houses'] > 5000:
        print(f"Warning: {simulation['number_of_houses']} houses is costly and generates a huge amount of characters")
    if not 0 <= seed['percentage_inhabited_houses'] <= 1:
        print(f"{seed['percentage_inhabited_houses']} is not a valid percentage")
        error = False
    
    # health stats
    if len(health_stats['physical_disabilities']) != len(health_stats['physical_disabilities_distribution']) != 'physical_disabilities_health_impact':
        print('Mismatch of lists in healt_stats.physical_disabilities')
        error = False
    for tup in health_stats['physical_disabilities_health_impact']:
        if len(tup) != 3:
            print('Incorrectly formatted tuple in physical_disabilities_health_impact')
            error = False
        
    # aesthetic seed
    if len(aesthetic_seed['hair_colors']) != len(aesthetic_seed['dark_skin_hair_color_distribution']) != len(aesthetic_seed['light_skin_hair_color_distribution']):
        print('Mismatch of hair color lists.')
        error = False
    if len(aesthetic_seed['eye_colors']) != len(aesthetic_seed['dark_skin_eye_color_distribution']) != len(aesthetic_seed['light_skin_eye_color_distribution']):
        print('Mismatch of eye color lists.')
        error = False
    
    # community
    if community['classes'] != len(community['class_names']) != len(community['class_distribution']):
        print('Mismatch in income class variables.')
        error = False
        
    try: 
        assert math.isclose(sum(community['class_distribution']), 1, abs_tol=0.0001)
        assert math.isclose(sum(community['faction_distribution']), 1, abs_tol=0.0001)
    except:
        print("Community distributions do not add up to 1")
        print(f"Class distr: {sum(community['class_distribution'])}")
        print(f"Faction distr: {sum(community['faction_distribution'])}")
        error = False
    if community['factions'] != len(community['faction_names']) != len(community['faction_distribution']):
        print('Mismatch in faction variables.')
        error = False

    # institutions
    if institutions['orphanage']:
        if not institutions['orphanages']:
            institutions['orphanages'] = 1
            institutions['orphanages_capacity'] = [1000]
        
        if institutions['orphanages_factions']:
            for faction in institutions['orphanages_factions'].values():
                if not faction in community['faction_names']:
                    print(f'Misspelled faction in orphanage (institutions): {faction}')
                    error = False

    if institutions['monastery']:
        if not institutions['orphanages']:
            institutions['monasteries'] = 1
            institutions['monasteries_capacity'] = [1000]

        if institutions['monasteries_factions']:
            for faction in institutions['monasteries_factions'].values():
                if not faction in community['faction_names']:
                    print(f'Misspelled faction in monastery (institutions): {faction}')
                    error = False
    
    return error


if __name__ == '__main__':
    if not check_config():
        print('There is a issue with the config formatting. Please check and try again.')
    else:
        names = read_names(seed['input_male_names'], seed['input_female_names'], seed['input_surnames'])
        community = Community(society, seed, health_stats,
                              aesthetic_seed, community, institutions, names)
        community.run(simulation['number_of_years'], simulation['simulation_output'])
        if simulation['json_output']: 
            community.json_output()
        
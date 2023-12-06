from input.config import *
from classes.community import *

def check_config(): 
    """
    Checks the integrity of the provided input.
    """
    error = True

    # population 
    if simulation['number_of_years'] > 1000: 
        print(f"Warning: {simulation['number_of_years']} years is costly and does not necessarily improve much over, say, 100 years")
    if population_seed['number_of_houses'] > 5000:
        print(f"Warning: {simulation['number_of_houses']} houses is costly and generates a huge amount of characters")
    if not 0 <= population_seed['percentage_inhabited_houses'] <= 1:
        print(f"{population_seed['percentage_inhabited_houses']} is not a valid percentage")
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
        pass
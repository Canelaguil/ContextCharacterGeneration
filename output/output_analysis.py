import json
import matplotlib.pyplot as plt
import argparse
import random
import numpy as np
import sys, os

experiment = 'AAADefault_'
def plot(x, y, title, xlabel='', ylabel=''):
    if isinstance(y[0], tuple):
        # print(y)
        for subY in y:
            plt.plot(x, subY[0], label=subY[1])
        plt.legend()
    else:
        plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.xticks(x)
    plt.savefig(f'output/analysis/plots/{experiment}{title}.png')
    plt.close()

def plot_scatter(x, y, title, xlabel='', ylabel='', all_xticks=False):
    if isinstance(y[0], tuple):
        for subY in y:
            plt.scatter(x, subY[0], label=subY[1])
        plt.legend()
    else:
        plt.scatter(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if all_xticks:
        plt.xticks(x)
    plt.savefig(f'output/analysis/plots/{experiment}{title}.png')
    plt.close()

def plot_bar(ys, title, xs = None, xlabel='', ylabel=''):
    if not xs:
        xs = [i for i in range(len(ys))]
    plt.bar(xs, ys)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.xticks(xs)
    plt.savefig(f'output/analysis/plots/{experiment}{title}.png')
    plt.close()
    
def plot3d(x, y, z, title, xlabel='', ylabel='', zlabel=''):
    ax = plt.figure().add_subplot(projection='3d')
    ax.scatter(x, y, z)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.title(title)
    plt.savefig(f'output/analysis/plots/{experiment}{title}.png')
    plt.close()

def relationship_analysis():
    directory = 'output/relationships_json/'
    dfs, cmp = [], [] # relationship compatiblitity / progression
    no_children = [0] * 16
    for f in os.listdir(directory):
        path = f"{directory}{f}"
        with open(path) as json_data:
            r = json.load(json_data)
        key = f[0:-5]
        r = r[key]
        difference = r['friendship trajectory']['current'] - r['friendship trajectory']['start']
        compatiblity = r['compatibility']
        if r['label'] in ['spouse', 'partner'] and r['duration'][0] != 1200 and (r['duration'][1] - r['duration'][0]) > 5:
            try:
                no_children[r['no birth children']] += 1
            except:
                print(f"Too many children: {r['no birth children']}")
        dfs.append(difference)
        cmp.append(compatiblity)
    plot_scatter(cmp, dfs, 'Relationship trajectory with compatiblity', 
                 'compatibility score', 'difference during relationship')
    plot_bar(no_children, 'Frequency of number of children per relationship with heterosexual sex', xlabel='Number of children', ylabel='Frequency')

def output_people():
    directory = 'output/people_json/'
    ages = [0] * 100
    age_to_die = [0] * 100
    for f in os.listdir(directory):
        path = f"{directory}{f}"
        with open(path) as json_data:
            p = json.load(json_data)
        key = f[0:-5]
        p = p[key]
        if p['alive']:
            try:
                ages[p['age']] += 1
            except:
                print(f"Living person too old: {p['age']}, key {p['key']}")
        else:
            try:
                age_to_die[p['age']] += 1
            except:
                print(f"Dead person too old: {p['age']}, key {p['key']}")
    
    plot_bar(ages, 'People per age', None, 'ages', 'number of people')
    plot_bar(age_to_die, 'People to die per age', None, 'ages', 'number of people')

def overall_stats():
    path = 'output/stats.json'
    with open(path) as json_data:
        s = json.load(json_data)
    x = [i for i in range(len(s['male births']))]
    ys = [(s[key], key) for key in s.keys()]
    ys.remove((s['male births'], 'male births'))
    ys.remove((s['female births'], 'female births'))
    # for i, l in ys:
    #     print(len(i))
    #     print(l)
    plot(x, ys, 'Demographics', 'years', 'number of people')

"""
DISTANC ANALYSIS
"""
def get_vector_distance(element1, element2):
    """
    Returns vector distance between two sets of vector attributes. 
    Normalized for range (0, 0, 0) -> (1, 1, 1)
    """
    # convert input to vectors
    if isinstance(element1, dict):
        e1 = np.array(list(element1.values()))
    else:
        e1 = np.array(element1)
    if isinstance(element2, dict):
        e2 = np.array(list(element2.values()))
    else:
        e2 = np.array(element2)

    distance = np.linalg.norm(e2 - e1)
    max_distance = 1.732 # distance between (0, 0, 0) and (1, 1, 1)
    return round(distance / max_distance, 3)

def get_personality_vector_from_person(per):
    a = list(per['personality'].values()) + [per['age']]
    # print(a)
    return a

def get_bornlikethis_vector_from_person(per):
    a = list(per['born this way'].values())
    a = a[1:4]
    return a

def similarity_analysis():
    directory = 'output/people_json/'
    people = []
    # people_vector = []
    matches = []
    output = []
    no_people = 10
    for i in range(no_people):
        output.append([])
        # select random person older than 15 NOT first gen
        while True:
            f = random.choice(os.listdir(directory))
            path = f"{directory}{f}"
            with open(path) as json_data:
                p = json.load(json_data)
            if p[f[0:-5]]['network']['parents'] != 'firstgen' and p[f[0:-5]]['age'] > 15:
                person =  p[f[0:-5]]
                # print(person)
                people.append(f[0:-5]) # save key
                break
        # create vector of personality and age
        person_vector = get_personality_vector_from_person(person)
        person_kin = get_bornlikethis_vector_from_person(person)
        # loop over all people finding best matches
        all_distances = []
        option_counter = 0
        for f in os.listdir(directory):
            path = f"{directory}{f}"
            with open(path) as json_data:
                p = json.load(json_data)[f[0:-5]]
            if p['network']['parents'] != 'firstgen' and p['age'] > 15:
                my_vector = get_personality_vector_from_person(p)
                this = (get_vector_distance(person_vector, my_vector), f[0:-5])
                all_distances.append(this)
                option_counter += 1
            else:
                break
        print(option_counter)
        all_distances.sort()
        best_matches = all_distances[0:6]
        matches.append(best_matches)

        # for each best match, determine number of life events and network size
        for ii, (s, k) in enumerate(best_matches):
            path = f"{directory}{k}.json"
            with open(path) as json_data:
                p = json.load(json_data)[k]

            match_info = {
                # f'key-{ii}' : k,
                f'age-{ii}' : p['age'],
                f'distance-{ii}' : s,
                f'kinsey distance-{ii}' : 0,
                f'network size-{ii}' : 0,
                f'life events-{ii}' : 0,
            }
            
            # life events
            for memkey in p['memory']:
                for y in p['memory'][memkey]:
                    acontecimientos = p['memory'][memkey][y]
                    if isinstance(acontecimientos, dict):
                        match_info[f'life events-{ii}'] += 1
                    else:
                        match_info[f'life events-{ii}'] += len(acontecimientos)
            # network size
            for rkey in p['network']['relationship keys']:
                netx = p['network']['relationship keys'][rkey]
                if isinstance(netx, dict):
                    match_info[f'network size-{ii}'] += len(netx['birth'])
                else: 
                    match_info[f'network size-{ii}'] += len(netx)

            # kinsey distance
            thiskin = get_bornlikethis_vector_from_person(p)
            match_info[f'kinsey distance-{ii}'] = get_vector_distance(person_kin, thiskin)
            # print(match_info)
            output[i].append(match_info)
            # print(output)
    # CSV output (thank you chatgpt)
    import csv
    csv_file_path = 'output/analysis/csv/difference_matches.csv'

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # Write the header
        writer.writeheader()

        # Write the data
        for inner_list in output:
            thisrow = {}
            for it in inner_list:
                thisrow = {
                    ** thisrow, 
                    ** it
                }
            writer.writerow(thisrow)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create analysis graphs for files created by generation.py.')
    parser.add_argument('experiment_name', type=str, nargs='?', 
                        help='name for experiment')
    arg = parser.parse_args().experiment_name

    if arg != None:
        experiment = arg + '_'

    directory = 'output/people_json/'
    counter = 0
    for f in os.listdir(directory):
        path = f"{directory}{f}"
        with open(path) as json_data:
            p = json.load(json_data)[f[0:-5]]
        if p['network']['parents'] != 'firstgen' and p['age'] > 15:
            counter += 1
    print(counter)
    # similarity_analysis()
    # relationship_analysis()
    # overall_stats()
    # output_people()
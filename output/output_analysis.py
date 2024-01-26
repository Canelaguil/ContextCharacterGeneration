import json
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
import argparse
import random
import numpy as np
import sys, os

experiment = 'AAADefault_'
def plot(x, y, title, xlabel='', ylabel='', stretch=False):
    if isinstance(y[0], tuple):
        # print(y)
        for subY in y:
            plt.plot(x, subY[0], label=subY[1])
        plt.legend()
    else:
        plt.plot(x, y)

    if stretch:
        fig = plt.gcf()
        fig.set_size_inches(9, 4)    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.xticks(x)
    plt.savefig(f'output/analysis/plots/{experiment}{title}.png')
    plt.close()

def plot_scatter(x, y, title, xlabel='', ylabel='', all_xticks=False, stretch=False):
    if isinstance(y[0], tuple):
        for subY in y:
            plt.scatter(x, subY[0], label=subY[1],  s=0.3, linewidth=0)
        plt.legend()
    else:
        plt.scatter(x, y, s=0.3, linewidth=0)
        
    if stretch:
        fig = plt.gcf()
        fig.set_size_inches(9, 4)   
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if all_xticks:
        plt.xticks(x)
    plt.savefig(f'output/analysis/plots/{experiment}{title}.png')
    plt.close()

def scatterspecial(xy1, xy2, title, xlabel='', ylabel='', stretch=True):
    x1, y1 = zip(*xy1)
    x2, y2 = zip(*xy2)
    plt.scatter(x1, y1, s=6, linewidth=0, label='closest')
    plt.scatter(x2, y2, s=6, linewidth=0, label='furthest')
    plt.legend()
    if stretch:
        fig = plt.gcf()
        fig.set_size_inches(9, 4)   
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # if all_xticks:
    #     plt.xticks(x)
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
                 'compatibility score', 'difference during relationship', True)
    plot_bar(no_children, 'Frequency of number of children per relationship with heterosexual sex', xlabel='Number of children', ylabel='Frequency')

def get_network_and_event_size(p):
    life_events = 0
    network_size = 0
    for memkey in p['memory']:
        for y in p['memory'][memkey]:
            acontecimientos = p['memory'][memkey][y]
            if isinstance(acontecimientos, dict):
                life_events += 1
            else:
                life_events += len(acontecimientos)
    # network size
    for rkey in p['network']['relationship keys']:
        netx = p['network']['relationship keys'][rkey]
        if isinstance(netx, dict):
            network_size  += len(netx['birth'])
        else: 
            network_size  += len(netx)
    return life_events, network_size

def output_people():
    directory = 'output/people_json/'
    ages = [0] * 100
    age_to_die = [0] * 100
    network_freq = [0] * 75
    event_freq = [0] * 300
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

        if p['age'] > 15 and not p['network']['parents'] != 'firstgen':
            no_events, no_connects = get_network_and_event_size(p)
            event_freq[no_events] += 1
            network_freq[no_connects] += 1
    # print(no_events, no_connects)
    plot_bar(event_freq[0:201], 'Number of life events per person', None, 'number of events', 'frequency')
    plot_bar(network_freq[0:50], 'Number of network connections per person', None, 'number of connections', 'frequency')
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
    ys.remove((s['living people'], 'living people'))
    plot(x, ys, 'Demographics', 'years', 'number of people', True)

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
    # max_distance = 1.732 # distance between (0, 0, 0) and (1, 1, 1)
    return round(distance, 3)

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
    output_closest = []
    output_furthest = []
    exemplar_results = []
    no_exemplars = 10 
    ftypes = ['age', 'distance', 'kinsey distance', 'network size', 'life events']
    field_names = [f"{ft}-{fi}" for ft in ftypes for fi in range(6)]
    exemplarletters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for exemplar in range(no_exemplars):
        # select random person older than 15 NOT first gen
        while True:
            f3 = random.choice(os.listdir(directory))
            path = f"{directory}{f3}"
            with open(path) as json_data:
                p5 = json.load(json_data)[f3[0:-5]]
            if p5['network']['parents'] != 'firstgen' and p5['age'] > 15:
                person =  p5
                # print(person)
                people.append(f3[0:-5]) # save key
                break
        # create vector of personality and age
        person_vector = get_personality_vector_from_person(person)
        person_kin = get_bornlikethis_vector_from_person(person)

        # loop over all people finding best matches
        all_distances = []
        for f2 in os.listdir(directory):
            path = f"{directory}{f2}"
            with open(path) as json_data:
                p2 = json.load(json_data)[f2[0:-5]]
            if p2['network']['parents'] != 'firstgen' and p2['age'] > 15:
                my_vector = get_personality_vector_from_person(p2)
                this = (get_vector_distance(person_vector, my_vector), f2[0:-5])
                all_distances.append(this)
            else:
                continue
        all_distances.sort()
        best_matches = all_distances[0:6]
        worst_matches = [all_distances[0]] + all_distances[-5:]
        matches.append(best_matches)

        this_row = {}
        print('BEST')
        # for each best match, determine number of life events and network size
        for ii, (s, k) in enumerate(best_matches):
            print(k)
            path = f"{directory}{k}.json"
            with open(path) as json_data:
                p = json.load(json_data)[k]
                   
            this_row[f'age-{ii}'] = p['age']
            this_row[f'distance-{ii}'] = s

            le, ns = get_network_and_event_size(p)     
            this_row[f'life events-{ii}'] = le
            this_row[f'network size-{ii}'] = ns
            
            thiskin = get_bornlikethis_vector_from_person(p)
            this_row[f'kinsey distance-{ii}'] = get_vector_distance(person_kin, thiskin)
            
            with open(f"output/analysis/closest_exemplars/{k}.closest_e{exemplarletters[exemplar]}.m{ii}.json", 'w') as exemplar_results:
                json.dump(p, exemplar_results, indent=2, separators=(',', ': '))
        output_closest.append(this_row)
        this_row2 = {}
        print('WORST')
        # for each worst match, determine number of life events and network size
        for ii, (s2, k2) in enumerate(worst_matches):
            path = f"{directory}{k2}.json"
            print(k2)
            with open(path) as json_data:
                p8 = json.load(json_data)[k2]
                   
            this_row2[f'age-{ii}'] = p8['age']
            this_row2[f'distance-{ii}'] = s2

            le, ns = get_network_and_event_size(p8)     
            this_row2[f'life events-{ii}'] = le
            this_row2[f'network size-{ii}'] = ns
            
            thiskin = get_bornlikethis_vector_from_person(p8)
            this_row2[f'kinsey distance-{ii}'] = get_vector_distance(person_kin, thiskin)

            
            with open(f"output/analysis/furthest_exemplars/{k2}.furthest_e{exemplarletters[exemplar]}.m{ii}.json", 'w') as exemplar_results:
                json.dump(p8, exemplar_results, indent=2, separators=(',', ': '))
        output_furthest.append(this_row2)

    # CSV output (thank you chatgpt)
    import csv
    csv_file_path = 'output/analysis/csv/closest_matches.csv'

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # Write the header
        writer.writeheader()

        # Write the data
        for thisrow in output_closest:
            writer.writerow(thisrow)

    csv_file_path = 'output/analysis/csv/furthest_matches.csv'

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # Write the header
        writer.writeheader()

        # Write the data
        for thisrow in output_furthest:
            writer.writerow(thisrow)

def links_analysis():
    import math
    no_links = [0] * 2000
    directory1 = 'output/analysis/thesis_results/closest_exemplars/'
    directory2 = 'output/analysis/thesis_results/furthest_exemplars/'
    directory3 = 'output/people_json/'
    close_points = []
    all_points = []
    furthest_points = []
    closest_results = []
    keys = [] # furthest has a lot of doubles, so to counteract
    for f in os.listdir(directory1):
        total_links = 0
        total_events = 0
        path = f"{directory1}{f}"
        with open(path) as json_data:
            per = json.load(json_data)

        memkey = 'events' # only count events
        for y in per['memory'][memkey]:
            acontecimientos = per['memory'][memkey][y]
            if isinstance(acontecimientos, dict):
                total_events += 1
            else:
                no_events = len(acontecimientos)
                total_events += no_events
                if no_events > 1:
                    total_links += math.comb(no_events, 2)
        descripte_title = f.split('.')
        keys.append(descripte_title[0])

        # process results
        no_links[total_links] += 1
        close_points.append((total_events, total_links))

        thisrow = {
            'key' : descripte_title[0],
            'events' : total_events,
            'links' : total_links,
            'type' : descripte_title[1].split('_')[0],
            'em' : f"{descripte_title[1].split('_')[1][1]}{descripte_title[2][1]}",
            'exemplar' : descripte_title[1].split('_')[1][1],
            'match' : descripte_title[2][1]
        }
        closest_results.append(thisrow)

    furthest_results = []
    for f in os.listdir(directory2):
        total_links = 0
        total_events = 0
        path = f"{directory2}{f}"
        with open(path) as json_data:
            per = json.load(json_data)

        memkey = 'events' # only count events
        for y in per['memory'][memkey]:
            acontecimientos = per['memory'][memkey][y]
            if isinstance(acontecimientos, dict):
                total_events += 1
            else:
                no_events = len(acontecimientos)
                total_events += no_events
                if no_events > 1:
                    total_links += math.comb(no_events, 2)
        descripte_title = f.split('.')
        if descripte_title[0] in keys:
            continue
        keys.append(descripte_title[0])

        no_links[total_links] += 1
        furthest_points.append((total_events, total_links))

        thisrow = {
            'key' : descripte_title[0],
            'events' : total_events,
            'links' : total_links,
            'type' : descripte_title[1].split('_')[0],
            'em' : f"{descripte_title[1].split('_')[1][1]}{descripte_title[2][1]}",
            'exemplar' : descripte_title[1].split('_')[1][1],
            'match' : descripte_title[2][1]
        }
        furthest_results.append(thisrow)

    for f in os.listdir(directory3):
        total_links = 0
        total_events = 0
        path = f"{directory3}{f}"
        with open(path) as json_data:
            per = json.load(json_data)
            per = per[list(per.keys())[0]]
        if per['age'] > 15 and per['network']['parents'] != 'firstgen':
            memkey = 'events' # only count events
            for y in per['memory'][memkey]:
                acontecimientos = per['memory'][memkey][y]
                if isinstance(acontecimientos, dict):
                    total_events += 1
                else:
                    no_events = len(acontecimientos)
                    total_events += no_events
                    if no_events > 1:
                        total_links += math.comb(no_events, 2)
            descripte_title = f.split('.')
            keys.append(descripte_title[0])

            # process results
            # no_links[total_links] += 1
            all_points.append((total_events, total_links))
    import numpy as np
    mx, my = zip(*all_points)
    print(len(mx))
    print(f"events mean: {np.mean(mx)}")
    print(f"events min: {np.min(mx)}, events max: {np.max(mx)}")
    print(f"links mean: {np.mean(my)}")
    print(f"links min: {np.min(my)}, links max: {np.max(my)}")
    # print(len(all_points))
    plot_scatter(mx, my, 'All relations between events and links', 'number of events', 'number of links', stretch=True)

    import csv
    field_names = list(thisrow.keys())

    csv_file_path1 = 'output/analysis/csv/closest_links.csv'
    with open(csv_file_path1, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        # Write the header
        writer.writeheader()
        # Write the data
        for thisrow in closest_results:
            writer.writerow(thisrow)

    csv_file_path2 = 'output/analysis/csv/furthest_links.csv'
    with open(csv_file_path2, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        # Write the header
        writer.writeheader()
        # Write the data
        for thisrow in furthest_results:
            writer.writerow(thisrow)

    scatterspecial(close_points, furthest_points, 'Relation between number of events and number of links', 'number of events', 'number of links')
    # plot_bar(no_links, 'Number of links - closest', None, 'number of links', 'frequency')
                    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create analysis graphs for files created by generation.py.')
    parser.add_argument('experiment_name', type=str, nargs='?', 
                        help='name for experiment')
    arg = parser.parse_args().experiment_name

    if arg != None:
        experiment = arg + '_'

    directory = 'output/people_json/'
    # counter = 0
    # for f in os.listdir(directory):
    #     path = f"{directory}{f}"
    #     with open(path) as json_data:
    #         p = json.load(json_data)[f[0:-5]]
    #     if p['network']['parents'] != 'firstgen' and p['age'] > 15:
    #         counter += 1
    # print(f"Number of people older than 15 and not first-gen: {counter}")
    # similarity_analysis()

    links_analysis()
    # relationship_analysis()
    # overall_stats()
    # output_people()
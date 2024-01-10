import json
import os
import shutil

def get_person(p_key):
    directory = 'output/people_json/'
    f = f"{p_key}.json"
    path = f"{directory}{f}"
    with open(path) as json_data:
        p = json.load(json_data)
    return p[f"{p_key}"]

def get_name(p_key):
    p = get_person(p_key)
    return p['full name']

def get_other_from_relationship(my_key, r_key, output=False):
    my_key = int(my_key) # important !
    directory = 'output/relationships_json/'
    f = f"{r_key}.json"
    path = f"{directory}{f}"
    with open(path) as json_data:
        r = json.load(json_data)
    r = r[f"{r_key}"]
    if output:
        print('---------')
        print(r['people'])
        print(my_key)
        p2 = r['people'][0] if r['people'][1] == my_key else r['people'][1]
        print(p2)
    else:
        p2 = r['people'][0] if r['people'][1] == my_key else r['people'][1]
    return get_person(p2)

def formatted(info, key=None):
    if key:
        return f'{key.upper()}: {info}\n'
    else:
        return f'{info}\n'
    
def title(txt):
    return f"\n{txt.upper()}\n---"
    
def write_to_file(place, info, key=None):
    place.write(formatted(info, key))

if __name__ == '__main__':
    directory = 'output/people_json/'
    target_directory = 'output/people_description/'
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
    os.mkdir(target_directory)
    count = 0
    for f in os.listdir(directory):
        key = f[0:-5]
        p = get_person(key)
        target = f"{target_directory}{key}.txt"
        with open(target, 'a') as d:
            # headline
            write_to_file(d, title(f"{p['full name']} ({p['sex']})"))
            if p['network']['parents'] != 'firstgen':
                write_to_file(d, f"Born in {p['birth year']} to {p['network']['parents']['mother']} and {p['network']['parents']['father']}.")
            else:
                write_to_file(d, f"Born in {p['birth year']} as a part of the first generation.")
            if 'greatgrandchild' in p['network']:
                print(p['key'])
            write_to_file(d, f"Is currently {'' if p['relationship status']['married'] else 'not '}married, has had {len(p['relationship status']['relationships'])} romantic relationship(s).\n")

            # basics
            write_to_file(d, f"{p['age']} ({'alive' if p['alive'] else 'dead'})", 'Age')
            for relation_type in p['network']['relationship keys']:
                ppl = ''
                
                if relation_type == 'child':
                    for c in p['network']['relationship keys']['child']['birth']:
                        other = get_other_from_relationship(key, c)
                        ppl += f"{other['full name']} ({other['key']}), "
                        label_name = 'children'
                elif relation_type == 'grandchild':
                    for c in p['network']['relationship keys']['grandchild']['birth']:
                        other = get_other_from_relationship(key, c)
                        ppl += f"{other['full name']} ({other['key']}), "
                        label_name = 'grandchildren'
                else:
                    for relation_keys in p['network']['relationship keys'][relation_type]:
                        other = get_other_from_relationship(key, relation_keys)
                        ppl += f"{other['full name']} ({other['key']}), "
                        label_name = relation_type + 's'
                write_to_file(d, ppl, label_name)
            if p['home']:
                write_to_file(d, f"{p['home']['street']} in the {p['home']['neighborhood']} neighborhood", 'address')
            else:
                write_to_file(d, f"no home", 'address')
            write_to_file(d, p['key'], 'key')

            # personality
            write_to_file(d, title('personality scales'))
            for t, v in p['personality'].items():
                write_to_file(d, v, t)

            # physical description
            write_to_file(d, title('physical description'))
            for k, t in p['genetics'].items():
                if k == 'hair_type':
                    if t == ['S', 'S']:                        
                        t = 'straight'
                    elif t == ['C', 'C']:
                        t = 'curly'
                    else:
                        t = 'wavy'
                if k not in ['communication_impaired', 'mobility_impaired', 'cognitive_impaired', 'hair_color_code']:
                    write_to_file(d, t, k)

            # occupation
            write_to_file(d, title('occupation'))
            write_to_file(d, p['occupation']['income class'][1], 'income class')
            if p['occupation']['has job']:
                write_to_file(d, f"Has job, latest income {p['occupation']['income']}")

            # relationship info
            write_to_file(d, title('relationship data'))
            for i, ii in p['born this way'].items():
                if i not in ['sexuality', 'sex']:
                    write_to_file(d, ii, i)

            # events
            write_to_file(d, title('events'))
            prev_year_neglected = False
            recorded = False
            for y, events in p['memory']['events'].items():
                # if the only event is being neglected and we're not gonna print that...
                if any(e2['topic'] == 'neglected' for e2 in events) and prev_year_neglected == True and len(events) == 1:
                    break
                write_to_file(d, f"-~{y}~-")
                for e in events:
                    topic = e['topic']
                    if topic == 'new home':
                        write_to_file(d, f"Moved to {e['home']['street']} in {e['home']['neighborhood']}.")
                    elif topic == 'person died':
                        if 'cause' in e and e['cause'] != '':
                            cause = f" of {e['cause']}"
                        else:
                            cause = ''
                            print(key)
                        write_to_file(d, f"{e['label'].title()} died{cause}: {e['person']['name']}")
                    elif topic == 'new relationship':
                        other = e['people names'][0] if p['key'] == e['people'][1] else e['people names'][1]
                        label = e['label'] if e['label'] != 'parentchild' else 'child'
                        if label in ['grandparentchild', 'greatgrandparentchild']:
                            if (int(y) - int(p['birth year'])) > 25:
                                label = 'grandchild' if label == 'grandparentchild' else 'greatgrandchild'
                            else:
                                break # don't print grandparent relations
                        write_to_file(d, f"New {label}: {other}")
                    elif topic == 'unmarried':
                        write_to_file(d, f"No longer married.")
                    elif topic == 'single':
                        write_to_file(d, f"No longer in a relationship.")
                    elif topic == 'feelings change':
                        write_to_file(d, f"Feelings change about {e['target name']}: now {e['state']}.")
                    elif topic == 'not enough income':
                        write_to_file(d, "Not enough income in household.")
                    elif topic == 'job notice':
                        write_to_file(d, f"Income change: {e['notice']}, with income {e['income']}.")
                    elif topic == 'neglected':
                        if not prev_year_neglected:
                            write_to_file(d, "Neglected while needing care.")
                    elif topic == 'now caretaker':
                        ppl = ''
                        for i in e['care dependants']:
                            other = get_person(i)
                            ppl += f"{other['full name']}"
                        write_to_file(d, f"Now caretaker of: {ppl}")
                    elif topic == 'new caretaker':
                        other = get_person(e['person'])
                        write_to_file(d, f"New caretaker in household: {other['full name']}.")
                    elif topic == 'not caretaker':
                        write_to_file(d, "No longer caretaker in household.")
                    elif topic == 'event':
                        write_to_file(d, f"{e['event'].title()} of {e['year']}")
                    elif topic == 'death':
                        recorded = True
                        write_to_file(d, f"Died of {e['cause']}.")
                    elif topic == 'update':
                        if e['update'] == 'parent married':
                            write_to_file(d, f"Parent {get_name(e['parent'])} remarried to {get_name(e['new partner'])}.")
                        elif e['update'] == 'new friendship label':
                            # print(e)
                            other = get_other_from_relationship(key, e['relationship'])
                            write_to_file(d, f"Now {e['friendship label']} relationship with {e['relationship label']} {other['full name']}.")
                    else:
                        print(e)

                    if any(e2['topic'] == 'neglected' for e2 in events):
                        prev_year_neglected = True
                    else:
                        prev_year_neglected = False

                # if not any(e2['topic'] == 'death' for e2 in events) and not p['alive']:
                #     death = False
            
            # if p['alive'] == False and recorded == False:
            #     print(p['key'])
            #     count += 1
    print(count)


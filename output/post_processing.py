import json
import os
import shutil

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
    for f in os.listdir(directory):
        path = f"{directory}{f}"
        with open(path) as json_data:
            p = json.load(json_data)
        key = f[0:-5]
        p = p[key]
        target = f"{target_directory}{key}.txt"
        with open(target, 'a') as d:
            write_to_file(d, title(f"{p['full name']} ({p['sex']})"))
            if p['network']['parents'] != 'firstgen':
                write_to_file(d, f"Born in {p['birth year']} to {p['network']['parents']['mother']} and {p['network']['parents']['father']}.")
            else:
                write_to_file(d, f"Born in {p['birth year']} as a part of the first generation.")
            write_to_file(d, f"Is currently {'' if p['relationship status']['married'] else 'not '}married, has had {len(p['relationship status']['relationships'])} romantic relationship(s).\n")

            write_to_file(d, f"{p['age']} ({'alive' if p['alive'] else 'dead'})", 'Age')

            if p['network']['siblings'] == []:
                write_to_file(d, "Has no siblings.")
            else:
                write_to_file(d, f"{len(p['network']['siblings'])}", 'siblings')


            if p['network']['children']['birth'] == {}:
                write_to_file(d, "Has no children.")
            else:
                write_to_file(d, f"{len(p['network']['children']['birth'])}", 'children')
            if p['home']:
                write_to_file(d, f"{p['home']['street']} in the {p['home']['neighborhood']} neighborhood", 'address')
            else:
                write_to_file(d, f"no home", 'address')

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

            # events
            write_to_file(d, title('events'))



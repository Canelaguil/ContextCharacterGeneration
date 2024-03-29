from classes.utils import *
import sys, os
import random
import json

if __name__ == '__main__':
    directory = 'output/people_json/'
    print("Welcome! Use this tool to quickly parse biographies.")
    print("Enter 'd' at any time to switch between descriptive and json mode for people.")
    print("Enter 'r' at any time to get a random (living) person from the selected directory.")
    print("Enter 's' to switch between the people and relationship json directories.")
    print("Enter 'e' at any time to leave.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    while True:
        inp = input("Enter a person's identification key: ")
        print("-------------------------------------------------------------")
        inp = inp.strip()
        if inp == 'd':
            if directory == 'output/people_description/':
                directory = 'output/people_json/'
            else:
                directory = 'output/people_description/'
            print(f'Directory switched to {directory}')
        elif inp == 'e':
            sys.exit()
        elif inp == 's':
            if directory == 'output/relationships_json/':
                directory = 'output/people_json/'
            else:
                directory = 'output/relationships_json/'
            print(f'Directory switched to {directory}')
        elif inp == 'r':
            f = random.choice(os.listdir(directory))
            path = f"{directory}{f}"

            # get a random, living adult person
            if 'json' in directory:
                while True:
                    with open(path) as json_data:
                        p = json.load(json_data)
                    if p[f[0:-5]]['alive'] and p[f[0:-5]]['age'] > 16:
                        beautify_print(p)
                        break
                    f = random.choice(os.listdir(directory))
                    path = f"{directory}{f}"
            else:
                path = f"{directory}{f}"
                with open(path, 'r') as des:
                    for l in des:
                        print(l.strip())
        else:
            try: 
                if ' ' in inp:
                    f, key = inp.split(' ')
                else:
                    f = inp
                    key = False
                if 'json' in directory:
                    path = f"{directory}{f}.json"
                    with open(path) as json_data:
                        p = json.load(json_data)

                    if key:
                        print(f)
                        beautify_print(p[f][key])
                    else:
                        beautify_print(p[f])
                else:
                    path = f"{directory}{f}.txt"
                    with open(path, 'r') as des:
                        for l in des:
                            print(l.strip())
                
            except:
                print("Did not recognize that key. Try again.")
        print("-------------------------------------------------------------")

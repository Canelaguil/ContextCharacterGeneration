from classes.utils import *
import sys, os
import random
import json

if __name__ == '__main__':
    directory = 'output/people_json/'
    print("Welcome! Use this tool to quickly parse biographies.")
    print("Enter 'd' at any time to switch to the descriptive mode.")
    print("Enter 'r' at any time to get a random person.")
    print("Enter 'e' at any time to leave.")
    while True:
        inp = input("Enter a person's identification key: ")
        print("-------------------------------------------------------------")
        inp = inp.strip()
        if inp == 'd':
            directory = 'output/people_description/'
            print(f'Directory switched to {directory}')
        elif inp == 'e':
            sys.exit()
        elif inp == 'r':
            f = random.choice(os.listdir(directory))
            path = f"{directory}{f}"
            with open(path) as json_data:
                p = json.load(json_data)
            beautify_print(p)
        else:
            try: 
                if ' ' in inp:
                    f, key = inp.split(' ')
                else:
                    f = inp
                    key = False

                path = f"{directory}{f}.json"
                with open(path) as json_data:
                    p = json.load(json_data)

                if key:
                    print(f)
                    beautify_print(p[f][key])
                else:
                    beautify_print(p[f])
                print("-------------------------------------------------------------")
            except:
                print("Did not recognize that key. Try again.")

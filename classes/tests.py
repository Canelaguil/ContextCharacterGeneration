from typing import Any
import pathlib
import numpy as np
from mesa import Agent, Model
from mesa.time import StagedActivation
from .city_classes import City, Institutions
from .community_classes import Factions, CommunityEvents
from .person_classes import Naming, Body
from .person import Person
from .relationship import Relationship
import matplotlib.pyplot as plt

def plot(x, y, title, xlabel='', ylabel=''):
    if isinstance(y[0], tuple):
        for subY in y:
            plt.plot(x, subY[0], label=subY[1])
        plt.legend()
    else:
        plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(x)
    plt.savefig(f'output/tests/plots/{title}.png')

def body_tests(no=500):
    # skin color tests
    skin8 = [0 for _ in range(Body.no_skins)]
    skin6 = [0 for _ in range(Body.no_skins)]
    skin4 = [0 for _ in range(Body.no_skins)]
    skin2 = [0 for _ in range(Body.no_skins)]
    skin0 = [0 for _ in range(Body.no_skins)]
    skins = [sk for sk in Body.skins]
    
    for _ in range(no):
        body8 = Body({'skin_color' : 9, 
                      'hair_type' : ['C', 'C'], 'hair_color_code' : 5, 
                      'eye_color' : 'brown', 'health' : 0.75}, 
                    {'skin_color' : 1, 
                     'hair_type' : ['S', 'S'], 'hair_color_code' : 3, 
                      'eye_color' : 'blue', 'health' : 0.8})
        body6 = Body({'skin_color' : 8, 
                      'hair_type' : ['C', 'S'], 'hair_color_code' : 5, 
                      'eye_color' : 'brown', 'health' : 0.2}, 
                    {'skin_color' : 2, 
                     'hair_type' : ['C', 'S'], 'hair_color_code' : 3, 
                     'eye_color' : 'green', 'health' : 0.75})
        body4 = Body({'skin_color' : 8, 
                      'hair_type' : ['C', 'S'], 'hair_color_code' : 5, 
                      'eye_color' : 'green', 'health' : 0.3}, 
                    {'skin_color' : 4, 
                     'hair_type' : ['S', 'S'], 'hair_color_code' : 3, 
                      'eye_color' : 'blue', 'health' : 0.6})
        body2 = Body({'skin_color' : 6, 
                      'hair_type' : ['C', 'C'], 'hair_color_code' : 5, 
                      'eye_color' : 'blue', 'health' : 0.2}, 
                    {'skin_color' : 4, 
                     'hair_type' : ['C', 'S'], 'hair_color_code' : 3, 
                      'eye_color' : 'blue', 'health' : 0.9})
        body0 = Body({'skin_color' : 4, 
                      'hair_type' : ['C', 'C'], 'hair_color_code' : 5, 
                      'eye_color' : 'blue', 'health' : 0.7}, 
                    {'skin_color' : 4, 
                     'hair_type' : ['C', 'C'], 'hair_color_code' : 5, 
                      'eye_color' : 'blue', 'health' : 0.7})

        skin8[body8.pass_gens()['skin_color']] += 1
        skin6[body6.pass_gens()['skin_color']] += 1
        skin4[body4.pass_gens()['skin_color']] += 1
        skin2[body2.pass_gens()['skin_color']] += 1
        skin0[body0.pass_gens()['skin_color']] += 1

    ys = [(skin2, 'parents skins: 6 & 4'), (skin4, 'parent skins: 8 & 4'), 
          (skin6, 'parents skins: 8 & 2'), (skin8, 'parents skins: 9 & 1'),
          (skin0, 'parents skins: 4 & 4')]
    plot(skins, ys, f"Skin color distribution: {no} bodies each", xlabel='skin color (int)')

    # hair type tests
    # shairccss = [0 for _ in range(Body.no_hairs)]
    # shaircscs = [0 for _ in range(Body.no_hairs)]
    # shaircsss = [0 for _ in range(Body.no_hairs)]
    # shaircccs = [0 for _ in range(Body.no_hairs)]

    # hair color tests
    # shairccss = [0 for _ in range(Body.no_hairs)]
    # shaircscs = [0 for _ in range(Body.no_hairs)]
    # shaircsss = [0 for _ in range(Body.no_hairs)]
    # shaircccs = [0 for _ in range(Body.no_hairs)]
    # shairccss[body8.pass_gens()['skin_color']] += 1
    # shaircscs[body6.pass_gens()['skin_color']] += 1
    # shaircsss[body4.pass_gens()['skin_color']] += 1
    # shaircccs[body2.pass_gens()['skin_color']] += 1

    # shairccss[body8.pass_gens()['skin_color']] 
    # shaircscs = [0 for _ in range(Body.no_hairs)]
    # shaircsss = [0 for _ in range(Body.no_hairs)]
    # shaircccs = [0 for _ in range(Body.no_hairs)]

def naming_tests(model):
    # pathlib.Path.unlink('output/tests/files/100names.txt')
    f = open('output/tests/files/100names.txt', 'a')
    for _ in range(100):
        test = Person(3, model)
        print(test.names.full(), file=f)
    f.close()

def base_test(model):
    test = Person(3, model)
    body2 = Body({'skin_color' : 6, 
                      'hair_type' : ['C', 'C'], 'hair_color_code' : 5, 
                      'eye_color' : 'blue', 'health' : 0.2}, 
                    {'skin_color' : 4, 
                     'hair_type' : ['C', 'S'], 'hair_color_code' : 3, 
                      'eye_color' : 'blue', 'health' : 0.9})
    print(body2.pass_gens())

def run_tests(model):
    # person tests
    base_test(model)
    body_tests()
    naming_tests(model)

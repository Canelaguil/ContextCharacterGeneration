import json
import matplotlib.pyplot as plt
import sys, os

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
    plt.savefig(f'output/analysis/plots/{title}.png')

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
    plt.savefig(f'output/analysis/plots/{title}.png')

def plot_bar(ys, title, xs = None, xlabel='', ylabel=''):
    if not xs:
        xs = [i for i in range(len(ys))]
    plt.bar(xs, ys)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(xs)
    plt.savefig(f'output/analysis/plots/{title}.png')
    

def plot3d(x, y, z, title, xlabel='', ylabel='', zlabel=''):
    ax = plt.figure().add_subplot(projection='3d')
    ax.scatter(x, y, z)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.title(title)
    plt.savefig(f'output/analysis/plots/{title}.png')

def relationship_analysis():
    directory = 'output/relationships_json/'
    dfs, cmp = [], [] # relationship compatiblitity / progression
    no_children = [0] * 15
    for f in os.listdir(directory):
        path = f"{directory}{f}"
        with open(path) as json_data:
            r = json.load(json_data)
        key = f[0:-5]
        r = r[key]
        difference = r['friendship trajectory']['current'] - r['friendship trajectory']['start']
        compatiblity = r['compatibility']
        try:
            no_children[r['no birth children']] += 1
        except:
            print(r['no birth children'])
        dfs.append(difference)
        cmp.append(compatiblity)
    plot_scatter(cmp, dfs, 'Relationship trajectory with compatiblity', 
                 'compatibility score', 'difference during relationship')
    plot_bar(no_children, 'Frequency of number of children per relationship with heterosexual sex', xlabel='Number of children', ylabel='Frequency')
        

if __name__ == '__main__':
    relationship_analysis()
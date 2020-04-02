import sys
import glob
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
mpl.rcParams['figure.figsize'] = (12,6)
import seaborn as sns
sns.set(font_scale=1.5, context="paper", style="white", font="serif")
pal = sns.color_palette()
cols = pal.as_hex()

def main():

#    systems = ['cosma7', 'oracle_cloud']
    systems = ['cosma7', 'diac', 'amd7452', 'cl6252', 'oracle cloud']
    sysdetails = {}

    tempd = {}
    tempd['dir'] = '../results/MI'
    tempd['dir'] = '../EAGLE_25_strong_scaling/results/cosma7/multi_node'
    tempd['cpn'] = 28
    tempd['label'] = 'COSMA7 (2x Intel Skylake 5120, 2.2GHz, 14c)'
    tempd['col'] = cols[0]
    sysdetails['cosma7'] = tempd.copy()
    tempd = {}
    tempd['dir'] = '../EAGLE_25_strong_scaling/results/csd3/replicate_2'
    tempd['cpn'] = 32
    tempd['label'] = 'Peta-4 Skylake (2x Intel Skylake 6142, 2.6GHz, 16c)'
    tempd['col'] = cols[3]
    sysdetails['diac'] = tempd.copy()

    nodes = {}
    perf = {}
    for system in systems:
        tempd = sysdetails[system]
        file_list = glob.glob(tempd['dir'] + "/timesteps_*")

        protodf = []

        for file in file_list:
            rundict = parse_file(file, tempd['cpn'])
            protodf.append(rundict)

        df = pd.DataFrame(protodf)

        print()
        print(tempd['label'])
        nodes[system], perf[system] = get_perf_stats(df, 'max', writestats=True)
    
    for system in systems:
        tempd = sysdetails[system]
        plt.plot(nodes[system], perf[system], marker='+', color=tempd['col'], label=tempd['label'], alpha=0.6)
    plt.xlabel('Nodes')
    plt.ylabel('Performance (updates/s)')
    plt.xlim([0,17])
    plt.legend(loc='best')
    sns.despine()
    plt.savefig('swift_perf.png', dpi=300)

def parse_file(infile, cpn):

    rundetails = {}
    rundetails['File'] = infile

    # Read the file header
    f = open(infile, "r")
    for line in f:
        if "Branch:" in line:
            s = line.split()
            branch = " ".join(s[2:])
            rundetails['Branch'] = branch.replace("_", "\\_")
        elif "Revision:" in line:
            s = line.split()
            rundetails['Revision'] = s[2]
        elif "Hydrodynamic scheme:" in line:
            line = line[2:-1]
            s = line.split()
            scheme = " ".join(s[2:])
            rundetails['Hydro Scheme'] = line
        elif "Hydrodynamic kernel:" in line:
            line = line[2:-1]
            s = line.split()
            kernel = " ".join(s[2:5])
            rundetails['Hydro Kernel'] = kernel
        elif "neighbours:" in line:
            s = line.split()
            rundetails['Neighbours'] = s[4]
        elif "Eta:" in line:
            s = line.split()
            rundetails['Eta'] = float(s[2])
        elif "threads:" in line:
            s = line.split()
            rundetails['Threads'] = int(s[4])
        elif "ranks:" in line:
            s = line.split()
            rundetails['Ranks'] = int(s[5])
    f.close()
    rundetails['Cores'] = int(rundetails['Ranks'] * rundetails['Threads'])
    if rundetails['Cores'] < cpn:
        rundetails['Nodes'] = 1
    else:
        rundetails['Nodes'] = int(rundetails['Cores'] / cpn)
    rundetails['Count'] = 1

    # Loop over all files for a given series and load the times
    times = np.loadtxt(infile, usecols=(11,))
    updates = np.loadtxt(infile, usecols=(7,))
    totalUpdates = np.sum(updates)
    totalTime = np.sum(times)
    perf = totalUpdates / totalTime

    rundetails['Runtime'] = totalTime
    rundetails['Updates'] = totalUpdates
    rundetails['Perf'] = perf

    return rundetails

def get_perf_stats(df, stat, threads=None, writestats=False):
    if threads is not None:
       query = '(Threads == {0})'.format(threads)
       df = df.query(query)
    df_num = df.drop(['File', 'Branch', 'Revision', 'Hydro Scheme', 'Hydro Kernel', 'Neighbours', 'Eta'], 1)
    groupf = {'Perf':['min','median','max','mean'], 'Count':'sum'}
    df_group = df_num.sort_values(by='Nodes').groupby(['Nodes','Cores']).agg(groupf)
    if writestats:
        print(df_group)
    # Reduce to nodes only so we get performance per node
    df_group = df_num.sort_values(by='Nodes').groupby(['Nodes']).agg(groupf)
    perf = df_group['Perf',stat].tolist()
    nodes = df_group.index.get_level_values(0).tolist()
    return nodes, perf

main()

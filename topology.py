import networkx as nx
import pandas as pd
import time
import matplotlib.pyplot as plt
import json
#https://towardsdatascience.com/visualizing-networks-in-python-d70f4cbeb259
#https://www.python-course.eu/networkx.php

def display_topo(filepath, output_1 = "path_graph1.png", output_2 = "path_graph2.png"):
    '''
    Args:
    
    param: filepath to render topology
    '''
    df=pd.read_csv(filepath)
    df['vertex2'] = df['vertex2'].apply(lambda x:json.loads(x)["screen_name"])
    df['vertex1'] = df['vertex1'].apply(lambda x:json.loads(x)["screen_name"])
    df=df[df["mentioned"]>1]
    G=nx.from_pandas_edgelist(df,source="vertex1",target="vertex2",edge_attr="mentioned")
    nx.draw_networkx(G,with_labels=True)
    time.sleep(3)
    plt.savefig(output_1)
    plt.show()
    nx.draw_circular(G,with_labels=True)
    plt.savefig(output_2)
    plt.show()

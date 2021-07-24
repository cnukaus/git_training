import pandas as pd
import numpy as np
from itertools import groupby
import ast
import json
from collections import Counter
import twint
import operator
import list_graph
from langdetect import detect




def get_tweets(file_output):
    c = twint.Config()
    c.Search = ["#IPFS", "#PresidentialHackathon"]
    # c.Store_json = True
    c.Store_csv = True
    c.Output = file_output
    # Date parameters
    c.Since = "2021-06-11"
    c.until = "2021-07-13"

    # Number of tweets to pull
    c.Limit = 5000

    # Run
    twint.run.Search(c)

def tweet_from_user(username):
    pass


def most_replied(df, col_name="reply_to"):
    """
    which user is most refered to in reply

    Args:

    Returns:
        dataframe
    """
    df = df.loc[df[col_name].notna()]
    list_replies = [row[col_name][1:-1] for index, row in df.iterrows()] #[1:-1] removes the surrounding square bracket, just need dicts of each replied
    new_list = []
    i,j,k=0,0,0
    for str_or_tuple in list_replies:
        str_or_tuple = ast.literal_eval(str_or_tuple)
        if isinstance(str_or_tuple, tuple):
            new_list += [x for x in list(str_or_tuple)]
            i +=1
        elif isinstance(str_or_tuple, dict):
            new_list.append(str_or_tuple)
            j +=1
        else:
            k+=1
    if k>1:
        print('count of multiple mention in tweet {}, single {}, exception{}'.format(i,j,k))
    return new_list

def run_most_replied():
    contents = most_replied(df)
    contents_str = [json.dumps(x) for x in contents]
    counted = Counter(contents_str)
    rev = {k: v for k, v in counted.items()}
    #print(sorted(rev.items(), key=operator.itemgetter(1), reverse=True))

def build_graph(df,twitter_graph, col_name_list=["reply_to","user_id","username","name"]):
    """
    build the graph

    [row[col_name_list]][0][0] is the content, not series column name, [0][1] shows first value of user_id
    convert dict type vertext to string, because dict can't be hashable key. for list_graph storage - v in self.graph fails
    Args:

    Returns:
        dataframe
    """
    
    df = df.loc[df[col_name_list[0]].notna()]
    for index, row in df.iterrows():
        vertex={}
        vertex['id']=[row[col_name_list]][0][1]
        vertex['screen_name']=[row[col_name_list]][0][2]
        vertex['name']=[row[col_name_list]][0][3]
        str_vertex=json.dumps(vertex)

        twitter_graph.add_vertex(str_vertex)
        reply=[row[col_name_list]][0][0]
        reply = ast.literal_eval(reply)
        for vertex_2 in [x for x in list(reply)]:
            str_vertex_2=json.dumps(vertex_2)
            twitter_graph.add_vertex(str_vertex_2)
            twitter_graph.add_edge(str_vertex,str_vertex_2,1,verbose=True)
   return twitter_graph

def parse_contents(contents):
    '''
    to use groupby to manipulate, WIP
    '''
    # nlargest(3, rev, key=lambda item: item["count"])


    # contents.sort(key=lambda content: content["screen_name"])

    # then use groupby with the same key
    groups = groupby(contents, lambda content: content["screen_name"])
    for screen_name, group in groups:
        # print(group)
        for content in group:
            # print("\t", content)
            content["screen_name"] + "_id:" + content["id"]
            print(content["screen_name"] + "_id:" + content["id"])


def count_interactions_of_user():
    return (replies, retweets,likes)

def highest_talked(twitter_graph):
    '''
    works for list_graph
    '''
    list_vertex2=[]
    for vertex in twitter_graph.graph:

        for edges in twitter_graph.graph[vertex]:
                list_vertex2.append([vertex,edges[0], edges[1]])

    df = pd.DataFrame(list_vertex2,columns=['vertex1','vertex2','mentioned'])
    df.to_csv("network_topo.csv",index=False)
    df['user_id']=df['vertex2'].apply(lambda x:int(json.loads(x)["id"]))
    df['username']=df['vertex2'].apply(lambda x:json.loads(x)["screen_name"])
    df['name']=df['vertex2'].apply(lambda x:json.loads(x)["name"])
    df_agg=df.groupby(['user_id','username','name'])['mentioned'].sum().to_frame()
    df_agg['mention_by_#ppl']=df.groupby(['user_id','username','name'])['vertex1'].nunique()
    return df_agg


def detect_languages(passage):
    return detect(passage)

def sum_to_account(df,key_col=['user_id','username','name'],value_col=['replies_count','retweets_count','likes_count','hashtags','cashtags'],value_2_col='lan',key_2_name='language_count'):
    df_summary = df.groupby(key_col)[value_col].sum()
    df_summary[key_2_name]=df.groupby(key_col)[value_2_col].nunique()
    return df_summary

def count_word_freq(df,column_name='tweet'):

    # to combine each ppl's words, then get group by freq
    stop = stopwords.words('english')
    newStopWords = ['hello','hi','hey','im','get']
    stop.extend(newStopWords)
    df[column_name] = df[column_name].str.replace("[^\w\s]", "").str.lower()
    df[column_name] = df[column_name].apply(lambda x: ' '.join([item for item in x.split() if item not in stop]))
    df[column_name].str.split(expand=True).stack().value_counts()


if __name__ == '__main__':

    get_tweets("test_6.csv")
    content_file_name = "test_6.csv"
    df = pd.read_csv(content_file_name)
    df[df.isin(["[]"])] = np.nan
    df['lan']=df['tweet'].apply(lambda x:detect_languages(x))
    i=0
    for index,rows in df.iterrows():
        if not rows["lan"]==rows['language']:
            i += 1

    df_summary = sum_to_account(df)
    df_summary = df_summary.reset_index(level=['username','name'])

    
    graph_result=list_graph.graph()
    build_graph(df,graph_result)
    df_graph = highest_talked(graph_result)


    df_summary = pd.merge(df_summary,df_graph,how='left',on=['user_id'])
    df_summary.to_csv('final_summary.csv')







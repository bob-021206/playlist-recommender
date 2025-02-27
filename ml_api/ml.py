import pandas as pd
from fpgrowth_py import fpgrowth
import json
import os
dataset_path = os.getenv("DATASET_PATH", "/project2-pv2/datasets/spotify/2023_spotify_ds1.csv")

# 读取数据集
df = pd.read_csv(dataset_path)

#print(df.columns)
#print(df.head())

baskets = df.groupby("pid")["track_name"].apply(list).tolist()

min_support = 0.05  
min_confidence = 0.5  

freq_itemsets, rules = fpgrowth(baskets, minSupRatio=min_support, minConf=min_confidence)

rules_json = [{"antecedent": list(rule[0]), "consequent": list(rule[1]), "confidence": rule[2]} for rule in rules]
output_path = "/project2-pv2/rules/play_rules.json"
with open(output_path, "w") as f:
    json.dump(rules_json, f, indent=4)
#docker run --rm -v /home/datasets:/home/datasets -v /home/binyan/project2-pv2:/home/binyan/project2-pv2 ml_api
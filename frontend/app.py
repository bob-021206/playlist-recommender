from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)

# 设置 JSON 规则文件路径
RULES_PATH = "/project2-pv2/rules/play_rules.json"
def load_rules():
    """ 加载 JSON 规则文件 """
    if os.path.exists(RULES_PATH):
        with open(RULES_PATH, "r") as f:
            rules = json.load(f)
        return rules
    return []


# 解析规则为字典结构，方便查询
def build_rule_dict(rules):
    """
    解析 JSON 规则，转换为：
    {
        "Night's On Fire": [("Crash And Burn", 0.7606)],
        "Lose My Mind": [("Crash And Burn", 0.8226)]
    }
    """
    rule_dict = {}
    
    for rule in rules:
        antecedent = rule["antecedent"][0]  # 取列表中的第一个歌曲名称
        consequent = rule["consequent"]     # 直接取列表
        confidence = rule["confidence"]     # 置信度

        if antecedent not in rule_dict:
            rule_dict[antecedent] = []
        rule_dict[antecedent].append((consequent, confidence))

    # 按置信度排序推荐
    for key in rule_dict:
        rule_dict[key] = sorted(rule_dict[key], key=lambda x: x[1], reverse=True)

    return rule_dict

rules = load_rules()

# 解析规则为字典结构，方便查询
rule_dict = build_rule_dict(rules)

# 记录模型最后修改时间
model_date = datetime.fromtimestamp(os.path.getmtime(RULES_PATH)).strftime('%Y-%m-%d')

@app.route("/")
def index():
    return render_template("index.html")  # 渲染前端页面

@app.route("/api/recommender", methods=["POST"])
def recommend():
    """ 处理推荐请求 """
    data = request.get_json()
    
    # 检查请求是否包含 "songs" 字段
    if "songs" not in data:
        return jsonify({"error": "Missing 'songs' field"}), 400
    
    input_songs = set(data["songs"])
    recommended_songs = set()

    # 遍历用户输入的歌曲，在规则字典中查找
    for song in input_songs:
        if song in rule_dict:
            for consequent, confidence in rule_dict[song]:
                print(type(consequent))
                recommended_songs.add(tuple(consequent))

    return jsonify({
        "songs": list(recommended_songs),
        "version": "1.0",
        "model_date": model_date
    })

if __name__ == "__main__":
    app.run(host= '0.0.0.0',  port=52005)
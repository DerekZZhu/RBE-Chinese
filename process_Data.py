import os
import json
import random
from tqdm import tqdm

FOLDER = "SWSR"
RULES_NAME = "chinese_rules.json"
EXEMPLARS_PER_RULE = 1

HATESPEECH_LABELS = {"hatespeech", "offensive"}
TRAIN_NAME = "train.json"
RESULT_NAME = "rule_to_exemplar.json"
NORMAL_LABEL = "normal"
TRAIN_FILE = os.path.join(FOLDER, TRAIN_NAME)
RULE_FILE = os.path.join(FOLDER, RULES_NAME)
RESULT_FILE = os.path.join(FOLDER,RESULT_NAME)

with open(TRAIN_FILE, encoding="utf-8") as f:
    train_data = json.load(f)

sentence_to_label = {}

labels = set()

for datapoint in train_data:
    sentence = datapoint[0]
    label = datapoint[1]
    sentence_to_label[sentence.lower()] = label
    labels.add(label)

with open(RULE_FILE, encoding="utf-8") as f:
    rules = json.load(f)

print(len(rules))
print(len(sentence_to_label))

ctr = 0
rule_to_exemplars = {}
for rule in tqdm(rules):
    rule = rule.lower()
    exemplars = []

    for sentence in sentence_to_label:
        if rule in sentence and sentence_to_label[sentence] in HATESPEECH_LABELS:
            exemplars.append(sentence)
    
    if len(exemplars) == 0:
        # no exemplars
        continue

    exemplars_sampled = random.sample(exemplars,EXEMPLARS_PER_RULE)
    rule_to_exemplars[rule] = exemplars_sampled

print(len(rule_to_exemplars))

with open(RESULT_FILE, "w+", encoding="utf-8") as f:
    json.dump(rule_to_exemplars,f, ensure_ascii=False)

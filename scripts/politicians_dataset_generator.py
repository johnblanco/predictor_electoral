import pandas as pd
import json
import random

q_count = 20

with open("../predictor_pol/json_data/candidatos.json") as f:
    CANDIDATOS = []
    file_parties = json.load(f)
    for party in file_parties:
    	CANDIDATOS.append({"party": party["party"].title(), "candidates": []})
    	for candidate in party["candidates"]:
        	rand_answers = [];
        	for i in range(20):
        		rand_answers.append(random.randint(1,7))
        	row = {"id" : candidate["id"], "name" : candidate["name"], "answers" : rand_answers}
        	CANDIDATOS[-1]["candidates"].append(row)

with open("../predictor_pol/json_data/random_politicians_dataset.json", "w") as outf:
	json.dump(CANDIDATOS, outf, indent=4)

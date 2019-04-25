import random
import json
import os

question_count = 20

with open("../predictor_pol/json_data/candidatos.json") as f:
	dataset_string = "candidate_id;candidate_name;"
	for i in range(1, question_count + 1):
		dataset_string += "question_" + str(i) + ";"
	dataset_string += "\n"
	file_parties = json.load(f)
	for party in file_parties:
		for candidate in party["candidates"]:
			dataset_string += str(candidate["id"]) + ";" + candidate["name"] + ";"
			for i in range(question_count):
				answer = str(random.randint(1, 7))
				dataset_string += answer + ";"
			dataset_string += "\n"

with open("../csvs/random_politicians_dataset.csv", "w+", encoding='utf-8') as outf:
	outf.write(dataset_string)
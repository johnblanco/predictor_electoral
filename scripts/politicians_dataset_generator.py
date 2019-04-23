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

#q_count = 20

#with open("../predictor_pol/json_data/candidatos.json") as f:
 #   CANDIDATOS = []
  #  file_parties = json.load(f)
   # for party in file_parties:
    #	CANDIDATOS.append({"party": party["party"].title(), "candidates": []})
    #	for candidate in party["candidates"]:
     #   	rand_answers = [];
      #  	for i in range(20):
       # 		rand_answers.append(random.randint(1,7))
        #	row = {"id" : candidate["id"], "name" : candidate["name"], "answers" : rand_answers}
        #	CANDIDATOS[-1]["candidates"].append(row)

#with open("../predictor_pol/json_data/random_politicians_dataset.json", "w") as outf:
#	json.dump(CANDIDATOS, outf, indent=4)
#}
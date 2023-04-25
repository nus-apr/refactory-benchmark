import os

questions = [x for x in os.listdir() if not os.path.isfile(x) and "question" in x]

file = open("meta-data.candidate.json", "w")
file.write("[")
id = 0
for question in questions:
    for bug_id in [
        x for x in os.listdir(question) if "wrong_" in x
    ]:
        id = id + 1
        name = bug_id.split("_")[-1].split('.')[0]
        data = """
        {{
            "id":{id},
            "subject":"{lab}",
            "bug_id":"{problem_id}",
            "source_file": "{bug_id}",
            "reference_file": "{correct_file}",
            "extra_files": ['global.py'],
            "line_numbers": [],
            "failing_test": "1",
            "passing_test": "",
            "count_neg": "1",
            "count_pos": "0",
            "binary_path": "",
            "crash_input": "",
            "exploit_file_list": [{inputs}],
            "test_timeout": 5,
            "bug_type": ""
        }},
        """.format(
            id=id,
            lab=question,
            name=name,
            problem_id=name,
            bug_id=bug_id,
            correct_file="reference.py",
            inputs=",".join(
                f'"{question}/ans/{x}"'
                for x in os.listdir(os.path.join("base", question,"ans"))
                if "input" in x
            ),
        )
        file.write(data)

file.write("]")
file.close()

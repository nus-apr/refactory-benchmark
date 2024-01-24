import os
from os.path import isfile, join, isdir
import subprocess
import pytest
import shutil
import json
from pytest_jsonreport.plugin import JSONReport

questions = [x for x in os.listdir() if not isfile(x) and "question" in x]


def execute_command(command: str, show_output=True, env=dict(), directory=None):
    # Print executed command and execute it in console
    command = command.encode().decode("ascii", "ignore")
    if not directory:
        directory = os.getcwd()
        print_command = command
    else:
        print_command = "[{}] {}".format(directory, command)
    print(print_command)
    command = "{{ {} ;}} 2> {}".format(command, "oof.log")
    if not show_output:
        command += " > /dev/null"
    # print(command)
    new_env = os.environ.copy()
    new_env.update(env)
    process = subprocess.Popen(
        [command], stdout=subprocess.PIPE, shell=True, env=new_env, cwd=directory
    )
    (output, error) = process.communicate()
    # out is the output of the command, and err is the exit value
    return int(process.returncode)


file = open("meta-data.candidate.json", "w")
file.write("[")
id = 0
cwd = os.getcwd()
for question in questions:
    os.chdir(cwd)
    for bug_id in [x for x in os.listdir(question) if isdir(join(question, x))]:
        id = id + 1
        name = bug_id
        inputs = ",".join(
            [
                f'"{question}/ans/{x}"'
                for x in os.listdir(os.path.join("base", question, "ans"))
                if "input" in x
            ]
        )
        correct_solutions = ",".join(
            [
                f'"{question}/ans/{x}"'
                for x in os.listdir(os.path.join("base", question, "correct"))
            ]
        )

        os.chdir(join(question, bug_id))
        os.system("pytest --json-report --timeout=5")
        with open(".report.json") as f:
            report = json.loads(f.read())

        passing_test_identifiers_count = report["summary"].get("passed", 0)
        failing_test_identifiers_count = report["summary"].get("failed", 0)
        passing_test_identifiers = []
        failing_test_identifiers = []
        for test in report["tests"]:
            if test["outcome"] == "passed":
                passing_test_identifiers.append(test["nodeid"])
            else:
                failing_test_identifiers.append(test["nodeid"])
        os.remove(".report.json")
        os.chdir(cwd)

        data = """
        {{
            "id":{id},
            "subject":"{lab}",
            "bug_id":"{problem_id}",
            "source_file": "wrong_{question_id}_{bug_id}.py",
            "reference_file": "{correct_file}",
            "correct_files": [{correct_solutions}],
            "extra_files": [{extra_files}],
            "line_numbers": [],
            "failing_test_identifiers": [{passing_test_identifiers}],
            "passing_test_identifiers": [{failing_test_identifiers}],
            "count_neg": "{passing_test_identifiers_count}",
            "count_pos": "{failing_test_identifiers_count}",
            "exploit_file_list": [{inputs}],
            "test_timeout": 5,
            "bug_type": "",
            "config_script": "",
            "build_script": "",
            "test_script": "run_test",
            "language": "python",
            "test_framework": "pytest"
        }},
        """.format(
            id=id,
            lab=question,
            problem_id=name,
            question_id=question.split("_")[1],
            bug_id=bug_id,
            correct_solutions=correct_solutions,
            extra_files='"global.py"'
            if isfile(join(question, bug_id, "global.py"))
            else "",
            correct_file="reference.py",
            inputs=inputs,
            passing_test_identifiers=",".join(map(lambda f: '"{}"'.format(f), passing_test_identifiers)),
            failing_test_identifiers=",".join(map(lambda f: '"{}"'.format(f), failing_test_identifiers)),
            passing_test_identifiers_count=passing_test_identifiers_count,
            failing_test_identifiers_count=failing_test_identifiers_count,
        )
        file.write(data)

file.write("]")
file.close()

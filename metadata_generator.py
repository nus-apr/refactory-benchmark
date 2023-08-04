import os
from os.path import isfile,join,isdir
import subprocess
import pytest
import shutil
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
    for bug_id in [
        x for x in os.listdir(question) if isdir(join(question,x))
    ]:
        id = id + 1
        name = bug_id
        inputs = ",".join(
                [f'"{question}/ans/{x}"'
                for x in os.listdir(os.path.join("base", question,"ans"))
                if "input" in x]
        )

        os.chdir(join(question,bug_id))
        os.system("touch init.py")
        shutil.rmtree('__pycache__',ignore_errors=True)
        shutil.rmtree('.pytest_cache',ignore_errors=True)
        plugin = JSONReport()
        pytest.main(['--json-report-file=none'], plugins=[plugin])
        passing_test_count = plugin.report["summary"]["passed"]
        failing_test_count = plugin.report["summary"]["failed"]
        passing_tests = []
        failing_tests = []
        for test in plugin.report["tests"]:
            if test["outcome"] == "passed":
                passing_tests.append(test["nodeid"])
            else:
                failing_tests.append(test["nodeid"])
        #os.remove("init.py")
        os.chdir(cwd)

        data = """
        {{
            "id":{id},
            "subject":"{lab}",
            "bug_id":"{problem_id}",
            "source_file": "{bug_id}",
            "reference_file": "{correct_file}",
            "extra_files": [{extra_files}],
            "line_numbers": [],
            "failing_test": [{passing_tests}],
            "passing_test": [{failing_tests}],
            "count_neg": "{passing_test_count}",
            "count_pos": "{failing_test_count}",
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
            bug_id=bug_id,
            extra_files = "'global.py'" if isfile(join(question,bug_id,'global.py')) else '',
            correct_file="reference.py",
            inputs=inputs,
            passing_tests = ','.join(map ( lambda f : '"{}"'.format(f), passing_tests)),
            failing_tests = ','.join(map ( lambda f : '"{}"'.format(f),failing_tests)),
            passing_test_count = passing_test_count,
            failing_test_count = failing_test_count
        )
        file.write(data)

file.write("]")
file.close()

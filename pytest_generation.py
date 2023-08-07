import os
from os.path import join, isfile

questions = [x for x in os.listdir() if not isfile(x) and "question" in x]

test_pattern = """{global_import}
{solution_import}
import pytest
@pytest.mark.timeout(5)
def test_{num}():
    assert {action} == {result}
"""

id = 0
for question in questions:
    test_path = join("base",question,"ans")
    pairs = [ (join(test_path,x),join(test_path,x.replace('input','output'))) for x in os.listdir(test_path) if x.startswith("input")]
    for submission in os.listdir(question):
        if isfile(join(question,submission)):
            continue
        global_import = ""
        if os.path.exists(join(question,submission,"global.py")):
            with open(join(question,submission,"global.py"),"r") as f:
                global_import = f.read()
        solution_import = "from {} import *".format([ x for x in os.listdir(join(question,submission)) if x.startswith('wrong_')][0][:-3])
        for (input_file,output_file) in pairs:
            with open(input_file,"r") as input, open(output_file) as output:
                action = input.readlines()[0].strip()
                result = output.readlines()[0].strip()
                num = input_file.split('_')[-1][:-4]
                test = test_pattern.format( 
                    global_import = global_import,
                    solution_import =solution_import,
                    num = num,
                    action = action,
                    result = result,
                )
                with open(join(question,submission,"test_{}.py".format(num)),"w") as f:
                    f.write(test)
   
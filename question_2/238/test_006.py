

tuple_of_possible_birthdays = (('May', '15'),
                              ('May', '16'),
                              ('May', '19'),
                              ('June', '17'),
                              ('June', '18'),
                              ('July', '14'),
                              ('July', '16'),
                              ('August', '14'),
                              ('August', '15'),
                              ('August', '17'))


from wrong_2_238 import *

def test_006():
    assert contains_unique_day("February", (("January","10"),("February","1"),("February","10"))) == True



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


from wrong_2_014 import *

import pytest
@pytest.mark.timeout(5)
def test_001():
    assert unique_day("1", (("January","1"),("February","1"))) == False

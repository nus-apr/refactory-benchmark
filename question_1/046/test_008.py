
from wrong_1_046 import *

import pytest
@pytest.mark.timeout(5)
def test_008():
    assert search(-100, (-5, -1, 3, 5, 7, 10)) == 0

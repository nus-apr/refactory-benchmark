
from wrong_1_090 import *

import pytest
@pytest.mark.timeout(5)
def test_003():
    assert search(5, (1, 5, 10)) == 1

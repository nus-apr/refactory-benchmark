
from wrong_4_130 import *

import pytest
@pytest.mark.timeout(5)
def test_006():
    assert sort_age([]) == []

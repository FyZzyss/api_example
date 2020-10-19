"""обман ci"""
import pytest

pytestmark = pytest.mark.unit


# Note: this test is for CI-confirmation and should be deleted when there would be normal tests
def test_dull():
    """обман ci"""
    assert True

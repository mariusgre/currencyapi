from utils import total_amount

def test_rounding_upwards():
    assert total_amount(100, 0.2555) == 0.26

def test_rounding_downwards():
    assert total_amount(100, 0.2515) == 0.25

import pytest

from main import get_log_entry


def test_neg_log_index():
    log_index = "-1"
    with pytest.raises(ValueError) as e_info:
        get_log_entry(log_index)

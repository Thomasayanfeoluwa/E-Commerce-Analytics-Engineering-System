from src import validate


def test_negative_values_pass():
    df = validate.check_negative_values()
    assert df.empty


def test_null_foreign_keys_pass():
    df = validate.check_null_foreign_keys()
    assert df.empty


def test_order_totals_match_items():
    assert validate.check_order_total_match_items().empty


def test_no_negative_values():
    assert validate.check_negative_values().empty


def test_no_null_foreign_keys():
    assert validate.check_null_foreign_keys().empty


def test_dates_are_sane():
    assert validate.check_sanity_date().empty
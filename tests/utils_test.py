from datetime import date, datetime

from src.spotlight.utils import get_comparable_dates


def test_get_comparable_dates():
    date1, date2 = get_comparable_dates(datetime.utcnow(), datetime.utcnow())
    date3, date4 = get_comparable_dates(date.today(), date.today())
    date5, date6 = get_comparable_dates(datetime.utcnow(), date.today())
    date7, date8 = get_comparable_dates(date.today(), datetime.utcnow())

    assert isinstance(date1, datetime) and isinstance(date2, datetime)
    assert isinstance(date3, date) and isinstance(date4, date)
    assert isinstance(date5, date) and isinstance(date6, date)
    assert isinstance(date7, date) and isinstance(date8, date)

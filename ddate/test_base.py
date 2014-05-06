"""Unit tests for base.py."""


import pytest
import datetime

from .base import DDate, day_postfix


@pytest.mark.parametrize("dateobj,holidayexp,strexp",
    [
        (
            datetime.date(year=2014, month=2, day=19),
            "Chaoflux",
            "Setting Orange, the 50th day of Chaos in the YOLD 3180.",
        ),
        (
            datetime.date(year=2014, month=5, day=31), 
            "Syaday",
            "Sweetmorn, the 5th day of Confusion in the YOLD 3180.",
        ),
    ],
    ids=("seasonal", "apostle"),
)
def test_discordian_holiday(dateobj, holidayexp, strexp):
    """Ensure the holidays are correctly accounted for."""

    hday = DDate(dateobj)
    assert hday.holiday == holidayexp
    # have to use endswith just in case today is the test day
    assert str(hday).endswith("{0} Celebrate {1}!".format(strexp, holidayexp))


@pytest.mark.parametrize("dateobj,weekday,season,dayofseason,year,strexp",
    [
        (
            datetime.datetime(year=2014, month=12, day=31),
            "Setting Orange", "The Aftermath", 73, 3180,
            "Setting Orange, the 73rd day of The Aftermath in the YOLD 3180"
        ),
        (
            datetime.datetime(year=2015, month=1, day=1),
            "Sweetmorn", "Chaos", 1, 3181, 
            "Sweetmorn, the 1st day of Chaos in the YOLD 3181"
        ),
        (
            datetime.date(year=2012, month=2, day=29),
            None, None, None, 3178,
            "St. Tib's Day, 3178 YOLD"
        ),
        (
            datetime.date(year=2012, month=3, day=1),
            "Setting Orange", "Chaos", 60, 3178,
            "Setting Orange, the 60th day of Chaos in the YOLD 3178"
        ),
        (
            datetime.date(year=2012, month=2, day=28),
            "Prickle-Prickle", "Chaos", 59, 3178,
            "Prickle-Prickle, the 59th day of Chaos in the YOLD 3178"
        ),
        (
            datetime.date(year=2014, month=2, day=1),
            "Boomtime", "Chaos", 32, 3180,
            "Boomtime, the 32nd day of Chaos in the YOLD 3180"
        ),
        (
            datetime.date(year=2012, month=4, day=20),
            "Setting Orange", "Discord", 37, 3178,
            "Setting Orange, the 37th day of Discord in the YOLD 3178"
        ),
    ],
    ids=("new years eve", "new years day", "st tibs day", "day after st tibs",
         "st tibs eve", "avg non leap", "avg post leap"),
)
def test_days_of_the_year(dateobj, weekday, season, dayofseason, year, strexp):
    """Test specific days of the year."""

    ddate_obj = DDate(dateobj)

    if weekday is None:
        # checks for st tibs edge cases, avoids TypeError's on [None] 
        assert ddate_obj.day_of_week == weekday
        assert ddate_obj.season == season
    else:
        assert ddate_obj.WEEKDAYS[ddate_obj.day_of_week] == weekday
        assert ddate_obj.SEASONS[ddate_obj.season] == season
        
    assert ddate_obj.day_of_season == dayofseason
    assert ddate_obj.year == year
    assert str(ddate_obj) == strexp


def test_data_in_repr():
    """Ensure object data is in the repr."""

    ddate_obj = DDate(datetime.date(year=2012, month=2, day=29))
    assert str(hex(id(ddate_obj))) in repr(ddate_obj)
    for attr in dir(ddate_obj):
        if not attr.startswith("_") and attr.lower() == attr:
            assert str(getattr(ddate_obj, attr)) in repr(ddate_obj)


@pytest.mark.parametrize("init_args", (None, object(), False, 0, "abc"))
def test_init_is_today(init_args):
    """If passed an object without a timetuple method, use today."""

    today = datetime.date.today().timetuple()
    if init_args is not None:
        ddate_obj = DDate(init_args).date.timetuple()
    else:
        ddate_obj = DDate().date.timetuple()
    assert today.tm_yday == ddate_obj.tm_yday
    assert today.tm_mon == ddate_obj.tm_mon


@pytest.mark.parametrize("day,postfix", [
    (81, "st"),
    (12, "th"),
    (13, "th"),
    (11, "th"),
    (192, "nd"),
    (93, "rd"),
    (72, "nd"),
    (327, "th"),
])
def test_date_postfixes(day, postfix):
    """Ensure we're putting the right st, nd, rd and th's to integers."""

    assert day_postfix(day) == postfix

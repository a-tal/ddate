"""Unit tests for ddate.py."""


import sys
import datetime

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from ddate import DDate
from ddate.base import day_postfix


class DDateTests(unittest.TestCase):
    """Testing the DDate object creation."""

    def test_specifc_leap_year_day(self):
        """Any old day in a leap year, basic accuracy test."""

        leap = DDate(datetime.date(year=2012, month=4, day=20))
        self.assertEqual(leap.WEEKDAYS[leap.day_of_week], "Setting Orange")
        self.assertEqual(leap.SEASONS[leap.season], "Discord")
        self.assertEqual(leap.day_of_season, 37)

    def test_specific_non_leap_year_day(self):
        """Any old day in a normal year."""

        non_leap = DDate(datetime.date(year=2014, month=2, day=1))
        self.assertEqual(non_leap.WEEKDAYS[non_leap.day_of_week], "Boomtime")
        self.assertEqual(non_leap.SEASONS[non_leap.season], "Chaos")
        self.assertEqual(non_leap.day_of_season, 32)

    def test_discordian_holiday_seasonal(self):
        """Ensure the seasonal holiday is correctly accounted for."""

        holiday = DDate(datetime.date(year=2014, month=2, day=19))
        self.assertEqual(holiday.holiday, "Chaoflux")
        self.assertTrue(str(holiday).endswith(
            "Setting Orange, the 50th day of Chaos in the YOLD 3180. "
            "Celebrate Chaoflux!",
        ))

    def test_discordian_holiday_apostle(self):
        """Ensure the apostle holiday is correctly accounted for."""

        holiday = DDate(datetime.date(year=2014, month=5, day=31))
        self.assertEqual(holiday.holiday, "Syaday")
        self.assertTrue(str(holiday).endswith(
            "Sweetmorn, the 5th day of Confusion in the YOLD 3180. "
            "Celebrate Syaday!",
        ))

    def test_st_tibs_day_eve(self):
        """Test the day before St. Tib's day for sanity."""

        st_tibs_eve = DDate(datetime.date(year=2012, month=2, day=28))
        self.assertEqual(
            str(st_tibs_eve),
            "Prickle-Prickle, the 59th day of Chaos in the YOLD 3178"
        )

    def test_st_tibs_day(self):
        """Test St. Tib's day, also known as leap day."""

        st_tibs_day = DDate(datetime.date(year=2012, month=2, day=29))
        self.assertEqual(str(st_tibs_day), "St. Tib's Day, 3178 YOLD")
        self.assertEqual(st_tibs_day.day_of_season, None)
        self.assertEqual(st_tibs_day.day_of_week, None)

    def test_day_after_st_tibs_day(self):
        """Test the day after St. Tib's."""

        post_st_tibs = DDate(datetime.date(year=2012, month=3, day=1))
        self.assertEqual(
            str(post_st_tibs),
            "Setting Orange, the 60th day of Chaos in the YOLD 3178"
        )

    def test_new_years_eve(self):
        """Test the last day of the year."""

        nye = DDate(datetime.datetime(year=2014, month=12, day=31))
        self.assertEqual(nye.WEEKDAYS[nye.day_of_week], "Setting Orange")
        self.assertEqual(nye.SEASONS[nye.season], "The Aftermath")
        self.assertEqual(nye.day_of_season, 73)
        self.assertEqual(nye.year, 3180)

    def test_new_years_day(self):
        """Test the first day of the year."""

        nyd = DDate(datetime.datetime(year=2015, month=1, day=1))
        self.assertEqual(nyd.WEEKDAYS[nyd.day_of_week], "Sweetmorn")
        self.assertEqual(nyd.SEASONS[nyd.season], "Chaos")
        self.assertEqual(nyd.day_of_season, 1)
        self.assertEqual(nyd.year, 3181)

    def test_data_in_repr(self):
        """Ensure object data is in the repr."""

        ddate_obj = DDate(datetime.date(year=2012, month=2, day=29))
        self.assertIn(str(hex(id(ddate_obj))), repr(ddate_obj))
        for attr in dir(ddate_obj):
            if not attr.startswith("_") and attr.lower() == attr:
                self.assertIn(str(getattr(ddate_obj, attr)), repr(ddate_obj))

    def test_date_being_none_is_today(self):
        """If not passed an argument, it should default to today."""

        today = datetime.date.today().timetuple()
        ddate_obj = DDate().date.timetuple()
        self.assertEqual(today.tm_yday, ddate_obj.tm_yday)
        self.assertEqual(today.tm_mon, ddate_obj.tm_mon)

    def test_non_date_obj_is_today(self):
        """If passed an object without a timetuple method, use today."""

        today = datetime.date.today().timetuple()
        ddate_obj = DDate(object()).date.timetuple()
        self.assertEqual(today.tm_yday, ddate_obj.tm_yday)
        self.assertEqual(today.tm_mon, ddate_obj.tm_mon)

    def test_date_postfixes(self):
        """Ensure we're putting the right st, nd, rd and th's to integers."""

        test_data = [
            (81, "st"),
            (12, "th"),
            (13, "th"),
            (11, "th"),
            (192, "nd"),
            (93, "rd"),
            (72, "nd"),
            (327, "th"),
        ]
        for day, postfix in test_data:
            self.assertEqual(day_postfix(day), postfix)


if __name__ == "__main__":
    unittest.main()

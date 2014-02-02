"""Unit tests for ddate.py."""


import datetime
import unittest

try:
    import ddate
except ImportError:
    import sys
    sys.path.insert(1, "..")
    import src as ddate


class DDateTests(unittest.TestCase):
    def test_specifc_leap_year_day(self):
        leap = ddate.DDate(datetime.date(year=2012, month=4, day=20))
        self.assertEqual(leap.WEEKDAYS[leap.day_of_week], "Setting Orange")
        self.assertEqual(leap.SEASONS[leap.season], "Discord")
        self.assertEqual(leap.day_of_season, 37)

    def test_specific_non_leap_year_day(self):
        non_leap = ddate.DDate(datetime.date(year=2014, month=2, day=1))
        self.assertEqual(non_leap.WEEKDAYS[non_leap.day_of_week], "Boomtime")
        self.assertEqual(non_leap.SEASONS[non_leap.season], "Chaos")
        self.assertEqual(non_leap.day_of_season, 32)

    def test_discordian_holiday(self):
        holiday = ddate.DDate(datetime.date(year=2014, month=2, day=19))
        self.assertEqual(holiday.holiday, "Chaoflux")
        self.assertTrue(str(holiday).endswith(
            "Setting Orange, the 50th day of Chaos in the YOLD 3180. "
            "Celebrate Chaoflux!",
        ))

    def test_st_tibs_day_eve(self):
        st_tibs_eve = ddate.DDate(datetime.date(year=2012, month=2, day=28))
        self.assertEqual(
            str(st_tibs_eve),
            "Prickle-Prickle, the 59th day of Chaos in the YOLD 3178"
        )

    def test_st_tibs_day(self):
        st_tibs_day = ddate.DDate(datetime.date(year=2012, month=2, day=29))
        self.assertEqual(str(st_tibs_day), "St. Tib's Day, 3178 YOLD")
        self.assertEqual(st_tibs_day.day_of_season, None)
        self.assertEqual(st_tibs_day.day_of_week, None)

    def test_day_after_st_tibs_day(self):
        post_st_tibs = ddate.DDate(datetime.date(year=2012, month=3, day=1))
        self.assertEqual(
            str(post_st_tibs),
            "Setting Orange, the 60th day of Chaos in the YOLD 3178"
        )

    def test_new_years_eve(self):
        nye = ddate.DDate(datetime.datetime(year=2014, month=12, day=31))
        self.assertEqual(nye.WEEKDAYS[nye.day_of_week], "Setting Orange")
        self.assertEqual(nye.SEASONS[nye.season], "The Aftermath")
        self.assertEqual(nye.day_of_season, 73)
        self.assertEqual(nye.year, 3180)

    def test_new_years_day(self):
        nyd = ddate.DDate(datetime.datetime(year=2015, month=1, day=1))
        self.assertEqual(nyd.WEEKDAYS[nyd.day_of_week], "Sweetmorn")
        self.assertEqual(nyd.SEASONS[nyd.season], "Chaos")
        self.assertEqual(nyd.day_of_season, 1)
        self.assertEqual(nyd.year, 3181)

    def test_data_in_repr(self):
        ddate_obj = ddate.DDate(datetime.date(year=2012, month=2, day=29))
        self.assertIn(str(hex(id(ddate_obj))), repr(ddate_obj))
        for attr in dir(ddate_obj):
            if not attr.startswith("_") and attr.lower() == attr:
                self.assertIn(str(getattr(ddate_obj, attr)), repr(ddate_obj))


if __name__ == "__main__":
    unittest.main()

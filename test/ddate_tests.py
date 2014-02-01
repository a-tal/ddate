"""Unit tests for ddate.py."""


import datetime
import unittest

import ddate


class DDateTests(unittest.TestCase):
    def test_specifc_leap_day(self):
        ddate_2012420 = ddate.DDate(datetime.date(year=2012, month=4, day=20))
        self.assertEqual(
            ddate_2012420.weekdays[ddate_2012420.day_of_week],
            "Setting Orange",
        )
        self.assertEqual(ddate_2012420.day_of_season, 37)
        self.assertEqual(
            ddate_2012420.seasons[ddate_2012420.season],
            "Discord",
        )

    def test_specific_non_leap_day(self):
        ddate_now = ddate.DDate(datetime.date(year=2014, month=2, day=1))
        self.assertEqual(
            ddate_now.weekdays[ddate_now.day_of_week],
            "Boomtime",
        )
        self.assertEqual(ddate_now.day_of_season, 32)
        self.assertEqual(
            ddate_now.seasons[ddate_now.season],
            "Chaos",
        )

    def test_string_formatting(self):
        ddate_now = ddate.DDate(datetime.date(year=2014, month=2, day=1))
        self.assertTrue(str(ddate_now).endswith(
            "Boomtime, the 32nd day of Chaos in the YOLD 3180",
        ))

    def test_holiday_string_formatting(self):
        ddate_now = ddate.DDate(datetime.date(year=2014, month=2, day=19))
        self.assertTrue(str(ddate_now).endswith(
            "Setting Orange, the 50th day of Chaos in the YOLD 3180. "
            "Celebrate Chaoflux!",
        ))

    def test_st_tibs_day(self):
        ddate_tibs = ddate.DDate(datetime.date(year=2012, month=2, day=29))
        self.assertEqual(
            str(ddate_tibs),
            "St. Tib's Day, 3178 YOLD",
        )

    def test_day_after_st_tibs_day(self):
        ddate_tibs = ddate.DDate(datetime.date(year=2012, month=3, day=1))
        self.assertEqual(
            str(ddate_tibs),
            "Setting Orange, the 60th day of Chaos in the YOLD 3178"
        )


if __name__ == "__main__":
    unittest.main()

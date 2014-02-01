"""DDate.py -- Discordian Date Object Class.

Usage Examples:

    from ddate import DDate

    print(DDate())
    print(DDate(datetime.date(year=2014, month=4, day=20)))
"""


import datetime


class DDate(object):
    """Discordian Date Object.

    Methods:
        __str__: returns a formatted Discordian date string

    Attributes::

        date: the datetime.[date|datetime] object used to initialize with
        day_of_week: the integer day of the week (0-5)
        day_of_season: the integer day of the season (1-73)
        holiday: string holiday currently, or None
        holidays: dict of Discordian holidays, {type: [holidays_per_season]}
        season: integer season number
        seasons: list of strings, Discordian seasons
        weekdays: list of strings, Discordian days of the week
        year: integer Discordian YOLD
    """

    def __init__(self, date=None, *args, **kwargs):
        """Discordian date setup and mangling.

        Args:
            date: optional, date object with a timetuple method, or uses now
        """

        if date is None or not hasattr(date, "timetuple"):
            date = datetime.date.today()

        self.date = date

        time_tuple = self.date.timetuple()
        year = time_tuple.tm_year
        day_of_year = time_tuple.tm_yday - 1

        is_leap_year = (
            (year % 100 != 0 and year % 4 == 0) or
            (year % 100 == 0 and year % 400 == 0)
        )

        day_of_year_leap_corrected = day_of_year
        if is_leap_year and day_of_year > 59:
            day_of_year_leap_corrected -= 1

        self.day_of_season = (day_of_year_leap_corrected % 73) + 1
        self.day_of_week = day_of_year_leap_corrected % 5
        self.season = int(day_of_year_leap_corrected / 73)
        self.year = year + 1166

        self.seasons = [
            "Chaos",
            "Discord",
            "Confusion",
            "Bureaucracy",
            "The Aftermath",
        ]
        self.weekdays = [
            "Sweetmorn",
            "Boomtime",
            "Pungenday",
            "Prickle-Prickle",
            "Setting Orange",
        ]
        self.holidays = {
            "apostle": [
                "Mungday",
                "Mojoday",
                "Syaday",
                "Zaraday",
                "Maladay",
            ],
            "seasonal": [
                "Chaoflux",
                "Discoflux",
                "Confuflux",
                "Bureflux",
                "Afflux",
            ],
        }

        if is_leap_year and day_of_year == 59:
            self.holiday = "St. Tib's Day"
        elif self.day_of_season == 5:
            self.holiday = self.holidays["apostle"][self.season]
        elif self.day_of_season == 50:
            self.holiday = self.holidays["seasonal"][self.season]
        else:
            self.holiday = None

        super(DDate, self).__init__(*args, **kwargs)

    def __str__(self):
        """String formatting for the current date."""

        today = 0 <= (self.date - datetime.date.today()).days < 1

        if self.holiday == "St. Tib's Day":
            return "{today}{self.holiday}, {self.year} YOLD".format(
                today="Today is " if today else "",
                self=self,
            )
        else:
            return (
                "{today}{day}, the {self.day_of_season}{pfix}"
                " day of {season} in the YOLD {self.year}"
                "{celebrate}{holiday}{exclamation}"
            ).format(
                today="Today is " if today else "",
                day=self.weekdays[self.day_of_week],
                self=self,
                pfix=_day_postfix(self.day_of_season),
                season=self.seasons[self.season],
                celebrate=". Celebrate " if self.holiday else "",
                holiday=self.holiday or "",
                exclamation="!" if self.holiday else "",
            )


def _day_postfix(day):
    """Returns day's correct postfix (2nd, 3rd, 61st, etc)."""

    if day != 11 and day % 10 == 1:
        pfix = "st"
    elif day != 12 and day % 10 == 2:
        pfix = "nd"
    elif day != 13 and day % 10 == 3:
        pfix = "rd"
    else:
        pfix = "th"

    return pfix


if __name__ == "__main__":
    print(DDate())

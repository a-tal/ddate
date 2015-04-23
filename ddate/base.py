"""DDate.py -- Discordian Date Object Class.

Usage Examples::

    >>> from ddate.base import DDate
    >>>
    >>> DDate()
    <src.ddate.DDate object at 0x7f3a6b88eb50>
    <DDate date: 2014-02-01, day_of_season: 32, day_of_week: 1, holiday: None,
    season: 0, year: 3180>
    >>>
    >>> print(DDate())
    Today is Boomtime, the 32nd day of Chaos in the YOLD 3180
    >>>
    >>> import datetime
    >>> print(DDate(datetime.date(year=2014, month=4, day=20)))
    Setting Orange, the 37th day of Discord in the YOLD 3180
"""


from __future__ import print_function

import sys
import datetime


is_leap_year = lambda x : (
    (x % 100 != 0 and x % 4 == 0) or (x % 100 == 0 and x % 400 == 0)
)


class DDate(object):
    """Discordian Date Object.

    Methods::

        __repr__: returns the typical repr plus the ddate attributes
        __str__: returns a formatted Discordian date string

    Attributes::

        date: the datetime.[date|datetime] object used to initialize with
        day_of_week: the ordinal integer day of the week (0-5), or None
        day_of_season: the cardinal integer day of the season (1-73), or None
        holiday: string holiday currently, or None
        season: ordinal integer season number (0-5)
        year: integer Discordian YOLD

    Statics::

        HOLIDAYS: dict of Discordian holidays, {type: [holidays_per_season]}
        SEASONS: list of strings, Discordian seasons
        WEEKDAYS: list of strings, Discordian days of the week
    """

    HOLIDAYS = {
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
    SEASONS = [
        "Chaos",
        "Discord",
        "Confusion",
        "Bureaucracy",
        "The Aftermath",
    ]
    WEEKDAYS = [
        "Sweetmorn",
        "Boomtime",
        "Pungenday",
        "Prickle-Prickle",
        "Setting Orange",
    ]

    def __init__(self, date=None, year=None, season=None, day_of_season=None,
                 *args, **kwargs):
        """Discordian date setup and mangling.

        Args:
            date: optional date object with a timetuple method, or uses today
            year: optional integer discordian year to create from (requires season and day_of_season)
            season: optional integer discodian season to create from (requires year and day_of_season)
            day_of_season: optional integer discordian day of season to create from (requires year and season)
        """

        if year is not None and season is not None and day_of_season is not None:
            date = datetime.datetime(year=year - 1166, month=1, day=1) + \
                   datetime.timedelta(days=(season * 73) + day_of_season - 1)
        elif date is None or not hasattr(date, "timetuple"):
            date = datetime.date.today()
        self.date = date

        time_tuple = self.date.timetuple()

        # calculate leap year using tradtional methods to align holidays
        year = time_tuple.tm_year
        self.year = year + 1166  # then adjust accordingly and assign

        day_of_year = time_tuple.tm_yday - 1  # ordinal
        if is_leap_year(year) and day_of_year > 59:
            day_of_year -= 1  # St. Tib's doesn't count

        self.day_of_week = day_of_year % 5
        self.day_of_season = day_of_year % 73 + 1  # cardinal
        self.season = int(day_of_year / 73)

        if is_leap_year(year) and time_tuple.tm_yday == 60:
            self.holiday = "St. Tib's Day"
            self.day_of_week = None
            self.day_of_season = None
            self.season = None
        elif self.day_of_season == 5:
            self.holiday = self.HOLIDAYS["apostle"][self.season]
        elif self.day_of_season == 50:
            self.holiday = self.HOLIDAYS["seasonal"][self.season]
        else:
            self.holiday = None

        super(DDate, self).__init__(*args, **kwargs)

    def __str__(self):
        """Return a formatted string for the current date."""

        today = self.date.timetuple().tm_yday == datetime.date.today(
            ).timetuple().tm_yday

        if self.holiday == "St. Tib's Day":
            return "{today}{self.holiday}, {self.year} YOLD".format(
                today="Today is " if today else "",
                self=self,
            )
        else:
            return (
                "{today}{day}, the {self.day_of_season}{pfix}"
                " day of {season} in the YOLD {self.year}{holiday}"
            ).format(
                today="Today is " if today else "",
                day=self.WEEKDAYS[self.day_of_week],
                self=self,
                pfix=day_postfix(self.day_of_season),
                season=self.SEASONS[self.season],
                holiday=". Celebrate {0}!".format(
                    self.holiday) if self.holiday else "",
            )

    def __repr__(self):
        """Return our id and attributes."""

        attributes = []
        for attr in dir(self):
            if not attr.startswith("_") and attr.lower() == attr:
                attributes.append(
                    "{attr}: {{self.{attr}}}".format(attr=attr)
                )

        return "<{name}.{cls} object at {id}>\n<{cls} {attributes}>".format(
            name=__name__,
            cls=self.__class__.__name__,
            id=hex(id(self)),
            attributes=", ".join(attributes).format(self=self),
        )


def day_postfix(day):
    """Returns day's correct postfix (2nd, 3rd, 61st, etc)."""

    if day != 11 and day % 10 == 1:
        postfix = "st"
    elif day != 12 and day % 10 == 2:
        postfix = "nd"
    elif day != 13 and day % 10 == 3:
        postfix = "rd"
    else:
        postfix = "th"

    return postfix


def _get_date(day=None, month=None, year=None):
    """Returns a datetime object with optional params or today."""

    now = datetime.date.today()
    if day is None:
        return now

    try:
        return datetime.date(
            day=int(day),
            month=int(month or now.month),
            year=int(year or now.year),
        )
    except ValueError as error:
        print("error: {0}".format(error), file=sys.stderr)


def main():
    """Command line entry point."""

    def help_exit():
        raise SystemExit("usage: ddate [day] [month] [year]")

    if "--help" in sys.argv or "-h" in sys.argv:
        help_exit()

    if len(sys.argv) == 2:  # allow for 23-2-2014 style, be lazy/sloppy with it
        for split_char in ".-/`,:;":  # who knows what the human will use...
            if split_char in sys.argv[1]:
                parts = sys.argv[1].split(split_char)
                del sys.argv[1]
                sys.argv.extend(parts)
                break

    date = _get_date(*sys.argv[1:])

    if date:
        print(DDate(date))
    else:
        help_exit()


if __name__ == "__main__":
    main()

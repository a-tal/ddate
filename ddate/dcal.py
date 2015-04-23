import os
import sys
from ddate.base import DDate, is_leap_year


__doc__ = """Similar to the `cal` command, but for the Discordian calendar.

Usage:
    {} [season] [year]

Season can be an integer between 1 and 5, steps with + or -, 'next', or any of
the Discordian season names. The year is in Discordian (+= 1166 to Gregorian).

Examples:
    dcal +2          # prints two seasons into the future
    dcal aft         # prints the last season (The Aftermath) of this year
    dcal discord -2  # prints the Discord season from two years ago
    dcal +6 +1       # prints the calendar 6 seasons and one year in the future

Discordian season names:
    {}""".format(
    os.path.basename(sys.argv[0]),
    "\n    ".join(DDate.SEASONS),
)


import datetime
import operator
from dateandtime.multicalendar import MultiCalendar


# adjusted for Discord
MINYEAR = datetime.MINYEAR + 1166
MAXYEAR = datetime.MAXYEAR + 1166


def _season_overflow(season, moved_year, now):
    """Pushes illegal seasons ints into the next/previous year."""

    if season > 4:
        while season > 4:
            if moved_year is None:
                moved_year = now.year + 1
            else:
                moved_year += 1
            season -= 5
    elif season < 0:
        while season < 0:
            if moved_year is None:
                moved_year = now.year - 1
            else:
                moved_year -= 1
            season += 5
    return season, moved_year


def discordian_calendar(season=None, year=None, dtobj=None):
    """Prints a discordian calendar for a particular season and year.

    Args::

        season: integer cardinal season from 1 to 5
        year: integer discordian year from 1166 to MAXYEAR + 1166
        dtobj: datetime object to instatiate the calendar from (Gregorian)
    """

    now = DDate(dtobj)

    moved_year = None

    if season is None:
        season = now.season
    elif season.lower() == "next":
        season, moved_year = _season_overflow(now.season or 0 + 1, moved_year, now)
    else:
        # allow for +1, -2, for seasons...
        for symbol, oper in zip(("+", "-"), (operator.add, operator.sub)):
            if symbol in season:
                try:
                    amount = int(season.strip(symbol))
                except ValueError:
                    raise ValueError("unknown season: {}".format(season))
                else:
                    season, moved_year = _season_overflow(
                        oper(now.season or 0, amount),
                        moved_year,
                        now,
                    )
                    break
        else:
            # allow to use the season name or some starting part of it
            input_name = season.lower()
            for season_name in now.SEASONS:
                _name = season_name.lower()
                if input_name == _name or any(
                        [n.startswith(input_name) for n in _name.split(" ")]):
                    season = now.SEASONS.index(season_name)
                    break
            else:
                try:  # last try with a literal int being passed in
                    season = int(season)
                except ValueError:
                    raise ValueError("unknown season: {}".format(season))
                else:
                    if not 1 <= season <= 5:
                        raise ValueError("season must be in 1..5")
                    season -= 1  # allowing cardinal numbers from the user

    if year is None:
        year = moved_year or now.year
    else:
        for symbol, oper in zip(("+", "-"), (operator.add, operator.sub)):
            if symbol in year:
                year = oper(moved_year or now.year, int(year.strip(symbol)))
                break
        else:
            try:
                year = int(year)
            except ValueError:
                raise ValueError("invalid year: {}".format(year))

    if not MINYEAR <= year <= MAXYEAR:
        # otherwise this error isn't that helpful
        raise ValueError("year must be in {}..{}".format(MINYEAR, MAXYEAR))

    if now.day_of_season is None:
        if is_leap_year(year - 1166):
            day_of_season = None
        else:
            day_of_season = 59
        season = season or 0
    else:
        day_of_season = now.day_of_season

    if day_of_season:
        cal_date = DDate(year=year, season=season, day_of_season=day_of_season)
        cal = MultiCalendar(discordian=True, date=cal_date)
        cal.print_calendar()
    else:
        print("{} in YOLD {}".format(now.holiday, year))


def main():
    """Command line entry point for dcal."""

    if "--help" in sys.argv or len(sys.argv) > 3:
        raise SystemExit(__doc__)

    try:
        discordian_calendar(*sys.argv[1:])
    except ValueError as error:
        raise SystemExit("Error: {}".format("\n".join(error.args)))


if __name__ == "__main__":
    main()

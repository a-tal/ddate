DDate
=====

[![Build Status](https://travis-ci.org/a-tal/ddate.png?branch=master)](https://travis-ci.org/a-tal/ddate)
[![Coverage Status](https://coveralls.io/repos/a-tal/ddate/badge.png?branch=master)](https://coveralls.io/r/a-tal/ddate?branch=master)
[![Version](https://pypip.in/v/ddate/badge.png)](https://pypi.python.org/pypi/ddate/)
[![Downloads this month](https://pypip.in/d/ddate/badge.png)](https://pypi.python.org/pypi/ddate/)

Discordian Date Python Object Class.


Python Usage Examples
---------------------

    >>> from ddate import DDate
    >>>
    >>> DDate()
    <src.ddate.DDate object at 0x7f3a6b88eb50>
    <DDate date: 2014-02-01, day_of_season: 32, day_of_week: 1, holiday: None, season: 0, year: 3180>
    >>>
    >>> print(DDate())
    Today is Boomtime, the 32nd day of Chaos in the YOLD 3180
    >>>
    >>> import datetime
    >>> print(DDate(datetime.date(year=2014, month=4, day=20)))
    Setting Orange, the 37th day of Discord in the YOLD 3180


Install
-------

    $ git clone https://github.com/a-tal/ddate
    $ cd ddate
    $ python setup.py build
    $ sudo python setup.py install
    $ ddate
    Today is Boomtime, the 32nd day of Chaos in the YOLD 3180


Also available through pip or easyinstall.

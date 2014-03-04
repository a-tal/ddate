DDate
=====

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

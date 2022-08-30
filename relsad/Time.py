from enum import Enum
from numbers import Number


class TimeUnit(Enum):
    """
    Time unit

    Attributes
    ----------
    SECOND : int
        Second
    MINUTE : int
        Minute
    HOUR : int
        Hour
    DAY : int
        Day
    WEEK : int
        Week
    MONTH : int
        Month
    YEAR : int
        Year
    """

    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4
    WEEK = 5
    MONTH = 6
    YEAR = 7


class Time:

    """
    Time utility class

    ...

    Attributes
    ----------
    SEC_per_MIN : float
        Seconds in a minute
    MIN_per_HOUR : float
        Minutes in an hour
    HOUR_per_DAY : float
        Hours in a day
    DAY_per_WEEK : float
        Days in a week
    WEEK_per_MONTH : float
        Weeks in a month
    MONTH_per_YEAR : float
        Months in a year
    quantity : float
        Time quantity, the quantity of a time unit
    unit : TimeUnit
        The time unit

    Methods
    ----------
    convert_unit(unit)
        Converts the time based on the sat time unit to the correct time
    get_unit_quantity(unit)
        Returns the time quantity of the class instance in the given unit
    get_seconds()
        Returns the time quantity in seconds
    get_minutes()
        Returns the time quantity in minutes
    get_hours()
        Returns the time quantity in hours
    get_days()
        Returns the time quantity in days
    get_months()
        Returns the time quantity in months
    get_years()
        Returns the time quantity in year

    """

    SEC_per_MIN = 60
    MIN_per_HOUR = 60
    HOUR_per_DAY = 24
    DAY_per_WEEK = 7
    WEEK_per_MONTH = 4.3452
    MONTH_per_YEAR = 12

    def __init__(self, quantity: float, unit: TimeUnit = TimeUnit.HOUR):
        if not isinstance(quantity, Number):
            raise Exception("The time quantity must be a number.")
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        if self.unit == TimeUnit.SECOND:
            return f"SEC_{self.quantity}"
        elif self.unit == TimeUnit.MINUTE:
            return f"MIN_{self.quantity}"
        elif self.unit == TimeUnit.HOUR:
            return f"HOUR_{self.quantity}"
        elif self.unit == TimeUnit.DAY:
            return f"DAY_{self.quantity}"
        elif self.unit == TimeUnit.WEEK:
            return f"WEEK_{self.quantity}"
        elif self.unit == TimeUnit.MONTH:
            return f"MONTH_{self.quantity}"
        elif self.unit == TimeUnit.YEAR:
            return f"YEAR_{self.quantity}"

    def __repr__(self):
        if self.unit == TimeUnit.SECOND:
            return f"SEC_{self.quantity}"
        elif self.unit == TimeUnit.MINUTE:
            return f"MIN_{self.quantity}"
        elif self.unit == TimeUnit.HOUR:
            return f"HOUR_{self.quantity}"
        elif self.unit == TimeUnit.DAY:
            return f"DAY_{self.quantity}"
        elif self.unit == TimeUnit.WEEK:
            return f"WEEK_{self.quantity}"
        elif self.unit == TimeUnit.MONTH:
            return f"MONTH_{self.quantity}"
        elif self.unit == TimeUnit.YEAR:
            return f"YEAR_{self.quantity}"

    def __hash__(self):
        if self.unit == TimeUnit.SECOND:
            return hash(f"SEC_{self.quantity}")
        elif self.unit == TimeUnit.MINUTE:
            return hash(f"MIN_{self.quantity}")
        elif self.unit == TimeUnit.HOUR:
            return hash(f"HOUR_{self.quantity}")
        elif self.unit == TimeUnit.DAY:
            return hash(f"DAY_{self.quantity}")
        elif self.unit == TimeUnit.WEEK:
            return hash(f"WEEK_{self.quantity}")
        elif self.unit == TimeUnit.MONTH:
            return hash(f"MONTH_{self.quantity}")
        elif self.unit == TimeUnit.YEAR:
            return hash(f"YEAR_{self.quantity}")

    def convert_unit(self, unit: TimeUnit):
        """
        Converts the time based on the sat time unit to the correct time

        Parameters
        ----------
        unit : TimeUnit
            The time unit

        Returns
        ----------
        None

        """
        if unit == TimeUnit.SECOND:
            self.quantity = self.get_seconds()
            self.unit = TimeUnit.SECOND
        elif unit == TimeUnit.MINUTE:
            self.quantity = self.get_minutes()
            self.unit = TimeUnit.MINUTE
        elif unit == TimeUnit.HOUR:
            self.quantity = self.get_hours()
            self.unit = TimeUnit.HOUR
        elif unit == TimeUnit.DAY:
            self.quantity = self.get_days()
            self.unit = TimeUnit.DAY
        elif unit == TimeUnit.WEEK:
            self.quantity = self.get_weeks()
            self.unit = TimeUnit.WEEK
        elif unit == TimeUnit.MONTH:
            self.quantity = self.get_months()
            self.unit = TimeUnit.MONTH
        elif unit == TimeUnit.YEAR:
            self.quantity = self.get_years()
            self.unit = TimeUnit.YEAR

    def get_unit_quantity(self, unit: TimeUnit):
        """
        Returns the time quantity of the class instance in the given unit

        Parameters
        ----------
        unit : TimeUnit
            The time unit

        Returns
        ----------
        time_quantity : float
            The time quantity of the class instance in the given unit

        """
        time_quantity = 0
        if unit == TimeUnit.SECOND:
            time_quantity = self.get_seconds()
        elif unit == TimeUnit.MINUTE:
            time_quantity = self.get_minutes()
        elif unit == TimeUnit.HOUR:
            time_quantity = self.get_hours()
        elif unit == TimeUnit.DAY:
            time_quantity = self.get_days()
        elif unit == TimeUnit.WEEK:
            time_quantity = self.get_weeks()
        elif unit == TimeUnit.MONTH:
            time_quantity = self.get_months()
        elif unit == TimeUnit.YEAR:
            time_quantity = self.get_years()
        return time_quantity

    def __lt__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity < other.get_unit_quantity(self.unit)

    def __le__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity <= other.get_unit_quantity(self.unit)

    def __gt__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity > other.get_unit_quantity(self.unit)

    def __ge__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity >= other.get_unit_quantity(self.unit)

    def __eq__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity == other.get_unit_quantity(self.unit)

    def __ne__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity != other.get_unit_quantity(self.unit)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception("Wrong type")
        return Time(
            self.quantity + other.get_unit_quantity(self.unit), self.unit
        )

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception("Wrong type")
        return Time(
            self.quantity - other.get_unit_quantity(self.unit), self.unit
        )

    def __truediv__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception("Wrong type")
        if other.get_hours() == 0:
            raise Exception("Other time is zero")
        return self.get_hours() / other.get_hours()

    def get_seconds(self):
        """
        Returns the time quantity in seconds

        Parameters
        ----------
        None

        Returns
        ----------
        seconds : float
            The time quantity in seconds

        """
        seconds = 0
        if self.unit == TimeUnit.SECOND:
            seconds = self.quantity
        elif self.unit == TimeUnit.MINUTE:
            seconds = self.quantity * self.SEC_per_MIN
        elif self.unit == TimeUnit.HOUR:
            seconds = self.quantity * self.SEC_per_MIN * self.MIN_per_HOUR
        elif self.unit == TimeUnit.DAY:
            seconds = (
                self.quantity
                * self.SEC_per_MIN
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
            )
        elif self.unit == TimeUnit.WEEK:
            seconds = (
                self.quantity
                * self.SEC_per_MIN
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
            )
        elif self.unit == TimeUnit.MONTH:
            seconds = (
                self.quantity
                * self.SEC_per_MIN
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.YEAR:
            seconds = (
                self.quantity
                * self.SEC_per_MIN
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
                * self.MONTH_per_YEAR
            )
        return seconds

    def get_minutes(self):
        """
        Returns the time quantity in minutes

        Parameters
        ----------
        None

        Returns
        ----------
        minutes : float
            The time quantity in minutes

        """
        minutes = 0
        if self.unit == TimeUnit.SECOND:
            minutes = self.quantity / self.SEC_per_MIN
        elif self.unit == TimeUnit.MINUTE:
            minutes = self.quantity
        elif self.unit == TimeUnit.HOUR:
            minutes = self.quantity * self.MIN_per_HOUR
        elif self.unit == TimeUnit.DAY:
            minutes = self.quantity * self.MIN_per_HOUR * self.HOUR_per_DAY
        elif self.unit == TimeUnit.WEEK:
            minutes = (
                self.quantity
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
            )
        elif self.unit == TimeUnit.MONTH:
            minutes = (
                self.quantity
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.YEAR:
            minutes = (
                self.quantity
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
                * self.MONTH_per_YEAR
            )
        return minutes

    def get_hours(self):
        """
        Returns the time quantity in hours

        Parameters
        ----------
        None

        Returns
        ----------
        hours : float
            The time quantity in hours

        """
        hours = 0
        if self.unit == TimeUnit.SECOND:
            hours = self.quantity / self.SEC_per_MIN / self.MIN_per_HOUR
        elif self.unit == TimeUnit.MINUTE:
            hours = self.quantity / self.MIN_per_HOUR
        elif self.unit == TimeUnit.HOUR:
            hours = self.quantity
        elif self.unit == TimeUnit.DAY:
            hours = self.quantity * self.HOUR_per_DAY
        elif self.unit == TimeUnit.WEEK:
            hours = self.quantity * self.HOUR_per_DAY * self.DAY_per_WEEK
        elif self.unit == TimeUnit.MONTH:
            hours = (
                self.quantity
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.YEAR:
            hours = (
                self.quantity
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
                * self.MONTH_per_YEAR
            )
        return hours

    def get_days(self):
        """
        Returns the time quantity in days

        Parameters
        ----------
        None

        Returns
        ----------
        days : float
            The time quantity in days

        """
        days = 0
        if self.unit == TimeUnit.SECOND:
            days = (
                self.quantity
                / self.SEC_per_MIN
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
            )
        elif self.unit == TimeUnit.MINUTE:
            days = self.quantity / self.MIN_per_HOUR / self.HOUR_per_DAY
        elif self.unit == TimeUnit.HOUR:
            days = self.quantity / self.HOUR_per_DAY
        elif self.unit == TimeUnit.DAY:
            days = self.quantity
        elif self.unit == TimeUnit.WEEK:
            days = self.quantity * self.DAY_per_WEEK
        elif self.unit == TimeUnit.MONTH:
            days = self.quantity * self.DAY_per_WEEK * self.WEEK_per_MONTH
        elif self.unit == TimeUnit.YEAR:
            days = (
                self.quantity
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
                * self.MONTH_per_YEAR
            )
        return days

    def get_weeks(self):
        """
        Returns the time quantity in weeks

        Parameters
        ----------
        None

        Returns
        ----------
        weeks : float
            The time quantity in weeks

        """
        weeks = 0
        if self.unit == TimeUnit.SECOND:
            weeks = (
                self.quantity
                / self.SEC_per_MIN
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
            )
        elif self.unit == TimeUnit.MINUTE:
            weeks = (
                self.quantity
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
            )
        elif self.unit == TimeUnit.HOUR:
            weeks = self.quantity / self.HOUR_per_DAY / self.DAY_per_WEEK
        elif self.unit == TimeUnit.DAY:
            weeks = self.quantity / self.DAY_per_WEEK
        elif self.unit == TimeUnit.WEEK:
            weeks = self.quantity
        elif self.unit == TimeUnit.MONTH:
            weeks = self.quantity * self.WEEK_per_MONTH
        elif self.unit == TimeUnit.YEAR:
            weeks = self.quantity * self.WEEK_per_MONTH * self.MONTH_per_YEAR
        return weeks

    def get_months(self):
        """
        Returns the time quantity in months

        Parameters
        ----------
        None

        Returns
        ----------
        months : float
            The time quantity in months

        """
        months = 0
        if self.unit == TimeUnit.SECOND:
            months = (
                self.quantity
                / self.SEC_per_MIN
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.MINUTE:
            months = (
                self.quantity
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.HOUR:
            months = (
                self.quantity
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.DAY:
            months = self.quantity / self.DAY_per_WEEK / self.WEEK_per_MONTH
        elif self.unit == TimeUnit.WEEK:
            months = self.quantity / self.WEEK_per_MONTH
        elif self.unit == TimeUnit.MONTH:
            months = self.quantity
        elif self.unit == TimeUnit.YEAR:
            months = self.quantity * self.MONTH_per_YEAR
        return months

    def get_years(self):
        """
        Returns the time quantity in years

        Parameters
        ----------
        None

        Returns
        ----------
        years : float
            The time quantity in years

        """
        years = 0
        if self.unit == TimeUnit.SECOND:
            years = (
                self.quantity
                / self.SEC_per_MIN
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
                / self.MONTH_per_YEAR
            )
        elif self.unit == TimeUnit.MINUTE:
            years = (
                self.quantity
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
                / self.MONTH_per_YEAR
            )
        elif self.unit == TimeUnit.HOUR:
            years = (
                self.quantity
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
                / self.MONTH_per_YEAR
            )
        elif self.unit == TimeUnit.DAY:
            years = (
                self.quantity
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
                / self.MONTH_per_YEAR
            )
        elif self.unit == TimeUnit.WEEK:
            years = self.quantity / self.WEEK_per_MONTH / self.MONTH_per_YEAR
        elif self.unit == TimeUnit.MONTH:
            years = self.quantity / self.MONTH_per_YEAR
        elif self.unit == TimeUnit.YEAR:
            years = self.quantity
        return years


class TimeStamp:
    """
    Time stamp utility class

    ...

    Attributes
    ----------
    year : int
        Number of years
    month : int
        Number of months
    day : int
        Number of days
    hour : int
        Number of hours
    minute : int
        Number of minutes
    second : int
        Number of seconds

    Methods
    ----------
    get_hour_of_day(time_passed)
        Returns the hour of day based on the time passed

    """

    def __init__(
        self,
        year: int = 0,
        month: int = 0,
        day: int = 0,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        # Calculate time quantity
        self.time_quantity = Time(0, TimeUnit.SECOND)
        self.time_quantity += Time(year, TimeUnit.YEAR)
        self.time_quantity += Time(month, TimeUnit.MONTH)
        self.time_quantity += Time(day, TimeUnit.DAY)
        self.time_quantity += Time(hour, TimeUnit.HOUR)
        self.time_quantity += Time(minute, TimeUnit.MINUTE)
        self.time_quantity += Time(second, TimeUnit.SECOND)

    def __str__(self):
        return (
            f"TIMESTAMP_Y{self.year}-"
            + f"M{self.month}-"
            + f"D{self.day}_"
            + f"H{self.hour}:"
            + f"M{self.month}:"
            + f"S{self.second}"
        )

    def __repr__(self):
        return (
            f"TIMESTAMP_Y{self.year}-"
            + f"M{self.month}-"
            + f"D{self.day}_"
            + f"H{self.hour}:"
            + f"M{self.minute}:"
            + f"S{self.second}"
        )

    def __hash__(self):
        return hash(
            f"TIMESTAMP_Y{self.year}-"
            + f"M{self.month}-"
            + f"D{self.day}_"
            + f"H{self.hour}:"
            + f"M{self.minute}:"
            + f"S{self.second}"
        )

    def get_hour_of_day(self, time_passed: Time):
        """
        Returns the hour of day based on the time passed

        Parameters
        ----------
        time_passed : Time
            Time passed

        Returns
        ----------
        hour_of_day : int
            The hour of day based on the time passed

        """
        if not isinstance(time_passed, Time):
            raise Exception("Wrong type")
        dup = Time(time_passed.quantity, time_passed.unit)
        if dup.get_years() > 1:
            y = int(dup.get_years())
            dup -= Time(y, TimeUnit.YEAR)
        if dup.get_months() > 1:
            m = int(dup.get_months())
            dup -= Time(m, TimeUnit.MONTH)
        if dup.get_days() > 1:
            d = int(dup.get_days())
            dup -= Time(d, TimeUnit.DAY)
        dup -= Time(self.hour, TimeUnit.HOUR)
        dup += Time(self.minute, TimeUnit.MINUTE)
        dup += Time(self.second, TimeUnit.SECOND)
        hour_of_day = int(dup.get_hours())
        return hour_of_day

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception("Wrong type")
        return (
            Time(self.year - other.year, TimeUnit.YEAR)
            + Time(self.month - other.month, TimeUnit.MONTH)
            + Time(self.day - other.day, TimeUnit.DAY)
            + Time(self.hour - other.hour, TimeUnit.HOUR)
            + Time(self.minute - other.minute, TimeUnit.MINUTE)
            + Time(self.second - other.second, TimeUnit.SECOND)
        )


if __name__ == "__main__":
    t1 = Time(5, TimeUnit.MINUTE)
    print(t1.get_years())
    print(t1.get_hours())
    t2 = Time(1, TimeUnit.HOUR)
    print(t2.get_years())
    print(t2.get_hours())

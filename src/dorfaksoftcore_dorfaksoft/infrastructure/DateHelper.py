# coding=utf-8
import calendar
import datetime
import math
import time

import jdatetime

from dorfaksoftcore.infrastructure import jalali


class DateHelper:

    @staticmethod
    def getPersianDatetime(dt=None, numerically=False):
        if dt is None:
            dt = datetime.datetime.now()
        pdt = f"{DateHelper.getPersianDate(dt)} {DateHelper.getPersianTime(dt)}"

        return int(pdt.replace("/", "").replace(":", "").replace(" ", "")) if numerically else pdt

    @staticmethod
    def getPersianYear(dt=None):
        date = f"{DateHelper.getPersianDate(dt)}".split("/")[0]
        return date
    @staticmethod
    def getPersianDatetimeFromNumber(number_pdt):
        number_str = str(number_pdt)
        date_part = number_str[:8]
        time_part = number_str[8:]

        year = date_part[:4]
        month = date_part[4:6]
        day = date_part[6:]

        hour = time_part[:2]
        minute = time_part[2:4]
        second = time_part[4:]

        return f"{year}/{month}/{day} {hour}:{minute}:{second}"

    @staticmethod
    def getPersianDatetimeWithMicros(dt=None):
        if dt is None:
            dt = datetime.datetime.now()
        return f"{DateHelper.getPersianDate(dt)} {DateHelper.getPersianTime(dt)}.{dt.microsecond}"

    @staticmethod
    def getPersianDate(dt=None, numerically=False):
        if dt is None:
            dt = datetime.datetime.now()
        if isinstance(dt, datetime.datetime):
            dt = dt.date()
        pdt = jalali.Gregorian(dt).persian_string("{:0>2}/{:0>2}/{:0>2}")
        return int(pdt.replace("/", "")) if numerically else pdt

    @staticmethod
    def getStyledPersianDate(dt=None, dt_format="%N، %d %M %Y"):
        dt_arr = DateHelper.getPersianDate(dt).split("/")
        week_day = DateHelper.getPersianWeekDay(dt)
        week_day_str = DateHelper.getWeekDayString(week_day)
        month_str = DateHelper.getMonthString(dt_arr[1])
        return dt_format.replace("%N", week_day_str).replace("%d", dt_arr[2]).replace("%M", month_str) \
            .replace("%Y", dt_arr[0]).replace("%T", DateHelper.getPersianTime(dt))

    @staticmethod
    def getStyledPersianDateDynamicYear(dt=None, dt_format="%N، %d %B %Y"):
        if not dt:
            dt = datetime.datetime.now()
        dt_arr = DateHelper.getPersianDate(dt).split("/")
        week_day = DateHelper.getPersianWeekDay(dt)
        week_day_str = DateHelper.getWeekDayString(week_day)
        month_str = DateHelper.getMonthString(dt_arr[1])
        y = ""
        py = DateHelper.getPersianDate().split("/")[0]
        if dt_arr[0] != py:
            y = dt_arr[0]
        from dorfaksoftcore.infrastructure.StringHelper import StringHelper
        return dt_format.replace("%N", week_day_str).replace("%d", dt_arr[2]).replace("%B", month_str) \
            .replace("%Y", y).replace("%H", StringHelper.add0(dt.hour)).replace("%M",
                                                                                StringHelper.add0(dt.minute)).replace(
            "%S", StringHelper.add0(dt.second))

    @staticmethod
    def getEnDate(dt=None):
        if dt == None:
            dt = datetime.datetime.now()

        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def getPersianTime(dt=None):
        if dt == None:
            dt = datetime.datetime.now()
        return dt.strftime("%H:%M:%S")

    @staticmethod
    def getPersianTimeFromStrDate(gDateStr):
        dt = datetime.datetime.strptime(gDateStr, "%Y/%m/%d")
        return DateHelper.getPersianDate(dt)

    @staticmethod
    def getPersianDateFromStrDate(gDateStr):
        dt = datetime.datetime.strptime(gDateStr, "%Y/%m/%d")
        return DateHelper.getPersianDate(dt)

    @staticmethod
    def getGregorianTime(dt=None):
        if dt == None:
            dt = datetime.datetime.now()
        return dt.strftime("%H:%M:%S")

    @staticmethod
    def getGregorianDate(dt=None):
        if dt == None:
            dt = datetime.datetime.now()
        return "{:0>2}/{:0>2}/{:0>2}".format(dt.year, dt.month, dt.day)

    @staticmethod
    def toGregorianDateTime(gDateStr, gTimeStr="12:00:00"):
        if '-' in gDateStr:
            gDateStr = gDateStr.replace("-", "/")
        return datetime.datetime.strptime(gDateStr + " " + gTimeStr, "%Y/%m/%d %H:%M:%S")

    @staticmethod
    def toDateTime(pDateStr, pTimeStr="12:00:00"):
        if " " in pDateStr:
            pTimeStr = pDateStr.split(" ")[1]
            pDateStr = pDateStr.split(" ")[0]

        d = list(map(int, pDateStr.split("/")))
        t = list(map(int, pTimeStr.split(":")))
        return jdatetime.datetime(d[0], d[1], d[2], t[0], t[1], t[2], 0).togregorian()

    @staticmethod
    def isoToDateTime(isoDateTimeStr):
        pDateStr = isoDateTimeStr.split("T")[0].replace("-", "/")
        pTimeStr = isoDateTimeStr.split("T")[1]
        pTimeStr = pTimeStr.split(".")[0]
        return DateHelper.toGregorianDateTime(pDateStr, pTimeStr)

    @staticmethod
    def dateDiffInMinute(startDate, endDate):
        diffTime = (endDate - startDate).total_seconds()
        return int((diffTime / (60)))

    @staticmethod
    def dateDiffInDay(startDate, endDate):
        diffTime = (endDate - startDate).total_seconds()
        return int((diffTime / (60 * 60 * 24)))

    @staticmethod
    def toStyledDateTimeString(date=None):
        dateToday = datetime.datetime.now()
        diffMin = DateHelper.dateDiffInMinute(date, dateToday)
        diffHour = int(diffMin / 60)

        if (diffHour < 24):
            if (diffMin == 0):
                return " لحظاتی پیش "
            elif (diffMin < 15):
                return str(diffMin) + " دقیقه پیش "
            else:

                if (diffMin >= 15 and diffMin < 30):
                    return " یک ربع پیش "

                elif (diffMin >= 30 and diffMin < 60):
                    return " نیم ساعت پیش"

                else:
                    h = int(math.floor(diffMin / 60))
                    return str(h) + " ساعت پیش"
        else:
            diffDay = int(diffHour / 24)
            if diffDay == 1 and (dateToday.day - 1) == date.day:
                return "دیروز"
            elif (diffDay == 2 and (dateToday.day - 2) == date.day):
                return "پریروز"
            elif (diffDay > 0 and diffDay < 7):
                return str(diffDay) + "  روز پیش"

            elif (diffDay >= 7 and diffDay < 14):
                return " ۱ هفته پیش"

            elif (diffDay >= 14 and diffDay < 21):
                return " ۲ هفته پیش"

            elif (diffDay >= 21 and diffDay < 28):
                return " ۳ هفته پیش"

            elif (diffDay >= 28 and diffDay < 31):
                return " ۴ هفته پیش"

            else:
                m = int(math.floor(diffDay / 30))
                if (m <= 12):
                    return str(m) + " ماه پیش"
                else:
                    y = int(math.floor(m / 12))
                    return str(y) + " سال پیش"

    @staticmethod
    def getMonthString(monthNum):
        monthNum = int(monthNum)
        if monthNum == 1:
            return "فروردین"
        elif monthNum == 2:
            return "اردیبهشت"
        elif monthNum == 3:
            return "خرداد"
        elif monthNum == 4:
            return "تیر"
        elif monthNum == 5:
            return "مرداد"
        elif monthNum == 6:
            return "شهریور"
        elif monthNum == 7:
            return "مهر"
        elif monthNum == 8:
            return "آبان"
        elif monthNum == 9:
            return "آذر"
        elif monthNum == 10:
            return "دی"
        elif monthNum == 11:
            return "بهمن"
        elif monthNum == 12:
            return "اسفند"
        else:
            return " "

    @staticmethod
    def getWeekDayString(weekDay):
        if weekDay == 0:
            return "شنبه"
        elif weekDay == 1:
            return "یک شنبه"
        elif weekDay == 2:
            return "دوشنبه"
        elif weekDay == 3:
            return "سه شنبه"
        elif weekDay == 4:
            return "چهارشنبه"
        elif weekDay == 5:
            return "پنج شنبه"
        elif weekDay == 6:
            return "جمعه"
        else:
            return ""

    @staticmethod
    def getPersianWeekDay(dt=None):
        if dt is None:
            dt = datetime.datetime.now()

        return (dt.weekday() + 2) % 7

    @staticmethod
    def validate(persian_date_str):
        if len(persian_date_str) != 10:
            return False

        arr = persian_date_str.split("/")

        if len(arr) != 3 or len(arr[0]) != 4 or len(arr[1]) != 2 or len(arr[2]) != 2:
            return False

        return True

    @staticmethod
    def gregorianDaterange(start_date, end_date):
        for n in range(int((end_date - start_date).days + 1)):
            yield start_date + datetime.timedelta(n)

    @staticmethod
    def persianDaterange(start_date, end_date):
        for dt in DateHelper.gregorianDaterange(DateHelper.toDateTime(start_date, "00:00:00"),
                                                DateHelper.toDateTime(end_date, "00:00:00")):
            yield DateHelper.getPersianDate(dt)

    @staticmethod
    def utcDatetimeToLocalDatetime(utcDatetime, TIME_FORMAT='%Y-%m-%d %H:%M:%S'):
        is_utc = False
        if isinstance(utcDatetime, datetime.datetime):
            utc = utcDatetime.strftime(TIME_FORMAT)
        else:
            is_utc = "+00:00" in utcDatetime or "Z" in utcDatetime
            if "+" in utcDatetime:
                utcDatetime = utcDatetime.split("+")[0]
            if "T" in utcDatetime:
                utcDatetime = utcDatetime.replace("T", " ")
            if "." in utcDatetime:
                utcDatetime = utcDatetime.split(".")[0]

            utc = utcDatetime
        if is_utc:
            utc = utc.replace("Z", "")
            timestamp = calendar.timegm((datetime.datetime.strptime(utc, TIME_FORMAT)).timetuple())
            local = datetime.datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
        else:
            local = datetime.datetime.strptime(utc, TIME_FORMAT)
        return local

    @staticmethod
    def localDatetimeToUtc(localDatetime):
        TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        local = localDatetime.strftime(TIME_FORMAT)
        timestamp = str(time.mktime(datetime.datetime.strptime(local, TIME_FORMAT).timetuple()))[:-2]
        utc = datetime.datetime.utcfromtimestamp(int(timestamp))
        return utc

    @staticmethod
    def toStyledString(year=0, month=0, day=0, hour=0, minute=0, second=0):
        week = 0
        if second > 60:
            minute = second // 60
            second = second % 60
        if minute > 60:
            hour = minute // 60
            minute = minute % 60
        if hour > 24:
            day = hour // 24
            hour = hour % 24
        if day > 365:
            year = day // 365
            day = day % 365
        elif day >= 30:
            month = day // 30
            day = day % 30
        elif day < 30:
            week = day // 7
            day = day % 7
        res = []
        if year > 0:
            res.append(f"{year} سال")
        if month > 0:
            res.append(f"{month} ماه")
        if week > 0:
            res.append(f"{week} هفته")
        if day > 0:
            res.append(f"{day} روز")
        if minute > 0:
            res.append(f"{minute} دقیقه")
        if hour > 0:
            res.append(f"{hour} ساعت")
        if second > 0:
            res.append(f"{second} ثانیه")
        return " و ".join(res)

    @staticmethod
    def parseSecond(seconds):
        td = datetime.timedelta(seconds=seconds)
        total_seconds = td.total_seconds()
        centuries, seconds = divmod(total_seconds, 60 * 60 * 24 * 365.25 * 100)
        years, seconds = divmod(seconds, 60 * 60 * 24 * 365.25)
        months, seconds = divmod(seconds, 60 * 60 * 24 * 30)
        days, seconds = divmod(seconds, 60 * 60 * 24)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return int(centuries), int(years), int(months), int(days), int(hours), int(minutes), int(seconds)

    @staticmethod
    def formatNumericallyDate(nummericallyDate):
        dt = str(nummericallyDate)
        return f"{dt[:4]}/{dt[4:6]}/{dt[6:8]}"

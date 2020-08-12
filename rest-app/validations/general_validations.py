from utils import (
    NATIONAL_HOLIDAYS,
    FLEXIBLE_HOLIDAY_DATES,
    CURRENT_YEAR,
    retrieve_flexible_holiday_date
)


def validate_annual_holiday(holiday_date: str):
    holiday_date = holiday_date.split('-', 1)[1]
    holiday_name = NATIONAL_HOLIDAYS.get(holiday_date)

    return holiday_name


def validate_flexible_holiday(holiday_date: str):
    holiday_name = None
    holiday_date_splitted = holiday_date.split('-')
    if holiday_date_splitted[0] != CURRENT_YEAR:
        flexible_holiday_dates = retrieve_flexible_holiday_date(choosen_year=int(holiday_date_splitted[0]))
        for key, value in flexible_holiday_dates.items():
            if holiday_date == value:
                holiday_name = key
    else:
        for key, value in FLEXIBLE_HOLIDAY_DATES.items():
            if holiday_date == value:
                holiday_name = key

    return holiday_name

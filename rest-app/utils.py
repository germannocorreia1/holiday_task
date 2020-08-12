from datetime import datetime
from sqlite3 import Connection

NATIONAL_HOLIDAYS = {
    "01-01": "Ano Novo",
    "04-21": "Tiradentes",
    "05-01": "Dia do Trabalhador",
    "09-07": "Independência",
    "10-12": "Nossa Senhora Aparecida",
    "11-02": "Finados",
    "11-15": "Proclamação da República",
    "12-25": "Natal"
}


FLEXIBLE_HOLIDAY_DATES = {
    "carnaval": "",
    "corpus-christi": "",
    "sexta-feira-santa": ""
}

FLEXIBLE_HOLIDAYS_RESPONSE = {
    "carnaval": "Carnaval",
    "corpus-christi": "Corpus Christi",
    "sexta-feira-santa": "Sexta-Feira Santa"
}

CURRENT_YEAR = datetime.now().year


def map_holiday_date_format(holiday_day: int, holiday_month: int):
    holiday_day_as_string = str(holiday_day)
    holiday_month_as_string = str(holiday_month)

    if len(holiday_day_as_string) < 2:
        holiday_day_as_string = f"0{holiday_day_as_string}"

    if len(holiday_month_as_string) < 2:
        holiday_month_as_string = f"0{holiday_month_as_string}"

    return holiday_day_as_string, holiday_month_as_string


def validate_bissextile_year(current_year: int):
    if (current_year % 100 != 0 and current_year % 4 == 0) or (current_year % 400 == 0):
        return True
    else:
        return False


def retrieve_flexible_holiday_date(choosen_year: int = None):
    if choosen_year:
        bissextile_year = validate_bissextile_year(choosen_year)
        easter_day, easter_month = retrieve_easter_holiday_date(choosen_year)
        flexible_holidays_dictionary = {}
    else:
        bissextile_year = validate_bissextile_year(int(CURRENT_YEAR))
        easter_day, easter_month = retrieve_easter_holiday_date(CURRENT_YEAR)

    parsed_easter_day, parsed_easter_month = map_holiday_date_format(easter_day, easter_month)

    easter_date_without_year = f"{parsed_easter_month}-{parsed_easter_day}"
    if not choosen_year:
        NATIONAL_HOLIDAYS[easter_date_without_year] = "Páscoa"

    if parsed_easter_month == '03':
        month_days_left = 31 - easter_day
        carnaval_day = 47 - easter_day
        corpus_christi_day = 60 - (month_days_left + 30)
        parsed_corpus_christi_day, parsed_corpus_christi_month = map_holiday_date_format(corpus_christi_day, 5)

        if choosen_year:
            flexible_holidays_dictionary["corpus-christi"] = f"{choosen_year}-" \
                                                             f"{parsed_easter_month}-" \
                                                             f"{parsed_corpus_christi_day}"
        else:
            FLEXIBLE_HOLIDAY_DATES["corpus-christi"] = f"{choosen_year}-" \
                                                  f"{parsed_easter_month}-" \
                                                  f"{parsed_corpus_christi_day}"

        if bissextile_year:
            if carnaval_day > 29:
                carnaval_day = carnaval_day - 29
                carnaval_day = 31 - carnaval_day
                parsed_carnaval_day, parsed_carnaval_month = map_holiday_date_format(carnaval_day, 1)
                if choosen_year:
                    flexible_holidays_dictionary["carnaval"] = f"{choosen_year}-" \
                                                               f"{parsed_carnaval_month}-" \
                                                               f"{parsed_carnaval_day}"
                else:
                    FLEXIBLE_HOLIDAY_DATES["carnaval"] = f"{CURRENT_YEAR}-" \
                                                    f"{parsed_carnaval_month}-" \
                                                    f"{parsed_carnaval_day}"
            else:
                carnaval_day = 29 - carnaval_day
                parsed_carnaval_day, parsed_carnaval_month = map_holiday_date_format(carnaval_day, 2)
                if choosen_year:
                    flexible_holidays_dictionary["carnaval"] = f"{choosen_year}-" \
                                                               f"{parsed_carnaval_month}-" \
                                                               f"{parsed_carnaval_day}"
                else:
                    FLEXIBLE_HOLIDAY_DATES["carnaval"] = f"{CURRENT_YEAR}-" \
                                                    f"{parsed_carnaval_month}-" \
                                                    f"{parsed_carnaval_day}"
        else:
            if carnaval_day > 28:
                carnaval_day = carnaval_day - 28
                carnaval_day = 31 - carnaval_day
                parsed_carnaval_day, parsed_carnaval_month = map_holiday_date_format(carnaval_day, 1)

                if choosen_year:
                    flexible_holidays_dictionary["carnaval"] = f"{choosen_year}-" \
                                                               f"{parsed_carnaval_month}-" \
                                                               f"{parsed_carnaval_day}"
                else:
                    FLEXIBLE_HOLIDAY_DATES["carnaval"] = f"{CURRENT_YEAR}-" \
                                                    f"{parsed_carnaval_month}-" \
                                                    f"{parsed_carnaval_day}"
            else:
                carnaval_day = 28 - carnaval_day
                parsed_carnaval_day, parsed_carnaval_month = map_holiday_date_format(carnaval_day, 2)

                if choosen_year:
                    flexible_holidays_dictionary["carnaval"] = f"{choosen_year}-" \
                                                               f"{parsed_carnaval_month}-" \
                                                               f"{parsed_carnaval_day}"
                else:
                    FLEXIBLE_HOLIDAY_DATES["carnaval"] = f"{CURRENT_YEAR}-" \
                                                    f"{parsed_carnaval_month}-" \
                                                    f"{parsed_carnaval_day}"
    elif parsed_easter_month == '04':
        month_days_left = 30 - easter_day
        carnaval_day = 47 - easter_day
        corpus_christi_day = 60 - (month_days_left + 31)
        parsed_corpus_christi_day, parsed_corpus_christi_month = map_holiday_date_format(corpus_christi_day, 6)

        if choosen_year:
            flexible_holidays_dictionary["corpus-christi"] = f"{choosen_year}-" \
                                                             f"{parsed_corpus_christi_month}-" \
                                                             f"{parsed_corpus_christi_day}"
        else:
            FLEXIBLE_HOLIDAY_DATES["corpus-christi"] = f"{CURRENT_YEAR}-" \
                                                  f"{parsed_corpus_christi_month}-" \
                                                  f"{parsed_corpus_christi_day}"

        if bissextile_year:
            if carnaval_day > 31:
                carnaval_day = carnaval_day - 31
                carnaval_day = 29 - carnaval_day
                parsed_carnaval_day, parsed_carnaval_month = map_holiday_date_format(carnaval_day, 2)

                if choosen_year:
                    flexible_holidays_dictionary["carnaval"] = f"{choosen_year}-" \
                                                               f"{parsed_carnaval_month}-" \
                                                               f"{parsed_carnaval_day}"
                else:
                    FLEXIBLE_HOLIDAY_DATES["carnaval"] = f"{CURRENT_YEAR}-" \
                                                    f"{parsed_carnaval_month}-" \
                                                    f"{parsed_carnaval_day}"
            else:
                carnaval_day = 31 - carnaval_day
                parsed_carnaval_day, parsed_carnaval_month = map_holiday_date_format(carnaval_day, 3)
                if choosen_year:
                    flexible_holidays_dictionary["carnaval"] = f"{choosen_year}-" \
                                                               f"{parsed_carnaval_month}-" \
                                                               f"{parsed_carnaval_day}"
                else:
                    FLEXIBLE_HOLIDAY_DATES["carnaval"] = f"{CURRENT_YEAR}-" \
                                                    f"{parsed_carnaval_month}-" \
                                                    f"{parsed_carnaval_day}"
        else:
            if carnaval_day > 31:
                carnaval_day = carnaval_day - 31
                carnaval_day = 28 - carnaval_day
                parsed_carnaval_day, parsed_carnaval_month = map_holiday_date_format(carnaval_day, 2)
                if choosen_year:
                    flexible_holidays_dictionary["carnaval"] = f"{choosen_year}-" \
                                                               f"{parsed_carnaval_month}-" \
                                                               f"{parsed_carnaval_day}"
                else:
                        FLEXIBLE_HOLIDAY_DATES["carnaval"] = f"{CURRENT_YEAR}-" \
                                                        f"{parsed_carnaval_month}-" \
                                                        f"{parsed_carnaval_day}"
            else:
                carnaval_day = 31 - carnaval_day
                parsed_carnaval_day, parsed_carnaval_month = map_holiday_date_format(carnaval_day, 3)
                if choosen_year:
                    flexible_holidays_dictionary["carnaval"] = f"{choosen_year}-" \
                                                               f"{parsed_carnaval_month}-" \
                                                               f"{parsed_carnaval_day}"
                else:
                    FLEXIBLE_HOLIDAY_DATES["carnaval"] = f"{CURRENT_YEAR}-" \
                                                    f"{parsed_carnaval_month}-" \
                                                    f"{parsed_carnaval_day}"

    # TODO: Adicionar validação para quando o dia da pascoa for 2 ou menor
    if choosen_year:
        flexible_holidays_dictionary["sexta-feira-santa"] = f"{choosen_year}-{parsed_easter_month}-{easter_day - 2}"
        return flexible_holidays_dictionary
    else:
        FLEXIBLE_HOLIDAY_DATES["sexta-feira-santa"] = f"{CURRENT_YEAR}-{parsed_easter_month}-{easter_day - 2}"

    return

def retrieve_easter_holiday_date(current_year: int):
    a = current_year % 19
    b = int(current_year / 100)
    c = current_year % 100
    d = int(b / 4)
    e = b % 4
    f = (int (b + 8) / 25)
    g = (int (b - f + 1) / 3)
    h = (19 * a + b - d - g + 15) % 30
    i = int( c / 4)
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = int( (a + 11 * h + 22 * l) / 451)

    easter_month = int((h + l - 7 * m + 114) / 31)
    easter_day = int(1 + (h + l - 7 * m + 114 ) % 31)

    return easter_day, easter_month


def close_session(database_session: Connection):
    database_session.close()
    return

from api_errors import IncorrectDateValue, IncorrectRequestFormat, IncorrectLocalityIdentifier


def validate_date_parameter_structure_for_get(holiday_date: str):

    try:
        holiday_date_splitted = holiday_date.split("-")
        year = holiday_date_splitted[0]
        month = holiday_date_splitted[1]
        day = holiday_date_splitted[2]
    except IndexError as exception:
        raise IncorrectDateValue
    if len(year) != 4:
        raise IncorrectDateValue()
    if len(month) != 2:
        raise IncorrectDateValue()
    if len(day) != 2:
        raise IncorrectDateValue()

    year = int(year)
    month = int(month)
    day = int(day)

    if month > 12 or month < 0:
        raise IncorrectDateValue()
    if day < 0 or day > 31:
        raise IncorrectDateValue()
    if year < 0:
        raise IncorrectDateValue()


def validate_date_parameter_structure_without_year(holiday_date: str):
    try:
        holiday_date_splitted = holiday_date.split("-")
        month = holiday_date_splitted[0]
        day = holiday_date_splitted[1]
    except IndexError as exception:
        raise IncorrectDateValue()
    if len(month) != 2:
        raise IncorrectDateValue()
    if len(day) != 2:
        raise IncorrectDateValue()


def validate_request_body(request_body: dict):
    holiday_name = request_body.get("name")

    if not holiday_name or not isinstance(holiday_name, str):
        raise IncorrectRequestFormat()


def validate_ibge_code(ibge_code: str, database_session):
    if len(ibge_code) != 2 and len(ibge_code) != 7:
        raise IncorrectLocalityIdentifier()

    # if len(ibge_code) == 7:
    #     retrieved_location = retrieve_ibge_code(ibge_code=int(ibge_code), database_session=database_session)
    #
    #     if not retrieved_location:
    #         raise IncorrectLocalityIdentifier()

#
# def retrieve_ibge_code(ibge_code: int, database_session):
#     retrieved_location = database_session.query(LocationModel).filter(
#         LocationModel.ibge_code == ibge_code
#     )
#
#     return retrieved_location

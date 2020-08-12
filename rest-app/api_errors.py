class IncorrectDateValue(Exception):
    pass


class IncorrectLocalityIdentifier(Exception):
    pass


class HolidayNotFound(Exception):
    pass


class IncorrectRequestFormat(Exception):
    pass


class NationalHolidayCannotBeRemoved(Exception):
    pass


class StateHolidayCannotBeRemovedFromCounty(Exception):
    pass


class HolidayAlreadyExists(Exception):
    pass


class InternalConnectionError(Exception):
    pass


ERRORS = {
    'IncorrectDateValue': {
        'message': "Invalid date format. Please enter a correct value in the format YYYY-MM-DD.",
        'status': 400
    },
    'IncorrectLocalityIdentifier': {
        'message': "Invalid locality identifier format. Please enter a correct value with two or seven digits.",
        'status': 400
    },
    'IncorrectRequestFormat': {
        'message': "Wrong request body format. Please enter the correct fields and field types.",
        'status': 400
    },
    'HolidayNotFound': {
        'message': "There is no registered holiday on this date.",
        'status': 404
    },
    'NationalHolidayCannotBeRemoved': {
        'message': "National holidays cannot be removed.",
        'status': 403
    },
    'StateHolidayCannotBeRemovedFromCounty': {
        'message': "State holidays cannot be removed from county.",
        'status': 403
    },
    'HolidayAlreadyExists': {
        'message': "This holiday already exists in that municipality / state.",
        'status': 403
    },
    'InternalConnectionError': {
        'message': "Some internal error has occurred. Please try again.",
        'status': 500
    }
}
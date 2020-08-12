import json
from datetime import datetime

from flask import make_response

from utils import CURRENT_YEAR


def map_get_response(holiday_name: str):
    resp = {
        "name": holiday_name
    }
    response = make_response(json.dumps(resp), 200)
    return response


def add_year_to_holiday_field(holiday_date: str):
    current_year = str(CURRENT_YEAR)
    mapped_date = f'{current_year}-' + holiday_date
    return mapped_date

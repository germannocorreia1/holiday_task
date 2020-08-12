import json

from flask import Flask, request, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from validations.request_structure_validation import (
    validate_date_parameter_structure_for_get,
    validate_date_parameter_structure_without_year,
    validate_request_body,
    validate_ibge_code
)
from persistency.database_connection import create_connection_with_db, commit_and_close_database_session
from api_errors import (
    ERRORS,
    HolidayNotFound,
    NationalHolidayCannotBeRemoved,
    StateHolidayCannotBeRemovedFromCounty
)
from mappers.general_mappers import (
    map_get_response,
    add_year_to_holiday_field
)
from validations.general_validations import (
    validate_annual_holiday,
    validate_flexible_holiday
)
from utils import (
    retrieve_flexible_holiday_date,
    FLEXIBLE_HOLIDAY_DATES,
    NATIONAL_HOLIDAYS,
    FLEXIBLE_HOLIDAYS_RESPONSE,
    close_session
)


DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/holidays_task"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
database = SQLAlchemy(app)
migrate = Migrate(app, database)
api = Api(app, errors=ERRORS)


class LocationModel(database.Model):
    __tablename__ = 'location'

    ibge_code = database.Column('ibge_code', database.Integer, primary_key=True)
    location_name = database.Column('location_name', database.String())

    def __init__(self, ibge_code, location_name):
        self.ibge_code = ibge_code
        self.location_name = location_name


class HolidayModel(database.Model):
    __tablename__ = 'holidays'

    holiday_id = database.Column('holiday_id', database.Integer, primary_key=True)
    ibge_code = database.Column('ibge_code', database.Integer)
    holiday_name = database.Column('holiday_name', database.String())
    holiday_date = database.Column('holiday_date', database.String())

    def __init__(self, ibge_code, holiday_name, holiday_date):
        self.ibge_code = ibge_code
        self.holiday_name = holiday_name
        self.holiday_date = holiday_date


class Holidays(Resource):
    def get(self, ibge_code, holiday):
        database_session = create_connection_with_db(database)
        validate_ibge_code(ibge_code=ibge_code, database_session=database_session)
        validate_date_parameter_structure_for_get(holiday_date=holiday)
        holiday_name = validate_annual_holiday(holiday_date=holiday)

        if holiday_name:
            return map_get_response(holiday_name=holiday_name)

        holiday_name = validate_flexible_holiday(holiday_date=holiday)

        if holiday_name:
            holiday_name_to_response = FLEXIBLE_HOLIDAYS_RESPONSE.get(holiday_name)
            return map_get_response(holiday_name=holiday_name_to_response)

        retrieved_holiday_name = retrieve_holiday_name(ibge_code=ibge_code,
                                                       holiday_date=holiday,
                                                       database_session=database_session)

        if retrieved_holiday_name:
            resp = {
                'name': retrieved_holiday_name
            }

            response = make_response(json.dumps(resp), 200)
            return response
        elif len(ibge_code) == 7:
            ibge_state_code = ibge_code[:2]
            retrieved_state_holiday = retrieve_holiday_name(ibge_code=ibge_state_code,
                                                            holiday_date=holiday,
                                                            database_session=database_session)

            if retrieved_state_holiday:
                resp = {
                    'name': retrieved_state_holiday
                }

                response = make_response(json.dumps(resp), 200)
                return response
            else:
                raise HolidayNotFound
        else:
            raise HolidayNotFound

    def put(self, ibge_code, holiday):
        database_session = create_connection_with_db(database=database)

        validate_ibge_code(ibge_code=ibge_code, database_session=database_session)

        if holiday in FLEXIBLE_HOLIDAY_DATES.keys():
            if FLEXIBLE_HOLIDAY_DATES[holiday] != "":
                holiday_date = FLEXIBLE_HOLIDAY_DATES[holiday]
            else:
                retrieve_flexible_holiday_date()
                holiday_date = FLEXIBLE_HOLIDAY_DATES[holiday]

            retrieved_holiday = retrieve_holiday(ibge_code=ibge_code,
                                                 holiday_date=holiday_date,
                                                 database_session=database_session)

            if retrieved_holiday:
                update_holiday(holiday_name=holiday,
                               retrieved_holiday=retrieved_holiday,
                               database_session=database_session)

                resp = {
                    "name": holiday
                }

                response = make_response(json.dumps(resp), 200)
                return response

            if holiday == "carnaval":

                create_holiday(ibge_code=ibge_code,
                               holiday_date=holiday_date,
                               holiday_name=holiday,
                               database_session=database_session)

                splitted_date = holiday_date.split('-')
                carnaval_monday = int(splitted_date[2]) - 1
                splitted_date[2] = str(carnaval_monday)
                holiday_date = '-'.join(splitted_date)

                create_holiday(ibge_code=ibge_code,
                               holiday_date=holiday_date,
                               holiday_name=holiday,
                               database_session=database_session)
            else:
                create_holiday(ibge_code=ibge_code,
                               holiday_date=holiday_date,
                               holiday_name=holiday,
                               database_session=database_session)

            holiday_name_to_response = FLEXIBLE_HOLIDAYS_RESPONSE.get(holiday)

            resp = {
                "name": holiday_name_to_response
            }

            close_session(database_session=database_session)

            response = make_response(json.dumps(resp), 201)
            return response

        else:

            validate_date_parameter_structure_without_year(holiday_date=holiday)

            request_body = json.loads(request.data)
            validate_request_body(request_body=request_body)

            request_date = add_year_to_holiday_field(holiday_date=holiday)
            holiday_name = request_body.get('name')

            retrieved_holiday = retrieve_holiday(ibge_code=ibge_code,
                                                 holiday_date=request_date,
                                                 database_session=database_session)

            if retrieved_holiday:
                update_holiday(holiday_name=holiday_name,
                               retrieved_holiday=retrieved_holiday,
                               database_session=database_session)

                resp = {
                    "name": holiday_name
                }

                response = make_response(json.dumps(resp), 200)
                return response

            else:
                create_holiday(ibge_code=ibge_code,
                               holiday_date=request_date,
                               holiday_name=holiday_name,
                               database_session=database_session)

                resp = {
                    "name": holiday_name
                }

                response = make_response(json.dumps(resp), 201)
                return response

    def delete(self, ibge_code, holiday):
        database_session = create_connection_with_db(database=database)

        validate_ibge_code(ibge_code=ibge_code, database_session=database_session)

        if holiday in FLEXIBLE_HOLIDAY_DATES.keys():
            if FLEXIBLE_HOLIDAY_DATES[holiday] != "":
                holiday_date = FLEXIBLE_HOLIDAY_DATES[holiday]
            else:
                retrieve_flexible_holiday_date()
                holiday_date = FLEXIBLE_HOLIDAY_DATES[holiday]

            retrieved_holiday = retrieve_holiday(ibge_code=ibge_code,
                                                 holiday_date=holiday_date,
                                                 database_session=database_session)

            if retrieved_holiday:
                delete_holiday(ibge_code=ibge_code,
                               holiday_date=holiday_date,
                               database_session=database_session)
            else:
                raise HolidayNotFound()

            response = make_response({}, 204)
            return response
        else:
            validate_date_parameter_structure_without_year(holiday_date=holiday)
            holiday_name = NATIONAL_HOLIDAYS.get(holiday)

            if holiday_name:
                raise NationalHolidayCannotBeRemoved

            request_date = add_year_to_holiday_field(holiday_date=holiday)

            if len(ibge_code) == 7:
                ibge_state_code = ibge_code[:2]
                retrieved_state_holiday = retrieve_holiday(ibge_code=ibge_state_code,
                                                           holiday_date=request_date,
                                                           database_session=database_session)

                if retrieved_state_holiday:
                    raise StateHolidayCannotBeRemovedFromCounty

            retrieved_holiday = retrieve_holiday(ibge_code=ibge_code,
                                                 holiday_date=request_date,
                                                 database_session=database_session)

            if retrieved_holiday:
                delete_holiday(ibge_code=ibge_code,
                               holiday_date=request_date,
                               database_session=database_session)
            else:
                raise HolidayNotFound()

            response = make_response({}, 204)
            return response


def retrieve_holiday_name(ibge_code: int, holiday_date: str, database_session):
    retrieved_model = database_session.query(HolidayModel).filter(
        HolidayModel.holiday_date == holiday_date,
        HolidayModel.ibge_code == ibge_code
    ).first()

    database_session.close()

    if retrieved_model:
        return retrieved_model.holiday_name
    else:
        return None


def retrieve_holiday(ibge_code: int, holiday_date: str, database_session):
    retrieved_model = database_session.query(HolidayModel).filter(
        HolidayModel.holiday_date == holiday_date,
        HolidayModel.ibge_code == ibge_code
    ).first()

    if retrieved_model:
        return retrieved_model
    else:
        return None


def delete_holiday(ibge_code: int, holiday_date: str, database_session):
    database_session.query(HolidayModel).filter(
        HolidayModel.holiday_date == holiday_date,
        HolidayModel.ibge_code == ibge_code
    ).delete()

    commit_and_close_database_session(database_session=database_session)

    return


def update_holiday(
        holiday_name: str,
        retrieved_holiday: HolidayModel,
        database_session
):
    retrieved_holiday.holiday_name = holiday_name
    updated_holiday = database_session.add(retrieved_holiday)

    commit_and_close_database_session(database_session=database_session)

    return updated_holiday


def create_holiday(ibge_code: int, holiday_date: str, holiday_name: str, database_session):
    model_to_be_created = HolidayModel(
        ibge_code=ibge_code,
        holiday_date=holiday_date,
        holiday_name=holiday_name
    )

    created_model = database_session.add(model_to_be_created)

    commit_and_close_database_session(database_session=database_session)

    return created_model


api.add_resource(Holidays, '/feriados/<string:ibge_code>/<string:holiday>/')

if __name__ == '__main__':
    retrieve_flexible_holiday_date()
    app.run()

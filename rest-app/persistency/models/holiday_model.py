from flask_sqlalchemy import Model
from sqlalchemy import Column, Integer, String, ForeignKey

from persistency.models.location_model import LocationModel


class HolidayModel(Model):
    __tablename__ = 'holidays'

    ibge_code = Column('ibge_code', Integer, ForeignKey(LocationModel.ibge_code))
    holiday_name = Column('holiday_name', String())
    holiday_date = Column('holiday_date', String())

    def __init__(self, ibge_code, holiday_name, holiday_date):
        self.ibge_code = ibge_code
        self.holiday_name = holiday_name
        self.holiday_date = holiday_date

from flask_sqlalchemy import Model
from sqlalchemy import Column, Integer, String


class LocationModel(Model):
    __tablename__ = 'location'

    ibge_code = Column('ibge_code', Integer, primary_key=True)
    location_name = Column('location_name', String())

    def __init__(self, ibge_code, location_name):
        self.ibge_code = ibge_code
        self.location_name = location_name

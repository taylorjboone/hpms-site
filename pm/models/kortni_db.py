from distutils.log import error
from sqlalchemy import Float, create_engine, text, orm, MetaData, Table, Column, Integer, String, ForeignKey, Date
from flask_sqlalchemy import SQLAlchemy
from pm import db,app
from wvdot_utils import check_seg_valid
import pandas as pd
import os
import json
import datetime


user_dir = os.path.expanduser('~')
engine = create_engine(f'sqlite+pysqlite:///{user_dir}\Documents\GitHub\hpms-site\database.db', echo=True, future=True)
activity_codes = pd.read_csv(f'{user_dir}/Documents/GitHub/hpms-site/pm/static/activity_codes.csv')

with open(f'{user_dir}/Documents/GitHub/hpms-site/pm/static/org_nums.json', 'r') as f:
    org_nums = json.loads(f.read())


metadata_obj = MetaData()

mapper_registry = orm.registry()
Base = mapper_registry.generate_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    route_id = Column(String)
    bmp = Column(Float)
    emp = Column(Float)
    org_num = Column(String(4))
    project_name = Column(String)
    activity_code = Column(String)
    activity_description = Column(String)
    route_name = Column(String)
    accomplishments = Column(Float)
    units = Column(String)
    crew_members = Column(Integer)
    travel_hours = Column(Float)
    onsite_hours = Column(Float)
    task_date = Column(Date)
    notes = Column(String)

    created_by = Column(String)
    created_date = Column(Date)
    updated_by = Column(String)
    updated_date = Column(Date)


    def validate1(self):
        print(self)
        return '',True

    def validate(self):
        error_list = []

        er0,bv0 = self.validate_geom()
        error_list += [er0]
        er1,bv1 = self.validate_org()
        error_list += [er1]
        er2,bv2 = self.validate_activity()
        error_list += [er2]
        er3,bv3 = self.validate_project_name()
        error_list += [er3]
        er4,bv4 = self.validate_accomplishments()
        error_list += [er4]
        er5,bv5 = self.validate_crew_members()
        error_list += [er5]
        er6,bv6 = self.validate_travel_hours()
        error_list += [er6]
        er7,bv7 = self.validate_onsite_hours()
        error_list += [er7]
        er8,bv8 = self.validate_task_date()
        error_list += [er8]

        return len(error_list)==0,error_list




        

    def validate_geom(self):
        corrected_segs,message,bv = check_seg_valid(self.route_id, self.bmp, self.emp)
        print(corrected_segs)
        if not bv and len(message) == 0:
            message = f'corrected segs are: {corrected_segs}'
        elif bv and len(message) > 0: 
            return message,bv 
        return message,bv

    def validate_org(self):
        # TODO populate org dict
        if not self.org_num in org_nums.keys():
            return f'Org Number: {self.org_num} not recognized',False
        return '',True

    def validate_activity(self):
        if not self.activity_code in activity_codes['Activity Code']:
            return f'Activity Code: {self.activity_code} not recognized',False
        return '',True

    def validate_project_name(self):
        if self.project_name == None or len(self.project_name) == 0:
            return f'Project name is empty',False
        return '',True

    def validate_accomplishments(self):
        if self.accomplishments == None:
            return 'Accomplishments field was left blank',False
        return '',True

    def validate_crew_members(self):
        if self.crew_members == None:
            return 'Crew members field was left blank',False
        return '',True

    def validate_travel_hours(self):
        if self.travel_hours == None:
            return 'Travel hours field was left blank',False
        return '',True
    
    def validate_onsite_hours(self):
        if self.onsite_hours == None:
            return 'Onsite hours field was left blank',False
        return '',True

    def validate_task_date(self):
        if not type(self.task_date) == datetime.date or not type(self.task_date) == datetime.datetime or self.task_date < datetime.date.today():
            return 'Task Date not valid',False
        return '',True

    def add_task(self):
        pass

    



    



# metadata_obj.create_all(engine)
# mapper_registry.metadata.create_all(engine)
# Base.metadata.create_all(engine)



t = Task()
print(t.validate())

# with app.app_context():

#     db.session.add(t)

#     db.session.commit()


from distutils.log import error
from dateutil import parser
from sqlalchemy import Float, create_engine, text, orm, MetaData, Table, Column, Integer, String, ForeignKey, Date, and_, or_, Boolean
from flask_sqlalchemy import SQLAlchemy
from wvdot_utils import check_seg_valid
import pandas as pd
import os
import json
import datetime


user_dir = os.path.expanduser('~')
db = create_engine(f'sqlite+pysqlite:///{user_dir}\Documents\GitHub\hpms-site\database.db', echo=True, future=True)
activity_codes = pd.read_csv(f'{user_dir}/Documents/GitHub/hpms-site/pm/static/activity_codes.csv')
activity_codes['Activity Code'] = activity_codes['Activity Code'].astype(int)

with open(f'{user_dir}/Documents/GitHub/hpms-site/pm/static/org_nums.json', 'r') as f:
    org_nums = json.loads(f.read())


metadata_obj = MetaData()

mapper_registry = orm.registry()
Base = mapper_registry.generate_base()
session = orm.Session(db)
LIMIT = 1000


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    route_id = Column(String)
    bmp = Column(Float)
    emp = Column(Float)
    org_num = Column(String(4))
    project_name = Column(String)
    activity_code = Column(Integer)
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
    deleted = Column(Boolean)
    deleted_by = Column(String)
    deleted_date = Column(Date)

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

        error_list = [i for i in error_list if i != '']

        return len(error_list)==0,error_list




    def validate_geom(self):
        corrected_segs,message,bv = check_seg_valid(self.route_id, self.bmp, self.emp)
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
        if not self.activity_code in activity_codes['Activity Code'].tolist():
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
        print(self.task_date, type(self.task_date))
        if (not type(self.task_date) == datetime.date) or (not self.task_date <= datetime.date.today()):
            return 'Task Date not valid',False
        return '',True

    def _debug(self):
        for k,v in self.__dict__.items():
            print(k,v,type(v))

    
mapper_registry.metadata.create_all(db)
Base.metadata.create_all(db)

def standardize_task(data):
    required_fields = ['route_id', 'bmp', 'emp', 'org_num', 'project_name', 'activity_description', 'route_name', 'accomplishments', 'crew_members', 'travel_hours', 'onsite_hours', 'task_date']
    errors = []

    try:
        data['bmp'] = float(data['bmp'])
        data['emp'] = float(data['emp'])
        data['route_id'] = str(data['route_id'])
    except:
        errors.append('BMP & EMP could not be converted into a float value.')

    for i in required_fields:
        if not i in data.keys():
            errors.append(f'No required field {i} given in dictionary object')

    if len(errors) == 0:
        task = Task()
        for k,v in data.items():
            setattr(task, k, v)
        try: 
            task.task_date = parser.parse(data['task_date']) if type(data.get('task_date','')) == str else ''
        except:
            print(task.task_date, 'invalid date')
        task.created_date = datetime.datetime.now()
        return task,errors
    else:
        return None,errors



def add_task(data):
    task,errors = standardize_task(data)
    bv,errors2 = task.validate()
    errors += errors2
    if bv and len(errors) == 0:
        session.add(task)
        session.commit()
        print('\n*****Task added to database\n')
    else:
        print('\n', bv, 'Errors: ', errors, '\n')
    return {'status': bv and len(errors) == 0, 'errors':errors, 'id':task.id}

date_fields = ['task_date', 'created_date', 'updated_date', 'deleted_date']
def update_task(data):
    task = session.query(Task).filter_by(id=data.get('id', None)).first()
    if task is None:
        return {'status': False, 'errors':['ID for record value does not exist'], 'id':data.get('id',None)}

    for k,v in data.items():
        if k in date_fields:
            boolval = False
            try:
                v = parser.parse(v) if type(v) == str else ''
                print('\nDate parsed properly\n')
                boolval = True
            except:
                pass
            if boolval: setattr(task,k,v)
        else:
            setattr(task,k,v)
    
    bv,errors = task.validate()
    if bv:
        # TODO task.updated_by = session['User']
        task.updated_date = datetime.datetime.now()
        session.commit()
        print('\n*****Task updated\n')
    else:
        session.rollback()
        print('\n*****Update failed, rolling back to previous version of db')
        print('*****Errors: ', errors, '\n')

    statusbool = task is not None and bv
    return {'id':task.id, 'status':statusbool, 'errors':errors}


def delete_task(id):
    q = session.query(Task).filter(Task.id == id,Task.deleted == None).first()
    errors = []
    try:
        del_data = {'deleted': True, 'deleted_date': datetime.datetime.today()}
        for k,v in del_data.items():
            setattr(q,k,v)
        session.commit()
        print('\n*****Task deleted\n')
        bv = True
    except:
        print('\n*****Could not find the indicated record\n')
        errors.append(f'ID: {id} does not exist or has already been deleted')
        bv = False
    return {'status': bv, 'id': id, 'errors':errors}


def apply_edits(obj):
    adds = obj.get('adds',[])
    if len(adds) > LIMIT:
        return {'status':False,'message':"Request had more than the limit of transactions per transaction type. %s " % LIMIT}
    else:
        add_results = [add_task(i) for i in adds]

    updates = obj.get('updates',[])
    if len(updates) > LIMIT:
        return {'status':False,'message':"Request had more than the limit of transactions per transaction type. %s " % LIMIT}
    else:
        update_results = [update_task(i) for i in updates]


    deletes = obj.get('deletes',[])
    if len(deletes) > LIMIT:
        return {'status':False,'message':"Request had more than the limit of transactions per transaction type. %s " % LIMIT}
    else:
        delete_results = [delete_task(i) for i in deletes]


    return {
        'addResults':add_results,
        'deleteResults':delete_results,
        'updateResults':update_results,
    }

def query_db(ids):
    q = session.query(Task).filter(Task.id.in_(ids)).all()
    data = {}
    try:
        for i in q:
            data[i.id] = {i.id, i.route_id, i.bmp, i.emp, i.org_num, i.project_name, i.activity_code, i.activity_description, i.route_name, i.accomplishments, i.units, i.crew_members, i.travel_hours, i.onsite_hours, i.task_date, i.notes}
    except:
        return {'status':False, 'data':data}
    return {'status':True, 'data':data}


        

dummy_data = {
    'route_id': '20200600000EB',
    'bmp': 19,
    'emp': 20,
    'org_num': '0121',
    'project_name': 'test_project 2',
    'activity_code': 405,
    'activity_description': 'Bridge Structure Replacement', 
    'route_name': 'River Rd.',
    'accomplishments': 132,
    'units': 'Employee Hours (EH)',
    'crew_members': 4, 
    'travel_hours': 11,
    'onsite_hours': 120,
    'task_date': '11-22-2022',
    'notes': 'test'
    }

print(add_task(dummy_data))

# q = session.query(Task).all()

# print('\n\n\n')
# print('id', 'route_id', 'bmp', 'emp', 'org_num', 'project_name', 'activity_code', 'activity_description', 'route_name', 'accomplishments', 'units', 'crew_members', 'travel_hours', 'onsite_hours', 'task_date', 'notes', 'created_by', 'created_date', 'updated_by', 'updated_date', 'deleted', 'deleted_by', 'deleted_date')
# for i in q:
#     print(i.id, i.route_id, i.bmp, i.emp, i.org_num, i.project_name, i.activity_code, i.activity_description, i.route_name, i.accomplishments, i.units, i.crew_members, i.travel_hours, i.onsite_hours, i.task_date, i.notes, i.created_by, i.created_date, i.updated_by, i.updated_date, i.deleted, i.deleted_by, i.deleted_date)


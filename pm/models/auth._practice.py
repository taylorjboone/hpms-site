import os
import sys  
from logging import RootLogger
from sqlalchemy import create_engine,text,MetaData,Table, Column, Integer, String,ForeignKey,insert,select, bindparam,func, cast,literal_column
from sqlalchemy.orm import Session,registry,relationship
engine = create_engine("sqlite+pysqlite:///C:\PythonTest\Voltron\district_chrystal_report_website\hpms-site\database.db", echo=True, future=True)
metadata_obj = MetaData()




mapper_registry=registry()
Base=mapper_registry.generate_base()
session = Session(engine)

class UserAccount(Base):
    __tablename__='user_account'
    e_number = Column(String)
    id = Column(Integer, primary_key=True)
    role = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    def __repr__(self):
        return f'user_data(e_number={self.e_number!r}, id = {self.id!r}, role = {self.role!r} , first_name = {self.first_name!r} , last_name = {self.last_name!r} )'

mapper_registry.metadata.create_all(engine)
Base.metadata.create_all(engine)

snoop = UserAccount()


e_number_info = input('What is your E Number?:')
role_info = input('What is your role?:')
first_name_info = input('What is your first name?:')
last_name_info = input('What is your last name?:')


def initialize(data):
    snoop = UserAccount()
    for k,v in data.items():
        setattr(snoop, k, v)
    session.add(snoop)


q = session.query(UserAccount).all()


boolval=False

for i in q:
    if (e_number_info == i.e_number) and (role_info == i.role) and (first_name_info == i.first_name) and (last_name_info == i.last_name):
        print('user found \n Accessing Terminal')
        boolval = True

if boolval == False:
    print('User not found')
    answer=input('Would you like to create a user? \n Y/N:')
    # print(answer)
    if answer.lower() in ['yes', 'y']:
        e_number = input('What is your e_number:')
        role = input('What is your role:')
        first_name = input('What is your first name:')
        last_name = input('What is your last name:')
        created_user = {'e_number':e_number,'role':role,'first_name':first_name,'last_name':last_name}
        initialize(created_user)
        session.commit()
    elif answer.lower() in ['no', 'n']:
        print('Ending Terminal...')
        sys.exit()


# while boolval == True:
#     print('meh')






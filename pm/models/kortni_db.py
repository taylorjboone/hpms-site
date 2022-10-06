from sqlalchemy import Float, create_engine, text, orm, MetaData, Table, Column, Integer, String, ForeignKey, Date
from flask_sqlalchemy import SQLAlchemy
from pm import db,app
from wvdot_utils import check_seg_valid


engine = create_engine(r'sqlite+pysqlite:///C:\Users\E025205\Documents\GitHub\hpms-site\database.db', echo=True, future=True)
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
        # for func in self.func_list:
        #     print(func(self))
        print(self.validate_geom())

    def validate_geom(self):
        corrected_segs,message,bv = check_seg_valid(self.route_id, self.bmp, self.emp)
        print(corrected_segs)
        if not bv:
            message = f'corrected segs are: {corrected_segs}'
        return message,bv



    



# metadata_obj.create_all(engine)
# mapper_registry.metadata.create_all(engine)
# Base.metadata.create_all(engine)



t = Task()
t.validate()
# with app.app_context():

#     db.session.add(t)

#     db.session.commit()


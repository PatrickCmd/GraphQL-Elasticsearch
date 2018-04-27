from sqlalchemy import Column, String, Integer, ForeignKey, func, DateTime,create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
engine = create_engine('sqlite:///db_w.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.metadata.create_all(engine)
Base.query = db_session.query_property()

class UtilityMethods:
    def save(self):
        if not self.id:
            db_session.add(self)
        return db_session.commit()

class Individual(Base, UtilityMethods):
    __tablename__ = 'Individual'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
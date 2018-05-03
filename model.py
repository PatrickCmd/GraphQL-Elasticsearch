from sqlalchemy import Column, String, Integer, ForeignKey, func, DateTime,create_engine
from sqlalchemy.orm import relationship, events, session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
engine = create_engine('sqlite:///db_w.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

from search import add_to_index, query_index, remove_from_index

Base = declarative_base()
Base.metadata.create_all(engine)
Base.query = db_session.query_property()


class SearchableMixin(object):
    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': [obj for obj in session.new if isinstance(obj, cls)],
            'update': [obj for obj in session.dirty if isinstance(obj, cls)],
            'delete': [obj for obj in session.deleted if isinstance(obj, cls)]
        }
    
    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['update']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['delete']:
            remove_from_index(cls.__tablename__, obj)
        session._changes = None
    
    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)
    
    @classmethod
    def search(cls, expression):
        ids = query_index(cls.__tablename__, expression)
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            session.sql.case(when, value=cls.id))


class UtilityMethods:
    def save(self):
        db_session.add(self)
        db_session.commit()


class Individual(SearchableMixin, Base, UtilityMethods):
    __tablename__ = 'Individual'
    __searchable__ = ['first_name', 'last_name']
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

events.event.listen(db_session, 'before_commit', Individual.before_commit)
events.event.listen(db_session, 'after_commit', Individual.after_commit)

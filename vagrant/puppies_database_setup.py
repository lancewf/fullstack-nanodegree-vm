import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Float

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
	__tablename__ = 'shelter'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	address = Column(String(255))
	city = Column(String(80))
	state = Column(String(80))
	zipCode = Column(String(80))
	website = Column(String(255))


class Puppy(Base):
	__tablename__ = 'menu_item'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	dateOfBirth = Column(String(250))
	gender = Column(String(250))
	weight = Column(Float(8))
	picture = Column(String(250))
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)


# end of file

engine = create_engine('sqlite:///puppies.db')

Base.metadata.create_all(engine)

#session.query(Puppy).group_by(Puppy.name).all()
#session.query(Puppy).filter(Puppy.dateOfBirth >= sixMonthAgo).order_by(Puppy.dateOfBirth.desc()).all()
#session.query(Puppy).order_by(Puppy.weight).all()
#session.query(Puppy).order_by(Puppy.shelter_id).all()
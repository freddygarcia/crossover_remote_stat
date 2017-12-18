from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, \
							Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import relationship
from CrossOverAssignment import config

DB_CONFIG = dict(config._sections['DATABASE'])

engine = create_engine('mysql+pymysql://{user}:{pass}@{host}/{name}'.format(**DB_CONFIG))
Base = declarative_base()
Session = sessionmaker(engine)()

class Client(Base):
	__tablename__ = 'client'

	id = Column(Integer, primary_key=True)
	ip_address = Column(String(50), nullable=False)
	hostname = Column(String(50))
	email = Column(String(50))
	token = Column(String(50))
	scan_date = Column(DateTime())
	scan_result = relationship("ScanResult")

	@staticmethod
	def load_from_dict(client_dict):
		client = Client()
		client.email = client_dict.get('email')
		client.ip_address = client_dict.get('ip')
		return client

	def __repr__(self):
		return '<Client(host="{}")>'.format(self.hostname)


class ScanType(Base):
	__tablename__ = 'scan_type'

	key = Column(String(10), primary_key=True)
	description = Column(String(50), nullable=False)

	def __init__(self, key=None, description=None):
		self.key = key
		self.description = description

	def __repr__(self):
		return '<ScanType(description="{}")>'.format(self.description)

class WindowsEventLog(Base):
	__tablename__ = 'windows_event_log'

	id = Column(String(10), primary_key=True)
	client_id = Column(Integer, ForeignKey('client.id'))
	event_id = Column(Integer)
	event_time = Column(DateTime)
	event_type = Column(String(50))
	event_msg = Column(Text)
	event_record = Column(Integer)
	event_source = Column(String(50))
	

class ScanResult(Base):
	__tablename__ = 'scan_result'

	id = Column(Integer, primary_key=True)
	limit_value = Column(Integer, nullable=False)
	obtained_value = Column(Integer)

	client_id = Column(Integer, ForeignKey('client.id'))
	scan_type_key = Column(String(10), ForeignKey('scan_type.key'))

	client = relationship("Client", back_populates="scan_result")
	scan_type = relationship("ScanType")
	
	def __repr__(self):
		return '<ScanResult(client="{}",scan_type="{}",scan_result="{}")>'.format(self.client_id, self.scan_type, self.obtained_value)

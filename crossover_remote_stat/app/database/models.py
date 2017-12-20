from datetime import datetime
from logging import getLogger
from sqlalchemy import Column, Integer, String, DateTime, Float, \
							Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import relationship
from crossover_remote_stat import config

log = getLogger(__name__)
DB_CONFIG = dict(config._sections['DATABASE'])

engine = create_engine('{engi}://{user}:{pass}@{host}/{name}'.format(**DB_CONFIG))
Base = declarative_base()
Session = sessionmaker(engine)()

class Client(Base):
	__tablename__ = 'client'

	id = Column(Integer, primary_key=True)
	ip_address = Column(String(50), nullable=False)
	hostname = Column(String(50))
	email = Column(String(50))
	os = Column(String(20))
	creation_date = Column(DateTime(), default=datetime.now)

	execution = relationship("Execution")

	@staticmethod
	def load_from_dict(client_dict):
		client = Client()
		client.os = client_dict.get('os')
		client.email = client_dict.get('email')
		client.ip_address = client_dict.get('ip')
		client.hostname = client_dict.get('hostname')
		return client

class Execution(Base):
	__tablename__ = 'execution'

	id = Column(Integer, primary_key=True)
	client_id = Column(Integer, ForeignKey('client.id'))

	memory_limit = Column(Float)
	cpu_limit = Column(Float)
	token = Column(String(50))
	uptime = Column(DateTime())
	start_date = Column(DateTime())

	scan = relationship("Scan")
	windows_event_log = relationship("WindowsEventLog")

	def __init__(self, token):
		self.token = token

	def __repr__(self):
		return '<Execution(ip={},host="{}")>'.format(self.ip_address,self.hostname)


class Scan(Base):
	__tablename__ = 'scan'

	id = Column(Integer, primary_key=True)
	execution_id = Column(Integer, ForeignKey('execution.id'))
	memory_usage = Column(Float)
	cpu_percent = Column(Float)
	last_update_date = Column(DateTime(), default=datetime.now)

	def __init__(self, statistics):
		self.cpu_percent = statistics.get('cpu_percent')
		self.memory_usage = statistics.get('memory_usage')


class WindowsEventLog(Base):
	__tablename__ = 'windows_event_log'

	id = Column(String(10), primary_key=True)
	execution_id = Column(Integer, ForeignKey('execution.id'))
	event_id = Column(Integer)
	event_time = Column(DateTime)
	event_type = Column(String(50))
	event_msg = Column(Text)
	event_record = Column(Integer)
	event_source = Column(String(50))

	execution = relationship("Execution", back_populates="windows_event_log")
	
	@staticmethod
	def load_from_dict(win_ev_log_dict):
		w_event_log = WindowsEventLog()
		w_event_log.event_id = win_ev_log_dict.get('event_id')
		w_event_log.event_time = win_ev_log_dict.get('event_time')
		w_event_log.event_type = win_ev_log_dict.get('event_type')
		w_event_log.event_msg = win_ev_log_dict.get('event_msg')
		w_event_log.event_record = win_ev_log_dict.get('event_record')
		w_event_log.event_source = win_ev_log_dict.get('event_source')
		return w_event_log


# class ScanResult(Base):
# 	__tablename__ = 'scan_result'

# 	id = Column(Integer, primary_key=True)
# 	limit_value = Column(Integer, nullable=False)
# 	obtained_value = Column(Integer)

# 	execution_id = Column(Integer, ForeignKey('execution.id'))
# 	scan_type_key = Column(String(10), ForeignKey('scan_type.key'))

# 	execution = relationship("Execution", back_populates="scan_result")
# 	scan_type = relationship("ScanType")
	
# 	def __repr__(self):
# 		return '<ScanResult(execution="{}",scan_type="{}",scan_result="{}")>'.format(self.execution_id, self.scan_type, self.obtained_value)

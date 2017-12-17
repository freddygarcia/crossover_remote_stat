from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('mysql+pymysql://root:toor@localhost/crossover_remote_stat')
Base = declarative_base()

class ClientResult(Base):
	__tablename__ = 'client_result'

	id = Column(Integer, primary_key=True)
	ip_address = Column(String(50), nullable=False)
	host_name = Column(String(50))
	email = Column(String(50))
	scan_date = Column(DateTime(), nullable=False, default=datetime.utcnow)
	scan_result = relationship("ScanResult")

	def __repr__(self):
		return '<ClientResult(host="{}")>'.format(self.host_name)


class ScanType(Base):
	__tablename__ = 'alert_type'

	key = Column(String(10), primary_key=True)
	description = Column(String(50), nullable=False)

	def __repr__(self):
		return '<ScanType(description="{}")>'.format(self.description)


class ScanResult(Base):
	__tablename__ = 'scan_result'

	id = Column(Integer, primary_key=True)
	client_id = Column(Integer, ForeignKey('client_result.id'))
	scan_type = Column(String(10), ForeignKey('alert_type.key'))
	limit_value = Column(Integer, nullable=False)
	obtained_value = Column(Integer, nullable=False)
	client = relationship("ClientResult", back_populates="scan_result")
	
	def __repr__(self):
		return '<ScanResult(client="{}",scan_type="{}",scan_result="{}")>'.format(self.client_id, self.scan_type, self.obtained_value)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


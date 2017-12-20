from crossover_remote_stat.app.database.models import engine, Client, ScanType, Base, Session
from logging import getLogger

log = getLogger(__name__)

def initialize_db():
	Base.metadata.drop_all(engine)
	log.info('database cleaned')
	Base.metadata.create_all(engine)
	log.info('database generated')

def populate():
	Session.add(ScanType('cpu', 'Procesador'))
	Session.add(ScanType('memory', 'Memoria Virtual'))

	try:
		Session.commit()
		log.info('database populated')
	except Exception as e:
		log.error('could populate database')
		log.error(e)

def initialize_and_populate():
	initialize_db()
	populate()
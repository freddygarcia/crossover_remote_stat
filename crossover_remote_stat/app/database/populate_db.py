from crossover_remote_stat.app.database.models import engine, Base, Session
from logging import getLogger

log = getLogger(__name__)

def initialize_db():
	Base.metadata.drop_all(engine)
	log.info('database cleaned')
	Base.metadata.create_all(engine)
	log.info('database generated')

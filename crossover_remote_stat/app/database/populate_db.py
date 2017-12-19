from crossover_remote_stat.app.database.models import engine, Client, ScanType, Base, Session
from logging import getLogger

log = getLogger(__name__)

Base.metadata.drop_all(engine)
log.info('database cleaned')
Base.metadata.create_all(engine)
log.info('database generated')

Session.add(ScanType('cpu', 'Procesador'))
Session.add(ScanType('memory', 'Memoria Virtual'))
Session.commit()
log.info('database populated')

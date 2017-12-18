from models import engine, Client, ScanType, Base, Session

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session.add(ScanType('cpu', 'Procesador'))
Session.add(ScanType('memory', 'Memoria Virtual'))
Session.commit()

from sqlalchemy.orm.session import sessionmaker
from models import engine, ClientResult

Session = sessionmaker(engine)()

c = ClientResult()
c.ip_address = 'localhost'
Session.add(c)
Session.commit()

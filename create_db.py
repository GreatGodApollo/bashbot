from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class ServerConfig(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True, nullable=False)
    serverId = Column(String(18), nullable=False)
    adminRole = Column(String(100), nullable=False)
    modRole = Column(String(100), nullable=False)


class ServerMutes(Base):
    __tablename__ = 'mutes'

    id = Column(Integer, primary_key=True, nullable=False)
    serverId = Column(String(18), nullable=False)
    userId = Column(String(18), nullable=False)


engine = create_engine('mysql+pymysql://apollo_bash:ThisAmazing@cpanel.theendlessweb.com/apollo_bashbot',
                       pool_pre_ping=True)

Base.metadata.create_all(engine)

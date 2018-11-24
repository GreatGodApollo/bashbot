from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ServerConfig(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True, nullable=False)
    serverId = Column(String(18), nullable=False)
    adminRole = Column(String(100), nullable=False)
    modRole = Column(String(100), nullable=False)

from sqlalchemy import Column, String, JSON, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from datasource.database import Base

class DataGame(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_matrix = Column(JSON, default=lambda: [[0,0,0],[0,0,0],[0,0,0]])
    status = Column(String, default="WAITING")
    game_type = Column(String, nullable=True)
    current_turn = Column(String, nullable=True)
    players = Column(ARRAY(String), default=[])
    symbols = Column(JSON, default={})

class DataUser(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
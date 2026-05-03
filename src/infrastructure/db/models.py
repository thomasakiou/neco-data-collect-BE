from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    state_code = Column(String, index=True, nullable=False)
    state_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class SSCEModel(Base):
    __tablename__ = "ssce"

    id = Column(Integer, primary_key=True, index=True)
    state_code = Column(String, index=True, nullable=False)
    state_name = Column(String, nullable=False)
    sch_num = Column(String, index=True, nullable=False)
    sch_name = Column(String, nullable=False)
    cust_code = Column(String, nullable=False)
    cust_name = Column(String, nullable=False)
    cust_town = Column(String, nullable=False)
    status = Column(String, nullable=True)
    type = Column(String, nullable=True)
    category = Column(String, nullable=True)
    accd_year = Column(String, nullable=True)
    lga = Column(String, index=True, nullable=True)
    sch_email = Column(String, nullable=True)
    accreditation_type = Column(String, nullable=True)
    lga_code = Column(String, index=True, nullable=True)

class BECEModel(Base):
    __tablename__ = "bece"

    id = Column(Integer, primary_key=True, index=True)
    state_code = Column(String, index=True, nullable=False)
    state_name = Column(String, nullable=False)
    sch_num = Column(String, index=True, nullable=False)
    sch_name = Column(String, nullable=False)
    cust_code = Column(String, nullable=False)
    cust_name = Column(String, nullable=False)
    cust_town = Column(String, nullable=False)
    status = Column(String, nullable=True)
    type = Column(String, nullable=True)
    category = Column(String, nullable=True)
    accd_year = Column(String, nullable=True)
    lga = Column(String, index=True, nullable=True)
    sch_email = Column(String, nullable=True)
    accreditation_type = Column(String, nullable=True)
    lga_code = Column(String, index=True, nullable=True)

class LGAModel(Base):
    __tablename__ = "lgas"

    id = Column(Integer, primary_key=True, index=True)
    state_name = Column(String, nullable=False)
    state_code = Column(String, index=True, nullable=False)
    lga_name = Column(String, index=True, nullable=False)
    lga_code = Column(String, index=True, nullable=True)

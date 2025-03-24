from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import yfinance as yf

DATABASE_URL = "postgresql://user:password@172.18.0.2:5432/portfolio_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

#Database model

class Portfolio(Base):
    __tablename__ = "portfolio"
    id = Column(Integer, primary_key=True,index=True)
    ticker = Column(String, index=True)
    allocation = Column(Float)

Base.metadata.create_all(bind=engine)

class PortfolioInput(BaseModel):
    tickers: list[dir]
    allocations : list[dir]
    class Config:
        arbitrary_types_allowed = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# fetch historical data
@app.get("/historical-data/")
def get_historical_data(tickers: str, start: str = "2023-01-01", end: str = "2024-01-01"):
    print("1")
    tickers_list = tickers.split(",")
    data = yf.download(tickers_list, start=start, end=end)["Adj Close"]
    return data.to_json()



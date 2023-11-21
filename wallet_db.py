import os
import asyncpg
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
port = int(os.getenv('port'))
dbname = os.getenv('dbname')


DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

create_script = '''CREATE TABLE IF NOT EXISTS income_and_expenses(
                    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                    date DATE NOT NULL,
                    description VARCHAR(250) NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    typeexpinc VARCHAR(10) NOT NULL
                    );'''

insert_query = '''INSERT INTO income_and_expenses (date, description, amount, typeexpinc)
                            VALUES ($1, $2, $3, $4);'''

select_all_query = '''SELECT * FROM income_and_expenses ORDER BY date;'''

_global_dbpool = None

# Connect to db and auto create table
async def startdb():
    global _global_dbpool
    if _global_dbpool is not None:
        return _global_dbpool
    try:
        dbpool = await asyncpg.create_pool(DATABASE_URL)
        async with dbpool.acquire() as conn:
            await conn.execute(create_script)
        _global_dbpool = dbpool
        return dbpool
    except Exception as e:
        return f'Error: {e}'

# Insert new data to table
async def insert_data(dbpool, date, description, amount, typeexpinc):
    try:
        if dbpool:
            async with dbpool.acquire() as conn:
                await conn.execute(insert_query, date, description, amount, typeexpinc)
    except Exception as e:
        return f'Error: {e}'

# Select all data
async def select_data(dbpool):
    try:
        if dbpool:
            async with dbpool.acquire() as conn:
                result = await conn.fetch(select_all_query)
                records = []
                for record in result:
                    record_dict = {
                    'Date': record['date'],
                    'Description': record['description'],
                    'Amount': record['amount'],
                    'Type': record['typeexpinc']
                    }
                    records.append(record_dict)
                return records
    except Exception as e:
        return f'Error: {e}'


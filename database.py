import pandas as pd
from sqlalchemy import create_engine

# MySQL Connection
engine = create_engine(
    "mysql+pymysql://root:root123@localhost/food_waste_db"
)

# Read CSV Files
providers = pd.read_csv("data/providers_data.csv")
receivers = pd.read_csv("data/receivers_data.csv")
food = pd.read_csv("data/food_listings_data.csv")
claims = pd.read_csv("data/claims_data.csv")

# Upload Data to MySQL
providers.to_sql(
    "providers",
    engine,
    if_exists="replace",
    index=False
)

receivers.to_sql(
    "receivers",
    engine,
    if_exists="replace",
    index=False
)

food.to_sql(
    "food_listings",
    engine,
    if_exists="replace",
    index=False
)

claims.to_sql(
    "claims",
    engine,
    if_exists="replace",
    index=False
)

print("Data uploaded successfully!")
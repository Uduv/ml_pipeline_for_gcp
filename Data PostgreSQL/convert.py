import pandas as pd


df = pd.read_csv('Data PostgreSQL\Dataset-Unicauca-Version2-87Atts.csv')
df.to_parquet('Data PostgreSQL\Dataset-Unicauca-Version2-87Atts.parquet')

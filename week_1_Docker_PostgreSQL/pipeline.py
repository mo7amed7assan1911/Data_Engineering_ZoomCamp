
# Ingesting data from the source URL then save it in PostgreSQL database.
import pandas as pd
from sqlalchemy import create_engine, types
from sqlalchemy_utils import database_exists, create_database
from time import time
import argparse
import os

def main(args):
    user = args.user
    password = args.password
    host = args.host
    port = args.port
    db   = args.db
    trips_table_name = args.trips_table_name
    zones_table_name = args.zones_table_name
    trips_data_url    = args.trips_data_url
    zones_data_url    = args.zones_data_url
    
    trips_data_csv_name   = './data/trips.csv'
    zones_data_csv_name   = './data/zones.csv'
    
    os.makedirs('./data/', exist_ok=True)
    
    # downloading the tips csv and name it 'output.csv'
    os.system(f'wget {trips_data_url} -O {trips_data_csv_name}')
    os.system(f'wget {zones_data_url} -O {zones_data_csv_name}')
    
    print('Data is downloaded and saved locally 🥰')
    
    df_trips = pd.read_csv(trips_data_csv_name, nrows=1, compression='gzip') # read only the first row to get the columns names.
    df_zones = pd.read_csv(zones_data_csv_name) # small so we will put it all in memory.
    
    print('good dataframe') 
    
    # connecting to the postgresql database.
    # create new database if not exists with this name.
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    if not database_exists(engine.url):
        create_database(engine.url)
        
    print(f'Connected to posgresql server | database: {db} 🥰')
    
    # Creating 2 tables schemas | no rows
    dtype_mapping_trips = {
        'lpep_pickup_datetime': types.DateTime(),
        'lpep_dropoff_datetime': types.DateTime(),
    }
    df_trips.head(0).to_sql(con=engine, name=trips_table_name, if_exists='replace', dtype=dtype_mapping_trips, index=False)
    df_zones.head(0).to_sql(con=engine, name=zones_table_name, if_exists='replace', index=False)
    
    print(f'Created 2 tables {trips_table_name} & {zones_table_name} correctly! 🥰')
    
    # Inserting data of zones into the DB.
    df_zones.to_sql(con=engine, name=zones_table_name, if_exists='replace', index=False)
    
    
    # We will not insert all data in one shot as it is has much records.
    # making it iterable to send batches of records.
    df_iter = pd.read_csv(trips_data_csv_name, iterator=True, chunksize=100000, compression='gzip')
    
    for i, batch in enumerate(df_iter):
        
        t_start = time()
        
        batch.lpep_dropoff_datetime = pd.to_datetime(batch.lpep_dropoff_datetime)
        batch.lpep_pickup_datetime  = pd.to_datetime(batch.lpep_pickup_datetime)

        batch.to_sql(con=engine, name=trips_table_name, if_exists='append', index=False)
        
        t_end = time()
        print(f'Inserted batch {i + 1}, took {(t_end - t_start):.3f} sec 🥰')
        
    print('ETL is finished 🥰🤝')
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Ingest CSV to postgresql database')

    # user, password, host, port, database name, table name, url of the csv
    parser.add_argument('--user', help='user name')
    parser.add_argument('--password', help='password of teh posgres server')
    parser.add_argument('--host', help='host of the pg server')
    parser.add_argument('--port', help='port of pg server')
    parser.add_argument('--db', help='database name')
    parser.add_argument('--trips_table_name', help='trips data table name')
    parser.add_argument('--zones_table_name', help='zones data table name')
    parser.add_argument('--trips_data_url', help='url of the green trips data as csv file')
    parser.add_argument('--zones_data_url', help='url of the zones data as csv file')
    
    args = parser.parse_args()
    
    main(args=args)


# The host will be pgServer (the PostgreSQL server in our `docker-compose` file) if you run the script inside a container that is on the pg-network.


# to run only python script
# trips_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
# zones_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

# python pipeline.py \
#     --user=root \
#     --password=mypass \
#     --host=localhost \
#     --port=5432 \
#     --db=ny_taxi \
#     --trips_table_name="taxi_trips" \
#     --zones_table_name="taxi_zones" \
#     --trips_data_url=${trips_url} \
#     --zones_data_url=${zones_url}
    
    
# to run the docker image
# trips_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
# zones_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

# docker run -it --network data_engineering_zoomcamp_pg-network data_ingestion \
#     --user=root \
#     --password=mypass \
#     --host=pgServer \
#     --port=5432 \
#     --db=ny_taxi \
#     --trips_table_name="taxi_trips" \
#     --zones_table_name="taxi_zones" \
#     --trips_data_url=${trips_url} \
#     --zones_data_url=${zones_url}





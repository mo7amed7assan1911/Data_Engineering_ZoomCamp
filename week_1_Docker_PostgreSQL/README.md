# ETL & Containerization of PostgreSQL Environment
### Building the PostgreSQL Environment
🚀 To build the PostgreSQL environment, run the following command:

```bash
docker-compose -f postgres_env.yml up -d
```

### Loading Dataset and Adding it to the Database

🛠️ To load the dataset and add it to the database, execute the `pipeline.py` script. Ensure accurate values for the arguments, such as user, password, host, and port based on the running containers.

📝 **NOTICE:** The `host` will be pgServer (the PostgreSQL server in our `docker-compose` file) if you run the script inside a container that is on the pg-network. and the network will be the `data_engineering_zoomcamp_pg-networ`

🚀 To run the code outside a docker container, Run the following command:

```bash
trips_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
zones_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

python pipeline.py \
    --user=root \
    --password=mypass \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --trips_table_name="taxi_trips" \
    --zones_table_name="taxi_zones" \
    --trips_data_url=${trips_url} \
    --zones_data_url=${zones_url}
```


To dockerize the pipeline.py code, just build the image of the Dockerfile.

```bash
docker build -t data_ingestion .
```

then run this command to run the application:

```bash
trips_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
zones_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

docker run -it --network data_engineering_zoomcamp_pg-network data_ingestion \
    --user=root \
    --password=mypass \
    --host=pgServer \
    --port=5432 \
    --db=ny_taxi \
    --trips_table_name="taxi_trips" \
    --zones_table_name="taxi_zones" \
    --trips_data_url=${trips_url} \
    --zones_data_url=${zones_url}
```
{{ config(materialized='table') }}

select
    vendor_id,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    fare_amount,
    extract(hour from tpep_pickup_datetime) as pickup_hour,
    to_char(tpep_pickup_datetime, 'Day') as pickup_day_of_week,
    round((fare_amount / trip_distance)::numeric, 2) as cost_per_mile,
    round(
        extract(epoch from (tpep_dropoff_datetime - tpep_pickup_datetime)) / 60::numeric, 
        2
    ) as trip_duration_minutes,
    "PULocationID",
    "DOLocationID"
from {{ ref('stg_taxi_trips') }}
where
    extract(epoch from (tpep_dropoff_datetime - tpep_pickup_datetime)) / 60 between 1 and 300

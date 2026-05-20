{{ config(materialized='view') }}

select
    "VendorID" as vendor_id,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    total_amount,
    payment_type,
    "PULocationID",
    "DOLocationID"
from {{ source('raw', 'taxi_trips_raw') }}
where 
    trip_distance > 0
    and fare_amount > 0
    and passenger_count > 0
    and "PULocationID" is not null
    and "DOLocationID" is not null

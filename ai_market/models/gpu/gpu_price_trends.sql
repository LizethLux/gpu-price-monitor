{{ config(materialized='table') }}

select 
date_trunc('DAY', collection_date) as collection_day,
gpu_model,
count(*) as total_listings,
round(avg(price),2) as average_price,
min(price) as lowest_price,
max(price) as highest_price

from {{ ref('stg_gpu_prices') }}

where valid_price = True
and out_of_stock = False

group by
collection_day,
gpu_model

order by
collection_day,
gpu_model
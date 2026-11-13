{{ config(materialized='table') }}

select
gpu_model,
count(*) as total_listings,
round(avg(price),2) as average_price,
min(price) as lowest_price,
max(price) as highest_price

from {{ ref('stg_gpu_prices') }}

where valid_price = True
and out_of_stock = False

group by gpu_model
order by average_price desc
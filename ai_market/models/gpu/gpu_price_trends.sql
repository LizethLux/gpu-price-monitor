{{ config(materialized='table') }}

select 
date_trunc('DAY', collectiuon_dates) as collection_day
gpu_model,
count(*) as total_listings,
round(avg)
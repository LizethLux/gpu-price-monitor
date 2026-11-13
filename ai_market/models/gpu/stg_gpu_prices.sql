{{ config(materialized='view') }} --tels dbt to create a view in snowflake rather than another physical table
select
collection_date,
gpu_model,
seller,
price,
currency,
condition,
stock_status,
product_title,
product_url,
valid_price,
price_category,
out_of_stock

from ai_hardware_db.raw.gpu_prices
--first dbt staging model. reads raw gpu price records from snowflake
--
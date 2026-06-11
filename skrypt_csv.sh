#!/usr/bin/env bash
uv run main.py \
  -i example/csv/brands.csv \
  -i example/csv/categories.csv \
  -i example/csv/customers.csv \
  -i example/csv/order_items.csv \
  -i example/csv/orders.csv \
  -i example/csv/products.csv \
  -i example/csv/staffs.csv \
  -i example/csv/stocks.csv \
  -i example/csv/stores.csv \
  -x \
  -r


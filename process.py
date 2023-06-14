import pandas as pd
import argparse

msg = "Finding top n sellers in a given data range"

parser = argparse.ArgumentParser(description=msg)
parser.add_argument('--min-date', type=str, default='2020-01-01',
                    help='start date of the data range in YYYY-MM-DD format')
parser.add_argument('--max-date', type=str, default='2020-06-30',
                    help='end date of the data range in YYYY-MM-DD format')
parser.add_argument('--top', type=int, default=3, help='desired number of top sellers to print')
args = parser.parse_args()

product = pd.read_csv('product.csv')
sales = pd.read_csv('sales.csv')
store = pd.read_csv('store.csv')

# merge dataframes on id columns
sales = pd.merge(sales, product, left_on='product', right_on='id')
sales = pd.merge(sales, store, left_on='store', right_on='id')

# convert date column to datetime format
sales['date'] = pd.to_datetime(sales['date'])
sales = sales.rename(columns={'id_y': 'id', 'name_y': 'name'})

# filter by date range given by the user
sales = sales[(sales['date'] >= args.min_date) & (sales['date'] <= args.max_date)]

# group by product and get the sum of quantity
top_products = sales.groupby(['name'])['quantity'].sum().reset_index().sort_values('quantity', ascending=False).head(
    args.top)

# group by store and get the sum of quantity
top_stores = sales.groupby(['name', 'city'])['quantity'].sum().reset_index().sort_values('quantity',
                                                                                         ascending=False).head(args.top)

# group by brand and get the sum of quantity
top_brands = sales.groupby(['brand'])['quantity'].sum().reset_index().sort_values('quantity', ascending=False).head(
    args.top)

# group by city and get the sum of quantity
top_cities = sales.groupby(['city'])['quantity'].sum().reset_index().sort_values('quantity', ascending=False).head(
    args.top)



def print_top_selling_products(top_products):
    print('-- top seller product --')
    print(top_products[['name', 'quantity']])


def print_top_selling_stores(top_stores):
    print('-- top seller store --')
    print(top_stores[['name', 'quantity']])


def print_top_selling_brands(top_brands):
    print('-- top seller brand --')
    print(top_brands[['brand', 'quantity']])


def print_top_selling_cities(top_cities):
    print('-- top seller city --')
    print(top_cities[['city', 'quantity']])

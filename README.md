# ShopifyCSV

ShopifyCSV is a library that helps with programmatically working with [uploading products to Shopify via a csv file](https://help.shopify.com/en/manual/products/import-export/using-csv)
(an alternative to using the Admin API). 
When I was writing a Python program that creates such a csv, I found it a pain to recreate the 47 columns in my code. 
This library provides a ShopifyRow class that exposes the columns as properties, offering validation. 

## Usage

```python
import csv
from shopify_csv import ShopifyRow

row = ShopifyRow()
row.handle = 'my-product-handle' # throws ValueError if value is does not conform to upload format
row.title = 'My Product!'
row.tags = ["red", "blue", "green"]
row.google_shopping_adwords_grouping = "products"
# ... set other relevant fields
row.validate_required_fields() # throws Value Error if a required field is empty

with open('upload-file.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerow(ShopifyRow.FIELDS)  # write header
	writer.writerow(row.writable) # write row
```
To make it easy, the csv will contain all optional fields, which will just be left blank if not required.
## API

An instance of the ```ShopifyRow``` class exposes all column fields as properties in the snake_case style (e.g. "Option1 Name" as `row.option1_name`). 
If the value does not conform to the required data format, a `ValueError` is being thrown with a human-readable error message.

A row instance also has a ```row.validate_required_fields(is_variant=False)``` method that checks if there are required fields that were not set, or
(in case it is a variant) if fields that should be blank are filled.

An instance has a ```writable``` property that returns all properties as a list that can be used for a csv writer.

## Limitations
Some things that can make a product csv invalid will not be detected by row-level validation, e.g. duplicate handles,
or if the image source points to a broken URL.


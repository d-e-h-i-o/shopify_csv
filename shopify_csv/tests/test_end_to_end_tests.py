import os
import csv

from shopify_csv import ShopifyRow


def get_template_rows():
    with open(
        os.path.join(
            os.getcwd(), "shopify_csv", "tests", "fixtures", "product_template.csv"
        ),
        "r",
    ) as file:
        reader = csv.reader(file, delimiter=";")
        return [row for row in reader]


def get_shopify_rows():
    return_rows = []

    return_rows.append(ShopifyRow.FIELDS)

    row = ShopifyRow()
    row.handle = "example-product"
    row.title = "Some product"
    row.vendor = "Vendor"
    row.type = "product"
    row.tags = "tag1"
    row.published = True
    row.option1_name = "Title"
    row.option1_value = "Some option value"
    row.variant_grams = 3629
    row.variant_inventory_policy = "deny"
    row.variant_fulfillment_service = "manual"
    row.variant_price = 25
    row.variant_requires_shipping = True
    row.variant_taxable = True
    row.image_src = "https://test.com/product.jpg"
    row.image_position = 1
    row.gift_card = False
    row.seo_title = "Seo title."
    row.seo_description = "Description"
    row.google_shopping_google_product_category = "Products > Products"
    row.google_shopping_gender = "Unisex"
    row.google_shopping_age_group = "Adult"
    row.google_shopping_mpn = "man"
    row.google_shopping_adwords_grouping = "products"
    row.google_shopping_adwords_labels = "labels"
    row.google_shopping_condition = "used"
    row.google_shopping_custom_product = "FALSE"
    row.variant_weight_unit = "g"
    row.status = "active"
    row.validate_required_fields()
    return_rows.append(row.writable)

    row = ShopifyRow()
    row.handle = "example-t-shirt"
    row.option1_value = "Small"
    row.variant_sku = "example-product-s"
    row.variant_grams = 200
    row.variant_inventory_policy = "deny"
    row.variant_fulfillment_service = "manual"
    row.variant_price = 29.99
    row.variant_compare_at_price = 34.99
    row.variant_requires_shipping = True
    row.variant_taxable = True
    row.variant_weight_unit = "g"
    row.validate_required_fields(is_variant=True)
    return_rows.append(row.writable)

    row = ShopifyRow()
    row.handle = "example-t-shirt"
    row.option1_value = "Medium"
    row.variant_sku = "example-product-m"
    row.variant_grams = 200
    row.variant_inventory_tracker = "shopify"
    row.variant_inventory_policy = "deny"
    row.variant_fulfillment_service = "manual"
    row.variant_price = 29.99
    row.variant_compare_at_price = 34.99
    row.variant_requires_shipping = True
    row.variant_taxable = True
    row.variant_weight_unit = "g"
    row.validate_required_fields(is_variant=True)
    return_rows.append(row.writable)

    return return_rows


def test_should_produce_template_csv():

    template_rows = get_template_rows()
    shopify_rows = get_shopify_rows()

    for template_row, shopify_row in zip(template_rows, shopify_rows):
        for field1, field2 in zip(template_row, shopify_row):
            assert field1 == field2

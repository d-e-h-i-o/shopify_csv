import pytest
from shopify_csv import ShopifyRow


def check_valid_values(attribute, values):
    row = ShopifyRow()
    for value in values:
        setattr(row, attribute, value)
        assert getattr(row, attribute) == value


def check_invalid_values(attribute, invalid_values):
    row = ShopifyRow()
    for value in invalid_values:
        with pytest.raises(ValueError):
            setattr(row, attribute, value)


def check_boolean_values(attribute):
    row = ShopifyRow()
    for valid_value in [True, False, "TRUE", "FALSE"]:
        setattr(row, attribute, valid_value)
        assert getattr(row, attribute) in ["TRUE", "FALSE"]

    for invalid_value in [1, 0, "false"]:
        with pytest.raises(ValueError):
            setattr(row, attribute, invalid_value)
            assert getattr(row, attribute) == ""


@pytest.mark.parametrize(
    "attribute,values",
    [
        ("handle", ["Product", "Product1", "Product-1"]),
        ("vendor", ["Vendor", ""]),
        ("variant_grams", [1, 2, 500]),
        ("variant_inventory_policy", ["deny", "continue"]),
        (
            "variant_inventory_tracker",
            ["shopify", "shipwire", "amazon_marketplace_web", ""],
        ),
        ("variant_price", [1, 1.0]),
        ("variant_compare_at_price", [1, 1.0]),
        ("image_src", ["some_image", "another_image"]),
        ("variant_fulfillment_service", "some_value"),
        ("variant_weight_unit", ["g", "kg", "", "lb", "oz"]),
        ("status", ["active", "draft", "archived"]),
    ],
)
def test_valid_values(attribute, values):
    check_valid_values(attribute, values)


@pytest.mark.parametrize(
    "attribute, invalid_values",
    [
        ("handle", ["My Product", "My Prodúct", "My.Product"]),
        ("vendor", ["a"]),
        ("published", [1, 0, "True", "FALSE Value"]),
        ("variant_grams", [1.0, "1.0", {"weight": 1}]),
        ("variant_inventory_policy", ["something", 1]),
        ("variant_inventory_tracker", ["something", 1]),
        ("variant_fulfillment_service", ["My Fulfillment Service"]),
        ("variant_price", ["string", {}]),
        ("variant_compare_at_price", ["string", {}]),
        ("image_src", ["image_thumb", "image_small", "image_medium"]),
        ("image_alt_text", ["a" * 513]),
        ("seo_description", ["a" * 321]),
        ("variant_weight_unit", ["gramms", "KG"]),
        ("status", ["", "some_status"]),
    ],
)
def test_invalid_values(attribute, invalid_values):
    check_invalid_values(attribute, invalid_values)


@pytest.mark.parametrize(
    "attribute", ["published", "variant_requires_shipping", "variant_taxable"]
)
def test_boolean_values(attribute):
    check_boolean_values(attribute)


def test_tag_setter():
    row = ShopifyRow()

    row.tags = ["red", "blue", "green"]
    assert row.tags == "red,blue,green"

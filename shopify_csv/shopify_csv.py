from shopify_csv import FIELDS, PROPERTIES
from .validation import (
    OneOf,
    String,
    Regex,
    Boolean,
    Integer,
    Numeric,
    Image,
    NoWhitespace,
    Tags,
)


class ShopifyRow:
    FIELDS = FIELDS
    handle = Regex(
        r"^[\w-]+$",
        "Handle can contain letters, dashes, and numbers, but no spaces, accents, or other "
        "characters, including periods. ",
    )
    title = String()
    body = String()
    vendor = String(predicate=lambda x: len(x) != 1)
    type = String()
    tags = Tags()
    published = Boolean()
    variant_sku = String(minsize=1)
    variant_grams = Integer()
    variant_inventory_tracker = OneOf(
        "shopify", "shipwire", "amazon_marketplace_web", ""
    )
    variant_inventory_qty = Integer()
    variant_inventory_policy = OneOf("deny", "continue")
    variant_fulfillment_service = NoWhitespace()
    variant_price = Numeric()
    variant_compare_at_price = Numeric()
    variant_requires_shipping = Boolean()
    variant_taxable = Boolean()
    variant_barcode = String()
    image_src = Image()
    image_position = Integer()
    image_alt_text = String(maxsize=512)
    gift_card = Boolean()
    seo_title = String()
    seo_description = String(maxsize=320)
    google_shopping_google_product_category = String()
    google_shopping_gender = String()
    google_shopping_age_group = String()
    google_shopping_mpn = String()
    google_shopping_adwords_grouping = String()
    google_shopping_adwords_labels = String()
    google_shopping_condition = String()
    google_shopping_custom_product = String()
    google_shopping_custom_label_0 = String()
    google_shopping_custom_label_1 = String()
    google_shopping_custom_label_2 = String()
    google_shopping_custom_label_3 = String()
    google_shopping_custom_label_4 = String()
    variant_image = String()
    variant_weight_unit = OneOf("", "g", "kg", "lb", "oz")
    variant_tax_code = String()
    cost_per_item = Numeric()
    status = OneOf("active", "draft", "archived")
    collection = String()

    def __init__(self, **kwargs):
        self.__dict__.update({var: "" for var in PROPERTIES})
        for prop in kwargs:
            setattr(self, prop, kwargs[prop])

    def validate_required_fields(self, is_variant=False):
        """Validates that all necessary fields are not blank, and some additional stuff."""

        self.check_empty_fields(is_variant=is_variant)

        if (
            self.variant_fulfillment_service
            not in ["manual", "shipwire", "webgistix", "amazon_marketplace_web"]
            and not self.variant_sku
        ):
            raise ValueError(
                "SKU can't be empty if custom fulfillment service is used."
            )

    def check_empty_fields(self, is_variant=False):
        """Checks whether the fields should be true or not"""
        not_empty = []
        should_be_empty = []

        if not is_variant:
            not_empty = [
                "handle",
                "title",
                "option1_name",
                "option1_value",
                "variant_grams",
                "variant_inventory_policy",
                "variant_fulfillment_service",
                "variant_price",
            ]

        elif is_variant:
            not_empty = [
                "handle",
            ]
            should_be_empty = ["title", "body_html", "vendor", "tags"]

        missing_fields = []
        for attr in not_empty:
            if getattr(self, attr, "") == "":
                missing_fields.append(attr)

        if missing_fields:
            raise ValueError(f"{', '.join(missing_fields)} can't be empty")

        fields_should_be_empty = []
        for attr in should_be_empty:
            if getattr(self, attr, "") != "":
                fields_should_be_empty.append(attr)

        if fields_should_be_empty:
            raise ValueError(f"{', '.join(fields_should_be_empty)} should be empty")

    @property
    def writable(self):
        return [str(getattr(self, key, "")) for key in PROPERTIES]

from itertools import izip
from categories_es import CATEGORIES_ES

categories = CATEGORIES_ES["categories"]

ALL_CATEGORIES = categories.keys()
FUNCTION_CATEGORIES = ["D", "C", "M", "T", "SP", "P"]
CONTENT_CATEGORIES = ["A", "N", "V"]


def category_name(code):
    return categories[code.upper()]


def parse_category(category_info):
    description = {}
    category_code = "SP" if category_info.startswith("SP") else category_info[0]
    category, attributes_code = categories[category_code], category_info[len(category_code):]
    description["category_code"] = category_code
    description["categoria"] = category["category"]
    for attribute, code in izip(category.get("attributes", []), attributes_code):
        if code in attribute:
            description[attribute["_"]] = (code, attribute[code])
    return description


def parse_category_brief(category_info):
    if category_info == "":  # for the <s> token
        return {}
    long_description = parse_category(category_info)
    description = {}
    description["C"] = long_description["category_code"]
    # note that every factor starts with a different letter!, otherwise this code doesnt work :P
    for factor in ["category_code", "numero", "genero", "persona", "modo", "tiempo"]:
        if factor in long_description:
            description[factor[0].upper()] = long_description[factor][0]
    return description

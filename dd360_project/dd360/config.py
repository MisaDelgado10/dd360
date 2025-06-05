FEATURE_SETS = {
    "surface": ["price", "num_bedrooms", "num_bathrooms", "age", "construction_surface"],
    "surface_improved": ["price_per_m2", "num_bedrooms", "num_bathrooms", "age", "has_amenities"],
    "price_rooms": ["price", "num_bedrooms", "num_bathrooms"],
    "all_numeric": ["price", "num_bedrooms", "num_bathrooms", "age", "construction_surface"],
    "improved": ["construction_surface", "age", "num_bathrooms", "num_bedrooms", "type_house", "price_per_m2", "has_amenities"],
    "no_categorial": ["construction_surface", "age", "num_bathrooms", "num_bedrooms", "num_parking_lots", "price_per_m2", "has_amenities"]
}

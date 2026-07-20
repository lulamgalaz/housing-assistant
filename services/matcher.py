def matches_preferences(listing, preference):

    if listing.price > preference.max_price:
        return False

    if listing.bedrooms < preference.min_bedrooms:
        return False

    neighborhoods = preference.neighborhoods.split(",")

    if listing.neighborhood not in neighborhoods:
        return False

    return True
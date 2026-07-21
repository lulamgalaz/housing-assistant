def normalize_listing(item):

    return {

        # -----------------------------
        # Información básica
        # -----------------------------

        "source": item.get(
            "source",
            "Unknown"
        ),

        "title": item.get(
            "title",
            "Sin título"
        ),

        "price": item.get(
            "price"
        ),

        "neighborhood": item.get(
            "neighborhood",
            "N/A"
        ),

        "district": item.get(
            "district"
        ),

        "bedrooms": item.get(
            "bedrooms",
            0
        ),

        "bathrooms": item.get(
            "bathrooms"
        ),

        "surface_m2": item.get(
            "surface_m2"
        ),

        "furnished": item.get(
            "furnished"
        ),

        "available_from": item.get(
            "available_from"
        ),


        # -----------------------------
        # Características vivienda
        # -----------------------------

        "balcony": item.get(
            "balcony",
            False
        ),

        "terrace": item.get(
            "terrace",
            False
        ),

        "elevator": item.get(
            "elevator"
        ),

        "air_conditioning": item.get(
            "air_conditioning"
        ),

        "separate_kitchen": item.get(
            "separate_kitchen"
        ),

        "expenses_included": item.get(
            "expenses_included"
        ),


        # -----------------------------
        # Contrato
        # -----------------------------

        "contract_months": item.get(
            "contract_months"
        ),

        "contract_type": item.get(
            "contract_type"
        ),


        # -----------------------------
        # Otros
        # -----------------------------

        "floor": item.get(
            "floor"
        ),

        "exterior": item.get(
            "exterior"
        ),

        "url": item.get(
            "url"
        ),
    }
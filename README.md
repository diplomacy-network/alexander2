# alexander v0.2

Eine mapAPI für DNW2.0.

Zurzeit erreichbar unter http://wulfheart.pythonanywhere.com/v0.2.

## [GET] /variants

**Response:**
```json
[
    {
        "name": "standard",
        "powers": [
            "FRANCE", "ENGLAND", "GERMANY", "..."
        ],
        "end_of_game": 18
    }
]
```


## [GET] /adjudicate/{variant-name}

Gets a basic game instance of a variant

**Response:**

```
Refer to ## [POST] /adjudicate
```

## [POST] /adjudicate

**Request:** 

```json
{
    "orders": [
        {
            "power": "FRANCE",
            "instructions": [
                "A LON H"
            ]
        }
    ],
    "previous_state_encoded": "<to_saved_game_format>"
}
```

**Response:** 

```json
{
    "phase": "Summer 1901 Movements",
    "phase_type": "M",
    "phase_power_data": [
    {
      "home_centers_count": 3,
      "name": "AUSTRIA",
      "supply_centers_count": 3,
      "unit_count": 3
    }
    ],
    "svg_with_orders": "",
    "svg_adjudicated": "",
    "current_state": "<to_saved_game_format>",
    "possible_orders": [
        {
            "power": "FRANCE",
            "units": [
                {
                    "location": "KIE",
                    "instructions": [
                        "A"
                    ]
                }
            ]
        }
    ]
}
```

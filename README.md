# mapAPI v0.1

## [GET] /variants

```json
["standard", "ancient_mediterrean"]
```


## [GET] /variants/{variant-name}

**Response:** 
```json
{
    "name": "standard",
    "powers": [
        "FRANCE", "ENGLAND", "GERMANY"
    ] 
}

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
    "previous_state": "<to_saved_game_format>"
}
```

**Response:** 

```json
{
    "phase": "S1901M",
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

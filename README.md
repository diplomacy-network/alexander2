# mapAPI v0.1

## [GET] /variants

```json

```


## [GET] /variants/{variant-name}

```json

```

## [GET] /adjudicate/{variant-name}

Gets a basic game instance of a variant

## [POST] /adjudicate

### Request

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

### Response

```json
{
    "next_phase": "S1901M",
    "svg_with_orders": "",
    "svg_adjudicated": "",
    "current_state": "<to_saved_game_format>"
}
```

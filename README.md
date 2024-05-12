# alexander v0.4

Eine mapAPI für DNW2.0.

Zurzeit erreichbar unter [https://alexander2.vercel.app/v0.4](https://alexander2.vercel.app/v0.4).

## [GET] /variants

**Response:**
```json
{
  "variants": [
    {
      "default_end_of_game": 18,
      "name": "standard",
      "powers": [
        "AUSTRIA",
        "ENGLAND",
        "FRANCE",
        "GERMANY",
        "ITALY",
        "RUSSIA",
        "TURKEY"
      ]
    }
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
	"previous_state_encoded": "<current_state_encoded_as_base64>",
	"orders": [
    {
    "power": "FRANCE",
    "instructions": ["A MAR - SPA", "F BRE-PIC"]
    }
	],
	"scs_to_win": 18
}
```

**Response:** 

```json
{
  "applied_orders": [
    {
      "orders": [],
      "power": "AUSTRIA"
    },
    {
      "orders": [
        "A MAR - SPA",
        "F BRE - PIC"
      ],
      "power": "FRANCE"
    }
  ],
  "current_state_encoded": "<current_state_encoded_as_base64>",
  "phase_long": "FALL 1901 MOVEMENT",
  "phase_power_data": [
    {
      "home_center_count": 3,
      "power": "AUSTRIA",
      "supply_center_count": 3,
      "unit_count": 3
    }
  ],
  "phase_short": "F1901M",
  "phase_type": "M",
  "possible_orders": [
    {
      "power": "AUSTRIA",
      "units": [
        {
          "possible_orders": [
            "A BUD H"
          ],
          "space": "BUD"
        },
        {
          "possible_orders": [
            "F TRI - ALB"
          ],
          "space": "TRI"
        }
      ]
    }
  ],
  "svg_adjudicated": "<some_svg_file>",
  "svg_with_orders": "<some_svg_file_of_the_previous_phase_with_orders>",
  "winners": ["FRANCE", "RUSSIA"],
  "winning_phase": "W1901A"
}
```
## [POST] /dumbbot

**Request:** 

```json
{
    "current_state_encoded": "<to_saved_game_format_encoded_as_base64>",
    "power": "FRANCE"
}
```

**Response:** 

```json
{
  "orders": [
    "F BRE - ENG",
    "A MAR - PIE",
    "A PAR - BUR"
  ],
  "power": "FRANCE"
}
```

# alexander v0.3

Eine mapAPI für DNW2.0.

Zurzeit erreichbar unter http://alexander2.herokuapp.com/v0.3.

## [GET] /variants

**Response:**
```json
{
  "standard": {
    "default_end_of_game": 18,
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
    "orders": {
		"FRANCE": ["A PAR-BUR"]
	},
    "previous_state_encoded": "<to_saved_game_format_encoded_as_base64>",
    "scs_to_win": 18,
}
```

**Response:** 

```json
{
  "applied_orders": {
    "AUSTRIA": [],
    "ENGLAND": [],
    "FRANCE": [
      "A PAR - BUR"
    ],
    "GERMANY": [],
    "ITALY": [],
    "RUSSIA": [],
    "TURKEY": []
  },
  "current_state_encoded": "<current_state_encoded_as_base64>",
  "phase_long": "FALL 1901 MOVEMENT",
  "phase_power_data": {
    "AUSTRIA": {
      "home_center_count": 3,
      "supply_center_count": 3,
      "unit_count": 3
    }
  },
  "phase_short": "F1901M",
  "phase_type": "M",
  "possible_orders": {
    "AUSTRIA": {
      "BUD": [
        "A BUD S A VIE - TRI"
      ]
    }
  },
  "svg_adjudicated": "<some_svg_file>",
  "svg_with_orders": "<some_svg_file_of_the_previous_phase_with_orders>",
  "winners": [],
  "winning_phase": "W1901A",
}
```
## [POST] /dumbbot

**Request:** 

```json
{
    "current_state_encoded": "<to_saved_game_format_encoded_as_base64>",
    "power": "FRANCE",
}
```

**Response:** 

```json
{
  [
    "A MAR - PAR",
    "F PIC - BRE"
  ]
}
```

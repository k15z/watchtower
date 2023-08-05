"""
The Cards API is used to power the cards feature of the app.
"""
from typing import Any
from .structs import card_name_to_class


def handle_card(name: str, options: Any, user_id=None):
    if user_id:
        options["user_id"] = user_id
    return card_name_to_class[name].build(options)

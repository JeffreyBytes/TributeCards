"""
TributeCards - ESO Tales of Tribute Card Generator
Copyright (C) 2025 Jeffrey C (JeffreyBytes / spazzywit)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import json
from card import Card

def load_deck(deck_path, deck_name):
    """Loads a deck JSON file and returns a list of Card objects."""
    try:
        with open(deck_path, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"❌ Error loading {deck_name}: Invalid JSON format ({e})")
        return []
    except FileNotFoundError:
        print(f"❌ Error: Deck file {deck_path} not found!")
        return []

    # Convert JSON data to Card objects
    return [Card.from_json(card, deck_name) for card in data]
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
import logging
import os
from load_deck import load_deck

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

if __name__ == "__main__":
    deck_files = [f for f in os.listdir('decks') if f.endswith('.json')]

    for deck_file in deck_files:
        deck_name = os.path.splitext(deck_file)[0]
        deck_path = os.path.join('decks', deck_file)

        logging.info(f"📜 Loading deck: {deck_name} from {deck_file}")

        deck = load_deck(deck_path, deck_name)

        for card in deck:
            logging.info(f"  🎴 Generating card: {card.name}")
            card.generate_art()
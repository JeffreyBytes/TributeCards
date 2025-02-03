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

from PIL import Image, ImageDraw, ImageFont
import os
from constants import *

class Card:
    CARD_WIDTH, CARD_HEIGHT = 284, 493
    COST_ICON_WIDTH, COST_ICON_HEIGHT = 128, 128
    SUIT_ICON_WIDTH, SUIT_ICON_HEIGHT = 64, 64
    NAME_BANNER_WIDTH, NAME_BANNER_HEIGHT = 256, 64
    DEFEAT_BANNER_WIDTH, DEFEAT_BANNER_HEIGHT = 64, 64

    def __init__(self, name, art, type_, cost, health, effects, taunt=False, deck_name=None, display_name=None):
        self.name = name
        self.display_name = display_name
        self.art_filename = art                  # Just the filename, full path handled separately
        self.type = type_
        self.cost = cost
        self.health = health
        self.effects = effects
        self.taunt = taunt
        self.deck_name = deck_name.lower() if deck_name else None
        self.atlas = get_deck_atlas(self.deck_name) if self.deck_name else None

        # Paths
        self.PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        self.ASSETS_DIR = os.path.join(self.PROJECT_ROOT, '../assets')
        self.OUTPUT_DIR = os.path.join(self.PROJECT_ROOT, '../output')
        self.FONT_PATH = os.path.join(self.ASSETS_DIR, 'fonts', 'ProseAntique-Regular.ttf')

    @staticmethod
    def from_json(data, deck_name=None):
        """Creates a Card object from a JSON dictionary."""
        required_fields = ["name", "art", "type", "effects"]

        for field in required_fields:
            if field not in data:
                logging.warning(f"Missing {field} in card: {data.get('name', 'Unknown Card')}")
                return None

        return Card(
            name=data["name"],
            display_name=data.get("display_name", None),
            art=data["art"],
            type_=data["type"],
            cost=data["cost"],
            health=data.get("health"),          # Some cards don’t have health
            effects=data.get("effects", {}),    # Default to empty dictionary if missing
            taunt=data.get("taunt", False),     # Default False if missing
            deck_name=deck_name
        )

    def generate_art(self):
        """Generates a full card image with all components"""
        deck_output_dir = os.path.join(self.OUTPUT_DIR, self.deck_name.lower())

        if not os.path.exists(deck_output_dir):
            os.makedirs(deck_output_dir)

        atlas = self._load_deck_atlas()
        canvas = Image.new("RGBA", (self.CARD_WIDTH, self.CARD_HEIGHT), (0, 0, 0, 0))

        # Load and paste card components
        card_frame = self._load_card_frame(atlas)
        canvas.paste(card_frame, (0, 0))

        card_art = self._load_card_art()
        canvas.paste(card_art, self._get_art_position(), mask=card_art.split()[3])

        art_frame = self._load_card_frame_image()
        canvas.paste(art_frame, self._get_art_position(), mask=art_frame.split()[3])

        banner = self._load_banner()
        if banner:
            canvas.paste(banner, (0, 0), mask=banner.split()[3])

        defeat_banner = self._render_defeat_banner()
        if defeat_banner:
            canvas.paste(defeat_banner, self._get_defeat_banner_position(), mask=defeat_banner.split()[3])

        name_banner = self._render_name_banner()
        canvas.paste(name_banner, self._get_name_banner_position(), mask=name_banner.split()[3])

        if self.cost is not None:
            cost_icon = self._render_cost_icon()
            canvas.paste(cost_icon, self._get_cost_icon_position(), mask=cost_icon.split()[3])

        suit_icon = self._load_suit_icon(atlas)
        canvas.paste(suit_icon, self._get_suit_icon_position(), mask=suit_icon.split()[3])

        left_positions, right_positions, mechanics = self._get_mechanic_position(self.effects)

        for mechanic in mechanics:
            mechanic_canvas = self._render_mechanic_canvas(mechanic)

            mechanic_position = None

            if mechanic["trigger"] in ["play", "while_in_play"] and left_positions:
                mechanic_position = left_positions.pop(0)
            elif mechanic["trigger"] == "combo" and right_positions:
                mechanic_position = right_positions.pop(0)

            if mechanic_position is None:
                print(f"Warning: No available positions for mechanic {mechanic}")
                continue

            canvas.paste(mechanic_canvas, mechanic_position, mask=mechanic_canvas)

        # Save & Show
        # canvas.show()
        output_path = os.path.join(deck_output_dir, f"{self.deck_name.lower()}_{self.name.lower().replace(' ', '_')}.png")
        canvas.save(output_path)

    def _load_deck_atlas(self):
        atlas_filename = get_deck_atlas(self.deck_name)
        atlas_path = os.path.join(self.ASSETS_DIR, "patrons", atlas_filename)
        return Image.open(atlas_path)

    def _load_card_art(self):
        """Loads card art with the correct mask applied"""
        art_path = os.path.join(self.ASSETS_DIR, "cards", self.art_filename)
        art = Image.open(art_path)

        mask_filename = mask_filename = "tributecardframe_agent_mask.dds" if "Agent" in self.type else "tributecardframe_action_mask.dds"
        mask_path = os.path.join(self.ASSETS_DIR, mask_filename)
        mask = Image.open(mask_path).convert("L")
        art.putalpha(mask)
        return art

    def _load_card_frame(self, atlas):
        """Extracts the main card frame from the deck atlas"""
        return atlas.crop((0, 0, self.CARD_WIDTH, self.CARD_HEIGHT))

    def _load_card_frame_image(self):
        """Loads the card frame image (Agent/Action frame)"""
        frame_filename = "tributecardframe_agent.dds" if "Agent" in self.type else "tributecardframe_action.dds"
        frame_path = os.path.join(self.ASSETS_DIR, frame_filename)
        return Image.open(frame_path)

    def _load_banner(self):
        """Loads contract or curse banner"""
        if "Contract" in self.type or "Curse" in self.type:
            filename = "tributecardcontractbanner.dds" if "Contract" in self.type else "tributecardcursebanner.dds"
            path = os.path.join(self.ASSETS_DIR, filename)
            return Image.open(path).crop((0, 0, self.CARD_WIDTH, self.CARD_HEIGHT))
        return None

    def _load_name_banner(self):
        """Loads the name banner"""
        path = os.path.join(self.ASSETS_DIR, "tributecardnamebanner.dds")
        return Image.open(path)

    def _load_cost_icon(self):
        """Loads the correct cost icon"""
        filename = "tributecardcost_contract_1.dds" if "Contract" in self.type else "tributecardcost_1.dds"
        path = os.path.join(self.ASSETS_DIR, filename)
        return Image.open(path)

    def _load_defeat_banner(self):
        """Loads the defeat banner"""
        filename = "tributecarddefeatbanner_taunt.dds" if self.taunt else "tributecarddefeatbanner_health.dds"
        path = os.path.join(self.ASSETS_DIR, filename)
        return Image.open(path)

    def _load_suit_icon(self, atlas):
        """Extracts the suit icon from the deck atlas"""
        return atlas.crop((448, 0, 512, 64))

    def _draw_text(self, draw, text, font_size, position, color, shadow=False):
        """Draws text with an optional shadow"""
        font = ImageFont.truetype(self.FONT_PATH, font_size)
        x, y = position

        if shadow:
            draw.text((x + 2, y + 2), text, font=font, fill="black")
        draw.text((x, y), text, font=font, fill=color)

    def _render_name_banner(self):
        """Creates a separate canvas for the name banner with text"""
        name_text = self.name
        if self.display_name is not None:
            name_text = self.display_name

        banner = self._load_name_banner()

        # Create a new blank canvas for the name banner
        banner_canvas = Image.new("RGBA", (self.NAME_BANNER_WIDTH, self.NAME_BANNER_HEIGHT), (0, 0, 0, 0))
        banner_canvas.paste(banner, (0, 0), mask=banner.split()[3])

        # Draw the name text on this new canvas
        draw = ImageDraw.Draw(banner_canvas)
        font_path = os.path.join(self.ASSETS_DIR, 'fonts', 'ProseAntique-Bold.ttf')
        font = ImageFont.truetype(font_path, 20)

        # Center the text within the banner
        bbox = draw.textbbox((0, 0), name_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (self.NAME_BANNER_WIDTH - text_width) / 2
        text_y = (self.NAME_BANNER_HEIGHT // 2) - (text_height // 2) - 13       # TODO: finetune later

        draw.text((text_x, text_y), name_text, font=font, fill="black")

        # banner_canvas.show()

        return banner_canvas

    def _render_cost_icon(self):
        """Creates a separate canvas for the cost icon with text"""
        icon = self._load_cost_icon()

        # Create a new blank canvas for the cost icon
        cost_canvas = Image.new("RGBA", (self.COST_ICON_WIDTH, self.COST_ICON_HEIGHT), (0, 0, 0, 0))
        cost_canvas.paste(icon, (0, 0), mask=icon.split()[3])

        # Draw the cost text on this new canvas
        draw = ImageDraw.Draw(cost_canvas)
        font = ImageFont.truetype(self.FONT_PATH, 52)

        # Center the text within the cost icon
        bbox = draw.textbbox((0, 0), str(self.cost), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = ((self.COST_ICON_WIDTH - text_width) // 2)
        text_y = (self.COST_ICON_HEIGHT // 2) - (text_height // 2) - 7      # TODO: finetune later

        # Draw shadow for the text
        draw.text((text_x + 2, text_y + 2), str(self.cost), font=font, fill="black")

        # Draw actual white text on top
        draw.text((text_x, text_y), str(self.cost), font=font, fill="white")

        return cost_canvas

    def _render_defeat_banner(self):
        """Creates a separate canvas for the defeat (health) banner with text"""
        if "Agent" not in self.type:
            return None

        banner = self._load_defeat_banner()

        # Create a new blank canvas for the defeat banner
        defeat_canvas = Image.new("RGBA", (self.DEFEAT_BANNER_WIDTH, self.DEFEAT_BANNER_HEIGHT), (0, 0, 0, 0))
        defeat_canvas.paste(banner, (0, 0), mask=banner.split()[3])

        # Draw the defeat cost (health value) on this canvas
        draw = ImageDraw.Draw(defeat_canvas)
        font = ImageFont.truetype(self.FONT_PATH, 52)

        health_string = str(self.health)

        bbox = draw.textbbox((0, 0), health_string, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (self.DEFEAT_BANNER_WIDTH - text_width) // 2
        if self.taunt:
            text_y = (self.DEFEAT_BANNER_HEIGHT // 2) - (text_height // 2) - 7     # TODO: finetune these later
        else:
            text_y = (self.DEFEAT_BANNER_HEIGHT // 2) - (text_height // 2) - 13     # TODO: finetune these later

        draw.text((text_x + 2, text_y + 2), health_string, font=font, fill="black")
        draw.text((text_x, text_y), health_string, font=font, fill="white")

        # defeat_canvas.show()

        return defeat_canvas

    def _render_mechanic_canvas(self, mechanic):
        """Creates a 64x64 effect mechanic canvas with frame, icon, and number"""
        MECHANIC_SIZE = 64
        ICON_SIZE = 32
        PIP_SIZE = 16
        combo_level = None
        font_color = "black"

        if "combo" in mechanic["trigger"]:
            trigger = "combo"
        else:
            trigger = mechanic["trigger"]

        if "opponent_" in mechanic["type"]:
            if mechanic["trigger"] == "play":
                trigger = "setback_play"
            elif mechanic["trigger"] == "combo":
                trigger = "setback_combo"
            effect_type = mechanic["type"].replace("opponent_", "")
            font_color = "#8c0808"
        else:
            effect_type = mechanic["type"]
        effect_value = mechanic["value"]
        combo_level = mechanic.get("combo_level", None)

        frame_filename = MECHANIC_BANNERS.get(trigger)
        frame_path = os.path.join(self.ASSETS_DIR, 'mechanics', frame_filename)
        frame = Image.open(frame_path)

        icon_filename = MECHANIC_ICONS.get(effect_type)
        icon_path = os.path.join(self.ASSETS_DIR, 'mechanics', icon_filename)
        icon = Image.open(icon_path)

        mechanic_canvas = Image.new("RGBA", (MECHANIC_SIZE, MECHANIC_SIZE), (0, 0, 0, 0))
        mechanic_canvas.paste(frame, (0, 0), mask=frame.split()[3])

        icon_x = 3
        icon_y = (MECHANIC_SIZE - ICON_SIZE) // 2
        mechanic_canvas.paste(icon, (icon_x, icon_y), mask=icon.split()[3])

        if effect_value is not None:
            effect_text = str(effect_value)
            draw = ImageDraw.Draw(mechanic_canvas)
            font = ImageFont.truetype(self.FONT_PATH, 35)

            bbox = draw.textbbox((0, 0), effect_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            text_x = (MECHANIC_SIZE - text_width) // 2 + 11         # TODO: finetune later
            text_y = ((MECHANIC_SIZE - text_height) // 2) - 4       # TODO: finetune later

            draw.text((text_x, text_y), effect_text, font=font, fill=font_color)

        if combo_level and combo_level >= 3:
            pip_filename = COMBO_PIP_ICON
            pip_path = os.path.join(self.ASSETS_DIR, 'mechanics', pip_filename)
            pip = Image.open(pip_path)

            num_pips = combo_level - 2

            if num_pips == 1:
                pip_x = (MECHANIC_SIZE - PIP_SIZE) // 2
                pip_y = MECHANIC_SIZE - PIP_SIZE
                mechanic_canvas.paste(pip, (pip_x, pip_y), mask=pip.split()[3])
            else:
                pip_layer = Image.new("RGBA", (MECHANIC_SIZE, MECHANIC_SIZE), (0, 0, 0, 0))

                for i in range(num_pips):
                    pip_x = ((MECHANIC_SIZE - (num_pips * PIP_SIZE)) // 2) + (i * PIP_SIZE)
                    pip_y = MECHANIC_SIZE - PIP_SIZE
                    pip_layer.paste(pip, (pip_x, pip_y), mask=pip.split()[3])

                if pip_layer.size != mechanic_canvas.size:
                    print(f"⚠️ Warning: Pip layer size mismatch. Expected {mechanic_canvas.size}, got {pip_layer.size}")

                mechanic_canvas.paste(pip_layer, (0, 0), mask=pip_layer.split()[3])

        # mechanic_canvas.show()
        return mechanic_canvas

    # Position Helpers
    def _get_art_position(self):
        return ((self.CARD_WIDTH - 256) // 2, (self.CARD_HEIGHT - 512) // 2)

    def _get_name_banner_position(self):
        return (self.CARD_WIDTH - self.NAME_BANNER_WIDTH) // 2, 402 - (self.NAME_BANNER_HEIGHT // 2) + 15

    def _get_cost_icon_position(self):
        return ((self.CARD_WIDTH - self.COST_ICON_WIDTH) // 2, 51 - (self.COST_ICON_HEIGHT // 2) + 2)

    def _get_cost_text_position(self):
        return (self.CARD_WIDTH - 52) // 2, 51 - (52 // 2)    # 52 is font size

    def _get_suit_icon_position(self):
        return self.CARD_WIDTH - self.SUIT_ICON_WIDTH - 2, 73

    def _get_defeat_banner_position(self):
        if self.taunt:
            return (self.CARD_WIDTH - self.DEFEAT_BANNER_WIDTH) // 2, self._get_name_banner_position()[1] + (self.NAME_BANNER_HEIGHT // 2) + 5
        else:
            return (self.CARD_WIDTH - self.DEFEAT_BANNER_WIDTH) // 2, self._get_name_banner_position()[1] + (self.NAME_BANNER_HEIGHT // 2)

    def _get_mechanic_position(self, effects):
        """Calculates positions for play/while-in-play (left) and combo (right) mechanics."""
        MECHANIC_SPACING = 0
        MECHANIC_START_Y = 134

        left_positions = []
        right_positions = []
        left_y = MECHANIC_START_Y
        right_y = MECHANIC_START_Y

        mechanics = []

        for effect_type, effect_list in effects.items():
            for effect in effect_list:
                if effect_type == "while_in_play":
                    mechanics.append({"trigger": "while_in_play", "type": effect["effect"]["type"], "value": effect["effect"]["value"]})
                else:
                    mechanics.append({"trigger": "combo" if "combo" in effect_type else effect_type, "type": effect["type"], "value": effect["value"], "combo_level": int(
                        effect_type.replace("combo", "")) if "combo" in effect_type else None})

        for mechanic in mechanics:
            if mechanic["trigger"] in ["play", "while_in_play"]:
                left_positions.append((6, left_y))
                left_y += 64 + MECHANIC_SPACING
            elif mechanic["trigger"] == "combo":
                right_positions.append((self.CARD_WIDTH - 6 - 64, right_y))
                right_y += 64 + MECHANIC_SPACING

        return left_positions, right_positions, mechanics
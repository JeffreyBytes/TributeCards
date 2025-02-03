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

from enum import Enum

# ----------------------------
# Card Type Enum
# ----------------------------
class CardType(Enum):
    ACTION = "Action"
    CONTRACT_ACTION = "Contract Action"
    AGENT = "Agent"
    CONTRACT_AGENT = "Contract Agent"
    CURSE = "Curse"
    CONTRACT_CURSE = "Contract Curse"

# ----------------------------
# Card Frame Mapping
# ----------------------------
CARD_FRAMES = {
    CardType.ACTION: "tributecardframe_action.dds",
    CardType.CONTRACT_ACTION: "tributecardframe_action.dds",
    CardType.AGENT: "tributecardframe_agent.dds",
    CardType.CONTRACT_AGENT: "tributecardframe_agent.dds",
    CardType.CURSE: "tributecardframe_action.dds",
    CardType.CONTRACT_CURSE: "tributecardframe_action.dds"
}

# ----------------------------
# Card Banners (for Contract & Curse cards)
# ----------------------------
CARD_BANNERS = {
    CardType.CONTRACT_ACTION: "tributecardcontractbanner.dds",
    CardType.CONTRACT_AGENT: "tributecardcontractbanner.dds",
    CardType.CONTRACT_CURSE: "tributecardcontractbanner.dds",
    CardType.CURSE: "tributecardcursebanner.dds"
}

# ----------------------------
# Cost Images (contract vs. regular)
# ----------------------------
CARD_COST_IMAGES = {
    "default": "tributecardcost_1.dds",
    "contract": "tributecardcost_contract_1.dds"
}

# ----------------------------
# Agent Health Banners (Taunt vs. Normal)
# ----------------------------
AGENT_HEALTH_BANNERS = {
    "taunt": "tributecarddefeatbanner_taunt.dds",
    "normal": "tributecarddefeatbanner_health.dds"
}

# ----------------------------
# Mechanic Icons
# ----------------------------
MECHANIC_ICONS = {
    "gain_power": "tributemechaniccarddisplay_gainresources_0.dds",
    "gain_coin": "tributemechaniccarddisplay_gainresources_1.dds",
    "gain_prestige": "tributemechaniccarddisplay_gainresources_2.dds",
    "donate": "tributemechaniccarddisplay_donatecards.dds",
    "confine": "tributemechaniccarddisplay_confinecards.dds",
    "bonus_patron": "tributemechaniccarddisplay_bonuspatroninteraction.dds",
    "draw": "tributemechaniccarddisplay_drawcards.dds",
    "ko_agent": "tributemechaniccarddisplay_koagent.dds",
    "ko_agent_all": "tributemechaniccarddisplay_koallagents.dds",
    "refresh": "tributemechaniccarddisplay_refreshcards.dds",
    "destroy_cards": "tributemechaniccarddisplay_destroycards.dds",
    "choose_one": "tributemechaniccarddisplay_chooseone.dds",
    "replace": "tributemechaniccarddisplay_cullfromdocks.dds",
    "create": "tributemechaniccarddisplay_createcards.dds",
    "discard": "tributemechaniccarddisplay_discardcards.dds",
    "acquire": "tributemechaniccarddisplay_acquirecards.dds",
    "toss": "tributemechaniccarddisplay_tosscards.dds"
}

# ----------------------------
# Mechanic Banners (Play, Combo, While in Play)
# ----------------------------
MECHANIC_BANNERS = {
    "play": "tributemechaniccardframe_activation_large_single.dds",
    "while_in_play": "tributemechaniccardframe_trigger_large_single.dds",
    "combo": "tributemechaniccardframe_combo_large_single.dds",
    "setback_play": "tributemechaniccardframe_activation_large_single_negative.dds",
    "setback_combo": "tributemechaniccardframe_combo_large_single_negative.dds"
}

# ----------------------------
# Combo Pip for Combos > 2
# ----------------------------
COMBO_PIP_ICON = "tributemechaniccombopip_full.dds"

# ----------------------------
# Deck Atlas Mapping
# ----------------------------
DEFAULT_ATLAS_DECK = "generic"
DECK_ATLAS = {
    "almalexia": "tributebackdrop_almalexia_2.dds",
    "mora": "tributebackdrop_mora_2.dds",
    "stalessia": "tributebackdrop_stalessia_2.dds",
    "blackfeather": "tributepatronsuitatlas_blackfeather_2.dds",
    "druid": "tributepatronsuitatlas_druid.dds",
    "generic": "tributepatronsuitatlas_generic.dds",
    "hlaalu": "tributepatronsuitatlas_hlaalu_2.dds",
    "hunding": "tributepatronsuitatlas_hunding_2.dds",
    "orgnum": "tributepatronsuitatlas_orgnum_2.dds",
    "pelin": "tributepatronsuitatlas_pelin_2.dds",
    "psijic": "tributepatronsuitatlas_psijic_2.dds",
    "rajhin": "tributepatronsuitatlas_rajhin_2.dds",
    "redeagle": "tributepatronsuitatlas_redeagle_2.dds",
}


def get_deck_atlas(deck_name):
    """Returns the correct atlas filename for the given deck"""
    deck_name = deck_name.lower()

    if deck_name in DECK_ATLAS:
        return DECK_ATLAS.get(deck_name)
    else:
        return DECK_ATLAS.get(DEFAULT_ATLAS_DECK)
from random import choice

from resources.weapons import Weapons

from bots import ABCBot


class Bot(ABCBot):
    """
    A bot to fire anything at anyone but itself
    """

    def action(self, country_status: dict, world_state: dict):
        weapon_choices = list(Weapons)
        if not self.has_nukes(country_status):
            # If you don't have nukes don't try firing them
            weapon_choices.remove(Weapons.NUKE)

        # Don't shoot yourself please...
        target_choices = world_state["alive_players"]
        target_choices.remove(country_status["ID"])

        # Fire!
        if target_choices:
            target = choice(tuple(target_choices))
            weapon = choice(weapon_choices)

            return {
                "Weapon": weapon,
                "Target": target,
                "Type": "Attack",
            }

        return {}

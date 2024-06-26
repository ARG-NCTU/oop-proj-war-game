from random import choice
from resources.weapons import Weapons
from bots import ABCBot


class Bot(ABCBot):
    """
    An opportunist which tries to kill the person with the most nukes,
    Unfortunately that may be itself.
    """

    def action(self, country_status: dict, world_state: dict):
        # Fire at...
        target = self.pick_target(world_state)

        # Select a weapon
        weapon = choice(list(Weapons))

        return {
            "Weapon": weapon,
            "Target": target,
            "Type": "Attack",
        }

    @staticmethod
    def pick_target(world_state: dict):
        """
        Return a country ID
        """

        nuke_count = {}
        for i in world_state["alive_players"]:
            nuke_count[i] = world_state["countries"][i]["Nukes"]

        max_nuke = max([nuke_count[i] for i in nuke_count])

        target_choices = []
        for i in world_state["alive_players"]:
            if world_state["countries"][i]["Nukes"] == max_nuke:
                target_choices.append(i)

        target = choice(target_choices)
        return target

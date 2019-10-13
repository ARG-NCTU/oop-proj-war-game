#!/usr/bin/python3

from copy import deepcopy
from typing import List
from resources import weapons
from os.path import abspath, dirname
import importlib
import os
import time


class Country:
    DEFAULT_HEALTH = 100
    DEFAULT_RESOURCES = 100
    NUKE_STOCKPILE = 1

    def __init__(self, player_class):
        self.alive = True
        self.health = self.DEFAULT_HEALTH
        self.resources = self.DEFAULT_RESOURCES
        self.nukes = self.NUKE_STOCKPILE
        self.player = player_class()


    def action(self, world_state):
        # Format action before appending
        country_status = self.serialize()

        action = self.player.action(deepcopy(country_status), deepcopy(world_state))
        action["Source"] = self.id

        if "Action" in action:
            if action["Action"] == weapons.Weapons.NUKE:  # Nuke
                action["Success"] = self.nukes > 0

                if action["Success"]:
                    self.nukes -= 1
            else:
                action["Success"] = True

        return action


    def serialize(self):
        country_status = {
            "Alive": self.alive,
            "Health": self.health,
            "ID": self.id,
            "Resources": self.resources,
            "Nukes": self.nukes
        }

        return country_status


    def take_damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.health = 0


class Game:
    MAX_TURNS = 30

    def __init__(self, countries: List[Country]):
        self.countries = countries
        self.events = []

        # Initialize ids
        for i, country in enumerate(self.countries):
            country.id = i

        self.turn = 1


    def start(self):
        while (self._get_alive_count() > 1
               and self.turn <= self.MAX_TURNS):

            print("Round", self.turn)
            actions = self._get_actions()
            self._run_actions(actions)
            self._print_events()
            self.turn += 1

        if self._get_alive_count() == 1:
            alive = self._get_alive_countries()[0]
            print(self.countries[alive].name, "is the last one standing.")

        else:
            print("There were no survivors.")

        print("Hit enter to exit.")
        input()

    def _get_alive_count(self):
        """ Returns an integer """
        return sum(country.alive for country in self.countries)


    def _get_alive_countries(self):
        """ Returns indexes """
        return [pos for pos, country in enumerate(self.countries) if country.alive]


    def _get_world_state(self):
        return {
            "countries": self._serialize_countries(),
            "events": self.events,
            "alive_players": self._get_alive_countries()
        }


    def _get_actions(self):
        actions = []
        world_state = self._get_world_state()

        for i, country in enumerate(self.countries):
            if not country.alive:
                continue

            action = country.action(world_state)

            # Check if action is valid
            # If action is invalid, nuke own country
            if not self._is_valid_action(action):
                action = {}

            actions.append(action)

        return actions


    def _is_valid_action(self, action):
        try:
            if "Action" not in action:
                return True

            return all((
                action["Action"] in weapons.Weapons,
                action["Target"] in self._get_alive_countries()
            ))
        except KeyError as e:
            print("KeyError", e)
            return False


    def _serialize_countries(self):
        countries = []
        for country in self.countries:
            countries.append(country.serialize())

        return countries

    def _run_actions(self, actions):
        self.events = []
        alive = self._get_alive_countries()

        for action in actions:
            if "Action" in action and action["Action"] in weapons.Weapons:
                self.events.append(action)

                if action["Success"]:
                    damage = action["Action"].value.DAMAGE
                    self.countries[action["Target"]].take_damage(damage)


        # Kill players who died this turn
        for player in alive:
            if self.countries[player].health == 0:
                self.countries[player].alive = False
                self.events.append({
                    "Action": "Death",
                    "Source": player
                })

    def _print_events(self):
        def name(id):
            return self.countries[id].name

        for event in self.events:
            source = name(event["Source"])

            if "Target" in event:
                target = name(event["Target"])
            else:
                target = None

            if "Action" not in event:
                if target:
                    print(source, "decided to wait and stared at", target)
                else:
                    print(source, "decided to wait.")

            elif event["Action"] == weapons.Weapons.LASER:  # LASER
                print(source, "fired a laser at", target)

            elif event["Action"] == weapons.Weapons.MISSILE:  # Missile
                print(source, "fired a missile at", target)

            elif event["Action"] == weapons.Weapons.NUKE:
                print(source, "fired a nuke at", target)

                if not event["Success"]:
                    print("But they ran out of nukes.")

            elif event["Action"] == "Death":
                print(source, "is dead!")

        time.sleep(1)


def get_bots():
    # Dynamically import bots in bots directory to BOTS dictionary
    BOTS = {}  # A dictionary of bot names to Bot classes
    bots = os.path.join(abspath(dirname(__file__)), "bots")
    for file in os.listdir(bots):
        if not file.endswith(".py"):
            continue

        name = file.replace(".py", "")
        module = "." + name
        BOTS[name] = importlib.import_module(module, "bots").Bot

    return BOTS


def get_countries():
    BOTS = get_bots()

    countries = []
    for name in BOTS:
        bot_class = BOTS[name]
        country = Country(bot_class)
        country.name = name
        countries.append(country)

    return countries


def main():
    countries = get_countries()
    active_game = Game(countries)
    active_game.start()


if __name__ == "__main__":
    main()

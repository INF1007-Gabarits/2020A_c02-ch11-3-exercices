"""
Chapitre 11.3

Classes pour représenter un magicien et ses pouvoirs magiques.
"""


import random

import utils
from character import *


class Spell(Weapon):
	def __init__(self, name, power, mp_cost, min_level):
		super().__init__(name, power, min_level)
		self.mp_cost = mp_cost

class Magician(Character):
	def __init__(self, name, max_hp, max_mp, attack, magic_attack, defense, level):
		super().__init__(name, max_hp, attack, defense, level)
		self.magic_attack = magic_attack
		self.__mp = max_mp
		self.spell = None
		self.using_magic = False

	@property
	def mp(self):
		return self.__mp

	@mp.setter
	def mp(self, val):
		self.__mp = utils.clamp(val, 0, self.max_hp)

	@property
	def spell(self):
		return self.__spell

	@spell.setter
	def spell(self, val):
		if val is not None and val.min_level > self.level:
			raise ValueError()
		self.__spell = val

	def compute_damage(self, other):
		if self.will_use_spell():
			self.mp -= self.spell.mp_cost
			return self._compute_magical_damage(other)
		else:
			return self._compute_physical_damage(other)

	def will_use_spell(self):
		return self.using_magic and self.spell is not None and self.mp >= self.spell.mp_cost

	def _compute_magical_damage(self, other):
		return Character.compute_damage_output(
			self.level + self.magic_attack,
			self.spell.power,
			1,
			1,
			1/8,
			(0.85, 1.00)
		)

	def _compute_physical_damage(self, other):
		return Character.compute_damage_output(
			self.level,
			self.weapon.power,
			self.attack,
			other.defense,
			1/16,
			(0.85, 1.00)
		)


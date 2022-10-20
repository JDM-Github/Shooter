import ast
import json
from os import makedirs, path, remove
from jcryptor import JCryptor
from configuration import SAVE_GAME
from file_formatter import Formatter
from random import randint, randrange

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.uix.widget import Widget
from design import HealthBar, CoinBar, Coin, LiveBar
from menu import MenuButton
from character.playable import Ship
from character.enemy import EnemyShip01


class GameWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_variable()
        self.all_json_load()
        self.all_widget()
        self.setup_window()
        self.start_loop()

    def start_loop(self):
        self.start_clock = Clock.schedule_interval(self.game_loop, 1.0/60.0)

    def game_loop(self, dt):
        if self.start_game and self.pause_game is False:
            self.delta_time = dt
            self.time_factor = self.delta_time*60
            if not self.player.main_lives <= 0:
                if self.player in self.player_parent.children:
                    self.player.update()
                else:
                    self.player.ship_revive()
                self.generate_enemy()
            self.update_loop(self.all_enemy.children, "update", True)
            self.update_loop(self.player_all_bullet.children, "update")
            self.update_loop(self.enemy_all_bullet.children, "update")
            self.update_loop(self.all_coin.children, "update")

            self.health_bar.update_health(
                self.player.main_health, self.player.original_health)

    def update_loop(self, iterable, func, check=False):
        for object in iterable:
            getattr(object, func)()
            if check:
                self.check_if_hit_enemy(object)

    def check_if_hit_enemy(self, enemy):
        if self.player in self.player_parent.children:
            if enemy.collide_widget(self.player):
                enemy.main_health -= self.player.main_damage
                if enemy.main_health <= 0:
                    enemy.drop_on_dead()
                self.player.check_if_can_damage(enemy.main_damage)
                enemy.hurt_animation()

    def setup_window(self):
        self._get_key_binding()
        self._keyboard = Window.request_keyboard(self._keyboard_close, self)
        self._keyboard.bind(on_key_down=self._keyboard_down_key)
        self._keyboard.bind(on_key_up=self._keyboard_up_key)
        Window.bind(on_request_close=self.exit_window)

    def exit_window(self, *_):
        self.save_progress()
        App.get_running_app().stop()
        Window.close()
        return True

    def _keyboard_close(self):
        self._keyboard.unbind(on_key_down=self._keyboard_down_key)
        self._keyboard.unbind(on_key_up=self._keyboard_up_key)
        self._keyboard = None

    def _get_key_binding(self):
        self.move_boost = self.key_binding["BOOST"]
        self.move_fire = self.key_binding["FIRE"]
        self.move_up = self.key_binding["UP"]
        self.move_down = self.key_binding["DOWN"]
        self.move_left = self.key_binding["LEFT"]
        self.move_right = self.key_binding["RIGHT"]

    def _keyboard_down_key(self, _, key, *__):
        if key[1] == "escape":
            self.exit_window()
        if key[1] in self.key_binding.values():
            self.start_game = True
        if key[1] == self.move_boost:
            self.player.move_boost = True
        elif key[1] == self.move_fire:
            self.player.move_attack = True
        elif key[1] == self.move_up:
            self.player.move_up = True
            self.player.move_down = False
        elif key[1] == self.move_down:
            self.player.move_down = True
            self.player.move_up = False
        elif key[1] == self.move_left:
            self.player.move_left = True
            self.player.move_right = False
        elif key[1] == self.move_right:
            self.player.move_right = True
            self.player.move_left = False

    def _keyboard_up_key(self, _, key, *__):
        if key[1] == self.move_boost:
            self.player.move_boost = False
        elif key[1] == self.move_fire:
            self.player.move_attack = False
        elif key[1] == self.move_up:
            self.player.move_up = False
        elif key[1] == self.move_down:
            self.player.move_down = False
        elif key[1] == self.move_left:
            self.player.move_left = False
        elif key[1] == self.move_right:
            self.player.move_right = False

    def all_json_load(self):
        self.game_progress = self.load_json(self.resource_json) \
            if not path.exists(self.save_resource_des) else json.loads(self.formatter.convert_bin_to_string(
                self.save_resource_des, self.cryptor))
        self.ship_attributes = self.load_json(self.ship_json) \
            if not path.exists(self.save_ship_des) else json.loads(self.formatter.convert_bin_to_string(
                self.save_ship_des, self.cryptor))
        self.ship_upgrade = self.load_json(self.ship_upgrade_json) \
            if not path.exists(self.save_ship_upgrade) else json.loads(self.formatter.convert_bin_to_string(
                self.save_ship_upgrade, self.cryptor))
        self.key_binding = self.load_json(self.keybind_json)

    def load_json(self, json_file):
        with open(json_file) as f:
            return json.load(f)

    def set_cryptor_key(self, key=None):
        if key is None:
            self.cryptor.generate_new_key()
        self.formatter.save_encrypted_bin_file(
            self.save_key_des, str(self.cryptor.get_key()))
        self.cryptor.set_key(ast.literal_eval(self.formatter.convert_bin_to_string(
            self.save_key_des)))
        self.delete_progress()
        self.create_progress()

    def create_progress(self):
        self.formatter.save_encrypted_bin_file(
            self.save_ship_des, self.ship_json, self.cryptor)
        self.formatter.save_encrypted_bin_file(
            self.save_resource_des, self.resource_json, self.cryptor)
        self.formatter.save_encrypted_bin_file(
            self.save_ship_upgrade, self.ship_upgrade_json, self.cryptor)

    def delete_progress(self):
        if path.exists(self.save_ship_des):
            remove(self.save_ship_des)
        if path.exists(self.save_resource_des):
            remove(self.save_resource_des)
        if path.exists(self.save_ship_upgrade):
            remove(self.save_ship_upgrade)

    def save_progress(self):
        self.save_progress_auto(self.save_resource_des, self.game_progress)
        self.save_progress_auto(self.save_ship_des, self.ship_attributes)
        self.save_progress_auto(self.save_ship_upgrade, self.ship_upgrade)

    def save_progress_auto(self, des, progress):
        self.formatter.save_encrypted_bin_file(
            des, json.dumps(progress), self.cryptor)

    def setup_progress(self):
        if not path.isdir("progress"):
            makedirs("progress")

        self.cryptor = JCryptor()
        self.formatter = Formatter()

        self.ship_json = "all_json/ship.json"
        self.resource_json = "all_json/resource.json"
        self.keybind_json = "all_json/keybinding.json"
        self.ship_upgrade_json = "all_json/ship_upgrade.json"

        self.save_key_des = "progress/" + \
            self.formatter.convert_string_to_bin("key")
        self.save_ship_upgrade = "progress/" + \
            self.formatter.convert_string_to_bin("upgrade")
        self.save_ship_des = "progress/" + \
            self.formatter.convert_string_to_bin("ship")
        self.save_resource_des = "progress/" + \
            self.formatter.convert_string_to_bin("resource")
        if path.exists(self.save_key_des) and SAVE_GAME:
            try:
                self.cryptor.set_key(ast.literal_eval(self.formatter.convert_bin_to_string(
                    self.save_key_des)))
            except ValueError:
                self.set_cryptor_key()
        else:
            self.set_cryptor_key()

    def all_variable(self):
        self.setup_progress()
        self.start_game = False
        self.pause_game = False
        self.game_variable()

    def game_variable(self):
        self.minimum_cd = 8
        self.maximum_cd = 15
        self.game_enemy_cooldown = self.get_enemy_cooldown()

    def get_enemy_cooldown(self) -> float:
        return randrange(self.minimum_cd, self.maximum_cd, 1) / 10

    def all_widget(self):
        self.player = Ship(self.ship_attributes,
                           self.ship_upgrade, "S-01", self)
        self.player_parent = Widget()
        self.player_parent.add_widget(self.player)
        self.all_enemy = Widget()
        self.player_all_bullet = Widget()
        self.enemy_all_bullet = Widget()
        self.all_coin = Widget()

        self.menu_button = MenuButton()
        self.health_bar = HealthBar()
        self.coin_bar = CoinBar()
        self.live_bar = LiveBar(self.player.main_lives)

        self.add_widget(self.all_enemy)
        self.add_widget(self.player_parent)
        self.add_widget(self.all_coin)
        self.add_widget(self.player_all_bullet)
        self.add_widget(self.enemy_all_bullet)

        self.add_widget(self.health_bar)
        self.add_widget(self.coin_bar)
        self.add_widget(self.menu_button)
        self.add_widget(self.live_bar)

        self.coin_bar.value = self.game_progress["Coin"]

    def restart_game(self):
        pass

    def generate_enemy(self):
        if self.game_enemy_cooldown <= 0:
            self.game_enemy_cooldown = self.get_enemy_cooldown()
            self.all_enemy.add_widget(EnemyShip01(self))
        self.game_enemy_cooldown -= self.delta_time

    def drop_on_dead(self, pos=None, value=50):
        self.all_coin.add_widget(Coin(pos, value))

from random import randint
import requests, datetime
from datetime import timedelta

class Trainer:
    def __init__(self, username):
        self.username = username

class Pokemon:
    pokemons = {}

    def __init__(self, trainer):
        self.lasttime = datetime.now()
        self.trainer = trainer
        self.pokemon_number = randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.weight, self.height = self.get_weight_height()
        self.happiness = 0 
        self.power = randint(30, 60)
        self.hp = randint(200, 400)
        Pokemon.pokemons[trainer.username] = self

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['sprites']['front_default']
        return None
    
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['forms'][0]['name']
        return "Pikachu"

    def get_weight_height(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['weight'], data['height']
        return None, None

    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()  
        delta_time = timedelta(second = feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.lasttime = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.lasttime + delta_time}"  

    def info(self):
        return (
            f"Имя покемона: {self.name}, "
            f"Вес: {self.weight}, Рост: {self.height}, "
            f"Уровень счастья: {self.happiness}, "
            f"Сила: {self.power}, Здоровье: {self.hp}, "
            f"Тренер: {self.trainer.username}"
        )
    
    def show_img(self):
        return self.img

    def attack(self, enemy):
        if enemy.hp > 0:
            damage = min(enemy.hp, self.power)  # Убедимся, что здоровье не станет отрицательным
            enemy.hp -= damage
            return f"""Сражение @{self.trainer.username} с @{enemy.trainer.username}
Здоровье @{enemy.trainer.username} теперь {enemy.hp}"""
        else:
            return f"Покемон @{enemy.trainer.username} уже побежден!"

class Wizard(Pokemon):
    def info(self):
        return "У тебя покемон-волшебник \n\n" + super().info()

class Fighter(Pokemon):
    def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой: {super_power}"

    def info(self):
        return "У тебя покемон-боец \n\n" + super().info()

# Пример использования
trainer1 = Trainer("Ash")
trainer2 = Trainer("Misty")

wizard = Wizard(trainer1)
fighter = Fighter(trainer2)

print(wizard.info())
print("#" * 10)
print(fighter.info())
print("#" * 10)

print(wizard.attack(fighter))
print(fighter.attack(wizard))

# Кормим покемонов
wizard.feed()
fighter.feed()

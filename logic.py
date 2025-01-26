from random import randint
import requests

class Pokemon:
    pokemons = {} # { username : pokemon}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()

        self.power = randint(30, 60)
        self.hp = randint(200, 400)

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']["other"]['official-artwork']["front_default"])
        else:
            return "https://static.wikia.nocookie.net/anime-characters-fight/images/7/77/Pikachu.png/revision/latest/scale-to-width-down/700?cb=20181021155144&path-prefix=ru"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"


    # Метод класса для получения информации
    def info(self):
        return f"""Имя твоего покеомона: {self.name}
Cила покемона: {self.power}
Здоровье покемона: {self.hp}"""

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
    
    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1,5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"""Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}
Здоровье @{enemy.pokemon_trainer} теперь {enemy.hp}"""
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

class Wizard(Pokemon):
    """Подкласс Pokemon, представляющий покемона-волшебника."""

    def info(self):
        """Возвращает информацию о покемоне-волшебнике."""
        return "У тебя покемон-волшебник \n\n" + super().info()
class Fighter(Pokemon):
    """Подкласс Pokemon, представляющий покемона-бойца."""

    def attack(self, enemy):
        """Атака с использованием супер-удара."""
        super_power = randint(5, 15)  # Генерируем дополнительную силу атаки
        self.power += super_power  # Увеличиваем силу атаки перед ударом
        result = super().attack(enemy)  # Вызываем стандартную атаку
        self.power -= super_power  # Возвращаем силу атаки к изначальному значению
        return result + f"\nБоец применил супер-атаку силой: {super_power} "

    def info(self):
        """Возвращает информацию о покемоне-бойце."""
        return "У тебя покемон-боец \n\n" + super().info()
# Создаём двух покемонов: волшебника и бойца
wizard = Wizard("username1")
fighter = Fighter("username2")

# Выводим информацию о покемонах
print(wizard.info())
print("#" * 10)
print(fighter.info())
print("#" * 10)

# Проводим сражение между покемонами
print(wizard.attack(fighter))
print(fighter.attack(wizard))
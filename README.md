# PenaltyLeagueGame

**PenaltyLeague** is an engaging penalty shootout game built using Python and the Pygame library. The game simulates the thrill of a penalty shootout, where players must score as many goals as possible. This project incorporates an Object-Relational Mapping (ORM) system tailored specifically for the game, a State design pattern for managing game states, and comprehensive tests using pytest.

## Table of Contents

- [Installation](#installation)
- [Running the Game](#running-the-game)
- [Object-Relational Mapping (ORM)](#object-relational-mapping-orm)
- [State Design Pattern](#state-design-pattern)
- [Testing with pytest](#testing-with-pytest)
- [Customization and Usage](#customization-and-usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started with **PenaltyLeague**, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/PenaltyLeague.git
    cd PenaltyLeague
    ```

2. **Install Python:**

    Ensure you have Python 3.8+ installed. You can download it from the [official Python website](https://www.python.org/downloads/).

3. **Set up a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Game

To run the game, execute the following command:

```bash
python -m src.main
```
This will launch the PenaltyLeague game window where you can start playing.

## Object-Relational Mapping (ORM)
The game uses a custom ORM system to manage and persist game data such as player scores, match history, and settings. This ORM simplifies interactions with the database, allowing for easy storage and retrieval of game data.

#### Example ORM Usage

```python
from src.models.orm_models import Model

class CustomePlayerGameModel(Model):
    db_fields_to_lookup = ['_id', 'name', 'team', 'points']

    def __init__(self, name=None, team=None, points=0):
        super().__init__()
        self.name = name
        self.team = team
        self.points = points
```
init new table
```bash
python -m src.db.db_init
```
```python

# Creating a new player
player = CustomePlayerGameModel(name="John Doe", team="Team A")
player.save().execute()

# Querying player data
players = CustomePlayerGameModel.query_creator.all().execute()
for p in players:
    print(p.name, p.team)

```

## State Design Pattern
The State design pattern is implemented to manage different states in the game, such as the SeasonState, MatchWeekState, PenaltyShootOutState, and AfterMatchState. This pattern allows the game to transition smoothly between different states, ensuring a flexible and scalable design. You can also create and add your own custom states to further extend the game’s functionality.

#### Example State Pattern Usage
```python
import os

from src.game_states.abstract import GameState
from src.game_states.season_page import SeasonPage
from src.ui_components.buttons.base_button import BaseBtn
from src.ui_components.colors import DARK_GRAY, WHITE
from src.settings import BASE_DIR, WINDOW_HEIGHT, WINDOW_WIDTH


class NewPage(GameState):
    def __init__(self, game, pygame, screen):
        super().__init__(game, pygame, screen)
        self.font = self.pygame.font.Font(None, 36)
        self.next_btn = BaseBtn(width=500, height=100, background=WHITE, color=DARK_GRAY, font=self.font, text="Next Page")

    def get_buttons(self):
        return (
            (
                self.next_btn,
                lambda: self.game.change_state(SeasonPage(self.game, self.pygame, self.screen))
            ),
        )

    def update(self):
        pass

    def draw(self):
        self.draw_background_image(path_dir_list=['assets', 'img', 'my-background.jpeg'])
        self.screen.blit(background_image, (0, 0))
        self.next_btn.draw(screen=self.screen, x=(WINDOW_WIDTH // 2) - self.next_btn.width // 2, y=WINDOW_HEIGHT // 2)
        self.pygame.display.flip()
```

## Testing with pytest
Tests are written using the pytest framework to ensure the reliability and correctness of the game. The tests cover various aspects of the game, including state transitions, ORM functionality, and gameplay mechanics.

#### Running Tests
To run the tests, simply execute:
```bash
pytest
```

This will discover and run all tests in the tests/ directory.

## Customization and Usage
PenaltyLeague is designed to be easily customizable. You can modify the game rules, add new features, or change the game's appearance. As we mentioned before, you can customize game models and game states. You can also add your own static elements, as well as animated elements.
##### Example Customization
Add static Elements
```python
from .abstract import StaticGameSprite
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH

class NewStaticEl(StaticGameSprite):
    def __init__(self, pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 15), image_path=['assets', 'img', 'Static', '1.png'], size=(430, 220)):
        super().__init__(pos, image_path, size)
```
Add animated Elements
```python
from .abstract import GameSprite

class NewAnimationEl(GameSprite):
    animation_speed = 0.3

    def __init__(self, start_pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50),
                       image_path=['assets', 'img', 'animation'],
                       start_size=(350, 280)):
        super().__init__(start_pos, image_path, start_size)
        self.animation = True

    def _get_rect(self):
        return self.image.get_rect(bottomleft=self.current_position)

    def end_animate_sequence(self):
        super().end_animate_sequence()
        self.animation = False
```
Add this elements into NewPage
```python
class NewPage(GameState):
    def __init__(self, game, pygame, screen):
        super().__init__(game, pygame, screen)
        self.font = self.pygame.font.Font(None, 36)
        self.next_btn = BaseBtn(width=500, height=100, background=WHITE, color=DARK_GRAY, font=self.font, text="Next Page")
        self.new_static_el = NewStaticEl()
        self.new_animation_el = NewAnimationEl()
        self.all_sprites = self.pygame.sprite.Group()
        self.all_sprites.add(self.new_static_el)
        self.all_sprites.add(self.new_animation_el)
    ...
    def update(self):
        self.new_animation_el.update()

    def draw(self):
        self.draw_background_image(path_dir_list=['assets', 'img', 'my-background.jpeg'])
        self.screen.blit(background_image, (0, 0))
        self.next_btn.draw(screen=self.screen, x=(WINDOW_WIDTH // 2) - self.next_btn.width // 2, y=WINDOW_HEIGHT // 2)
        self.all_sprites.draw(self.screen)
        self.pygame.display.flip()
```

You can also extend existing classes or create new ones to add more functionality.

#### Adding Custom Football Club
```python
from .models.game_models import FootballClub

class CustomFootballClub(FootballClub):
    db_fields_to_lookup += ['skill_level']
    def __init__(self, title=None, potential=None, logo=None,
                 points=0, mood=5, games=0, wins=0, draws=0, losses=0, computer=1,
                 skill_level=5):
        super().__init__(title=None, potential=None, logo=None, points=0, mood=5, games=0, wins=0, draws=0, losses=0, computer=1)
        self.skill_level = skill_level

    def compare_skils(self):
        # Custom ogic
        pass
```
init new table
```bash
python -m src.db.db_init
```
Using the custom FootballClub
```python
new_football_club = CustomFootballClub(title="New", potential=30, logo='new_logo.png',skill_level=8)
new_football_club.save().execute()
```
Customization teams in `teams.config.json` file
```json
{
    "My_New_Team": {
        "logo": "new_logo.png",
        "potential": 100,
        "computer": 0
    },
    "Second_team": {
        "logo": "3.png",
        "potential": 19,
        "computer": 1
    },
    "Middle_team": {
        "logo": "4.png",
        "potential": 9,
        "computer": 1
    },
    "Last_team": {
        "logo": "5.png",
        "potential": 5,
        "computer": 1
    }
}
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an Issue if you have any ideas or bug reports.

#### Fork the repository 
1. **Create your feature branch** `git checkout -b feature/AmazingFeature`
2. **Commit your changes**
`git commit -m 'Add someAmazingFeature'`
3. **Push to the branch** `git push origin feature/AmazingFeature`
4. **Open a Pull Request**

## License
This project is licensed under the MIT License - see the LICENSE file for details.
```
This comprehensive `README.md` file provides detailed instructions and explanations for installation, usage, testing, customization, and contributing to the **PenaltyLeague** project.
```
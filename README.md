# Air Traffic Control

#### Video Demo: https://drive.google.com/file/d/18gXRZaoK89c7Phy1pobEfeIxZjyoX_P-/view?usp=sharing

## Project Overview

Air Traffic Control is a Python terminal game in which the player takes the role of an air traffic controller. The goal is to guide incoming aircraft to the runway and safely land 10 aircraft before anything goes wrong.

Each aircraft has a randomly generated codename, a distance from the runway, a speed, an amount of fuel, and a status that indicates whether it is inbound, returning, or holding. The player interacts with the game through simple text commands such as `wait`, `inspect`, `land`, `hold`, and `resume`.

The game is designed to make the player think about timing and planning rather than simply reacting to one aircraft at a time. Aircraft continue moving after each turn, new aircraft can enter the airspace, fuel decreases over time, and aircraft must not occupy the same distance at the same time. The player therefore has to decide when to let an aircraft continue, when to place it on hold, and when it is safe to land it.

## How the Game Works

At the beginning of the game, three aircraft are created with distinct distances and codenames. On each turn, aircraft that are not holding move according to their speed, while aircraft on hold remain in position but continue using fuel.

An aircraft can land when its distance from the runway reaches `0`. Aircraft can approach the runway from either direction. Movement stops exactly at `0` for that turn, even if the aircraft's speed would otherwise skip over zero. Its direction stays the same, so if it is not landed or held, it continues past the runway on the next turn. Negative distances indicate that an inbound aircraft has passed the runway. The player can then use `return CODENAME` to change its direction and bring it back toward the runway.

The player can use `hold CODENAME` to stop an aircraft from moving and `resume CODENAME` to allow it to move again. This gives the player some control over the timing of aircraft and helps prevent collisions.

The game ends if an aircraft runs out of fuel or if two aircraft occupy the same distance. The player wins after successfully landing 10 aircraft.

## Commands

- `wait` — advance the game by one turn.
- `inspect CODENAME` — display the aircraft's distance, fuel, speed, and codename.
- `land CODENAME` — land an aircraft when it is at the runway.
- `hold CODENAME` — place an aircraft on hold.
- `resume CODENAME` — allow a held aircraft to move again.
- `return CODENAME` — turn an aircraft back toward the runway after it has passed into negative distances.
- `help` — display the available commands.
- `quit` — exit the game.

## Files

### `project.py`

This is the main program. It contains the `main` function and the game's classes and functions.

The `Aircraft` class represents each aircraft and stores its state. Its methods handle aircraft movement and determine whether an aircraft can land.

The additional functions in `project.py` handle tasks such as finding an aircraft by codename, displaying the current game state, advancing a turn, checking for dangerous situations, creating new aircraft, and checking whether the player has won.

### `test_project.py`

This file contains the project's automated tests. The tests are written for `pytest` and check important parts of the program independently from playing the game manually.

Testing is particularly useful for this project because aircraft movement involves several possible states, including holding, moving toward the runway, reaching zero, and moving back in the opposite direction.

### `requirements.txt`

This file lists `pytest`, which is needed to run the automated tests. The game itself only uses the standard library.

### `.gitignore`

This file prevents unnecessary local files and folders from being included in the project repository.

### `README.md`

This file explains the project, its design, how the game works, and the purpose of each project file.

## Design Decisions

One of the main design decisions was to represent each aircraft as an object using the `Aircraft` class. This keeps the information belonging to one aircraft together and makes it easier to manage multiple aircraft at the same time.

Randomness is used when aircraft are created so that each game can be different. Distance, speed, fuel, and codenames are generated automatically. Each aircraft starts with enough fuel to reach the runway directly and still have at least one unit left. Holding or returning uses additional fuel, so the player still needs to plan carefully. At the same time, the movement system is designed so that every aircraft can eventually reach the runway rather than generating an aircraft that is mathematically unable to land.

The `holding` attribute was added to give the player a meaningful decision to make. Holding an aircraft stops its movement but does not stop the passage of time completely, since fuel continues to decrease. This means holding an aircraft can be useful, but it also has a cost.

The game uses separate functions for different responsibilities instead of putting all of the logic inside `main`. This makes the program easier to understand, test, and modify.

## Running the Program

Make sure Python is installed, then run:

```bash
python project.py
```

To run the automated tests, install `pytest` if necessary and run:

```bash
pytest
```

The project itself uses Python's standard library for its game logic, including `random` and `sys`.

## Goal

The goal of the project was to build a complete Python program rather than a collection of isolated exercises. Air Traffic Control combines object-oriented programming, functions, conditionals, loops, randomization, user input, error handling, and automated testing into one interactive terminal game.

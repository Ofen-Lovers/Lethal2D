# Lethal2D

**Lethal2D** is a 2D top-down survival-exploration game built with Python and Pygame. Inspired by the popular game *Lethal Company*, Lethal2D tasks players with exploring abandoned moons, collecting scrap, and returning to their ship to meet an ever-increasing profit quota—all while avoiding dangerous entities.

<img width="1008" height="564" alt="image" src="https://github.com/user-attachments/assets/e933c4cf-eaf1-4d78-a6d1-dd4d842002d0" />

## Game Overview
In Lethal2D, you play as a contract worker for "The Company." Your objective is simple but dangerous:
1. **Land** on a moon.
2. **Explore** abandoned buildings and collect valuable scrap.
3. **Return** to your ship before midnight.
4. **Deposit** loot to reach your quota and live another day.

## Gameplay Mechanics

<img width="903" height="593" alt="image" src="https://github.com/user-attachments/assets/6b5a080b-771a-4150-92fe-7a717f8684d6" />

- **Dynamic Environments**: Move between different rooms including your **Spaceship** (home base), the **Moon** surface, and the **Abandoned Building**.
- **Time Management**: Monitor the in-game clock. If the day ends at midnight and you haven't met the quota, it's game over.
- **Inventory System**: You can carry up to 5 items at a time. Manage your value and weight efficiently.
- **Increasing Difficulty**: As you meet quotas, the profit expectations and enemy spawn rates increase, making every day faster and more challenging.
- **Enemies & Pathfinding**: Watch out for "Hoarder Bugs" and other entities. They don't have a health system yet, but touching one will make you drop all your hard-earned loot.

## Controls

<img width="1022" height="574" alt="image" src="https://github.com/user-attachments/assets/dc021c4c-2138-4e78-9f6f-3ad8b136159e" />

- **Movement**: `W`, `A`, `S`, `D` or Arrow Keys.
- **Collect Scrap**: `Space` when standing over an item.
- **Drop Loot at Ship**: `G` while inside the spaceship.
- **Room Transition**: Press `1` or `2` at portals/doors (depending on destination).

## Technical Details
### Data Structures and Algorithms
- **A* Pathfinding**: The hoarding bugs utilize the **A* Algorithm** to chase the player efficiently. This uses a Euclidean distance heuristic for optimized shortest-path calculation.
- **Scene Management**: A dictionary-based system manages transitions between the Spaceship, Moon, and Building rooms.
- **Inventory Management**: Implemented using list data structures for efficient item tracking and weight calculation.

### Design Assets
All sprites, including the player character, enemies (Hoarder Bugs), and various scrap items (horns, gold bars, mugs, stop signs, etc.), were custom-designed using **Aseprite**.

## Project Motivation
This project was developed to recreate the immersive and challenging essence of *Lethal Company* in a 2D space. It serves as a demonstration of applying complex algorithms (like A*) and structured game design using the Pygame library.

## Contributors
Developed by **Group 3 - CS2B**:
- **Krystal Bacalso**
- **Chas Madlos**
- **Shaira Dadios**
- **Joseph Deysolong**
- **Javier Raut**

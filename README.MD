# 🕹️ Pygame Tetris Clone

A classic **Tetris game** implemented in **Python** using the **Pygame** library.

This project is a functional clone of the popular puzzle game where the player must rotate and move falling geometric shapes (Tetriminos) to create complete horizontal lines, which are then cleared, scoring points.

## ✨ Features

* **Classic Gameplay**: Contains all seven standard Tetriminos (I, J, L, O, S, T, Z).
* **Rotations and Movement**: Full control over piece movement (Left, Right, Down) and rotation.
* **Soft Drop**: Pressing 'Down' speeds up the fall rate.
* **Hard Drop**: Pressing 'Space' instantly drops the piece to the bottom.
* **Line Clearing**: Automatically clears completed rows.
* **Scoring**: Simple scoring system based on lines cleared.
* **High Score Tracking**: Stores the highest score in a local `highscore.txt` file.
* **Next Piece Display**: Shows the next piece to fall.
* **Game Over**: Detects when the stack reaches the top.

---

## 🛠️ Installation

### Prerequisites

You need to have **Python** installed on your system.

### 🎮 Controls

| Key | Action |
| :--- | :--- |
| **Left Arrow** | Move piece **left** |
| **Right Arrow** | Move piece **right** |
| **Down Arrow** | **Soft drop** (move piece down faster) |
| **Up Arrow** | **Rotate** piece (clockwise) |
| **Spacebar** | **Hard drop** (instant drop to the bottom) |
| **Window Close** | Quit the game |

### Dependencies

This project requires the **Pygame** library. You can install it using `pip`:

```bash
pip install pygame
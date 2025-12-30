# 🐍 Snake Game Using Python

A classic **Snake Game** built using **Python** and the **Turtle graphics library**, following an **Object-Oriented Programming (OOP)** approach.
The player controls a snake using keyboard arrow keys and tries to eat apples to increase the score while avoiding collisions.

---
<img width="1342" height="276" alt="Image" src="https://github.com/user-attachments/assets/cc673758-00dc-4f0b-ba2f-c88acab9db3a" />

## 📌 About the Project

This project recreates the traditional **Snake Game**, where:
- The snake moves in four directions: **Up, Down, Left, Right**
- An apple appears randomly on the screen
- Each apple eaten increases the **score** and **snake length**
- The game ends if:
  - The snake hits the **boundary**
  - The snake collides with **its own tail**

This project focuses on **OOP concepts**, game logic, and GUI development using Python.

---

## 🎮 Game Controls

| Key | Action |
|----|-------|
| ⬆️ Up Arrow | Move Up |
| ⬇️ Down Arrow | Move Down |
| ⬅️ Left Arrow | Move Left |
| ➡️ Right Arrow | Move Right |

---

## 🖥️ Game Specifications

- Screen size: **400 × 400 pixels**
- Grid size: **20 × 20**
- Graphics library: **Turtle**
- Programming language: **Python**

---

## 🧠 Object-Oriented Design

The game is implemented using **Object-Oriented Programming**.

### Main Classes:
- **Snake**
  - Handles movement and direction
  - Manages tail growth
  - Detects wall and self-collision
- **Apple**
  - Appears at random locations
  - Respawns after being eaten

Both classes inherit from Python’s built-in `turtle.Turtle` class.

---

## ▶️ How to Run the Game

### Requirements
- Python **3.10 or above**
- Turtle module (comes pre-installed with Python)

### Steps to Run
```bash
python snake_game.py
```

⚠️ **Note:**  
Run the game from **Command Prompt or PowerShell**, not from restricted IDE terminals.

---

## 📂 Project Structure

```
Snake-Game/
│── snake_game.py
│── README.md
```

---

## 🏁 Game Rules

- Eat apples to increase score
- Avoid touching the walls
- Avoid colliding with your own body
- Game resets after collision

---

## 🚀 Future Enhancements

- Increasing difficulty levels
- Sound effects
- High score saving
- Speed control
- Pygame-based version

---

## 📚 Concepts Used

- Python Object-Oriented Programming (OOP)
- Turtle Graphics
- Event handling
- Collision detection
- Game loop logic

---

## 👨‍💻 Author

**Himanshu Patle**  
📍 Nagpur, India  

⭐ If you like this project, don’t forget to star the repository!

---

## 📜 License

This project is open-source and intended for **educational purposes**.

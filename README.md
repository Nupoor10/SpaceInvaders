# 👾 Pixel Siege

An intense, infinitely scaling 8-bit retro arcade shooter built with Phaser 3. Defend your sector against an ever-growing, color-coded armada of enemy ships, collect weapon drops, and fight to claim the high score.

This project was built as part of a **Finish-Up-A-Thon**, breathing new life into an older, archived Python game codebase by completely rewriting it from scratch using modern web technologies and a fully modular architectural pattern.

---

## 🚀 Play Now
* **Live Deployment:** [Insert your hosting link here]

---

## 🕹️ How to Play

* **[ ARROW KEYS ]** - Move Ship (Full 8-directional movement)
* **[ SPACEBAR ]** - Fire Lasers

### 📦 Power-Ups & Drops
Enemies have a **10% chance** to drop a tactical capsule upon destruction. You must physically navigate your ship to collect them:
* 🟢 **Green Drops:** Upgrades your weapon system to dual-firing **Double Lasers**.
* 🔴 **Red Drops:** Emergency hull repairs. Instantly restores **20 Health** (Capped at 100 HP).
* *Note: Taking damage from an enemy ship instantly strips away your weapon upgrades!*

### 🛸 Enemy Intel & Scoring
* **Blue Ships (10 pts):** Swift scout ships. Standard health (1 HP), moving straight down.
* **Green Ships (20 pts):** Agility interceptors. Standard health (1 HP), weaving horizontally in a sinusoidal pattern.
* **Red Ships (50 pts):** Heavy kamikaze dreadnoughts. Armor plating (2 HP). They descend to mid-screen before executing a high-speed diagonal charge directly at your position.

---

## 🛠️ Architecture & Tech Stack

* **Game Engine:** Phaser 3 (Arcade Physics System)
* **Language:** Modern JavaScript (ES6+ Modules)
* **Configuration & Meta:** Node.js / npm

### Code Modularization
The game has been completely decoupled from a single global state file into a production-ready, object-oriented structure:
1. `index.html` - The application entry point utilizing ES6 modules (`type="module"`).
2. `main.js` - Global Phaser game initialization and scene registration.
3. `MenuScene.js` - Handles asset preloading, splash UI, instruction text, and retro title audio looping.
4. `GameScene.js` - Scoped entirely within a Phaser Class. Drives the main game loop, performance-optimized pool management (automatic clean-up of off-screen lasers/enemies), dynamic text tweens, and frame-accurate collision metrics via `postupdate` event hooks.

---

## 📈 Mechanics & Design Choices

### Infinite Wave Scaling (Anti-Overlap System)
Unlike traditional level-locked arcade games, *Pixel Siege* utilizes a procedurally scaling wave generator. Every 5 seconds, a new wave spawns with an increased enemy count. The ship deployment uses a precise **250ms stagger delay** to guarantee that massive end-game waves drop gracefully without overlapping or generating artificial performance walls.

### Target Management Shift
Rather than forcing players to dodge dozens of incoming projectiles, this version shifts the mechanical core to physical target priority. Enemies act as kamikaze threats, turning the screen into a puzzle of positioning, target management, and risk-versus-reward as you decide whether to dive into danger to grab a vital health drop.

---

## 📦 Setup & Local Development

To run this game locally without CORS browser blockages, you should serve it via a local web server:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pixel-siege.git
   ```
2. Navigate into the directory:
   ```bash
   cd pixel-siege
   ```
3. Boot up a local static server (using an extension like VS Code's Live Server, or via npm):
   ```bash
   npx serve .
   ```
4. Open the provided localhost link in your browser.

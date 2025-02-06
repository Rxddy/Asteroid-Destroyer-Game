# Asteroid Destroyer

Asteroid Destroyer is a space-themed shooter game built with Python using the **Turtle** and **Pygame** libraries. The game allows you to control a spaceship, shoot missiles at enemies, and avoid obstacles. The objective is to score as many points as possible while surviving against waves of enemies.

## Features
- **Player Controls**: 
  - **A**: Turn Left
  - **D**: Turn Right
  - **Up Arrow**: Accelerate
  - **Down Arrow**: Decelerate
  - **Spacebar**: Fire Missiles
- **Enemies**: Shoot or avoid enemy ships.
- **Allies**: Collect allies to earn extra points, but be cautious of collisions.
- **Game Over**: The game ends when all lives are lost.
- **Cheat**: Press `0` to instantly gain extra lives and score points (for testing purposes).

## How to Play

1. **Movement**:
   - Press **A** to turn left.
   - Press **D** to turn right.
   - Press the **Up Arrow** to accelerate.
   - Press the **Down Arrow** to decelerate.
   
2. **Firing**:
   - Press **Spacebar** to fire missiles at enemies.

3. **Game Over**:
   - The game ends when your lives reach 0.

4. **Cheat Mode**:
   - Press **0** to add extra lives and increase the score (for testing purposes).

## Installation

### Requirements
- Python 3.x
- Pygame (for sound and game-related operations)
  
### Steps to Install

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/asteroid-destroyer.git

Navigate into the project folder:

bash
cd asteroid-destroyer
Install the required Python libraries:

bash
pip install pygame
Download the necessary game assets (images and sounds):

images/: For sprite images (e.g., enemy.gif, ally.gif, background.gif).
sounds/: For sound effects (e.g., laser.mp3, explosion.mp3).
Place these files in their respective folders within the project directory.

Run the game:

bash
python main.py
File Structure
main.py: The main game script with all the game logic.
images/: Contains game sprites (e.g., enemy.gif, ally.gif).
sounds/: Contains sound effects (e.g., laser.mp3, explosion.mp3).

Contributing
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.

License
This project is open-source and available under the MIT License.

yaml
---
This version is visually organized with markdown formatting for easy readability. Just copy and paste it into your GitHub repository's README file. You can also replace the placeholder (`your-username`) with your GitHub username, and add any additional custom details you want!

🚀 Running the Game on macOS with Wine
To run this game on macOS, you'll need to install Wine, a compatibility layer that allows you to run Windows applications on macOS. Follow the steps below to set it up.

Step 1: Install Homebrew
Homebrew is a package manager for macOS that makes it easy to install software. Follow these steps to install Homebrew:

Open the Terminal app (press Command + Space, type "Terminal", and hit Enter).
Run the following command to install Homebrew:
sh
Copy
Edit
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Once the installation is complete, follow the on-screen instructions to finish setting up Homebrew.
Step 2: Install Wine
Now that you have Homebrew installed, use it to install Wine:

In the Terminal, run:
sh
Copy
Edit
brew install --cask wine-stable
Wine will be installed on your system. You can verify this by running:
sh
Copy
Edit
wine --version
Step 3: Locate Your .exe File
Find your .exe file (the game or installer you want to run).
Use Finder to navigate to the folder where your .exe file is located.
If you're unsure of the file's location, right-click on the file and select Get Info to see the full path.
Step 4: Run the Game
Open Terminal.

Navigate to the folder containing the .exe file using the cd command. Example:

sh
Copy
Edit
cd /path/to/your/game
Example for Desktop:

sh
Copy
Edit
cd ~/Desktop
Run the game using Wine:

sh
Copy
Edit
wine gamefile.exe
Example:

sh
Copy
Edit
wine mygame.exe
Or, if you prefer not to navigate directories, provide the full path:

sh
Copy
Edit
wine /Users/yourusername/Desktop/mygame.exe
🛠 Troubleshooting
If you get errors or need further help, check the Wine FAQ for additional troubleshooting.
Make sure your .exe file is compatible with Wine (some Windows applications may not run smoothly).








# Conway's Game of Life - Interactive Python Application
This project is an interactive implementation of **Conway's Game of Live**, built with *Python* and *Tkinter*. It provides a dynamic environment for simulating and experimenting with the cellular automaton game.
## Table of Contents
1. [Overwiew](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [File Import/Export](#file-importexport)
6. [Configuration](#configuration)
7. [Contribution](#contributing)
8. [License](#license)
https://github.com/user-attachments/assets/50af5f9d-1aa8-4c99-bb54-32d4a5c09bb3


### Overview
Conway's Game of Life is a zero-player game where cells on a grid live, die, or evolve based on simple rules. This application provides a user-friendly interface to:
- Set initial cell states
- Change the simulation rules
- Import and export configurations
- Adjust the display with zoom and pan features
### Features
- **Interactive Control Panel**: Start, pause, clear, save and load cell configurations.
- **Rule Customization**: Modify survival and birth conditions.
- **Zoom & Pan**: Use the mouse to zoom in/out and pan across the grid.
- **Real-time Simulation**: Run the game at a user-defined speed (FPS - Frames Per Second)
- **Responsive Interface**: Optimized UI for seamless cell interactions and rule adjustments.
### Installation
Ensure you have Python 3.x installed. Then follow these steps:
1. Clone the repository:
   ```
   git clone https://github.com/Falanger-debug/Conway-s-Game-of-Life.git
   cd Conway-s-Game-of-Life
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```
### Usage
Once launched, the application window provides:
- **Canvas**: Displays the grid, where you can click to add/remove cells.
- **Controls**:
  - **Start/Pause**: Toggles the simulation.
  - **Clear**: Resets the grid.
  - **Load**: Load a saved configuration (.csv format, ```(0,0) == top left cell```)
  - **Save**: Save the current cell configuration to a .csv file.
  - **Rules**: Select rule presets for the game.
  - **FPS**: Choose the frames per second for simulation speed.
### File Import/Export
- **Save**: Exports live cell positions to a .csv file. Each line contains the x and y coordinates of a cell.
- **Load**: Imports a .cv file with x, y coordinates, setting those cells as live.
  **File format**:
  ```
  x1, y1
  x2, y1
  ...
  ```
### Configuration
Settings can be adjusted via the ```settings.py``` file
- **Grid Size** ```WIDTH```, ```HEIGHT```: Adjusts grid dimensions.
- **Cell Size** ```CELL_SIZE```: Defines the default display size of each cell.
- **Rules** ```RULES```: Modify birth and survival conditions.
- **Colors**: Customize the background, cell color and grid color
### Contributing
1. Fork the repository.
2. Create a new branch ```"git checkout -b feature-branch```.
3. Make changes, commit them and push to your fork.
4. Open a pull request with a clear description of your changes.
## License
This project is licensed under the MIT License.
   


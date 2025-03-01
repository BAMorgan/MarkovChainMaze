# MazeMarkov - Agent Transitions using Markov Chains

## Overview
This project models an **agent’s movement in a maze** using a **Markov Chain**. The agent moves randomly based on transition probabilities, and the program analyzes **state probabilities over time**, determines the **steps to reach a goal**, and computes the **steady-state distribution**. The **transition matrix** updates dynamically, and **multiple paths** are visualized.

## Features
- Supports **10×10** and **custom-sized** mazes  
- Implements **Markov transitions** with a dynamic **transition matrix**  
- Computes **probability distribution after each step**  
- Tracks **steps needed to reach the goal state**  
- Displays **agent paths and transition matrices**  
- Supports **loop percentage settings** (0% or 50%)  

## Usage
Run the program with the following command:
```sh
python MazeRunner.py [size] [loopperc]
```
**Example:**
```sh
python MazeRunner.py 10 50
```
- **size** = Maze size (e.g., 10 for 10×10)  
- **loopperc** = 0 (no loops) or 50 (50% loops)  

## Markov Model Implementation
- **Transition Matrix**: Defines movement probabilities based on open paths.  
- **State Evolution**: Computes probability of being in each cell after `n` steps.  
- **Goal Search**: Determines `n` steps required to reach the goal.  
- **Steady-State Analysis**: Calculates long-term probability distribution.  

## Outputs
1. **GUI Output**: Visualizes up to **three possible paths** to the goal.  
2. **Console Output**:  
   - Transition matrix after every **10 steps**  
   - Steps required to reach goal  
   - Transition matrix at goal state  
   - **(Optional)** Steady-state transition matrix  

## Requirements
- Python 3.x  
- Required libraries: `numpy`, `pygame`, `random`, `pyamaze`  

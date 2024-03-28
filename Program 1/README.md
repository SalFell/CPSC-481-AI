Sokoban is a puzzle game where the player has to move boxes into storage locations with some obstacles in between.

## Input Format

* O - Obstacle
* S - Storage
* B - Block
* R - Robot

## GUI Format

* Grey - Obstacle
* Green - Storage
* Blue - Block
* Red - Robot

## Running the program

The program currently uses input.txt as the input file to read the game board. There are multiple game boards you can copy and paste from inputs.txt into input.txt to see how the program performs with varying situations. Please make sure there is only one game board in input.txt during run time, the program has not been tested to work with multiple game boards per run.

Please use the following command in the terminal to run the program.

```
python SokobanSolver.py
```

or

```
python3 SokobanSolver.py
```

Once the game board has been solved by the algorithm, a GUI window will pop up prompting you to input the file that holds the game board so you may see it be solved with the solution previously provided by the algorithm. Please use input.txt for this input. Use of a different game board for the GUI will result in a misrepresentation of the solution, i.e. the algorithm's solution may show the Player/Bot performing unwanted behavior like moving through boxes and obstacles. 


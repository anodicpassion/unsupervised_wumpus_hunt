# Unsupervised Wumpus Hunt

## Abstract
The Wumpus world is a cave which has 4/4 rooms connected with passageways. So there are total 16 rooms which are connected with each other. We have a knowledge-based agent who will go forward in this world. The cave has a room with a beast which is called Wumpus, who eats anyone who enters the room. The Wumpus can be shot by the agent, but the agent has a single arrow. In the Wumpus world, there are some Pits rooms which are bottomless, and if agent falls in Pits, then he will be stuck there forever. The exciting thing with this cave is that in one room there is a possibility of finding a heap of gold. So the agent goal is to find the gold and climb out the cave without fallen into Pits or eaten by Wumpus. The agent will get a reward if he comes out with gold, and he will get a penalty if eaten by Wumpus or falls in the pit.

<center>
  <img width="300" alt="Screenshot 2024-12-27 at 9 54 03 PM" src="https://github.com/user-attachments/assets/e3c10d66-0553-40c8-9910-37e0b10d6268" />
</center>

## Installation 

### 1] Clone the repository:

```git clone https://github.com/anodicpassion/unsupervised_wumpus_hunt.git```

### 2] Install the requirements:

`cd unsupervised_wumpus_hunt`
 
  * Windows:
    `pip install requirements.txt`
 
  * Linux | MacOS:
    `pip3 install requirements.txt`


### 3] Run the GUI application:
* Windows:
  ```python Wumpus_GUI.py```

* Linux | MacOS:
  ```python3 Wumpus_GUI.py```

## GUI glimpse

<center>
  <img width="500" alt="Screenshot 2024-12-27 at 9 54 03 PM" src="https://github.com/user-attachments/assets/840a8389-f311-410b-9188-77145bc9728f" />
</center>


## Controls:

### Move: 
To move the agent through the caves, click on the grids with highlighted cells. The text in the cell represents the surrounding that AI agent can sence in that particular cell.

### Kill Wumpus:
To kill the Wumpus, AI agent has got only one arrow. The arrow can only kill the wumpus if it is pointed in the correct direction. The arrow can move only one cell in that particular direction. Use the direction buttons given in the control pannel to throw arrow towards wumpus.

### Grab the Gold:
To grab the gold use the Grab button in the control pannel.

## Future Scope:
* Developing an AI agent which is aware of its environment and can make moves to achieve the highest score possible.

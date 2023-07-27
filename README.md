# Flappy Bird Game with NEAT

## Description

This is a Flappy Bird game implemented using Python and the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. NEAT is an evolutionary algorithm that evolves neural networks to play the game and achieve higher scores over time. The game aims to demonstrate how an AI agent can learn to play Flappy Bird through evolutionary computation.


## How to Play

- Clone the repository to your local machine.
- Install the required dependencies by running: `pip install -r requirements.txt`
- Run the Flappy Bird game with NEAT by executing: `python flappy_bird_neat.py`
- The game will launch, and the AI will start learning to play Flappy Bird automatically using NEAT.
- Sit back and watch as the AI improves its performance over generations!

## NEAT Implementation Details

The NEAT algorithm works by evolving a population of neural networks. The neural networks control the bird's actions in the game. Each neural network represents a bird and is initially assigned random weights for its connections.

- The neural networks are evaluated based on their performance in the game. Birds that achieve higher scores are more likely to be selected for reproduction.
- The selected neural networks undergo crossover and mutation to produce offspring with new combinations of weights.
- The process of evaluation, selection, crossover, and mutation continues over generations until the AI improves its ability to play the game effectively.

## Repository Structure

- `Game.py`: The main Python script that implements the Flappy Bird game and integrates NEAT for AI learning.
- `config.txt`: Configuration file for NEAT, containing parameters for the evolutionary algorithm.
-

## Dependencies

The game requires the following Python packages:

- `pygame`: For building the game environment.
- `NEAT-Python`: For implementing the NEAT algorithm.


## Contributions

Contributions to the project are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or create a pull request.

Happy gaming and AI learning!

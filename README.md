# Initial State - EON-1 Orbital Mission

A simple gravitational orbit simulation game built with Python and Pygame.

## Game Background

In a distant future, Earth has become uninhabitable. You are the orbital engineer in charge of launching a space station colony called EON-1 into a stable orbit around a new host star. With limited fuel and no engines after launch, your only tool is the gravitational pull of the sun. The survival of your people depends entirely on whether you can place the colony in a safe and stable orbit.

This simulation is inspired by the N-body problem, but simplified to a single sun and one orbiting satellite for clarity and playability.

## Game Objective

Launch the space colony EON-1 into orbit using a single mouse drag to set its initial velocity. Once released, the only force acting on it is gravity from the central star. Your goal is to survive in a stable orbit for 10 in-game years without crashing into the star or drifting off into space.

## How to Play

1. **Launch Phase:**
   - Click on screen to place the colony
   - Click and drag to define the launch vector (direction and speed)
   - Release the mouse to launch

2. **Simulation Phase:**
   - Watch as your colony orbits the central star
   - Monitor the years survived and distance from the star
   - Try to maintain a stable orbit for 10 years

3. **Game Rules:**
   - If the colony crashes into the sun: game over
   - If the colony escapes the gravitational field (off screen): game over
   - If the colony survives for 10 years in orbit: you win!

## Installation and Running

1. Make sure you have Python and Pygame installed:
   ```
   pip install pygame
   ```

2. Run the game:
   ```
   python initial_state.py
   ```

## Controls

- **Mouse Click**: Place colony
- **Mouse Drag**: Set launch velocity and direction
- **R or Space**: Restart game (after win/loss)

## Physics

The game uses simplified Newtonian physics:
- Gravitational force: F = G * m1 * m2 / r²
- Acceleration: a = F / m
- Position and velocity updates via time steps

## Tips

- A stable orbit requires the right balance of speed and distance
- Too close to the star and you'll burn up
- Too far and you'll drift into deep space
- The perfect orbit is nearly circular

## Development

This game was developed using Amazon Q CLI as part of the "Build Games with Amazon Q CLI" campaign. Amazon Q provided assistance with code generation, debugging, and implementation of physics-based gameplay mechanics.

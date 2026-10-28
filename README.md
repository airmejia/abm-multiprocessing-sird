
# CPU Performance Evaluation for Multiprocessing Agent-Based Simulations

## Overview

This repository provides a Python-based Agent-Based Model (ABM) for evaluating CPU performance through parallel epidemiological simulations.

The project focuses on measuring multiprocessing efficiency, execution time, and computational variability across different processor architectures.

Researchers, students, and developers are invited to execute the simulation on their hardware and voluntarily share their results to support a collaborative performance evaluation study.

## Simulation Model

The simulation implements an epidemiological SIRD model using autonomous agents that move and interact within a two-dimensional environment.

Each agent can transition between the following epidemiological states:

- **S — Susceptible**
- **I — Infected**
- **R — Recovered**
- **D — Deceased**

The model uses stochastic interactions to simulate disease transmission and population dynamics.

## Computational Implementation

The simulation is implemented in Python using the `multiprocessing` library.

Multiple independent simulation runs are distributed across available worker processes, allowing the evaluation of parallel execution performance.

The program records:

- CPU and OS name 
- Individual simulation execution times.
- Total execution time.
- Number of parallel processes.
- Execution time variability.

## How to Contribute

1. Download or clone this repository.
2. Install the required Python dependencies.
3. Run the simulation using the provided configuration.
4. Record and share your results.

## Submitting Results

Participants are encouraged to send their results to:

**Email:** aisrael.ramirez.mejia@gmail.com

**Suggested subject:** ABM CPU Performance Evaluation – Experimental Results

Please include your github profile name.

Participation is voluntary. Submitted results will be used for academic research purposes.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Citation

If you use this software in academic research, please cite the associated publication when its bibliographic information becomes available.

## Research Collaboration

Contributions from different processor architectures and computing environments are welcome. The collected execution data will support a comparative study of multiprocessing performance in agent-based simulations of complex systems.academic publications, please cite the associated research work once its bibliographic information becomes available.

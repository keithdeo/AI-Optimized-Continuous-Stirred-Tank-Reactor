# AI-Optimized Continuous Stirred Tank Reactor (CSTR) Simulation

## Overview

This project develops a Python-based simulation of a **Continuous Stirred Tank Reactor** that models the conversion of reactant **A into product B**.

The purpose of this project is to combine **chemical engineering principles, reaction kinetics, and computational programming** to simulate reactor behavior and create a foundation for future AI-driven optimization. The model analyzes how changes in operating conditions influence reaction rate, conversion efficiency, and product formation.

Future versions of this project will implement machine learning and optimization algorithms to automatically determine the ideal reactor operating conditions for maximum efficiency. Future versions will also include drastic changes to accommodate multiple reactant-product reactions.

---

# Chemical Reaction Model

The reactor simulates a first-order irreversible reaction:

A ➡ B

where:

- **A** = reactant compound
- **B** = desired product

The reaction rate is determined using chemical kinetics:

r = k*C_a

where:

- r = reaction rate
- k = reaction rate constant
- C_a = concentration of reactant A

The temperature dependence of the reaction rate is calculated using the Arrhenius equation:

k = A*e^{-E_a/(R*T)}


where:

- A = pre-exponential factor
- E_ = activation energy
- R = universal gas constant
- T = reactor temperature

This allows the program to predict how increasing temperature affects reaction kinetics and overall reactor performance.

---

# Project Objectives

The main goals of this project are:

- Develop a computational model of a continuous stirred tank reactor
- Simulate the conversion of compound A into compound B
- Analyze the effect of temperature on reaction performance
- Calculate reaction rate and product formation
- Create a foundation for AI-based reactor optimization

# Current Features

The current Python model is capable of:

### Reaction Rate Calculation

The program calculates the reaction rate based on:

- Temperature
- Activation energy
- Reactant concentration

### Conversion Prediction

The model predicts the fraction of reactant A converted into product B over a specified reaction time.

### Material Balance Analysis

The simulation calculates:

- Remaining concentration of reactant A
- Amount of product B generated
- Overall conversion efficiency


# Python Implementation

The project currently contains the following files:

## reactor_model.py

This file contains the core reactor calculations.

The model:

1. Accepts reactor operating conditions as inputs
2. Calculates the reaction rate constant using the Arrhenius equation
3. Determines reaction rate
4. Calculates conversion from A to B
5. Returns reactor performance data

Example:

```python
temperature = 500
concentration = 2
time = 10

results = calculations(
    temperature,
    concentration,
    time
)

print(results)

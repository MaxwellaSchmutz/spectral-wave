# Spectral Wave Lab

An interactive numerical sandbox for exploring spectral representations of wave propagation and frequency-dependent scattering.

This application allows users to define arbitrary spectral integrands, numerically compute the resulting wave evolution, and experiment with custom scattering operators in a fully interactive GUI.

---

## Overview

The system computes wave evolution using a spectral integral representation:

ψ(t, x) = ∫ F(t, x, y) dy

Users define the integrand F(t, x, y) directly.  
The integral is evaluated numerically over a configurable frequency interval.

When scattering is enabled, the system computes:

ψ(t, x) =
- ∫ (F + R(y)F) dy   if x < x₀  
- ∫ (T(y)F) dy       if x ≥ x₀  

where:

- R(y) is a user-defined reflection coefficient
- T(y) is a user-defined transmission coefficient
- x₀ is the obstacle position

All integrations are performed numerically using the trapezoidal rule.

---

## Features

- Multi-integrand stacking
- Complex-valued wave support
- Frequency-dependent scattering
- Piecewise wave computation
- Numerical precomputation with progress tracking
- Replayable animation
- Resizable UI layout
- Symbolic expression parsing via SymPy

This project is designed as a flexible spectral experimentation tool rather than a fixed physical model.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/spectral-wave.git
cd spectral-wave
2. Create and Activate a Virtual Environment

macOS / Linux:

python -m venv .venv
source .venv/bin/activate

Windows:

python -m venv .venv
.venv\Scripts\activate
3. Install Dependencies
pip install numpy sympy matplotlib pyqt6

Optional:

pip install scipy
4. Run the Application
python main.py
Example Usage
Basic Wave Packet

F(t, x, y):

exp(1j*(t*cos(y) + x*y))
Resonant Scattering

R(y):

0.5/(0.5 + 1j*(y-0.8))

T(y):

1 - R(y)

Obstacle position:

0
Perfect Reflection

R(y):

-1

T(y):

0
Mathematical Intent

This tool is useful for exploring:

Spectral decomposition of wave packets

Frequency-selective scattering behavior

Phase distortion under reflection

Interference between multiple spectral components

Piecewise-defined wave evolution

It is intentionally built to allow experimentation with arbitrary integrands rather than restricting the user to a predefined PDE model.

Tech Stack

Python

NumPy

SymPy

Matplotlib

PyQt6

Project Status

Active development.
Planned expansions include:

Matrix-valued scattering operators

Energy-conserving enforcement modes

Multi-channel wave systems

Exportable simulation output

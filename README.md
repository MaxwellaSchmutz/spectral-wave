# Spectral Wave Lab

An interactive spectral wave simulation tool for experimenting with custom integrands and frequency-dependent scattering operators.

---

## What It Does

The application numerically computes wave evolution using a spectral integral:

ψ(t, x) = ∫ F(t, x, y) dy

Users define the integrand F(t, x, y) directly.

When scattering is enabled:

ψ(t, x) =
    ∫ (F + R(y)F) dy   if x < x₀
    ∫ (T(y)F) dy       if x ≥ x₀

All integrals are evaluated numerically using the trapezoidal rule.

---

## Setup

Clone the repository:

    git clone https://github.com/YOUR_USERNAME/spectral-wave.git
    cd spectral-wave

Create and activate a virtual environment:

macOS / Linux:

    python -m venv .venv
    source .venv/bin/activate

Windows:

    python -m venv .venv
    .venv\Scripts\activate

Install dependencies:

    pip install numpy sympy matplotlib pyqt6

(Optional)

    pip install scipy

Run the application:

    python main.py

---

## Example Integrand

    exp(1j*(t*cos(y) + x*y))

---

## Example Scattering

    R(y) = 0.5/(0.5 + 1j*(y-0.8))
    T(y) = 1 - R(y)
    x₀ = 0

---

## Tech Stack

Python  
NumPy  
SymPy  
Matplotlib  
PyQt6  

---

Built as a numerical sandbox for exploring spectral wave representations and scattering dynamics.

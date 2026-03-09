# Spectral Wave Lab

Interactive spectral wave simulation engine with customizable integrands and frequency-dependent scattering operators.

---

## Requirements

- Python 3.10+
- Git

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/spectral-wave.git
cd spectral-wave
### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux

# or

```bash
.venv\Scripts\activate         # Windows

### 3. Install Dependencies
```bash
pip install numpy sympy matplotlib pyqt6

If scattering features are used heavily, also install:

```bash
pip install scipy

### 4. Run the Application
```bash
python main.py

Usage
Define an Integrand

Enter a spectral integrand of the form:

F(t,x,y)

Example:

exp(1j*(t*cos(y) + x*y))

Click Add Integrand, then Precompute & Animate.

Enable Scattering (Optional)

Check Enable Scattering and define:

R(y)
T(y)
Obstacle position x₀

Example:

R(y) = 0.5/(0.5 + 1j*(y-0.8))
T(y) = 1 - R(y)
x₀ = 0
Notes

The system computes:

ψ(t,x) = ∫ F(t,x,y) dy

With scattering enabled:

ψ(t,x) =
    ∫ (F + R(y)F) dy   if x < x₀
    ∫ (T(y)F) dy       if x ≥ x₀

All integrals are evaluated numerically using the trapezoidal rule.

Tech Stack

PyQt6

NumPy

SymPy

Matplotlib
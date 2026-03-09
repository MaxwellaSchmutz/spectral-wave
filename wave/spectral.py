import numpy as np
import sympy as sp


class SpectralSystem:

    def __init__(self, t_values, x_values, y_low, y_high, Ny):

        self.t_values = t_values
        self.x_values = x_values

        self.y_low = y_low
        self.y_high = y_high
        self.Ny = Ny

        self.y_values = np.linspace(y_low, y_high, Ny)

        self.t_sym, self.x_sym, self.y_sym = sp.symbols("t x y")

        self.integrand_funcs = []

        # Scattering controls
        self.scattering_enabled = False
        self.obstacle_position = 0

        self.R_func = None
        self.T_func = None

    # ==========================================
    # ADD INTEGRAND
    # ==========================================

    def add_integrand(self, expr_string):

        expr = sp.sympify(expr_string.replace("^", "**"))

        func = sp.lambdify(
            (self.t_sym, self.x_sym, self.y_sym),
            expr,
            "numpy"
        )

        self.integrand_funcs.append(func)

    def clear_integrands(self):
        self.integrand_funcs = []

    # ==========================================
    # SET SCATTERING
    # ==========================================

    def set_scattering(self, enabled, R_expr=None, T_expr=None, obstacle_position=0):

        self.scattering_enabled = enabled
        self.obstacle_position = obstacle_position

        if enabled:

            R_sym = sp.sympify(R_expr.replace("^", "**"))
            T_sym = sp.sympify(T_expr.replace("^", "**"))

            self.R_func = sp.lambdify(self.y_sym, R_sym, "numpy")
            self.T_func = sp.lambdify(self.y_sym, T_sym, "numpy")

        else:
            self.R_func = None
            self.T_func = None

    # ==========================================
    # COMPUTE
    # ==========================================

    def compute_frames(self, progress_callback=None):

        if not self.integrand_funcs:
            return None, None

        frames = []
        global_max = 0

        X = self.x_values[:, None]
        Y = self.y_values[None, :]

        total_steps = len(self.t_values)

        for i, t_val in enumerate(self.t_values):

            curves = []

            for func in self.integrand_funcs:

                values = func(t_val, X, Y)

                if self.scattering_enabled:

                    # -------------------------------
                    # Evaluate scattering coefficients
                    # -------------------------------

                    R_vals = self.R_func(self.y_values)
                    T_vals = self.T_func(self.y_values)

                    # Force to complex numpy arrays
                    R_vals = np.asarray(R_vals, dtype=complex)
                    T_vals = np.asarray(T_vals, dtype=complex)

                    # If scalar (e.g. R(y)=0 or R(y)=-1), expand properly
                    if R_vals.ndim == 0:
                        R_vals = np.full(self.y_values.shape, R_vals, dtype=complex)

                    if T_vals.ndim == 0:
                        T_vals = np.full(self.y_values.shape, T_vals, dtype=complex)

                    R_vals = R_vals[None, :]
                    T_vals = T_vals[None, :]

                    psi = np.zeros(len(self.x_values), dtype=complex)

                    for idx, x in enumerate(self.x_values):

                        row = values[idx]

                        if x < self.obstacle_position:
                            integrand = row + R_vals[0] * row
                        else:
                            integrand = T_vals[0] * row

                        psi[idx] = np.trapezoid(
                            integrand,
                            self.y_values
                        )

                else:

                    psi = np.trapezoid(
                        values,
                        self.y_values,
                        axis=1
                    )

                amplitude = np.abs(psi)

                curves.append(amplitude)

                local_max = np.max(amplitude)
                if local_max > global_max:
                    global_max = local_max

            frames.append(curves)

            if progress_callback is not None:
                percent = int((i + 1) / total_steps * 100)
                progress_callback(percent)

        return frames, global_max
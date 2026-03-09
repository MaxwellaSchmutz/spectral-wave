import numpy as np

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidget,
    QProgressBar,
    QSplitter,
    QCheckBox
)
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from wave.spectral import SpectralSystem


# ==========================================================
# WORKER THREAD
# ==========================================================

class ComputeWorker(QThread):

    progress = pyqtSignal(int)
    finished = pyqtSignal(object, float)

    def __init__(self, system):
        super().__init__()
        self.system = system

    def run(self):

        frames, global_max = self.system.compute_frames(
            progress_callback=self.progress.emit
        )

        if frames is None:
            self.finished.emit([], 0.0)
        else:
            self.finished.emit(frames, float(global_max))


# ==========================================================
# MAIN WINDOW
# ==========================================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spectral Multi-ψ Lab")

        # ==================================================
        # BENCHMARK GRIDS
        # ==================================================

        self.t_values = np.arange(-300, 301)
        self.x_values = np.arange(-300, 301)

        self.system = SpectralSystem(
            t_values=self.t_values,
            x_values=self.x_values,
            y_low=0.4,
            y_high=0.6,
            Ny=2000
        )

        # ==================================================
        # CENTRAL WIDGET + SPLITTER
        # ==================================================

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # ==================================================
        # LEFT PANEL
        # ==================================================

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        # Formula Display
        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-weight: bold;")
        left_layout.addWidget(self.title_label)

        # Integrand input
        row = QHBoxLayout()
        row.addWidget(QLabel("F(t,x,y) ="))

        self.input_field = QLineEdit(
            "exp(1j*(t*cos(y) + x*y))"
        )
        row.addWidget(self.input_field)
        left_layout.addLayout(row)

        self.add_button = QPushButton("Add Integrand")
        self.add_button.clicked.connect(self.add_integrand)
        left_layout.addWidget(self.add_button)

        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_integrands)
        left_layout.addWidget(self.clear_button)

        self.list_widget = QListWidget()
        left_layout.addWidget(self.list_widget)

        # =========================
        # SCATTERING CONTROLS
        # =========================

        self.scatter_checkbox = QCheckBox("Enable Scattering")
        self.scatter_checkbox.stateChanged.connect(self.update_formula_display)
        left_layout.addWidget(self.scatter_checkbox)

        left_layout.addWidget(QLabel("R(y) ="))
        self.R_input = QLineEdit("5/(5 + 1j*y)")
        left_layout.addWidget(self.R_input)

        left_layout.addWidget(QLabel("T(y) ="))
        self.T_input = QLineEdit("(1j*y)/(5 + 1j*y)")
        left_layout.addWidget(self.T_input)

        left_layout.addWidget(QLabel("Obstacle position x₀ ="))
        self.obstacle_input = QLineEdit("0")
        left_layout.addWidget(self.obstacle_input)

        # =========================
        # PROGRESS + RUN
        # =========================

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        left_layout.addWidget(self.progress_bar)

        self.run_button = QPushButton("Precompute & Animate")
        self.run_button.clicked.connect(self.precompute)
        left_layout.addWidget(self.run_button)

        self.replay_button = QPushButton("Play Again")
        self.replay_button.clicked.connect(self.play_again)
        self.replay_button.setEnabled(False)
        left_layout.addWidget(self.replay_button)

        left_layout.addStretch()

        splitter.addWidget(left_widget)

        # ==================================================
        # RIGHT PANEL (GRAPH)
        # ==================================================

        self.figure = Figure(figsize=(7, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        splitter.addWidget(self.canvas)
        splitter.setSizes([400, 900])

        # ==================================================
        # ANIMATION
        # ==================================================

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)

        self.frames = None
        self.current_index = 0
        self.ylim = 1
        self.lines = []

        self.update_formula_display()

    # ==================================================
    # FORMULA DISPLAY
    # ==================================================

    def update_formula_display(self):

        if self.scatter_checkbox.isChecked():

            text = (
                "ψ(t,x) = ⎧\n"
                "              ⎪  ∫ (F(t,x,y) + R(y)F(t,x,y)) dy      ,  x < x₀\n"
                "              ⎨\n"
                "              ⎪  ∫ (T(y)F(t,x,y)) dy                  ,  x ≥ x₀\n"
                "              ⎩\n"
                f"           y ∈ [{self.system.y_low}, {self.system.y_high}]"
            )

        else:

            text = (
                "ψ(t,x) = ∫ F(t,x,y) dy\n"
                f"y ∈ [{self.system.y_low}, {self.system.y_high}]"
            )

        self.title_label.setText(text)

    # ==================================================
    # ADD INTEGRAND
    # ==================================================

    def add_integrand(self):
        expr_string = self.input_field.text()
        try:
            self.system.add_integrand(expr_string)
            self.list_widget.addItem(expr_string)
        except Exception as e:
            print("Parse error:", e)

    # ==================================================
    # CLEAR
    # ==================================================

    def clear_integrands(self):
        self.system.clear_integrands()
        self.list_widget.clear()

    # ==================================================
    # PRECOMPUTE
    # ==================================================

    def precompute(self):

        self.progress_bar.setValue(0)
        self.replay_button.setEnabled(False)

        if self.scatter_checkbox.isChecked():
            try:
                self.system.set_scattering(
                    True,
                    self.R_input.text(),
                    self.T_input.text(),
                    float(self.obstacle_input.text())
                )
            except Exception as e:
                print("Scattering parse error:", e)
                return
        else:
            self.system.set_scattering(False)

        self.ax.clear()
        self.ax.set_title("Computing...")
        self.canvas.draw()

        self.worker = ComputeWorker(self.system)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_compute_finished)
        self.worker.start()

    # ==================================================
    # FINISHED
    # ==================================================

    def on_compute_finished(self, frames, global_max):

        self.frames = frames

        if not self.frames:
            return

        self.ylim = global_max * 1.1
        self.current_index = 0
        self.lines = []

        self.progress_bar.setValue(100)
        self.replay_button.setEnabled(True)

        self.timer.start(1)

    # ==================================================
    # REPLAY
    # ==================================================

    def play_again(self):
        if self.frames is None:
            return
        self.current_index = 0
        self.timer.start(1)

    # ==================================================
    # UPDATE PLOT
    # ==================================================

    def update_plot(self):

        if self.current_index >= len(self.frames):
            self.timer.stop()
            return

        curves = self.frames[self.current_index]

        if self.current_index == 0:
            self.ax.clear()
            self.lines = []

            for curve in curves:
                line, = self.ax.plot(
                    self.x_values,
                    curve,
                    marker="o",
                    linestyle="None",
                    markersize=2
                )
                self.lines.append(line)

            self.ax.set_ylim(0, self.ylim)
            self.ax.set_xlim(min(self.x_values), max(self.x_values))
            self.ax.grid(True)

        else:
            for line, curve in zip(self.lines, curves):
                line.set_ydata(curve)

        self.ax.set_title(f"t = {self.t_values[self.current_index]}")
        self.canvas.draw_idle()

        self.current_index += 1
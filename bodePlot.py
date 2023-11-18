from GUI.main_window import MainWindow
from GUI.main_window import BodePlotterApp

# Instantiate a main window
window_app = MainWindow()

# Instantiate the app (with required frames)
app = BodePlotterApp(window_app)

# Run the GUI
app.main_window.mainloop()
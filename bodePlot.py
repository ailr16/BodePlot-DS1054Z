from GUI.main_window import MainWindow
from GUI.main_window import BodePlotterApp


window_app = MainWindow()

app = BodePlotterApp(window_app)
app.main_window.mainloop()
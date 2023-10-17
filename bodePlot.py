from GUI.main_window import MainWindow
from GUI.main_window import InstrumentFrame


app = MainWindow()
frame = InstrumentFrame(app)
app.mainloop()
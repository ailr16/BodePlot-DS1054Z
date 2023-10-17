from GUI.main_window import BodePlotterApp
from GUI.main_window import InstrumentFrame
from GUI.main_window import TestFrame


app = BodePlotterApp()
inst = InstrumentFrame(app)
test = TestFrame(app)
app.mainloop()
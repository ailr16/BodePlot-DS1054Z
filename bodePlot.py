from GUI.main_window import BodePlotterApp
from GUI.main_window import InstrumentFrame
from GUI.main_window import TestFrame
from GUI.main_window import ActionsFrame


app = BodePlotterApp()
inst = InstrumentFrame(app)
test = TestFrame(app)
actions = ActionsFrame(app)
app.mainloop()
import sys
import streamlit as st

sys.path.append("./")
from ocik.demo import mutliapp, demo__intro, demo__parameter, demo__home

app = mutliapp.MultiApp()
app.add_app("Home", demo__home.app)
app.add_app("Introduction", demo__intro.app)
app.add_app("Parameter Learning", demo__parameter.app)
app.run()
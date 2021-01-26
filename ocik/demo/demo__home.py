import streamlit as st
import sys
from PIL import Image

sys.path.append("./")


def app():
    st.write(r'''
    ## Home Page
    ''')

    image = Image.open('ocik/demo/media/home.png')
    st.image(image, use_column_width=True)


if __name__ == '__main__':
    app()

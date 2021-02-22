import streamlit as st
from graphviz import Digraph
import sys

sys.path.append("./")

from ocik.example import Asia


def app():
    st.write(r'''
    ## Apprentissage des paramètres

    Imaginons qu'on ait construit un réseau Bayésien représentant notre modèle causale, la prochaine étape consiste à
    remplir les tables de probabilité conditionnelle. Une façon de faire cela est de rechercher le meilleur jeu de
    paramètres pour rendre compte des données observées.

    Il existe deux approches pour calculer les paramètres :

    - **Le Maximum de vraisemblence**: qui cosidère les paramètres comme des constantes et cherches à les determiner en
    maximixant la vraisemblance

    - **Le Maximum à Priori**: Utilise les résultats du maximum de vraisemblance pour construire une distribution à
    posteriori.

    Nous allons tester les méthodes d'apprentissages sur un reseau baysien à partir des données. 
    ''')

    # Load th data
    asia = Asia()

    # bn = asia.get_network()
    # f = Digraph()
    # f.edges(bn.G.edges())
    # st.graphviz_chart(f.source)
    #
    # # Generate data
    # st.write(r"""
    # D'abord nous allons générer des données à partir du reseau bayesien.
    # """)
    # df = asia.load_data(nrows=1000)
    # st.write(df.head())


if __name__ == '__main__':
    app()

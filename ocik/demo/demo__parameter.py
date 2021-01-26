import streamlit as st


def app():

    st.write(r'''
    ## 3. Apprentissage des paramètres

    Imaginons qu'on ait construit un réseau Bayésien représentant notre modèle causale, la prochaine étape consiste à
    remplir les tables de probabilité conditionnelle. Une façon de faire cela est de rechercher le meilleur jeu de
    paramètres pour rendre compte des données observées.

    Il existe deux approches pour calculer les paramètres :

    - **Le Maximum de vraisemblence**: qui cosidère les paramètres comme des constantes et cherches à les determiner en
    maximixant la vraisemblance

    - **Le Maximum à Priori**: Utilise les résultats du maximum de vraisemblance pour construire une distribution à
    posteriori.

    Nous allons tester les méthodes d'apprentissages sur un reseau baysien dont les noeuds correspondes aux résulats de
    porte logique.
    ''')


if __name__ == '__main__':
    app()

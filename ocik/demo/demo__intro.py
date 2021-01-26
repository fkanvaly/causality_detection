import sys

sys.path.append("../../demo/")

import streamlit as st
from ocik.network import BayesianNetwork


def app():
    st.write(r'''
    # Causality Detection in Smart Home
    Auteur : Kanvaly FADIGA
    
    ## Abstract
    Anomaly detection is a topic that generates a lot of interest in the ML community.  
    Rather than focusing on anomaly detection, this study aims to determine the cause 
    of anomalies in a smart home scenario. We approached this problem by first building 
    the smart home causal models using an innovative approach that combines interaction 
    with the environment and observation of the house functioning through its sensors data. 
    Then we embed the resulting causal model into a Bayesian network which is used to do 
    inverse inference to find the most probable cause for an abnormal event. 
    
    
    Sommaire : 
    
    1. Introduction
    
    2. Causalité
    
    2. Inférence
    ''')

    st.write(r'''
    ## 1. Introduction 
    
    L’enjeu de ce projet est de prédire la cause des anomalies qui pourraient avoir lieu dans une maison intelligente. 
    Plaçons-nous dans une maison avec des objets connectés, des caméras et des senseurs qui collectent des données en 
    temps réel.  Dans cette maison nous imaginons avoir un système de monitoring qui est capable de détecter des 
    anomalies. Disons que le système trouve que la température est beaucoup plus élevée, qu'elle ne l’est habituellement. 
    Afin de fixer cette anomalie, il serait intéressant de connaître sa cause. Ici, le dysfonctionnement du capteur de 
    température ou une valeur élevée du thermostat pourrait en être la cause.  Une fois la cause connue, nous pouvons 
    réfléchir à un moyen de résoudre le problème. 
    
    L’objectif du projet est de construire un tel système, qui partant des anomalies, trouve les causes qui les auraient 
    engendrées. Une manière d’approcher ce problème, est de consulter un expert afin de pouvoir coder en dur les 
    relations de cause à effet entre les objets de notre maison intelligente. Cependant, cette approche manque de 
    flexibilité comme nous pouvons le voir. En effet, à chaque fois qu'un nouvel objet est intégré à notre environnement 
    il faudrait pouvoir déterminer à l’avance l’impact qu'il pourrait avoir avec les autres éléments de notre 
    environnement. Pour certains objets cela peut être simple à prédire, mais pour d'autres, les relations causales ne 
    sont pas évidentes car elles sont spécifiques à notre environnement. Prenons pour exemple, une ampoule et un 
    détecteur de température. Dans la construction d’un modèle causal de notre maison on dirait à priori que ces deux 
    éléments n’ont pas vraiment une relation. Maintenant, imaginez que ce détecteur soit placé à côté de l'ampoule, 
    cela aurait pour conséquence créé une interaction entre les deux et ainsi fait augmenter la mesure du capteur. Notre 
    système codé en dur serait incapable de voir une telle relation dans son diagnostic. Ainsi, il nous faut donc 
    développer un système intelligent qui serait capable de découvrir de nouvelles relations causales, de répondre à nos 
    questions sur les causes des anomalies tout en étant flexible aux variations de l’environnement. Pour ce projet nous 
    avons imaginé un système qui construit le modèle de fonctionnement causal de la maison en l’observant et en 
    interagissant avec elle. Ensuite, nous utiliserons ce modèle pour faire des requêtes pour expliquer les anomalies que 
    nous allons détecter. 
    
    Pour résoudre ce problème il nous faut quatre éléments. Le premier est le modèle de représentation du fonctionnement 
    causal de la maison. Ensuite, nous allons chercher à construire un modèle pour notre environnement de façon 
    automatique. Puis, nous allons essayer de voir comment poser des questions à notre modèle. Enfin, vu que notre 
    système sera en fonctionnement de façon continue, il nous faudra développer un algorithme qui va contrôler la 
    construction et la mise à jour de notre modèle en continu. 
    
    ## 2. Causalité et Diagramme causal
    
    on ne découvre pas les relations de causalités juste en observant le monde, mais, elles peuvent s’obtenir en menant 
    des expérimentations pour valider nos hypothèses de potentiels relations causales. Ensuite, une fois qu'on les a 
    découvertes, on peut les représenter grâce à un digramme causal. Un diagramme causal est un graphe orienté qui 
    présente les relations causales entre les variables. Le diagramme comprend un ensemble de variables (ou nœuds) et 
    chaque nœud est relié par une flèche à un ou plusieurs autres nœuds sur lesquels il exerce une influence causale. Une 
    pointe de flèche délimite la direction de la causalité, par exemple, une flèche reliant les variables A et B avec la 
    pointe de flèche à B indique qu'un changement dans A entraîne un changement dans B. 
    
    Les diagrammes de cause sont indépendants des probabilités quantitatives qui les informent. Cela veut dire que le 
    diagramme causal ne dépend pas des données. Les modifications de ces probabilités (par exemple, en raison 
    d'améliorations technologiques) n'exigent pas de changements au modèle (c’est-à-dire la relation causale). 
    
    ## 3. Réseau Bayésien
    
    Pour transformer le diagramme de causalité en un réseau bayésien, nous devons spécifier les tableaux de probabilité 
    conditionnelle inhérents aux réseaux bayésiens. Cependant l’interprétation qu’on se fait d’un arc dans un diagramme 
    causal n’est pas la même que celle qu’un réseau bayésien donne à ses arcs. Un réseau bayésien peut être utilisé pour 
    représenter un diagramme causal cependant il peut être utilisé pour fournir la probabilité inverse d'un événement (
    étant donné un résultat, quelles sont les probabilités d'une cause spécifique).
     
    Un réseau bayésien n'est littéralement rien d'autre qu'une représentation compacte d'un immense tableau de 
    probabilité. Les flèches signifient seulement que les probabilités des nœuds enfants sont liées aux valeurs des nœuds 
    parents par une certaine formule ( les tableaux de probabilité conditionnelle) et que cette relation est suffisante. 
    C'est-à-dire que le fait de connaître d'autres ancêtres de l'enfant ne changera pas la formule. De même, une flèche 
    manquante entre deux nœuds quelconques signifie qu'ils sont indépendants, une fois nous connaissons les valeurs de 
    leurs parents.
    
    L’utilisation essentielle des réseaux bayésiens est donc de calculer des Probabilités conditionnelles d’événements 
    reliés les uns aux autres par des Relations de cause à effet. Cette utilisation s’appelle inférence. 
     
    En fonction des informations observées, on calcule la probabilité des données non 
    observées. Par exemple, en fonction des symptômes d’un Malade, on calcule les probabilités des différentes 
    pathologies compatibles avec ces symptômes. On peut aussi calculer la probabilité de symptômes non observés, 
    et en déduire les examens complémentaires les plus intéressants.
    
    ''')

if __name__ == '__main__':
    app()
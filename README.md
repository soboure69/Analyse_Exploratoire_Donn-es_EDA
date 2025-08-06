# Analyse_Exploratoire_Donnees_EDA
Il est question de faire une analyse exploratoire des données en Banque et en Marketing

Ce projet est réalisé tout entier en Python de manière interactive sur un seul fichier .ipynb (notebook) et comporte deux parties :

- En Banque : Faire l'EDA pour analyser les transactions bancaires pour identifier des schémas de fraude 

- En Marketing : Faire l'EDA pour identifier les segments de clients les plus rentables en fonction de leurs interactions avec des campagnes 

## Contexte
L'analyse exploratoire des données (EDA) est une étape clé dans tout projet de data science. Ce projet permet de montrer votre capacité à comprendre des données brutes, à les nettoyer, et à formuler des hypothèses avant d'appliquer des modèles plus complexes.


## Objectifs
Comprendre la structure des données et leur distribution.
Identifier les variables importantes et les relations entre elles.
Produire des visualisations claires pour présenter les résultats.

## Problématiques

- En Banque : Comment analyser les transactions bancaires pour identifier des schémas de fraude ?

Dataset : [https://www.kaggle.com/datasets/mlgulb/creditcardfraud](https://www.kaggle.com/datasets/mlgulb/creditcardfraud)

```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")

print("Path to dataset files:", path)

```

- En Marketing : Quels sont les segments de clients les plus rentables en fonction de leurs interactions avec des campagnes ?

Dataset : [https://www.kaggle.com/datasets/rodsaldanha/arketingcampaign/data
](https://www.kaggle.com/datasets/rodsaldanha/arketingcampaign/data)

```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("rodsaldanha/arketingcampaign/data")

print("Path to dataset files:", path)

```

## Technologies Utilisées
- Python
- Pandas : Pour la manipulation et la transformation des données.
- Matplotlib/Seaborn : Pour visualiser les tendances à travers des graphiques comme les histogrammes, scatter plots, et heatmaps.
- NumPy : Pour les calculs mathématiques et statistiques.
- Shiny/Streamlit/Dash : Pour déployer un tableau de bord interactif afin de présenter les résultats de l'EDA aux parties prenantes.
- Statistique Univariée : Analyse d'une seule variable pour en comprendre la distribution et les caractéristiques.
- Statistique Multivariée : Analyse des relations entre plusieurs variables afin d'explorer des corrélations ou des interactions.

## Compétences Acquises
- Manipulation des données : Capacité à manipuler de larges volumes de données avec Pandas et NumPy.
- Nettoyage des données : Utilisation de méthodes d’identification des valeurs manquantes, gestion des doublons et transformation des variables catégorielles.
- Visualisation des données : Création de visualisations perspicaces avec Matplotlib et Seaborn pour communiquer efficacement les résultats.
- Statistique Univariée : Capacité à analyser les caractéristiques d'une variable individuelle.
- Statistique Multivariée : Capacité à analyser et interpréter les relations entre plusieurs variables.
- Déploiement d’un tableau de bord interactif : Création d'applications de data visualisation avec Streamlit, Dash, ou Shiny pour fournir des insights interactifs et accessibles aux non-techniciens.

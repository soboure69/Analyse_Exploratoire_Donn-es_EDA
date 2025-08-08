# 🔧 Guide de Dépannage - Dashboards EDA Bancaire & Marketing

[![Version](https://img.shields.io/badge/Version-2.1-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io)

## 🎯 Vue d'Ensemble

Ce guide vous aide à résoudre les problèmes courants rencontrés lors de l'utilisation des dashboards interactifs pour l'analyse exploratoire des données bancaires et marketing.

## 😨 Problèmes Critiques et Solutions

### 📄 1. Erreurs de Parsing CSV

#### **Problème :** "Cannot convert to numeric" ou colonnes mal séparées

**🔍 Cause :** Délimiteur CSV incorrect (`;` vs `,`)

**⚙️ Solution Automatique :**

```python
# Détection automatique implémentée dans les dashboards
def detect_delimiter(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline()
        if ';' in first_line and first_line.count(';') > first_line.count(','):
            return ';'
        return ','
```

**🛠️ Solution Manuelle :**

```python
# Test des délimiteurs
df_comma = pd.read_csv("fichier.csv", sep=',')
df_semicolon = pd.read_csv("fichier.csv", sep=';')

# Choisir celui avec le plus de colonnes
if len(df_semicolon.columns) > len(df_comma.columns):
    df = df_semicolon
else:
    df = df_comma
```

### 2. Erreur "'list' object has no attribute 'sum'"

**Problème :** Tentative d'appeler `.sum()` sur une liste au lieu d'un DataFrame.

**Solution :** ✅ **CORRIGÉ** - Le code utilise maintenant `df[purchase_vars].sum(axis=1)`

### 3. Données Marketing Non Trouvées

**Solutions possibles :**

1. **Placez le fichier CSV dans le répertoire du projet**
   ```
   Analyse_Exploratoire_Donnees_EDA/
   ├── marketing_campaign.csv  ✅
   ├── dashboard_marketing.py
   └── ...
   ```

2. **Noms de fichiers acceptés :**
   - `marketing*.csv`
   - `*campaign*.csv`
   - `marketing_campaign.csv`

3. **Format de données attendu :**
   ```csv
   ID;Year_Birth;Education;Income;Recency;MntWines;NumWebPurchases;...
   5524;1957;Graduation;58138;58;635;8;...
   ```

### 4. Variables RFM Manquantes

**Variables recherchées automatiquement :**
- **Recency** : Nombre de jours depuis le dernier achat
- **Frequency** : Variables commençant par `Num` et contenant `Purchases`
- **Monetary** : Variables commençant par `Mnt` (montants)

**Si aucune variable RFM trouvée :**
- Le dashboard utilisera les 3 premières variables numériques disponibles
- Message d'avertissement affiché

### 5. Erreurs de Clustering

**Causes possibles :**
- Données non numériques
- Toutes les valeurs sont NaN
- Pas assez de données

**Solutions automatiques implémentées :**
- Conversion automatique en numérique
- Remplacement des NaN par la médiane
- Fallback vers d'autres variables si RFM indisponible

## 🔍 Diagnostic Rapide

### Vérifier le Format des Données

```python
import pandas as pd

# Test du délimiteur
df_comma = pd.read_csv("votre_fichier.csv", sep=',')
print(f"Avec virgule: {df_comma.shape}")

df_semicolon = pd.read_csv("votre_fichier.csv", sep=';')
print(f"Avec point-virgule: {df_semicolon.shape}")

# Le bon format aura plus de colonnes
```

### Vérifier les Variables RFM

```python
# Vérifier les colonnes disponibles
print("Colonnes disponibles:")
print(df.columns.tolist())

# Chercher les variables RFM
spending_vars = [col for col in df.columns if 'Mnt' in col]
purchase_vars = [col for col in df.columns if 'Num' in col and 'Purchases' in col]

print(f"Variables de dépenses: {spending_vars}")
print(f"Variables d'achats: {purchase_vars}")
print(f"Recency disponible: {'Recency' in df.columns}")
```

## 📊 Données d'Exemple

Si vous n'avez pas de données, voici comment créer un dataset de test :

```python
import pandas as pd
import numpy as np

# Créer des données de test
np.random.seed(42)
n_samples = 1000

test_data = pd.DataFrame({
    'ID': range(1, n_samples + 1),
    'Year_Birth': np.random.randint(1940, 2000, n_samples),
    'Income': np.random.randint(20000, 100000, n_samples),
    'Recency': np.random.randint(1, 100, n_samples),
    'MntWines': np.random.randint(0, 1000, n_samples),
    'MntFruits': np.random.randint(0, 200, n_samples),
    'MntMeatProducts': np.random.randint(0, 500, n_samples),
    'NumWebPurchases': np.random.randint(0, 20, n_samples),
    'NumStorePurchases': np.random.randint(0, 15, n_samples),
})

# Sauvegarder
test_data.to_csv('marketing_test.csv', sep=';', index=False)
print("✅ Fichier de test créé: marketing_test.csv")
```

## 🚀 Lancement des Dashboards

### Dashboard Fraude Bancaire
```bash
# Méthode 1 - Script Windows
launch_dashboard.bat

# Méthode 2 - Python
python launch_dashboard.py

# Méthode 3 - Streamlit direct
streamlit run dashboard_fraud.py --server.port=8501
```

### Dashboard Marketing
```bash
# Méthode 1 - Script Windows  
launch_marketing.bat

# Méthode 2 - Streamlit direct
streamlit run dashboard_marketing.py --server.port=8502
```

## ⚡ Optimisation des Performances

### Pour les Gros Datasets

1. **Échantillonnage automatique** : Le dashboard limite automatiquement à 10,000 lignes par défaut

2. **Filtrage des données** : Utilisez les filtres de la sidebar pour réduire le volume

3. **Variables limitées** : Seules les variables RFM principales sont utilisées pour le clustering

### Paramètres Recommandés

- **Nombre de clusters** : 3-5 pour la plupart des cas
- **Taille d'échantillon** : 5,000-10,000 pour une bonne performance
- **Variables RFM** : Maximum 3-4 variables pour éviter la malédiction de la dimensionnalité

## 📞 Support Technique

### Messages d'Erreur Courants

| Erreur | Cause | Solution |
|--------|--------|----------|
| `FileNotFoundError` | Fichier CSV manquant | Placer le fichier dans le répertoire |
| `Cannot convert to numeric` | Mauvais délimiteur | Utiliser `sep=';'` |
| `'list' object has no attribute 'sum'` | Erreur de code | ✅ Corrigé dans la v2 |
| `Aucune variable RFM trouvée` | Colonnes manquantes | Vérifier les noms de colonnes |

### Logs de Debug

Pour activer les logs détaillés :

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Contact

Pour des problèmes non résolus :
1. Vérifiez ce guide de dépannage
2. Consultez les logs d'erreur
3. Vérifiez le format des données
4. Testez avec les données d'exemple

---

**Version :** 2.0  
**Dernière mise à jour :** 2025-08-07  
**Compatibilité :** Python 3.8+, Streamlit 1.25+

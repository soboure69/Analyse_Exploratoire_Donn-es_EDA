# 🚀 Dashboard Unifié EDA - Guide Utilisateur

[![Dash](https://img.shields.io/badge/Dash-2.10+-blue.svg)](https://dash.plotly.com)
[![Plotly](https://img.shields.io/badge/Plotly-5.0+-green.svg)](https://plotly.com)
[![Python](https://img.shields.io/badge/Python-3.8+-orange.svg)](https://python.org)

## 🎯 Vue d'Ensemble

Le **Dashboard Unifié EDA** combine l'analyse des secteurs bancaire et marketing dans une seule interface web moderne et interactive, construite avec **Dash** et **Plotly**.

### ✨ Fonctionnalités Principales

- 🏦 **Analyse Bancaire** - Détection de fraude et patterns transactionnels
- 🛍️ **Analyse Marketing** - Segmentation RFM et profiling client
- 📊 **Vue Comparative** - Comparaison des deux datasets
- 🎨 **Interface Moderne** - Design responsive avec Font Awesome
- ⚡ **Performance Optimisée** - Chargement dynamique des données

## 🚀 Démarrage Rapide

### 📋 Prérequis

```bash
# Vérifier Python (3.8+ requis)
python --version

# Installer les dépendances
pip install -r requirements.txt
```

### 🖱️ Lancement Simple (Windows)

**Double-cliquez sur :** `launch_unified_dashboard.bat`

### 💻 Lancement en Ligne de Commande

```bash
# Option 1: Script Python avec vérifications
python launch_unified.py

# Option 2: Lancement direct
python dashboard_unified.py
```

### 🌐 Accès au Dashboard

Une fois lancé, ouvrez votre navigateur sur :
**http://localhost:8050**

## 📊 Guide d'Utilisation

### 1️⃣ Chargement des Données

#### 🏦 **Données Bancaires**
- Cliquez sur **"Charger Données Bancaires"**
- Fichiers acceptés : `*credit*.csv`, `*fraud*.csv`
- Format attendu : colonnes `Amount`, `Time`, `Class`/`is_fraud`

#### 🛍️ **Données Marketing**
- Cliquez sur **"Charger Données Marketing"**
- Fichiers acceptés : `*marketing*.csv`, `*campaign*.csv`, `*customer*.csv`
- Format attendu : colonnes `Recency`, `Mnt*`, `Num*Purchases`

### 2️⃣ Navigation par Onglets

#### 🏦 **Onglet Analyse Bancaire**

**Graphiques disponibles :**
- 📊 **Distribution des Transactions** - Pie chart Normal vs Fraude
- 💰 **Distribution des Montants** - Box plot par type de transaction
- ⏰ **Taux de Fraude par Heure** - Line chart temporel

**Métriques clés :**
- Nombre total de transactions
- Pourcentage de fraudes
- Montants moyens par catégorie
- Heures de pic de fraude

#### 🛍️ **Onglet Analyse Marketing**

**Graphiques disponibles :**
- 🎯 **Distribution des Segments** - Bar chart des segments RFM
- 📈 **Analyse RFM 3D** - Scatter plot 3D interactif
- 💰 **Dépenses par Segment** - Bar chart des moyennes

**Segmentation automatique :**
- 🏆 **Champions** - Clients les plus rentables
- ⭐ **Loyaux** - Achats réguliers
- 🔮 **Potentiels** - Opportunités d'upselling
- 💤 **Endormis** - Clients à réactiver

#### 📊 **Onglet Vue Comparative**

**Comparaisons disponibles :**
- Nombre de lignes et colonnes par dataset
- Statistiques descriptives croisées
- Graphiques de comparaison des volumes

### 3️⃣ Fonctionnalités Interactives

#### 🎨 **Visualisations Plotly**
- **Zoom** - Molette de la souris
- **Pan** - Clic-glisser
- **Sélection** - Rectangle ou lasso
- **Hover** - Détails au survol
- **Légendes** - Clic pour masquer/afficher

#### 📱 **Design Responsive**
- Interface adaptative desktop/mobile
- Graphiques redimensionnables
- Navigation tactile optimisée

## 🔧 Configuration Avancée

### ⚙️ **Paramètres de Performance**

```python
# Dans dashboard_unified.py, ligne ~67
if len(df) > 50000:
    df = df.sample(n=50000, random_state=42)  # Échantillonnage
```

### 🎨 **Personnalisation Visuelle**

```python
# Couleurs personnalisées
color_discrete_sequence=['#2E86AB', '#A23B72']  # Bleu/Rose
color_continuous_scale='Viridis'  # Échelle de couleurs
```

### 🔌 **Port et Host**

```python
# Modification du port (défaut: 8050)
app.run_server(debug=True, host='0.0.0.0', port=8051)
```

## 🛠️ Dépannage

### ❗ **Problèmes Courants**

#### 1. **Port déjà utilisé**
```bash
# Erreur: Address already in use
# Solution: Changer le port dans dashboard_unified.py
app.run_server(port=8051)  # Au lieu de 8050
```

#### 2. **Données non chargées**
- Vérifiez que les fichiers CSV sont dans le bon répertoire
- Contrôlez le format des délimiteurs (`,` vs `;`)
- Consultez les messages d'erreur dans la console

#### 3. **Graphiques vides**
- Vérifiez les noms des colonnes attendues
- Assurez-vous que les données sont numériques
- Consultez les logs Python pour les erreurs

#### 4. **Performance lente**
- Réduisez la taille de l'échantillon (ligne 67)
- Fermez les autres applications gourmandes
- Utilisez un navigateur moderne (Chrome, Firefox)

### 📋 **Logs de Débogage**

```bash
# Lancement en mode debug
python dashboard_unified.py
# Les erreurs s'affichent dans la console
```

### 🔍 **Vérification des Dépendances**

```bash
# Test des imports
python -c "import dash, plotly, pandas, sklearn; print('✅ Toutes les dépendances OK')"
```

## 📈 Fonctionnalités Avancées

### 🤖 **Machine Learning Intégré**

- **K-Means Clustering** - Segmentation automatique
- **PCA** - Réduction dimensionnelle
- **StandardScaler** - Normalisation des données
- **Détection d'anomalies** - Identification des outliers

### 📊 **Analyses Statistiques**

- **Tests de normalité** - Shapiro-Wilk
- **Corrélations** - Pearson et Spearman
- **Analyses temporelles** - Patterns horaires
- **Profiling descriptif** - Moyennes, médianes, écarts-types

### 🎯 **Métriques Business**

#### 🏦 **Secteur Bancaire**
- Taux de fraude global et par segment
- Montants moyens par type de transaction
- Patterns temporels des fraudes
- ROI de la détection

#### 🛍️ **Secteur Marketing**
- Customer Lifetime Value (CLV)
- Taux de conversion par segment
- Panier moyen par catégorie
- Churn rate et rétention

## 🚀 Évolutions Futures

### 🔮 **Roadmap v3.0**

- [ ] **API REST** - Intégration avec systèmes externes
- [ ] **Base de données** - Persistance des analyses
- [ ] **Alertes temps réel** - Notifications automatiques
- [ ] **Export avancé** - PDF, PowerPoint, Excel
- [ ] **Multi-langues** - Interface EN/FR/ES
- [ ] **Authentification** - Gestion des utilisateurs
- [ ] **Déploiement cloud** - AWS/Azure/GCP

### 🎨 **Améliorations UX**

- [ ] **Thèmes** - Mode sombre/clair
- [ ] **Filtres avancés** - Sélection multi-critères
- [ ] **Annotations** - Commentaires sur graphiques
- [ ] **Favoris** - Sauvegarde de vues
- [ ] **Partage** - URLs de vues spécifiques

## 📞 Support et Contact

### 🆘 **Besoin d'Aide ?**

1. **Documentation** - Consultez ce README
2. **Issues GitHub** - Signalez les bugs
3. **Email** - [soboure.bello@gmail.com](mailto:soboure.bello@gmail.com)
4. **LinkedIn** - [Soboure Bello](https://www.linkedin.com/in/sobourebello/)

### 🤝 **Contribution**

Les contributions sont les bienvenues ! Voir `CONTRIBUTING.md` pour les guidelines.

---

**📧 Contact** : [soboure.bello@gmail.com](mailto:soboure.bello@gmail.com)  
**🔗 Portfolio** : [https://github.com/soboure69](https://github.com/soboure69)  
**💼 LinkedIn** : [https://www.linkedin.com/in/sobourebello/](https://www.linkedin.com/in/sobourebello/)

*Développé avec ❤️ pour la communauté Data Science*

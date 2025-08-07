# Section 3.9 - Déploiement d'un Tableau de Bord Interactif
# À ajouter comme nouvelle cellule dans le notebook EDA_Banque_Marketing.ipynb

print("🔸 SECTION 3.9 - TABLEAU DE BORD INTERACTIF")
print("=" * 50)
print("""
# Section 3.9 - Déploiement d'un Tableau de Bord Interactif

# Création d'un dashboard interactif avec Streamlit
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration de la page Streamlit
def create_fraud_dashboard():
    '''
    Crée un tableau de bord interactif pour l'analyse des fraudes bancaires
    '''
    
    st.set_page_config(
        page_title="🏦 Analyse des Fraudes Bancaires",
        page_icon="🚨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Titre principal
    st.title("🏦 Tableau de Bord - Détection de Fraudes Bancaires")
    st.markdown("---")
    
    # Vérification de la disponibilité des données
    if 'fraud_df' not in locals() and 'fraud_df' not in globals():
        st.error("❌ Dataset de fraude non disponible. Veuillez d'abord charger les données.")
        return
    
    # Utilisation des données globales
    df = fraud_df.copy()
    
    # Sidebar pour les filtres
    st.sidebar.header("🎛️ Filtres et Paramètres")
    
    # Filtre par montant
    min_amount = float(df['Amount'].min())
    max_amount = float(df['Amount'].max())
    amount_range = st.sidebar.slider(
        "💰 Plage de montants",
        min_value=min_amount,
        max_value=max_amount,
        value=(min_amount, max_amount),
        format="%.2f"
    )
    
    # Filtre par temps (si disponible)
    if 'Time' in df.columns:
        df['Time_Hours'] = df['Time'] / 3600
        time_range = st.sidebar.slider(
            "⏰ Plage horaire",
            min_value=0.0,
            max_value=24.0,
            value=(0.0, 24.0),
            step=1.0
        )
        
        # Application des filtres
        df_filtered = df[
            (df['Amount'] >= amount_range[0]) & 
            (df['Amount'] <= amount_range[1]) &
            (df['Time_Hours'] >= time_range[0]) & 
            (df['Time_Hours'] <= time_range[1])
        ]
    else:
        df_filtered = df[
            (df['Amount'] >= amount_range[0]) & 
            (df['Amount'] <= amount_range[1])
        ]
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_transactions = len(df_filtered)
        st.metric("📊 Total Transactions", f"{total_transactions:,}")
    
    with col2:
        fraud_count = df_filtered[target_col].sum()
        st.metric("🚨 Fraudes Détectées", f"{fraud_count:,}")
    
    with col3:
        fraud_rate = (fraud_count / total_transactions * 100) if total_transactions > 0 else 0
        st.metric("📈 Taux de Fraude", f"{fraud_rate:.2f}%")
    
    with col4:
        avg_amount = df_filtered['Amount'].mean()
        st.metric("💵 Montant Moyen", f"${avg_amount:.2f}")
    
    st.markdown("---")
    
    # Graphiques interactifs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Vue d'ensemble", "⏰ Analyse Temporelle", "💰 Analyse des Montants", "🔍 Détection d'Anomalies"])
    
    with tab1:
        st.header("📊 Vue d'ensemble des Transactions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique en secteurs
            fraud_counts = df_filtered[target_col].value_counts()
            fig_pie = px.pie(
                values=fraud_counts.values,
                names=['Normal', 'Fraude'],
                title="Répartition des Types de Transactions",
                color_discrete_sequence=['skyblue', 'salmon']
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Histogramme des montants
            fig_hist = px.histogram(
                df_filtered,
                x='Amount',
                color=target_col,
                nbins=50,
                title="Distribution des Montants par Type",
                labels={'Amount': 'Montant ($)', target_col: 'Type'},
                color_discrete_sequence=['skyblue', 'salmon']
            )
            st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab2:
        if 'Time' in df.columns:
            st.header("⏰ Analyse Temporelle des Fraudes")
            
            # Analyse par heure
            df_filtered['Hour'] = (df_filtered['Time'] / 3600).astype(int) % 24
            hourly_stats = df_filtered.groupby('Hour').agg({
                target_col: ['count', 'sum', 'mean']
            }).reset_index()
            hourly_stats.columns = ['Hour', 'Total', 'Fraudes', 'Taux_Fraude']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Graphique en barres des fraudes par heure
                fig_bar = px.bar(
                    hourly_stats,
                    x='Hour',
                    y='Fraudes',
                    title="Nombre de Fraudes par Heure",
                    labels={'Hour': 'Heure', 'Fraudes': 'Nombre de Fraudes'},
                    color='Fraudes',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                # Courbe du taux de fraude par heure
                fig_line = px.line(
                    hourly_stats,
                    x='Hour',
                    y='Taux_Fraude',
                    title="Taux de Fraude par Heure",
                    labels={'Hour': 'Heure', 'Taux_Fraude': 'Taux de Fraude'},
                    markers=True
                )
                fig_line.update_traces(line_color='red')
                st.plotly_chart(fig_line, use_container_width=True)
            
            # Heatmap temporelle
            if len(df_filtered) > 0:
                df_filtered['Day'] = (df_filtered['Time'] / (3600 * 24)).astype(int)
                heatmap_data = df_filtered.groupby(['Day', 'Hour'])[target_col].sum().reset_index()
                
                if len(heatmap_data) > 0:
                    pivot_data = heatmap_data.pivot(index='Day', columns='Hour', values=target_col).fillna(0)
                    
                    fig_heatmap = px.imshow(
                        pivot_data,
                        title="Heatmap des Fraudes (Jour vs Heure)",
                        labels={'x': 'Heure', 'y': 'Jour', 'color': 'Nombre de Fraudes'},
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info("⚠️ Données temporelles non disponibles")
    
    with tab3:
        st.header("💰 Analyse Détaillée des Montants")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Box plot interactif
            fig_box = px.box(
                df_filtered,
                y='Amount',
                color=target_col,
                title="Distribution des Montants par Type",
                labels={'Amount': 'Montant ($)', target_col: 'Type'},
                color_discrete_sequence=['skyblue', 'salmon']
            )
            st.plotly_chart(fig_box, use_container_width=True)
        
        with col2:
            # Violin plot
            fig_violin = px.violin(
                df_filtered,
                y='Amount',
                color=target_col,
                title="Densité des Montants par Type",
                labels={'Amount': 'Montant ($)', target_col: 'Type'},
                color_discrete_sequence=['skyblue', 'salmon']
            )
            st.plotly_chart(fig_violin, use_container_width=True)
        
        # Statistiques comparatives
        st.subheader("📊 Statistiques Comparatives")
        normal_stats = df_filtered[df_filtered[target_col] == 0]['Amount'].describe()
        fraud_stats = df_filtered[df_filtered[target_col] == 1]['Amount'].describe()
        
        comparison_df = pd.DataFrame({
            'Transactions Normales': normal_stats,
            'Transactions Frauduleuses': fraud_stats
        })
        
        st.dataframe(comparison_df.round(2))
    
    with tab4:
        st.header("🔍 Détection d'Anomalies")
        
        # Calcul des outliers avec IQR
        Q1 = df_filtered['Amount'].quantile(0.25)
        Q3 = df_filtered['Amount'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df_filtered[
            (df_filtered['Amount'] < lower_bound) | 
            (df_filtered['Amount'] > upper_bound)
        ]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🎯 Outliers Détectés", f"{len(outliers):,}")
        
        with col2:
            outlier_rate = (len(outliers) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
            st.metric("📊 Taux d'Outliers", f"{outlier_rate:.2f}%")
        
        with col3:
            if len(outliers) > 0:
                outlier_fraud_rate = outliers[target_col].mean() * 100
                st.metric("🚨 Fraude dans Outliers", f"{outlier_fraud_rate:.2f}%")
            else:
                st.metric("🚨 Fraude dans Outliers", "0.00%")
        
        # Scatter plot avec outliers
        if 'Time' in df_filtered.columns:
            df_filtered['Is_Outlier'] = (
                (df_filtered['Amount'] < lower_bound) | 
                (df_filtered['Amount'] > upper_bound)
            )
            
            fig_scatter = px.scatter(
                df_filtered.sample(min(10000, len(df_filtered))),  # Échantillon pour performance
                x='Time',
                y='Amount',
                color=target_col,
                size='Is_Outlier',
                title="Montant vs Temps (Outliers en gros points)",
                labels={'Time': 'Temps', 'Amount': 'Montant ($)', target_col: 'Type'},
                color_discrete_sequence=['skyblue', 'salmon']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Section de téléchargement des résultats
    st.markdown("---")
    st.header("📥 Téléchargement des Résultats")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bouton pour télécharger les données filtrées
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📊 Télécharger les données filtrées (CSV)",
            data=csv,
            file_name=f"fraud_analysis_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Bouton pour télécharger le rapport des outliers
        if len(outliers) > 0:
            outliers_csv = outliers.to_csv(index=False)
            st.download_button(
                label="🎯 Télécharger les outliers (CSV)",
                data=outliers_csv,
                file_name=f"outliers_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# Code pour lancer le dashboard
if __name__ == "__main__":
    print("🚀 LANCEMENT DU TABLEAU DE BORD INTERACTIF")
    print("=" * 45)
    print("Pour lancer le dashboard, exécutez dans votre terminal :")
    print("streamlit run dashboard_fraud.py")
    print("=" * 45)

# Code à exécuter dans le notebook
print("\\n💡 Instructions pour le déploiement :")
print("1. Copiez ce code dans une nouvelle cellule du notebook")
print("2. Exécutez la cellule pour définir la fonction")
print("3. Pour créer le fichier dashboard séparé, exécutez :")
print("   create_fraud_dashboard()")
print("4. Ou utilisez le code ci-dessous pour créer un fichier .py séparé")
""")

print("\n🔸 CODE POUR CRÉER LE FICHIER DASHBOARD SÉPARÉ")
print("=" * 55)
print("""
# Création du fichier dashboard séparé
dashboard_code = '''
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Configuration de la page
st.set_page_config(
    page_title="🏦 Analyse des Fraudes Bancaires",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chargement des données
@st.cache_data
def load_data():
    """Charge les données de fraude"""
    try:
        # Remplacez par le chemin vers votre fichier CSV
        df = pd.read_csv("creditcard.csv")
        return df
    except FileNotFoundError:
        st.error("❌ Fichier de données non trouvé. Veuillez vérifier le chemin.")
        return None

def main():
    st.title("🏦 Tableau de Bord - Détection de Fraudes Bancaires")
    st.markdown("---")
    
    # Chargement des données
    df = load_data()
    if df is None:
        return
    
    target_col = 'Class'  # Nom de la colonne cible
    
    # Interface utilisateur et visualisations
    # [Insérez ici le code de create_fraud_dashboard() adapté]
    
    # Sidebar pour les filtres
    st.sidebar.header("🎛️ Filtres et Paramètres")
    
    # ... (reste du code du dashboard)

if __name__ == "__main__":
    main()
'''

# Écriture du fichier dashboard
with open('dashboard_fraud.py', 'w', encoding='utf-8') as f:
    f.write(dashboard_code)

print("✅ Fichier dashboard_fraud.py créé avec succès!")
print("\\nPour lancer le dashboard :")
print("1. Ouvrez un terminal")
print("2. Naviguez vers le dossier du projet")
print("3. Exécutez : streamlit run dashboard_fraud.py")
""")

print("\n" + "=" * 80)
print("✅ SECTION 3.9 - TABLEAU DE BORD INTERACTIF CRÉÉE")
print("=" * 80)
print("Cette section inclut :")
print("• 📊 Dashboard interactif avec Streamlit")
print("• 🎛️ Filtres dynamiques pour l'exploration")
print("• 📈 Visualisations interactives avec Plotly")
print("• ⏰ Analyse temporelle des fraudes")
print("• 💰 Analyse détaillée des montants")
print("• 🔍 Détection d'anomalies en temps réel")
print("• 📥 Téléchargement des résultats")
print("=" * 80)

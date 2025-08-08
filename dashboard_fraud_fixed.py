#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Interactif pour l'Analyse des Fraudes Bancaires
=========================================================

Tableau de bord Streamlit pour visualiser et analyser les données de fraude bancaire
avec des graphiques interactifs et des filtres dynamiques.

Auteur: Analyse Exploratoire des Données
Date: 2025-08-08
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="🏦 Analyse des Fraudes Bancaires",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.tab-content {
    padding: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Charge les données de fraude depuis un fichier CSV"""
    try:
        # Essayer de charger le fichier creditcard.csv
        df = pd.read_csv("creditcard.csv")
        return df
    except FileNotFoundError:
        st.error("❌ Fichier 'creditcard.csv' non trouvé dans le répertoire courant.")
        st.info("💡 Veuillez vous assurer que le fichier 'creditcard.csv' est présent dans le même dossier que ce script.")
        return None
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {str(e)}")
        return None

def create_fraud_dashboard(df, target_col='Class'):
    """Crée le tableau de bord principal pour l'analyse des fraudes"""
    
    # En-tête principal
    st.markdown('<h1 class="main-header">🏦 Tableau de Bord - Détection de Fraudes Bancaires</h1>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Informations sur le dataset
    st.sidebar.header("📊 Informations sur les Données")
    st.sidebar.info(f"""
    **Dataset chargé avec succès!**
    - Nombre total de transactions: {len(df):,}
    - Nombre de fraudes: {df[target_col].sum():,}
    - Taux de fraude: {(df[target_col].sum() / len(df) * 100):.3f}%
    - Période couverte: {df['Time'].max() / 3600:.1f} heures
    """)
    
    # Sidebar - Filtres et paramètres
    st.sidebar.header("🎛️ Filtres et Paramètres")
    
    # Filtre par montant
    min_amount, max_amount = float(df['Amount'].min()), float(df['Amount'].max())
    amount_range = st.sidebar.slider(
        "💰 Plage de montants ($)",
        min_value=min_amount,
        max_value=max_amount,
        value=(min_amount, min(max_amount, 1000.0)),  # Limiter la valeur max par défaut
        format="%.2f"
    )
    
    # Filtre par temps
    if 'Time' in df.columns:
        df['Time_Hours'] = df['Time'] / 3600
        max_hours = df['Time_Hours'].max()
        time_range = st.sidebar.slider(
            "⏰ Plage horaire",
            min_value=0.0,
            max_value=max_hours,
            value=(0.0, max_hours),
            step=1.0
        )
        
        # Application des filtres
        df_filtered = df[
            (df['Amount'] >= amount_range[0]) & 
            (df['Amount'] <= amount_range[1]) &
            (df['Time_Hours'] >= time_range[0]) & 
            (df['Time_Hours'] <= time_range[1])
        ].copy()
    else:
        df_filtered = df[
            (df['Amount'] >= amount_range[0]) & 
            (df['Amount'] <= amount_range[1])
        ].copy()
    
    # Échantillonnage pour améliorer les performances
    sample_size = st.sidebar.selectbox(
        "📈 Taille de l'échantillon pour les graphiques",
        options=[1000, 5000, 10000, 25000, "Toutes les données"],
        index=2
    )
    
    if sample_size != "Toutes les données" and len(df_filtered) > sample_size:
        df_display = df_filtered.sample(n=sample_size, random_state=42)
        st.sidebar.warning(f"⚠️ Affichage d'un échantillon de {sample_size:,} transactions pour optimiser les performances.")
    else:
        df_display = df_filtered
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    total_transactions = len(df_filtered)
    fraud_count = int(df_filtered[target_col].sum())
    fraud_rate = (fraud_count / total_transactions * 100) if total_transactions > 0 else 0
    avg_amount = df_filtered['Amount'].mean()
    
    with col1:
        st.metric("📊 Total Transactions", f"{total_transactions:,}")
    
    with col2:
        st.metric("🚨 Fraudes Détectées", f"{fraud_count:,}")
    
    with col3:
        st.metric("📈 Taux de Fraude", f"{fraud_rate:.3f}%")
    
    with col4:
        st.metric("💵 Montant Moyen", f"${avg_amount:.2f}")
    
    st.markdown("---")
    
    # Onglets de visualisation
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Vue d'ensemble", 
        "⏰ Analyse Temporelle", 
        "💰 Analyse des Montants", 
        "🔍 Détection d'Anomalies"
    ])
    
    # Tab 1: Vue d'ensemble
    with tab1:
        st.header("📊 Vue d'ensemble des Transactions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique en secteurs
            fraud_counts = df_filtered[target_col].value_counts()
            labels = ['Transactions Normales', 'Transactions Frauduleuses']
            
            fig_pie = px.pie(
                values=fraud_counts.values,
                names=labels,
                title="Répartition des Types de Transactions",
                color_discrete_sequence=['#87CEEB', '#FA8072']
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Histogramme des montants
            fig_hist = px.histogram(
                df_display,
                x='Amount',
                color=target_col,
                nbins=50,
                title="Distribution des Montants par Type",
                labels={'Amount': 'Montant ($)', target_col: 'Type de Transaction'},
                color_discrete_sequence=['#87CEEB', '#FA8072']
            )
            fig_hist.update_layout(bargap=0.1)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        # Statistiques descriptives
        st.subheader("📈 Statistiques Descriptives")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Transactions Normales**")
            normal_stats = df_filtered[df_filtered[target_col] == 0]['Amount'].describe()
            st.dataframe(normal_stats.round(2))
        
        with col2:
            st.write("**Transactions Frauduleuses**")
            if fraud_count > 0:
                fraud_stats = df_filtered[df_filtered[target_col] == 1]['Amount'].describe()
                st.dataframe(fraud_stats.round(2))
            else:
                st.info("Aucune transaction frauduleuse dans les données filtrées")
    
    # Tab 2: Analyse Temporelle
    with tab2:
        if 'Time' in df.columns:
            st.header("⏰ Analyse Temporelle des Fraudes")
            
            # Analyse par heure
            df_filtered['Hour'] = (df_filtered['Time'] / 3600).astype(int) % 24
            hourly_stats = df_filtered.groupby('Hour').agg({
                target_col: ['count', 'sum', 'mean']
            }).reset_index()
            hourly_stats.columns = ['Hour', 'Total_Transactions', 'Fraudes', 'Taux_Fraude']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Graphique en barres des fraudes par heure
                fig_bar = px.bar(
                    hourly_stats,
                    x='Hour',
                    y='Fraudes',
                    title="Nombre de Fraudes par Heure",
                    labels={'Hour': 'Heure de la journée', 'Fraudes': 'Nombre de Fraudes'},
                    color='Fraudes',
                    color_continuous_scale='Reds'
                )
                fig_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                # Courbe du taux de fraude par heure
                fig_line = px.line(
                    hourly_stats,
                    x='Hour',
                    y='Taux_Fraude',
                    title="Taux de Fraude par Heure",
                    labels={'Hour': 'Heure de la journée', 'Taux_Fraude': 'Taux de Fraude'},
                    markers=True
                )
                fig_line.update_traces(line_color='#DC143C', line_width=3)
                st.plotly_chart(fig_line, use_container_width=True)
            
            # Heatmap temporelle
            if len(df_filtered) > 0:
                st.subheader("🔥 Heatmap Temporelle des Fraudes")
                
                df_filtered['Day'] = (df_filtered['Time'] / (3600 * 24)).astype(int)
                heatmap_data = df_filtered.groupby(['Day', 'Hour'])[target_col].sum().reset_index()
                
                if len(heatmap_data) > 0:
                    pivot_data = heatmap_data.pivot(index='Day', columns='Hour', values=target_col)
                    pivot_data = pivot_data.fillna(0)
                    
                    fig_heatmap = px.imshow(
                        pivot_data,
                        title="Intensité des Fraudes par Jour et Heure",
                        labels={'x': 'Heure de la journée', 'y': 'Jour', 'color': 'Nombre de Fraudes'},
                        color_continuous_scale='Reds',
                        aspect='auto'
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info("⚠️ Données temporelles non disponibles dans ce dataset")
    
    # Tab 3: Analyse des Montants
    with tab3:
        st.header("💰 Analyse Détaillée des Montants")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Box plot interactif
            fig_box = px.box(
                df_display,
                y='Amount',
                color=target_col,
                title="Distribution des Montants par Type",
                labels={'Amount': 'Montant ($)', target_col: 'Type de Transaction'},
                color_discrete_sequence=['#87CEEB', '#FA8072']
            )
            fig_box.update_layout(showlegend=True)
            st.plotly_chart(fig_box, use_container_width=True)
        
        with col2:
            # Violin plot
            fig_violin = px.violin(
                df_display,
                y='Amount',
                color=target_col,
                title="Densité des Montants par Type",
                labels={'Amount': 'Montant ($)', target_col: 'Type de Transaction'},
                color_discrete_sequence=['#87CEEB', '#FA8072']
            )
            st.plotly_chart(fig_violin, use_container_width=True)
        
        # Analyse comparative des montants
        st.subheader("📊 Comparaison des Montants")
        
        if fraud_count > 0:
            normal_amounts = df_filtered[df_filtered[target_col] == 0]['Amount']
            fraud_amounts = df_filtered[df_filtered[target_col] == 1]['Amount']
            
            comparison_data = {
                'Métrique': ['Moyenne', 'Médiane', 'Écart-type', 'Min', 'Max'],
                'Transactions Normales': [
                    normal_amounts.mean(),
                    normal_amounts.median(),
                    normal_amounts.std(),
                    normal_amounts.min(),
                    normal_amounts.max()
                ],
                'Transactions Frauduleuses': [
                    fraud_amounts.mean(),
                    fraud_amounts.median(),
                    fraud_amounts.std(),
                    fraud_amounts.min(),
                    fraud_amounts.max()
                ]
            }
            
            comparison_df = pd.DataFrame(comparison_data)
            comparison_df['Transactions Normales'] = comparison_df['Transactions Normales'].round(2)
            comparison_df['Transactions Frauduleuses'] = comparison_df['Transactions Frauduleuses'].round(2)
            
            st.dataframe(comparison_df, use_container_width=True)
    
    # Tab 4: Détection d'Anomalies
    with tab4:
        st.header("🔍 Détection d'Anomalies")
        
        # Calcul des outliers avec la méthode IQR
        Q1 = df_filtered['Amount'].quantile(0.25)
        Q3 = df_filtered['Amount'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df_filtered[
            (df_filtered['Amount'] < lower_bound) | 
            (df_filtered['Amount'] > upper_bound)
        ]
        
        # Métriques des anomalies
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🎯 Outliers Détectés", f"{len(outliers):,}")
        
        with col2:
            outlier_rate = (len(outliers) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
            st.metric("📊 Taux d'Outliers", f"{outlier_rate:.2f}%")
        
        with col3:
            if len(outliers) > 0:
                outlier_fraud_rate = outliers[target_col].mean() * 100
                st.metric("🚨 % Fraude dans Outliers", f"{outlier_fraud_rate:.1f}%")
            else:
                st.metric("🚨 % Fraude dans Outliers", "0.0%")
        
        # Scatter plot avec indication des outliers
        if 'Time' in df_filtered.columns and len(df_display) > 0:
            st.subheader("📈 Visualisation des Anomalies")
            
            # Créer une colonne pour indiquer les outliers (convertir en numérique)
            df_display_copy = df_display.copy()
            df_display_copy['Is_Outlier'] = (
                (df_display_copy['Amount'] < lower_bound) | 
                (df_display_copy['Amount'] > upper_bound)
            ).astype(int)  # Convertir boolean en int pour Plotly
            
            # Créer des tailles de points basées sur les outliers
            df_display_copy['Point_Size'] = df_display_copy['Is_Outlier'] * 10 + 5
            
            fig_scatter = px.scatter(
                df_display_copy,
                x='Time',
                y='Amount',
                color=target_col,
                size='Point_Size',
                title="Montant vs Temps (Points plus gros = Outliers)",
                labels={
                    'Time': 'Temps (secondes)', 
                    'Amount': 'Montant ($)', 
                    target_col: 'Type de Transaction'
                },
                color_discrete_sequence=['#87CEEB', '#FA8072'],
                size_max=15
            )
            fig_scatter.update_layout(showlegend=True)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Informations sur les seuils de détection
        st.subheader("📋 Seuils de Détection d'Anomalies")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Méthode: Interquartile Range (IQR)**
            - Q1 (25e percentile): ${Q1:.2f}
            - Q3 (75e percentile): ${Q3:.2f}
            - IQR: ${IQR:.2f}
            """)
        
        with col2:
            st.warning(f"""
            **Seuils d'Anomalie:**
            - Seuil inférieur: ${lower_bound:.2f}
            - Seuil supérieur: ${upper_bound:.2f}
            """)
    
    # Section de téléchargement
    st.markdown("---")
    st.header("📥 Téléchargement des Résultats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Télécharger les données filtrées
        csv_filtered = df_filtered.to_csv(index=False)
        st.download_button(
            label="📊 Données Filtrées (CSV)",
            data=csv_filtered,
            file_name=f"fraud_analysis_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Télécharger les outliers
        if len(outliers) > 0:
            csv_outliers = outliers.to_csv(index=False)
            st.download_button(
                label="🎯 Outliers Détectés (CSV)",
                data=csv_outliers,
                file_name=f"outliers_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucun outlier à télécharger")
    
    with col3:
        # Télécharger le rapport de synthèse
        summary_data = {
            'Métrique': [
                'Total Transactions',
                'Fraudes Détectées',
                'Taux de Fraude (%)',
                'Montant Moyen ($)',
                'Outliers Détectés',
                'Taux d\'Outliers (%)'
            ],
            'Valeur': [
                total_transactions,
                fraud_count,
                round(fraud_rate, 3),
                round(avg_amount, 2),
                len(outliers),
                round(outlier_rate, 2)
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        csv_summary = summary_df.to_csv(index=False)
        
        st.download_button(
            label="📋 Rapport de Synthèse (CSV)",
            data=csv_summary,
            file_name=f"fraud_summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def main():
    """Fonction principale du dashboard"""
    
    # Chargement des données
    df = load_data()
    
    if df is not None:
        # Vérifier que les colonnes nécessaires existent
        required_columns = ['Amount', 'Class']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"❌ Colonnes manquantes dans le dataset: {missing_columns}")
            st.info("💡 Le dataset doit contenir au minimum les colonnes 'Amount' et 'Class'")
            return
        
        # Lancer le dashboard
        create_fraud_dashboard(df, target_col='Class')
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>🏦 Dashboard d'Analyse des Fraudes Bancaires | 
            Développé avec ❤️ en utilisant Streamlit et Plotly</p>
            <p>📊 Pour des analyses plus poussées, consultez le notebook Jupyter associé</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Impossible de charger les données. Veuillez vérifier le fichier 'creditcard.csv'")
        
        # Instructions pour l'utilisateur
        st.markdown("""
        ## 📋 Instructions pour utiliser ce dashboard:
        
        1. **Téléchargez le dataset**: Obtenez le fichier `creditcard.csv` depuis Kaggle ou une autre source
        2. **Placez le fichier**: Mettez `creditcard.csv` dans le même dossier que ce script
        3. **Relancez l'application**: Rafraîchissez la page ou relancez Streamlit
        
        ### 🔗 Sources de données recommandées:
        - [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud)
        - Dataset avec colonnes: Time, V1-V28, Amount, Class
        """)

if __name__ == "__main__":
    main()

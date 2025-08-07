import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import glob
import os

# Configuration de la page
st.set_page_config(
    page_title="🛍️ Dashboard Marketing - Segmentation Client",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_marketing_data():
    """Charge les données marketing"""
    try:
        # Recherche du fichier CSV marketing
        csv_files = glob.glob("**/marketing*.csv", recursive=True)
        if not csv_files:
            csv_files = glob.glob("**/*campaign*.csv", recursive=True)
        
        if csv_files:
            # Essayer différents délimiteurs
            try:
                df = pd.read_csv(csv_files[0], sep=',')
                if len(df.columns) == 1:  # Si une seule colonne, essayer point-virgule
                    df = pd.read_csv(csv_files[0], sep=';')
            except:
                df = pd.read_csv(csv_files[0], sep=';')  # Essayer directement point-virgule
            
            st.success(f"✅ Données marketing chargées : {csv_files[0]} ({df.shape[0]} lignes, {df.shape[1]} colonnes)")
            
            # Vérifier si les données sont correctement chargées
            if len(df.columns) == 1:
                st.error("⚠️ Problème de délimiteur détecté. Vérifiez le format du fichier CSV.")
                st.info("💡 Le fichier semble utiliser un délimiteur non standard.")
            
            return df
        else:
            st.error("❌ Fichier marketing non trouvé")
            return None
    except Exception as e:
        st.error(f"❌ Erreur de chargement : {str(e)}")
        return None

def prepare_segmentation_data(df):
    """Prépare les données pour la segmentation"""
    try:
        # Variables de dépenses
        spending_vars = [col for col in df.columns if 'Mnt' in col]
        if spending_vars:
            # Convertir en numérique avant de sommer
            for col in spending_vars:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df['Total_Spending'] = df[spending_vars].sum(axis=1)
        
        # Variables d'achats
        purchase_vars = [col for col in df.columns if 'Num' in col and 'Purchases' in col]
        if purchase_vars:
            # Convertir en numérique avant de sommer
            for col in purchase_vars:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df['Total_Purchases'] = df[purchase_vars].sum(axis=1)
        
        # Variables RFM
        rfm_vars = []
        
        # Vérifier Recency
        if 'Recency' in df.columns:
            df['Recency'] = pd.to_numeric(df['Recency'], errors='coerce')
            if not df['Recency'].isna().all():
                rfm_vars.append('Recency')
        
        # Vérifier Total_Purchases
        if 'Total_Purchases' in df.columns and not df['Total_Purchases'].isna().all():
            rfm_vars.append('Total_Purchases')
        
        # Vérifier Total_Spending
        if 'Total_Spending' in df.columns and not df['Total_Spending'].isna().all():
            rfm_vars.append('Total_Spending')
        
        # Si aucune variable RFM, essayer d'autres variables numériques
        if not rfm_vars:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                rfm_vars = numeric_cols[:3]  # Prendre les 3 premières variables numériques
        
        return df, rfm_vars
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la préparation des données : {str(e)}")
        return df, []

def perform_clustering(df, rfm_vars, n_clusters):
    """Effectue la segmentation K-Means"""
    if not rfm_vars:
        return df, None, None
    
    try:
        # Vérifier que les variables RFM existent et sont numériques
        available_rfm_vars = []
        for var in rfm_vars:
            if var in df.columns:
                # Convertir en numérique si possible
                df[var] = pd.to_numeric(df[var], errors='coerce')
                if df[var].dtype in ['int64', 'float64']:
                    available_rfm_vars.append(var)
        
        if not available_rfm_vars:
            st.warning("⚠️ Aucune variable RFM numérique trouvée pour la segmentation")
            return df, None, None
        
        # Préparation des données
        X = df[available_rfm_vars].copy()
        
        # Gestion des valeurs manquantes
        for col in available_rfm_vars:
            if X[col].isnull().any():
                median_val = X[col].median()
                if pd.isna(median_val):  # Si la médiane est NaN, utiliser 0
                    median_val = 0
                X[col].fillna(median_val, inplace=True)
        
        # Standardisation
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df['Cluster'] = kmeans.fit_predict(X_scaled)
        
        return df, kmeans, X_scaled
        
    except Exception as e:
        st.error(f"❌ Erreur lors du clustering : {str(e)}")
        return df, None, None

def main():
    st.title("🛍️ Dashboard Marketing - Segmentation Client")
    st.markdown("---")
    
    # Chargement des données
    df = load_marketing_data()
    if df is None:
        st.info("💡 Placez un fichier CSV marketing dans le répertoire")
        return
    
    # Préparation des données
    df, rfm_vars = prepare_segmentation_data(df)
    
    # Sidebar
    st.sidebar.header("🎛️ Paramètres de Segmentation")
    
    # Informations dataset
    st.sidebar.markdown("### 📊 Informations Dataset")
    st.sidebar.write(f"**Clients :** {len(df):,}")
    st.sidebar.write(f"**Variables :** {len(df.columns)}")
    
    if rfm_vars:
        st.sidebar.write(f"**Variables RFM :** {len(rfm_vars)}")
        st.sidebar.write(f"- {', '.join(rfm_vars)}")
    
    # Paramètres de clustering
    if rfm_vars:
        n_clusters = st.sidebar.slider("🎯 Nombre de clusters", 2, 8, 4)
        
        # Segmentation
        df, kmeans, X_scaled = perform_clustering(df, rfm_vars, n_clusters)
        
        if 'Cluster' in df.columns:
            st.sidebar.success(f"✅ Segmentation réalisée ({n_clusters} clusters)")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Clients", f"{len(df):,}")
    
    with col2:
        if 'Total_Spending' in df.columns:
            avg_spending = df['Total_Spending'].mean()
            st.metric("💰 Dépense Moyenne", f"${avg_spending:.0f}")
        else:
            st.metric("💰 Dépense Moyenne", "N/A")
    
    with col3:
        if 'Total_Purchases' in df.columns:
            avg_purchases = df['Total_Purchases'].mean()
            st.metric("🛒 Achats Moyens", f"{avg_purchases:.1f}")
        else:
            st.metric("🛒 Achats Moyens", "N/A")
    
    with col4:
        if 'Cluster' in df.columns:
            st.metric("🎯 Segments", f"{df['Cluster'].nunique()}")
        else:
            st.metric("🎯 Segments", "0")
    
    st.markdown("---")
    
    # Onglets
    if 'Cluster' in df.columns:
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Vue d'ensemble", "🎯 Segments", "📈 Analyse RFM", "💡 Recommandations"])
    else:
        tab1, tab2 = st.tabs(["📊 Vue d'ensemble", "📈 Variables"])
    
    with tab1:
        st.header("📊 Vue d'ensemble des Données Marketing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution des dépenses totales
            if 'Total_Spending' in df.columns:
                fig_spending = px.histogram(
                    df, x='Total_Spending', nbins=50,
                    title="Distribution des Dépenses Totales",
                    labels={'Total_Spending': 'Dépenses Totales ($)'}
                )
                st.plotly_chart(fig_spending, use_container_width=True)
        
        with col2:
            # Variables de dépenses par catégorie
            spending_vars = [col for col in df.columns if 'Mnt' in col]
            if spending_vars:
                spending_means = df[spending_vars].mean().sort_values(ascending=True)
                fig_categories = px.bar(
                    x=spending_means.values,
                    y=spending_means.index,
                    orientation='h',
                    title="Dépenses Moyennes par Catégorie",
                    labels={'x': 'Montant Moyen ($)', 'y': 'Catégorie'}
                )
                st.plotly_chart(fig_categories, use_container_width=True)
        
        # Corrélations
        numeric_cols = df.select_dtypes(include=[np.number]).columns[:10]
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            fig_corr = px.imshow(
                corr_matrix,
                title="Matrice de Corrélation",
                color_continuous_scale='RdBu',
                aspect="auto"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
    
    if 'Cluster' in df.columns:
        with tab2:
            st.header("🎯 Analyse des Segments Client")
            
            # Distribution des clusters
            cluster_counts = df['Cluster'].value_counts().sort_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie = px.pie(
                    values=cluster_counts.values,
                    names=[f'Segment {i}' for i in cluster_counts.index],
                    title="Répartition des Segments"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                fig_bar = px.bar(
                    x=[f'Segment {i}' for i in cluster_counts.index],
                    y=cluster_counts.values,
                    title="Nombre de Clients par Segment"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Profil des segments
            if rfm_vars:
                st.subheader("📊 Profil des Segments")
                
                cluster_profiles = df.groupby('Cluster')[rfm_vars].mean().round(2)
                
                # Heatmap des profils
                fig_heatmap = px.imshow(
                    cluster_profiles.T,
                    title="Profil des Segments (Variables RFM)",
                    labels={'x': 'Segment', 'y': 'Variable', 'color': 'Valeur'},
                    aspect="auto"
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
                
                # Tableau des profils
                st.dataframe(cluster_profiles)
        
        with tab3:
            st.header("📈 Analyse RFM Détaillée")
            
            if len(rfm_vars) >= 2:
                # Visualisation PCA
                pca = PCA(n_components=2)
                X_pca = pca.fit_transform(X_scaled)
                
                pca_df = pd.DataFrame({
                    'PC1': X_pca[:, 0],
                    'PC2': X_pca[:, 1],
                    'Cluster': df['Cluster']
                })
                
                fig_pca = px.scatter(
                    pca_df, x='PC1', y='PC2', color='Cluster',
                    title="Visualisation des Segments (PCA)",
                    labels={
                        'PC1': f'PC1 ({pca.explained_variance_ratio_[0]:.1%})',
                        'PC2': f'PC2 ({pca.explained_variance_ratio_[1]:.1%})'
                    }
                )
                st.plotly_chart(fig_pca, use_container_width=True)
            
            # Analyse par variable RFM
            for var in rfm_vars:
                st.subheader(f"📊 Analyse de {var}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_box = px.box(
                        df, x='Cluster', y=var,
                        title=f"Distribution de {var} par Segment"
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
                
                with col2:
                    cluster_means = df.groupby('Cluster')[var].mean()
                    fig_bar = px.bar(
                        x=[f'Segment {i}' for i in cluster_means.index],
                        y=cluster_means.values,
                        title=f"Moyenne de {var} par Segment"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
        
        with tab4:
            st.header("💡 Recommandations Stratégiques")
            
            # Analyse des segments
            for cluster_id in range(n_clusters):
                cluster_data = df[df['Cluster'] == cluster_id]
                size = len(cluster_data)
                pct = (size / len(df)) * 100
                
                with st.expander(f"🎯 Segment {cluster_id} - {size} clients ({pct:.1f}%)"):
                    
                    # Caractéristiques du segment
                    if rfm_vars:
                        st.write("**Profil RFM :**")
                        for var in rfm_vars:
                            mean_val = cluster_data[var].mean()
                            global_mean = df[var].mean()
                            ratio = mean_val / global_mean if global_mean != 0 else 0
                            
                            if ratio > 1.2:
                                status = "🔥 Élevé"
                            elif ratio < 0.8:
                                status = "❄️ Faible"
                            else:
                                status = "⚖️ Moyen"
                            
                            st.write(f"- {var}: {mean_val:.0f} ({ratio:.1f}x global) {status}")
                    
                    # Recommandations basées sur le profil
                    st.write("**Recommandations :**")
                    
                    if 'Recency' in rfm_vars and 'Total_Spending' in rfm_vars:
                        recency = cluster_data['Recency'].mean()
                        spending = cluster_data['Total_Spending'].mean()
                        
                        if recency < df['Recency'].median() and spending > df['Total_Spending'].median():
                            st.success("💎 **Clients VIP** - Fidélisation premium, offres exclusives")
                        elif recency > df['Recency'].median() and spending < df['Total_Spending'].median():
                            st.warning("⚠️ **Clients à risque** - Campagnes de réactivation")
                        elif spending > df['Total_Spending'].median():
                            st.info("💰 **Gros dépensiers** - Upselling, produits premium")
                        else:
                            st.info("📈 **Potentiel de croissance** - Promotions ciblées")
    
    else:
        with tab2:
            st.header("📈 Analyse des Variables")
            st.info("⚠️ Segmentation non disponible - variables RFM manquantes")
            
            # Analyse des variables disponibles
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                selected_var = st.selectbox("Choisir une variable à analyser", numeric_cols)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_hist = px.histogram(df, x=selected_var, title=f"Distribution de {selected_var}")
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    fig_box = px.box(df, y=selected_var, title=f"Box Plot de {selected_var}")
                    st.plotly_chart(fig_box, use_container_width=True)
    
    # Export des résultats
    st.markdown("---")
    st.header("📥 Export des Résultats")
    
    if 'Cluster' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Préparer export segments"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Télécharger données segmentées",
                    data=csv,
                    file_name=f"segmentation_clients_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Préparer rapport segments"):
                if rfm_vars:
                    cluster_summary = df.groupby('Cluster')[rfm_vars].agg(['mean', 'std', 'count']).round(2)
                    summary_csv = cluster_summary.to_csv()
                    st.download_button(
                        label="💾 Télécharger rapport",
                        data=summary_csv,
                        file_name=f"rapport_segments_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )

if __name__ == "__main__":
    main()

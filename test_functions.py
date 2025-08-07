#!/usr/bin/env python3
"""
Script de test des fonctions sans Streamlit
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def prepare_segmentation_data_test(df):
    """Version test de la fonction de préparation"""
    try:
        # Variables de dépenses
        spending_vars = [col for col in df.columns if 'Mnt' in col]
        if spending_vars:
            for col in spending_vars:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df['Total_Spending'] = df[spending_vars].sum(axis=1)
        
        # Variables d'achats
        purchase_vars = [col for col in df.columns if 'Num' in col and 'Purchases' in col]
        if purchase_vars:
            for col in purchase_vars:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df['Total_Purchases'] = df[purchase_vars].sum(axis=1)
        
        # Variables RFM
        rfm_vars = []
        
        if 'Recency' in df.columns:
            df['Recency'] = pd.to_numeric(df['Recency'], errors='coerce')
            if not df['Recency'].isna().all():
                rfm_vars.append('Recency')
        
        if 'Total_Purchases' in df.columns and not df['Total_Purchases'].isna().all():
            rfm_vars.append('Total_Purchases')
        
        if 'Total_Spending' in df.columns and not df['Total_Spending'].isna().all():
            rfm_vars.append('Total_Spending')
        
        if not rfm_vars:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                rfm_vars = numeric_cols[:3]
        
        return df, rfm_vars
        
    except Exception as e:
        print(f"Erreur préparation: {e}")
        return df, []

def perform_clustering_test(df, rfm_vars, n_clusters):
    """Version test de la fonction de clustering"""
    if not rfm_vars:
        return df, None, None
    
    try:
        available_rfm_vars = []
        for var in rfm_vars:
            if var in df.columns:
                df[var] = pd.to_numeric(df[var], errors='coerce')
                if df[var].dtype in ['int64', 'float64']:
                    available_rfm_vars.append(var)
        
        if not available_rfm_vars:
            print("Aucune variable RFM numérique trouvée")
            return df, None, None
        
        X = df[available_rfm_vars].copy()
        
        for col in available_rfm_vars:
            if X[col].isnull().any():
                median_val = X[col].median()
                if pd.isna(median_val):
                    median_val = 0
                X[col].fillna(median_val, inplace=True)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df['Cluster'] = kmeans.fit_predict(X_scaled)
        
        return df, kmeans, X_scaled
        
    except Exception as e:
        print(f"Erreur clustering: {e}")
        return df, None, None

def test_with_sample_data():
    """Test avec des données d'exemple"""
    print("🧪 TEST AVEC DONNÉES D'EXEMPLE")
    print("=" * 35)
    
    # Créer des données de test réalistes
    np.random.seed(42)
    n_samples = 100
    
    test_df = pd.DataFrame({
        'ID': range(1, n_samples + 1),
        'Year_Birth': np.random.randint(1940, 2000, n_samples),
        'Income': np.random.randint(20000, 100000, n_samples),
        'Recency': np.random.randint(1, 100, n_samples),
        'MntWines': np.random.randint(0, 1000, n_samples),
        'MntFruits': np.random.randint(0, 200, n_samples),
        'MntMeatProducts': np.random.randint(0, 500, n_samples),
        'NumWebPurchases': np.random.randint(0, 20, n_samples),
        'NumStorePurchases': np.random.randint(0, 15, n_samples),
        'NumCatalogPurchases': np.random.randint(0, 10, n_samples)
    })
    
    print(f"📊 Données créées: {test_df.shape}")
    print(f"📋 Colonnes: {list(test_df.columns)}")
    
    # Test préparation
    print("\n🔧 Test préparation des données...")
    df_prepared, rfm_vars = prepare_segmentation_data_test(test_df.copy())
    
    print(f"✅ Variables RFM: {rfm_vars}")
    
    if 'Total_Spending' in df_prepared.columns:
        print(f"💰 Total_Spending - Min: {df_prepared['Total_Spending'].min():.0f}, Max: {df_prepared['Total_Spending'].max():.0f}")
    
    if 'Total_Purchases' in df_prepared.columns:
        print(f"🛒 Total_Purchases - Min: {df_prepared['Total_Purchases'].min():.0f}, Max: {df_prepared['Total_Purchases'].max():.0f}")
    
    # Test clustering
    if rfm_vars:
        print("\n🎯 Test clustering...")
        df_clustered, kmeans, X_scaled = perform_clustering_test(df_prepared.copy(), rfm_vars, 4)
        
        if 'Cluster' in df_clustered.columns:
            print(f"✅ Clustering réussi!")
            cluster_counts = df_clustered['Cluster'].value_counts().sort_index()
            print(f"📊 Distribution des clusters:")
            for cluster, count in cluster_counts.items():
                pct = (count / len(df_clustered)) * 100
                print(f"   Cluster {cluster}: {count} clients ({pct:.1f}%)")
            
            # Profil des clusters
            print(f"\n📈 Profil des clusters:")
            cluster_profiles = df_clustered.groupby('Cluster')[rfm_vars].mean().round(2)
            print(cluster_profiles)
            
        else:
            print("❌ Clustering échoué")
    
    return df_clustered if 'Cluster' in locals() and 'Cluster' in df_clustered.columns else None

def test_csv_parsing():
    """Test du parsing CSV avec différents délimiteurs"""
    print("\n📄 TEST PARSING CSV")
    print("=" * 20)
    
    # Données avec point-virgule
    csv_semicolon = """ID;Income;Recency;MntWines
1;50000;10;100
2;60000;20;200
3;55000;15;150"""
    
    # Données avec virgule
    csv_comma = """ID,Income,Recency,MntWines
1,50000,10,100
2,60000,20,200
3,55000,15,150"""
    
    # Test point-virgule
    try:
        from io import StringIO
        df_semicolon = pd.read_csv(StringIO(csv_semicolon), sep=';')
        print(f"✅ CSV point-virgule: {df_semicolon.shape} - Colonnes: {len(df_semicolon.columns)}")
    except Exception as e:
        print(f"❌ Erreur CSV point-virgule: {e}")
    
    # Test virgule
    try:
        df_comma = pd.read_csv(StringIO(csv_comma), sep=',')
        print(f"✅ CSV virgule: {df_comma.shape} - Colonnes: {len(df_comma.columns)}")
    except Exception as e:
        print(f"❌ Erreur CSV virgule: {e}")
    
    # Test auto-détection
    try:
        # Simuler la détection automatique
        test_csv = csv_semicolon
        df_auto = pd.read_csv(StringIO(test_csv), sep=',')
        if len(df_auto.columns) == 1:
            df_auto = pd.read_csv(StringIO(test_csv), sep=';')
        print(f"✅ Auto-détection: {df_auto.shape} - Colonnes: {len(df_auto.columns)}")
    except Exception as e:
        print(f"❌ Erreur auto-détection: {e}")

def main():
    """Fonction principale"""
    print("🔧 TESTS DES FONCTIONS DASHBOARD")
    print("=" * 40)
    
    test_csv_parsing()
    result_df = test_with_sample_data()
    
    print("\n" + "=" * 40)
    if result_df is not None:
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("🚀 Le dashboard marketing devrait fonctionner correctement")
    else:
        print("⚠️ Certains tests ont échoué")
    print("=" * 40)

if __name__ == "__main__":
    main()

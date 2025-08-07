#!/usr/bin/env python3
"""
Script de test pour vérifier le bon fonctionnement des dashboards
"""

import pandas as pd
import numpy as np
import sys
import os

def test_dashboard_imports():
    """Test des imports des dashboards"""
    print("🔍 Test des imports...")
    
    try:
        import dashboard_fraud
        print("✅ dashboard_fraud importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import dashboard_fraud: {e}")
    
    try:
        import dashboard_marketing
        print("✅ dashboard_marketing importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import dashboard_marketing: {e}")

def test_data_loading():
    """Test du chargement des données"""
    print("\n📊 Test du chargement des données...")
    
    # Test données marketing avec différents délimiteurs
    test_data_semicolon = """ID;Year_Birth;Education;Marital_Status;Income;Kidhome;Teenhome;Dt_Customer;Recency;MntWines;MntFruits;MntMeatProducts;MntFishProducts;MntSweetProducts;MntGoldProds;NumDealsPurchases;NumWebPurchases;NumCatalogPurchases;NumStorePurchases;NumWebVisitsMonth;AcceptedCmp3;AcceptedCmp4;AcceptedCmp5;AcceptedCmp1;AcceptedCmp2;Complain;Z_CostContact;Z_Revenue;Response
5524;1957;Graduation;Single;58138;0;0;2012-09-04;58;635;88;546;172;88;88;3;8;10;4;7;0;0;0;0;0;0;3;11;1
2174;1954;Graduation;Single;46344;1;1;2014-03-08;38;11;1;6;2;1;6;2;1;1;2;5;0;0;0;0;0;0;3;11;0"""
    
    # Créer un fichier de test
    with open("test_marketing.csv", "w") as f:
        f.write(test_data_semicolon)
    
    try:
        # Test avec point-virgule
        df_semicolon = pd.read_csv("test_marketing.csv", sep=';')
        print(f"✅ Données avec point-virgule: {df_semicolon.shape}")
        
        # Test avec virgule (devrait échouer)
        df_comma = pd.read_csv("test_marketing.csv", sep=',')
        print(f"⚠️ Données avec virgule: {df_comma.shape}")
        
    except Exception as e:
        print(f"❌ Erreur test données: {e}")
    
    # Nettoyer
    if os.path.exists("test_marketing.csv"):
        os.remove("test_marketing.csv")

def test_data_preparation():
    """Test de la préparation des données"""
    print("\n🔧 Test de la préparation des données...")
    
    # Créer des données de test
    test_df = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5],
        'MntWines': ['100', '200', '150', '300', '250'],
        'MntFruits': ['50', '75', '60', '90', '80'],
        'NumWebPurchases': ['5', '3', '7', '2', '4'],
        'NumStorePurchases': ['2', '1', '3', '1', '2'],
        'Recency': ['10', '20', '15', '25', '30'],
        'Income': ['50000', '60000', '55000', '70000', '65000']
    })
    
    try:
        # Test de la fonction de préparation
        from dashboard_marketing import prepare_segmentation_data
        
        df_prepared, rfm_vars = prepare_segmentation_data(test_df.copy())
        
        print(f"✅ Variables RFM identifiées: {rfm_vars}")
        print(f"✅ Colonnes après préparation: {list(df_prepared.columns)}")
        
        # Vérifier les types de données
        for var in rfm_vars:
            if var in df_prepared.columns:
                print(f"   {var}: {df_prepared[var].dtype}")
        
    except Exception as e:
        print(f"❌ Erreur préparation données: {e}")

def test_clustering():
    """Test du clustering"""
    print("\n🎯 Test du clustering...")
    
    # Créer des données numériques de test
    np.random.seed(42)
    test_df = pd.DataFrame({
        'Recency': np.random.randint(1, 100, 50),
        'Total_Spending': np.random.randint(100, 1000, 50),
        'Total_Purchases': np.random.randint(1, 20, 50)
    })
    
    try:
        from dashboard_marketing import perform_clustering
        
        rfm_vars = ['Recency', 'Total_Spending', 'Total_Purchases']
        df_clustered, kmeans, X_scaled = perform_clustering(test_df.copy(), rfm_vars, 3)
        
        if 'Cluster' in df_clustered.columns:
            print(f"✅ Clustering réussi: {df_clustered['Cluster'].nunique()} clusters")
            print(f"   Distribution: {df_clustered['Cluster'].value_counts().to_dict()}")
        else:
            print("❌ Colonne Cluster non créée")
        
    except Exception as e:
        print(f"❌ Erreur clustering: {e}")

def main():
    """Fonction principale de test"""
    print("🧪 TESTS DES DASHBOARDS")
    print("=" * 30)
    
    test_dashboard_imports()
    test_data_loading()
    test_data_preparation()
    test_clustering()
    
    print("\n" + "=" * 30)
    print("✅ Tests terminés")
    print("💡 Si tous les tests passent, les dashboards devraient fonctionner correctement")

if __name__ == "__main__":
    main()

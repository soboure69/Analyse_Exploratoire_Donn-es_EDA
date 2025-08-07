# Section 4 - Analyse Secteur Marketing - Segmentation Client
# À ajouter comme nouvelles cellules dans le notebook EDA_Banque_Marketing.ipynb

print("🔸 SECTION 4 - ANALYSE SECTEUR MARKETING")
print("=" * 50)

print("\n🔸 SECTION 4.1 - EXPLORATION INITIALE")
print("=" * 40)
print("""
# Section 4.1 - Exploration Initiale du Dataset Marketing

print("🛍️ ANALYSE DU SECTEUR MARKETING - SEGMENTATION CLIENT")
print("=" * 55)

if 'marketing_df' in locals():
    print(f"📊 Dimensions : {marketing_df.shape}")
    print(f"📋 Colonnes : {list(marketing_df.columns)}")
    print("\\n📈 Informations générales :")
    print(marketing_df.info())
    print("\\n👀 Aperçu :")
    display(marketing_df.head())
    print("\\n📊 Statistiques :")
    display(marketing_df.describe())
else:
    print("❌ Dataset marketing non disponible")
""")

print("\n🔸 SECTION 4.2 - QUALITÉ DES DONNÉES")
print("=" * 40)
print("""
# Section 4.2 - Qualité des Données Marketing

if 'marketing_df' in locals():
    print("🔍 ANALYSE DE LA QUALITÉ")
    print("=" * 25)
    
    # Valeurs manquantes
    missing = marketing_df.isnull().sum()
    missing_pct = (missing / len(marketing_df)) * 100
    missing_df = pd.DataFrame({
        'Valeurs_Manquantes': missing,
        'Pourcentage': missing_pct
    }).sort_values('Pourcentage', ascending=False)
    
    print("📋 Valeurs manquantes :")
    display(missing_df[missing_df['Valeurs_Manquantes'] > 0])
    
    # Types et variables
    categorical_cols = marketing_df.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = marketing_df.select_dtypes(include=[np.number]).columns.tolist()
    
    print(f"\\n📊 Variables catégorielles : {categorical_cols}")
    print(f"📊 Variables numériques : {numerical_cols}")
""")

print("\n🔸 SECTION 4.3 - SEGMENTATION K-MEANS")
print("=" * 40)
print("""
# Section 4.3 - Segmentation Client avec K-Means

if 'marketing_df' in locals():
    print("🎯 SEGMENTATION CLIENT")
    print("=" * 25)
    
    # Variables pour segmentation
    spending_vars = [col for col in marketing_df.columns if 'Mnt' in col]
    purchase_vars = [col for col in marketing_df.columns if 'Num' in col and 'Purchases' in col]
    
    if spending_vars:
        marketing_df['Total_Spending'] = marketing_df[spending_vars].sum(axis=1)
    if purchase_vars:
        marketing_df['Total_Purchases'] = marketing_df[purchase_vars].sum(axis=1)
    
    # Variables RFM
    rfm_vars = []
    if 'Recency' in marketing_df.columns:
        rfm_vars.append('Recency')
    if 'Total_Purchases' in marketing_df.columns:
        rfm_vars.append('Total_Purchases')
    if 'Total_Spending' in marketing_df.columns:
        rfm_vars.append('Total_Spending')
    
    print(f"📊 Variables RFM : {rfm_vars}")
    
    if rfm_vars:
        # Préparation données
        X = marketing_df[rfm_vars].fillna(marketing_df[rfm_vars].median())
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Détermination nombre optimal clusters
        from sklearn.metrics import silhouette_score
        silhouette_scores = []
        K_range = range(2, 8)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            labels = kmeans.fit_predict(X_scaled)
            silhouette_scores.append(silhouette_score(X_scaled, labels))
        
        optimal_k = K_range[np.argmax(silhouette_scores)]
        print(f"🎯 Nombre optimal de clusters : {optimal_k}")
        
        # Segmentation finale
        kmeans_final = KMeans(n_clusters=optimal_k, random_state=42)
        marketing_df['Cluster'] = kmeans_final.fit_predict(X_scaled)
        
        print("✅ Segmentation terminée")
        
        # Analyse clusters
        cluster_summary = marketing_df.groupby('Cluster')[rfm_vars].mean().round(2)
        print("\\n📊 Profil des clusters :")
        display(cluster_summary)
        
        # Distribution
        cluster_counts = marketing_df['Cluster'].value_counts().sort_index()
        print("\\n📊 Distribution :")
        for i, count in cluster_counts.items():
            pct = (count / len(marketing_df)) * 100
            print(f"   Cluster {i}: {count} clients ({pct:.1f}%)")
""")

print("\n🔸 SECTION 4.4 - VISUALISATION DES SEGMENTS")
print("=" * 45)
print("""
# Section 4.4 - Visualisation des Segments

if 'marketing_df' in locals() and 'Cluster' in marketing_df.columns:
    print("📊 VISUALISATION DES SEGMENTS")
    print("=" * 30)
    
    # PCA pour visualisation
    if len(rfm_vars) >= 2:
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        
        plt.figure(figsize=(12, 8))
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        
        for i in range(optimal_k):
            mask = marketing_df['Cluster'] == i
            plt.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                       c=colors[i], label=f'Cluster {i}', alpha=0.6)
        
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
        plt.title('Visualisation des Clusters (PCA)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    # Heatmap comparative
    cluster_means = marketing_df.groupby('Cluster')[rfm_vars].mean()
    cluster_normalized = (cluster_means - cluster_means.mean()) / cluster_means.std()
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(cluster_normalized.T, annot=True, cmap='RdYlBu_r', 
                center=0, fmt='.2f')
    plt.title('Profil des Clusters (Standardisé)')
    plt.xlabel('Cluster')
    plt.ylabel('Variables RFM')
    plt.tight_layout()
    plt.show()
    
    # Profiling détaillé
    print("\\n👥 PROFILING DES SEGMENTS")
    print("=" * 25)
    
    for cluster_id in range(optimal_k):
        cluster_data = marketing_df[marketing_df['Cluster'] == cluster_id]
        size = len(cluster_data)
        pct = (size / len(marketing_df)) * 100
        
        print(f"\\n🎯 CLUSTER {cluster_id}")
        print(f"👥 Taille: {size} clients ({pct:.1f}%)")
        
        for var in rfm_vars:
            mean_val = cluster_data[var].mean()
            global_mean = marketing_df[var].mean()
            ratio = mean_val / global_mean if global_mean != 0 else 0
            print(f"💰 {var}: {mean_val:.2f} ({ratio:.2f}x global)")
""")

print("\n" + "=" * 60)
print("✅ SECTION 4 - MARKETING ET SEGMENTATION CRÉÉE")
print("=" * 60)
print("Sections incluses :")
print("• 📊 4.1 - Exploration initiale")
print("• 🔍 4.2 - Qualité des données")
print("• 🎯 4.3 - Segmentation K-Means")
print("• 📊 4.4 - Visualisation des segments")
print("=" * 60)

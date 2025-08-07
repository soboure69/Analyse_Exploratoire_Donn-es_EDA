# Sections avancées à ajouter dans le notebook EDA_Banque_Marketing.ipynb
# Copiez et collez ces sections comme nouvelles cellules dans votre notebook

print("=" * 80)
print("📋 SECTIONS AVANCÉES À AJOUTER DANS LE NOTEBOOK")
print("=" * 80)
print("Copiez chaque section ci-dessous comme nouvelle cellule de code dans votre notebook")
print("=" * 80)

print("\n🔸 SECTION 3.5 - ANALYSE COMPARATIVE")
print("=" * 50)
print("""
# Section 3.5 - Analyse Comparative : Transactions Normales vs Frauduleuses

# Comparaison des distributions entre transactions normales et frauduleuses
if 'fraud_df' in locals():
    print("⚖️ COMPARAISON TRANSACTIONS NORMALES vs FRAUDULEUSES")
    print("=" * 55)
    
    # Séparation des données
    normal_transactions = fraud_df[fraud_df[target_col] == 0]
    fraud_transactions = fraud_df[fraud_df[target_col] == 1]
    
    print(f"📊 Transactions normales : {len(normal_transactions):,}")
    print(f"🚨 Transactions frauduleuses : {len(fraud_transactions):,}")
    
    # Analyse comparative pour les variables clés
    if 'Amount' in fraud_df.columns:
        print("\\n💰 Analyse des montants :")
        print("-" * 25)
        
        # Statistiques comparatives
        normal_amount_stats = normal_transactions['Amount'].describe()
        fraud_amount_stats = fraud_transactions['Amount'].describe()
        
        comparison_df = pd.DataFrame({
            'Transactions_Normales': normal_amount_stats,
            'Transactions_Frauduleuses': fraud_amount_stats
        })
        
        print(comparison_df)
        
        # Test statistique
        stat, p_value = stats.mannwhitneyu(normal_transactions['Amount'], 
                                          fraud_transactions['Amount'], 
                                          alternative='two-sided')
        print(f"\\n📈 Test de Mann-Whitney U :")
        print(f"   Statistique : {stat:.2f}")
        print(f"   P-value : {p_value:.2e}")
        significance = "significative" if p_value < 0.05 else "non significative"
        print(f"   Différence {significance} entre les groupes")
        
        # Visualisation comparative
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Histogrammes comparatifs
        axes[0,0].hist(normal_transactions['Amount'], bins=50, alpha=0.7, 
                      label='Normal', color='skyblue', density=True)
        axes[0,0].hist(fraud_transactions['Amount'], bins=50, alpha=0.7, 
                      label='Fraude', color='salmon', density=True)
        axes[0,0].set_title('Distribution des Montants')
        axes[0,0].set_xlabel('Montant')
        axes[0,0].set_ylabel('Densité')
        axes[0,0].legend()
        
        # Box plots comparatifs
        fraud_df.boxplot(column='Amount', by=target_col, ax=axes[0,1])
        axes[0,1].set_title('Box Plot des Montants par Type')
        axes[0,1].set_xlabel('Type de Transaction')
        
        # Montants en échelle log
        normal_amounts_log = np.log1p(normal_transactions['Amount'])
        fraud_amounts_log = np.log1p(fraud_transactions['Amount'])
        
        axes[1,0].hist(normal_amounts_log, bins=50, alpha=0.7, 
                      label='Normal', color='skyblue', density=True)
        axes[1,0].hist(fraud_amounts_log, bins=50, alpha=0.7, 
                      label='Fraude', color='salmon', density=True)
        axes[1,0].set_title('Distribution des Montants (échelle log)')
        axes[1,0].set_xlabel('Log(Montant + 1)')
        axes[1,0].set_ylabel('Densité')
        axes[1,0].legend()
        
        # Violin plot
        data_for_violin = [normal_transactions['Amount'], fraud_transactions['Amount']]
        axes[1,1].violinplot(data_for_violin, positions=[0, 1])
        axes[1,1].set_title('Violin Plot des Montants')
        axes[1,1].set_xlabel('Type de Transaction')
        axes[1,1].set_ylabel('Montant')
        axes[1,1].set_xticks([0, 1])
        axes[1,1].set_xticklabels(['Normal', 'Fraude'])
        
        plt.tight_layout()
        plt.show()
""")

print("\n🔸 SECTION 3.6 - ANALYSE TEMPORELLE")
print("=" * 50)
print("""
# Section 3.6 - Analyse Temporelle

# Analyse temporelle des fraudes
if 'fraud_df' in locals() and 'Time' in fraud_df.columns:
    print("⏰ ANALYSE TEMPORELLE DES FRAUDES")
    print("=" * 35)
    
    # Conversion du temps en heures
    fraud_df['Time_Hours'] = fraud_df['Time'] / 3600
    
    # Analyse par tranche horaire
    fraud_df['Hour_Bin'] = pd.cut(fraud_df['Time_Hours'], bins=24, labels=range(24))
    
    # Comptage des fraudes par heure
    hourly_fraud = fraud_df.groupby('Hour_Bin')[target_col].agg(['count', 'sum', 'mean']).reset_index()
    hourly_fraud.columns = ['Heure', 'Total_Transactions', 'Fraudes', 'Taux_Fraude']
    hourly_fraud['Heure'] = hourly_fraud['Heure'].astype(int)
    
    print("📊 Statistiques par heure :")
    print(f"   Heure avec le plus de fraudes : {hourly_fraud.loc[hourly_fraud['Fraudes'].idxmax(), 'Heure']}h")
    print(f"   Heure avec le taux de fraude le plus élevé : {hourly_fraud.loc[hourly_fraud['Taux_Fraude'].idxmax(), 'Heure']}h")
    
    # Visualisation temporelle
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Distribution temporelle des transactions
    axes[0,0].hist(fraud_df['Time_Hours'], bins=50, alpha=0.7, color='skyblue')
    axes[0,0].set_title('Distribution Temporelle des Transactions')
    axes[0,0].set_xlabel('Temps (heures)')
    axes[0,0].set_ylabel('Nombre de Transactions')
    
    # Nombre de fraudes par heure
    axes[0,1].bar(hourly_fraud['Heure'], hourly_fraud['Fraudes'], color='salmon', alpha=0.7)
    axes[0,1].set_title('Nombre de Fraudes par Heure')
    axes[0,1].set_xlabel('Heure')
    axes[0,1].set_ylabel('Nombre de Fraudes')
    
    # Taux de fraude par heure
    axes[1,0].plot(hourly_fraud['Heure'], hourly_fraud['Taux_Fraude'], 
                   marker='o', color='red', linewidth=2)
    axes[1,0].set_title('Taux de Fraude par Heure')
    axes[1,0].set_xlabel('Heure')
    axes[1,0].set_ylabel('Taux de Fraude')
    axes[1,0].grid(True, alpha=0.3)
    
    # Heatmap des transactions par heure
    hourly_matrix = hourly_fraud.set_index('Heure')[['Total_Transactions', 'Fraudes']].T
    sns.heatmap(hourly_matrix, annot=False, cmap='YlOrRd', ax=axes[1,1])
    axes[1,1].set_title('Heatmap des Transactions par Heure')
    
    plt.tight_layout()
    plt.show()
    
    # Analyse des patterns temporels
    print("\\n🔍 Patterns temporels identifiés :")
    peak_fraud_hours = hourly_fraud.nlargest(3, 'Fraudes')['Heure'].tolist()
    print(f"   Heures de pic des fraudes : {peak_fraud_hours}")
    
    low_fraud_hours = hourly_fraud.nsmallest(3, 'Fraudes')['Heure'].tolist()
    print(f"   Heures de faible activité frauduleuse : {low_fraud_hours}")
""")

print("\n🔸 SECTION 3.7 - ANALYSE MULTIVARIÉE")
print("=" * 50)
print("""
# Section 3.7 - Analyse Multivariée et Corrélations

# Analyse des corrélations
if 'fraud_df' in locals():
    print("🔗 ANALYSE MULTIVARIÉE ET CORRÉLATIONS")
    print("=" * 40)
    
    # Matrice de corrélation (sélection d'un sous-ensemble pour la lisibilité)
    numeric_cols_subset = fraud_df.select_dtypes(include=[np.number]).columns[:15]
    correlation_matrix = fraud_df[numeric_cols_subset].corr()
    
    # Visualisation de la matrice de corrélation
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', 
                center=0, square=True, linewidths=0.5)
    plt.title('Matrice de Corrélation des Variables')
    plt.tight_layout()
    plt.show()
    
    # Corrélations avec la variable cible
    target_correlations = fraud_df.corr()[target_col].abs().sort_values(ascending=False)
    print("\\n🎯 Corrélations avec la variable cible (valeurs absolues) :")
    print(target_correlations.head(10))
    
    # Variables les plus corrélées avec la fraude
    top_corr_vars = target_correlations.drop(target_col).head(5).index.tolist()
    
    if len(top_corr_vars) >= 2:
        # Analyse PCA pour réduction dimensionnelle
        print("\\n🔬 Analyse en Composantes Principales (PCA)")
        print("-" * 45)
        
        # Préparation des données pour PCA
        features_for_pca = fraud_df[numeric_cols_subset].drop(columns=[target_col])
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_for_pca)
        
        # Application PCA
        pca = PCA()
        pca_result = pca.fit_transform(features_scaled)
        
        # Variance expliquée
        explained_variance_ratio = pca.explained_variance_ratio_
        cumulative_variance = np.cumsum(explained_variance_ratio)
        
        print(f"Variance expliquée par les 5 premières composantes : {cumulative_variance[:5]}")
        
        # Visualisation PCA
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Variance expliquée
        axes[0].plot(range(1, len(explained_variance_ratio) + 1), 
                    cumulative_variance, 'bo-')
        axes[0].set_xlabel('Nombre de Composantes')
        axes[0].set_ylabel('Variance Expliquée Cumulée')
        axes[0].set_title('Variance Expliquée par les Composantes PCA')
        axes[0].grid(True, alpha=0.3)
        
        # Projection 2D des données
        scatter = axes[1].scatter(pca_result[:, 0], pca_result[:, 1], 
                                 c=fraud_df[target_col], cmap='coolwarm', alpha=0.6)
        axes[1].set_xlabel('Première Composante Principale')
        axes[1].set_ylabel('Deuxième Composante Principale')
        axes[1].set_title('Projection PCA des Transactions')
        plt.colorbar(scatter, ax=axes[1], label='Type de Transaction')
        
        plt.tight_layout()
        plt.show()
""")

print("\n🔸 SECTION 3.8 - DÉTECTION D'ANOMALIES")
print("=" * 50)
print("""
# Section 3.8 - Détection d'Anomalies et Patterns

# Détection d'anomalies dans les montants
if 'fraud_df' in locals() and 'Amount' in fraud_df.columns:
    print("🚨 DÉTECTION D'ANOMALIES")
    print("=" * 25)
    
    # Méthode IQR pour détecter les outliers
    Q1 = fraud_df['Amount'].quantile(0.25)
    Q3 = fraud_df['Amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = fraud_df[(fraud_df['Amount'] < lower_bound) | (fraud_df['Amount'] > upper_bound)]
    print(f"📊 Nombre d'outliers détectés : {len(outliers)} ({len(outliers)/len(fraud_df)*100:.2f}%)")
    
    # Analyse des outliers par type de transaction
    outlier_fraud_rate = outliers[target_col].mean()
    normal_fraud_rate = fraud_df[target_col].mean()
    
    print(f"🎯 Taux de fraude dans les outliers : {outlier_fraud_rate:.4f}")
    print(f"🎯 Taux de fraude global : {normal_fraud_rate:.4f}")
    print(f"📈 Ratio : {outlier_fraud_rate/normal_fraud_rate:.2f}x plus élevé")
    
    # Visualisation des anomalies
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Distribution avec outliers marqués
    axes[0].hist(fraud_df['Amount'], bins=100, alpha=0.7, color='skyblue', label='Normal')
    axes[0].hist(outliers['Amount'], bins=50, alpha=0.8, color='red', label='Outliers')
    axes[0].set_xlabel('Montant')
    axes[0].set_ylabel('Fréquence')
    axes[0].set_title('Distribution des Montants avec Outliers')
    axes[0].legend()
    axes[0].set_yscale('log')
    
    # Box plot avec outliers
    fraud_df.boxplot(column='Amount', ax=axes[1])
    axes[1].set_title('Box Plot des Montants')
    axes[1].set_ylabel('Montant')
    
    # Scatter plot montant vs temps coloré par type
    if 'Time' in fraud_df.columns:
        scatter = axes[2].scatter(fraud_df['Time'], fraud_df['Amount'], 
                                 c=fraud_df[target_col], cmap='coolwarm', alpha=0.6, s=1)
        axes[2].set_xlabel('Temps')
        axes[2].set_ylabel('Montant')
        axes[2].set_title('Montant vs Temps par Type')
        plt.colorbar(scatter, ax=axes[2], label='Type de Transaction')
    
    plt.tight_layout()
    plt.show()
""")

print("\n" + "=" * 80)
print("✅ TOUTES LES SECTIONS AVANCÉES SONT PRÊTES À ÊTRE COPIÉES")
print("=" * 80)
print("Instructions :")
print("1. Copiez chaque section ci-dessus")
print("2. Créez une nouvelle cellule de code dans votre notebook")
print("3. Collez le code de la section")
print("4. Exécutez la cellule")
print("5. Répétez pour toutes les sections")
print("=" * 80)

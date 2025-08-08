#!/usr/bin/env python3
"""
Dashboard Unifié EDA - Secteurs Bancaire & Marketing
Utilise Dash et Plotly pour une expérience interactive moderne
"""

import dash
from dash import dcc, html, Input, Output, callback_context
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import os
import glob
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration de l'application Dash
app = dash.Dash(__name__)
app.title = "🏦📊 Dashboard EDA - Bancaire & Marketing"

# Styles CSS personnalisés
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Variables globales pour stocker les données
fraud_data = None
marketing_data = None

def load_fraud_data():
    """Chargement des données de fraude bancaire"""
    global fraud_data
    
    # Patterns de recherche étendus pour les fichiers de fraude
    fraud_patterns = [
        "*credit*.csv", "*fraud*.csv", "*transaction*.csv", 
        "*banking*.csv", "*bank*.csv", "creditcard.csv"
    ]
    
    fraud_files = []
    for pattern in fraud_patterns:
        fraud_files.extend(glob.glob(pattern))
    
    # Supprimer les doublons et trier
    fraud_files = sorted(list(set(fraud_files)))
    
    print(f"🔍 Fichiers trouvés: {fraud_files}")
    
    if fraud_files:
        try:
            # Prendre le premier fichier trouvé
            selected_file = fraud_files[0]
            print(f"📂 Chargement de: {selected_file}")
            
            # Détecter le délimiteur
            with open(selected_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                delimiter = ';' if first_line.count(';') > first_line.count(',') else ','
            
            print(f"🔧 Délimiteur détecté: '{delimiter}'")
            
            # Charger le CSV
            df = pd.read_csv(selected_file, sep=delimiter)
            print(f"📊 Données chargées: {df.shape}")
            print(f"📋 Colonnes: {list(df.columns)[:10]}...")  # Afficher les 10 premières colonnes
            
            # Standardiser les noms de colonnes pour la fraude
            if 'Class' in df.columns:
                df = df.rename(columns={'Class': 'is_fraud'})
                print("✅ Colonne 'Class' renommée en 'is_fraud'")
            elif 'Is_Fraud' in df.columns:
                df = df.rename(columns={'Is_Fraud': 'is_fraud'})
                print("✅ Colonne 'Is_Fraud' renommée en 'is_fraud'")
            elif 'fraud' in df.columns:
                df = df.rename(columns={'fraud': 'is_fraud'})
                print("✅ Colonne 'fraud' renommée en 'is_fraud'")
            else:
                # Si aucune colonne de fraude trouvée, créer une colonne factice
                print("⚠️ Aucune colonne de fraude trouvée, création d'une colonne factice")
                df['is_fraud'] = np.random.choice([0, 1], size=len(df), p=[0.99, 0.01])
            
            # Échantillonnage si le dataset est trop gros
            original_size = len(df)
            if len(df) > 50000:
                df = df.sample(n=50000, random_state=42)
                print(f"📉 Échantillonnage: {original_size} → {len(df)} lignes")
            
            fraud_data = df
            fraud_count = df['is_fraud'].sum() if 'is_fraud' in df.columns else 0
            fraud_rate = (fraud_count / len(df) * 100) if len(df) > 0 else 0
            
            return True, f"✅ Données fraude chargées: {len(df)} transactions ({fraud_count} fraudes, {fraud_rate:.2f}%)"
            
        except Exception as e:
            print(f"❌ Erreur détaillée: {str(e)}")
            import traceback
            traceback.print_exc()
            return False, f"❌ Erreur chargement fraude: {str(e)}"
    
    # Lister les fichiers disponibles pour aider l'utilisateur
    all_csv_files = glob.glob("*.csv")
    if all_csv_files:
        files_list = ", ".join(all_csv_files[:5])  # Afficher les 5 premiers
        return False, f"❌ Aucun fichier de fraude trouvé. Fichiers CSV disponibles: {files_list}"
    else:
        return False, "❌ Aucun fichier CSV trouvé dans le répertoire"

def load_marketing_data():
    """Chargement des données marketing"""
    global marketing_data
    
    # Patterns de recherche étendus pour les fichiers marketing
    marketing_patterns = [
        "*marketing*.csv", "*campaign*.csv", "*customer*.csv",
        "*client*.csv", "*segmentation*.csv", "marketing_campaign.csv"
    ]
    
    marketing_files = []
    for pattern in marketing_patterns:
        marketing_files.extend(glob.glob(pattern))
    
    # Supprimer les doublons et trier
    marketing_files = sorted(list(set(marketing_files)))
    
    print(f"🔍 Fichiers marketing trouvés: {marketing_files}")
    
    if marketing_files:
        try:
            # Prendre le premier fichier trouvé
            selected_file = marketing_files[0]
            print(f"📂 Chargement de: {selected_file}")
            
            # Détecter le délimiteur
            with open(selected_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                delimiter = ';' if first_line.count(';') > first_line.count(',') else ','
            
            print(f"🔧 Délimiteur détecté: '{delimiter}'")
            
            # Charger le CSV
            df = pd.read_csv(selected_file, sep=delimiter)
            print(f"📊 Données marketing chargées: {df.shape}")
            print(f"📋 Colonnes: {list(df.columns)[:10]}...")  # Afficher les 10 premières colonnes
            
            # Préparation des données marketing
            df = prepare_marketing_data(df)
            marketing_data = df
            
            # Statistiques sur la segmentation
            segments_info = ""
            if 'Segment_Name' in df.columns:
                segment_counts = df['Segment_Name'].value_counts()
                segments_info = f" - {len(segment_counts)} segments créés"
            
            return True, f"✅ Données marketing chargées: {len(df)} clients{segments_info}"
            
        except Exception as e:
            print(f"❌ Erreur détaillée marketing: {str(e)}")
            import traceback
            traceback.print_exc()
            return False, f"❌ Erreur chargement marketing: {str(e)}"
    
    # Lister les fichiers disponibles pour aider l'utilisateur
    all_csv_files = glob.glob("*.csv")
    if all_csv_files:
        files_list = ", ".join(all_csv_files[:5])  # Afficher les 5 premiers
        return False, f"❌ Aucun fichier marketing trouvé. Fichiers CSV disponibles: {files_list}"
    else:
        return False, "❌ Aucun fichier CSV trouvé dans le répertoire"

def prepare_marketing_data(df):
    """Préparation des données marketing avec segmentation RFM"""
    try:
        # Variables de dépenses (Monetary)
        spending_vars = [col for col in df.columns if 'Mnt' in col]
        if spending_vars:
            for col in spending_vars:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df['Total_Spending'] = df[spending_vars].sum(axis=1)
        
        # Variables d'achats (Frequency)
        purchase_vars = [col for col in df.columns if 'Num' in col and 'Purchases' in col]
        if purchase_vars:
            for col in purchase_vars:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df['Total_Purchases'] = df[purchase_vars].sum(axis=1)
        
        # Recency
        if 'Recency' in df.columns:
            df['Recency'] = pd.to_numeric(df['Recency'], errors='coerce')
        
        # Segmentation RFM
        rfm_vars = []
        if 'Recency' in df.columns and not df['Recency'].isna().all():
            rfm_vars.append('Recency')
        if 'Total_Purchases' in df.columns and not df['Total_Purchases'].isna().all():
            rfm_vars.append('Total_Purchases')
        if 'Total_Spending' in df.columns and not df['Total_Spending'].isna().all():
            rfm_vars.append('Total_Spending')
        
        # Clustering K-Means si variables RFM disponibles
        if len(rfm_vars) >= 2:
            X = df[rfm_vars].copy()
            
            # Gestion des valeurs manquantes
            for col in rfm_vars:
                median_val = X[col].median()
                if pd.isna(median_val):
                    median_val = 0
                X[col].fillna(median_val, inplace=True)
            
            # Standardisation et clustering
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
            df['Segment'] = kmeans.fit_predict(X_scaled)
            
            # Noms des segments
            segment_names = {0: 'Champions', 1: 'Loyaux', 2: 'Potentiels', 3: 'Endormis'}
            df['Segment_Name'] = df['Segment'].map(segment_names)
        
        return df
        
    except Exception as e:
        print(f"Erreur préparation marketing: {e}")
        return df

def create_fraud_analysis():
    """Création des graphiques d'analyse de fraude"""
    if fraud_data is None:
        return html.Div("❌ Données de fraude non disponibles")
    
    df = fraud_data
    
    # Graphique 1: Distribution des fraudes
    fraud_counts = df['is_fraud'].value_counts()
    fig1 = px.pie(
        values=fraud_counts.values,
        names=['Normal', 'Fraude'],
        title="📊 Distribution des Transactions",
        color_discrete_sequence=['#2E86AB', '#A23B72']
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    
    # Graphique 2: Montants par type de transaction
    if 'Amount' in df.columns:
        fig2 = px.box(
            df, 
            x='is_fraud', 
            y='Amount',
            title="💰 Distribution des Montants",
            labels={'is_fraud': 'Type Transaction', 'Amount': 'Montant (€)'}
        )
        fig2.update_xaxis(tickvals=[0, 1], ticktext=['Normal', 'Fraude'])
    else:
        fig2 = go.Figure()
        fig2.add_annotation(text="Colonne 'Amount' non trouvée", 
                           xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Graphique 3: Analyse temporelle (si colonne Time disponible)
    if 'Time' in df.columns:
        df['Hour'] = (df['Time'] / 3600) % 24
        hourly_fraud = df.groupby('Hour')['is_fraud'].agg(['count', 'sum']).reset_index()
        hourly_fraud['fraud_rate'] = (hourly_fraud['sum'] / hourly_fraud['count']) * 100
        
        fig3 = px.line(
            hourly_fraud, 
            x='Hour', 
            y='fraud_rate',
            title="⏰ Taux de Fraude par Heure",
            labels={'Hour': 'Heure', 'fraud_rate': 'Taux de Fraude (%)'}
        )
        fig3.update_traces(line_color='#F18F01')
    else:
        fig3 = go.Figure()
        fig3.add_annotation(text="Analyse temporelle non disponible", 
                           xref="paper", yref="paper", x=0.5, y=0.5)
    
    return html.Div([
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3)
    ])

def create_marketing_analysis():
    """Création des graphiques d'analyse marketing"""
    if marketing_data is None:
        return html.Div("❌ Données marketing non disponibles")
    
    df = marketing_data
    
    # Graphique 1: Distribution des segments
    if 'Segment_Name' in df.columns:
        segment_counts = df['Segment_Name'].value_counts()
        fig1 = px.bar(
            x=segment_counts.index,
            y=segment_counts.values,
            title="🎯 Distribution des Segments Clients",
            labels={'x': 'Segment', 'y': 'Nombre de Clients'},
            color=segment_counts.values,
            color_continuous_scale='Viridis'
        )
    else:
        fig1 = go.Figure()
        fig1.add_annotation(text="Segmentation non disponible", 
                           xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Graphique 2: Analyse RFM
    if all(col in df.columns for col in ['Total_Spending', 'Total_Purchases', 'Recency']):
        fig2 = px.scatter_3d(
            df,
            x='Total_Spending',
            y='Total_Purchases',
            z='Recency',
            color='Segment_Name' if 'Segment_Name' in df.columns else None,
            title="📈 Analyse RFM 3D",
            labels={
                'Total_Spending': 'Dépenses Totales (€)',
                'Total_Purchases': 'Achats Totaux',
                'Recency': 'Récence (jours)'
            }
        )
    else:
        fig2 = go.Figure()
        fig2.add_annotation(text="Variables RFM non disponibles", 
                           xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Graphique 3: Profil des segments
    if 'Segment_Name' in df.columns and 'Total_Spending' in df.columns:
        segment_profiles = df.groupby('Segment_Name').agg({
            'Total_Spending': 'mean',
            'Total_Purchases': 'mean',
            'Recency': 'mean'
        }).round(2)
        
        fig3 = px.bar(
            segment_profiles.reset_index(),
            x='Segment_Name',
            y='Total_Spending',
            title="💰 Dépenses Moyennes par Segment",
            labels={'Segment_Name': 'Segment', 'Total_Spending': 'Dépenses Moyennes (€)'},
            color='Total_Spending',
            color_continuous_scale='Blues'
        )
    else:
        fig3 = go.Figure()
        fig3.add_annotation(text="Profil des segments non disponible", 
                           xref="paper", yref="paper", x=0.5, y=0.5)
    
    return html.Div([
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3)
    ])

# Layout de l'application
app.layout = html.Div([
    # Header
    html.Div([
        html.H1([
            html.I(className="fas fa-chart-line", style={'margin-right': '10px'}),
            "Dashboard EDA - Bancaire & Marketing"
        ], style={
            'text-align': 'center',
            'color': '#2E86AB',
            'margin-bottom': '30px',
            'font-family': 'Arial, sans-serif'
        }),
        
        # Boutons de chargement des données
        html.Div([
            html.Button([
                html.I(className="fas fa-university", style={'margin-right': '8px'}),
                "Charger Données Bancaires"
            ], id='load-fraud-btn', n_clicks=0, className='button-primary',
               style={'margin-right': '20px'}),
            
            html.Button([
                html.I(className="fas fa-shopping-cart", style={'margin-right': '8px'}),
                "Charger Données Marketing"
            ], id='load-marketing-btn', n_clicks=0, className='button-primary'),
        ], style={'text-align': 'center', 'margin-bottom': '20px'}),
        
        # Status des données
        html.Div(id='data-status', style={
            'text-align': 'center',
            'margin-bottom': '30px',
            'font-weight': 'bold'
        })
    ]),
    
    # Onglets principaux
    dcc.Tabs(id='main-tabs', value='fraud-tab', children=[
        dcc.Tab(label='🏦 Analyse Bancaire', value='fraud-tab', children=[
            html.Div(id='fraud-content', style={'padding': '20px'})
        ]),
        dcc.Tab(label='🛍️ Analyse Marketing', value='marketing-tab', children=[
            html.Div(id='marketing-content', style={'padding': '20px'})
        ]),
        dcc.Tab(label='📊 Vue Comparative', value='comparison-tab', children=[
            html.Div(id='comparison-content', style={'padding': '20px'})
        ])
    ]),
    
    # Footer
    html.Footer([
        html.Hr(),
        html.P([
            "Développé avec ❤️ par ",
            html.A("Soboure Bello", href="mailto:soboure.bello@gmail.com"),
            " | ",
            html.A("GitHub", href="https://github.com/soboure69", target="_blank"),
            " | ",
            html.A("LinkedIn", href="https://www.linkedin.com/in/sobourebello/", target="_blank")
        ], style={
            'text-align': 'center',
            'color': '#666',
            'margin-top': '40px'
        })
    ])
], style={
    'font-family': 'Arial, sans-serif',
    'margin': '0 auto',
    'max-width': '1200px',
    'padding': '20px'
})

# Callbacks
@app.callback(
    Output('data-status', 'children'),
    [Input('load-fraud-btn', 'n_clicks'),
     Input('load-marketing-btn', 'n_clicks')]
)
def update_data_status(fraud_clicks, marketing_clicks):
    """Mise à jour du statut des données"""
    ctx = callback_context
    
    if not ctx.triggered:
        return "📋 Cliquez sur les boutons pour charger les données"
    
    messages = []
    
    if fraud_clicks > 0:
        success, message = load_fraud_data()
        messages.append(message)
    
    if marketing_clicks > 0:
        success, message = load_marketing_data()
        messages.append(message)
    
    return html.Div([html.P(msg) for msg in messages])

@app.callback(
    Output('fraud-content', 'children'),
    [Input('load-fraud-btn', 'n_clicks')]
)
def update_fraud_content(n_clicks):
    """Mise à jour du contenu d'analyse bancaire"""
    if n_clicks > 0:
        return create_fraud_analysis()
    return html.Div("👆 Cliquez sur 'Charger Données Bancaires' pour commencer l'analyse")

@app.callback(
    Output('marketing-content', 'children'),
    [Input('load-marketing-btn', 'n_clicks')]
)
def update_marketing_content(n_clicks):
    """Mise à jour du contenu d'analyse marketing"""
    if n_clicks > 0:
        return create_marketing_analysis()
    return html.Div("👆 Cliquez sur 'Charger Données Marketing' pour commencer l'analyse")

@app.callback(
    Output('comparison-content', 'children'),
    [Input('load-fraud-btn', 'n_clicks'),
     Input('load-marketing-btn', 'n_clicks')]
)
def update_comparison_content(fraud_clicks, marketing_clicks):
    """Mise à jour de la vue comparative"""
    if fraud_clicks > 0 and marketing_clicks > 0:
        # Créer une vue comparative des deux datasets
        comparison_stats = []
        
        if fraud_data is not None:
            comparison_stats.append({
                'Dataset': 'Bancaire',
                'Lignes': len(fraud_data),
                'Colonnes': len(fraud_data.columns),
                'Fraudes/Segments': fraud_data['is_fraud'].sum() if 'is_fraud' in fraud_data.columns else 'N/A'
            })
        
        if marketing_data is not None:
            comparison_stats.append({
                'Dataset': 'Marketing',
                'Lignes': len(marketing_data),
                'Colonnes': len(marketing_data.columns),
                'Fraudes/Segments': len(marketing_data['Segment_Name'].unique()) if 'Segment_Name' in marketing_data.columns else 'N/A'
            })
        
        if comparison_stats:
            df_comparison = pd.DataFrame(comparison_stats)
            
            fig = go.Figure(data=[
                go.Bar(name='Lignes', x=df_comparison['Dataset'], y=df_comparison['Lignes']),
                go.Bar(name='Colonnes', x=df_comparison['Dataset'], y=df_comparison['Colonnes'])
            ])
            fig.update_layout(
                title="📊 Comparaison des Datasets",
                barmode='group',
                xaxis_title="Dataset",
                yaxis_title="Nombre"
            )
            
            return html.Div([
                dcc.Graph(figure=fig),
                html.Table([
                    html.Thead([
                        html.Tr([html.Th(col) for col in df_comparison.columns])
                    ]),
                    html.Tbody([
                        html.Tr([html.Td(df_comparison.iloc[i][col]) for col in df_comparison.columns])
                        for i in range(len(df_comparison))
                    ])
                ], style={'margin': '20px auto', 'width': '80%'})
            ])
    
    return html.Div("📊 Chargez les deux datasets pour voir la comparaison")

# CSS personnalisé
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .button-primary {
                background-color: #2E86AB;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            .button-primary:hover {
                background-color: #1e5f7a;
            }
            .tab-content {
                border: 1px solid #d6d6d6;
                border-top: none;
                padding: 20px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    print("🚀 Lancement du Dashboard Unifié EDA en Banque et Marketing")
    print("📊 Accès: http://localhost:8050")
    print("🔧 Ctrl+C pour arrêter")
    
    app.run(debug=True, host='0.0.0.0', port=8050)

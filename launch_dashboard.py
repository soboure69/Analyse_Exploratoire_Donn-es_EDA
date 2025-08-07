#!/usr/bin/env python3
"""
Script de lancement du tableau de bord interactif pour l'analyse des fraudes bancaires
"""

import subprocess
import sys
import os
import webbrowser
import time

def check_requirements():
    """Vérifie si les packages requis sont installés"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'seaborn',
        'matplotlib',
        'scipy',
        'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_requirements():
    """Installe les packages manquants"""
    print("📦 Installation des dépendances...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Toutes les dépendances ont été installées avec succès!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation des dépendances: {e}")
        return False

def launch_dashboard():
    """Lance le tableau de bord Streamlit"""
    print("🚀 Lancement du tableau de bord...")
    print("=" * 50)
    print("📊 Tableau de Bord - Détection de Fraudes Bancaires")
    print("🌐 Le dashboard va s'ouvrir dans votre navigateur")
    print("🛑 Pour arrêter le serveur, appuyez sur Ctrl+C")
    print("=" * 50)
    
    try:
        # Lancement de Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "dashboard_fraud.py",
            "--server.port=8501",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du tableau de bord...")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

def main():
    """Fonction principale"""
    print("🏦 TABLEAU DE BORD - DÉTECTION DE FRAUDES BANCAIRES")
    print("=" * 55)
    
    # Vérification du fichier dashboard
    if not os.path.exists("dashboard_fraud.py"):
        print("❌ Fichier dashboard_fraud.py non trouvé!")
        print("💡 Assurez-vous d'être dans le bon répertoire.")
        return
    
    # Vérification des dépendances
    print("🔍 Vérification des dépendances...")
    missing = check_requirements()
    
    if missing:
        print(f"⚠️  Packages manquants: {', '.join(missing)}")
        
        if os.path.exists("requirements.txt"):
            install_choice = input("📦 Installer les dépendances manquantes? (o/n): ").lower().strip()
            if install_choice in ['o', 'oui', 'y', 'yes']:
                if not install_requirements():
                    return
            else:
                print("❌ Installation annulée. Le dashboard ne peut pas fonctionner sans les dépendances.")
                return
        else:
            print("❌ Fichier requirements.txt non trouvé!")
            print("💡 Installez manuellement les packages : streamlit, pandas, numpy, plotly, etc.")
            return
    else:
        print("✅ Toutes les dépendances sont installées!")
    
    # Lancement du dashboard
    launch_dashboard()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script de lancement du Dashboard Unifié EDA
Vérifie les dépendances et lance l'application Dash
"""

import sys
import subprocess
import importlib
import os

def check_and_install_package(package_name, import_name=None):
    """Vérifie et installe un package si nécessaire"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError:
        print(f"⚠️ {package_name} manquant - Installation...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✅ {package_name} - Installé")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Erreur installation {package_name}")
            return False

def main():
    """Fonction principale"""
    print("🚀 DASHBOARD UNIFIÉ EDA - LANCEMENT")
    print("=" * 50)
    
    # Vérification de Python
    print(f"🐍 Python {sys.version}")
    
    # Liste des dépendances requises
    dependencies = [
        ("dash", "dash"),
        ("plotly", "plotly"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("scikit-learn", "sklearn"),
    ]
    
    print("\n🔍 Vérification des dépendances:")
    all_ok = True
    
    for package, import_name in dependencies:
        if not check_and_install_package(package, import_name):
            all_ok = False
    
    if not all_ok:
        print("\n❌ Certaines dépendances n'ont pas pu être installées")
        input("Appuyez sur Entrée pour continuer quand même...")
    
    print("\n🎯 Lancement du dashboard...")
    print("📍 URL: http://localhost:8050")
    print("🛑 Ctrl+C pour arrêter")
    print("-" * 50)
    
    # Changement vers le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Import et lancement du dashboard
    try:
        from dashboard_unified import app
        app.run(debug=False, host='0.0.0.0', port=8050)
    except ImportError:
        print("❌ Impossible d'importer dashboard_unified.py")
        print("📁 Vérifiez que le fichier existe dans le même répertoire")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
    
    input("\nAppuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur pour le Dashboard de Fraudes Bancaires
==============================================

Script simple pour lancer le dashboard Streamlit
"""

import subprocess
import sys
import os

def main():
    """Lance le dashboard Streamlit"""
    
    print("🚀 Lancement du Dashboard de Fraudes Bancaires")
    print("=" * 50)
    
    # Vérifier que le fichier dashboard existe
    dashboard_file = "dashboard_fraud_fixed.py"
    if not os.path.exists(dashboard_file):
        print(f"❌ Erreur: Le fichier {dashboard_file} n'existe pas")
        return
    
    # Vérifier que streamlit est installé
    try:
        import streamlit
        print("✅ Streamlit détecté")
    except ImportError:
        print("❌ Streamlit n'est pas installé")
        print("💡 Installez-le avec: pip install streamlit")
        return
    
    # Lancer le dashboard
    try:
        print(f"🌐 Lancement du dashboard: {dashboard_file}")
        print("📱 Le dashboard s'ouvrira dans votre navigateur web")
        print("🛑 Pour arrêter le serveur, appuyez sur Ctrl+C")
        print("-" * 50)
        
        # Lancer streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", dashboard_file,
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

if __name__ == "__main__":
    main()

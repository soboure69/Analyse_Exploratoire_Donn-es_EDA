@echo off
echo ========================================================
echo 🏦 TABLEAU DE BORD - DETECTION DE FRAUDES BANCAIRES
echo ========================================================
echo.
echo 🚀 Lancement du tableau de bord interactif...
echo 🌐 Le dashboard va s'ouvrir dans votre navigateur
echo 🛑 Pour arreter le serveur, fermez cette fenetre
echo.
echo ========================================================

REM Vérification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou non accessible
    echo 💡 Veuillez installer Python et l'ajouter au PATH
    pause
    exit /b 1
)

REM Vérification de Streamlit
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Streamlit n'est pas installé
    echo 📦 Installation de Streamlit...
    pip install streamlit
)

REM Vérification du fichier dashboard
if not exist "dashboard_fraud.py" (
    echo ❌ Fichier dashboard_fraud.py non trouvé!
    echo 💡 Assurez-vous d'être dans le bon répertoire
    pause
    exit /b 1
)

REM Lancement du dashboard
echo ✅ Lancement du dashboard...
"C:\Users\bello\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\streamlit.exe" run dashboard_fraud.py --server.port=8501

pause

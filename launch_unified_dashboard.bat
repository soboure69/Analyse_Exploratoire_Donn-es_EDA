@echo off
title Dashboard Unifié EDA - Bancaire & Marketing

echo.
echo ========================================
echo 🚀 DASHBOARD UNIFIÉ EDA
echo ========================================
echo.
echo 📊 Secteurs: Bancaire + Marketing
echo 🛠️ Technologie: Dash + Plotly
echo 🌐 Interface: Web Interactive
echo.

REM Vérification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo 📥 Téléchargez Python depuis: https://python.org
    pause
    exit /b 1
)

REM Vérification des dépendances
echo 🔍 Vérification des dépendances...
python -c "import dash, plotly, pandas, sklearn" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Installation des dépendances manquantes...
    pip install dash plotly pandas scikit-learn numpy
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation des dépendances
        pause
        exit /b 1
    )
)

echo ✅ Dépendances vérifiées

REM Changement vers le répertoire du script
cd /d "%~dp0"

echo.
echo 🎯 Lancement du dashboard...
echo 📍 URL: http://localhost:8050
echo 🛑 Appuyez sur Ctrl+C pour arrêter
echo.

REM Lancement du dashboard
python dashboard_unified.py

pause

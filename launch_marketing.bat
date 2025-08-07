@echo off
echo ========================================================
echo 🛍️ DASHBOARD MARKETING - SEGMENTATION CLIENT
echo ========================================================
echo.
echo 🚀 Lancement du dashboard marketing...
echo 🌐 Le dashboard va s'ouvrir dans votre navigateur
echo 🛑 Pour arreter le serveur, fermez cette fenetre
echo.
echo ========================================================

REM Vérification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou non accessible
    pause
    exit /b 1
)

REM Vérification du fichier dashboard
if not exist "dashboard_marketing.py" (
    echo ❌ Fichier dashboard_marketing.py non trouvé!
    pause
    exit /b 1
)

REM Lancement du dashboard marketing
echo ✅ Lancement du dashboard marketing...
"C:\Users\bello\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\streamlit.exe" run dashboard_marketing.py --server.port=8502

pause

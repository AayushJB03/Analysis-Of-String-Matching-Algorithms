
@echo off
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Starting Streamlit app...
streamlit run streamlit_app.py

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Immo Predictor Rabat",
    page_icon="🏠",
    layout="centered"
)

@st.cache_resource
def load_model():
    try:
        model = joblib.load('models/price_predictor.pkl')
        return model
    except FileNotFoundError:
        return None

model = load_model()


st.title("🇲🇦 Prédicteur de Prix Immobilier (Rabat)")
st.markdown("Ce projet utilise le **Machine Learning** pour estimer le prix d'un appartement basé sur des données scrapées sur Avito.")

if model is None:
    st.error("Erreur : Le modèle n'est pas trouvé. As-tu bien lancé `src/model.py` ?")
else:
    with st.form("prediction_form"):
        st.subheader("Entrez les caractéristiques :")
        
        quartier = st.selectbox(
            "Quartier",
            ["Agdal", "Hay Riad", "Hassan", "Océan", "Souissi", "Autre"]
        )
        
        surface = st.slider("Surface (m²)", min_value=30, max_value=300, value=80, step=5)
        
        submitted = st.form_submit_button("Estimer le Prix")

    if submitted:
        input_data = pd.DataFrame({
            'surface_final': [surface],
            'quartier': [quartier],
            'ville': ['Rabat'] 
        })
        
        prediction = model.predict(input_data)[0]
        
        st.success(f"Estimation : {prediction:,.0f} DH")
        
        prix_m2 = prediction / surface
        st.info(f"Soit environ {prix_m2:,.0f} DH / m²")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import joblib 
import os

def train_model():
    print("Démarrage de l'entraînement...")

    try:
        df = pd.read_csv('data/processed/cleaned_listings.csv')
    except FileNotFoundError:
        print("Erreur : Fichier cleaned_listings.csv introuvable.")
        return

    X = df[['surface_final', 'quartier', 'ville']] 
    y = df['prix_final']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Entraînement sur {len(X_train)} annonces, Test sur {len(X_test)} annonces.")

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['quartier', 'ville'])
        ],
        remainder='passthrough' 
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    print(f"\n Performance du modèle :")
    print(f"Erreur Moyenne Absolue (MAE) : {mae:,.0f} DH")
    print("Cela veut dire que le modèle se trompe en moyenne de ce montant.")

    avg_price = y.mean()
    error_percentage = (mae / avg_price) * 100
    print(f"Marge d'erreur relative : {error_percentage:.2f}%")
    os.makedirs('models', exist_ok=True)
    
    joblib.dump(model, 'models/price_predictor.pkl')
    print("\nCerveau sauvegardé sous : models/price_predictor.pkl")
    print("Prêt pour l'application Streamlit !")

if __name__ == "__main__":
    train_model()
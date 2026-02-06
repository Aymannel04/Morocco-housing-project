import pandas as pd
import re

def clean_existing_price(price_str):
    
    if pd.isna(price_str) or price_str == "0" or price_str == "Non défini":
        return None
    
    # On transforme "3 800 000 DH" ou "3 800 000" en entier 3800000
    # On garde que les chiffres
    clean_str = re.sub(r'[^\d]', '', str(price_str))
    
    try:
        val = int(clean_str)
        if val < 10000: # Filtre anti-bruit (prix trop bas = erreur ou location par nuit)
            return None
        return val
    except:
        return None

def extract_surface(text):
    if not isinstance(text, str): return None
    match = re.search(r'(\d+)\s*m²', text)
    if match:
        return int(match.group(1))
    return None

def extract_location(text):
    if not isinstance(text, str): return "Rabat", "Autre" 
    
    match = re.search(r'Appartements dans\s+(.*)', text)
    
    if match:
        full_loc = match.group(1)
        parts = full_loc.split(',')
        
        if len(parts) >= 2:
            return parts[0].strip(), parts[1].strip() 
        else:
            return parts[0].strip(), "Autre"
            
    if "Agdal" in text: return "Rabat", "Agdal"
    if "Hay Riad" in text: return "Rabat", "Hay Riad"
    if "Hassan" in text: return "Rabat", "Hassan"
    
    return "Rabat", "Autre"

def run_cleaning():
    print("Démarrage du nettoyage (Version Optimisée)...")
    
    try:
        df = pd.read_csv('data/raw/avito_listings.csv')
    except FileNotFoundError:
        print("Erreur : Fichier introuvable.")
        return

    print("... Nettoyage des prix")
    df['prix_final'] = df['prix_extracted'].apply(clean_existing_price)
    
    print("... Extraction des surfaces")
    df['surface_final'] = df['raw_text'].apply(extract_surface)
    
    print("... Extraction des quartiers")
    loc_data = df['raw_text'].apply(lambda x: extract_location(x))
    df['ville'] = [x[0] for x in loc_data]
    df['quartier'] = [x[1] for x in loc_data]
    initial_count = len(df)
    
    df_clean = df.dropna(subset=['prix_final', 'surface_final'])
    
    df_clean = df_clean[df_clean['surface_final'] > 20]

    final_count = len(df_clean)
    print(f"\nRésultat : {final_count} annonces valides (sur {initial_count} au départ).")
    
    print("\n--- Top 5 des données propres ---")
    print(df_clean[['quartier', 'surface_final', 'prix_final']].head())

    df_clean.to_csv('data/processed/cleaned_listings.csv', index=False)
    print("\nFichier sauvegardé : data/processed/cleaned_listings.csv")

if __name__ == "__main__":
    run_cleaning()
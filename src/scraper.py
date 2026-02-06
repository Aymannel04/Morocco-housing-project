import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def scrape_pages(max_pages=3):

    print("Démarrage du navigateur...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    all_data = [] 

    for page in range(1, max_pages + 1):
        url = f"https://www.avito.ma/fr/rabat/appartements-%C3%A0_vendre?o={page}"
        
        print(f"\n--- Scraping de la Page {page} ---")
        driver.get(url)
        
        time.sleep(3) 

        try:
            annonces = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[class*='sc-1jge648-0']"))
            )
            print(f"Trouvé {len(annonces)} annonces sur cette page.")

            for annonce in annonces:
                try:
                    lien = annonce.get_attribute('href')
                    texte_complet = annonce.text  
                    
                    try:
                        prix_element = annonce.find_element(By.CSS_SELECTOR, "span[class*='sc-3286ebc5-2']")
                        prix_text = prix_element.text
                    except:
                        prix_text = "0" 

                    all_data.append({
                        'raw_text': texte_complet,
                        'prix_extracted': prix_text,
                        'lien': lien
                    })

                except Exception as e:
                    continue 
            
        except Exception as e:
            print(f"Erreur sur la page {page} : {e}")

        time.sleep(random.uniform(2, 5))

    driver.quit()
    
    print(f"\n Terminé ! {len(all_data)} annonces récupérées.")
    
    df = pd.DataFrame(all_data)
    
    filename = "data/raw/avito_listings.csv"
    
    import os
    os.makedirs('data/raw', exist_ok=True)
    
    df.to_csv(filename, index=False, encoding='utf-8-sig') 
    print(f"Fichier sauvegardé : {filename}")

if __name__ == "__main__":
    scrape_pages(max_pages=5) 
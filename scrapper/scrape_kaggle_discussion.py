import requests
from bs4 import BeautifulSoup
import json
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def extract_kaggle_metadata(text):
    problem_types = ['clasificación', 'regresión', 'clustering', 'nlp', 
                    'computer-vision', 'series temporales', 'reinforcement learning']
    
    metrics_keywords = ['accuracy', 'precisión', 'recall', 'f1', 'mae',
                      'mse', 'rmse', 'auc', 'logloss', 'r2']
    
    data_types = ['imágenes', 'texto', 'csv', 'json', 'sql', 'sensores',
                 'audio', 'video', 'datos tabulares']

    problem_found = list(set([p for p in problem_types if re.search(p, text, re.IGNORECASE)]))
    metrics_found = list(set([m for m in metrics_keywords if re.search(rf'\b{m}\b', text, re.IGNORECASE)]))
    data_found = list(set([d for d in data_types if re.search(d, text, re.IGNORECASE)]))

    return {
        "problem_type": problem_found[0] if problem_found else "no especificado",
        "metrics": metrics_found[:3] if metrics_found else ["no especificado"],
        "required_data": data_found[:2] if data_found else ["no especificado"]
    }

def scrape_kaggle_discussion(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        discussion = {}
        
        # Extraer pregunta principal
        main_question = soup.find('div', class_='km-list__item--question')
        if main_question:
            title = main_question.find('h3').get_text(strip=True)
            content = main_question.find('div', class_='markdown-converter__text').get_text(strip=True)
            
            discussion['input'] = title
            discussion['metadata'] = extract_kaggle_metadata(f"{title} {content}")
        
        # Extraer comentarios
        comments = []
        for comment in soup.find_all('div', class_='km-list__item--comment'):
            user = comment.find('span', class_='kds-username').get_text(strip=True)
            content = comment.find('div', class_='markdown-converter__text').get_text(strip=True)
            votes = comment.find('span', class_='vote-count').get_text(strip=True) if comment.find('span', class_='vote-count') else '0'
            
            comments.append({
                "usuario": user,
                "contenido": content,
                "votos": votes,
                "metadata": extract_kaggle_metadata(content)
            })
        
        discussion['comentarios'] = comments
        time.sleep(3)
        return discussion
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# URL específica de ejemplo
url = "https://www.kaggle.com/discussions/general/231948"
data = scrape_kaggle_discussion(url)

if data:
    with open('kaggle_discusion.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Datos guardados en kaggle_discusion.json")
else:
    print("No se pudo obtener la información")
import pandas as pd
import unicodedata
import json

def normalize_text(text):
    """
    Normalizes text by converting to lowercase, removing accents and non-spacing marks.
    """
    if not isinstance(text, str):
        text = str(text)
    text = text.strip().lower()
    text = unicodedata.normalize('NFD', text)
    return "".join(c for c in text if unicodedata.category(c) != 'Mn')

def process_excel(file_path):
    """
    Processes an Excel file and returns a list of items based on column mapping.
    """
    # Column mapping (0-indexed)
    # ID: 0, Nome: 1, Sobrenome: 2, Departamento: 4, Celular: 7, Email: 8 (Cartão), Informado no Relatorio: 9 (Email)
    df = pd.read_excel(file_path, header=None)

    items = []
    for _, row in df.iterrows():
        try:
            id_val = str(row[0]).strip() if pd.notna(row[0]) else "-"
            nome = str(row[1]).strip() if pd.notna(row[1]) else "-"
            sobrenome = str(row[2]).strip() if pd.notna(row[2]) else "-"
            department = str(row[4]).strip() if pd.notna(row[4]) and str(row[4]).strip() else "Portaria Virtual"
            celular = str(row[7]).strip() if pd.notna(row[7]) else "-"
            cartao = str(row[8]).strip() if pd.notna(row[8]) else "-"
            email = str(row[9]).strip() if pd.notna(row[9]) else "-"

            if id_val == "-" or nome == "-" or sobrenome == "-" or department == "Portaria Virtual" and id_val == "-":
                # Assuming basic validation as in JS
                if id_val == "-" and nome == "-" and sobrenome == "-":
                    continue

            # Search text normalization
            search_text = normalize_text(f"{nome} {sobrenome} {id_val} {email} {celular} {cartao}")

            item = {
                "id": id_val,
                "nome": nome,
                "sobrenome": sobrenome,
                "department": department,
                "celular": celular,
                "cartao": cartao,
                "email": email,
                "search_text": search_text
            }
            items.append(item)
        except Exception:
            continue

    return items

def filter_items(items, search_query="", selected_departments=None):
    """
    Filters items based on search query and selected departments.
    """
    search_query = normalize_text(search_query)
    search_words = search_query.split()

    filtered = []
    for item in items:
        if selected_departments and item['department'] not in selected_departments:
            continue

        if all(word in item['search_text'] for word in search_words):
            filtered.append(item)

    return filtered

if __name__ == "__main__":
    # Example usage
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        data = process_excel(file_path)
        print(f"Processed {len(data)} items.")
        # Example filter
        if len(sys.argv) > 2:
            query = sys.argv[2]
            results = filter_items(data, query)
            print(f"Found {len(results)} matches for '{query}':")
            for r in results[:5]:
                print(f" - {r['nome']} {r['sobrenome']} ({r['department']})")

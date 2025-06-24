import json
from tinydb import TinyDB
from new_app import detect_type

db = TinyDB('templates_db.json', encoding='utf-8')
templates = db.table('_default')

test_data = [
    {"login": "test@example.com", "tel": "+7 123 456 78 90"},  # Полное совпадение с первым шаблоном
    {"customer": "Иван", "дата_заказа": "2025-05-27"},  # Частичное совпадение со вторым шаблоном (2 из 4)
    {"contact": "+7 987 654 32 10"},  # Частичное совпадение (1 из 4)
    {"user_email": "john@example.com", "user_phone": "+7 111 222 33 44"},  # Нет совпадений
]

def find_template(input_fields):
    input_types = {k: detect_type(v) for k, v in input_fields.items()}
    best_match = None
    max_matches = 0
    
    for template in templates.all():
        template_fields = {k: v for k, v in template.items() if k != 'name'}
        matches = sum(
            1 for field, field_type in template_fields.items()
            if field in input_types and input_types[field] == field_type
        )
        
        if matches > max_matches:
            max_matches = matches
            best_match = template['name']
    
    return {"name": best_match} if best_match else input_types

def run_tests():
    for data in test_data:
        print("Input:", json.dumps(data, ensure_ascii=False))
        result = find_template(data)
        print("Result:", json.dumps(result, indent=2, ensure_ascii=False))
        print("-" * 50)

if __name__ == "__main__":
    run_tests()

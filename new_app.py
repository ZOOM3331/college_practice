import sys
import json
import re
from tinydb import TinyDB, Query

db = TinyDB('templates_db.json', encoding='utf-8')
templates = db.table('_default')

def main():
    if len(sys.argv) < 2 or sys.argv[1] != 'get_tpl':
        print("Использование: python app.py get_tpl --поле=значение --поле2=значение2")
        return

    input_fields = {}
    for arg in sys.argv[2:]:
        if arg.startswith('--') and '=' in arg:
            key, val = arg[2:].split('=', 1)
            input_fields[key] = val

    if not input_fields:
        print("Ошибка: поля не указаны")
        return

    input_types = {k: detect_type(v) for k, v in input_fields.items()}
    best_match = None
    max_matches = 0
    
    for template in templates.all():
        template_name = template['name']
        template_fields = {k: v for k, v in template.items() if k != 'name'}
        
        matches = sum(
            1 for field, field_type in template_fields.items()
            if field in input_types and input_types[field] == field_type
        )
        
        if matches == len(template_fields):
            print(json.dumps({"name": template_name}, indent=2, ensure_ascii=False))
            return
        
        if matches > max_matches:
            max_matches = matches
            best_match = template_name

    if best_match and max_matches > 0:
        print(json.dumps({"name": best_match}, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(input_types, indent=2, ensure_ascii=False))

def detect_type(value):
    if not isinstance(value, str):
        return 'text'
    
    if re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
        return 'email'
    
    if re.fullmatch(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value):
        return 'phone'
    
    if (re.fullmatch(r'^\d{2}\.\d{2}\.\d{4}$', value) or 
        re.fullmatch(r'^\d{4}-\d{2}-\d{2}$', value)):
        return 'date'
    
    return 'text'

if __name__ == "__main__":
    main()

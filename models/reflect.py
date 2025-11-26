from sqlalchemy import inspect
from db.connection import engine

def verify_existing_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("Existing tables in database:")
    for table in tables:
        print(f"  - {table}")
        columns = inspector.get_columns(table)
        for col in columns:
            print(f"    • {col['name']}: {col['type']}")
    
    return tables

if __name__ == "__main__":
    existing = verify_existing_tables()
    
    expected = [
        'articles', 'categories', 'tags', 'classifications',
        'article_categories', 'article_tags', 
        'article_references', 'article_classifications'
    ]
    
    missing = set(expected) - set(existing)
    if missing:
        print(f"\nMissing tables: {missing}")
    else:
        print(f"\nAll tables exist!")
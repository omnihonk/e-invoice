"""
Test script to verify model syntax without SQLModel dependencies.
"""

import ast
from pathlib import Path

def check_syntax(file_path):
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse the AST to check syntax
        ast.parse(source)
        print(f"✓ {file_path.name}: Syntax OK")
        return True
    except SyntaxError as e:
        print(f"✗ {file_path.name}: Syntax Error - {e}")
        return False
    except Exception as e:
        print(f"✗ {file_path.name}: Error - {e}")
        return False

def main():
    """Check all model files."""
    models_dir = Path("models")
    
    if not models_dir.exists():
        print("Models directory not found")
        return
    
    model_files = [
        "sqlmodel_base.py",
        "accounting_sqlmodel.py",
    ]
    
    print("Checking model file syntax...")
    print("=" * 50)
    
    all_good = True
    for filename in model_files:
        file_path = models_dir / filename
        if file_path.exists():
            if not check_syntax(file_path):
                all_good = False
        else:
            print(f"✗ {filename}: File not found")
            all_good = False
    
    print("=" * 50)
    if all_good:
        print("✓ All model files have valid syntax!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install sqlmodel pydantic")
        print("2. Test database setup: python database_setup.py")
    else:
        print("✗ Some files have syntax errors. Please fix them first.")

if __name__ == "__main__":
    main()

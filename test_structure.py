#!/usr/bin/env python3
"""
Test script to verify the RAG project structure and dependencies
This can be run without internet access or Ollama
"""
import sys
import os
from pathlib import Path


def test_project_structure():
    """Verify all necessary files exist"""
    print("Testing project structure...")
    
    required_files = [
        "main.py",
        "ingest.py",
        "requirements.txt",
        "README.md",
        "static/index.html"
    ]
    
    all_exist = True
    for file in required_files:
        exists = Path(file).exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {file}")
        if not exists:
            all_exist = False
    
    return all_exist


def test_imports():
    """Test that Python files can be imported without errors"""
    print("\nTesting Python syntax...")
    
    files = ["main.py", "ingest.py"]
    all_valid = True
    
    for file in files:
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print(f"  ✓ {file}")
        except SyntaxError as e:
            print(f"  ✗ {file}: {e}")
            all_valid = False
    
    return all_valid


def test_html():
    """Test that HTML file exists and has required elements"""
    print("\nTesting frontend HTML...")
    
    html_path = "static/index.html"
    if not Path(html_path).exists():
        print(f"  ✗ {html_path} not found")
        return False
    
    with open(html_path, 'r') as f:
        content = f.read()
    
    required_elements = [
        'textarea',
        '/chat',
        'question',
        'answer',
        'onclick'
    ]
    
    all_found = True
    for element in required_elements:
        if element in content:
            print(f"  ✓ Found '{element}'")
        else:
            print(f"  ✗ Missing '{element}'")
            all_found = False
    
    return all_found


def test_requirements():
    """Test that requirements.txt has necessary packages"""
    print("\nTesting requirements.txt...")
    
    with open("requirements.txt", 'r') as f:
        requirements = f.read()
    
    required_packages = [
        'fastapi',
        'chromadb',
        'sentence-transformers',
        'ollama',
        'pypdf2'
    ]
    
    all_found = True
    for package in required_packages:
        if package.lower() in requirements.lower():
            print(f"  ✓ {package}")
        else:
            print(f"  ✗ {package} missing")
            all_found = False
    
    return all_found


def main():
    print("=" * 50)
    print("Mathematical Baymax - Project Validation")
    print("=" * 50)
    print()
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Python Syntax", test_imports),
        ("Frontend HTML", test_html),
        ("Requirements", test_requirements)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nError in {name}: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 50)
    print("Summary")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("✓ All tests passed! Project structure is valid.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Download embedding model (requires internet)")
        print("3. Install and run Ollama with llama2 model")
        print("4. Add PDFs to pdfs/ directory")
        print("5. Run: python ingest.py")
        print("6. Run: python main.py")
        return 0
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
Installation and Setup Verification Script

This script verifies that all dependencies are installed correctly
and the environment is properly configured.
"""

import sys
import os


def check_python_version():
    """Check if Python version is 3.8+."""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  Warning: Python 3.8+ recommended")
        return False
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    dependencies = {
        'openai': 'OpenAI API client',
        'PyPDF2': 'PDF processing',
        'faiss': 'Vector search (FAISS)',
        'numpy': 'Numerical computing'
    }
    
    print("\nChecking dependencies:")
    all_installed = True
    
    for package, description in dependencies.items():
        try:
            if package == 'faiss':
                # FAISS might be installed as faiss-cpu
                try:
                    import faiss
                except ImportError:
                    import faiss_cpu as faiss
            else:
                __import__(package)
            print(f"  ✓ {package:15s} - {description}")
        except ImportError:
            print(f"  ✗ {package:15s} - {description} [MISSING]")
            all_installed = False
    
    return all_installed


def check_optional_dependencies():
    """Check optional dependencies."""
    optional = {
        'dotenv': 'Environment variable management',
        'langchain': 'LangChain framework (optional)'
    }
    
    print("\nOptional dependencies:")
    
    for package, description in optional.items():
        try:
            if package == 'dotenv':
                from dotenv import load_dotenv
            else:
                __import__(package)
            print(f"  ✓ {package:15s} - {description}")
        except ImportError:
            print(f"  ○ {package:15s} - {description} [Not installed]")


def check_environment():
    """Check environment configuration."""
    print("\nEnvironment configuration:")
    
    # Check for .env file
    if os.path.exists('.env'):
        print("  ✓ .env file exists")
    else:
        print("  ○ .env file not found")
        print("    Create one from .env.example")
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        masked_key = api_key[:7] + "..." + api_key[-4:]
        print(f"  ✓ OPENAI_API_KEY set ({masked_key})")
    else:
        print("  ✗ OPENAI_API_KEY not set")
        print("    Set it in .env file or environment")
        return False
    
    return True


def check_modules():
    """Check if project modules can be imported."""
    print("\nProject modules:")
    
    modules = [
        'document_processor',
        'vector_store_manager',
        'doc_qa_agent'
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except Exception as e:
            print(f"  ✗ {module} - {str(e)}")
            all_ok = False
    
    return all_ok


def test_basic_functionality():
    """Test basic agent functionality without loading documents."""
    print("\nBasic functionality test:")
    
    try:
        # This will fail if API key not set, which is expected
        from doc_qa_agent import DocumentQAAgent
        
        try:
            agent = DocumentQAAgent()
            print("  ✓ Agent initialization successful")
            
            # Test basic methods
            status = agent.get_status()
            print("  ✓ Status check works")
            
            help_text = agent.get_help()
            print("  ✓ Help system works")
            
            return True
            
        except ValueError as e:
            if "OPENAI_API_KEY" in str(e):
                print("  ⚠️  Agent initialization requires API key")
                print("     Set OPENAI_API_KEY to test full functionality")
            else:
                print(f"  ✗ Agent initialization failed: {str(e)}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False


def print_summary(results):
    """Print summary of verification results."""
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_critical_passed = all([
        results['python'],
        results['dependencies']
    ])
    
    if all_critical_passed:
        print("✓ All critical checks passed!")
        
        if not results['environment']:
            print("\n⚠️  Action required:")
            print("   1. Copy .env.example to .env")
            print("   2. Add your OPENAI_API_KEY to .env")
            print("   3. Run this script again")
        elif results['modules'] and results['functionality']:
            print("\n🎉 System is fully configured and ready to use!")
            print("\nNext steps:")
            print("   1. Run: python demo.py")
            print("   2. Try: python cli.py")
            print("   3. Load a PDF and ask questions!")
        else:
            print("\n⚠️  Some optional checks failed")
            print("   Review the output above for details")
    else:
        print("✗ Critical checks failed!")
        print("\nPlease install missing dependencies:")
        print("   pip install -r requirements.txt")
    
    print("=" * 60)


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Document Q&A Agent - Installation Verification")
    print("=" * 60)
    
    # Load environment variables if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    results = {
        'python': check_python_version(),
        'dependencies': check_dependencies(),
        'environment': False,
        'modules': False,
        'functionality': False
    }
    
    check_optional_dependencies()
    
    results['environment'] = check_environment()
    
    if results['dependencies']:
        results['modules'] = check_modules()
    
    if results['modules'] and results['environment']:
        results['functionality'] = test_basic_functionality()
    
    print_summary(results)


if __name__ == "__main__":
    main()


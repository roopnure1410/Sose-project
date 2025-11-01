#!/usr/bin/env python3
"""
Test script to verify OpenMusic project setup
This script tests if the basic dependencies and project structure are correctly set up.
"""

import sys
import os
import importlib.util

def test_imports():
    """Test if required packages can be imported"""
    required_packages = [
        'torch',
        'torchvision', 
        'torchaudio',
        'transformers',
        'diffusers',
        'gradio',
        'librosa',
        'soundfile',
        'einops',
        'omegaconf'
    ]
    
    print("Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package}: {e}")
            failed_imports.append(package)
    
    return failed_imports

def test_project_structure():
    """Test if project directories and files exist"""
    print("\nTesting project structure...")
    
    required_paths = [
        'audioldm_train',
        'gradio',
        'infer',
        'audioldm_train/config/mos_as_token/qa_mdt.yaml',
        'offset_pretrained_checkpoints.json',
        'requirements.txt',
        'gradio/requirements.txt',
        'gradio/gradio_app.py'
    ]
    
    missing_paths = []
    
    for path in required_paths:
        if os.path.exists(path):
            print(f"✓ {path}")
        else:
            print(f"✗ {path}")
            missing_paths.append(path)
    
    return missing_paths

def test_torch_cuda():
    """Test CUDA availability"""
    print("\nTesting CUDA availability...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✓ CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"✓ CUDA version: {torch.version.cuda}")
            return True
        else:
            print("⚠ CUDA not available - will use CPU")
            return False
    except Exception as e:
        print(f"✗ Error checking CUDA: {e}")
        return False

def main():
    """Main test function"""
    print("OpenMusic Project Setup Test")
    print("=" * 40)
    
    # Test imports
    failed_imports = test_imports()
    
    # Test project structure
    missing_paths = test_project_structure()
    
    # Test CUDA
    cuda_available = test_torch_cuda()
    
    # Summary
    print("\n" + "=" * 40)
    print("SETUP TEST SUMMARY")
    print("=" * 40)
    
    if not failed_imports:
        print("✓ All required packages imported successfully")
    else:
        print(f"✗ Failed to import: {', '.join(failed_imports)}")
    
    if not missing_paths:
        print("✓ All required project files found")
    else:
        print(f"✗ Missing files: {', '.join(missing_paths)}")
    
    if cuda_available:
        print("✓ CUDA is available for GPU acceleration")
    else:
        print("⚠ CUDA not available - will use CPU (slower)")
    
    # Overall status
    if not failed_imports and not missing_paths:
        print("\n🎉 Project setup is ready!")
        print("You can now proceed to download model checkpoints and run the demo.")
    else:
        print("\n⚠ Setup incomplete - please address the issues above.")
    
    return len(failed_imports) == 0 and len(missing_paths) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
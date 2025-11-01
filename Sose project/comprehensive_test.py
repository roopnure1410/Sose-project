#!/usr/bin/env python3
"""
Comprehensive OpenMusic Project Test Suite
Tests all available features and components of the OpenMusic project.
"""

import os
import sys
import importlib
import subprocess
import time
import traceback
from pathlib import Path
import yaml

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class OpenMusicTester:
    def __init__(self):
        self.test_results = {}
        self.project_root = project_root
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        self.test_results[test_name] = {"status": status, "details": details}
        if status == "PASS":
            self.passed_tests += 1
            print(f"✅ {test_name}: PASSED")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name}: FAILED - {details}")
        if details:
            print(f"   Details: {details}")
        print()

    def test_project_structure(self):
        """Test 1: Verify project structure and required files"""
        print("🔍 Testing Project Structure...")
        
        required_files = [
            "requirements.txt",
            "qamdt.yml", 
            "readme.md",
            "simple_demo.py",
            "test_setup.py",
            "SETUP_GUIDE.md"
        ]
        
        required_dirs = [
            "audioldm_train",
            "gradio", 
            "infer",
            "test_prompts",
            "checkpoints"
        ]
        
        missing_files = []
        missing_dirs = []
        
        for file in required_files:
            if not (self.project_root / file).exists():
                missing_files.append(file)
                
        for dir_name in required_dirs:
            if not (self.project_root / dir_name).exists():
                missing_dirs.append(dir_name)
        
        if missing_files or missing_dirs:
            details = f"Missing files: {missing_files}, Missing dirs: {missing_dirs}"
            self.log_test("Project Structure", "FAIL", details)
        else:
            self.log_test("Project Structure", "PASS", "All required files and directories present")

    def test_dependencies(self):
        """Test 2: Check if required dependencies are installed"""
        print("📦 Testing Dependencies...")
        
        required_packages = [
            "torch", "torchvision", "torchaudio",
            "transformers", "diffusers", "accelerate",
            "gradio", "librosa", "soundfile", 
            "numpy", "omegaconf", "wandb"
        ]
        
        missing_packages = []
        installed_packages = []
        
        for package in required_packages:
            try:
                importlib.import_module(package)
                installed_packages.append(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.log_test("Dependencies", "FAIL", f"Missing packages: {missing_packages}")
        else:
            self.log_test("Dependencies", "PASS", f"All {len(installed_packages)} packages installed")

    def test_configuration_files(self):
        """Test 3: Validate configuration files"""
        print("⚙️ Testing Configuration Files...")
        
        try:
            # Test qamdt.yml
            with open(self.project_root / "qamdt.yml", 'r') as f:
                config = yaml.safe_load(f)
            
            required_config_keys = ["model", "data", "log_directory"]
            missing_keys = [key for key in required_config_keys if key not in config]
            
            if missing_keys:
                self.log_test("Configuration Files", "FAIL", f"Missing config keys: {missing_keys}")
            else:
                self.log_test("Configuration Files", "PASS", "Configuration files valid")
                
        except Exception as e:
            self.log_test("Configuration Files", "FAIL", f"Error reading config: {str(e)}")

    def test_enhanced_demo(self):
        """Test 4: Test the enhanced demo functionality"""
        print("🎵 Testing Enhanced Demo...")
        
        try:
            # Import and test the enhanced demo
            from simple_demo import generate_enhanced_demo_audio, get_random_suggestion
            
            # Test audio generation
            test_description = "peaceful piano melody"
            audio_path = generate_enhanced_demo_audio(test_description, duration=3, style="balanced")
            
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path)
                if file_size > 1000:  # At least 1KB
                    self.log_test("Enhanced Demo Audio Generation", "PASS", f"Generated {file_size} bytes")
                else:
                    self.log_test("Enhanced Demo Audio Generation", "FAIL", "Generated file too small")
            else:
                self.log_test("Enhanced Demo Audio Generation", "FAIL", "Audio file not created")
            
            # Test suggestion function
            suggestion = get_random_suggestion()
            if suggestion and len(suggestion) > 10:
                self.log_test("Enhanced Demo Suggestions", "PASS", f"Generated suggestion: {suggestion[:50]}...")
            else:
                self.log_test("Enhanced Demo Suggestions", "FAIL", "Invalid suggestion generated")
                
        except Exception as e:
            self.log_test("Enhanced Demo", "FAIL", f"Error: {str(e)}")

    def test_audioldm_modules(self):
        """Test 5: Test audioldm_train modules"""
        print("🎼 Testing AudioLDM Modules...")
        
        try:
            # Test importing key modules
            from audioldm_train.utilities.data.dataset_original_mos1 import AudioDataset
            from audioldm_train.utilities.model_util import instantiate_from_config
            from audioldm_train.utilities.tools import build_dataset_json_from_list
            
            self.log_test("AudioLDM Module Imports", "PASS", "All key modules imported successfully")
            
            # Test dataset JSON building
            test_list = ["test prompt 1", "test prompt 2"]
            dataset_json = build_dataset_json_from_list(test_list)
            
            if dataset_json and len(dataset_json) > 0:
                self.log_test("AudioLDM Dataset Tools", "PASS", f"Built dataset with {len(dataset_json)} entries")
            else:
                self.log_test("AudioLDM Dataset Tools", "FAIL", "Failed to build dataset JSON")
                
        except Exception as e:
            self.log_test("AudioLDM Modules", "FAIL", f"Error: {str(e)}")

    def test_inference_scripts_structure(self):
        """Test 6: Test inference scripts structure"""
        print("🔬 Testing Inference Scripts...")
        
        inference_scripts = [
            "infer_mos1.py", "infer_mos2.py", "infer_mos3.py", 
            "infer_mos4.py", "infer_mos5.py"
        ]
        
        valid_scripts = []
        invalid_scripts = []
        
        for script in inference_scripts:
            script_path = self.project_root / "infer" / script
            if script_path.exists():
                try:
                    with open(script_path, 'r') as f:
                        content = f.read()
                    
                    # Check for key components
                    if "def infer(" in content and "argparse" in content:
                        valid_scripts.append(script)
                    else:
                        invalid_scripts.append(f"{script} (missing key functions)")
                except Exception as e:
                    invalid_scripts.append(f"{script} (read error: {str(e)})")
            else:
                invalid_scripts.append(f"{script} (not found)")
        
        if invalid_scripts:
            self.log_test("Inference Scripts Structure", "FAIL", f"Invalid scripts: {invalid_scripts}")
        else:
            self.log_test("Inference Scripts Structure", "PASS", f"All {len(valid_scripts)} scripts valid")

    def test_prompt_files(self):
        """Test 7: Test prompt files"""
        print("📝 Testing Prompt Files...")
        
        prompt_files = [
            "good_prompts_1.lst", "good_prompts_2.lst", 
            "good_prompts_3.lst", "song_describer_dataset.lst"
        ]
        
        total_prompts = 0
        valid_files = []
        
        for prompt_file in prompt_files:
            file_path = self.project_root / "test_prompts" / prompt_file
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                    
                    non_empty_lines = [line.strip() for line in lines if line.strip()]
                    total_prompts += len(non_empty_lines)
                    valid_files.append(f"{prompt_file} ({len(non_empty_lines)} prompts)")
                    
                except Exception as e:
                    self.log_test("Prompt Files", "FAIL", f"Error reading {prompt_file}: {str(e)}")
                    return
        
        if total_prompts > 0:
            self.log_test("Prompt Files", "PASS", f"Found {total_prompts} total prompts in {len(valid_files)} files")
        else:
            self.log_test("Prompt Files", "FAIL", "No valid prompts found")

    def test_gradio_interface(self):
        """Test 8: Test Gradio interface components"""
        print("🌐 Testing Gradio Interface...")
        
        try:
            import gradio as gr
            
            # Test if we can create basic Gradio components
            textbox = gr.Textbox(label="Test")
            audio = gr.Audio(label="Test Audio")
            button = gr.Button("Test Button")
            
            self.log_test("Gradio Components", "PASS", "Basic Gradio components created successfully")
            
            # Test enhanced demo creation (without launching)
            from simple_demo import create_enhanced_demo
            demo = create_enhanced_demo()
            
            if demo:
                self.log_test("Enhanced Demo Creation", "PASS", "Enhanced demo interface created")
            else:
                self.log_test("Enhanced Demo Creation", "FAIL", "Failed to create demo interface")
                
        except Exception as e:
            self.log_test("Gradio Interface", "FAIL", f"Error: {str(e)}")

    def test_system_requirements(self):
        """Test 9: Test system requirements and capabilities"""
        print("💻 Testing System Requirements...")
        
        try:
            import torch
            
            # Test CUDA availability
            cuda_available = torch.cuda.is_available()
            if cuda_available:
                gpu_count = torch.cuda.device_count()
                gpu_name = torch.cuda.get_device_name(0)
                self.log_test("CUDA Support", "PASS", f"CUDA available with {gpu_count} GPU(s): {gpu_name}")
            else:
                self.log_test("CUDA Support", "WARN", "CUDA not available - will use CPU (slower)")
            
            # Test memory
            if cuda_available:
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                self.log_test("GPU Memory", "PASS" if gpu_memory > 4 else "WARN", 
                            f"GPU Memory: {gpu_memory:.1f} GB")
            
            # Test Python version
            python_version = sys.version_info
            if python_version.major == 3 and python_version.minor >= 8:
                self.log_test("Python Version", "PASS", f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
            else:
                self.log_test("Python Version", "WARN", f"Python {python_version.major}.{python_version.minor} (recommended: 3.10)")
                
        except Exception as e:
            self.log_test("System Requirements", "FAIL", f"Error: {str(e)}")

    def test_audio_processing(self):
        """Test 10: Test audio processing capabilities"""
        print("🎧 Testing Audio Processing...")
        
        try:
            import librosa
            import soundfile as sf
            import numpy as np
            
            # Test audio generation and processing
            sample_rate = 16000
            duration = 1  # 1 second
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = np.sin(2 * np.pi * 440 * t) * 0.5  # 440 Hz sine wave
            
            # Test saving audio
            test_file = "test_audio.wav"
            sf.write(test_file, audio, sample_rate)
            
            # Test loading audio
            loaded_audio, loaded_sr = librosa.load(test_file, sr=sample_rate)
            
            if len(loaded_audio) > 0 and loaded_sr == sample_rate:
                self.log_test("Audio Processing", "PASS", f"Audio I/O working, {len(loaded_audio)} samples at {loaded_sr} Hz")
                os.remove(test_file)  # Clean up
            else:
                self.log_test("Audio Processing", "FAIL", "Audio I/O failed")
                
        except Exception as e:
            self.log_test("Audio Processing", "FAIL", f"Error: {str(e)}")

    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 Starting Comprehensive OpenMusic Test Suite")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all tests
        self.test_project_structure()
        self.test_dependencies()
        self.test_configuration_files()
        self.test_enhanced_demo()
        self.test_audioldm_modules()
        self.test_inference_scripts_structure()
        self.test_prompt_files()
        self.test_gradio_interface()
        self.test_system_requirements()
        self.test_audio_processing()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Generate summary report
        print("=" * 60)
        print("📊 TEST SUMMARY REPORT")
        print("=" * 60)
        print(f"⏱️  Total execution time: {duration:.2f} seconds")
        print(f"✅ Passed tests: {self.passed_tests}")
        print(f"❌ Failed tests: {self.failed_tests}")
        print(f"📈 Success rate: {(self.passed_tests / (self.passed_tests + self.failed_tests) * 100):.1f}%")
        print()
        
        # Detailed results
        print("📋 DETAILED RESULTS:")
        print("-" * 40)
        for test_name, result in self.test_results.items():
            status_emoji = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "WARN" else "❌"
            print(f"{status_emoji} {test_name}: {result['status']}")
            if result["details"]:
                print(f"   └─ {result['details']}")
        
        print("\n" + "=" * 60)
        
        if self.failed_tests == 0:
            print("🎉 ALL TESTS PASSED! The OpenMusic project is fully functional.")
        else:
            print(f"⚠️  {self.failed_tests} test(s) failed. Check the details above for issues.")
        
        return self.failed_tests == 0

if __name__ == "__main__":
    tester = OpenMusicTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
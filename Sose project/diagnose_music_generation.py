#!/usr/bin/env python3
"""
Diagnostic script to identify and fix music generation issues
"""

import numpy as np
import soundfile as sf
import os
import traceback
from pathlib import Path

def test_basic_generation():
    """Test basic music generation without advanced features"""
    print("🔍 Testing basic music generation...")
    
    try:
        # Generate simple sine wave
        duration = 3
        sample_rate = 44100
        frequency = 440  # A4 note
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = np.sin(2 * np.pi * frequency * t) * 0.3
        
        # Save test file
        test_file = "basic_test.wav"
        sf.write(test_file, audio, sample_rate)
        
        if os.path.exists(test_file):
            print("✅ Basic audio generation works")
            os.remove(test_file)
            return True
        else:
            print("❌ Basic audio generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Basic generation error: {e}")
        return False

def test_advanced_generator():
    """Test the advanced music generator"""
    print("🔍 Testing advanced music generator...")
    
    try:
        from advanced_music_generator import AdvancedMusicGenerator, MusicStyle
        
        generator = AdvancedMusicGenerator(sample_rate=44100)
        print("✅ Advanced generator imported successfully")
        
        # Test composition generation
        audio = generator.generate_composition("simple test melody", duration=3)
        
        if len(audio) > 0 and np.max(np.abs(audio)) > 0:
            print("✅ Advanced generator produces audio")
            
            # Save test file
            test_file = "advanced_test.wav"
            sf.write(test_file, audio, generator.sample_rate)
            print(f"✅ Test file saved: {test_file}")
            return True
        else:
            print("❌ Advanced generator produces empty/silent audio")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Advanced generator error: {e}")
        traceback.print_exc()
        return False

def test_demo_function():
    """Test the demo function directly"""
    print("🔍 Testing demo function...")
    
    try:
        from simple_demo import generate_enhanced_demo_audio
        
        output_path = generate_enhanced_demo_audio("test melody", duration=3, style="classical")
        
        if os.path.exists(output_path):
            print(f"✅ Demo function works: {output_path}")
            
            # Check file size
            file_size = os.path.getsize(output_path)
            print(f"📁 File size: {file_size} bytes")
            
            if file_size > 1000:  # Should be larger than 1KB for 3 seconds
                print("✅ Generated file has reasonable size")
                return True
            else:
                print("❌ Generated file is too small")
                return False
        else:
            print("❌ Demo function failed to create file")
            return False
            
    except Exception as e:
        print(f"❌ Demo function error: {e}")
        traceback.print_exc()
        return False

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    dependencies = [
        ('numpy', 'np'),
        ('soundfile', 'sf'),
        ('gradio', 'gr'),
    ]
    
    all_good = True
    for dep_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {dep_name} available")
        except ImportError:
            print(f"❌ {dep_name} missing")
            all_good = False
    
    return all_good

def fix_common_issues():
    """Attempt to fix common issues"""
    print("🔧 Attempting to fix common issues...")
    
    # Check if output directory exists
    if not os.path.exists("generated_music_demos"):
        os.makedirs("generated_music_demos")
        print("✅ Created generated_music_demos directory")
    
    # Clean up old demo files
    demo_files = [f for f in os.listdir(".") if f.startswith("demo_output_")]
    if demo_files:
        print(f"🧹 Cleaning up {len(demo_files)} old demo files")
        for file in demo_files:
            try:
                os.remove(file)
            except:
                pass
    
    print("✅ Common issues check complete")

def main():
    """Main diagnostic function"""
    print("🎵 MUSIC GENERATION DIAGNOSTIC")
    print("=" * 40)
    
    # Run diagnostics
    results = {}
    
    results['dependencies'] = check_dependencies()
    results['basic'] = test_basic_generation()
    results['advanced'] = test_advanced_generator()
    results['demo'] = test_demo_function()
    
    # Fix common issues
    fix_common_issues()
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 DIAGNOSTIC RESULTS")
    print("=" * 40)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper()}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! Music generation should work.")
        print("🌐 Try the demo at: http://localhost:7860")
    else:
        print("\n⚠️  Some tests failed. Issues identified:")
        
        if not results['dependencies']:
            print("- Missing dependencies - run: pip install -r requirements.txt")
        if not results['basic']:
            print("- Basic audio generation failed - check numpy/soundfile")
        if not results['advanced']:
            print("- Advanced generator failed - check advanced_music_generator.py")
        if not results['demo']:
            print("- Demo function failed - check simple_demo.py")
    
    return all_passed

if __name__ == "__main__":
    main()
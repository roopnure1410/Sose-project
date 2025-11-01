#!/usr/bin/env python3
"""
Comprehensive debugging script to identify music generation issues
"""

import sys
import os
import traceback
import tempfile
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all required imports"""
    print("🔍 TESTING IMPORTS")
    print("=" * 40)
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except Exception as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import soundfile as sf
        print("✅ soundfile imported successfully")
    except Exception as e:
        print(f"❌ soundfile import failed: {e}")
        return False
    
    try:
        import gradio as gr
        print("✅ gradio imported successfully")
    except Exception as e:
        print(f"❌ gradio import failed: {e}")
        return False
    
    try:
        from advanced_music_generator import AdvancedMusicGenerator, MusicStyle
        print("✅ AdvancedMusicGenerator imported successfully")
    except Exception as e:
        print(f"❌ AdvancedMusicGenerator import failed: {e}")
        return False
    
    return True

def test_music_generator():
    """Test the music generator directly"""
    print("\n🎵 TESTING MUSIC GENERATOR")
    print("=" * 40)
    
    try:
        from advanced_music_generator import AdvancedMusicGenerator, MusicStyle
        
        # Initialize generator
        generator = AdvancedMusicGenerator()
        print("✅ Generator initialized")
        
        # Test generation
        description = "peaceful piano melody"
        duration = 3
        style = MusicStyle.CLASSICAL
        
        print(f"🎼 Generating: '{description}' ({style.value}, {duration}s)")
        
        audio_data = generator.generate_music(description, duration, style)
        
        if audio_data is not None and len(audio_data) > 0:
            print(f"✅ Audio generated: {len(audio_data)} samples")
            print(f"📊 Max amplitude: {abs(audio_data).max():.3f}")
            return True
        else:
            print("❌ No audio data generated")
            return False
            
    except Exception as e:
        print(f"❌ Generator test failed: {e}")
        traceback.print_exc()
        return False

def test_demo_function():
    """Test the demo generation function"""
    print("\n🎧 TESTING DEMO FUNCTION")
    print("=" * 40)
    
    try:
        from simple_demo import generate_enhanced_demo_audio
        
        description = "peaceful piano melody"
        duration = 3
        style = "classical"
        
        print(f"🎼 Testing demo function: '{description}' ({style}, {duration}s)")
        
        output_path = generate_enhanced_demo_audio(description, duration, style)
        
        if output_path and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Demo audio generated: {output_path}")
            print(f"📊 File size: {file_size} bytes")
            
            # Try to read the audio
            import soundfile as sf
            audio_data, sample_rate = sf.read(output_path)
            duration_actual = len(audio_data) / sample_rate
            print(f"📊 Duration: {duration_actual:.2f}s")
            print(f"📊 Sample rate: {sample_rate}Hz")
            
            # Clean up
            os.remove(output_path)
            return True
        else:
            print(f"❌ Demo function failed to generate file: {output_path}")
            return False
            
    except Exception as e:
        print(f"❌ Demo function test failed: {e}")
        traceback.print_exc()
        return False

def test_gradio_function():
    """Test the Gradio interface function directly"""
    print("\n🌐 TESTING GRADIO FUNCTION")
    print("=" * 40)
    
    try:
        # Import the demo module
        import simple_demo
        
        # Get the demo object
        demo = simple_demo.create_enhanced_demo()
        
        # Find the generate function
        if hasattr(demo, 'fns') and demo.fns:
            print("✅ Gradio demo created successfully")
            print(f"📊 Number of functions: {len(demo.fns)}")
            
            # Try to find the generation function
            for i, fn in enumerate(demo.fns):
                if fn and hasattr(fn, 'fn'):
                    print(f"📋 Function {i}: {fn.fn.__name__ if hasattr(fn.fn, '__name__') else 'unknown'}")
            
            return True
        else:
            print("❌ No functions found in Gradio demo")
            return False
            
    except Exception as e:
        print(f"❌ Gradio function test failed: {e}")
        traceback.print_exc()
        return False

def test_file_permissions():
    """Test file creation permissions"""
    print("\n📁 TESTING FILE PERMISSIONS")
    print("=" * 40)
    
    try:
        # Test creating a temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(b'test data')
        
        if os.path.exists(tmp_path):
            print(f"✅ Can create temporary files: {tmp_path}")
            os.remove(tmp_path)
            return True
        else:
            print("❌ Cannot create temporary files")
            return False
            
    except Exception as e:
        print(f"❌ File permission test failed: {e}")
        return False

def test_gradio_interface_live():
    """Test if the Gradio interface is responding"""
    print("\n🔗 TESTING LIVE GRADIO INTERFACE")
    print("=" * 40)
    
    try:
        import requests
        
        response = requests.get("http://localhost:7860", timeout=5)
        if response.status_code == 200:
            print("✅ Gradio interface is accessible")
            print(f"📊 Response size: {len(response.content)} bytes")
            
            # Check if it contains expected elements
            content = response.text.lower()
            if 'generate music' in content:
                print("✅ Generate button found in interface")
            else:
                print("⚠️ Generate button not found in interface")
            
            return True
        else:
            print(f"❌ Interface returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Live interface test failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("🔧 COMPREHENSIVE MUSIC GENERATION DIAGNOSTICS")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Music Generator", test_music_generator),
        ("Demo Function", test_demo_function),
        ("Gradio Function", test_gradio_function),
        ("File Permissions", test_file_permissions),
        ("Live Interface", test_gradio_interface_live)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 30)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Music generation should be working.")
        print("💡 If you're still having issues, try:")
        print("   1. Refresh the browser page")
        print("   2. Clear browser cache")
        print("   3. Try a different browser")
        print("   4. Check browser console for JavaScript errors")
    else:
        print("\n⚠️ Some tests failed. This explains why music generation isn't working.")
        print("💡 Please check the failed tests above for specific issues.")

if __name__ == "__main__":
    main()
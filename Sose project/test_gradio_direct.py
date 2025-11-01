#!/usr/bin/env python3
"""
Direct test of Gradio interface functions to diagnose web interface issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_demo import generate_enhanced_demo_audio
from simple_working_demo import generate_music_simple

def test_gradio_functions():
    """Test both Gradio interface functions directly"""
    
    print("🧪 Testing Gradio Interface Functions...")
    print("=" * 50)
    
    # Test 1: Enhanced demo function
    print("\n1. Testing Enhanced Demo Function:")
    try:
        result = generate_enhanced_demo_audio(
            description="peaceful piano melody",
            duration=3,
            style="classical"
        )
        print(f"   ✅ Enhanced demo: {result}")
        if os.path.exists(result):
            print(f"   📁 File exists: {os.path.getsize(result)} bytes")
        else:
            print(f"   ❌ File not found: {result}")
    except Exception as e:
        print(f"   ❌ Enhanced demo error: {e}")
    
    # Test 2: Simple demo function
    print("\n2. Testing Simple Demo Function:")
    try:
        audio_path, status = generate_music_simple(
            description="peaceful piano melody",
            duration=3,
            style="classical"
        )
        print(f"   ✅ Simple demo: {audio_path}")
        print(f"   📝 Status: {status}")
        if audio_path and os.path.exists(audio_path):
            print(f"   📁 File exists: {os.path.getsize(audio_path)} bytes")
        else:
            print(f"   ❌ File not found: {audio_path}")
    except Exception as e:
        print(f"   ❌ Simple demo error: {e}")
    
    # Test 3: Check for common issues
    print("\n3. Checking Common Issues:")
    
    # Check if soundfile can write properly
    try:
        import soundfile as sf
        import numpy as np
        test_audio = np.random.random(44100) * 0.1  # 1 second of quiet noise
        test_path = "test_soundfile.wav"
        sf.write(test_path, test_audio, 44100)
        if os.path.exists(test_path):
            print("   ✅ SoundFile write test: OK")
            os.remove(test_path)
        else:
            print("   ❌ SoundFile write test: Failed")
    except Exception as e:
        print(f"   ❌ SoundFile error: {e}")
    
    # Check file permissions
    try:
        test_file = "permission_test.txt"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("   ✅ File permissions: OK")
    except Exception as e:
        print(f"   ❌ File permission error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Diagnosis Complete!")
    print("\n💡 If functions work but web interface doesn't:")
    print("   1. Try refreshing the browser")
    print("   2. Check browser console for errors (F12)")
    print("   3. Try a different browser")
    print("   4. Check if antivirus is blocking audio files")
    print("   5. Try downloading the generated file directly")

if __name__ == "__main__":
    test_gradio_functions()
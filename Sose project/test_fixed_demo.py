#!/usr/bin/env python3
"""
Quick test to verify the fixed demo music generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_demo import generate_enhanced_demo_audio
import soundfile as sf

def test_fixed_generation():
    """Test that the fixed demo can generate music"""
    print("🎵 TESTING FIXED DEMO GENERATION")
    print("=" * 40)
    
    test_cases = [
        ("peaceful piano melody", 5, "classical"),
        ("upbeat electronic dance", 5, "electronic"),
        ("jazz saxophone solo", 5, "jazz")
    ]
    
    for description, duration, style in test_cases:
        print(f"\n🎼 Testing: '{description}' ({style}, {duration}s)")
        
        try:
            # Generate audio
            output_path = generate_enhanced_demo_audio(description, duration, style)
            
            # Verify the file exists and has content
            if os.path.exists(output_path):
                audio_data, sample_rate = sf.read(output_path)
                duration_actual = len(audio_data) / sample_rate
                max_amplitude = abs(audio_data).max()
                
                print(f"✅ Generated: {output_path}")
                print(f"📊 Duration: {duration_actual:.2f}s")
                print(f"📊 Sample rate: {sample_rate}Hz")
                print(f"📊 Max amplitude: {max_amplitude:.3f}")
                print(f"✅ {style} generation successful!")
                
                # Clean up test file
                os.remove(output_path)
            else:
                print(f"❌ File not generated: {output_path}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎉 Fixed demo test completed!")

if __name__ == "__main__":
    test_fixed_generation()
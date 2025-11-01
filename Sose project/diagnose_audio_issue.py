#!/usr/bin/env python3
"""
Diagnose Audio Generation Issues
Quick test to verify audio generation and file saving works properly.
"""

import numpy as np
import soundfile as sf
import os
from advanced_music_generator import AdvancedMusicGenerator, MusicStyle

def test_audio_generation():
    """Test complete audio generation pipeline"""
    print("🔍 Diagnosing Audio Generation...")
    
    try:
        # Initialize generator
        print("1. Initializing music generator...")
        generator = AdvancedMusicGenerator()
        print("   ✅ Generator initialized successfully")
        
        # Test basic generation
        print("2. Testing basic audio generation...")
        description = "peaceful piano melody"
        duration = 3
        audio_data = generator.generate_composition(description, duration)
        print(f"   ✅ Generated {len(audio_data)} samples ({len(audio_data)/generator.sample_rate:.2f}s)")
        print(f"   📊 Audio range: {np.min(audio_data):.3f} to {np.max(audio_data):.3f}")
        
        # Test file saving
        print("3. Testing file saving...")
        output_file = "audio_test_output.wav"
        sf.write(output_file, audio_data, generator.sample_rate)
        print(f"   ✅ Audio saved to: {output_file}")
        
        # Verify file exists and has content
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"   📁 File size: {file_size:,} bytes")
            
            # Test reading back
            read_audio, read_sr = sf.read(output_file)
            print(f"   🔄 Read back: {len(read_audio)} samples at {read_sr}Hz")
            print("   ✅ File read/write successful")
        else:
            print("   ❌ File was not created")
            return False
        
        # Test different styles
        print("4. Testing different musical styles...")
        styles_to_test = [MusicStyle.CLASSICAL, MusicStyle.JAZZ, MusicStyle.ELECTRONIC]
        
        for style in styles_to_test:
            try:
                test_audio = generator.generate_composition(f"test {style.value} music", 2, style)
                print(f"   ✅ {style.value.capitalize()}: {len(test_audio)} samples")
            except Exception as e:
                print(f"   ❌ {style.value.capitalize()}: {e}")
                return False
        
        # Test Gradio interface function
        print("5. Testing Gradio interface function...")
        try:
            # Import the function used by Gradio
            import simple_demo
            if hasattr(simple_demo, 'generate_music'):
                result = simple_demo.generate_music("test melody", 2, "classical")
                if result and len(result) == 2:  # Should return (sample_rate, audio_data)
                    sr, audio = result
                    print(f"   ✅ Gradio function: {len(audio)} samples at {sr}Hz")
                else:
                    print(f"   ⚠️  Gradio function returned unexpected format: {type(result)}")
            else:
                print("   ⚠️  Gradio function not found in simple_demo")
        except Exception as e:
            print(f"   ❌ Gradio function test failed: {e}")
        
        print("\n🎉 Audio generation diagnosis completed successfully!")
        print(f"🎵 Test file created: {output_file}")
        print("\n💡 If you still can't hear audio in the browser:")
        print("   1. Check browser audio settings")
        print("   2. Try a different browser")
        print("   3. Check system volume")
        print("   4. Try downloading the generated audio file")
        
        return True
        
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_audio_generation()
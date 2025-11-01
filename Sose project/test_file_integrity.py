#!/usr/bin/env python3
"""
Simple file integrity test for audio generation
"""

import os
import numpy as np
import soundfile as sf
from advanced_music_generator import AdvancedMusicGenerator, MusicStyle

def test_file_integrity():
    """Test basic file I/O operations"""
    print("🔧 Testing File Integrity")
    print("=" * 40)
    
    generator = AdvancedMusicGenerator()
    
    try:
        # Generate a simple audio sample
        print("1. Generating audio...")
        audio_data = generator.generate_composition(
            description="simple test tone",
            duration=2,
            style=MusicStyle.CLASSICAL
        )
        
        if audio_data is None or len(audio_data) == 0:
            print("❌ No audio data generated")
            return False
            
        print(f"✅ Generated {len(audio_data):,} samples")
        print(f"   Sample rate: {generator.sample_rate}")
        print(f"   Duration: {len(audio_data)/generator.sample_rate:.2f}s")
        print(f"   Data type: {audio_data.dtype}")
        print(f"   Shape: {audio_data.shape}")
        print(f"   Min/Max: {np.min(audio_data):.3f}/{np.max(audio_data):.3f}")
        
        # Test file writing
        output_file = "test_integrity.wav"
        print(f"\n2. Writing to file: {output_file}")
        
        try:
            sf.write(output_file, audio_data, generator.sample_rate)
            print("✅ File written successfully")
            
            # Check file exists and size
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✅ File exists, size: {file_size:,} bytes")
            else:
                print("❌ File does not exist after writing")
                return False
                
        except Exception as e:
            print(f"❌ Error writing file: {e}")
            return False
        
        # Test file reading
        print(f"\n3. Reading back from file...")
        try:
            read_audio, read_sr = sf.read(output_file)
            print(f"✅ File read successfully")
            print(f"   Read {len(read_audio):,} samples")
            print(f"   Sample rate: {read_sr}")
            print(f"   Data type: {read_audio.dtype}")
            print(f"   Shape: {read_audio.shape}")
            print(f"   Min/Max: {np.min(read_audio):.3f}/{np.max(read_audio):.3f}")
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False
        
        # Compare data
        print(f"\n4. Comparing data...")
        
        # Check basic properties
        if len(read_audio) != len(audio_data):
            print(f"❌ Length mismatch: {len(read_audio)} vs {len(audio_data)}")
            return False
        
        if read_sr != generator.sample_rate:
            print(f"❌ Sample rate mismatch: {read_sr} vs {generator.sample_rate}")
            return False
        
        # Check data similarity (allowing for small floating point differences)
        max_diff = np.max(np.abs(read_audio - audio_data))
        print(f"   Max difference: {max_diff:.6f}")
        
        if max_diff > 1e-4:  # More lenient threshold
            print(f"❌ Data differs too much: {max_diff}")
            print(f"   Original range: [{np.min(audio_data):.6f}, {np.max(audio_data):.6f}]")
            print(f"   Read range: [{np.min(read_audio):.6f}, {np.max(read_audio):.6f}]")
            
            # Show first few samples for debugging
            print("   First 10 samples comparison:")
            for i in range(min(10, len(audio_data))):
                print(f"     [{i}] Original: {audio_data[i]:.6f}, Read: {read_audio[i]:.6f}, Diff: {abs(audio_data[i] - read_audio[i]):.6f}")
            
            return False
        
        print("✅ Data matches within tolerance")
        
        # Clean up
        print(f"\n5. Cleaning up...")
        try:
            os.remove(output_file)
            print("✅ Test file removed")
        except Exception as e:
            print(f"⚠️  Could not remove test file: {e}")
        
        print("\n✅ File integrity test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_file_integrity()
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")
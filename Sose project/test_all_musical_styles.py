#!/usr/bin/env python3
"""
Comprehensive test for all 8 musical styles in OpenMusic
Tests each style with different descriptions and durations
"""

import os
import sys
import time
from advanced_music_generator import AdvancedMusicGenerator, MusicStyle

def test_all_musical_styles():
    """Test all 8 musical styles with various parameters"""
    print("🎵 Testing All Musical Styles in OpenMusic")
    print("=" * 60)
    
    # Initialize the generator
    generator = AdvancedMusicGenerator()
    
    # Define test cases for each style
    test_cases = [
        {
            "style": MusicStyle.CLASSICAL,
            "description": "peaceful piano melody with strings",
            "duration": 5,
            "expected": "classical composition"
        },
        {
            "style": MusicStyle.JAZZ,
            "description": "smooth saxophone with walking bass",
            "duration": 6,
            "expected": "jazz improvisation"
        },
        {
            "style": MusicStyle.ELECTRONIC,
            "description": "upbeat electronic dance music",
            "duration": 4,
            "expected": "electronic beats"
        },
        {
            "style": MusicStyle.ROCK,
            "description": "energetic guitar riffs with drums",
            "duration": 7,
            "expected": "rock composition"
        },
        {
            "style": MusicStyle.FOLK,
            "description": "acoustic guitar with gentle vocals",
            "duration": 5,
            "expected": "folk melody"
        },
        {
            "style": MusicStyle.WORLD,
            "description": "traditional instruments with ethnic rhythms",
            "duration": 6,
            "expected": "world music"
        },
        {
            "style": MusicStyle.AMBIENT,
            "description": "atmospheric soundscape with soft pads",
            "duration": 8,
            "expected": "ambient atmosphere"
        },
        {
            "style": MusicStyle.EXPERIMENTAL,
            "description": "unconventional sounds and structures",
            "duration": 5,
            "expected": "experimental composition"
        }
    ]
    
    results = []
    total_tests = len(test_cases)
    passed_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        style = test_case["style"]
        description = test_case["description"]
        duration = test_case["duration"]
        
        print(f"\n🎼 Test {i}/{total_tests}: {style.value.upper()}")
        print(f"   Description: {description}")
        print(f"   Duration: {duration}s")
        
        try:
            # Generate music
            start_time = time.time()
            audio_data = generator.generate_composition(
                description=description,
                duration=duration,
                style=style
            )
            generation_time = time.time() - start_time
            
            # Verify audio data
            if audio_data is not None and len(audio_data) > 0:
                # Calculate audio properties
                sample_rate = 44100  # Default sample rate
                expected_samples = duration * sample_rate
                actual_samples = len(audio_data)
                duration_actual = actual_samples / sample_rate
                
                print(f"   ✅ SUCCESS: Generated {actual_samples:,} samples")
                print(f"   ⏱️  Generation time: {generation_time:.2f}s")
                print(f"   🎵 Audio duration: {duration_actual:.2f}s")
                print(f"   📊 Sample rate: {sample_rate}Hz")
                
                # Save test file
                output_file = f"test_style_{style.value}_{int(time.time())}.wav"
                try:
                    import soundfile as sf
                    sf.write(output_file, audio_data, sample_rate)
                    file_size = os.path.getsize(output_file)
                    print(f"   💾 Saved: {output_file} ({file_size:,} bytes)")
                    
                    # Clean up test file
                    os.remove(output_file)
                    print(f"   🗑️  Cleaned up test file")
                except Exception as e:
                    print(f"   ⚠️  File save/cleanup warning: {e}")
                
                results.append({
                    "style": style.value,
                    "status": "PASSED",
                    "duration": duration_actual,
                    "samples": actual_samples,
                    "generation_time": generation_time
                })
                passed_tests += 1
                
            else:
                print(f"   ❌ FAILED: No audio data generated")
                results.append({
                    "style": style.value,
                    "status": "FAILED",
                    "error": "No audio data"
                })
                
        except Exception as e:
            print(f"   ❌ FAILED: {str(e)}")
            results.append({
                "style": style.value,
                "status": "FAILED",
                "error": str(e)
            })
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 MUSICAL STYLES TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n📋 DETAILED RESULTS:")
    print("-" * 40)
    for result in results:
        status_icon = "✅" if result["status"] == "PASSED" else "❌"
        print(f"{status_icon} {result['style'].upper()}: {result['status']}")
        if result["status"] == "PASSED":
            print(f"   Duration: {result['duration']:.2f}s")
            print(f"   Samples: {result['samples']:,}")
            print(f"   Gen Time: {result['generation_time']:.2f}s")
        else:
            print(f"   Error: {result.get('error', 'Unknown')}")
    
    print("\n🎵 All musical styles tested!")
    return passed_tests == total_tests

if __name__ == "__main__":
    success = test_all_musical_styles()
    sys.exit(0 if success else 1)
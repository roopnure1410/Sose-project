#!/usr/bin/env python3
"""
Test different duration settings for OpenMusic generation
Tests various time lengths from 3-10 seconds to ensure consistent quality
"""

import os
import sys
import time
import numpy as np
from advanced_music_generator import AdvancedMusicGenerator, MusicStyle

def test_duration_settings():
    """Test music generation with different duration settings"""
    print("⏱️ Testing Different Duration Settings")
    print("=" * 60)
    
    # Initialize the generator
    generator = AdvancedMusicGenerator()
    
    # Test different durations
    test_durations = [3, 4, 5, 6, 7, 8, 9, 10]
    test_description = "peaceful piano melody with gentle strings"
    test_style = MusicStyle.CLASSICAL
    
    results = []
    total_tests = len(test_durations)
    passed_tests = 0
    
    for i, duration in enumerate(test_durations, 1):
        print(f"\n⏱️ Test {i}/{total_tests}: {duration} seconds")
        print(f"   Description: {test_description}")
        print(f"   Style: {test_style.value}")
        
        try:
            # Generate music
            start_time = time.time()
            audio_data = generator.generate_composition(
                description=test_description,
                duration=duration,
                style=test_style
            )
            generation_time = time.time() - start_time
            
            # Verify audio data
            if audio_data is not None and len(audio_data) > 0:
                # Calculate audio properties
                sample_rate = 44100  # Default sample rate
                expected_samples = duration * sample_rate
                actual_samples = len(audio_data)
                duration_actual = actual_samples / sample_rate
                duration_error = abs(duration_actual - duration)
                
                # Check if duration is within acceptable range (±0.1 seconds)
                duration_ok = duration_error <= 0.1
                
                # Check audio quality
                max_amplitude = np.max(np.abs(audio_data))
                has_content = max_amplitude > 0.01  # Should have audible content
                not_clipping = max_amplitude <= 1.0  # Should not clip
                
                print(f"   ✅ SUCCESS: Generated {actual_samples:,} samples")
                print(f"   ⏱️  Generation time: {generation_time:.2f}s")
                print(f"   🎵 Expected duration: {duration:.2f}s")
                print(f"   🎵 Actual duration: {duration_actual:.2f}s")
                print(f"   📏 Duration error: {duration_error:.3f}s")
                print(f"   📊 Max amplitude: {max_amplitude:.3f}")
                print(f"   ✅ Duration accuracy: {'PASS' if duration_ok else 'FAIL'}")
                print(f"   ✅ Audio content: {'PASS' if has_content else 'FAIL'}")
                print(f"   ✅ No clipping: {'PASS' if not_clipping else 'FAIL'}")
                
                # Save test file
                output_file = f"test_duration_{duration}s_{int(time.time())}.wav"
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
                
                # Overall test result
                test_passed = duration_ok and has_content and not_clipping
                
                results.append({
                    "duration_requested": duration,
                    "duration_actual": duration_actual,
                    "duration_error": duration_error,
                    "max_amplitude": max_amplitude,
                    "generation_time": generation_time,
                    "samples": actual_samples,
                    "status": "PASSED" if test_passed else "FAILED",
                    "duration_ok": duration_ok,
                    "has_content": has_content,
                    "no_clipping": not_clipping
                })
                
                if test_passed:
                    passed_tests += 1
                
            else:
                print(f"   ❌ FAILED: No audio data generated")
                results.append({
                    "duration_requested": duration,
                    "status": "FAILED",
                    "error": "No audio data"
                })
                
        except Exception as e:
            print(f"   ❌ FAILED: {str(e)}")
            results.append({
                "duration_requested": duration,
                "status": "FAILED",
                "error": str(e)
            })
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 DURATION SETTINGS TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    # Calculate statistics
    successful_results = [r for r in results if r["status"] == "PASSED"]
    if successful_results:
        avg_generation_time = np.mean([r["generation_time"] for r in successful_results])
        avg_duration_error = np.mean([r["duration_error"] for r in successful_results])
        max_duration_error = np.max([r["duration_error"] for r in successful_results])
        avg_amplitude = np.mean([r["max_amplitude"] for r in successful_results])
        
        print(f"\n📈 PERFORMANCE STATISTICS:")
        print(f"   Average generation time: {avg_generation_time:.2f}s")
        print(f"   Average duration error: {avg_duration_error:.3f}s")
        print(f"   Maximum duration error: {max_duration_error:.3f}s")
        print(f"   Average max amplitude: {avg_amplitude:.3f}")
    
    print("\n📋 DETAILED RESULTS:")
    print("-" * 60)
    for result in results:
        status_icon = "✅" if result["status"] == "PASSED" else "❌"
        duration_req = result["duration_requested"]
        print(f"{status_icon} {duration_req}s: {result['status']}")
        
        if result["status"] == "PASSED":
            duration_act = result["duration_actual"]
            error = result["duration_error"]
            gen_time = result["generation_time"]
            amplitude = result["max_amplitude"]
            print(f"   Actual: {duration_act:.2f}s | Error: {error:.3f}s | Gen: {gen_time:.2f}s | Amp: {amplitude:.3f}")
            
            # Quality indicators
            quality_indicators = []
            if result["duration_ok"]:
                quality_indicators.append("✅ Duration")
            else:
                quality_indicators.append("❌ Duration")
            if result["has_content"]:
                quality_indicators.append("✅ Content")
            else:
                quality_indicators.append("❌ Content")
            if result["no_clipping"]:
                quality_indicators.append("✅ No Clip")
            else:
                quality_indicators.append("❌ Clipping")
            
            print(f"   Quality: {' | '.join(quality_indicators)}")
        else:
            print(f"   Error: {result.get('error', 'Unknown')}")
    
    print("\n⏱️ Duration settings tested!")
    return passed_tests == total_tests

if __name__ == "__main__":
    success = test_duration_settings()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
Audio Quality Verification Test for OpenMusic
Tests audio generation quality, file integrity, and audio characteristics
"""

import os
import sys
import time
import numpy as np
import soundfile as sf
from advanced_music_generator import AdvancedMusicGenerator, MusicStyle

def analyze_audio_quality(audio_data, sample_rate=44100):
    """Analyze audio quality metrics"""
    if len(audio_data) == 0:
        return None
    
    # Basic metrics
    duration = len(audio_data) / sample_rate
    max_amplitude = np.max(np.abs(audio_data))
    rms_amplitude = np.sqrt(np.mean(audio_data**2))
    
    # Dynamic range
    dynamic_range = max_amplitude / (rms_amplitude + 1e-10)
    
    # Check for silence
    silence_threshold = 0.001
    is_silent = max_amplitude < silence_threshold
    
    # Check for clipping
    clipping_threshold = 0.99
    is_clipping = max_amplitude > clipping_threshold
    
    # Frequency content analysis (basic)
    fft = np.fft.fft(audio_data[:min(len(audio_data), sample_rate)])  # First second
    magnitude = np.abs(fft)
    freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
    
    # Find dominant frequency
    positive_freqs = freqs[:len(freqs)//2]
    positive_magnitude = magnitude[:len(magnitude)//2]
    dominant_freq_idx = np.argmax(positive_magnitude)
    dominant_freq = positive_freqs[dominant_freq_idx]
    
    # Check frequency distribution
    low_freq_energy = np.sum(positive_magnitude[positive_freqs < 500])
    mid_freq_energy = np.sum(positive_magnitude[(positive_freqs >= 500) & (positive_freqs < 4000)])
    high_freq_energy = np.sum(positive_magnitude[positive_freqs >= 4000])
    total_energy = low_freq_energy + mid_freq_energy + high_freq_energy
    
    freq_distribution = {
        'low': low_freq_energy / (total_energy + 1e-10),
        'mid': mid_freq_energy / (total_energy + 1e-10),
        'high': high_freq_energy / (total_energy + 1e-10)
    }
    
    return {
        'duration': duration,
        'max_amplitude': max_amplitude,
        'rms_amplitude': rms_amplitude,
        'dynamic_range': dynamic_range,
        'is_silent': is_silent,
        'is_clipping': is_clipping,
        'dominant_freq': dominant_freq,
        'freq_distribution': freq_distribution,
        'sample_count': len(audio_data)
    }

def test_audio_quality():
    """Test audio generation quality across different scenarios"""
    print("🎧 Testing Audio Quality and File Generation")
    print("=" * 60)
    
    # Initialize the generator
    generator = AdvancedMusicGenerator()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Classical Piano",
            "description": "peaceful piano melody with gentle dynamics",
            "style": MusicStyle.CLASSICAL,
            "duration": 5,
            "expected_freq_range": (200, 2000)  # Piano frequency range
        },
        {
            "name": "Jazz Saxophone",
            "description": "smooth jazz saxophone with walking bass",
            "style": MusicStyle.JAZZ,
            "duration": 6,
            "expected_freq_range": (100, 1500)  # Sax + bass range
        },
        {
            "name": "Electronic Synth",
            "description": "bright electronic synthesizer with bass",
            "style": MusicStyle.ELECTRONIC,
            "duration": 4,
            "expected_freq_range": (50, 8000)  # Wide electronic range
        },
        {
            "name": "Ambient Atmosphere",
            "description": "atmospheric ambient soundscape with pads",
            "style": MusicStyle.AMBIENT,
            "duration": 8,
            "expected_freq_range": (50, 4000)  # Ambient frequency range
        }
    ]
    
    results = []
    total_tests = len(test_scenarios)
    passed_tests = 0
    
    for i, scenario in enumerate(test_scenarios, 1):
        name = scenario["name"]
        description = scenario["description"]
        style = scenario["style"]
        duration = scenario["duration"]
        
        print(f"\n🎼 Test {i}/{total_tests}: {name}")
        print(f"   Description: {description}")
        print(f"   Style: {style.value}")
        print(f"   Duration: {duration}s")
        
        try:
            # Generate audio
            start_time = time.time()
            audio_data = generator.generate_composition(
                description=description,
                duration=duration,
                style=style
            )
            generation_time = time.time() - start_time
            
            if audio_data is not None and len(audio_data) > 0:
                # Analyze audio quality
                quality_metrics = analyze_audio_quality(audio_data)
                
                # Quality checks
                checks = {
                    'has_content': not quality_metrics['is_silent'],
                    'no_clipping': not quality_metrics['is_clipping'],
                    'proper_duration': abs(quality_metrics['duration'] - duration) <= 0.1,
                    'good_dynamic_range': quality_metrics['dynamic_range'] > 1.5,
                    'balanced_frequency': (
                        quality_metrics['freq_distribution']['low'] > 0.02 and
                        quality_metrics['freq_distribution']['mid'] > 0.3
                    )
                }
                
                # Test file generation and integrity
                output_file = f"quality_test_{name.lower().replace(' ', '_')}_{int(time.time())}.wav"
                try:
                    sf.write(output_file, audio_data, generator.sample_rate)
                    file_size = os.path.getsize(output_file)
                    
                    # Verify file can be read back
                    read_audio, read_sr = sf.read(output_file)
                    file_integrity = (
                        len(read_audio) == len(audio_data) and
                        read_sr == generator.sample_rate and
                        np.allclose(read_audio, audio_data, rtol=1e-4, atol=1e-4)
                    )
                    
                    # Clean up
                    os.remove(output_file)
                    
                    checks['file_integrity'] = file_integrity
                    
                except Exception as e:
                    print(f"   ⚠️  File I/O error: {e}")
                    checks['file_integrity'] = False
                
                # Print results
                print(f"   ✅ Generated: {quality_metrics['sample_count']:,} samples")
                print(f"   ⏱️  Generation time: {generation_time:.2f}s")
                print(f"   🎵 Duration: {quality_metrics['duration']:.2f}s")
                print(f"   📊 Max amplitude: {quality_metrics['max_amplitude']:.3f}")
                print(f"   📊 RMS amplitude: {quality_metrics['rms_amplitude']:.3f}")
                print(f"   📊 Dynamic range: {quality_metrics['dynamic_range']:.1f}")
                print(f"   🎵 Dominant freq: {quality_metrics['dominant_freq']:.1f} Hz")
                
                # Frequency distribution
                freq_dist = quality_metrics['freq_distribution']
                print(f"   🎵 Freq distribution: Low:{freq_dist['low']:.2f} Mid:{freq_dist['mid']:.2f} High:{freq_dist['high']:.2f}")
                
                # Quality checks
                print(f"   ✅ Quality Checks:")
                for check_name, check_result in checks.items():
                    status = "PASS" if check_result else "FAIL"
                    icon = "✅" if check_result else "❌"
                    print(f"      {icon} {check_name.replace('_', ' ').title()}: {status}")
                
                # Overall result
                all_checks_passed = all(checks.values())
                test_status = "PASSED" if all_checks_passed else "FAILED"
                
                results.append({
                    "name": name,
                    "status": test_status,
                    "generation_time": generation_time,
                    "quality_metrics": quality_metrics,
                    "checks": checks,
                    "all_checks_passed": all_checks_passed
                })
                
                if all_checks_passed:
                    passed_tests += 1
                    print(f"   ✅ Overall: {test_status}")
                else:
                    print(f"   ❌ Overall: {test_status}")
                
            else:
                print(f"   ❌ FAILED: No audio data generated")
                results.append({
                    "name": name,
                    "status": "FAILED",
                    "error": "No audio data"
                })
                
        except Exception as e:
            print(f"   ❌ FAILED: {str(e)}")
            results.append({
                "name": name,
                "status": "FAILED",
                "error": str(e)
            })
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 AUDIO QUALITY TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    # Performance statistics
    successful_results = [r for r in results if r["status"] == "PASSED"]
    if successful_results:
        avg_generation_time = np.mean([r["generation_time"] for r in successful_results])
        print(f"\n📈 PERFORMANCE:")
        print(f"   Average generation time: {avg_generation_time:.2f}s")
    
    print("\n📋 DETAILED RESULTS:")
    print("-" * 40)
    for result in results:
        status_icon = "✅" if result["status"] == "PASSED" else "❌"
        print(f"{status_icon} {result['name']}: {result['status']}")
        
        if result["status"] == "PASSED":
            checks = result["checks"]
            failed_checks = [name for name, passed in checks.items() if not passed]
            if failed_checks:
                print(f"   Failed checks: {', '.join(failed_checks)}")
            else:
                print(f"   All quality checks passed")
        else:
            print(f"   Error: {result.get('error', 'Unknown')}")
    
    print("\n🎧 Audio quality verification completed!")
    return passed_tests == total_tests

if __name__ == "__main__":
    success = test_audio_quality()
    sys.exit(0 if success else 1)
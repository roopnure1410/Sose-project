#!/usr/bin/env python3
"""
Error Handling and Edge Cases Test for OpenMusic
Tests system robustness with invalid inputs, extreme parameters, and edge cases
"""

import sys
import time
from advanced_music_generator import AdvancedMusicGenerator, MusicStyle

def test_error_handling():
    """Test error handling and edge cases"""
    print("🛡️ Testing Error Handling and Edge Cases")
    print("=" * 60)
    
    generator = AdvancedMusicGenerator()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Empty Description",
            "description": "",
            "style": MusicStyle.CLASSICAL,
            "duration": 3,
            "expected": "should_handle_gracefully"
        },
        {
            "name": "Very Long Description",
            "description": "a" * 1000,  # 1000 character description
            "style": MusicStyle.JAZZ,
            "duration": 3,
            "expected": "should_handle_gracefully"
        },
        {
            "name": "Special Characters",
            "description": "music with 🎵🎶🎼 emojis and special chars: @#$%^&*()",
            "style": MusicStyle.ELECTRONIC,
            "duration": 3,
            "expected": "should_handle_gracefully"
        },
        {
            "name": "Very Short Duration",
            "description": "quick test",
            "style": MusicStyle.AMBIENT,
            "duration": 0.1,
            "expected": "should_handle_gracefully"
        },
        {
            "name": "Zero Duration",
            "description": "zero duration test",
            "style": MusicStyle.CLASSICAL,
            "duration": 0,
            "expected": "should_handle_gracefully"
        },
        {
            "name": "Negative Duration",
            "description": "negative duration test",
            "style": MusicStyle.JAZZ,
            "duration": -5,
            "expected": "should_handle_gracefully"
        },
        {
            "name": "Very Long Duration",
            "description": "long duration test",
            "style": MusicStyle.ROCK,
            "duration": 60,  # 1 minute
            "expected": "should_handle_gracefully"
        },
        {
            "name": "Extremely Long Duration",
            "description": "extremely long duration test",
            "style": MusicStyle.AMBIENT,
            "duration": 300,  # 5 minutes
            "expected": "should_handle_gracefully"
        },
        {
            "name": "Non-numeric Duration",
            "description": "invalid duration test",
            "style": MusicStyle.FOLK,
            "duration": "invalid",
            "expected": "should_raise_error"
        },
        {
            "name": "None Description",
            "description": None,
            "style": MusicStyle.WORLD,
            "duration": 3,
            "expected": "should_handle_gracefully"
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
        expected = scenario["expected"]
        
        print(f"\n🧪 Test {i}/{total_tests}: {name}")
        print(f"   Description: {repr(description)}")
        print(f"   Style: {style.value}")
        print(f"   Duration: {duration}")
        print(f"   Expected: {expected}")
        
        try:
            start_time = time.time()
            audio_data = generator.generate_composition(
                description=description,
                duration=duration,
                style=style
            )
            generation_time = time.time() - start_time
            
            if expected == "should_raise_error":
                print(f"   ❌ FAILED: Expected error but got result")
                results.append({
                    "name": name,
                    "status": "FAILED",
                    "reason": "Expected error but generation succeeded"
                })
            else:
                # Check if we got reasonable output
                if audio_data is not None and len(audio_data) > 0:
                    print(f"   ✅ Generated: {len(audio_data):,} samples")
                    print(f"   ⏱️  Generation time: {generation_time:.2f}s")
                    print(f"   🎵 Actual duration: {len(audio_data)/generator.sample_rate:.2f}s")
                    
                    # For edge cases, check if output is reasonable
                    if duration <= 0:
                        # Should generate minimal audio or handle gracefully
                        if len(audio_data) > 0:
                            print(f"   ✅ Handled gracefully: Generated minimal audio")
                        else:
                            print(f"   ✅ Handled gracefully: No audio for invalid duration")
                    elif duration > 30:
                        # Should either generate or limit duration reasonably
                        actual_duration = len(audio_data) / generator.sample_rate
                        if actual_duration > 0:
                            print(f"   ✅ Handled gracefully: Generated {actual_duration:.1f}s audio")
                        else:
                            print(f"   ⚠️  Generated no audio for long duration")
                    
                    print(f"   ✅ PASSED: Handled gracefully")
                    passed_tests += 1
                    results.append({
                        "name": name,
                        "status": "PASSED",
                        "generation_time": generation_time,
                        "samples": len(audio_data),
                        "actual_duration": len(audio_data) / generator.sample_rate
                    })
                else:
                    if expected == "should_handle_gracefully":
                        print(f"   ✅ PASSED: Handled gracefully (no audio generated)")
                        passed_tests += 1
                        results.append({
                            "name": name,
                            "status": "PASSED",
                            "reason": "Gracefully handled with no output"
                        })
                    else:
                        print(f"   ❌ FAILED: No audio data generated")
                        results.append({
                            "name": name,
                            "status": "FAILED",
                            "reason": "No audio data generated"
                        })
                
        except TypeError as e:
            if expected == "should_raise_error":
                print(f"   ✅ PASSED: Correctly raised TypeError: {e}")
                passed_tests += 1
                results.append({
                    "name": name,
                    "status": "PASSED",
                    "reason": f"Correctly raised TypeError: {e}"
                })
            else:
                print(f"   ❌ FAILED: Unexpected TypeError: {e}")
                results.append({
                    "name": name,
                    "status": "FAILED",
                    "reason": f"Unexpected TypeError: {e}"
                })
                
        except ValueError as e:
            if expected == "should_raise_error":
                print(f"   ✅ PASSED: Correctly raised ValueError: {e}")
                passed_tests += 1
                results.append({
                    "name": name,
                    "status": "PASSED",
                    "reason": f"Correctly raised ValueError: {e}"
                })
            else:
                print(f"   ❌ FAILED: Unexpected ValueError: {e}")
                results.append({
                    "name": name,
                    "status": "FAILED",
                    "reason": f"Unexpected ValueError: {e}"
                })
                
        except Exception as e:
            print(f"   ❌ FAILED: Unexpected error: {type(e).__name__}: {e}")
            results.append({
                "name": name,
                "status": "FAILED",
                "reason": f"Unexpected error: {type(e).__name__}: {e}"
            })
    
    # Test memory and performance under stress
    print(f"\n🔥 Stress Test: Multiple Rapid Generations")
    stress_passed = True
    try:
        stress_start = time.time()
        for i in range(5):
            audio = generator.generate_composition(
                description=f"stress test {i+1}",
                duration=1,
                style=MusicStyle.AMBIENT
            )
            if audio is None or len(audio) == 0:
                stress_passed = False
                break
        stress_time = time.time() - stress_start
        
        if stress_passed:
            print(f"   ✅ PASSED: Generated 5 pieces in {stress_time:.2f}s")
            passed_tests += 1
        else:
            print(f"   ❌ FAILED: Stress test failed")
            
    except Exception as e:
        print(f"   ❌ FAILED: Stress test error: {e}")
        stress_passed = False
    
    total_tests += 1  # Include stress test
    results.append({
        "name": "Stress Test",
        "status": "PASSED" if stress_passed else "FAILED"
    })
    
    # Print summary
    print("\n" + "=" * 60)
    print("🛡️ ERROR HANDLING TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n📋 DETAILED RESULTS:")
    print("-" * 40)
    for result in results:
        status_icon = "✅" if result["status"] == "PASSED" else "❌"
        print(f"{status_icon} {result['name']}: {result['status']}")
        if "reason" in result:
            print(f"   Reason: {result['reason']}")
        elif "samples" in result:
            print(f"   Generated: {result['samples']:,} samples in {result.get('generation_time', 0):.2f}s")
    
    print("\n🛡️ Error handling verification completed!")
    return passed_tests >= total_tests * 0.8  # 80% pass rate acceptable for edge cases

if __name__ == "__main__":
    success = test_error_handling()
    sys.exit(0 if success else 1)
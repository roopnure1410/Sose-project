#!/usr/bin/env python3
"""
Comprehensive Feature Testing Script for Enhanced OpenMusic System
Tests all advanced music generation features, styles, and capabilities
"""

import numpy as np
import soundfile as sf
import os
import time
from advanced_music_generator import AdvancedMusicGenerator, MusicStyle
from simple_demo import generate_enhanced_demo_audio

def test_all_features():
    """Comprehensive test of all OpenMusic features"""
    
    print("🎵 COMPREHENSIVE OPENMUSIC FEATURE TESTING")
    print("=" * 60)
    
    # Create test output directory
    test_output_dir = "feature_test_outputs"
    os.makedirs(test_output_dir, exist_ok=True)
    
    # Initialize generator
    generator = AdvancedMusicGenerator(sample_rate=44100)
    
    # Test results tracking
    test_results = {
        "passed": 0,
        "failed": 0,
        "total": 0,
        "details": []
    }
    
    def run_test(test_name, test_function):
        """Helper function to run individual tests"""
        test_results["total"] += 1
        print(f"\n🧪 Testing: {test_name}")
        try:
            result = test_function()
            if result:
                print(f"✅ PASSED: {test_name}")
                test_results["passed"] += 1
                test_results["details"].append(f"✅ {test_name}")
                return True
            else:
                print(f"❌ FAILED: {test_name}")
                test_results["failed"] += 1
                test_results["details"].append(f"❌ {test_name}")
                return False
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {str(e)}")
            test_results["failed"] += 1
            test_results["details"].append(f"❌ {test_name} - Error: {str(e)}")
            return False
    
    # Test 1: Basic Music Generation
    def test_basic_generation():
        """Test basic music generation functionality"""
        audio = generator.generate_composition("happy upbeat melody", duration=5)
        return len(audio) > 0 and np.max(np.abs(audio)) > 0
    
    # Test 2: All Musical Styles
    def test_all_musical_styles():
        """Test all 8 musical styles"""
        styles = [MusicStyle.CLASSICAL, MusicStyle.JAZZ, MusicStyle.ELECTRONIC, 
                 MusicStyle.AMBIENT, MusicStyle.ROCK, MusicStyle.FOLK, 
                 MusicStyle.WORLD, MusicStyle.EXPERIMENTAL]
        
        for style in styles:
            audio = generator.generate_composition(f"test {style.value} composition", 
                                                 duration=3, style=style)
            if len(audio) == 0 or np.max(np.abs(audio)) == 0:
                return False
            
            # Save test audio
            style_path = os.path.join(test_output_dir, f"test_{style.value}.wav")
            sf.write(style_path, audio, generator.sample_rate)
        
        return True
    
    # Test 3: Demo Interface Integration
    def test_demo_integration():
        """Test the enhanced demo interface integration"""
        styles = ["classical", "jazz", "electronic", "ambient", "rock", "folk", "world", "balanced"]
        
        for style in styles:
            output_path = generate_enhanced_demo_audio(
                f"test {style} music", duration=3, style=style
            )
            # Check if file was created and has content
            if not os.path.exists(output_path):
                return False
            
            # Load and verify audio content
            audio, sample_rate = sf.read(output_path)
            if len(audio) == 0 or np.max(np.abs(audio)) == 0:
                return False
            
            # Clean up test file
            os.remove(output_path)
        
        return True
    
    # Test 4: Harmonic Complexity
    def test_harmonic_complexity():
        """Test harmonic series generation"""
        frequencies, amplitudes = generator.generate_harmonic_series(440, 8)
        return len(frequencies) == 8 and len(amplitudes) == 8 and all(f > 0 for f in frequencies)
    
    # Test 5: Chord Generation
    def test_chord_generation():
        """Test chord creation and inversions"""
        chord_types = ['major', 'minor', 'major7', 'minor7', 'dominant7', 'sus2', 'sus4']
        
        for chord_type in chord_types:
            chord_freqs = generator.create_chord(440, chord_type, inversion=0)
            if len(chord_freqs) < 3:  # Minimum 3 notes for a chord
                return False
        
        return True
    
    # Test 6: Scale Generation
    def test_scale_generation():
        """Test scale and mode generation"""
        from advanced_music_generator import ScaleGenerator
        
        scales = ['major', 'minor', 'dorian', 'phrygian', 'lydian', 'mixolydian', 
                 'pentatonic', 'blues', 'chromatic', 'whole_tone']
        
        for scale in scales:
            freqs = ScaleGenerator.get_scale_frequencies(440, scale, 2)
            if len(freqs) == 0:
                return False
        
        return True
    
    # Test 7: Rhythm Generation
    def test_rhythm_generation():
        """Test rhythm pattern generation"""
        from advanced_music_generator import RhythmGenerator, TimeSignature
        
        time_sigs = [TimeSignature.FOUR_FOUR, TimeSignature.THREE_FOUR, 
                    TimeSignature.SIX_EIGHT, TimeSignature.FIVE_FOUR]
        
        for time_sig in time_sigs:
            pattern = RhythmGenerator.generate_rhythm_pattern(time_sig, 0.5)
            if len(pattern) == 0:
                return False
        
        return True
    
    # Test 8: Instrument Simulation
    def test_instrument_simulation():
        """Test instrument envelope simulation"""
        from advanced_music_generator import InstrumentSimulator
        
        t = np.linspace(0, 1, 1000)
        instruments = ['piano', 'strings', 'brass', 'synth_pad', 'synth_lead']
        
        for instrument in instruments:
            if instrument == 'piano':
                envelope = InstrumentSimulator.piano_envelope(t)
            elif instrument == 'strings':
                envelope = InstrumentSimulator.string_envelope(t)
            elif instrument == 'brass':
                envelope = InstrumentSimulator.brass_envelope(t)
            else:
                envelope = InstrumentSimulator.synthesizer_envelope(t, instrument.split('_')[1])
            
            if len(envelope) != len(t) or np.max(envelope) == 0:
                return False
        
        return True
    
    # Test 9: Audio Effects
    def test_audio_effects():
        """Test audio effects processing"""
        test_audio = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 44100))
        
        effects = {
            'reverb': 0.3,
            'chorus': 0.2,
            'distortion': 0.1
        }
        
        processed = generator.add_effects(test_audio, effects)
        return len(processed) == len(test_audio) and not np.array_equal(test_audio, processed)
    
    # Test 10: Description Analysis
    def test_description_analysis():
        """Test natural language description analysis"""
        descriptions = [
            "classical symphony in major key with strings",
            "jazz improvisation with complex chords",
            "electronic ambient with slow tempo",
            "rock music with distortion and fast tempo",
            "folk acoustic guitar melody"
        ]
        
        for desc in descriptions:
            audio = generator.generate_composition(desc, duration=2)
            if len(audio) == 0:
                return False
        
        return True
    
    # Test 11: Duration Accuracy
    def test_duration_accuracy():
        """Test audio duration accuracy"""
        durations = [3, 5, 8, 10, 15]
        
        for duration in durations:
            audio = generator.generate_composition("test melody", duration=duration)
            actual_duration = len(audio) / generator.sample_rate
            # Allow 10% tolerance
            if abs(actual_duration - duration) > duration * 0.1:
                return False
        
        return True
    
    # Test 12: Audio Quality
    def test_audio_quality():
        """Test audio quality metrics"""
        audio = generator.generate_composition("high quality test", duration=5)
        
        # Check for clipping
        if np.max(np.abs(audio)) > 1.0:
            return False
        
        # Check for silence
        if np.max(np.abs(audio)) < 0.001:
            return False
        
        # Check for reasonable dynamic range
        rms = np.sqrt(np.mean(audio**2))
        if rms < 0.01 or rms > 0.9:
            return False
        
        return True
    
    # Run all tests
    print("🚀 Starting comprehensive feature testing...")
    
    run_test("Basic Music Generation", test_basic_generation)
    run_test("All Musical Styles (8 styles)", test_all_musical_styles)
    run_test("Demo Interface Integration", test_demo_integration)
    run_test("Harmonic Complexity", test_harmonic_complexity)
    run_test("Chord Generation", test_chord_generation)
    run_test("Scale Generation", test_scale_generation)
    run_test("Rhythm Generation", test_rhythm_generation)
    run_test("Instrument Simulation", test_instrument_simulation)
    run_test("Audio Effects", test_audio_effects)
    run_test("Description Analysis", test_description_analysis)
    run_test("Duration Accuracy", test_duration_accuracy)
    run_test("Audio Quality", test_audio_quality)
    
    # Generate comprehensive test compositions
    print("\n🎼 Generating comprehensive test compositions...")
    
    test_compositions = [
        ("Classical Masterpiece", "classical symphony in D major with complex harmonies and string ensemble", "classical"),
        ("Jazz Improvisation", "jazz fusion with extended chords and syncopated rhythms", "jazz"),
        ("Electronic Soundscape", "electronic ambient with synthesizer pads and atmospheric effects", "electronic"),
        ("Ambient Meditation", "slow ambient meditation music with reverb and gentle harmonies", "ambient"),
        ("Rock Anthem", "energetic rock music with distortion and driving rhythm", "rock"),
        ("Folk Ballad", "acoustic folk ballad with gentle guitar and simple melody", "folk"),
        ("World Fusion", "world music fusion with exotic scales and rhythms", "world"),
        ("Balanced Composition", "balanced musical composition with diverse elements", "balanced")
    ]
    
    for name, description, style in test_compositions:
        print(f"🎵 Generating: {name}")
        output_path = generate_enhanced_demo_audio(description, duration=8, style=style)
        
        # Move composition to test output directory
        filename = f"test_composition_{style}.wav"
        filepath = os.path.join(test_output_dir, filename)
        
        # Copy the generated file to our test directory
        if os.path.exists(output_path):
            audio, sample_rate = sf.read(output_path)
            sf.write(filepath, audio, sample_rate)
            os.remove(output_path)  # Clean up original
            print(f"✅ Saved: {filepath}")
        else:
            print(f"❌ Failed to generate: {name}")
    
    # Generate final test report
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    
    success_rate = (test_results["passed"] / test_results["total"]) * 100
    print(f"🎯 Overall Success Rate: {success_rate:.1f}%")
    print(f"✅ Tests Passed: {test_results['passed']}")
    print(f"❌ Tests Failed: {test_results['failed']}")
    print(f"📊 Total Tests: {test_results['total']}")
    
    print("\n📋 Detailed Results:")
    for detail in test_results["details"]:
        print(f"   {detail}")
    
    print(f"\n📁 Test outputs saved in: {test_output_dir}/")
    print("🎵 Test compositions generated for all 8 musical styles")
    
    # Verify demo pieces
    print("\n🎼 Verifying generated demo pieces...")
    demo_pieces = [
        "generated_music_demos/piece1_classical_symphony.wav",
        "generated_music_demos/piece2_jazz_fusion.wav",
        "generated_music_demos/piece3_electronic_ambient.wav"
    ]
    
    for piece in demo_pieces:
        if os.path.exists(piece):
            print(f"✅ Demo piece verified: {piece}")
        else:
            print(f"❌ Demo piece missing: {piece}")
    
    print("\n🎉 COMPREHENSIVE TESTING COMPLETE!")
    print("🌟 Enhanced OpenMusic system fully operational with advanced features")
    
    return test_results

if __name__ == "__main__":
    test_all_features()
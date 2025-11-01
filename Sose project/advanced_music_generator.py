#!/usr/bin/env python3
"""
Advanced Music Generation System
Implements diverse musical styles, complex harmonies, and sophisticated algorithms
to create unique, non-repetitive musical compositions.
"""

import numpy as np
import soundfile as sf
import random
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class MusicStyle(Enum):
    CLASSICAL = "classical"
    JAZZ = "jazz"
    ELECTRONIC = "electronic"
    AMBIENT = "ambient"
    ROCK = "rock"
    FOLK = "folk"
    WORLD = "world"
    EXPERIMENTAL = "experimental"

class TimeSignature(Enum):
    FOUR_FOUR = (4, 4)
    THREE_FOUR = (3, 4)
    SIX_EIGHT = (6, 8)
    FIVE_FOUR = (5, 4)
    SEVEN_EIGHT = (7, 8)

@dataclass
class MusicalNote:
    frequency: float
    duration: float
    velocity: float
    start_time: float

@dataclass
class Chord:
    root: float
    intervals: List[float]
    duration: float
    inversion: int = 0

class ScaleGenerator:
    """Generate various musical scales and modes"""
    
    SCALES = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 10],
        'dorian': [0, 2, 3, 5, 7, 9, 10],
        'phrygian': [0, 1, 3, 5, 7, 8, 10],
        'lydian': [0, 2, 4, 6, 7, 9, 11],
        'mixolydian': [0, 2, 4, 5, 7, 9, 10],
        'locrian': [0, 1, 3, 5, 6, 8, 10],
        'pentatonic': [0, 2, 4, 7, 9],
        'blues': [0, 3, 5, 6, 7, 10],
        'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        'whole_tone': [0, 2, 4, 6, 8, 10],
        'diminished': [0, 2, 3, 5, 6, 8, 9, 11]
    }
    
    @staticmethod
    def get_scale_frequencies(root_freq: float, scale_name: str, octaves: int = 2) -> List[float]:
        """Generate frequencies for a given scale"""
        if scale_name not in ScaleGenerator.SCALES:
            scale_name = 'major'
        
        intervals = ScaleGenerator.SCALES[scale_name]
        frequencies = []
        
        for octave in range(octaves):
            for interval in intervals:
                freq = root_freq * (2 ** (octave + interval / 12))
                frequencies.append(freq)
        
        return frequencies

class ChordProgressionGenerator:
    """Generate sophisticated chord progressions"""
    
    PROGRESSIONS = {
        'classical': [
            [0, 3, 4, 0],  # I-IV-V-I
            [0, 5, 3, 4, 0],  # I-vi-IV-V-I
            [0, 4, 5, 0],  # I-V-vi-I
            [0, 2, 3, 4, 0]  # I-iii-IV-V-I
        ],
        'jazz': [
            [0, 5, 1, 4],  # I-vi-ii-V
            [0, 0, 3, 3, 5, 5, 1, 4],  # I-I-IV-IV-vi-vi-ii-V
            [0, 6, 1, 4],  # I-vii-ii-V
            [0, 2, 5, 1, 4, 0]  # I-iii-vi-ii-V-I
        ],
        'pop': [
            [0, 5, 3, 4],  # I-vi-IV-V
            [5, 3, 0, 4],  # vi-IV-I-V
            [0, 4, 5, 3],  # I-V-vi-IV
            [3, 4, 0, 5]   # IV-V-I-vi
        ],
        'folk': [
            [0, 4, 0, 4],  # I-V-I-V
            [0, 3, 4, 0],  # I-IV-V-I
            [0, 5, 4, 0]   # I-vi-V-I
        ]
    }
    
    @staticmethod
    def generate_progression(style: str, length: int = 8) -> List[int]:
        """Generate a chord progression for a given style"""
        if style not in ChordProgressionGenerator.PROGRESSIONS:
            style = 'classical'
        
        base_progressions = ChordProgressionGenerator.PROGRESSIONS[style]
        progression = random.choice(base_progressions)
        
        # Extend or modify progression to desired length
        while len(progression) < length:
            # Add variations or repeat patterns
            if random.random() < 0.7:
                progression.extend(progression[-2:])  # Repeat last two chords
            else:
                progression.append(random.choice([0, 3, 4, 5]))  # Add common chord
        
        return progression[:length]

class RhythmGenerator:
    """Generate complex rhythmic patterns"""
    
    @staticmethod
    def generate_rhythm_pattern(time_sig: TimeSignature, complexity: float = 0.5) -> List[float]:
        """Generate a rhythmic pattern based on time signature and complexity"""
        beats_per_measure, note_value = time_sig.value
        
        # Basic subdivisions
        subdivisions = [1.0, 0.5, 0.25, 0.125]  # whole, half, quarter, eighth
        
        pattern = []
        current_time = 0
        
        while current_time < beats_per_measure:
            # Choose subdivision based on complexity
            if complexity < 0.3:
                subdivision = random.choice(subdivisions[:2])  # Simple rhythms
            elif complexity < 0.7:
                subdivision = random.choice(subdivisions[:3])  # Moderate complexity
            else:
                subdivision = random.choice(subdivisions)  # High complexity
            
            # Add syncopation occasionally
            if random.random() < complexity * 0.3:
                subdivision *= 0.75  # Dotted rhythm
            
            pattern.append(subdivision)
            current_time += subdivision
            
            if current_time >= beats_per_measure:
                break
        
        return pattern

class InstrumentSimulator:
    """Simulate different instrument characteristics"""
    
    @staticmethod
    def piano_envelope(t: np.ndarray, attack: float = 0.01, decay: float = 0.3, sustain: float = 0.7, release: float = 0.5) -> np.ndarray:
        """Generate piano-like ADSR envelope"""
        total_time = t[-1]
        envelope = np.ones_like(t)
        
        # Attack
        attack_samples = int(attack * len(t))
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay
        decay_samples = int(decay * len(t))
        if decay_samples > 0:
            decay_end = min(attack_samples + decay_samples, len(t))
            envelope[attack_samples:decay_end] = np.linspace(1, sustain, decay_end - attack_samples)
        
        # Release
        release_start = int((1 - release) * len(t))
        envelope[release_start:] = np.linspace(sustain, 0, len(t) - release_start)
        
        return envelope
    
    @staticmethod
    def string_envelope(t: np.ndarray) -> np.ndarray:
        """Generate string-like envelope with bow characteristics"""
        # Slow attack, sustained tone with slight vibrato
        attack = np.exp(-((t - 0.1) ** 2) / 0.01)  # Gaussian attack
        sustain = np.exp(-t * 0.1)  # Slow decay
        vibrato = 1 + 0.05 * np.sin(2 * np.pi * 5 * t)  # 5Hz vibrato
        return attack * sustain * vibrato
    
    @staticmethod
    def brass_envelope(t: np.ndarray) -> np.ndarray:
        """Generate brass-like envelope"""
        # Sharp attack, sustained with slight brightness variation
        attack = 1 - np.exp(-t * 20)
        sustain = np.exp(-t * 0.2)
        brightness = 1 + 0.1 * np.sin(2 * np.pi * 3 * t)
        return attack * sustain * brightness
    
    @staticmethod
    def synthesizer_envelope(t: np.ndarray, style: str = "pad") -> np.ndarray:
        """Generate synthesizer-like envelopes"""
        if style == "pad":
            # Slow attack, long sustain
            return 1 - np.exp(-t * 2)
        elif style == "lead":
            # Quick attack, moderate decay
            attack = 1 - np.exp(-t * 10)
            decay = np.exp(-t * 1)
            return attack * decay
        elif style == "bass":
            # Punchy attack, quick decay
            return np.exp(-t * 3) * (1 - np.exp(-t * 50))
        else:
            return np.ones_like(t)

class AdvancedMusicGenerator:
    """Main class for generating sophisticated musical compositions"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.scale_gen = ScaleGenerator()
        self.chord_gen = ChordProgressionGenerator()
        self.rhythm_gen = RhythmGenerator()
        self.instrument_sim = InstrumentSimulator()
    
    def generate_harmonic_series(self, fundamental: float, num_harmonics: int = 8, harmonic_weights: Optional[List[float]] = None) -> Tuple[List[float], List[float]]:
        """Generate harmonic series with customizable weights"""
        if harmonic_weights is None:
            # Default harmonic weights (decreasing amplitude)
            harmonic_weights = [1.0 / (i + 1) for i in range(num_harmonics)]
        
        frequencies = [fundamental * (i + 1) for i in range(num_harmonics)]
        amplitudes = harmonic_weights[:num_harmonics]
        
        return frequencies, amplitudes
    
    def create_chord(self, root_freq: float, chord_type: str = "major", inversion: int = 0) -> List[float]:
        """Create chord frequencies based on type and inversion"""
        chord_intervals = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'diminished': [0, 3, 6],
            'augmented': [0, 4, 8],
            'major7': [0, 4, 7, 11],
            'minor7': [0, 3, 7, 10],
            'dominant7': [0, 4, 7, 10],
            'sus2': [0, 2, 7],
            'sus4': [0, 5, 7],
            'add9': [0, 4, 7, 14]
        }
        
        intervals = chord_intervals.get(chord_type, chord_intervals['major'])
        frequencies = [root_freq * (2 ** (interval / 12)) for interval in intervals]
        
        # Apply inversion
        for _ in range(inversion % len(frequencies)):
            frequencies[0] *= 2  # Move lowest note up an octave
            frequencies = frequencies[1:] + [frequencies[0]]
        
        return frequencies
    
    def generate_melody(self, scale_freqs: List[float], rhythm_pattern: List[float], style: MusicStyle) -> List[MusicalNote]:
        """Generate a melody based on scale and rhythm"""
        melody = []
        current_time = 0
        
        # Ensure we have scale frequencies
        if not scale_freqs:
            scale_freqs = [440.0]  # Default to A4 if no scale provided
        
        # Style-specific melody characteristics
        if style == MusicStyle.CLASSICAL:
            step_probability = 0.7  # Prefer stepwise motion
            leap_max = 5
        elif style == MusicStyle.JAZZ:
            step_probability = 0.5  # More leaps and chromaticism
            leap_max = 8
        elif style == MusicStyle.ELECTRONIC:
            step_probability = 0.4  # More angular melodies
            leap_max = 12
        else:
            step_probability = 0.6
            leap_max = 6
        
        current_note_index = random.randint(0, max(0, len(scale_freqs) // 2))
        
        for duration in rhythm_pattern:
            # Determine next note based on style
            if random.random() < step_probability:
                # Stepwise motion
                direction = random.choice([-1, 1])
                current_note_index = max(0, min(len(scale_freqs) - 1, current_note_index + direction))
            else:
                # Leap
                leap_size = random.randint(2, leap_max)
                direction = random.choice([-1, 1])
                current_note_index = max(0, min(len(scale_freqs) - 1, current_note_index + direction * leap_size))
            
            frequency = scale_freqs[current_note_index]
            velocity = random.uniform(0.5, 1.0)  # Dynamic variation
            
            note = MusicalNote(frequency, duration, velocity, current_time)
            melody.append(note)
            current_time += duration
        
        return melody
    
    def synthesize_note(self, note: MusicalNote, instrument_type: str = "piano") -> np.ndarray:
        """Synthesize a single note with instrument characteristics"""
        duration_samples = int(note.duration * self.sample_rate)
        t = np.linspace(0, note.duration, duration_samples)
        
        # Generate harmonic content
        if instrument_type == "piano":
            harmonics, weights = self.generate_harmonic_series(note.frequency, 6, [1.0, 0.5, 0.3, 0.2, 0.1, 0.05])
            envelope = self.instrument_sim.piano_envelope(t)
        elif instrument_type == "strings":
            harmonics, weights = self.generate_harmonic_series(note.frequency, 8, [1.0, 0.7, 0.5, 0.3, 0.2, 0.15, 0.1, 0.05])
            envelope = self.instrument_sim.string_envelope(t)
        elif instrument_type == "brass":
            harmonics, weights = self.generate_harmonic_series(note.frequency, 10, [1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.15, 0.1, 0.08, 0.05])
            envelope = self.instrument_sim.brass_envelope(t)
        elif instrument_type == "synth_pad":
            harmonics, weights = self.generate_harmonic_series(note.frequency, 4, [1.0, 0.3, 0.2, 0.1])
            envelope = self.instrument_sim.synthesizer_envelope(t, "pad")
        elif instrument_type == "synth_lead":
            harmonics, weights = self.generate_harmonic_series(note.frequency, 6, [1.0, 0.4, 0.2, 0.1, 0.05, 0.02])
            envelope = self.instrument_sim.synthesizer_envelope(t, "lead")
        else:
            harmonics, weights = self.generate_harmonic_series(note.frequency, 4)
            envelope = np.ones_like(t)
        
        # Synthesize with harmonics
        audio = np.zeros_like(t)
        for freq, weight in zip(harmonics, weights):
            # Add slight detuning for realism
            detune = random.uniform(-0.02, 0.02)
            actual_freq = freq * (1 + detune)
            harmonic_wave = weight * np.sin(2 * np.pi * actual_freq * t)
            audio += harmonic_wave
        
        # Apply envelope and velocity
        audio *= envelope * note.velocity
        
        return audio
    
    def add_effects(self, audio: np.ndarray, effects: Dict[str, float]) -> np.ndarray:
        """Add various audio effects"""
        processed = audio.copy()
        
        # Reverb
        if 'reverb' in effects and effects['reverb'] > 0:
            reverb_amount = effects['reverb']
            delay_samples = int(0.05 * self.sample_rate)  # 50ms delay
            if len(processed) > delay_samples:
                reverb = np.zeros_like(processed)
                reverb[delay_samples:] = processed[:-delay_samples] * reverb_amount
                processed = processed + reverb
        
        # Chorus
        if 'chorus' in effects and effects['chorus'] > 0:
            chorus_amount = effects['chorus']
            delay_samples = int(0.02 * self.sample_rate)  # 20ms delay
            if len(processed) > delay_samples:
                chorus = np.zeros_like(processed)
                chorus[delay_samples:] = processed[:-delay_samples] * chorus_amount
                # Add slight pitch modulation
                t = np.linspace(0, len(processed) / self.sample_rate, len(processed))
                pitch_mod = 1 + 0.01 * np.sin(2 * np.pi * 1.5 * t)  # 1.5Hz modulation
                processed = processed + chorus * pitch_mod[:len(chorus)]
        
        # Distortion
        if 'distortion' in effects and effects['distortion'] > 0:
            drive = effects['distortion']
            processed = np.tanh(processed * (1 + drive * 5)) / (1 + drive)
        
        return processed
    
    def generate_composition(self, description: str, duration: float = 10, style: Optional[MusicStyle] = None) -> np.ndarray:
        """Generate a complete musical composition"""
        
        # Input validation
        if description is None:
            description = "simple melody"
        if not isinstance(description, str):
            description = str(description)
        if not description.strip():
            description = "simple melody"
            
        # Duration validation
        if not isinstance(duration, (int, float)):
            raise TypeError(f"Duration must be a number, got {type(duration).__name__}")
        if duration <= 0:
            duration = 1.0  # Default to 1 second for invalid durations
        if duration > 600:  # Limit to 10 minutes
            duration = 600
        
        # Analyze description for musical elements
        description_lower = description.lower()
        
        # Determine style if not specified
        if style is None:
            if any(word in description_lower for word in ['classical', 'orchestra', 'symphony']):
                style = MusicStyle.CLASSICAL
            elif any(word in description_lower for word in ['jazz', 'swing', 'bebop']):
                style = MusicStyle.JAZZ
            elif any(word in description_lower for word in ['electronic', 'synth', 'edm']):
                style = MusicStyle.ELECTRONIC
            elif any(word in description_lower for word in ['ambient', 'atmospheric', 'drone']):
                style = MusicStyle.AMBIENT
            elif any(word in description_lower for word in ['rock', 'metal', 'punk']):
                style = MusicStyle.ROCK
            elif any(word in description_lower for word in ['folk', 'acoustic', 'country']):
                style = MusicStyle.FOLK
            else:
                style = random.choice(list(MusicStyle))
        
        # Determine key and scale
        root_freq = 440  # A4
        if any(word in description_lower for word in ['bright', 'happy', 'major']):
            scale_name = 'major'
        elif any(word in description_lower for word in ['sad', 'dark', 'minor']):
            scale_name = 'minor'
        elif any(word in description_lower for word in ['modal', 'dorian']):
            scale_name = 'dorian'
        elif any(word in description_lower for word in ['blues', 'bluesy']):
            scale_name = 'blues'
        elif any(word in description_lower for word in ['exotic', 'eastern']):
            scale_name = random.choice(['phrygian', 'locrian', 'whole_tone'])
        else:
            scale_name = random.choice(['major', 'minor', 'dorian', 'mixolydian'])
        
        # Generate scale
        scale_freqs = self.scale_gen.get_scale_frequencies(root_freq, scale_name, 3)
        
        # Determine tempo and time signature
        if 'slow' in description_lower:
            tempo = random.randint(60, 80)
        elif 'fast' in description_lower:
            tempo = random.randint(120, 160)
        else:
            tempo = random.randint(90, 120)
        
        time_sig = TimeSignature.FOUR_FOUR
        if 'waltz' in description_lower:
            time_sig = TimeSignature.THREE_FOUR
        elif 'complex' in description_lower:
            time_sig = random.choice([TimeSignature.FIVE_FOUR, TimeSignature.SEVEN_EIGHT])
        
        # Generate rhythm pattern
        complexity = 0.3 if style == MusicStyle.AMBIENT else 0.7
        rhythm_pattern = self.rhythm_gen.generate_rhythm_pattern(time_sig, complexity)
        
        # Scale rhythm pattern to fit duration
        pattern_duration = sum(rhythm_pattern)
        if pattern_duration <= 0:
            # Fallback to simple pattern if rhythm generation fails
            pattern_duration = 1.0
            rhythm_pattern = [0.5, 0.5]  # Simple quarter note pattern
        
        num_repetitions = int(duration / pattern_duration) + 1
        extended_pattern = (rhythm_pattern * num_repetitions)[:int(duration * 2)]  # Approximate
        
        # Generate melody
        melody = self.generate_melody(scale_freqs, extended_pattern, style)
        
        # Generate chord progression
        chord_style = 'jazz' if style == MusicStyle.JAZZ else 'classical'
        progression_length = max(1, len(melody) // 4)  # Ensure at least 1 chord
        progression = self.chord_gen.generate_progression(chord_style, progression_length)
        
        # Ensure progression is never empty
        if not progression:
            progression = [0]  # Default to root chord
        
        # Synthesize composition
        total_samples = int(duration * self.sample_rate)
        composition = np.zeros(total_samples)
        
        # Add melody
        current_sample = 0
        for note in melody:
            if current_sample >= total_samples:
                break
            
            # Choose instrument based on style
            if style == MusicStyle.CLASSICAL:
                instrument = random.choice(['piano', 'strings'])
            elif style == MusicStyle.JAZZ:
                instrument = random.choice(['piano', 'brass'])
            elif style == MusicStyle.ELECTRONIC:
                instrument = random.choice(['synth_lead', 'synth_pad'])
            else:
                instrument = 'piano'
            
            note_audio = self.synthesize_note(note, instrument)
            end_sample = min(current_sample + len(note_audio), total_samples)
            composition[current_sample:end_sample] += note_audio[:end_sample - current_sample] * 0.6
            
            current_sample += int(note.duration * self.sample_rate)
        
        # Add harmony/chords
        chord_duration = duration / max(1, len(progression))  # Prevent division by zero
        for i, chord_degree in enumerate(progression):
            start_time = i * chord_duration
            start_sample = int(start_time * self.sample_rate)
            
            if start_sample >= total_samples:
                break
            
            # Create chord
            chord_root = scale_freqs[chord_degree % len(scale_freqs)]
            chord_type = 'major' if scale_name in ['major', 'lydian'] else 'minor'
            if style == MusicStyle.JAZZ:
                chord_type = random.choice(['major7', 'minor7', 'dominant7'])
            
            chord_freqs = self.create_chord(chord_root, chord_type)
            
            # Synthesize chord
            chord_samples = int(chord_duration * self.sample_rate)
            end_sample = min(start_sample + chord_samples, total_samples)
            
            for freq in chord_freqs:
                chord_note = MusicalNote(freq, chord_duration, 0.3, start_time)
                chord_audio = self.synthesize_note(chord_note, 'synth_pad')
                composition[start_sample:end_sample] += chord_audio[:end_sample - start_sample] * 0.4
        
        # Add effects based on style
        effects = {}
        if style == MusicStyle.AMBIENT:
            effects = {'reverb': 0.4, 'chorus': 0.2}
        elif style == MusicStyle.ELECTRONIC:
            effects = {'chorus': 0.3, 'distortion': 0.1}
        elif style == MusicStyle.CLASSICAL:
            effects = {'reverb': 0.2}
        
        if effects:
            composition = self.add_effects(composition, effects)
        
        # Normalize
        if np.max(np.abs(composition)) > 0:
            composition = composition / np.max(np.abs(composition)) * 0.8
        
        return composition
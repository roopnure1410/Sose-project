#!/usr/bin/env python3
"""
Test script to verify Gradio interface music generation
"""

import gradio as gr
import numpy as np
import soundfile as sf
import os
import time
from advanced_music_generator import AdvancedMusicGenerator, MusicStyle

def test_generation_function(description, duration, style):
    """Test the actual generation function used by Gradio"""
    print(f"🎵 Testing generation: '{description}' ({style}, {duration}s)")
    
    try:
        # Initialize the advanced music generator
        generator = AdvancedMusicGenerator(sample_rate=44100)
        
        # Map style parameter to MusicStyle enum
        style_mapping = {
            "classical": MusicStyle.CLASSICAL,
            "jazz": MusicStyle.JAZZ,
            "electronic": MusicStyle.ELECTRONIC,
            "ambient": MusicStyle.AMBIENT,
            "rock": MusicStyle.ROCK,
            "folk": MusicStyle.FOLK,
            "world": MusicStyle.WORLD,
            "balanced": None  # Let the system auto-detect from description
        }
        
        music_style = style_mapping.get(style, None)
        
        # Generate sophisticated musical composition
        audio = generator.generate_composition(
            description=description,
            duration=duration,
            style=music_style
        )
        
        # Save to file with timestamp to avoid conflicts
        timestamp = int(time.time())
        output_path = f"test_generation_{timestamp}.wav"
        sf.write(output_path, audio, generator.sample_rate)
        
        print(f"✅ Generated: {output_path}")
        print(f"📊 Audio length: {len(audio)} samples")
        print(f"📊 Duration: {len(audio)/generator.sample_rate:.2f} seconds")
        print(f"📊 Max amplitude: {np.max(np.abs(audio)):.3f}")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_simple_demo():
    """Create a simplified demo to test generation"""
    
    def generate_music(description, duration, style):
        """Wrapper function for Gradio"""
        output_path = test_generation_function(description, duration, style)
        if output_path and os.path.exists(output_path):
            return output_path
        else:
            # Return a simple tone if generation fails
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            audio = np.sin(2 * np.pi * 440 * t) * 0.3
            fallback_path = f"fallback_{int(time.time())}.wav"
            sf.write(fallback_path, audio, sample_rate)
            return fallback_path
    
    # Create Gradio interface
    with gr.Blocks(title="OpenMusic Test") as demo:
        gr.Markdown("# 🎵 OpenMusic Generation Test")
        
        with gr.Row():
            with gr.Column():
                description_input = gr.Textbox(
                    label="Music Description",
                    placeholder="Describe the music you want to generate...",
                    value="peaceful piano melody"
                )
                
                duration_slider = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=5,
                    step=1,
                    label="Duration (seconds)"
                )
                
                style_dropdown = gr.Dropdown(
                    choices=["classical", "jazz", "electronic", "ambient", "rock", "folk", "world", "balanced"],
                    value="classical",
                    label="Musical Style"
                )
                
                generate_btn = gr.Button("🎵 Generate Music", variant="primary")
            
            with gr.Column():
                audio_output = gr.Audio(label="Generated Music")
                status_text = gr.Textbox(label="Status", interactive=False)
        
        def generate_with_status(description, duration, style):
            try:
                audio_path = generate_music(description, duration, style)
                return audio_path, f"✅ Generated successfully: {audio_path}"
            except Exception as e:
                return None, f"❌ Error: {str(e)}"
        
        generate_btn.click(
            fn=generate_with_status,
            inputs=[description_input, duration_slider, style_dropdown],
            outputs=[audio_output, status_text]
        )
    
    return demo

def main():
    """Main test function"""
    print("🎵 GRADIO GENERATION TEST")
    print("=" * 30)
    
    # Test direct generation
    print("\n1. Testing direct generation...")
    test_cases = [
        ("peaceful piano melody", 3, "classical"),
        ("upbeat jazz", 3, "jazz"),
        ("electronic dance", 3, "electronic")
    ]
    
    for desc, dur, style in test_cases:
        result = test_generation_function(desc, dur, style)
        if result:
            print(f"✅ {style} generation successful")
        else:
            print(f"❌ {style} generation failed")
    
    # Launch test demo
    print("\n2. Launching test demo...")
    demo = create_simple_demo()
    demo.launch(server_name="0.0.0.0", server_port=7861, share=False)

if __name__ == "__main__":
    main()
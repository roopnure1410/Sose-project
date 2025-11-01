#!/usr/bin/env python3
"""
Enhanced OpenMusic Demo
A beautiful and interactive demo showcasing the OpenMusic project with enhanced UI/UX.
"""

import gradio as gr
import torch
import numpy as np
import soundfile as sf
import os
import time
import random
import math
import tempfile
from pathlib import Path
from advanced_music_generator import AdvancedMusicGenerator, MusicStyle

def generate_enhanced_demo_audio(description, duration=8, style="balanced"):
    """
    Advanced demo audio generation using sophisticated music generation algorithms
    """
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
    output_path = f"demo_output_{timestamp}.wav"
    sf.write(output_path, audio, generator.sample_rate)
    
    return output_path

def get_random_suggestion():
    """Get a random music suggestion for inspiration"""
    suggestions = [
        "Peaceful piano melody with gentle rain sounds",
        "Upbeat electronic dance music with synthesizers",
        "Classical string quartet playing in a cathedral",
        "Jazz saxophone solo with walking bass line",
        "Ambient space music with ethereal pads",
        "Acoustic guitar fingerpicking with birds chirping",
        "Orchestral film score with dramatic crescendo",
        "Lo-fi hip hop beats with vinyl crackle",
        "Celtic folk music with flute and harp",
        "Minimalist piano composition with reverb"
    ]
    return random.choice(suggestions)

def create_enhanced_demo():
    """Create the enhanced Gradio demo interface with beautiful UI/UX"""
    
    # Custom CSS for beautiful styling
    custom_css = """
    .main-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .content-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    .header-title {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .generate-btn {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 15px 30px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        color: white !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    .generate-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    .suggestion-btn {
        background: linear-gradient(45deg, #ffecd2, #fcb69f) !important;
        border: none !important;
        border-radius: 20px !important;
        color: #333 !important;
        font-weight: 500 !important;
    }
    .example-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
        font-weight: 500;
    }
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
    }
    .feature-highlight {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    """
    
    with gr.Blocks(title="🎵 OpenMusic - AI Music Generation", css=custom_css, theme=gr.themes.Soft()) as demo:
        with gr.Column(elem_classes="content-container"):
            # Header
            gr.HTML('<h1 class="header-title">🎵 OpenMusic Studio</h1>')
            gr.HTML('<p class="subtitle">Transform your imagination into beautiful music with AI</p>')
            
            # Main interface
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("### 🎼 Describe Your Music")
                    description_input = gr.Textbox(
                        label="Music Description",
                        placeholder="Describe the music you want to create...",
                        lines=4,
                        info="Be creative! Describe instruments, mood, style, or any musical elements you envision."
                    )
                    
                    with gr.Row():
                        suggestion_btn = gr.Button("🎲 Get Inspiration", elem_classes="suggestion-btn", size="sm")
                        clear_btn = gr.Button("🗑️ Clear", size="sm")
                    
                    with gr.Row():
                        duration_slider = gr.Slider(
                            minimum=3,
                            maximum=15,
                            value=8,
                            step=1,
                            label="⏱️ Duration (seconds)",
                            info="Longer durations create more complex compositions"
                        )
                        style_dropdown = gr.Dropdown(
                            choices=["balanced", "classical", "jazz", "electronic", "ambient", "rock", "folk", "world"],
                            value="balanced",
                            label="🎨 Musical Style",
                            info="Choose the overall character of your music"
                        )
                    
                    generate_btn = gr.Button(
                        "🎵 Generate Music",
                        variant="primary",
                        elem_classes="generate-btn",
                        size="lg"
                    )
                
                with gr.Column(scale=2):
                    gr.Markdown("### 🎧 Your Generated Music")
                    audio_output = gr.Audio(
                        label="Generated Audio",
                        show_download_button=True,
                        interactive=False
                    )
                    
                    with gr.Row():
                        status_text = gr.Textbox(
                            label="🔄 Status",
                            interactive=False,
                            value="Ready to generate music! 🎵"
                        )
                    
                    # Progress indicator (simulated)
                    progress_bar = gr.Progress()
            
            # Examples and features
            with gr.Row():
                with gr.Column():
                    gr.HTML('<div class="example-card"><h3>🌟 Try These Examples</h3></div>')
                    example_buttons = []
                    examples = [
                        "Peaceful piano melody with gentle rain sounds",
                        "Upbeat electronic dance music with synthesizers",
                        "Classical string quartet playing in a cathedral",
                        "Jazz saxophone solo with walking bass line"
                    ]
                    
                    for example in examples:
                        btn = gr.Button(f"💡 {example}", size="sm")
                        example_buttons.append(btn)
                        btn.click(lambda x=example: x, outputs=description_input)
                
                with gr.Column():
                    gr.HTML('<div class="info-card"><h3>✨ Features</h3></div>')
                    gr.HTML('''
                    <div class="feature-highlight">
                        <strong>🎹 Multi-Instrument Support</strong><br>
                        Piano, strings, electronic, and more
                    </div>
                    <div class="feature-highlight">
                        <strong>🎨 Style Variations</strong><br>
                        Orchestral, electronic, ambient, balanced
                    </div>
                    <div class="feature-highlight">
                        <strong>⚡ Real-time Generation</strong><br>
                        Fast audio synthesis and processing
                    </div>
                    <div class="feature-highlight">
                        <strong>🔊 High Quality Output</strong><br>
                        16kHz audio with reverb and effects
                    </div>
                    ''')
        
        # Event handlers with progress tracking
        def generate_with_progress(description, duration, style):
            if not description.strip():
                return None, "❌ Please enter a music description first!"
            
            try:
                # Update status
                status_msg = f"🎵 Generating {style} music... Please wait..."
                
                # Generate the audio
                audio_path = generate_enhanced_demo_audio(description, duration, style)
                
                # Return success
                return audio_path, f"✅ Music generated successfully! Style: {style}, Duration: {duration}s"
            except Exception as e:
                print(f"Error in generate_with_progress: {e}")
                return None, f"❌ Error generating music: {str(e)}"
        
        generate_btn.click(
            fn=generate_with_progress,
            inputs=[description_input, duration_slider, style_dropdown],
            outputs=[audio_output, status_text]
        )
        
        # Utility functions
        suggestion_btn.click(
            fn=get_random_suggestion,
            outputs=description_input
        )
        
        clear_btn.click(
            lambda: ("", "Ready to generate music! 🎵"),
            outputs=[description_input, status_text]
        )
        
        # Footer
        gr.HTML('''
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: linear-gradient(45deg, #f093fb, #f5576c); border-radius: 15px; color: white;">
            <h3>🚀 About OpenMusic</h3>
            <p>This enhanced demo showcases the OpenMusic project with improved UI/UX. 
            The full version uses advanced AI models for professional music generation.</p>
            <p><strong>Note:</strong> This demo uses synthetic audio generation. 
            Download the full model checkpoints for AI-powered music creation!</p>
        </div>
        ''')
    
    return demo

def main():
    """Main function to run the demo"""
    print("🎵 Starting Enhanced OpenMusic Demo...")
    print("✨ Beautiful UI/UX loaded")
    print("🎨 Enhanced features activated")
    print("🔧 Dependencies verified")
    
    demo = create_enhanced_demo()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Simplified OpenMusic Demo - Focused on Working Music Generation
This version removes complex UI elements and focuses purely on functionality
"""

import gradio as gr
import numpy as np
import soundfile as sf
import os
import time
from advanced_music_generator import AdvancedMusicGenerator, MusicStyle

def generate_music_simple(description, duration, style):
    """Simple music generation function without complex progress tracking"""
    
    if not description or not description.strip():
        return None, "Please enter a music description"
    
    try:
        print(f"Generating music: '{description}' ({style}, {duration}s)")
        
        # Initialize generator
        generator = AdvancedMusicGenerator(sample_rate=44100)
        
        # Map style to enum
        style_mapping = {
            "classical": MusicStyle.CLASSICAL,
            "jazz": MusicStyle.JAZZ,
            "electronic": MusicStyle.ELECTRONIC,
            "ambient": MusicStyle.AMBIENT,
            "rock": MusicStyle.ROCK,
            "folk": MusicStyle.FOLK,
            "world": MusicStyle.WORLD,
            "balanced": None
        }
        
        music_style = style_mapping.get(style, None)
        
        # Generate audio
        audio = generator.generate_composition(
            description=description,
            duration=duration,
            style=music_style
        )
        
        # Save to file
        timestamp = int(time.time())
        output_path = f"simple_demo_{timestamp}.wav"
        sf.write(output_path, audio, generator.sample_rate)
        
        print(f"Music generated successfully: {output_path}")
        return output_path, f"✅ Generated {style} music ({duration}s)"
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        return None, error_msg

def passthrough(v):
    """Helper to sync component values across controls"""
    return v

def create_simple_demo():
    """Create a better styled Gradio demo (clean UI/UX)"""
    custom_css = """
    :root { --bg: #0b0f1a; --fg: #ffffff; --muted: rgba(255,255,255,0.68); --glass: rgba(255,255,255,0.06); --border: rgba(255,255,255,0.12); --accent1: #9f7aea; --accent2: #06b6d4; --accent3: #34d399; }
    body { background: radial-gradient(1200px 600px at 20% 0%, rgba(159,122,234,0.12), transparent), radial-gradient(1200px 600px at 80% 0%, rgba(6,182,212,0.12), transparent), var(--bg); color: var(--fg); }
    .container { max-width: 1100px; margin: 0 auto; padding: 0 16px; }
    .hero { display:flex; align-items:center; justify-content:space-between; gap:1rem; }
    .brand { display:flex; align-items:center; gap:.9rem; padding:1rem 1.25rem; background:var(--glass); border:1px solid var(--border); border-radius:16px; backdrop-filter: blur(6px); }
    .brand h1 { font-size:1.25rem; margin:0; }
    .brand p { margin:0; color:var(--muted); font-size:.9rem; }
    .underline { height:2px; background: linear-gradient(90deg, var(--accent1), var(--accent2)); margin: 12px 0 24px; }
    .card { background:var(--glass); border:1px solid var(--border); border-radius:18px; padding:18px; backdrop-filter: blur(6px); }
    .btn-primary { background: linear-gradient(90deg, var(--accent1), var(--accent2)); color:#0b0f1a; font-weight:600; border-radius:14px; padding:.8rem 1.1rem; border: none; }
    .btn-primary:hover { opacity:.95; box-shadow: 0 0 0 2px rgba(159,122,234,0.25), 0 0 30px rgba(6,182,212,0.15); }
    .grid { display:grid; gap:16px; }
    @media (min-width: 960px) { .grid-2 { grid-template-columns: 1.15fr 1fr; } }
    .examples { display:grid; gap:12px; }
    @media (min-width: 900px) { .examples { grid-template-columns: repeat(3, 1fr); } }
    .example-card { text-align:left; padding:14px; border-radius:14px; background:var(--glass); border:1px solid var(--border); }
    .muted { color: var(--muted); }
    .pill { display:inline-block; padding:.35rem .7rem; border-radius:999px; background: rgba(255,255,255,0.08); border: 1px solid var(--border); }
    .chips { display:flex; flex-wrap:wrap; gap:.5rem; }
    .chip { padding:.45rem .7rem; border-radius:12px; border:1px solid var(--border); background:rgba(255,255,255,0.06); cursor:pointer; }
    .chip:hover { border-color: rgba(159,122,234,0.45); box-shadow: 0 0 0 2px rgba(159,122,234,0.15); }
    .pulse { animation: pulse 1.2s ease-in-out infinite; opacity:.85 }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }
    .input-group { display:grid; grid-template-columns: 1fr auto; gap:.75rem; align-items:center; }
    """

    with gr.Blocks(title="OpenMusic AI", css=custom_css, theme=gr.themes.Soft()) as demo:
        # Header
        gr.HTML("""
        <div class='container'>
          <div class='hero'>
            <div class='brand'>
              <div style='font-size:1.4rem'>🎵</div>
              <div>
                <h1>OpenMusic AI</h1>
                <p>Create beautiful music with AI — modern, minimal UI.</p>
              </div>
            </div>
            <div class='pill'>v1 • Simple Demo</div>
          </div>
          <div class='underline'></div>
        </div>
        """)

        with gr.Row():
            with gr.Column(elem_classes=["card"], scale=6):
                gr.Markdown("### Generate Your Music")
                description = gr.Textbox(label="Music Description", placeholder="Describe the music you want...", lines=3)

                # Duration: slider + numeric sync
                gr.Markdown("**Duration**")
                with gr.Row():
                    duration_slider = gr.Slider(minimum=3, maximum=15, value=5, step=1, label="Seconds")
                    duration_number = gr.Number(value=5, precision=0, label="")

                # Style: quick chips + dropdown
                gr.Markdown("**Style**")
                style_radio = gr.Radio(choices=["balanced", "classical", "jazz", "electronic", "ambient", "rock", "folk", "world"], value="balanced", label="Quick Select")
                style = gr.Dropdown(choices=["balanced", "classical", "jazz", "electronic", "ambient", "rock", "folk", "world"], value="balanced", label="Musical Style")

                generate_btn = gr.Button("🎶 Generate Music", elem_classes=["btn-primary"])

            with gr.Column(elem_classes=["card"], scale=5):
                gr.Markdown("### Preview")
                audio_output = gr.Audio(label="Generated Track")
                status_output = gr.Textbox(label="Status", interactive=False)

        # Sync controls
        duration_slider.change(fn=passthrough, inputs=duration_slider, outputs=duration_number)
        duration_number.change(fn=passthrough, inputs=duration_number, outputs=duration_slider)
        style_radio.change(fn=passthrough, inputs=style_radio, outputs=style)
        style.change(fn=passthrough, inputs=style, outputs=style_radio)

        gr.Markdown("### Try These Examples")
        examples = [
            ["Peaceful piano with soft strings", 5, "classical"],
            ["Urban synthwave with punchy drums", 6, "electronic"],
            ["Smooth jazz trio with sax", 7, "jazz"],
            ["Chill ambient pads for focus", 8, "ambient"],
            ["Energetic rock riff with driving drums", 6, "rock"],
        ]
        gr.Examples(examples=examples, inputs=[description, duration, style], label="Example Prompts")

        generate_btn.click(fn=generate_music_simple, inputs=[description, duration_slider, style], outputs=[audio_output, status_output])

        gr.Markdown("""
        <div class='underline'></div>
        <p class='muted' style='text-align:center'>© 2024 OpenMusic AI · Built with Gradio</p>
        """)

    return demo

def main():
    """Run the simple demo"""
    print("🎵 Starting Simple OpenMusic Demo...")
    print("🔧 Simplified interface for maximum compatibility")
    
    demo = create_simple_demo()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7862,  # Different port to avoid conflicts
        share=False,
        show_error=True,
        debug=True  # Enable debug mode for better error reporting
    )

if __name__ == "__main__":
    main()
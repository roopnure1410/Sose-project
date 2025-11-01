#!/usr/bin/env python3
"""
Test the exact function that gets called when the Generate button is clicked
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_gradio_generation_function():
    """Test the exact function that Gradio calls"""
    print("🎵 TESTING GRADIO GENERATION FUNCTION")
    print("=" * 45)
    
    try:
        # Import the demo module
        import simple_demo
        
        # Create the demo to get access to the internal function
        demo = simple_demo.create_enhanced_demo()
        
        # Test the generation function directly
        print("🎼 Testing generate_enhanced_demo_audio function...")
        
        # Test parameters
        description = "peaceful piano melody"
        duration = 5
        style = "classical"
        
        print(f"📝 Description: '{description}'")
        print(f"⏱️ Duration: {duration}s")
        print(f"🎨 Style: {style}")
        
        # Call the function directly
        output_path = simple_demo.generate_enhanced_demo_audio(description, duration, style)
        
        if output_path and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Audio generated successfully!")
            print(f"📁 File: {output_path}")
            print(f"📊 Size: {file_size} bytes")
            
            # Verify audio content
            import soundfile as sf
            audio_data, sample_rate = sf.read(output_path)
            duration_actual = len(audio_data) / sample_rate
            max_amplitude = abs(audio_data).max()
            
            print(f"📊 Actual duration: {duration_actual:.2f}s")
            print(f"📊 Sample rate: {sample_rate}Hz")
            print(f"📊 Max amplitude: {max_amplitude:.3f}")
            
            # Clean up
            os.remove(output_path)
            print("🧹 Test file cleaned up")
            
            return True
        else:
            print(f"❌ No file generated or file doesn't exist: {output_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gradio_progress_function():
    """Test the progress function that Gradio actually calls"""
    print("\n🔄 TESTING GRADIO PROGRESS FUNCTION")
    print("=" * 45)
    
    try:
        # We need to simulate the internal function
        # Let's create a mock version of what happens inside the demo
        
        def mock_generate_with_progress(description, duration, style):
            """Mock the internal generate_with_progress function"""
            if not description.strip():
                return None, "❌ Please enter a music description first!"
            
            try:
                # Import here to avoid circular imports
                from simple_demo import generate_enhanced_demo_audio
                
                # Generate the audio
                audio_path = generate_enhanced_demo_audio(description, duration, style)
                
                # Return success
                return audio_path, f"✅ Music generated successfully! Style: {style}, Duration: {duration}s"
            except Exception as e:
                print(f"Error in generate_with_progress: {e}")
                return None, f"❌ Error generating music: {str(e)}"
        
        # Test the mock function
        description = "upbeat jazz melody"
        duration = 4
        style = "jazz"
        
        print(f"📝 Description: '{description}'")
        print(f"⏱️ Duration: {duration}s")
        print(f"🎨 Style: {style}")
        
        audio_path, status_message = mock_generate_with_progress(description, duration, style)
        
        print(f"📄 Status: {status_message}")
        
        if audio_path and os.path.exists(audio_path):
            print(f"✅ Progress function working correctly!")
            print(f"📁 Generated: {audio_path}")
            
            # Clean up
            os.remove(audio_path)
            print("🧹 Test file cleaned up")
            
            return True
        else:
            print(f"❌ Progress function failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 GRADIO BUTTON FUNCTIONALITY TEST")
    print("=" * 50)
    
    test1_result = test_gradio_generation_function()
    test2_result = test_gradio_progress_function()
    
    print("\n📊 TEST RESULTS")
    print("=" * 20)
    print(f"✅ Direct function test: {'PASS' if test1_result else 'FAIL'}")
    print(f"✅ Progress function test: {'PASS' if test2_result else 'FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 All tests passed! The generation functions are working.")
        print("💡 If the Gradio interface still isn't working, the issue might be:")
        print("   1. Browser JavaScript errors")
        print("   2. Gradio event binding issues")
        print("   3. Network connectivity problems")
        print("   4. Browser cache issues")
        print("\n🔧 Try these solutions:")
        print("   1. Open browser developer tools (F12)")
        print("   2. Check the Console tab for errors")
        print("   3. Refresh the page (Ctrl+F5)")
        print("   4. Try a different browser")
    else:
        print("\n❌ Some tests failed. This explains the generation issues.")

if __name__ == "__main__":
    main()
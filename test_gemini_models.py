#!/usr/bin/env python3
"""
Test script to check available Gemini models and test the configuration.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_config():
    """Test Gemini configuration and list available models."""
    print("🧪 Testing Gemini configuration...")
    
    try:
        import google.generativeai as genai
        from config.gemini import gemini_config
        
        if not gemini_config:
            print("❌ Gemini configuration not available")
            print("💡 Please set GOOGLE_API_KEY in your environment")
            return False
        
        print(f"✅ Gemini configuration loaded")
        print(f"📋 Model: {gemini_config.model_name}")
        print(f"🌡️  Temperature: {gemini_config.temperature}")
        print(f"📏 Max tokens: {gemini_config.max_output_tokens}")
        
        # Test API connection by listing models
        print("\n🔍 Listing available models...")
        try:
            models = genai.list_models()
            available_models = []
            
            for model in models:
                # Check if the model supports generateContent
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
                    print(f"✅ {model.name}")
            
            if not available_models:
                print("❌ No models found that support generateContent")
                return False
            
            # Test if our configured model is available
            current_model = f"models/{gemini_config.model_name}"
            if current_model in available_models:
                print(f"\n✅ Current model '{gemini_config.model_name}' is available")
            else:
                print(f"\n⚠️  Current model '{gemini_config.model_name}' not found")
                print("📋 Available models for generateContent:")
                for model in available_models:
                    model_name = model.replace('models/', '')
                    print(f"   • {model_name}")
                print(f"\n💡 Consider using: {available_models[0].replace('models/', '')}")
                return False
            
            # Test a simple generation
            print("\n🧪 Testing content generation...")
            try:
                model = genai.GenerativeModel(gemini_config.model_name)
                response = model.generate_content("Say 'Hello, World!' in a friendly way.")
                
                if response.text:
                    print("✅ Content generation successful!")
                    print(f"📝 Response: {response.text[:100]}...")
                    return True
                else:
                    print("❌ Empty response from model")
                    return False
                    
            except Exception as e:
                print(f"❌ Content generation failed: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to list models: {e}")
            print("💡 Check your API key and internet connection")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Run Gemini configuration test."""
    print("🚀 Gemini Model Configuration Test\n")
    
    success = test_gemini_config()
    
    print("\n" + "="*60)
    if success:
        print("🎉 Gemini configuration is working correctly!")
        print("📱 The AI analysis should now work in the Streamlit app.")
    else:
        print("❌ Gemini configuration needs attention.")
        print("\n📋 Troubleshooting steps:")
        print("1. Verify your GOOGLE_API_KEY is correct")
        print("2. Check internet connection")
        print("3. Try a different model name if suggested above")
        print("4. Ensure API quotas are not exceeded")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

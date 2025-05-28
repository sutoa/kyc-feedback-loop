#!/usr/bin/env python3
"""
Simple OpenAI Chat Script
A straightforward script to submit prompts to OpenAI and get responses.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def chat_with_openai(prompt, model="gpt-4o-mini", max_tokens=1000, temperature=0.7):
    """
    Send a prompt to OpenAI and return the response.
    
    Args:
        prompt (str): The prompt to send to OpenAI
        model (str): The model to use (default: gpt-3.5-turbo)
        max_tokens (int): Maximum tokens in response (default: 1000)
        temperature (float): Creativity level 0-1 (default: 0.7)
    
    Returns:
        str: The response from OpenAI
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        # Send the prompt to OpenAI
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        # Extract and return the response
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"

def interactive_chat():
    """
    Interactive chat mode - keep chatting until user types 'quit'
    """
    print("🤖 OpenAI Chat Bot")
    print("Type 'quit' to exit")
    print("-" * 40)
    
    while True:
        prompt = input("\nYou: ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
        
        if not prompt:
            print("Please enter a prompt.")
            continue
        
        print("\n🤖 Thinking...")
        response = chat_with_openai(prompt)
        print(f"\nAI: {response}")

def single_prompt_mode():
    """
    Single prompt mode - ask for one prompt and return response
    """
    prompt = input("Enter your prompt: ").strip()
    
    if not prompt:
        print("No prompt provided.")
        return
    
    print("\n🤖 Thinking...")
    response = chat_with_openai(prompt)
    print(f"\nAI Response:\n{response}")

def main():
    """
    Main function to choose between interactive and single prompt mode
    """
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please add your OpenAI API key to the .env file:")
        print("OPENAI_API_KEY=your_api_key_here")
        return
    
    print("Choose mode:")
    print("1. Interactive chat (type 'quit' to exit)")
    print("2. Single prompt")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        interactive_chat()
    elif choice == "2":
        single_prompt_mode()
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main() 
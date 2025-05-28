#!/usr/bin/env python3
"""
Test script for CSM Researcher Crew
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

# Add the src directory to Python path
sys.path.insert(0, str(project_root / "src"))

def test_csm_crew():
    """Test the CSM Researcher Crew"""
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY environment variable")
        print("export OPENAI_API_KEY='your_key_here'")
        return False
    
    try:
        from self_evaluation_loop_flow.crews.csm_researcher_crew.csm_researcher_crew import CsmResearcherCrew
        
        print("🚀 Testing CSM Researcher Crew...")
        
        # Create crew instance
        crew_instance = CsmResearcherCrew()
        
        # Check what agents and tasks are available
        print(f"Available agents: {len(crew_instance.agents) if hasattr(crew_instance, 'agents') else 'Not loaded yet'}")
        print(f"Available tasks: {len(crew_instance.tasks) if hasattr(crew_instance, 'tasks') else 'Not loaded yet'}")
        
        # Create the crew
        crew = crew_instance.crew()
        
        print(f"✅ Crew created successfully!")
        print(f"   - Agents: {len(crew.agents)}")
        print(f"   - Tasks: {len(crew.tasks)}")
        
        # Test inputs
        inputs = {
            "client": "Alpha LongTail LLC",
            "current_year": "2024",
            "feedback": None
        }
        
        print(f"\n🔍 Testing with client: {inputs['client']}")
        print("Starting crew execution...")
        
        # Run the crew
        result = crew.kickoff(inputs=inputs)
        
        print("\n✅ Crew execution completed!")
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        
        # Check for output file
        output_files = list(Path.cwd().glob("*.md"))
        if output_files:
            print(f"\n📄 Output files created: {[f.name for f in output_files]}")
            for file in output_files:
                if file.stat().st_size > 0:
                    with open(file, "r") as f:
                        content = f.read()
                        print(f"\n📄 {file.name} preview (first 200 chars):")
                        print(content[:200] + "..." if len(content) > 200 else content)
        else:
            print("\n⚠️  No output files found")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("CSM Researcher Crew Test")
    print("=" * 60)
    
    success = test_csm_crew()
    
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
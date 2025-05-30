#!/usr/bin/env python3
"""
Test script for CSM Review Crew
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

def test_csm_review_crew():
    """Test the CSM Review Crew"""
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY environment variable")
        print("export OPENAI_API_KEY='your_key_here'")
        return False
    
    try:
        from self_evaluation_loop_flow.crews.csm_review_crew.csm_review_crew import CsmReviewCrew
        
        print("🚀 Testing CSM Review Crew...")
        
        # Create crew instance
        crew_instance = CsmReviewCrew()
        
        # Check what agents and tasks are available
        print(f"Available agents: {len(crew_instance.agents) if hasattr(crew_instance, 'agents') else 'Not loaded yet'}")
        print(f"Available tasks: {len(crew_instance.tasks) if hasattr(crew_instance, 'tasks') else 'Not loaded yet'}")
        
        # Create the crew
        crew = crew_instance.crew()
        
        print(f"✅ Crew created successfully!")
        print(f"   - Agents: {len(crew.agents)}")
        print(f"   - Tasks: {len(crew.tasks)}")
        
        # Test inputs with sample CSM lists to review
        sample_csm_lists = """
        Result: {
        "CSMs": [
            {
            "Name": "Mohan Phansalkar",
            "Email": "compliance@longtailalpha.com",
            "Phone": "(949) 706-6693",
            "Title": "Chief Legal Officer",
            "Department": "Legal and Compliance",
            "Company": "Alpha LongTail LLC",
            "origin": "ADV Form, Page x",
            "reason": "Holds a key executive position with decision-making authority."
            },
            {
            "Name": "Linda Chang",
            "Email": "not provided",
            "Phone": "not provided",
            "Title": "Vice President, Portfolio Management and Trading",
            "Department": "Investment",
            "Company": "Alpha LongTail LLC",
            "origin": "Company Website",
            "reason": "Integral to investment management and trading activities."
            },
            {
            "Name": "Andrew Sawyer",
            "Email": "not provided",
            "Phone": "not provided",
            "Title": "Senior Advisor",
            "Department": "Advisory",
            "Company": "Alpha LongTail LLC",
            "origin": "Company Biography",
            "reason": "Serves as an advisor with significant influence in strategic decisions."
            },
            {
            "Name": "Benjamin Kelly",
            "Email": "not provided",
            "Phone": "not provided",
            "Title": "Senior Advisor",
            "Department": "Advisory",
            "Company": "Alpha LongTail LLC",
            "origin": "Company Biography",
            "reason": "Has extensive experience and influence in financial services."
            }
        ],
        "non-CSM Senior Officers": [
            {
            "Name": "Jayaditya (Jay) Maliye",
            "Email": "not provided",
            "Phone": "not provided",
            "Title": "Operations and Portfolio Management Analyst",
            "Department": "Operations",
            "Company": "Alpha LongTail LLC",
            "origin": "Company Biography",
            "reason": "Does not hold executive powers or decision-making authority."
            },
            {
            "Name": "Dennis Blyashov",
            "Email": "not provided",
            "Phone": "not provided",
            "Title": "Client Services Associate",
            "Department": "Client Services",
            "Company": "Alpha LongTail LLC",
            "origin": "Company Biography",
            "reason": "An associate primarily focusing on servicing client accounts."
            }
        ]
        }
        """
        
        inputs = {
            "client": "Alpha LongTail LLC",
            "csm_lists": sample_csm_lists
        }
        
        print(f"\n🔍 Testing with client: {inputs['client']}")
        print("Starting crew execution...")
        
        # Run the crew
        result = crew.kickoff(inputs=inputs)
        
        print("\n✅ Crew execution completed!")
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        
        # Check if result has the expected structure
        if hasattr(result, 'pydantic'):
            pydantic_result = result.pydantic
            print(f"\n📊 Structured Output:")
            print(f"   - Valid: {pydantic_result.valid}")
            print(f"   - Feedback: {pydantic_result.feedback}")
        
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
    print("CSM Review Crew Test")
    print("=" * 60)
    
    success = test_csm_review_crew()
    
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
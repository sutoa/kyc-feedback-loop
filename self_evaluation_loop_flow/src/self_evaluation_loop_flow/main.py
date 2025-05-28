#!/usr/bin/env python
from random import randint
from typing import Optional

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router

from self_evaluation_loop_flow.crews.poem_crew.poem_crew import PoemCrew

from self_evaluation_loop_flow.crews.csm_researcher_crew.csm_researcher_crew import CsmResearcherCrew

from self_evaluation_loop_flow.crews.csm_review_crew.csm_review_crew import CsmReviewCrew

class CSMReviewState(BaseModel):
    sentence_count: int = 1
    csm_report: str = ""
    feedback: Optional[str] = None
    retry_count: int = 0
    valid: bool = False


class CSMReviewFlow(Flow[CSMReviewState]):

    @start("retry")
    def generate_CSM_list(self):
        print("Generating the list of CSMs from different data sources. ")
        # TODO: ADD CSM researcher crew
        CsmResearcherCrew().crew().kickoff(
            inputs={
                "client": "Alpha LongTail LLC",
                "feedback": self.state.feedback
            },
        )

    @router(generate_CSM_list)
    def review_CSM_list(self):
        print("Reviewing the list of CSMs produced by ")
        # TODO: ADD CSM reviewer crew
        # 1. completed
        # 2. max_retries_exceeded
        # 3. retry
        pass

    @listen("completed")
    def save_CSM_list(self):
        print("Saving the list of CSMs")
        # TODO: save
        pass

    @listen("max_retries_exceeded")
    def handle_max_retries_exceeded(self):
        print("Exit on Failure: Max retries exceeded")
        # TODO: Exit
        pass


def kickoff():
    poem_flow = CSMReviewFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = CSMReviewFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()

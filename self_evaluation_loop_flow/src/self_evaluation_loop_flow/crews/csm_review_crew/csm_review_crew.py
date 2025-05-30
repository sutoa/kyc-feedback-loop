from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Optional
from pydantic import BaseModel

class CsmReviewOutput(BaseModel):
    valid: bool
    feedback: Optional[str] = None


@CrewBase
class CsmReviewCrew():
    """CsmReviewCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    

    @agent
    def csm_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['csm_reviewer'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def csm_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['csm_review_task'], # type: ignore[index]
            output_pydantic=CsmReviewOutput,
        )


    @crew
    def crew(self) -> Crew:
        """Creates the CsmReviewCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

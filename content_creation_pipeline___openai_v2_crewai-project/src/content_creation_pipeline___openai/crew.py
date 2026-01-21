import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool,
	SerplyScholarSearchTool
)





@CrewBase
class ContentCreationPipelineOpenAICrew:
    """ContentCreationPipelineOpenAI crew"""

    
    @agent
    def web_research_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["web_research_specialist"],
            
            
            tools=[				SerperDevTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/chatgpt-4o-latest",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def academic_research_analyst(self) -> Agent:
        
        return Agent(
            config=self.agents_config["academic_research_analyst"],
            
            
            tools=[				SerplyScholarSearchTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/chatgpt-4o-latest",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def content_strategist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["content_strategist"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/chatgpt-4o-latest",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def content_writer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["content_writer"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/chatgpt-4o-latest",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def quality_reviewer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["quality_reviewer"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/chatgpt-4o-latest",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def web_research(self) -> Task:
        return Task(
            config=self.tasks_config["web_research"],
            markdown=False,
            
            
        )
    
    @task
    def academic_research(self) -> Task:
        return Task(
            config=self.tasks_config["academic_research"],
            markdown=False,
            
            
        )
    
    @task
    def content_strategy_development(self) -> Task:
        return Task(
            config=self.tasks_config["content_strategy_development"],
            markdown=False,
            
            
        )
    
    @task
    def content_creation(self) -> Task:
        return Task(
            config=self.tasks_config["content_creation"],
            markdown=False,
            
            
        )
    
    @task
    def quality_review_and_final_approval(self) -> Task:
        return Task(
            config=self.tasks_config["quality_review_and_final_approval"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the ContentCreationPipelineOpenAI crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            chat_llm=LLM(model="gpt-4o"),
            
        )



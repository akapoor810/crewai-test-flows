#!/usr/bin/env python
from random import randint
from datetime import datetime

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from complex_demo_flow.crews.poem_crew.poem_crew import PoemCrew
from research_crew.crew import ResearchCrew
from writing_crew.crew import WritingCrew
from review_crew.crew import ReviewCrew


class ComplexFlowState(BaseModel):
    topic: str = "AI LLMs"
    current_year: str = str(datetime.now().year)
    research_report: str = ""
    writing_report: str = ""
    review_report: str = ""
    sentence_count: int = 1
    poem: str = ""


class PoemState(BaseModel):
    sentence_count: int = 1
    poem: str = ""


class ComplexDemoFlow(Flow[ComplexFlowState]):
    """
    A complete flow that orchestrates all four crews:
    1. ResearchCrew - conducts research on a topic
    2. WritingCrew - writes content based on research
    3. ReviewCrew - reviews the written content
    4. PoemCrew - creates a poem about the topic
    """

    @start()
    def research_phase(self, crewai_trigger_payload: dict = None):
        """Phase 1: Research the topic"""
        print(f"Starting research phase on topic: {self.state.topic}")

        # Use trigger payload if available
        if crewai_trigger_payload:
            self.state.topic = crewai_trigger_payload.get('topic', self.state.topic)
            self.state.current_year = crewai_trigger_payload.get('current_year', self.state.current_year)
            print(f"Using trigger payload: {crewai_trigger_payload}")

        result = (
            ResearchCrew()
            .crew()
            .kickoff(inputs={
                "topic": self.state.topic,
                "current_year": self.state.current_year
            })
        )

        print(f"Research phase completed")
        self.state.research_report = result.raw

    @listen(research_phase)
    def writing_phase(self):
        """Phase 2: Write content based on research"""
        print(f"Starting writing phase")

        result = (
            WritingCrew()
            .crew()
            .kickoff(inputs={
                "topic": self.state.topic,
                "current_year": self.state.current_year
            })
        )

        print(f"Writing phase completed")
        self.state.writing_report = result.raw

    @listen(writing_phase)
    def review_phase(self):
        """Phase 3: Review the written content"""
        print(f"Starting review phase")

        result = (
            ReviewCrew()
            .crew()
            .kickoff(inputs={
                "topic": self.state.topic,
                "current_year": self.state.current_year
            })
        )

        print(f"Review phase completed")
        self.state.review_report = result.raw

    @listen(review_phase)
    def generate_sentence_count(self):
        """Phase 4a: Generate sentence count for poem"""
        print("Generating sentence count for poem")
        self.state.sentence_count = randint(1, 5)
        print(f"Poem will have {self.state.sentence_count} sentences")

    @listen(generate_sentence_count)
    def poem_phase(self):
        """Phase 4b: Create a poem about the topic"""
        print(f"Starting poem phase")

        result = (
            PoemCrew()
            .crew()
            .kickoff(inputs={"sentence_count": self.state.sentence_count})
        )

        print(f"Poem phase completed")
        self.state.poem = result.raw

    @listen(poem_phase)
    def save_outputs(self):
        """Save all outputs to files"""
        print("Saving all outputs to files")

        with open("research_report.md", "w") as f:
            f.write(self.state.research_report)

        with open("writing_report.md", "w") as f:
            f.write(self.state.writing_report)

        with open("review_report.md", "w") as f:
            f.write(self.state.review_report)

        with open("poem.txt", "w") as f:
            f.write(self.state.poem)

        print("All outputs saved successfully")


class PoemFlow(Flow[PoemState]):

    @start()
    def generate_sentence_count(self, crewai_trigger_payload: dict = None):
        print("Generating sentence count")

        # Use trigger payload if available
        if crewai_trigger_payload:
            # Example: use trigger data to influence sentence count
            self.state.sentence_count = crewai_trigger_payload.get('sentence_count', randint(1, 5))
            print(f"Using trigger payload: {crewai_trigger_payload}")
        else:
            self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_poem(self):
        print("Generating poem")
        result = (
            PoemCrew()
            .crew()
            .kickoff(inputs={"sentence_count": self.state.sentence_count})
        )

        print("Poem generated", result.raw)
        self.state.poem = result.raw

    @listen(generate_poem)
    def save_poem(self):
        print("Saving poem")
        with open("poem.txt", "w") as f:
            f.write(self.state.poem)


def kickoff():
    """Run the complete flow with all four crews"""
    flow = ComplexDemoFlow()
    flow.kickoff()


def kickoff_poem_only():
    """Run only the poem flow (original behavior)"""
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    """Plot the complete flow"""
    flow = ComplexDemoFlow()
    flow.plot()


def plot_poem_only():
    """Plot only the poem flow"""
    poem_flow = PoemFlow()
    poem_flow.plot()


def run_with_trigger():
    """
    Run the complete flow with trigger payload.
    """
    import json
    import sys

    # Get trigger payload from command line argument
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    # Create flow and kickoff with trigger payload
    # The @start() methods will automatically receive crewai_trigger_payload parameter
    flow = ComplexDemoFlow()

    try:
        result = flow.kickoff({"crewai_trigger_payload": trigger_payload})
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the flow with trigger: {e}")


def run_poem_with_trigger():
    """
    Run only the poem flow with trigger payload (original behavior).
    """
    import json
    import sys

    # Get trigger payload from command line argument
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    # Create flow and kickoff with trigger payload
    poem_flow = PoemFlow()

    try:
        result = poem_flow.kickoff({"crewai_trigger_payload": trigger_payload})
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the flow with trigger: {e}")


if __name__ == "__main__":
    kickoff()

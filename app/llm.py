from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


def is_docker():
    try:
        with open("/proc/self/cgroup", "r") as f:
            return any("docker" in line for line in f)
    except FileNotFoundError:
        return False

class TrendsToStory:
    def __init__(self):
        if is_docker():
            self.llm = ChatOllama(base_url="http://host.docker.internal:11434", model="llama3.2:3b", temperature=0.5)
        else:
            self.llm = ChatOllama(model="llama3.2:3b", temperature=0.5)
        self.prompt = PromptTemplate(
            input_variables=["trends", "theme"],
            template = """
                You are a creative writer tasked with crafting a short story in the style of a {theme} tale.

                Below are the trending topics from the past 24 hours. Your job is to subtly weave their essence, themes, or events into a fictional narrative. Do **not** list them as-is — instead, use them as **inspiration** for characters, situations, or plot twists. Think beyond the headlines and consider the underlying human stories or societal shifts they represent.

                Trending Topics:
                {trends}

                Guidelines:
                - Immerse the reader in a natural and engaging storytelling experience.
                - The tone must resonate deeply with the selected theme: {theme}, evoking its characteristic mood and atmosphere.
                - Unleash your imagination! Employ metaphors, symbolism, and even satire to add layers of meaning and intrigue.
                - Skillfully integrate the trends so they feel organic to the story, not like a forced summary of recent news.
                - Craft a narrative that is concise yet emotionally resonant or humorously sharp, leaving a lasting impression.

                Begin the story below:
            """,
        )

        self.chain = self.prompt | self.llm

    async def generate_story(self, trends: str, theme: str) -> str:
        # Create a dictionary with the input variables
        inputs = {"trends": trends, "theme": theme}

        # Run the chain and get the result
        result = await self.chain.ainvoke(inputs)

        return result.content if hasattr(result, "content") else str(result)

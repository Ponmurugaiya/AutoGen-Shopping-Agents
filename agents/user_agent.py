from autogen_agentchat.agents import BaseChatAgent
from memory import PersistentMemory
from utils import parse_intent_entities

class UserAgent(BaseChatAgent):
    def __init__(self, name, description, memory_file, user_queue):
        super().__init__(name=name, description=description)
        self.memory = PersistentMemory(memory_file)
        self.user_queue = user_queue

    def produced_message_types(self):
        return ["text"]

    async def on_messages(self, messages, *args, **kwargs):
        latest = messages[-1]["content"]
        intent, entities = parse_intent_entities(latest)
        self.memory.set("last_query", latest)
        self.memory.set("last_intent", intent)
        self.memory.set("last_entities", entities)

        history = self.memory.get("history", [])
        history.append(latest)
        self.memory.set("history", history)

        print(f"[UserAgent] Query: '{latest}' | Intent: {intent} | Entities: {entities}")
        await self.user_queue.put(latest)
        return {"type": "text", "content": latest}

    async def on_reset(self, *args, **kwargs):
        self.memory.memory.clear()
        self.memory.save()

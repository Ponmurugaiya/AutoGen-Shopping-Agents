from autogen_agentchat.agents import BaseChatAgent
from memory import PersistentMemory
from utils import aggregate_results

class AggregatorAgent(BaseChatAgent):
    def __init__(self, name, description, memory_file):
        super().__init__(name=name, description=description)
        self.memory = PersistentMemory(memory_file)

    def produced_message_types(self):
        return ["text"]

    async def aggregate(self, user_mem, search_results):
        intent = user_mem.get("last_intent", "search")
        entities = user_mem.get("last_entities", {})
        amazon_res, flipkart_res, ebay_res = search_results

        all_results = [amazon_res, flipkart_res, ebay_res]

        if intent == "filter_store" and "store_name" in entities:
            store = entities["store_name"]
            all_results = [search_results[["Amazon","Flipkart","eBay"].index(store)]]

        memory_filter = {}
        if intent == "filter_price" and "max_price" in entities:
            memory_filter["max_price"] = entities["max_price"]

        final_results = aggregate_results(all_results, memory_filter)
        self.memory.set("final", final_results)
        print("[AggregatorAgent] Final Recommendations:", final_results)
        return final_results

    async def on_messages(self, messages, user_mem, search_results, *args, **kwargs):
        return await self.aggregate(user_mem, search_results)

    async def on_reset(self, *args, **kwargs):
        self.memory.memory.pop("final", None)
        self.memory.save()

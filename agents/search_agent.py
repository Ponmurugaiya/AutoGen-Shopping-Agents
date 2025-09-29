import asyncio
from autogen_agentchat.agents import BaseChatAgent
from memory import PersistentMemory
from utils import search_store

class SearchAgent(BaseChatAgent):
    def __init__(self, name, description, memory_file, user_queue, search_queue):
        super().__init__(name=name, description=description)
        self.memory = PersistentMemory(memory_file)
        self.user_queue = user_queue
        self.search_queue = search_queue

    def produced_message_types(self):
        return ["text"]

    async def on_messages(self, messages, *args, **kwargs):
        query = messages[-1]["content"]
        results = await self.run_searches_parallel(query)
        await self.search_queue.put(results)
        print(f"[SearchAgent] Search completed for query: {query}")
        return results

    async def on_reset(self, *args, **kwargs):
        for store in ["amazon", "flipkart", "ebay"]:
            self.memory.memory.pop(store, None)
        self.memory.save()

    async def run_searches_parallel(self, query):
        amazon_task = asyncio.create_task(self.search_store_name("Amazon", query))
        flipkart_task = asyncio.create_task(self.search_store_name("Flipkart", query))
        amazon_res, flipkart_res = await asyncio.gather(amazon_task, flipkart_task)

        total_len = len(amazon_res) + len(flipkart_res)
        ebay_res = []
        if total_len < 4:
            ebay_res = await self.search_store_name("eBay", query)
        else:
            self.memory.set("ebay", [])
        return amazon_res, flipkart_res, ebay_res

    async def search_store_name(self, store, query):
        results = self.memory.get(store.lower())
        if not results:
            results = search_store(store, query)
            self.memory.set(store.lower(), results)
        print(f"[SearchAgent] {store} results:", results)
        return results or []

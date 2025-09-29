import re
from config import PRODUCT_DB

def search_store(store, query):
    return [
        f"{p['name']} - ${p['price']}"
        for p in PRODUCT_DB.get(store, [])
        if query.lower() in p['name'].lower()
    ]

def parse_intent_entities(query):
    query_lower = query.lower()
    intent = "search"
    entities = {}
    if "cheaper" in query_lower or "below" in query_lower or "under" in query_lower:
        intent = "filter_price"
        match = re.search(r"\$(\d+)", query)
        entities["max_price"] = int(match.group(1)) if match else 55
    for store in ["amazon", "flipkart", "ebay"]:
        if store in query_lower:
            intent = "filter_store"
            entities["store_name"] = store.capitalize()
    return intent, entities

def aggregate_results(results_list, memory_filter=None):
    combined = []
    for res in results_list:
        if res is None:
            res = []
        combined.extend(res)
    if memory_filter and "max_price" in memory_filter:
        combined = [
            item for item in combined
            if int(item.split("$")[1]) <= memory_filter["max_price"]
        ]
    combined.sort(key=lambda x: int(x.split("$")[1]))
    return combined[:5]

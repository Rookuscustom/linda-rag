from typing import List


class Retriever:
  def __init__(self, vector_store):
    self.vs = vector_store
  
  
  def retrieve(self, query: str, brand_id: str | None = None, top_k: int = 6):
    filter_payload = {'brand_id': brand_id} if brand_id else None
    results = self.vs.search(query, top_k=top_k, filter_payload=filter_payload)
    # transform results to simple dicts
    docs = []
    for r in results:
      docs.append({'id': r.id, 'score': r.score, 'text': r.payload.get('text'), 'payload': r.payload})
    return docs

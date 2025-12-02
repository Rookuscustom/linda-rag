from fastapi import FastAPI, HTTPException
from app.schemas import GenerateRequest
from app.ingest import ingest_file
from app.generator import Generator
from app.retriever import Retriever
from app.vector_store import VectorStore


app = FastAPI(title='Linda RAG API')


vs = VectorStore()
emb = vs # VectorStore uses same embedder wrapper internally
retriever = Retriever(vector_store=vs)
generator = Generator(retriever=retriever)


@app.post('/v1/ingest')
async def ingest_endpoint(file_path: str, brand_id: str):
# simple demo ingest; in prod accept file upload and async process
job = ingest_file(file_path=file_path, brand_id=brand_id, vector_store=vs)
return {"status":"ok","ingested_chunks": job}


@app.post('/v1/generate')
async def generate_endpoint(req: GenerateRequest):
try:
result = generator.generate(req)
return result
except Exception as e:
raise HTTPException(status_code=500, detail=str(e))

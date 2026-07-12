from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from backend.graph.context import GraphContextBuilder
from backend.graph.store import KnowledgeGraph
from backend.ontology.manager import OntologyManager


app = FastAPI(
    title="Semantic-Translator API",
    version="0.6.0",
    description="Semantic translator with vector memory, RAG, LLM and knowledge graph",
)

graph = KnowledgeGraph()
ontology_manager = OntologyManager(graph)
graph_context = GraphContextBuilder(graph)


class GraphNodeRequest(BaseModel):
    semantic_id: str
    domain: str = "common"
    labels: dict[str, str]
    aliases: dict[str, list[str]] = {}
    definition: str = ""
    metadata: dict = {}


class GraphRelationRequest(BaseModel):
    source_id: str
    relation_type: str
    target_id: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: dict = {}
    relation_id: str | None = None


class GraphSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    domain: str = "auto"
    top_k: int = Field(default=10, ge=1, le=100)


class GraphNeighborsRequest(BaseModel):
    semantic_id: str
    relation_type: str | None = None
    direction: str = "both"


class GraphPathRequest(BaseModel):
    source_id: str
    target_id: str
    max_depth: int = Field(default=6, ge=1, le=20)


class OntologyImportRequest(BaseModel):
    path: str


@app.get("/")
def root() -> dict:
    return {
        "project": "Semantic-Translator",
        "version": "0.6.0",
        "vector_search": True,
        "rag": True,
        "translation_memory": True,
        "llm_orchestration": True,
        "knowledge_graph": True,
    }


@app.post("/graph/node")
def graph_add_node(payload: GraphNodeRequest) -> dict:
    node = graph.add_node(
        semantic_id=payload.semantic_id,
        domain=payload.domain,
        labels=payload.labels,
        aliases=payload.aliases,
        definition=payload.definition,
        metadata=payload.metadata,
    )
    return {"status": "saved", "node": node.__dict__}


@app.post("/graph/relation")
def graph_add_relation(payload: GraphRelationRequest) -> dict:
    relation = graph.add_relation(
        source_id=payload.source_id,
        relation_type=payload.relation_type,
        target_id=payload.target_id,
        confidence=payload.confidence,
        metadata=payload.metadata,
        relation_id=payload.relation_id,
    )
    return {"status": "saved", "relation": relation.__dict__}


@app.post("/graph/search")
def graph_search(payload: GraphSearchRequest) -> dict:
    domain = None if payload.domain == "auto" else payload.domain
    results = graph.search(payload.query, domain=domain, top_k=payload.top_k)
    return {"query": payload.query, "count": len(results), "results": results}


@app.post("/graph/neighbors")
def graph_neighbors(payload: GraphNeighborsRequest) -> dict:
    results = graph.neighbors(
        semantic_id=payload.semantic_id,
        relation_type=payload.relation_type,
        direction=payload.direction,
    )
    return {
        "semantic_id": payload.semantic_id,
        "count": len(results),
        "neighbors": results,
    }


@app.post("/graph/path")
def graph_path(payload: GraphPathRequest) -> dict:
    path = graph.shortest_path(
        payload.source_id,
        payload.target_id,
        max_depth=payload.max_depth,
    )
    return {
        "source_id": payload.source_id,
        "target_id": payload.target_id,
        "length": len(path),
        "path": path,
    }


@app.get("/graph/status")
def graph_status() -> dict:
    return graph.status()


@app.post("/graph/export")
def graph_export() -> dict:
    return graph.export()


@app.post("/ontology/import")
def ontology_import(payload: OntologyImportRequest) -> dict:
    result = ontology_manager.import_json(Path(payload.path))
    return {"status": "imported", **result}


@app.post("/ontology/validate")
def ontology_validate() -> dict:
    return ontology_manager.validate()

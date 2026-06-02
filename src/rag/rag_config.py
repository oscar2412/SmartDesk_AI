import yaml
import os

_config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yaml')
with open(_config_path, 'r') as _f:
    _cfg = yaml.safe_load(_f)

_rag = _cfg['rag']

CHUNK_SIZE             = _rag['chunk_size']
CHUNK_OVERLAP          = _rag['chunk_overlap']
TOP_K_RESULTS          = _rag['top_k_results']
CONFIDENCE_THRESHOLD   = _rag['confidence_threshold']
EMBEDDING_MODEL        = _rag['embedding_model']
LLM_MODEL              = _rag['llm_model']
CHROMA_DB_PATH         = _rag['chroma_db_path']
CHROMA_COLLECTION_NAME = _rag['chroma_collection_name']

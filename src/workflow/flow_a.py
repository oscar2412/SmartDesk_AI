from src.rag.rag_chain import get_rag_answer, format_sources, ANSWER_FOUND
from src.utils.helpers import build_api_error_response


def handle_kb_query(message: str, session: dict) -> str:
    """
    Flow A — Knowledge base query.
    If RAG finds an answer returns it.
    If not found escalates to Flow B ticket creation.
    """
    try:
        rag_result = get_rag_answer(message)

        if rag_result["status"] == ANSWER_FOUND:
            answer  = rag_result["answer"]
            sources = format_sources(rag_result["sources"])
            response = answer
            if sources:
                response += f"\n\n{sources}"
            return response

        else:
            session["original_query"] = message
            from src.workflow.flow_b import handle_ticket_creation_start
            return handle_ticket_creation_start(session)

    except Exception as e:
        print(f"  [Agent] RAG error: {str(e)}")
        return build_api_error_response("the knowledge base")

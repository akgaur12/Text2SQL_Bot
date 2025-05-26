from src.pipeline import sql_query_pipeline
from llama_index.core.base.llms.types import ChatResponse


def run_text2sql_api(query_str):
    """Run the API using the provided query string."""
    response = sql_query_pipeline.run(query_str=query_str)

    if isinstance(response, ChatResponse):
        return {"message": response.message.content}
    else:
        try:
            return {"message": response[0].message.content}
        except:
            return {"message": response[0]}


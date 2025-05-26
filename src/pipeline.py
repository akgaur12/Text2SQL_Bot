from llama_index.core.query_pipeline import FnComponent
from llama_index.core.query_pipeline import  QueryPipeline, InputComponent, Link

from src.settings import table_retriever, llm
from src.prompt import (
    sql_llm_prompt_function,
    final_response_prompt
)

from src.pipeline_modules import (
    get_sqltable_info, 
    extract_sql_query_from_response,
    execute_sql_query,
)

# Define functional components for the pipeline
get_table_info_component = FnComponent(fn=get_sqltable_info)
text2sql_prompt = FnComponent(fn=sql_llm_prompt_function)
sql_query_fetcher = FnComponent(fn=extract_sql_query_from_response)
sql_query_executor = FnComponent(fn=execute_sql_query)
response_prompt = FnComponent(fn=final_response_prompt)


# Create the query pipeline with defined modules
sql_query_pipeline = QueryPipeline(
    modules={
        "input": InputComponent(),
        "fetch_table_name": table_retriever,
        "get_table_info": get_table_info_component,
        "text2sql_prompt": text2sql_prompt,
        "text2sql_llm": llm,
        "sql_query_fetcher": sql_query_fetcher,
        "sql_query_executor": sql_query_executor,
        "response_prompt": response_prompt,
        "response_llm": llm,
    }, 
    verbose=True
)

# Define the flow of data between components
sql_query_pipeline.add_links([
    Link("input", "fetch_table_name"),
    Link("fetch_table_name", "get_table_info", dest_key="table_schema_objs"),
    Link("input", "text2sql_prompt", dest_key="query_str"),
    Link("get_table_info", "text2sql_prompt", dest_key="schema"),
    Link("text2sql_prompt", "text2sql_llm"),
    Link("text2sql_llm", "sql_query_fetcher", dest_key="response"),
    Link("sql_query_fetcher", "sql_query_executor", dest_key="sql_query"),

    Link("input", "response_prompt", dest_key="query_str"),
    Link("sql_query_fetcher", "response_prompt", dest_key="sql_query"),
    Link("sql_query_executor", "response_prompt", dest_key="data"),

    Link("response_prompt", "response_llm"),
])


# # Create a graph visualization of the pipeline
# from pyvis.network import Network
# net = Network(notebook=True, cdn_resources="in_line", directed=True)
# net.from_nx(sql_query_pipeline.dag)
# net.show("sql_query_pipeline.html")
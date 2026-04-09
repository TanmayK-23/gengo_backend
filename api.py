from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import execute_read_only_query
from validator import is_safe_select, format_sql
from prompts import build_prompt, build_correction_prompt
from llm_caller import call_llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    use_fallback: bool = False

def clean_sql_output(sql):
    sql = sql.strip()

    # Remove markdown
    if "```" in sql:
        sql = sql.split("```")[1]

    # Remove leading text before SELECT
    sql = sql.upper().split("SELECT", 1)[-1]
    sql = "SELECT " + sql

    # Remove semicolon issues
    sql = sql.split(";")[0] + ";"

    return sql

@app.post("/query")
def query(req: QueryRequest):
    prompt = build_prompt(req.question)
    sql = call_llm(prompt, req.use_fallback)
    sql = clean_sql_output(sql)

    if not is_safe_select(sql):
        return {"error": "Unsafe query"}

    try:
        rows, cols, time_taken, suggestion = execute_read_only_query(sql)
    except Exception as e:
        # self-correct once
        fix_prompt = build_correction_prompt(sql, str(e))
        sql = call_llm(fix_prompt, req.use_fallback)
        sql = clean_sql_output(sql)

        if not is_safe_select(sql):
            return {"error": "Unsafe corrected query"}

        try:
            rows, cols, time_taken, suggestion = execute_read_only_query(sql)
        except Exception as e2:
            return {"error": str(e2)}

    return {
        "sql": format_sql(sql),
        "results": rows,
        "columns": cols,
        "execution_time_ms": round(time_taken * 1000, 2),
        "suggestion": suggestion,
        "error": None
    }
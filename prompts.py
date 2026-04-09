from db import get_schema_info, get_foreign_keys

def get_dynamic_schema_description():
    schema = get_schema_info()

    desc = "Tables:\n"
    for table, cols in schema.items():
        desc += f"{table}({', '.join(cols)})\n"

    desc += "\nRelationships:\n"
    relationships = get_foreign_keys()
    if relationships:
        for rel in relationships:
            desc += f"{rel}\n"
    else:
        desc += "None specifically defined, rely on column naming conventions.\n"

    return desc
def build_prompt(question):
    return f"""
You are an expert SQL generator.

Rules:
- Only generate SELECT queries
- Use correct joins
- Use table aliases
- Output ONLY raw SQL starting with SELECT
- Do not include any text before or after the SQL query
- Use LIMIT when user asks for top results

Schema:
{get_dynamic_schema_description()}

Examples:

Q: Show all customers
SQL: SELECT * FROM cust_mast;

Q: Total orders per customer
SQL:
SELECT c.cust_name, COUNT(*) 
FROM ord_hist o
JOIN cust_mast c ON o.cust_id = c.cust_id
GROUP BY c.cust_name;

User Question:
{question}

SQL:
"""

def build_correction_prompt(sql, error):
    return f"""
Fix this SQL query.

Error:
{error}

SQL:
{sql}

Return ONLY corrected SQL.
"""

def build_explanation_prompt(sql):
    return f"Explain this SQL query simply:\n{sql}"
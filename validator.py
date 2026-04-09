import sqlparse

BLACKLIST = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE"]

def is_safe_select(sql):
    sql_upper = sql.upper().strip()

    if not sql_upper.startswith("SELECT"):
        return False

    for keyword in BLACKLIST:
        if keyword in sql_upper:
            return False

    return True

def format_sql(sql):
    return sqlparse.format(sql, reindent=True, keyword_case="upper")
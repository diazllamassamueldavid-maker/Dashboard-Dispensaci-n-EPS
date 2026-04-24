import sqlite3
import pandas as pd

DB_PATH = 'medicamentos.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def execute_query(query, params=None):
    conn = get_connection()
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

def get_kpis(grupo_fco=None, año=None, mes=None, regional=None):
    base_query = "SELECT COUNT(DISTINCT id) as total_personas, COUNT(DISTINCT formula) as total_formulas, SUM(costo_total)/COUNT(DISTINCT formula) as costo_promedio FROM dispensacion WHERE 1=1"
    params = []
    
    if grupo_fco:
        base_query += " AND grupo_fco_economico = ?"
        params.append(grupo_fco)
    if año:
        base_query += " AND strftime('%Y', fecha_entrega) = ?"
        params.append(año)
    if mes:
        base_query += " AND strftime('%m', fecha_entrega) = ?"
        params.append(mes)
    if regional:
        base_query += " AND regional_caf = ?"
        params.append(regional)
        
    return execute_query(base_query, params)

def get_dispensacion_tiempo(grupo_fco=None, año=None, mes=None, regional=None):
    base_query = "SELECT strftime('%Y-%m', fecha_entrega) as mes_año, COUNT(*) as dispensaciones FROM dispensacion WHERE 1=1"
    params = []
    
    if grupo_fco:
        base_query += " AND grupo_fco_economico = ?"
        params.append(grupo_fco)
    if año:
        base_query += " AND strftime('%Y', fecha_entrega) = ?"
        params.append(año)
    if mes:
        base_query += " AND strftime('%m', fecha_entrega) = ?"
        params.append(mes)
    if regional:
        base_query += " AND regional_caf = ?"
        params.append(regional)
    
    base_query += " GROUP BY mes_año ORDER BY mes_año"
    return execute_query(base_query, params)

def get_top_medicamentos_costo(grupo_fco=None, año=None, mes=None, regional=None, limit=10):
    base_query = "SELECT descripcion, SUM(costo_total) as costo_total FROM dispensacion WHERE 1=1"
    params = []
    
    if grupo_fco:
        base_query += " AND grupo_fco_economico = ?"
        params.append(grupo_fco)
    if año:
        base_query += " AND strftime('%Y', fecha_entrega) = ?"
        params.append(año)
    if mes:
        base_query += " AND strftime('%m', fecha_entrega) = ?"
        params.append(mes)
    if regional:
        base_query += " AND regional_caf = ?"
        params.append(regional)
        
    base_query += f" GROUP BY descripcion ORDER BY costo_total DESC LIMIT {limit}"
    return execute_query(base_query, params)

def get_costo_pbs(grupo_fco=None, año=None, mes=None, regional=None):
    base_query = "SELECT pbs, SUM(costo_total) as costo_total FROM dispensacion WHERE 1=1"
    params = []
    
    if grupo_fco:
        base_query += " AND grupo_fco_economico = ?"
        params.append(grupo_fco)
    if año:
        base_query += " AND strftime('%Y', fecha_entrega) = ?"
        params.append(año)
    if mes:
        base_query += " AND strftime('%m', fecha_entrega) = ?"
        params.append(mes)
    if regional:
        base_query += " AND regional_caf = ?"
        params.append(regional)
        
    base_query += " GROUP BY pbs"
    return execute_query(base_query, params)

def get_costo_municipio(grupo_fco=None, año=None, mes=None, regional=None):
    base_query = "SELECT municipio_caf, SUM(costo_total) as costo_total FROM dispensacion WHERE municipio_caf IS NOT NULL AND municipio_caf != '0'"
    params = []
    
    if grupo_fco:
        base_query += " AND grupo_fco_economico = ?"
        params.append(grupo_fco)
    if año:
        base_query += " AND strftime('%Y', fecha_entrega) = ?"
        params.append(año)
    if mes:
        base_query += " AND strftime('%m', fecha_entrega) = ?"
        params.append(mes)
    if regional:
        base_query += " AND regional_caf = ?"
        params.append(regional)
        
    base_query += " GROUP BY municipio_caf ORDER BY costo_total DESC"
    return execute_query(base_query, params)

def get_costo_tipo_entrega(grupo_fco=None, año=None, mes=None, regional=None):
    base_query = "SELECT tipo_entrega, SUM(costo_total) as costo_total FROM dispensacion WHERE 1=1"
    params = []
    
    if grupo_fco:
        base_query += " AND grupo_fco_economico = ?"
        params.append(grupo_fco)
    if año:
        base_query += " AND strftime('%Y', fecha_entrega) = ?"
        params.append(año)
    if mes:
        base_query += " AND strftime('%m', fecha_entrega) = ?"
        params.append(mes)
    if regional:
        base_query += " AND regional_caf = ?"
        params.append(regional)
        
    base_query += " GROUP BY tipo_entrega ORDER BY costo_total DESC"
    return execute_query(base_query, params)

def get_filter_options():
    conn = get_connection()
    try:
        grupos = pd.read_sql_query("SELECT DISTINCT grupo_fco_economico FROM dispensacion WHERE grupo_fco_economico IS NOT NULL", conn)['grupo_fco_economico'].tolist()
        regionales = pd.read_sql_query("SELECT DISTINCT regional_caf FROM dispensacion WHERE regional_caf IS NOT NULL", conn)['regional_caf'].tolist()
        años = pd.read_sql_query("SELECT DISTINCT strftime('%Y', fecha_entrega) as anio FROM dispensacion WHERE fecha_entrega IS NOT NULL", conn)['anio'].tolist()
        meses = pd.read_sql_query("SELECT DISTINCT strftime('%m', fecha_entrega) as mes FROM dispensacion WHERE fecha_entrega IS NOT NULL", conn)['mes'].tolist()
        return grupos, regionales, sorted(años), sorted(meses)
    finally:
        conn.close()

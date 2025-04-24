from db.connection import run_query


def get_sla_tecnicos():
    return run_query("""
        SELECT
            dtec.email as Tecnico,
            COUNT(*) AS total_atendimentos,
            COUNT(*) FILTER (WHERE fct.arrival_date <= fct.deadline_date) AS atendimentos_no_prazo,
            ROUND(
                COUNT(*) FILTER (WHERE fct.arrival_date <= fct.deadline_date) * 100.0 / NULLIF(COUNT(*), 0),
                2
            ) AS sla_percent
        FROM public.fct_orders fct
        LEFT JOIN public.dim_technicians dtec ON fct.technician_id = dtec.technician_id
        GROUP BY dtec.email
        ORDER BY sla_percent DESC;
    """)


def get_sla_bases():
    return run_query("""
        SELECT
            fct.provider as base,
            COUNT(*) AS total_atendimentos,
            COUNT(*) FILTER (WHERE fct.arrival_date <= fct.deadline_date) AS atendimentos_no_prazo,
            ROUND(
                COUNT(*) FILTER (WHERE fct.arrival_date <= fct.deadline_date) * 100.0 / NULLIF(COUNT(*), 0),
                2
            ) AS sla_percent
        FROM public.fct_orders fct
        LEFT JOIN public.dim_technicians dtec ON fct.technician_id = dtec.technician_id
        GROUP BY fct.provider
        ORDER BY sla_percent DESC;
    """)


def get_produtividade():
    return run_query("""
        WITH atendimentos_por_tecnico AS (
            SELECT
                dtec.email,
                MIN(fct.arrival_date::date) AS primeiro_dia,
                MAX(fct.arrival_date::date) AS ultimo_dia,
                COUNT(*) AS total_atendimentos
            FROM public.fct_orders fct
            LEFT JOIN public.dim_technicians dtec ON fct.technician_id = dtec.technician_id
            GROUP BY dtec.email
        ),
        dias_uteis AS (
            SELECT email, COUNT(*) AS dias_uteis
            FROM (
                SELECT a.email, gs::date AS data
                FROM atendimentos_por_tecnico a,
                     generate_series(a.primeiro_dia, a.ultimo_dia, interval '1 day') gs
                WHERE EXTRACT(DOW FROM gs) BETWEEN 1 AND 5
            ) AS dias
            GROUP BY email
        )
        SELECT
            a.email as tecnico,
            a.total_atendimentos,
            d.dias_uteis,
            ROUND(a.total_atendimentos::numeric / NULLIF(d.dias_uteis, 0), 2) AS produtividade_diaria
        FROM atendimentos_por_tecnico a
        JOIN dias_uteis d ON a.email = d.email
        ORDER BY produtividade_diaria DESC;
    """)


def get_motivos_cancelamento():
    return run_query("""
        SELECT
            dcr.reason AS motivo_cancelamento,
            COUNT(*) AS total
        FROM public.fct_orders fct
        JOIN public.dim_cancellation_reasons dcr ON fct.cancellation_reason_id = dcr.id
        GROUP BY dcr.reason
        ORDER BY total DESC
        LIMIT 5;
    """)


def get_cobertura_geografica():
    return run_query("""
        SELECT
            dtec.email,
            COUNT(DISTINCT da.city) AS cidades_atendidas
        FROM public.fct_orders fct
        LEFT JOIN public.dim_technicians dtec ON fct.technician_id = dtec.technician_id
        LEFT JOIN public.dim_addresses da ON fct.address_id = da.address_id
        GROUP BY dtec.email
        ORDER BY cidades_atendidas DESC;
    """)


def get_distribuicao_terminais():
    return run_query("""
        SELECT
            dt.model,
            dt.type,
            COUNT(*) AS total_usos
        FROM public.fct_orders fct
        LEFT JOIN public.dim_terminals dt ON fct.terminal_id  = dt.terminal_id
        GROUP BY dt.model, dt.type
        ORDER BY total_usos DESC;
    """)


def get_atendimentos_por_estado():
    return run_query("""
        SELECT
            COUNT(*) as qtd_orders,
            da.country_state
        FROM public.fct_orders fct
        LEFT JOIN public.dim_technicians dtec ON fct.technician_id = dtec.technician_id
        LEFT JOIN public.dim_addresses da ON fct.address_id = da.address_id
        GROUP BY da.country_state 
        ORDER BY qtd_orders DESC;
    """)

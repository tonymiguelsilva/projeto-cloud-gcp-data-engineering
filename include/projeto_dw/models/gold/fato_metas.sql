select
    mes,
    meta_vendas
from {{ ref("stg_metas_vendas") }}

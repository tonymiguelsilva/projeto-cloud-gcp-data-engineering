{{ config(
    materialized="table",
    partition_by={
        "field": "data_pedido",
        "data_type": "date",
        "granularity": "month"
    },
    cluster_by=["cliente_id", "produto_id"]
) }}

select
    i.item_id,
    i.pedido_id,
    p.cliente_id,
    i.produto_id,
    p.data_pedido,
    p.status,
    p.valor_total,
    i.quantidade,
    i.preco_unitario,
    i.valor_item
from {{ ref("stg_itens_pedido") }} i
inner join {{ ref("stg_pedidos") }} p
    on i.pedido_id = p.pedido_id

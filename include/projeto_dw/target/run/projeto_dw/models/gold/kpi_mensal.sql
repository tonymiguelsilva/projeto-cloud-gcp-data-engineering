

  create or replace view `project-c3b69582-833e-4e2a-88c`.`gold`.`kpi_mensal`
  OPTIONS()
  as with vendas as (
    select
        date(date_trunc(data_pedido, month)) as mes,
        count(distinct pedido_id) as pedidos,
        count(distinct cliente_id) as clientes,
        sum(valor_item) as faturamento,
        sum(quantidade) as itens_vendidos
    from `project-c3b69582-833e-4e2a-88c`.`gold`.`fato_vendas`
    group by 1
),
metas as (
    select
        parse_date("%Y-%m", mes) as mes,
        meta_vendas
    from `project-c3b69582-833e-4e2a-88c`.`gold`.`fato_metas`
)
select
    v.mes,
    v.pedidos,
    v.clientes,
    v.faturamento,
    v.itens_vendidos,
    m.meta_vendas,
    safe_divide(v.faturamento, m.meta_vendas) as percentual_meta,
    safe_divide(v.faturamento, v.pedidos) as ticket_medio
from vendas v
left join metas m
    on v.mes = m.mes;


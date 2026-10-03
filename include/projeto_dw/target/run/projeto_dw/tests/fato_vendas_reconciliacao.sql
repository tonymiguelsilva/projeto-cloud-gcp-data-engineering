
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  with valores as (
    select
        pedido_id,
        round(sum(valor_item), 2) as total_itens,
        round(max(valor_total), 2) as valor_pedido
    from `project-c3b69582-833e-4e2a-88c`.`gold`.`fato_vendas`
    group by pedido_id
)
select *
from valores
where total_itens != valor_pedido
  
  
      
    ) dbt_internal_test
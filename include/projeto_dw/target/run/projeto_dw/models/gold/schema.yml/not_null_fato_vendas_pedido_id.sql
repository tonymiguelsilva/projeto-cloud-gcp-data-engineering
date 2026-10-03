
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select pedido_id
from `project-c3b69582-833e-4e2a-88c`.`gold`.`fato_vendas`
where pedido_id is null



  
  
      
    ) dbt_internal_test
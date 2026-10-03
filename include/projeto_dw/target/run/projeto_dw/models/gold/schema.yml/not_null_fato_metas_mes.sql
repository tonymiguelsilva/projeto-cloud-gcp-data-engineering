
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select mes
from `project-c3b69582-833e-4e2a-88c`.`gold`.`fato_metas`
where mes is null



  
  
      
    ) dbt_internal_test
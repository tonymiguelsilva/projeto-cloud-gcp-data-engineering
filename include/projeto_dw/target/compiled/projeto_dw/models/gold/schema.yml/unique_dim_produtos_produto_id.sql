
    
    

with dbt_test__target as (

  select produto_id as unique_field
  from `project-c3b69582-833e-4e2a-88c`.`gold`.`dim_produtos`
  where produto_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1



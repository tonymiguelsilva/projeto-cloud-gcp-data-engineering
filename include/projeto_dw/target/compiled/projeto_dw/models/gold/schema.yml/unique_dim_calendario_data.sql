
    
    

with dbt_test__target as (

  select data as unique_field
  from `project-c3b69582-833e-4e2a-88c`.`gold`.`dim_calendario`
  where data is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1



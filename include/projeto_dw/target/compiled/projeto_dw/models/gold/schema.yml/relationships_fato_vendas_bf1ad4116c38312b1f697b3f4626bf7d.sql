
    
    

with child as (
    select cliente_id as from_field
    from `project-c3b69582-833e-4e2a-88c`.`gold`.`fato_vendas`
    where cliente_id is not null
),

parent as (
    select cliente_id as to_field
    from `project-c3b69582-833e-4e2a-88c`.`gold`.`dim_clientes`
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



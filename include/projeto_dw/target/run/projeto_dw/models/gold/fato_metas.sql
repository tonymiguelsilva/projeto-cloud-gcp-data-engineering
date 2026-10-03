

  create or replace view `project-c3b69582-833e-4e2a-88c`.`gold`.`fato_metas`
  OPTIONS()
  as select
    mes,
    meta_vendas
from `project-c3b69582-833e-4e2a-88c`.`silver`.`stg_metas_vendas`;




  create or replace view `project-c3b69582-833e-4e2a-88c`.`gold`.`dim_clientes`
  OPTIONS()
  as select *
from `project-c3b69582-833e-4e2a-88c`.`silver`.`stg_clientes`;


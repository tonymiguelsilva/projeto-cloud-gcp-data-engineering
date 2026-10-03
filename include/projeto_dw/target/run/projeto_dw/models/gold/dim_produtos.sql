

  create or replace view `project-c3b69582-833e-4e2a-88c`.`gold`.`dim_produtos`
  OPTIONS()
  as select *
from `project-c3b69582-833e-4e2a-88c`.`silver`.`stg_produtos`;


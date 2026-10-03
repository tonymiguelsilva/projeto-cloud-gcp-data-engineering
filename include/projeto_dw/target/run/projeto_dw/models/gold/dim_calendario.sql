

  create or replace view `project-c3b69582-833e-4e2a-88c`.`gold`.`dim_calendario`
  OPTIONS()
  as select
    data
from unnest(
    generate_date_array(
        date("2026-01-01"),
        current_date()
    )
) as data;


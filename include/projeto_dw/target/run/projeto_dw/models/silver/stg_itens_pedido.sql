

  create or replace view `project-c3b69582-833e-4e2a-88c`.`silver`.`stg_itens_pedido`
  OPTIONS()
  as select
    item_id,
    pedido_id,
    produto_id,
    quantidade,
    preco_unitario,
    quantidade * preco_unitario as valor_item,
    updated_at
from `project-c3b69582-833e-4e2a-88c`.`bronze`.`itens_pedido`;


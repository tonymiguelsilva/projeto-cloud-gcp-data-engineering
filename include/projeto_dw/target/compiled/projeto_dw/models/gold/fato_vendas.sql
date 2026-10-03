select
    i.item_id,
    i.pedido_id,
    p.cliente_id,
    i.produto_id,
    p.data_pedido,
    p.status,
    p.valor_total,
    i.quantidade,
    i.preco_unitario,
    i.valor_item
from `project-c3b69582-833e-4e2a-88c`.`silver`.`stg_itens_pedido` i
inner join `project-c3b69582-833e-4e2a-88c`.`silver`.`stg_pedidos` p
    on i.pedido_id = p.pedido_id
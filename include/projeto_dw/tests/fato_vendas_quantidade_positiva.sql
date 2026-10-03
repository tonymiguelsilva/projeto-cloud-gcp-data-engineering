select *
from {{ ref("fato_vendas") }}
where quantidade <= 0

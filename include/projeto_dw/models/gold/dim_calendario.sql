select
    data
from unnest(
    generate_date_array(
        date("2026-01-01"),
        current_date()
    )
) as data

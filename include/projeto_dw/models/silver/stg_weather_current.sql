select * from {{ source("bronze", "weather_current") }}

{{ config(
    materialized='table',
    tags=['finance', 'core'],
    unique_key='id'
) }}

with source as (
    select * from {{ ref('stg_active_users') }}
),

transformed as (
    select
        id,
        user_id,
        amount * 100 as amount_cents,
        status,
        case 
            when status = 'paid' then amount 
            else 0 
        end as recognized_revenue,
        created_at
    from source
)

select * from transformed

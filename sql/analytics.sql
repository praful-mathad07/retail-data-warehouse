
-- Retail Sales Analytics Queries
-- Revenue = quantity * unit_price
-- Profit = quantity * (unit_price - unit_cost)

-- 1. Overall business KPIs
SELECT
    SUM(quantity * unit_price) AS total_revenue,
    SUM(quantity * unit_cost) AS total_cost,
    SUM(quantity * (unit_price - unit_cost)) AS total_profit,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS total_orders
FROM fact_sales;


-- 2. Revenue and profit by product category
SELECT
    p.category,
    SUM(f.quantity * f.unit_price) AS total_revenue,
    SUM(f.quantity * (f.unit_price - f.unit_cost)) AS total_profit,
    SUM(f.quantity) AS units_sold
FROM fact_sales AS f
JOIN dim_product AS p
    ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- 3. Monthly revenue and profit
SELECT
    d.year_number,
    d.month_number,
    d.month_name,
    SUM(f.quantity * f.unit_price) AS total_revenue,
    SUM(f.quantity * (f.unit_price - f.unit_cost)) AS total_profit
FROM fact_sales AS f
JOIN dim_date AS d
    ON f.date_key = d.date_key
GROUP BY
    d.year_number,
    d.month_number,
    d.month_name
ORDER BY
    d.year_number,
    d.month_number;


-- 4. Revenue by product
SELECT
    p.product_name,
    p.category,
    SUM(f.quantity * f.unit_price) AS total_revenue,
    SUM(f.quantity) AS units_sold
FROM fact_sales AS f
JOIN dim_product AS p
    ON f.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY total_revenue DESC;


-- 5. Revenue by customer region
SELECT
    c.region,
    SUM(f.quantity * f.unit_price) AS total_revenue,
    SUM(f.quantity * (f.unit_price - f.unit_cost)) AS total_profit,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_sales AS f
JOIN dim_customer AS c
    ON f.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_revenue DESC;

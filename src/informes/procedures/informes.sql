delimiter $$

create procedure informe_producto_ciudad_resumen()
begin
    select 
        ci.cityname as nombre,
        p.productname as producto,
        avg(p.price) as precio_promedio,
        count(sa.salesid) as cantidad_ventas,
        round((count(sa.salesid) / vt.total_cant) * 100, 2) as porcentaje_ventas_ciudad
    from sales sa
    join customers cu on sa.customerid = cu.customerid
    join cities ci on cu.cityid = ci.cityid
    join products p on sa.productid = p.productid
    join (
        select ci.cityname as ciudad, count(sa.salesid) as total_cant
        from sales sa
        join customers cu on sa.customerid = cu.customerid
        join cities ci on cu.cityid = ci.cityid
        group by ci.cityname
    ) vt on ci.cityname = vt.ciudad
    group by ci.cityname, p.productname
    order by ci.cityname, precio_promedio desc;
end $$

create procedure informe_top_clientes()
begin
    select
        cu.customerid as cliente,
        cu.firstname as nombre_cliente,
        cu.lastname as apellido_cliente,
        count(s.salesid) as cantidad_compras,
        sum(s.totalprice) as total_gastado
    from sales s
    join customers cu on s.customerid = cu.customerid
    group by cu.customerid, cu.firstname, cu.lastname
    order by total_gastado desc
    limit 10;
end $$

create procedure informe_ventas_categoria()
begin
    select 
        c.categoryname as categoria,
        count(s.salesid) as total_ventas,
        sum(s.totalprice) as total_ingresos
    from sales s
    join products p on s.productid = p.productid
    join categories c on p.categoryid = c.categoryid
    group by c.categoryname
    order by total_ingresos desc;
end $$


CREATE PROCEDURE informe_ventas()
BEGIN
    SELECT 
        salesid, 
        salespersonid, 
        customerid, 
        productid,
        quantity, 
        discount, 
        totalprice, 
        salesdate, 
        transactionnumber
    FROM sales
    ORDER BY salesdate DESC;
END $$

delimiter ;

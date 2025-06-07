delimiter $$

create trigger venta_insert
after insert on sales
for EACH row
begin
    insert into sales_log (
        SalesID, SalesPersonID, CustomerID, ProductID, Quantity, Discount, TotalPrice, SalesDate, TransactionNumber
    )
    values (
        NEW.salesid, NEW.salespersonid, NEW.customerid, NEW.productid, NEW.quantity, NEW.discount, NEW.totalprice, NEW.salesdate, NEW.transactionnumber
    );
end $$

delimiter ;

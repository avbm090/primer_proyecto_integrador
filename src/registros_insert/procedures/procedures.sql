DELIMITER //

-- Category
CREATE PROCEDURE InsertCategory(
    IN p_CategoryName VARCHAR(100),
    OUT p_ResultMessage VARCHAR(50)
)
BEGIN
    IF EXISTS (SELECT 1 FROM categories WHERE CategoryName = p_CategoryName) THEN
        SET p_ResultMessage = 'Categoría ya existe';
    ELSE
        INSERT INTO categories (CategoryName) VALUES (p_CategoryName);
        SET p_ResultMessage = 'Categoría insertada';
    END IF;
END //

-- Country
CREATE PROCEDURE InsertCountry(
    IN p_CountryName VARCHAR(100),
    IN p_CountryCode VARCHAR(10),
    OUT p_ResultMessage VARCHAR(50)
)
BEGIN
    IF EXISTS (SELECT 1 FROM countries WHERE CountryName = p_CountryName OR CountryCode = p_CountryCode) THEN
        SET p_ResultMessage = 'País ya existe';
    ELSE
        INSERT INTO countries (CountryName, CountryCode) VALUES (p_CountryName, p_CountryCode);
        SET p_ResultMessage = 'País insertado';
    END IF;
END //

-- City
CREATE PROCEDURE InsertCity(
    IN p_CityName VARCHAR(100),
    IN p_Zipcode VARCHAR(10),
    IN p_CountryID INT,
    OUT p_ResultMessage VARCHAR(50)
)
BEGIN
    IF EXISTS (SELECT 1 FROM cities WHERE CityName = p_CityName AND CountryID = p_CountryID) THEN
        SET p_ResultMessage = 'Ciudad ya existe en ese país';
    ELSE
        INSERT INTO cities (CityName, Zipcode, CountryID) VALUES (p_CityName, p_Zipcode, p_CountryID);
        SET p_ResultMessage = 'Ciudad insertada';
    END IF;
END //

-- Customer
CREATE PROCEDURE InsertCustomer(
    IN p_FirstName VARCHAR(50),
    IN p_MiddleInitial CHAR(1),
    IN p_LastName VARCHAR(50),
    IN p_CityID INT,
    IN p_Address VARCHAR(150),
    OUT p_ResultMessage VARCHAR(50)
)
BEGIN
    INSERT INTO customers (FirstName, MiddleInitial, LastName, CityID, Address) 
    VALUES (p_FirstName, p_MiddleInitial, p_LastName, p_CityID, p_Address);
    SET p_ResultMessage = 'Cliente insertado';
END //

-- Employee
CREATE PROCEDURE InsertEmployee(
    IN p_FirstName VARCHAR(50),
    IN p_MiddleInitial CHAR(1),
    IN p_LastName VARCHAR(50),
    IN p_BirthDate DATETIME,
    IN p_Gender CHAR(1),
    IN p_CityID INT,
    IN p_HireDate DATETIME,
    OUT p_ResultMessage VARCHAR(50)
)
BEGIN
    INSERT INTO employees (FirstName, MiddleInitial, LastName, BirthDate, Gender, CityID, HireDate)
    VALUES (p_FirstName, p_MiddleInitial, p_LastName, p_BirthDate, p_Gender, p_CityID, p_HireDate);
    SET p_ResultMessage = 'Empleado insertado';
END //

-- Product
CREATE PROCEDURE InsertProduct(
    IN p_ProductName VARCHAR(150),
    IN p_Price DECIMAL(10,4),
    IN p_CategoryID INT,
    IN p_Class VARCHAR(20),
    IN p_ModifyDate TIME,
    IN p_Resistant VARCHAR(20),
    IN p_IsAllergic VARCHAR(10),
    IN p_VitalityDays INT,
    OUT p_ResultMessage VARCHAR(50)
)
BEGIN
    IF EXISTS (SELECT 1 FROM products WHERE ProductName = p_ProductName AND CategoryID = p_CategoryID) THEN
        SET p_ResultMessage = 'Producto ya existe en esa categoría';
    ELSE
        INSERT INTO products (ProductName, Price, CategoryID, Class, ModifyDate, Resistant, IsAllergic, VitalityDays)
        VALUES (p_ProductName, p_Price, p_CategoryID, p_Class, p_ModifyDate, p_Resistant, p_IsAllergic, p_VitalityDays);
        SET p_ResultMessage = 'Producto insertado';
    END IF;
END //

--ventas
CREATE PROCEDURE InsertSale(
    IN p_SalesPersonName VARCHAR(100),
    IN p_CustomerName VARCHAR(100),
    IN p_ProductName VARCHAR(150),
    IN p_Quantity INT,
    IN p_Discount DECIMAL(5,2),
    IN p_TotalPrice DECIMAL(10,2),
    IN p_SalesDate TIME,
    IN p_TransactionNumber VARCHAR(50),
    OUT p_ResultMessage VARCHAR(255)
)
BEGIN
    DECLARE v_SalesPersonID INT;
    DECLARE v_CustomerID INT;
    DECLARE v_ProductID INT;

    -- Buscar o crear vendedor
    SELECT EmployeeID INTO v_SalesPersonID FROM employees WHERE FirstName = p_SalesPersonName LIMIT 1;
    IF v_SalesPersonID IS NULL THEN
        INSERT INTO employees (FirstName, MiddleInitial, LastName, BirthDate, Gender, CityID, HireDate)
        VALUES (p_SalesPersonName, NULL, NULL, NOW(), NULL, NULL, NOW());
        SET v_SalesPersonID = LAST_INSERT_ID();
    END IF;

    -- Buscar o crear cliente
    SELECT CustomerID INTO v_CustomerID FROM customers WHERE FirstName = p_CustomerName LIMIT 1;
    IF v_CustomerID IS NULL THEN
        INSERT INTO customers (FirstName, MiddleInitial, LastName, CityID, Address)
        VALUES (p_CustomerName, NULL, NULL, NULL, NULL);
        SET v_CustomerID = LAST_INSERT_ID();
    END IF;

    -- Buscar o crear producto
    SELECT ProductID INTO v_ProductID FROM products WHERE ProductName = p_ProductName LIMIT 1;
    IF v_ProductID IS NULL THEN
        INSERT INTO products (ProductName, Price, CategoryID, Class, ModifyDate, Resistant, IsAllergic, VitalityDays)
        VALUES (p_ProductName, 0, NULL, NULL, '00:00:00', NULL, NULL, 0);
        SET v_ProductID = LAST_INSERT_ID();
    END IF;

    -- Insertar venta
    INSERT INTO sales (SalesPersonID, CustomerID, ProductID, Quantity, Discount, TotalPrice, SalesDate, TransactionNumber)
    VALUES (v_SalesPersonID, v_CustomerID, v_ProductID, p_Quantity, p_Discount, p_TotalPrice, p_SalesDate, p_TransactionNumber);

    SET p_ResultMessage = CONCAT('Venta insertada. IDs usados -> Vendedor: ', v_SalesPersonID, ', Cliente: ', v_CustomerID, ', Producto: ', v_ProductID);

END //

DELIMITER ;

-- NO SE UTILIZA, SE HIZO LA CARGA DESDE EL SCRIPT CARGA_PY CON PANDAS, PERO SE DEJA POR LAS DUDAS.


LOAD DATA LOCAL INFILE 'C:/Users/Usuario/Desktop/H/proyecto/data/countries.csv'
INTO TABLE countries
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE 'C:/Users/Usuario/Desktop/H/proyecto/data/cities.csv'
INTO TABLE cities
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE 'C:/Users/Usuario/Desktop/H/proyecto/data/categories.csv'
INTO TABLE categories
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE 'C:/Users/Usuario/Desktop/H/proyecto/data/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE 'C:/Users/Usuario/Desktop/H/proyecto/data/employees.csv'
INTO TABLE employees
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE 'C:/Users/Usuario/Desktop/H/proyecto/data/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE 'C:/Users/Usuario/Desktop/H/proyecto/data/sales.csv'
INTO TABLE sales
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
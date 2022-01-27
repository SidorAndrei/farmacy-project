import datetime

import database_connection


@database_connection.connection_handler
def get_user(cursor, username):
    query = """
            SELECT *
            FROM farmacy.users
            WHERE username=%(username)s
            ;"""
    cursor.execute(query, {"username": username})
    return cursor.fetchone()


@database_connection.connection_handler
def insert_user(cursor, username, password):
    query = """
                INSERT INTO users(username, password)
                VALUES(%(username)s, %(password)s )
                ;"""
    cursor.execute(query, {"username": username, "password": password})


# INSERARI
@database_connection.connection_handler
def insert_medicine(cursor, medicine):
    query = """
                INSERT INTO medicines 
                    (Code, Name, Activity_area, Production_date, Expiration_date, Price, ID_provider, Stock)
                VALUES 
                    (%(code)s, %(name)s, %(activity_area)s, %(production_date)s, %(expiration_date)s, 
                    %(price)s, %(id_provider)s,  %(stock)s)
            ;"""
    cursor.execute(query, medicine)


@database_connection.connection_handler
def insert_employee(cursor, employee):
    query = """
            INSERT INTO employees
                (Name, CNP)
            VALUES
                (%(name)s, %(CNP)s)
            ;"""
    cursor.execute(query, employee)


@database_connection.connection_handler
def insert_client(cursor, client):
    query = """
            INSERT INTO clients
                (Name, Adress, CNP, code_client, gender)
            VALUES
                (%(name)s, %(adress)s, %(CNP)s, %(code_client)s, %(gender)s)
            ;"""
    cursor.execute(query, client)


@database_connection.connection_handler
def insert_provider(cursor, provider):
    query = """
            INSERT INTO providers
                (Name, Adress)
            VALUES
                (%(name)s, %(adress)s)
            ;"""
    cursor.execute(query, provider)


# STERGERI
@database_connection.connection_handler
def delete_medicine(cursor, ID_medicine):
    query = """
                    DELETE 
                    FROM recipe_content
                    WHERE ID_medicine=%(ID_medicine)s
                    ;"""
    cursor.execute(query, {"ID_medicine": ID_medicine})
    query = """
                    DELETE 
                    FROM sales
                    WHERE ID_medicine=%(ID_medicine)s
                    ;"""
    cursor.execute(query, {"ID_medicine": ID_medicine})
    query = """
                DELETE 
                FROM medicines
                WHERE ID_medicine=%(ID_medicine)s
                ;"""
    cursor.execute(query, {"ID_medicine": ID_medicine})


@database_connection.connection_handler
def delete_employee(cursor, ID_employee):
    query = """
                DELETE FROM recipe_content
                WHERE ID_recipes IN (SELECT ID_recipes FROM recipes WHERE ID_employee=%(ID_employee)s);
            ;"""
    cursor.execute(query, {"ID_employee": ID_employee})
    query = """
                DELETE FROM recipes
                WHERE ID_employee=%(ID_employee)s;
            ;"""
    cursor.execute(query, {"ID_employee": ID_employee})
    query = """
                DELETE 
                FROM employees
                WHERE ID_employee=%(ID_employee)s
            ;"""
    cursor.execute(query, {"ID_employee": ID_employee})


@database_connection.connection_handler
def delete_client(cursor, ID_client):
    query = """
                    DELETE 
                    FROM recipe_content
                    WHERE ID_recipes IN (SELECT ID_recipes FROM recipes WHERE ID_client=%(ID_client)s)
                    ;"""
    cursor.execute(query, {"ID_client": ID_client})
    query = """
                    DELETE 
                    FROM recipes
                    WHERE ID_client=%(ID_client)s
                    ;"""
    cursor.execute(query, {"ID_client": ID_client})
    query = """
                DELETE 
                FROM clients
                WHERE ID_client=%(ID_client)s
                ;"""
    cursor.execute(query, {"ID_client": ID_client})


@database_connection.connection_handler
def delete_provider(cursor, ID_provider):
    query = """
                    DELETE 
                    FROM medicines 
                    WHERE ID_provider=%(ID_provider)s
                    ;"""
    cursor.execute(query, {"ID_provider": ID_provider})
    query = """
                DELETE 
                FROM providers 
                WHERE ID_provider=%(ID_provider)s
                ;"""
    cursor.execute(query, {"ID_provider": ID_provider})


# ACTUALIZARI
@database_connection.connection_handler
def update_client(cursor, client):
    print(client)
    query = """
                UPDATE clients
                SET 
                    Name = %(Name)s,
                    Adress = %(Adress)s
                WHERE id_client = %(id_client)s
            ;"""
    cursor.execute(query, client)


@database_connection.connection_handler
def update_provider(cursor, provider):
    query = """
                UPDATE providers
                SET 
                    Name = %(Name)s,
                    Adress = %(Adress)s
                WHERE ID_provider = %(ID_provider)s
            ;"""
    cursor.execute(query, provider)


@database_connection.connection_handler
def update_medicine(cursor, medicine):
    query = """
                UPDATE medicines
                SET 
                    Name = %(Name)s,
                    Activity_area = %(Activity_area)s,
                    Price = %(Price)s,
                    Stock = %(Stock)s
                WHERE ID_provider = %(ID_provider)s
            ;"""
    cursor.execute(query, medicine)


@database_connection.connection_handler
def update_employee(cursor, employee):
    query = """
                UPDATE employees
                SET 
                    Name = %(Name)s
                WHERE ID_employee = %(ID_employee)s
            ;"""
    cursor.execute(query, employee)


# INTEROGARI SIMPLE (JOIN)
@database_connection.connection_handler
def get_all_products_grouped_by_provider(cursor):
    query = """
                SELECT  *
                FROM medicines m
                INNER JOIN providers p on p.ID_provider = m.ID_provider
                GROUP BY  p.ID_provider,m.Activity_area
                ORDER BY p.ID_provider
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_all_products_grouped_by_provider_id(cursor, provider_id):
    query = """
                SELECT  *
                FROM medicines m
                INNER JOIN providers p ON p.ID_provider = m.ID_provider
                WHERE m.ID_provider = %(provider_id)s
            ;"""
    cursor.execute(query, {"provider_id": provider_id})
    return cursor.fetchall()


@database_connection.connection_handler
def get_all_recipes(cursor):
    query = """
                SELECT  r.id_recipes, r.code, r.id_client, r.expiration_date, r.prescription_date, r.id_employee,
                        c.id_client, c.name AS Client_name, c.adress AS Client_Address, c.cnp, c.code_client, c.gender,
                        e.id_employee, e.name AS Employee_name, e.cnp AS Employee_CNP
                FROM recipes r
                INNER JOIN clients c on c.id_client = r.ID_client
                INNER JOIN employees e on e.ID_employee = r.ID_employee
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_recipes_placed_by_employee_name(cursor, employee_name):
    query = """
                SELECT  r.id_recipes, r.code, r.id_client, r.expiration_date, r.prescription_date, r.id_employee,
                        c.id_client, c.name AS Client_name, c.adress AS Client_Address, c.cnp, c.code_client, c.gender,
                        e.id_employee, e.name AS Employee_name, e.cnp AS Employee_CNP
                FROM recipes r
                INNER JOIN clients c on c.id_client = r.ID_client
                INNER JOIN employees e on e.ID_employee = r.ID_employee
                WHERE e.Name LIKE %(employee_name)s
            ;"""
    cursor.execute(query, {"employee_name": f"%{employee_name}%"})
    return cursor.fetchall()


@database_connection.connection_handler
def get_all_available_sales(cursor):
    query = """
                SELECT percent, start_date, finish_date,
                    m.id_medicine, code, m.name, activity_area, production_date, expiration_date, price, m.id_provider, stock,
                    p.name AS provider_name, p.adress as provider_address
                FROM sales s
                INNER JOIN medicines m on m.ID_medicine = s.ID_medicine
                INNER JOIN providers p on m.ID_provider = p.ID_provider
                WHERE CURRENT_DATE BETWEEN Start_date AND Finish_date
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_recipe_content(cursor, id_recipe):
    query = """
                   SELECT recipe_content.id_recipes, recipe_content.id_medicine, recipe_content.quantity,
                     m.code, m.name AS medicine_name, m.activity_area, m.production_date, m.expiration_date, m.price, m.stock,
                     p.id_provider, p.name AS provider_name, p.adress AS provider_address,
                      r.id_recipes, r.code, r.id_client, r.expiration_date, r.prescription_date,
                       c.id_client, c.name AS client_name, c.adress AS client_address, c.cnp AS client_cnp, c.code_client, c.gender,
                        e.id_employee, e.name AS employee_name, e.cnp AS employee_cnp
                   FROM recipe_content
                   INNER JOIN medicines m on recipe_content.ID_medicine = m.ID_medicine
                   INNER JOIN providers p on m.ID_provider = p.ID_provider
                   INNER JOIN recipes r on recipe_content.ID_recipes = r.ID_recipes
                   INNER JOIN clients c on r.ID_client = c.id_client
                   INNER JOIN employees e on r.ID_employee = e.ID_employee
                   WHERE r.ID_recipes = %(id_recipe)s
               ;"""
    cursor.execute(query, {"id_recipe": id_recipe})
    return cursor.fetchall()


# INTEROGARI COMPLEXE
@database_connection.connection_handler
def get_all_products(cursor):
    query = """
                SELECT  id_medicine, code, m.name AS name, activity_area, production_date, expiration_date,
                        IF((SELECT COUNT(Percent) FROM sales)>0,
                            Price*                                
                                (SELECT Percent                                 
                                FROM sales s                                
                                WHERE 
                                        m.ID_medicine= s.ID_medicine                                    
                                    AND                                      
                                        CURRENT_DATE BETWEEN Start_date AND Finish_date)/100
                        ,
                            Price) AS price_with_sale
                        , Price AS default_price,
                        stock,p.id_provider, p.name AS provider_name, adress AS Address
                FROM medicines m
                INNER JOIN providers p ON p.ID_provider = m.ID_provider
                
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_products_by_provider_name(cursor, provider_name):
    query = """
                    SELECT  id_medicine, code, m.name AS name, activity_area, production_date, expiration_date,
                            IF((SELECT COUNT(Percent) FROM sales)>0,
                                Price*                                
                                    (SELECT Percent                                 
                                    FROM sales s                                
                                    WHERE 
                                            m.ID_medicine= s.ID_medicine                                    
                                        AND                                      
                                            CURRENT_DATE BETWEEN Start_date AND Finish_date)/100
                            ,
                                price) AS price_with_sale
                            , Price AS default_price,
                            stock,p.id_provider, p.name AS provider_name, adress AS Address
                    FROM medicines m
                    INNER JOIN providers p ON 
                        p.ID_provider IN (SELECT ID_provider 
                                            FROM providers p 
                                            WHERE LOWER(p.Name) LIKE LOWER(%(provider_name)s))
                    WHERE p.ID_provider=m.ID_provider
                ;"""
    cursor.execute(query, {"provider_name": f"%{provider_name}%"})
    return cursor.fetchall()


@database_connection.connection_handler
def get_products_by_provider_city(cursor, provider_city):
    query = """
                    SELECT  id_medicine, code, m.name AS name, activity_area, production_date, expiration_date,
                            IF((SELECT COUNT(Percent) FROM sales WHERE 
                                            m.ID_medicine= s.ID_medicine                                    
                                        AND                                      
                                            CURRENT_DATE BETWEEN Start_date AND Finish_date)>0,
                                Price*                                
                                    (SELECT Percent                                 
                                    FROM sales s                                
                                    WHERE 
                                            m.ID_medicine= s.ID_medicine                                    
                                        AND                                      
                                            CURRENT_DATE BETWEEN Start_date AND Finish_date)/100
                            ,
                                Price) AS price_with_sale
                            , Price AS default_price,
                            stock,p.id_provider, p.name AS provider_name, adress AS Address
                    FROM medicines m
                    INNER JOIN providers p ON 
                        p.ID_provider IN (SELECT ID_provider 
                                            FROM providers p 
                                            WHERE LOWER(p.Adress) LIKE LOWER(%(provider_city)s))
                    WHERE m.ID_provider=p.ID_provider
                ;"""
    cursor.execute(query, {"provider_city": f"%{provider_city}%"})
    return cursor.fetchall()


@database_connection.connection_handler
def get_products_by_name(cursor, medicine_name):
    query = """
                    SELECT  id_medicine, code, m.name AS name, activity_area, production_date, expiration_date,
                            IF((SELECT COUNT(Percent) FROM sales s 
                                        WHERE 
                                            m.ID_medicine= s.ID_medicine                                    
                                        AND                                      
                                            CURRENT_DATE BETWEEN Start_date AND Finish_date)>0,
                                Price*                                
                                    (SELECT Percent                                 
                                    FROM sales s                                
                                    WHERE 
                                            m.ID_medicine= s.ID_medicine                                    
                                        AND                                      
                                            CURRENT_DATE BETWEEN Start_date AND Finish_date)/100
                            ,
                                Price) AS price_with_sale
                            , Price AS default_price,
                            stock,p.id_provider, p.name AS provider_name, adress AS Address
                    FROM medicines m
                    INNER JOIN providers p ON p.ID_provider = m.ID_provider
                    WHERE LOWER(m.Name) LIKE LOWER(%(medicine_name)s)
                ;"""
    cursor.execute(query, {"medicine_name": f"%{medicine_name}%"})
    return cursor.fetchall()


# SIMPLE SELECTS
@database_connection.connection_handler
def get_all_providers(cursor):
    query = """
                SELECT *
                FROM providers
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_all_clients(cursor):
    query = """
                SELECT *
                FROM clients
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_all_employees(cursor):
    query = """
                SELECT *
                FROM employees
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_all_medicines(cursor):
    query = """
                SELECT *
                FROM medicines
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_providers_by_id(cursor, id):
    query = """
                SELECT *
                FROM providers
                WHERE ID_provider = %(id)s
            ;"""
    cursor.execute(query, {"id": id})
    return cursor.fetchone()


@database_connection.connection_handler
def get_client_by_id(cursor, id):
    query = """
                SELECT *
                FROM clients
                WHERE id_client = %(id)s
            ;"""
    cursor.execute(query, {"id": id})
    return cursor.fetchone()


@database_connection.connection_handler
def get_employee_by_id(cursor, id):
    query = """
                SELECT *
                FROM employees
                WHERE ID_employee = %(id)s
            ;"""
    cursor.execute(query, {"id": id})
    return cursor.fetchone()


@database_connection.connection_handler
def get_medicine_by_id(cursor, id):
    query = """
                SELECT *
                FROM medicines
                WHERE ID_medicine = %(id)s
            ;"""
    cursor.execute(query, {"id": id})
    return cursor.fetchone()

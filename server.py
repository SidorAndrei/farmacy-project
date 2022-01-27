from flask import Flask, render_template, redirect, url_for, request, session

import cryptography
import database_manager

# import dotenv
# dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = b'_5#87x"F4Qdu\n\xec]/'


# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        user = database_manager.get_user(request.form["username"])
        if cryptography.verify_password(request.form["password"], user["password"]):
            session.update({"username": user["username"], "user_id": user["ID_user"]})
            print("connection ok")
            return redirect(url_for("main_page"))
    return render_template(
        "login_page.html",
        username=session["username"],
    )


# LOGOUT PAGE
@app.route("/logout")
def logout_page():
    session.pop("username")
    session.pop("user_id")
    print(session)
    return redirect(url_for("main_page"))


# REGISTER PAGE
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        password = request.form.get("reg_password")
        confirm_password = request.form.get("reg_password_confirm")
        if password == confirm_password:
            database_manager.insert_user(
                username=request.form.get("reg_username"),
                password=cryptography.hash_password(password),
            )
            return redirect(url_for("login_page"))
    return render_template(
        "register_page.html",
        username=session["username"],
    )


@app.route("/")
def main_page():
    print(session)
    if "username" not in session:
        return redirect(url_for("login_page"))
    if "q" in request.args:
        products = database_manager.get_products_by_name(request.args.get("q"))
    else:
        products = database_manager.get_all_products()
    for product in products:
        print(product)
    return render_template(
        "products.html",
        username=session["username"],
        user_id=session["user_id"],
        products=products,
    )


@app.route("/inserts")
def inserts_page():
    providers = database_manager.get_all_providers()
    if "message" in request.args:
        message = request.args.get("message")
        return render_template(
            "inserts.html",
            username=session["username"],
            message=message,
            providers=providers,
        )
    return render_template(
        "inserts.html", username=session["username"], providers=providers
    )


@app.route("/inserts/insert_medicine", methods=["POST"])
def insert_medicine():
    medicine = {
        "code": request.form.get("medicine_code"),
        "name": request.form.get("medicine_name"),
        "activity_area": request.form.get("medicine_activity_area"),
        "production_date": request.form.get("medicine_production_date"),
        "expiration_date": request.form.get("medicine_expiration_date"),
        "price": request.form.get("medicine_price"),
        "id_provider": request.form.get("medicine_provider"),
        "stock": request.form.get("medicine_stock"),
    }
    if not medicine.get("id_provider"):
        message = "SELECT PROVIDER"
    else:
        database_manager.insert_medicine(medicine)
        message = "MEDICINE INSERTED SUCCESFULLY!"
    return redirect(url_for("inserts_page", message=message))


@app.route("/inserts/insert_employee", methods=["POST"])
def insert_employee():
    employee = {
        "name": request.form.get("employee_name"),
        "CNP": request.form.get("employee_cnp"),
    }
    if not (employee.get("name") and employee.get("CNP")):
        return redirect(
            url_for("inserts_page", message="COMPLETE ALL REQUIRED FIELDS!")
        )
    database_manager.insert_employee(employee)
    return redirect(url_for("inserts_page", message="EMPLOYEE ADDED SUCCESFULLY!"))


@app.route("/inserts/insert_client", methods=["POST"])
def insert_client():
    client = {
        "name": request.form.get("customer_name"),
        "adress": request.form.get("customer_address"),
        "CNP": request.form.get("customer_cnp"),
        "code_client": request.form.get("customer_code"),
        "gender": request.form.get("customer_gender"),
    }
    if not (
        client.get("name")
        and client.get("adress")
        and client.get("CNP")
        and client.get("code_client")
        and client.get("gender")
    ):
        return redirect(
            url_for("inserts_page", message="COMPLETE ALL REQUIRED FIELDS!")
        )
    database_manager.insert_client(client)
    return redirect(url_for("inserts_page", message="CLIENT ADDED SUCCESFULLY!"))


@app.route("/inserts/insert_provider", methods=["POST"])
def insert_provider():
    provider = {
        "name": request.form.get("provider_name"),
        "adress": request.form.get("provider_adress"),
    }
    if not (provider.get("name") and provider.get("adress")):
        return redirect(
            url_for("inserts_page", message="COMPLETE ALL REQUIRED FIELDS!")
        )
    return redirect(url_for("inserts_page", message="PROVIDER ADDED SUCCESFULLY!"))


@app.route("/deletes")
def deletes_page():
    clients = database_manager.get_all_clients()
    employees = database_manager.get_all_employees()
    medicines = database_manager.get_all_medicines()
    providers = database_manager.get_all_providers()
    if "message" in request.args:
        return render_template(
            "deletes.html",
            username=session["username"],
            clients=clients,
            employees=employees,
            medicines=medicines,
            providers=providers,
            message=request.args.get("message"),
        )
    return render_template(
        "deletes.html",
        username=session["username"],
        clients=clients,
        employees=employees,
        medicines=medicines,
        providers=providers,
    )


@app.route("/deletes/delete_client", methods=["POST"])
def delete_client():
    id_client = request.form.get("delete_client")
    if not id_client:
        return redirect(url_for("deletes_page", message="SELECT A CLIENT!"))
    database_manager.delete_client(id_client)
    return redirect(
        url_for("deletes_page", message=f"CUSTUMER {id_client} HAS BEEN DELETED!")
    )


@app.route("/deletes/delete_medicine", methods=["POST"])
def delete_medicine():
    id_medicine = request.form.get("delete_medicine")
    if not id_medicine:
        return redirect(url_for("deletes_page", message="SELECT A MEDICINE!"))
    database_manager.delete_medicine(id_medicine)
    return redirect(
        url_for("deletes_page", message=f"MEDICINE {id_medicine} HAS BEEN DELETED!")
    )


@app.route("/deletes/delete_provider", methods=["POST"])
def delete_provider():
    id_provider = request.form.get("delete_provider")
    if not id_provider:
        return redirect(url_for("deletes_page", message="SELECT A PROVIDER!"))
    database_manager.delete_provider(id_provider)
    return redirect(
        url_for("deletes_page", message=f"PROVIDER {id_provider} HAS BEEN DELETED!")
    )


@app.route("/deletes/delete_employee", methods=["POST"])
def delete_employee():
    id_employee = request.form.get("delete_employee")
    if not id_employee:
        return redirect(url_for("deletes_page", message="SELECT AN EMPLOYEE!"))
    database_manager.delete_employee(id_employee)
    return redirect(
        url_for("deletes_page", message=f"EMPLOYEE {id_employee} HAS BEEN DELETED!")
    )


@app.route("/updates")
def updates_page():
    clients = database_manager.get_all_clients()
    employees = database_manager.get_all_employees()
    medicines = database_manager.get_all_medicines()
    providers = database_manager.get_all_providers()
    if "message" in request.args:
        return render_template(
            "updates.html",
            username=session["username"],
            clients=clients,
            employees=employees,
            medicines=medicines,
            providers=providers,
            message=request.args.get("message"),
        )
    return render_template(
        "updates.html",
        username=session["username"],
        clients=clients,
        employees=employees,
        medicines=medicines,
        providers=providers,
    )


@app.route("/updates/update_employee", methods=["GET", "POST"])
def update_employee():
    id_employee = request.form.get("update_employee")
    if not id_employee:
        return redirect(url_for("updates_page", message="SELECT A EMPLOYEE!"))
    employee = database_manager.get_employee_by_id(id_employee)
    return render_template(
        "update_employee.html", username=session["username"], employee=employee
    )


@app.route("/updates/update_employee_<id_employee>", methods=["GET", "POST"])
def update_employee_in_db(id_employee):
    employee = database_manager.get_employee_by_id(id_employee)
    employee.update(
        {
            "Name": request.form.get("employee_name"),
        }
    )
    database_manager.update_employee(employee)
    return redirect(
        url_for(
            "updates_page", message=f"EMPLOYEE {employee.get('Name')} HAS BEEN UPDATED!"
        )
    )


@app.route("/updates/update_client", methods=["GET", "POST"])
def update_client():
    id_client = request.form.get("update_client")
    if not id_client:
        return redirect(url_for("updates_page", message="SELECT A CLIENT!"))
    client = database_manager.get_client_by_id(id_client)
    return render_template(
        "update_client.html", username=session["username"], client=client
    )


@app.route("/updates/update_client_<id_client>", methods=["GET", "POST"])
def update_client_in_db(id_client):
    client = database_manager.get_client_by_id(id_client)
    client.update(
        {
            "Name": request.form.get("client_name"),
            "Adress": request.form.get("client_address"),
        }
    )
    database_manager.update_client(client)
    return redirect(
        url_for(
            "updates_page", message=f"CUSTOMER {client.get('Name')} HAS BEEN UPDATED!"
        )
    )


@app.route("/updates/update_medicine", methods=["GET", "POST"])
def update_medicine():
    id_medicine = request.form.get("update_medicine")
    if not id_medicine:
        return redirect(url_for("updates_page", message="SELECT A MEDICINE!"))
    medicine = database_manager.get_medicine_by_id(id_medicine)
    return render_template(
        "update_medicine.html", username=session["username"], medicine=medicine
    )


@app.route("/updates/update_client_<id_medicine>", methods=["GET", "POST"])
def update_medicine_in_db(id_medicine):
    medicine = database_manager.get_medicine_by_id(id_medicine)
    medicine.update(
        {
            "Name": request.form.get("medicine_name"),
            "Activity_area": request.form.get("medicine_activity_area"),
            "Price": request.form.get("medicine_price"),
            "Stock": request.form.get("medicine_stock"),
        }
    )
    database_manager.update_medicine(medicine)
    return redirect(
        url_for(
            "updates_page", message=f"MEDICINE {medicine.get('Name')} HAS BEEN UPDATED!"
        )
    )


@app.route("/updates/update_provider", methods=["GET", "POST"])
def update_provider():
    id_provider = request.form.get("update_provider")
    if not id_provider:
        return redirect(url_for("updates_page", message="SELECT A PROVIDER!"))
    provider = database_manager.get_providers_by_id(id_provider)
    print(provider)
    return render_template(
        "update_provider.html", username=session["username"], provider=provider
    )


@app.route("/updates/update_provider_<id_provider>", methods=["GET", "POST"])
def update_provider_in_db(id_provider):
    provider = database_manager.get_providers_by_id(id_provider)
    provider.update(
        {
            "Name": request.form.get("provider_name"),
            "Adress": request.form.get("provider_address"),
        }
    )
    database_manager.update_provider(provider)
    return redirect(
        url_for("updates_page", message=f"PROVIDER {id_provider} HAS BEEN UPDATED!")
    )


@app.route("/selects_join")
def selects_join_page():
    recipes = database_manager.get_all_recipes()
    providers = database_manager.get_all_providers()
    return render_template(
        "selects_join.html",
        username=session["username"],
        recipes=recipes,
        providers=providers,
    )


@app.route("/selects_join/join_1", methods=["POST"])
def select_join_1():
    elements = database_manager.get_all_products_grouped_by_provider()
    return render_template(
        "table_page.html",
        username=session["username"],
        elements=elements,
        headers=elements[0].keys(),
    )


@app.route("/selects_join/join_2", methods=["POST"])
def select_join_2():
    elements = database_manager.get_all_products_grouped_by_provider_id(
        request.form.get("provider")
    )
    return render_template(
        "table_page.html",
        username=session["username"],
        elements=elements,
        headers=elements[0].keys(),
    )


@app.route("/selects_join/join_3", methods=["POST"])
def select_join_3():
    elements = database_manager.get_all_recipes()
    return render_template(
        "table_page.html",
        username=session["username"],
        elements=elements,
        headers=elements[0].keys(),
    )


@app.route("/selects_join/join_4", methods=["POST"])
def select_join_4():
    elements = database_manager.get_recipes_placed_by_employee_name(
        request.form.get("employee_name")
    )
    return render_template(
        "table_page.html",
        username=session["username"],
        elements=elements,
        headers=elements[0].keys(),
    )


@app.route("/selects_join/join_5", methods=["POST"])
def select_join_5():
    elements = database_manager.get_all_available_sales()
    return render_template(
        "table_page.html",
        username=session["username"],
        elements=elements,
        headers=elements[0].keys(),
    )


@app.route("/selects_join/join_6", methods=["POST"])
def select_join_6():
    elements = database_manager.get_recipe_content(request.form.get("recipe"))
    return render_template(
        "table_page.html",
        username=session["username"],
        elements=elements,
        headers=elements[0].keys(),
    )


@app.route("/selects_complex")
def selects_complex_page():
    return render_template(
        "complex_selects.html",
        username=session["username"],
    )


@app.route("/selects_complex/select_complex_1", methods=["POST"])
def select_complex_1():
    elements = database_manager.get_all_products()
    return render_template(
        "table_page.html",
        username=session["username"],
        elements=elements,
        headers=elements[0].keys(),
    )


@app.route("/selects_complex/select_complex_2", methods=["POST"])
def select_complex_2():
    elements = database_manager.get_products_by_provider_name(
        request.form.get("provider")
    )
    return render_template(
        "table_page.html",
        username=session["username"],
        elements=elements,
        headers=elements[0].keys(),
    )


@app.route("/selects_complex/select_complex_3", methods=["POST"])
def select_complex_3():
    elements = database_manager.get_products_by_provider_city(
        request.form.get("provider")
    )
    return render_template(
        "table_page.html",
        username=session["username"],
        elements=elements,
        headers=elements[0].keys(),
    )


@app.route("/selects_complex/select_complex_4", methods=["POST"])
def select_complex_4():
    elements = database_manager.get_products_by_name(request.form.get("product"))
    print(elements)
    return render_template(
        "table_page.html",
        username=session["username"],
        elements=elements,
        headers=elements[0].keys(),
    )


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )

import numpy as np
from flask import Flask, redirect, url_for, request, Response, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "testing"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "dccassignment4"

mysql = MySQL(app)

def run_query(query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    res = []
    for i in data:
        res.append(list(i))
    return np.array(res)

@app.route("/", methods=["GET"])
def main_page():
    print(run_query("describe purchased")[:, 0])
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html")

@app.route("/search/purchased/result", methods=["POST"])
def search_purchased():
    field = request.form["Fields_Purchased"]
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from purchased where {field} = %s", (request.form["Field_val"],))
    data = cursor.fetchall()
    cursor.close()
    return render_template("search.html", result=data, table="Purchased")

@app.route("/search/encashed/result", methods=["POST"])
def search_encashed():
    field = request.form["Fields_Encashed"]
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from encashed where {field} = %s", (request.form["Field_val"],))
    data = cursor.fetchall()
    cursor.close()
    return render_template("search.html", result=data, table="Encashed")

@app.route("/company_purchases", methods=["GET"])
def company_purchases():
    return render_template('company_purchases.html')

@app.route("/company_purchases/result", methods=['POST'])
def comapany_purchases_result():
    cursor = mysql.connection.cursor()
    cn = request.form["Company_Name"]
    data = cursor.execute(f"select year(str_to_date(Date_of_Purchase, '%d/%M/%Y')) as year, sum(Denominations) as value, count(Denominations) as total from purchased where Name_of_the_Purchaser = '{cn}' group by year;")
    data = cursor.fetchall()
    cursor.close()
    if len(data) == 0:
        data = "none"
    return render_template("company_purchases.html", result=data, companyname=request.form["Company_Name"])

@app.route("/party_encashments")
def party_encashment_year():
    return render_template('party_encashments.html')

@app.route("/party_encashments/result", methods=['POST'])
def party_encashment_result():
    cursor = mysql.connection.cursor()
    pn = request.form["Party_Name"]
    cursor.execute(f"select year(STR_TO_DATE(Date_of_Encashment, '%d/%M/%Y')) as year, sum(Denominations) as value, count(Denominations) as total from encashed where Name_of_the_Political_Party = '{pn}' group by year;")
    data = cursor.fetchall()
    cursor.close()
    if len(data) == 0:
        data = "none"
    return render_template("party_encashments.html", result=data, partyname=request.form["Party_Name"])

@app.route("/donations_recieved")
def party_donations():
   return render_template("donations_recieved.html")

@app.route("/donations_recieved/result", methods=["POST"])
def party_donations_result():
    pn = request.form["Party_Name"]
    cursor = mysql.connection.cursor()
    cursor.execute(f"select Name_of_the_Purchaser, sum(encashed.Denominations) as amt from encashed join purchased on (encashed.Prefix, encashed.Bond_Number) = (purchased.Prefix, purchased.Bond_Number) where Name_of_the_Political_Party = '{pn}' group by Name_of_the_Purchaser")
    data = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute(f"select sum(encashed.Denominations) from encashed join purchased on (encashed.Prefix,encashed.Bond_Number) = (purchased.Prefix, purchased.Bond_Number) where Name_of_the_Political_Party = '{pn}'")
    amt = cursor.fetchall() 
    cursor.close()

    return render_template("donations_recieved.html", result=data, partyname=request.form["Party_Name"], amt=amt)

@app.route("/donations")
def company_donations():
   return render_template("donations.html")

@app.route("/donations/result", methods=["POST"])
def company_donations_result():
    cn = request.form["Company_Name"]
    cursor = mysql.connection.cursor()    
    cursor.execute(f"select Name_of_the_Political_Party, sum(encashed.Denominations) as amt from encashed join purchased on (encashed.Prefix, encashed.Bond_Number) = (purchased.Prefix, purchased.Bond_Number) where Name_of_the_Purchaser = '{cn}' group by Name_of_the_Political_Party")
    data = cursor.fetchall()
    cursor.close()
    
    cursor = mysql.connection.cursor()
    cursor.execute(f"select sum(encashed.Denominations) as amt from encashed join purchased on (encashed.Prefix, encashed.Bond_Number) = (purchased.Prefix, purchased.Bond_Number) where Name_of_the_Purchaser = '{cn}' ")
    amt = cursor.fetchall()
    cursor.close()
    
    return render_template("donations.html", result=data, companyname=request.form["Company_Name"], amt=amt)



# @app.route("/total_donations_pie")
# def total_donations_pie():
#    cursor = mysql.connection.cursor()

#    cursor.execute("select Name_of_the_Political_Party, sum(Denominations) from encashed group by Name_of_the_Political_Party")

#    data = cursor.fetchall()

#    cursor.close()

#    return render_template("total_donations_pie.html", result = data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80", debug=True)

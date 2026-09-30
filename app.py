import json
from datetime import datetime
from flask import Flask,flash,redirect,render_template,request,session,url_for
from uuid import uuid4
app=Flask(__name__)
app.secret_key="bsbggbwegkhjwjoqwjlkqwrkgr"
DATA_FILE="data.json"
CATEGORIES=["Food","Transport","Shopping","Bills","Entertainment","Health","Education","Other"]

def load_data():
    try:
        with open(DATA_FILE,"r") as file:
         data=json.load(file)
        return data
    except:
        return {"users":[],"expenses":[]}
    
def save_data(data):
    with open(DATA_FILE,"w") as file:
     json.dump(data,file,indent=2)

def login_required():
    if "username" not in session:
        return False
    return True

@app.route("/register",methods=["GET","POST"])
def register():
    if "username" in session:
        return redirect(url_for("home"))
    if request.method=="POST":
        username=request.form.get("username","").strip()
        password=request.form.get("password","")
        data=load_data()
        if username=="" or password=="":
            flash("Username and password are required.","error")
        else:
            exists=False
            for user in data["users"]:
                if user["username"].lower()==username.lower():
                    exists=True
                    break
            if exists:
                flash("Username already exists.","error")
            else:
                user={"username":username,"password":password}
                data["users"].append(user)
                save_data(data)
                flash("Account created.","success")
                return redirect(url_for("login"))
    return render_template("auth.html",mode="register")

@app.route("/login",methods=["GET","POST"])
def login():
    if "username" in session:
        return redirect(url_for("home"))
    if request.method=="POST":
        username=request.form.get("username","").strip()
        password=request.form.get("password","")
        data=load_data()
        user=None
        for u in data["users"]:
            if u["username"]==username and u["password"]==password:
                user=u
                break
        if user:
            session["username"]=user["username"]
            return redirect(url_for("home"))
        flash("Invalid username or password.","error")
    return render_template("auth.html",mode="login")

def current_user_expenses():
    data=load_data()
    expenses=[]
    for expense in data["expenses"]:
        if expense["username"]==session["username"]:
            expenses.append(expense)
    return expenses

def find_expense(expense_id):
    data=load_data()
    for expense in data["expenses"]:
        if expense["id"]==expense_id and expense["username"]==session["username"]:
            return expense
    return None

def validate_expense(form):
    name=form.get("name","").strip()
    category=form.get("category","").strip()
    date=form.get("date","").strip()
    amount=form.get("amount","").strip()
    errors=[]
    if name=="":
        errors.append("Enter the expense name.")
    if category not in CATEGORIES:
        errors.append("Choose a valid category.")
    try:
        datetime.strptime(date,"%Y-%m-%d")
    except:
        errors.append("Enter a valid date.")
    try:
        amount=float(amount)
        if amount<=0:
            errors.append("Enter a valid amount.")
    except:
        errors.append("Enter a valid amount.")
        amount=0
    values={"name":name,"category":category,"date":date,"amount":amount}
    return values,errors

@app.route("/")
def home():
    if "username" not in session:
        return render_template("home.html")
    expenses=current_user_expenses()
    total=0
    for expense in expenses:
        total=total+expense["amount"]
    recent=expenses[-5:]
    return render_template("home.html",total=total,recent=recent)

@app.route("/expenses")
def expenses():
    if not login_required():
        return redirect(url_for("login"))
    data=current_user_expenses()
    total=0
    for expense in data:
        total=total+expense["amount"]
    return render_template("expenses.html",expenses=data,total=total)

@app.route("/add-expense",methods=["GET","POST"])
def add_expense():
    if not login_required():
        return redirect(url_for("login"))
    values={"name":"","category":"","date":datetime.today().strftime("%Y-%m-%d"),"amount":""}
    if request.method=="POST":
        values,errors=validate_expense(request.form)
        if len(errors)>0:
            for error in errors:
                flash(error,"error")
        else:
            data=load_data()
            expense={"id":uuid4().hex,"username":session["username"],"name":values["name"],"category":values["category"],"date":values["date"],"amount":values["amount"]}
            data["expenses"].append(expense)
            save_data(data)
            flash("Expense added.","success")
            return redirect(url_for("expenses"))
    return render_template("expense_form.html",values=values,categories=CATEGORIES,title="Add expense",submit_label="Add expense")

@app.route("/edit-expense/<expense_id>",methods=["GET","POST"])
def edit_expense(expense_id):
    if not login_required():
        return redirect(url_for("login"))
    expense=find_expense(expense_id)
    if expense is None:
        flash("Expense not found.","error")
        return redirect(url_for("expenses"))
    values=expense.copy()
    if request.method=="POST":
        values,errors=validate_expense(request.form)
        if len(errors)>0:
            for error in errors:
                flash(error,"error")
        else:
            data=load_data()
            for item in data["expenses"]:
                if item["id"]==expense_id and item["username"]==session["username"]:
                    item["name"]=values["name"]
                    item["category"]=values["category"]
                    item["date"]=values["date"]
                    item["amount"]=values["amount"]
                    break
            save_data(data)
            flash("Expense updated.","success")
            return redirect(url_for("expenses"))
    return render_template("expense_form.html",values=values,categories=CATEGORIES,title="Edit expense",submit_label="Save changes")

@app.route("/delete-expense/<expense_id>",methods=["POST"])
def delete_expense(expense_id):
    if not login_required():
        return redirect(url_for("login"))
    expense=find_expense(expense_id)
    if expense is None:
        flash("Expense not found.","error")
    else:
        data=load_data()
        new_expenses=[]
        for item in data["expenses"]:
            if item["id"]!=expense_id:
                new_expenses.append(item)
        data["expenses"]=new_expenses
        save_data(data)
        flash("Expense deleted.","success")
    return redirect(url_for("expenses"))

@app.route("/analytics",methods=["GET","POST"])
def analytics():
    if not login_required():
        return redirect(url_for("login"))
    expenses=current_user_expenses()
    selected_date=request.form.get("date","")
    selected_month=request.form.get("month","")
    selected_year=request.form.get("year","")
    date_total=None
    month_total=None
    year_total=None
    if selected_date!="":
        date_total=0
        for expense in expenses:
            if expense["date"]==selected_date:
                date_total=date_total+expense["amount"]
    if selected_month!="":
        month_total=0
        for expense in expenses:
            if expense["date"].startswith(selected_month):
                month_total=month_total+expense["amount"]
    if selected_year!="":
        year_total=0
        for expense in expenses:
            if expense["date"].startswith(selected_year):
                year_total=year_total+expense["amount"]
    total=0
    categories={}
    for expense in expenses:
        total=total+expense["amount"]
        category=expense["category"]
        if category not in categories:
            categories[category]=0
        categories[category]=categories[category]+expense["amount"]
    by_category=[]
    for category in categories:
        by_category.append((category,categories[category]))
    return render_template("analytics.html",total=total,by_category=by_category,selected_date=selected_date,selected_month=selected_month,selected_year=selected_year,date_total=date_total,month_total=month_total,year_total=year_total)

@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("home"))

@app.template_filter("currency")
def currency(value):
    return f"₹{float(value):,.2f}"

if __name__=="__main__":
    app.run(debug=True, port=5000)
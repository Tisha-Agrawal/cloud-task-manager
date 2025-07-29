from flask import Flask, render_template, request, redirect
from cloudant.client import Cloudant
from dotenv import load_dotenv
import os

# Load .env credentials
load_dotenv()

app = Flask(__name__)

# Connect to IBM Cloudant
client = Cloudant.iam(
    os.getenv("CLOUDANT_USERNAME"),
    os.getenv("CLOUDANT_API_KEY"),
    connect=True
)

# Use the database (must already exist in Cloudant dashboard)
db = client[os.getenv("CLOUDANT_DB_NAME")]

@app.route("/")
def index():
    tasks = [doc for doc in db]
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        db.create_document({"task": task})
    return redirect("/")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    doc = db[id]
    if request.method == "POST":
        doc["task"] = request.form.get("task")
        doc.save()
        return redirect("/")
    return render_template("edit.html", task=doc)

@app.route("/delete/<id>")
def delete(id):
    db[id].delete()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

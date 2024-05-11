from flask import Flask, render_template, request
import requests
from mailjet_rest import Client
import os

api_key = '4fca7b5c7fb404819cfe8816d868a8a1'
api_secret = '9be67413216440f7098a92ce1a03f45a'

app = Flask(__name__)


response = requests.get("https://api.npoint.io/afb592a1804a6161359b")
data = response.json()


@app.route("/")
def home():
    return render_template("index.html", all_posts=data)


@app.route("/post/<int:index>")
def post_page(index):
    post_data = None
    for blog_post in data:
        if blog_post["id"] == index:
            post_data = blog_post
    return render_template("post.html", post=post_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact",  methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        input_name = request.form["name"]
        input_email = request.form["email"]
        input_phone = request.form["phone"]
        input_message = request.form["message"]
        send_email(name=input_name, email=input_email, phone=input_phone, message=input_message)
    return render_template("contact.html")


def send_email(name, email, phone, message):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "lizaabadzan@gmail.com",
                    "Name": "Yelyzaveta"
                },
                "To": [
                    {
                        "Email": "lizaabadzan@gmail.com",
                        "Name": "Yelyzaveta"
                    }
                ],
                "Subject": "Message from my_blog",
                "TextPart": f"Name: {name}\nEmail: {email}\nPhone Number: {phone}\nMessage: {message}",
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())


if __name__ == "__main__":
    app.run(debug=True)


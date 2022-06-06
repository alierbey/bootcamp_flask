from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# from requests import request


con = sqlite3.connect("book.db")


def veriEkle(title, author, year):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute(
            "insert into tblBook (booktitle, bookauthor, bookyear) values (?, ?, ?)", (title, author, year))
        con.commit()
    print("veriler eklendi")


data = []


def veriAl():
    global data
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("select * from tblBook order by id desc ")
        data = cur.fetchall()
        # print(data)
        for i in data:
            print(i)


def verisil(id):

    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("delete from tblBook where id=?", (id,))
        # data = cur.fetchall()


# veriAl()
# print("---")
# print(data)
app = Flask(__name__)


@app.route("/")
def index():
    books = [
        {
            "bookID": 1,
            "bookTitle": "Cehenneme Övgü",
            "bookAuthor": "Gündüz Vassaf",
            "bookYear": 1995},
        {
            "bookID": 2,
            "bookTitle": "Saatleri Ayarlama Enstitüsü",
            "bookAuthor": "Ahmet Hamdi Tanpınar",
            "bookYear": 1960},
        {
            "bookID": 1,
            "bookTitle": "Dublör Dilemması",
            "bookAuthor": "Murat Menteş",
            "bookYear": 2007}
    ]
    return render_template("index.html", books=books)


@app.route("/book/<string:id>")
def bookdetail(id):
    return "book id :" + id


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/bookadd", methods=["POST", "GET"])
def bookadd():
    if request.method == "POST":
        bookTitle = request.form["bookTitle"]
        bookAuthor = request.form["bookAuthor"]
        bookYear = request.form["bookYear"]

        print(bookTitle, bookAuthor, bookYear)
        veriEkle(bookTitle, bookAuthor, bookYear)

    return render_template("bookadd.html")


@app.route("/kitap")
def kitap():
    veriAl()
    return render_template("kitap.html", veri=data)


@app.route("/bookdelete/<string:id>")
def bookdelete(id):
    verisil(id)
    return redirect(url_for("kitap"))


if __name__ == "__main__":
    app.run(debug=True)

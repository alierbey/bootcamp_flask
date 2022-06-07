from flask import Flask, render_template, request, redirect, url_for
import sqlite3


# CRUD - Create - Read - Update - Delete


# Veri Ekleme Fonksiyonu
def veriEkle(title, author, year):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute(
            "insert into tblBook (booktitle, bookauthor, bookyear) values (?, ?, ?)", (title, author, year))
        con.commit()
    print("veriler eklendi")


data = []


# Verileri listeye çekiyoruz
def veriAl():
    global data
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("select * from tblBook order by id desc ")
        data = cur.fetchall()
        # print(data)
        for i in data:
            print(i)


# Veri silmek icin kullanılan fonksiyon
def veriSil(id):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("delete from tblBook where id=?", (id,))
        # data = cur.fetchall()


def veriGuncelle(id, title, author, year):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("update tblBook set bookTitle = ?, bookAuthor = ?, bookYear = ? where id = ?",
                    (title, author, year, id,))
        con.commit()
    print("Veriler Guncellendi...")


veriAl()
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
    detayveri = []
    for d in data:
        if str(d[0]) == id:
            detayveri = list(d)
    return render_template("kitapdetay.html", veri=detayveri)


@app.route("/bookedit/<string:id>", methods=["GET", "POST"])
def bookedit(id):
    if request.method == "POST":
        id = request.form["id"]
        bookTitle = request.form["bookTitle"]
        bookAuthor = request.form["bookAuthor"]
        bookYear = request.form["bookYear"]
        print("Guncellenecek Veriler : ", bookTitle, bookAuthor, bookYear)
        veriGuncelle(id, bookTitle, bookAuthor, bookYear)
        return redirect(url_for("kitap"))
    else:
        guncellenecekveri = []
        for d in data:
            if str(d[0]) == id:
                guncellenecekveri = list(d)
        return render_template("bookedit.html", veri=guncellenecekveri)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


# http method
# POST - Veri ekleyeveğimiz
# GET - veri talep ediyorsunuz
# PUT - update
# DELETE - silmek

@app.route("/bookadd", methods=["POST", "GET"])
def bookadd():
    if request.method == "POST":
        bookTitle = request.form["bookTitle"]
        bookAuthor = request.form["bookAuthor"]
        bookYear = request.form["bookYear"]

        print("Eklenecek Veriler : ", bookTitle, bookAuthor, bookYear)
        veriEkle(bookTitle, bookAuthor, bookYear)

    return render_template("bookadd.html")


@app.route("/kitap")
def kitap():
    veriAl()
    return render_template("kitap.html", veri=data)


@app.route("/bookdelete/<string:id>")
def bookdelete(id):
    veriSil(id)
    return redirect(url_for("kitap"))


if __name__ == "__main__":
    app.run(debug=True)

from flask import render_template, Blueprint


index_page = Blueprint("index", __name__, url_prefix="/")


@index_page.route("")
def root():
    return render_template("index.html")

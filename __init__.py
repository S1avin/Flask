from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage():

    title = "Empty page"
    paragraph = ["Nothing here right now"]

    try:
        return render_template("index.html", title = title, paragraph=paragraph)
    except Exception, e:
        return str(e)

@app.route('/new')
def nawpage():

    title = "Add new Item"
    paragraph = ["Here will be some input boxes."]

    return render_template("index.html", title=title, paragraph=paragraph)

@app.route('/update')
def updatePage():

    title = "update"
    paragraph = ["update"]

    return render_template("index.html", title=title, paragraph=paragraph)

@app.route('/update/price')
def updatepricePage():

    title = "update price"
    paragraph = ["You can update any price here"]

    return render_template("index.html", title=title, paragraph=paragraph)

@app.route('/update/description')
def updatedescriptionPage():

    title = "update description"
    paragraph = ["You can update any description here"]

    return render_template("index.html", title=title, paragraph=paragraph)

@app.route('/update/location')
def updatelocationPage():

    title = "update location"
    paragraph = ["You can update any location here"]

    return render_template("index.html", title=title, paragraph=paragraph)


if __name__ == "__main__":
        app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)



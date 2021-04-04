import matplotlib.pyplot as plt
import persistenceLayer
from flask import Flask, render_template, request, flash, redirect, url_for, Response
from covidRecordModel import CovidRecordModel
import pandas as pd
import mpld3
import matplotlib
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
matplotlib.use('Agg')


app = Flask(__name__)
app.secret_key = "Ahmed"


records = persistenceLayer.fetchRecords()
'''Array that holds the records fetched from the database'''


displayRange = [0, 100]
'''the range of data displayed on the screen, defaults to 100'''

plotColumn = 'ratetotal'

# Author: Ahmed Aziz


@app.route("/", methods=["POST", "GET"])
def home():
    '''Home Method is exuectued to render the home page of the web app and to handle diffrent Post and Get requests coming from user interactions, it returns the template to be rendered'''
    global records
    global displayRange
    global plotColumn
    '''needed to declare the variables gloval to access them between diffrent methods'''
    if request.method == "POST":
        '''if condition to handle all POST requests coming from user interactions'''

        if request.form['submit_button'] == 'presist':
            '''if condition to handle presist button pressed'''
            persistenceLayer.writeToFile(records)
            flash("Data Written to File")
# Author: Ahmed Aziz
        elif request.form['submit_button'] == 'select':
            '''if condition to handle the range selected to display when the button pressed, inner if conditions are to handle invalid range selected'''
            if request.form['min-row'] == "-1" or request.form['max-row'] == "-1":
                flash("Please select min or max row")
            elif request.form['min-row'] > request.form['max-row']:
                flash("Minimum value should not be larger than Maximum value")
            else:
                displayRange = [int(request.form['min-row'])-1,
                                int(request.form['max-row'])]
                flash("Record ID range from {} to {} displayed".format(
                    str(displayRange[0]+1), str(displayRange[1])))
# Author: Ahmed Aziz
        elif request.form['submit_button'] == 'create':
            '''if condition to handle the create button pressed and redirects to the create/edit page with index=-1 to signal creation'''
            return redirect(url_for("editCreate", index='-1'))

        elif request.form['submit_button'] == 'edit':
            '''if condition to handle the create button pressed and redirects to the edit page with the index of the record to be edited'''
            return redirect(url_for("editCreate", index=request.form['index']))

        elif request.form['submit_button'] == 'delete':
            '''if condition to handle the delete button pressed and deletes the record from the array and database and adjusts the display range accordingly'''
            deletedIndex = int(request.form['index'])
            persistenceLayer.deleteRecord(records[deletedIndex].recordID)
            flash("Record ID {} deleted".format(
                records[deletedIndex].recordID))
            del records[deletedIndex]
            displayRange = [displayRange[0], displayRange[1]-1]
# Author: Ahmed Aziz
        elif request.form['submit_button'] == 'editCreate':
            '''if condition to handle the post request from the edit/create page, if conditions checks the indexs if it's -1 then it's a new record, else edit the records with the specified index'''
            if request.form['index'] == "-1":

                newRecord = CovidRecordModel(-1, request.form['pruid'], request.form['prname'], request.form['prnameFR'], request.form['date'],
                                             request.form['numconf'], request.form['numprob'], request.form['numdeaths'], request.form['numtotal'], request.form['numtoday'], request.form['ratetotal'])
                newRecord.recordID = persistenceLayer.createRecord(newRecord)

                records.append(newRecord)
                displayRange = [displayRange[0], displayRange[1]+1]
                flash("New Record created")
            else:
                updatedIndex = int(request.form['index'])

                updatedRecord = CovidRecordModel(records[updatedIndex].recordID, request.form['pruid'], request.form['prname'], request.form['prnameFR'], request.form['date'],
                                                 request.form['numconf'], request.form['numprob'], request.form['numdeaths'], request.form['numtotal'], request.form['numtoday'], request.form['ratetotal'])

                persistenceLayer.updateRecord(updatedRecord)
                records[updatedIndex].pruid = request.form['pruid']
                records[updatedIndex].prname = request.form['prname']
                records[updatedIndex].prnameFR = request.form['prnameFR']
                records[updatedIndex].date = request.form['date']
                records[updatedIndex].numconf = request.form['numconf']
                records[updatedIndex].numprob = request.form['numprob']
                records[updatedIndex].numdeaths = request.form['numdeaths']
                records[updatedIndex].numtotal = request.form['numtotal']
                records[updatedIndex].numtoday = request.form['numtoday']
                records[updatedIndex].ratetotal = request.form['ratetotal']
                flash("Record {} edited".format(
                    records[updatedIndex].recordID))
        elif request.form['submit_button'] == 'displayAll':
            displayRange = [0, 100]
        elif request.form['submit_button'] == 'plot':
            plotColumn = request.form['plot-column']

    return render_template("presentation.html", rows=records, rowRange=displayRange, totalrows=len(records))

# Author: Ahmed Aziz


@app.route("/editCreate/<index>")
def editCreate(index):
    '''function to edit or cerate a new record based on the index passed to it'''
    global records
    if index == "-1":
        return render_template("editCreate.html", index=index, record=CovidRecordModel("", "", "", "", "", "", "", "", "", "", ""))
    else:
        return render_template("editCreate.html", index=index, record=records[int(index)])


@app.route('/plot.png')
def plot_png():
    global plotColumn

    records2 = [record.__dict__ for record in records]
    df = pd.DataFrame(records2)
    df = df.groupby(['prname'])[plotColumn].mean()

    df.plot.barh(title=plotColumn,
                 ylabel="numtotal", xlabel="Provinces and Territories")

    figure = plt.gcf()
    output = io.BytesIO()
    figure.set_figwidth(10)
    figure.set_figheight(4.4)

    FigureCanvas(figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)
    '''used to start the flask app'''

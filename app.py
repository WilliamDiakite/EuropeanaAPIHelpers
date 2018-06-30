import tasks
import csv
import shutil
import os

from tasks import long_task
from flask import Flask, render_template, request, jsonify, Response, url_for


# ---------------------------- #
#           GLOBAL             #
# ---------------------------- #

app = Flask(__name__)
app.secret_key = "EuropeanaOnTheFly"

RESULT = None


# ---------------------------- #
#           VIEWS              #
# ---------------------------- #

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/runTask", methods=['POST'])
def longtask():
    usr_data = request.json
    usr_data.update({'root': app.root_path})
    task = tasks.long_task.delay(usr_data=request.json)

    print('Background task just started')
    print(usr_data)

    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)

    # Background task at work
    if task.state == 'working':
        print('RECEIVED STATE : working')
        response = {
            'state': task.state,
            'info': task.info
        }

    # Background task is done
    elif task.state == 'SUCCESS':

        print('RECEIVED STATE : SUCCESS')
        result = task.info['info']

        # The api call returned something
        if result['query_status'] is True:
            print('No data found in query result')
            # No results found after api call
            if result['data'] is None:
                response = {
                    'state': 'empty',
                    'dir': result['dir']
                }

            # Data available after api call
            else:
                print('data available in query result')
                response = {
                    'state': 'loaded',
                    'dir': result['dir']
                }

        # There was an error during api call
        else:
            response = {
                'state': 'error',
                'dir': result['dir'],
                'error': result['error']
            }

    # Something went wrong the the background task
    else:
        print('unseen query state :', task.state)
        response = {
            'state': 'error',
            'dir': '',
            'error': 'Problème lors de la gestion de la requête'
        }

    return jsonify(response)


@app.route('/display/<dir_name>', methods=['GET', 'POST'])
def display(dir_name):

    # Read csv to display
    f_path = app.root_path + '/public/' + dir_name + '/output.csv'
    try:
        with open(f_path) as f:
            items = [i for i in csv.DictReader(f)]
    except FileNotFoundError:
        print(f_path)
        print(os.listdir('{}/public/'.format(app.root_path)))

    # Create download urls
    csv_url = '/download-csv/' + dir_name
    json_url = '/download-json/' + dir_name
    xml_url = '/download-xml/' + dir_name

    # Render template
    return render_template('display.html',
                           items=items, dir=dir_name,
                           json=json_url, csv=csv_url, xml=xml_url,
                           len=len(items))


@app.route('/cleaning/<dir_name>', methods=['GET', 'POST'])
def clean(dir_name):
    print('Cleaning demand received')
    if request.method == 'POST':
        try:
            dir_path = app.root_path + '/public/' + dir_name
            shutil.rmtree(dir_path)
            print(dir_name, ' has been removed !')
        except Exception as e:
            print('An error occured during dir cleaning : ')
            print(e)
    return '', 204


# ---------------------------- #
#         DOWLOAD VIEWS        #
# ---------------------------- #

@app.route('/download-csv/<dir_name>', methods=['GET', 'POST'])
def download_csv(dir_name):
    print('demande de téléchargement pour :', dir_name)
    file_path = app.root_path + '/public/' + dir_name + '/output.csv'
    with open(file_path) as f:
        data = f.read()
    return Response(
        data,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=europeana_data.csv"})


@app.route('/download-json/<dir_name>', methods=['GET', 'POST'])
def download_json(dir_name):
    print('demande de téléchargement pour :', dir_name)
    file_path = app.root_path + '/public/' + dir_name + '/output.json'
    with open(file_path) as f:
        data = f.read()
    return Response(
        data,
        mimetype="text/json",
        headers={"Content-disposition":
                 "attachment; filename=europeana_data.json"})


@app.route('/download-xml/<dir_name>', methods=['GET', 'POST'])
def download_xml(dir_name):
    print('demande de téléchargement pour :', dir_name)
    file_path = app.root_path + '/public/' + dir_name + '/output.xml'
    with open(file_path) as f:
        data = f.read()
    return Response(
        data,
        mimetype="text/xml",
        headers={"Content-disposition":
                 "attachment; filename=europeana_data.xml"})


# @app.errorhandler(Exception)
# def handle_error(e):
#     code = 500
#     if isinstance(e, HTTPException):
#         code = e.code
#     return render_template('error.html')

# ---------------------------- #
#           MAIN               #
# ---------------------------- #


if __name__ == "__main__":

    app.run(debug=True)

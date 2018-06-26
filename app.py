from flask import Flask, render_template, request, jsonify, session, \
    redirect, url_for, Response
from flask_socketio import SocketIO, join_room
import uuid
import tasks
import csv


app = Flask(__name__)
app.secret_key = "EuropeanaOnTheFly"

socketio = SocketIO(app, message_queue='amqp:///socketio')

RESULT = None


# ---------------------------- #
#           VIEWS              #
# ---------------------------- #

@app.route("/")
def index():
    # create a unique session id
    if 'uid' not in session:
        session['uid'] = str(uuid.uuid4())

    return render_template('index.html')


@app.route("/runTask", methods=['POST'])
def long_task():
    print('je lance la tache')
    print('RETOUR FORM')
    print(request.json)

    sid = str(session['uid'])
    task = tasks.long_task.delay(usr_data=request.json, session=sid)

    return jsonify({'id': task.id})


@app.route('/display/<dir_name>', methods=['GET', 'POST'])
def display(dir_name):

    # Read csv to display
    f_path = './tmp/' + dir_name + '/output.csv'
    with open(f_path) as f:
        items = [i for i in csv.DictReader(f)]

    # Create download urls
    csv_url = '/download-csv/' + dir_name
    json_url = '/download-json/' + dir_name

    # Render template
    return render_template('display.html',
                           items=items, dir=dir_name,
                           json=json_url, csv=csv_url)


@app.route('/download-csv/<dir_name>', methods=['GET', 'POST'])
def download_csv(dir_name):
    print('demande de téléchargement pour :', dir_name)
    file_path = './tmp/' + dir_name + '/output.csv'
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
    file_path = './tmp/' + dir_name + '/output.json'
    with open(file_path) as f:
        data = f.read()
    return Response(
        data,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=europeana_data.json"})


# ---------------------------- #
#      SOCKETS MANAGER         #
# ---------------------------- #
@socketio.on('connect')
def socket_connect():
    pass


@socketio.on('join_room', namespace='/long_task')
def on_room():
    room = str(session['uid'])
    join_room(room)


# ---------------------------- #
#           MAIN               #
# ---------------------------- #


if __name__ == "__main__":

    socketio.run(app, debug=True, host="0.0.0.0")

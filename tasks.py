import os
from celery import Celery
from flask_socketio import SocketIO
from api_caller import execute_query


celery = Celery('europeana-search')
socketio = SocketIO(message_queue='amqp:///socketio')

celery.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                   CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])


def send_message(event, namespace, room, message):
    print(message)
    socketio.emit(event, {'msg': message}, namespace=namespace, room=room)


@celery.task
def long_task(usr_data, session):

    # setting up background task
    room = session
    namespace = '/long_task'
    send_message('working', namespace, room, 'at work')

    # Execute background task
    result = execute_query(usr_data, session)

    # Return result message
    if result['query_status'] is True:
        if result['data'] is None:
            send_message('empty', namespace, room, '')
        else:
            send_message('done', namespace, room, {
                'data': result['data'],
                'dir': result['dir']})

    elif result['query_status'] == 'False':
        send_message('error', namespace, room, result['error'])

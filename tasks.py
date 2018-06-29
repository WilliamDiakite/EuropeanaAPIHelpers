from celery import Celery
from api_caller import execute_query


celery = Celery()

celery.config_from_object('celery_settings')


@celery.task(bind=True)
def long_task(self, usr_data):

    self.update_state(state='working', meta={'message': 'je suis en route'})

    # Execute background task
    result = execute_query(usr_data)

    self.update_state(state='done', meta=result)
    return {'state': 'done', 'info': result}

    # # Return result message
    # if result['query_status'] is True:
    #     if result['data'] is None:
    #         print('EMPTY DATA')
    #         self.update_state(state='done', meta={'message': 'empty'})
    #     else:
    #         print('DATA')
    #         self.update_state(state='done', meta={'message': 'ok',
    #                                               'data': result})
    #
    # elif result['query_status'] == 'False':
    #     print('ERROR')
    #     self.update_state(state='error', meta={'message': result})

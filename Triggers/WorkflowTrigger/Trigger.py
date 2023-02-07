# "template ; https://medium.com/codeshake/build-a-serverless-bigquery-ingestion-pipeline-using-cloud-workflows-f893f6b701ee"


import json
import google.auth
from google.auth.transport.requests import AuthorizedSession


def onNewFile(event, context):
    table_name = event['name'].replace(".", "_").replace("/","_")
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))
    print('table_name: {}'.format(table_name))

    scoped_credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    authed_session = AuthorizedSession(scoped_credentials)

    URL = 'https://workflowexecutions.googleapis.com/v1/projects/cloud4us-gcp-o1hoqiotj2rjjg8i9/locations/us-central1/workflows/workflow-triggers/executions'
    file_id_dict = { 'bucket': '{}'.format(event['bucket']), 'object': '{}'.format(event['name']),'table_name' :'{}'.format(table_name) }
    PARAMS = { 'argument' : json.dumps(file_id_dict) }
    response = authed_session.post(url=URL, json=PARAMS)
    print(response)
    
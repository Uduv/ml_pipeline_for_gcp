# Pipeline for Machine Learning

# General Idea

The pipeline generate and/or retrieve data from a PostgreSQL then upload the data to a GCP bucket. When the upload is finished, a Cloud Functions is triggered to generate a table on BigQuery for each file.

### Diagram of Processes

![generate,_retrieve_and_process_data.png]()

# Generate Dataset

The `generate_upload_csv.py` python file call each dataset generator and then transfers to the GCP uploader the CSVs path in order to upload them to a bucket.

## Generate Film Dataset

Datasets are generated with Faker python Package and classic random number generation. Random generation as been preferred on specific use cases rather than Faker to reduce the resources needed to generate files.

The main dataset is a 1.7Go `.csv` file of Films as the preview show below :

| Title                 | Genre       | Premiere | Runtime | Rating Score | Language | Author          |
| --------------------- | ----------- | -------- | ------- | ------------ | -------- | --------------- |
| Drive Billion Real    | Documentary | 07/01/06 | 358     | 5.697228     | English  | Danny Hudson    |
| Floor Family Worry    | Action      | 89/07/09 | 114     | 0.772004     | Italian  | John Pruitt     |
| Create First Week     | Horror      | 09/02/04 | 74      | 3.676618     | Italian  | Anthony Perez   |
| Police His Population | Comedy      | 05/06/14 | 125     | 7.304545     | Hindi    | Matthew Jackson |
| Report Country So     | Horror      | 78/07/14 | 107     | 8.982453     | Chinese  | Jason Delgado   |

---

## Generate Client Dataset

The second dataset is around 2Go \*\*\*\*`.csv` files of Client and information about their film preferences and credit score:

| name             | sex    | mail                        | client_movie_genres                                             | client_language_spoken  | client_car                 | credit_score |
| ---------------- | ------ | --------------------------- | --------------------------------------------------------------- | ----------------------- | -------------------------- | ------------ |
| Charles House    | Male   | charleshouse@gmail.com      | Horror,Thriller,Mystery                                         | Spanish,Japanese        | Kia Sorento                | 775          |
| Tiffany Parsons  | Male   | tiffanyparsons@gmail.com    | Action,Romance,Thriller,Documentary,Drama,Horror,Comedy,Mystery | Spanish,Chinese         | Mercury Villager           | 559          |
| George Maldonado | Female | georgemaldonado@hotmail.com | Action,Mystery,Thriller,Horror,Drama,Documentary,Comedy         | Japanese,Spanish        | Volkswagen Touareg         | 615          |
| Jessica Roberts  | Male   | jessicaroberts@orange.com   | Documentary,Horror,Romance                                      | Italian                 | Volvo V70                  | 473          |
| Natalie Delgado  | Female | nataliedelgado@hotmail.com  | Action,Horror,Thriller,Romance                                  | English,Spanish,Italian | Nissan NV3500 HD Passenger | 309          |

## PostgreSQL Database queried with python

A script is available to retrieve data from a PosgreSQL database then upload to GCP.

I set up an database with PostgreSQL to reproduce an system where you need to retrieve data from. Then, I query this database from python with the package `psycopg2` and process SQL request to clean and select data from a table on this database.

The dataset created is uploaded to GCP via gcloud SDK.

| Time | V1       | V2       | V3       | V4       | …   | V27      | Amount | Class |
| ---- | -------- | -------- | -------- | -------- | --- | -------- | ------ | ----- |
| 0    | -1.35981 | -0.07278 | 2.536347 | 1.378155 | …   | 0.133558 | 149.62 | 0     |
| 0    | 1.191857 | 0.266151 | 0.16648  | 0.448154 | …   | -0.00898 | 2.69   | 0     |
| 1    | -1.35835 | -1.34016 | 1.773209 | 0.37978  | …   | -0.05535 | 378.66 | 0     |
| 1    | -0.96627 | -0.18523 | 1.792993 | -0.86329 | …   | 0.062723 | 123.5  | 0     |
| 2    | -1.15823 | 0.877737 | 1.548718 | 0.403034 | …   | 0.219422 | 69.99  | 0     |
| 2    | -0.42597 | 0.960523 | 1.141109 | -0.16825 | …   | 0.253844 | 3.67   | 0     |
| 4    | 1.229658 | 0.141004 | 0.045371 | 1.202613 | …   | 0.034507 | 4.99   | 0     |

# Setup & Explore

## Upload Data to Google Cloud Platform

The script`upload_files_gcp.py` is a file uploader to GCP based on the gcloud SDK client.

In order to use the gcloud SDK , you need to set up your account on it. When set up, the SDK generate a ssh tokens in your `%AppData% local/gcloud/` folder that are needed during to process the gcloud APIs calls.

Then, you can use the function `upload_blob` which gather all needed information to login in cloud, and upload the file that you specify in parameters during the function call.

```python
def upload_blob(bucket_name="movies-personal" , source_file_name="PATH\DATASET.csv", destination_blob_name="client_remote.csv"):
    """Uploads a file to the bucket.
    The ID of your GCS \n
    bucket_name = "your-bucket-name" \n
    The path to your file to upload \n
    source_file_name = "local/path/to/file" \n
    The ID of your GCS object \n
    destination_blob_name = "storage-object-name"
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    try :
        blob.upload_from_filename(source_file_name)
    except Exception as e:
        print('You may disconnect to the VPN')
        print(e)
        exit()

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
```

## Google Cloud Storage

After enable all APIs and the proper IAM rules, a bucket on a GCP Storage is need. This bucket has an ID which will be use by GCP SDK to identity where send files on your Cloud.

## Google Cloud Functions and Workflows

[↗️Tutorial link](https://medium.com/codeshake/build-a-serverless-bigquery-ingestion-pipeline-using-cloud-workflows-f893f6b701ee)

### Idea

A Cloud Functions is listening if there is a file upload on Cloud Storage. If the file is a csv or paquet, the Functions call a Cloud Workflow to generate or append a BigQuery table.

### functioning

**Cloud Functions:**

While a file is upload to bucket, a google cloud Functions will be triggered. The Cloud Functions will generate a dictionary with all the files information (filename ,object, bucket) and transfer it to a Workflow instance.

_Code of the Cloud Functions :_

```python
import json
import google.auth
from google.auth.transport.requests import AuthorizedSession

def onNewFile(event, context):
    table_name = event['name'].replace(".", "_").replace("/","_") #  create a table name var to fit the requirement of Bigquery table name.
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))
    print('table_name: {}'.format(table_name))

    scoped_credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    authed_session = AuthorizedSession(scoped_credentials)
    if event['name'].endswith('.csv') :
        URL = 'https://workflowexecutions.googleapis.com/v1/projects/PROJECT_ID/locations/us-central1/workflows/WORKFLOW_NAME_CSV/executions'
        file_id_dict = { 'bucket': '{}'.format(event['bucket']), 'object': '{}'.format(event['name']),'table_name' :'{}'.format(table_name) }
        PARAMS = { 'argument' : json.dumps(file_id_dict) }
        response = authed_session.post(url=URL, json=PARAMS)
        print(response)
    elif event['name'].endswith('.parquet') :
        URL = 'https://workflowexecutions.googleapis.com/v1/projects/PROJECT_ID/locations/us-central1/workflows/WORKFLOW_NAME_PARQUET/executions'
        file_id_dict = { 'bucket': '{}'.format(event['bucket']), 'object': '{}'.format(event['name']),'table_name' :'{}'.format(table_name) }
        PARAMS = { 'argument' : json.dumps(file_id_dict) }
        response = authed_session.post(url=URL, json=PARAMS)
        print(response)
```

**Cloud Workflow**

Cloud Workflow is a way to de execute YAML code on call.

The Cloud Workflow instance retrieve the dictionary variable from the Cloud functions and assign to the proper variable in order to create a BigQuery table on the right dataset.

_Code of the Cloud Workflow :_

```yaml
main:
  params: [args]
  steps:
    - assign_vars:
        assign:
          - request_body : {
            "load": {
              "sourceUris": [
                "${ \"gs://\" + args.bucket + \"/\" + args.object}"
                ],
              "destinationTable": {
                "datasetId": "DATASET_NAME",
                "projectId": "PROJECT_ID",
                "tableId": "${args.table_name}"
              },
              "sourceFormat": "FORMAT",
              "autodetect": "true",
            }
          }

    - createBigQueryLoadJob:
        call: http.post
        args:
          url: https://bigquery.googleapis.com/bigquery/v2/projects/1058030566156/jobs
          body:
            configuration: ${request_body}
          headers:
            Content-Type: "application/json"
          auth:
            type: OAuth2
        result: jobLoadRes

    - getJobFinalStatus:
        call: sub_getJobFinalStatus
        args:
              joburl: ${jobLoadRes.body.selfLink}
        result: finalStatus

    - checkJobResult:
        switch:
          - condition: ${"errorResult" in finalStatus.body.status }
            raise: ${finalStatus.body.status.errors}

    - tagSourceObject:
        call: http.put
        args:
          url: "${\"https://storage.googleapis.com/storage/v1/b/\" + args.bucket + \"/o/\" + args.object }"
          body:
            metadata:
              "status": "loaded"
              "loadJobId": ${finalStatus.body.id}
          headers:
            Content-Type: "application/json"
          auth:
            type: OAuth2

    - returnResult:
        return:
          "jobStatus" : ${finalStatus}

sub_getJobFinalStatus:
    params: [joburl]
    steps:
      - sleep:
          call: sys.sleep
          args:
            seconds: 5
      - getJobCurrentStatus:
          call: http.get
          args:
            url: ${joburl}
            auth:
              type: OAuth2
          result: jobStatusRes
      - isJobFinished:
          switch:
            - condition: ${jobStatusRes.body.status.state == "DONE"}
              return: ${jobStatusRes}
          # else
          next: sleep
```

## GCP BigQuery

An SQL Procedure has been create to join tables by calling them in a procedure with a regex replacement expression.

```sql
-- Replace DATASET_NAME

CREATE OR REPLACE PROCEDURE
`DATASET_NAME.PROC_CLI_UNION_TABLE`(NAME_REGEX STRING,IS_NEW_TABLE BOOL,FILE_NAME STRING,ENV STRING )
BEGIN
DECLARE MERGED_DATE STRING;
DECLARE TABLE_NAME STRING;
DECLARE EXECUTION_QUERY STRING;
DECLARE CREATION_QUERY STRING;

SET FILE_NAME = IFNULL(FILE_NAME, "client_merged");
SET ENV = IFNULL(ENV, "DEV");
SET TABLE_NAME = CONCAT(FILE_NAME, IF(ENV = "PROD", "", CONCAT("_", ENV)));

SET CREATION_QUERY =
IF(IS_NEW_TABLE,
"CREATE OR REPLACE TABLE `DATASET_NAME.TABLE_NAME` ( name STRING,sex STRING,mail STRING,client_movie_genres STRING ,client_language_spoken STRING,client_car STRING,credit_score INT ,timestamp TIMESTAMP)", "" ) ;

SET CREATION_QUERY = REGEXP_REPLACE(CREATION_QUERY, "TABLE_NAME", TABLE_NAME);
EXECUTE IMMEDIATE CREATION_QUERY;

SET EXECUTION_QUERY =
"INSERT INTO `DATASET_NAME.TABLE_NAME` ( name ,sex ,mail ,client_movie_genres ,client_language_spoken,client_car,credit_score) SELECT DISTINCT name,sex,mail,client_movie_genres,client_language_spoken,client_car,credit_score FROM `DATASET_NAME.NAME_REGEX*` ORDER BY credit_score DESC";

SET EXECUTION_QUERY = REGEXP_REPLACE(EXECUTION_QUERY, "NAME_REGEX", NAME_REGEX);
SET EXECUTION_QUERY = REGEXP_REPLACE(EXECUTION_QUERY, "TABLE_NAME", TABLE_NAME);
EXECUTE IMMEDIATE EXECUTION_QUERY;
END;

CALL `DATASET_NAME.PROC_CLI_UNION_TABLE` ("client", TRUE,"union_client_merged", "PROD");
```

# Merge data

**Problematic :** Multiple files has been generated during the development periods and needs to be merged together. There is 3 different methods that I developed to merge data :

- A python script to merge all specifics csv files together before upload to GCP. This is not reliable method as the script doesn’t have access to files already upload to GCP.
- An auto merge on the ingress job processed by a Workflow Trigger that will append an existing table or create a new table if the datafile name is unknown. This is the most reliable and solid solution.
- A SQL procedure merging a set of dataset selected by a regex command to a new SQL table or appending an existing table. Fastidious but reliable.

## GCP Authorization required for the machine account

### Functions instance rights

- `workflows.executions.create`

### Workflows instance rights

- `bigquery.tables.create`
- `bigquery.tables.updateData`
- `bigquery.tables.update`
- `bigquery.jobs.create`
- `storage.buckets.get`
- `storage.objects.get`
- `storage.objects.list` (mandatory if you use a generic character in the URI)

### User rights

analyticshub.dataExchanges.list
apikeys.keys.create
apikeys.keys.delete
apikeys.keys.getKeyString
apikeys.keys.list
apikeys.keys.update
appengine.applications.get
appengine.instances.enableDebug
appengine.services.list
artifactregistry.locations.list
artifactregistry.repositories.list
bigquery.connections.create
bigquery.connections.list
bigquery.datasets.create
bigquery.datasets.delete
bigquery.datasets.get
bigquery.datasets.getIamPolicy
bigquery.datasets.listTagBindings
bigquery.datasets.setIamPolicy
bigquery.datasets.update
bigquery.jobs.create
bigquery.jobs.get
bigquery.jobs.list
bigquery.jobs.listAll
bigquery.models.list
bigquery.readsessions.create
bigquery.readsessions.getData
bigquery.reservationAssignments.list
bigquery.reservations.list
bigquery.routines.create
bigquery.routines.delete
bigquery.routines.get
bigquery.routines.list
bigquery.routines.update
bigquery.rowAccessPolicies.list
bigquery.savedqueries.list
bigquery.tables.getIamPolicy
bigquery.tables.setIamPolicy
bigquery.transfers.get
bigquery.transfers.update
billing.resourceCosts.get
clientauthconfig.brands.create
clientauthconfig.brands.get
clientauthconfig.brands.update
clientauthconfig.clients.create
clientauthconfig.clients.delete
clientauthconfig.clients.get
clientauthconfig.clients.getWithSecret
clientauthconfig.clients.list
clientauthconfig.clients.listWithSecrets
clientauthconfig.clients.update
cloudasset.assets.searchAllResources
cloudbuild.builds.approve
cloudbuild.builds.create
cloudbuild.builds.get
cloudbuild.builds.list
cloudbuild.builds.update
cloudbuild.connections.fetchLinkableRepositories
cloudbuild.connections.list
cloudbuild.connections.update
cloudbuild.integrations.get
cloudbuild.integrations.list
cloudbuild.repositories.create
cloudbuild.workerpools.list
cloudfunctions.functions.call
cloudfunctions.functions.create
cloudfunctions.functions.delete
cloudfunctions.functions.get
cloudfunctions.functions.getIamPolicy
cloudfunctions.functions.list
cloudfunctions.functions.setIamPolicy
cloudfunctions.functions.sourceCodeGet
cloudfunctions.functions.sourceCodeSet
cloudfunctions.functions.update
cloudfunctions.locations.list
cloudfunctions.operations.get
cloudfunctions.operations.list
cloudnotifications.activities.list
cloudscheduler.jobs.create
cloudscheduler.jobs.list
cloudscheduler.locations.list
cloudtrace.insights.list
cloudtrace.tasks.list
cloudtrace.traces.list
compute.acceleratorTypes.list
compute.addresses.create
compute.addresses.delete
compute.addresses.list
compute.disks.list
compute.diskTypes.list
compute.firewalls.create
compute.firewalls.delete
compute.firewalls.get
compute.firewalls.list
compute.forwardingRules.list
compute.globalAddresses.list
compute.globalForwardingRules.list
compute.globalOperations.get
compute.instances.addAccessConfig
compute.instances.create
compute.instances.delete
compute.instances.deleteAccessConfig
compute.instances.list
compute.instances.listReferrers
compute.instances.osLogin
compute.instances.reset
compute.instances.resume
compute.instances.setLabels
compute.instances.start
compute.instances.stop
compute.instances.suspend
compute.instanceTemplates.list
compute.machineImages.create
compute.machineTypes.list
compute.networks.addPeering
compute.networks.create
compute.networks.delete
compute.networks.get
compute.networks.getEffectiveFirewalls
compute.networks.list
compute.networks.removePeering
compute.networks.switchToCustomMode
compute.networks.update
compute.networks.updatePolicy
compute.projects.get
compute.projects.setCommonInstanceMetadata
compute.projects.setDefaultServiceAccount
compute.projects.setUsageExportBucket
compute.regions.list
compute.reservations.list
compute.resourcePolicies.create
compute.resourcePolicies.delete
compute.resourcePolicies.list
compute.routers.get
compute.routers.list
compute.routes.create
compute.routes.delete
compute.routes.list
compute.subnetworks.create
compute.subnetworks.getIamPolicy
compute.subnetworks.list
compute.subnetworks.setIamPolicy
compute.targetPools.list
compute.zones.list
consumerprocurement.entitlements.list
container.clusters.create
container.clusters.delete
container.clusters.get
container.clusters.list
container.clusters.update
container.operations.list
containeranalysis.occurrences.get
containeranalysis.occurrences.list
dataflow.jobs.create
dataflow.jobs.list
dataflow.snapshots.delete
dataflow.snapshots.list
datalineage.events.get
datalineage.locations.searchLinks
datalineage.processes.get
datalineage.runs.list
datapipelines.pipelines.list
dataproc.jobs.cancel
dataproc.jobs.create
dataproc.jobs.delete
dataproc.jobs.get
dataproc.jobs.list
dataproc.jobs.update
dataproc.operations.cancel
dataproc.operations.delete
dataproc.operations.get
dataproc.operations.list
dataproc.workflowTemplates.list
dns.policies.list
errorreporting.groups.list
eventarc.triggers.create
eventarc.triggers.list
gkehub.memberships.delete
gkehub.memberships.update
iam.roles.get
iam.roles.list
iam.serviceAccountKeys.create
iam.serviceAccountKeys.delete
iam.serviceAccountKeys.list
iam.serviceAccounts.actAs
iam.serviceAccounts.create
iam.serviceAccounts.delete
iam.serviceAccounts.disable
iam.serviceAccounts.enable
iam.serviceAccounts.get
iam.serviceAccounts.getIamPolicy
iam.serviceAccounts.list
iam.serviceAccounts.setIamPolicy
iam.serviceAccounts.update
iap.tunnelInstances.accessViaIAP
logging.logEntries.download
logging.logEntries.list
logging.logs.list
logging.logServiceIndexes.list
logging.logServices.list
logging.privateLogEntries.list
logging.queries.create
logging.queries.delete
logging.queries.get
logging.queries.list
logging.queries.listShared
logging.queries.share
logging.queries.update
logging.queries.updateShared
monitoring.alertPolicies.list
monitoring.dashboards.create
monitoring.dashboards.get
monitoring.dashboards.update
monitoring.groups.list
monitoring.metricDescriptors.list
monitoring.monitoredResourceDescriptors.get
monitoring.monitoredResourceDescriptors.list
monitoring.timeSeries.list
networkmanagement.topologygraphs.read
oauthconfig.testusers.get
oauthconfig.testusers.update
oauthconfig.verification.get
oauthconfig.verification.update
opsconfigmonitoring.resourceMetadata.list
orgpolicy.policy.get
osconfig.inventories.get
osconfig.osPolicyAssignments.create
osconfig.patchDeployments.get
osconfig.patchDeployments.list
osconfig.patchJobs.get
osconfig.patchJobs.list
osconfig.vulnerabilityReports.get
osconfig.vulnerabilityReports.list
policysimulator.replayResults.list
policysimulator.replays.create
policysimulator.replays.run
pubsub.schemas.list
pubsub.snapshots.create
pubsub.snapshots.list
pubsub.subscriptions.create
pubsub.subscriptions.list
pubsub.topics.attachSubscription
pubsub.topics.create
pubsub.topics.delete
pubsub.topics.get
pubsub.topics.getIamPolicy
pubsub.topics.list
pubsub.topics.publish
pubsub.topics.setIamPolicy
pubsub.topics.update
pubsublite.subscriptions.create
pubsublite.subscriptions.list
pubsublite.topics.create
pubsublite.topics.list
recommender.computeFirewallInsights.list
recommender.computeInstanceIdleResourceRecommendations.list
recommender.computeInstanceMachineTypeRecommendations.list
recommender.iamPolicyInsights.get
recommender.iamPolicyInsights.list
recommender.iamPolicyLateralMovementInsights.get
recommender.iamPolicyLateralMovementInsights.list
recommender.iamPolicyRecommendations.get
recommender.iamPolicyRecommendations.list
recommender.iamPolicyRecommendations.update
resourcemanager.projects.createBillingAssignment
resourcemanager.projects.get
resourcemanager.projects.getIamPolicy
resourcemanager.projects.setIamPolicy
resourcemanager.projects.update
run.services.create
run.services.setIamPolicy
secretmanager.secrets.create
secretmanager.secrets.list
secretmanager.secrets.setIamPolicy
secretmanager.versions.add
serviceusage.operations.get
serviceusage.quotas.get
serviceusage.services.enable
serviceusage.services.get
serviceusage.services.list
serviceusage.services.use
source.repos.create
source.repos.delete
source.repos.get
source.repos.list
source.repos.update
source.repos.updateRepoConfig
stackdriver.projects.get
stackdriver.resourceMetadata.list
storage.buckets.create
storage.buckets.delete
storage.buckets.list
storage.buckets.listEffectiveTags
storage.hmacKeys.list
storageinsights.reportConfigs.create
storagetransfer.jobs.create
workflows.executions.cancel
workflows.executions.create
workflows.executions.get
workflows.executions.list
workflows.operations.get
workflows.workflows.create
workflows.workflows.delete
workflows.workflows.get
workflows.workflows.list
workflows.workflows.update

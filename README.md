# Usage

This python client can be used to query the ehb-service for information about subjects and external records. The client can only be used if the user possesses an API key to access the service.

## Types of questions

An external system might be provided with a neutral [ehb-service identifier](http://github.com/chop-dbhi/biorepo-portal/wiki/Using-the-ehb-service-to-hide-external-identifiers) representing an external record. That system might need to query for information about the subject, or find the real record id used to represent the user's record in its system.

##  Example Queries

The following constants are used in the code snippets below
- EHB_HOST: This is the hostname of the ehb-service
- EHB_PATH: This is the path on on EHB_HOST where the ehb-service is mounted, in practice typically `ehb-service`
- EHB_SECURE: Whether or not the ehb-service is using SSL
- COLLECTION_PATH: This is the "Path to record collection" set on the Protocol Datasource used by an External Record
- DATASOURCE_NAME: The name of the datasource for this external record, set on the Datasource object
- API_KEY: The API token used to authenticate against the eHB service.

### Querying for external record id

Below `row_id` refers to the [neutral primary key](http://github.com/chop-dbhi/biorepo-portal/wiki/Using-the-ehb-service-to-hide-external-identifiers) of the external record in the ehb-service:

```python
    from ehb_client.requests.external_record_request_handler import ExternalRecordRequestHandler
    from ehb_client.requests.subject_request_handler import SubjectRequestHandler

    ext_rec_req = ExternalRecordRequestHandler(EHB_HOST,
            root_path=EHB_PATH,
            secure=EHB_SECURE,
            api_key=API_KEY)
    ext_rec = ext_rec_req.get(id=row_id)
    # Now we can access the real record id
    real_id = ext_rec.record_id
```

Here `ext_rec` represents an [ExternalRecord object](http://github.com/chop-dbhi/ehb-client/blob/example/ehb_client/requests/external_record_request_handler.py#L9-L18).

### Querying for subject information

Continuing from the above example, if we needed to get information about the subject, for example,
date of birth or last name:

```python
    subject_id = ext_rec.subject_id
    sub_rec_req = SubjectRequestHandler(settings.EHB_HOST,
            root_path=EHB_PATH,
            secure=EHB_SECURE,
            api_key=API_KEY)
    sub_rec = sub_rec_req.get(id = subject_id)
    # Now we can access the date of birth and last name
    dob = sub_rec.dob
    last_name = sub_rec.last_name
```

Here `sub_rec` represents a [SubjectRecord object](http://github.com/chop-dbhi/ehb-client/blob/example/ehb_client/requests/subject_request_handler.py#L8-L17).

### Querying for External Record given external record id
It less likely an application would require this, but if for some reason an application had its internal record ID and needed to get the ehb-service's corresponding External Record, the following would work. The code assumes the id we have is in `external_id`.

```python
    ext_rec_req = ExternalRecordRequestHandler(EHB_HOST,
            root_path=EHB_PATH,
            secure=EHB_SECURE,
            api_key=API_KEY)

    # Here we try to supply as much information as we have because we
    # don't have a unique identifier that we can search on like
    # was possible when we had the actual primary key (neutral id) of the
    # External Record
    ext_recs = ext_rec_req.get(external_system_name = DATASOURCE_NAME,
            path = COLLECTION_PATH)

    # Run through all matches and find the one that matches the external_id we
    # have
    ext_rec = None
    for rec in ext_recs:
        if rec.record_id == external_id:
            ext_rec = rec

    # We can now get the Subject Record the same as before by using the ext_rec.subject_id
```

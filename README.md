# AHS

#### How to start:

###### Create new secret:
```bash
$ python -c 'import secrets;print(secrets.token_urlsafe(48))'

# Out:
<YOUR_SECRET_KEY>
```
###### Create .env file and save it in project root
```bash
# .env
DEBUG=True
SECRET_KEY=<YOUR_SECRET_KEY>
DB_USER=<YOUR_DB_USERNAME>
DB_PASS=<YOUR_DB_PASSWORD>
DB_NAME=ahs_dev
DB_HOST=
DB_PORT=
DJANGO_SETTINGS_MODULE='ahs.settings'
DB_BACKUP_ON_SHUTDOWN=1
DB_RESTORE_ON_START=0
```
###### - leave DB_HOST & DB_PORT empty in order to connect django & postgres container over a UNIX socket connection. 
###### - IDE or Database Tool connects to postgres on localhost:5433
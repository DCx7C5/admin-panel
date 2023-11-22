# AsshatSuite

#### How to start:

###### Create .env file in project root:
```shell
$ echo -e 'DEBUG=True\nSECRET_KEY=' | tee .env
```

###### Create new secret:
```shell
$ python -c 'import secrets;print(secrets.token_urlsafe())'
ACl_3BY4Uu-SECRET_KEY-p09cN1QgTY
```
###### Then add key to .env
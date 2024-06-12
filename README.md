# Traffic Devils Test Task 😈 

## How to start application?
1. Build Docker container
```shell
make build 
```
2. Run built container
```shell
make run
```
3. Apply migrations
```shell
make migrations MIGRATION_NAME="name_of_the_migration"
make migrate
```
Server should start at: <b>http://0.0.0.0:8080</b>
<br>
Docs url: <b>http://0.0.0.0:8080/docs </b>


<hr>

## How to use app?
1. Restore data for dump file which located <b>dump/dump.sql</b>
2. In file <b>dump/credentials.json</b> you can find credentials for login
3. Login by one of those credentials, at result you will have JWT
4. Set this JWT into request header as Authorization: Bearer your-jwt-token...
5. Use endpoint <b>POST: /telegram/send-message </b> for sending message
6. Use endpoint <b>GET: /telegram/get-all-records </b> for fetch all responses according to your permission

<hr>
 
<p>
This task was done by Dmytro Sheptytskyi for company Traffic Devils 
as test task of hiring recruitment. <br>
Telegram: @dmytro_sheptytskyi <br>
Gmail: channektoshka@gmail.com <br>
Technology Stack: (Python, FastApi, Postgres, Sqlalchemy, Docker)
</p>

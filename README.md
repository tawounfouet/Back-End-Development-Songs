# Building a songs microservice in Flask and MongoDB


## Project Overview
In this project we built a pictures service as a microservice in Flask. 
This microservice works with MongoDB database to store lyrics of the most popular songs of the band. We used   the PyMongo python module to interact with MongoDB programatically.


## REST API Guidelines Review

The REST API guidelines are as follows:

| Action | Method | Return code | Body | URL Endpoint |
|--------|--------|-------------|------|--------------|
| List   | GET    | 200 OK      | Array of songs [{...}] | GET /song |
| Create | POST   | 201 CREATED | A song resource as json {...} | POST /song |
| Read   | GET    | 200 OK      | A song as json {...} | GET /song/{id} |
| Update | PUT    | 200 OK      | A song as json {...} | PUT /song/{id} |
| Delete | DELETE | 204 NO CONTENT | "" | DELETE /song/{id} |
| Health | GET    | 200 OK      | "" | GET /health |
| Count  | GET    | 200 OK      | "" | GET /count |
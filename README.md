# PTK

PTK project consists of a Python Django Rest Framework Dockerize API with no front-end. The app grabs information mainly from 2 sources,
api.postcodes.io to find out postcodes and nexus postcodes and from a file called 'listings.csv' to extract the desired data. The first data source is called 
over APIand the second is loaded as Pandas as is a much faster and convenient way to manipulate big amount of data.
The project returns the data in and XML format intead of JSON.
If not consist data found the app will return a 404 status Data not found
As well the project got an auth method from from Rest-auth to be able for theuser to create an account login, logout and change password as usual in the auth library.
There are some tests for main capabilities, as login, helper function check and return 200 OK for the two main views Outcodes and Nexus.

## Installation

Prerequisites: Docker installed and Python 3+
Clone/ download from repo
Install dependencies
```bash
$docker-compose build
```
Docker run
```bash
$docker-compose run
```
We need to make migrations with Docker, open new terminal to find out our docker id
```bash
$docker ps
$docker exec -it <container id> python manage.py makemigrations
```
Migrate
```bash
$docker exec -it <container id> python manage.py migrate
```
Create superuser
```bash
$docker exec -it <container id> python manage.py createsuperuser
```
name
password

Access the Application, if never acces application before go to registration
http://0.0.0.0:8000/registration/
If already an user
http://0.0.0.0:8000/api/outcode/m1/

http://0.0.0.0:8000/api/nexus/m1/


## Usage

As an User mainly you want to upload multiple files in a row, over, the endpoint http://0.0.0.0:8000/photos/file/
Use Postman as shown to upload multiple files

![image](https://user-images.githubusercontent.com/664965/114632793-b0925a00-9cbf-11eb-808c-dace36b894c2.png)

This will show the outcodes
http://0.0.0.0:8000/api/outcode/m1/


Or view users
http://0.0.0.0:8000/api/nexus/m1/

As well as part of the django rest-auth you would be able to register, login, logout, generate Token,  as User.

## How to test
Pytest been installed, to be able to test.
```bash
$docker exec -it <container id> Pytest
```
There are some test based in Unitest too 
```bash
$docker exec -it <container id> python manage.py test
```
## Impelentation
Not quite happy on how the urls end points are distributed, still thinking could be much clearer.
The uploading process as mentioned before needs new thinking with more time.
Focus on development based on messages responses.
Adding the filter and image processing capabilities to the app.
Update mysql to postgres
Microservizing with docker to communicate between apps, or maybe RabbitMQ to do async?
Pytest all application

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Future
Definitively a base platform to move deeper into microservices for future projects


# PTK

PTK project consists of a Python Django Rest Framework Dockerize API with no front-end. The app grabs information mainly from 2 sources,
api.postcodes.io to find out postcodes and nexus postcodes and from a file called 'listings.csv' to extract the desired data. The first data source is called 
over API and the second is loaded with Pandas as is a much faster and convenient way to manipulate big amount of data.
The project returns the data in and XML format intead of JSON.
If not consist data found the app will return a 404 status Data not found.
As well the project got an auth method from from Rest-auth to be able for the user to create an account login, logout and change password as usual in the auth library.
There are some tests for main capabilities, as login, helper function check and return 200 OK for the two main views Outcodes and Nexus.

## Installation

Prerequisites: Docker installed and Python 3.7 preferable to avoid conflicts.
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
or
http://0.0.0.0:8000/api/nexus/m1/


## Usage

This application is for internal purposes where the user can extract information from Manchester Postcodes. The main information 
you can extract is the amount of listings in the area and the average daily price of the area in the Outcode end point,
in the Nexus endpoint user can find nearest postcodes, with same information as above plus distance from the code user introduce
as main outcode.


End point that shows the Outcodes
http://0.0.0.0:8000/api/outcode/m1/

![image](https://user-images.githubusercontent.com/664965/116588934-685c7400-a91c-11eb-9374-e1af473fe91b.png)

End point showing the Nexus Outcodes
http://0.0.0.0:8000/api/nexus/m1/

![image](https://user-images.githubusercontent.com/664965/116594861-f8052100-a922-11eb-9d0d-b969dee13bc1.png)


## How to test
There are some test based in Unitest. Test check user creation and login, end-points to return 200 Ok and formuola to calculate the distamce based on longitude and latitude.
```bash
$docker exec -it <container id> python manage.py test
```
## Implementation
Main implementation wouldbe in the Nexus data return as it doesn't acomplish 100% the expected structured, is quitesimilar and not that complex to implement but definitively can be implemented. As well test cases are the basics and more cases can be done to make sure no bugs are in the dev process. as far I'm concern indeed there is no bugs in the app.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Future
Asmention above some test cases more and finishing the proper data implementation.


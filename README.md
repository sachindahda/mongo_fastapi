# mongo_fastapi_courses
1. Firstly Clone the repo.
2. copy .env.example to .env
3. In .env , Update all of values of database keys like db_username, db_password,db_host,db_port,db_name . These will be used to setup user for accessing database
4. Open CMD and Navigate to "mongo_fastapi" folder. 
5. Make sure you docker and docker compose installed on your system
6. Run "docker compose up --build" . It will build up the app's image from "DockerFile" , install the required libraries from "requirements.txt" file and then will run docker container
7. All the Services will be up and running.
8. Run "docker exec -it {fastapi_app_container_name} bash" and run "python3 save_courses.py" to save courses data from courses.json in mongodb database.
9. Now FastApi Server will start listening on port defined in docker-compose file (8000 in our case). It can be accessed from http://localhost:8000/docs .
10. Then all of the  APIs endpoints can be tested and validated.
11. Also endpoints can be tested using pytest framework. Run "docker exec -it {fastapi_app_container_name} bash" to go inside container (in app directory) and run "pytest -v test_endpoints.py" to test validity of all endpoints.
12. Thanks

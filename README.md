# Truckpad Backend Test

## Dependencies
- [Docker](https://www.docker.com/)

## Installation
```shell script
git clone https://github.com/enicioli/truckpad-backend-test.git
```
```shell script
cd truckpad-backend-test
```
```shell script
sudo docker-compose build && sudo docker-compose up -d
```
Two containers will be initialized:
- truckpad-backend-test-mongo (MongoDB)
- truckpad-backend-test-app (REST API connected to the host port 5000)

#### Database
![Relationship Entity Diagram](https://github.com/enicioli/truckpad-backend-test/blob/master/resources/DER.jpg)

>When the containers are running in development mode, some sample data is imported to the database.
This sample data is based in this [files](https://github.com/enicioli/truckpad-backend-test/tree/master/resources) *_samples.json

### Tests
```
sudo docker exec -it truckpad-backend-test-app sh -c "python3 -m pytest"
```

## REST API
```
POST    /trucker                            (Creates a new trucker)
GET     /trucker/:trucker_id                (Retrieves a specific trucker)
PATCH   /trucker/:trucker_id                (Updates a specific trucker - partial)
PUT     /trucker/:trucker_id                (Updates a specific trucker - full)
DELETE  /trucker/:trucker_id                (Removes a specific trucker)
GET     /trucker/available                  (Retrieves truckers that has only checked in and are not loaded)
GET     /trucker/owner                      (Retrieves truckers that has own truck)

POST    /check-in/trucker/:trucker_id       (Creates a new trucker check in)
GET     /check-in/:check_in_id              (Retrieves a specific trucker check in)
PATCH   /check-in/:check_in_id/checkout     (Updates a specific trucker check in by adding a checkout timestamp)
GET     /check-in/loaded/:days              (Counts the loaded check ins from past x days)
GET     /check-in/distribution              (Counts the check ins distribution by route and truck types)
```
[Postman](https://www.getpostman.com/) collection with some examples in [this file](https://github.com/enicioli/truckpad-backend-test/blob/master/resources/truckpad-backend-test.postman_collection.json).

#### Main technologies
- [Docker](https://www.docker.com/)
- [Python3](https://www.python.org/)
- [MongoDB](https://www.mongodb.com/)
- [Flask](https://palletsprojects.com/p/flask/)
- [MongoFrames MongoDB ODM](http://mongoframes.com/)
- [JSON Schema](http://json-schema.org/)
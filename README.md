# Characters API

This is a simple REST API for getting details of a selected Marvel character with a real-time translation to target language.

This API uses [Marvel API](https://developer.marvel.com/) as the master source of character details, syncing those to an interim storage, and serving character detgails from that replica to clients. Synching between Marvel master and local replica happens on API start, by checking for tge last modified timestamp in the local replica, and replicating changes to characters since that timestamp.

API supports in-flight translation of character's description, using [AWS Translate service](https://aws.amazon.com/translate/). Default language of character description is based on the master source (Marvel API), and is English.

## Implementation approach
* Base language of the implementation is Python 3.
* API is implemented as a REST service on Flask. 
* Local storage is implemented with SQLite, and data access is abstracted with SQLAlchemy.
* API is documented with Swagger.
* API is packaged and distributed as a Docker image.

## Pre-requisites
Create configuration file based on provided example:
```
cp .sample_env .env
```

Please update the folling parameters in `.env`:
* MARVEL_API_PUBLIC_KEY: public key for Marvel API, can be obtained at [Marvel Developer Portal](https://developer.marvel.com/)
* MARVEL_API_PRIVATE_KEY: private key for Marvel API, can be obtained at [Marvel Developer Portal](https://developer.marvel.com/)
* AWS_ACCESS_KEY_ID: AWS access key ID, can be obtained from AWS Console, IAM service
* AWS_SECRET_ACCESS_KEY: AWS secret key, can be obtained from AWS Console, IAM service

Create Docker volume:
```
docker volume create marvel-character-data
```

Build Docker image:
```
docker build --tag marvel-character-api .
```

## Running
Start Docker container:
```
docker run --mount source=marvel-character-data,destination=/app --publish 8080:8080 -d marvel-character-api
```

## Testing
Try calling from command line:
```
curl -X GET "http://localhost:8080/character"
curl -X GET "http://localhost:8080/character/1009717"
curl -X GET "http://localhost:8080/character/1009717?language=de"
```

Also, integration tests are available in `./tests/integration`, try calling by:
```
python3 -m unittest discover -s ./tests/integration -p 'test_*.py' -v
```
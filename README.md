# marvel-characters-api

docker build --tag marvel-chars .
docker run --publish 5000:5000 marvel-chars

curl -X GET "http://localhost:5000/character"
curl -X GET "http://localhost:5000/character/1009717"
curl -X GET "http://localhost:5000/character/1009717?language=de"
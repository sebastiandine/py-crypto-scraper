Build Docker image:
```
docker build -t myid/pyscraper .
```

Run with .env file
```
docker run -it --env-file .env sdine/pyscrape
```
# skwee
skwee: a url shortener with platform detection.

## Getting Started
- Download and install [Docker](https://docs.docker.com/engine/installation/) & [docker-compose](https://docs.docker.com/compose/install/)
- For this project, there is just one container that sets up and runs the Django app
   - The container is named "mservices" to represent the microservices for this URL shortener app
- First clone the repo into your destination workspace, then to run the Django Docker container, do:
   - `docker-compose up`

- That's it for setup! This command should install all dependencies then start the server.

- NOTE: Docker for Windows/Mac will run on a different IP than Docker Toolbox
   - Docker for Windows/Mac : 0.0.0.0:8000
   - Docker Toolbox : 192.168.99.100:8000 (my dev env)
      - Tried to programmatically use try/except to detect and account for this.

- To stop the server, do ctrl-C and `docker-compose down`

## Testing
- Throughout development I used Google's Postman REST client and Django Unit tests to check functionality
   - A postman collection is included if you so desire to test with Postman.
   - To run the Django unit tests, open a separate docker terminal after running `docker-compose up`
   - In the separate terminal, do `docker exec -it mservices bash`
   - Once inside of the microservices container, do `python manage.py test`

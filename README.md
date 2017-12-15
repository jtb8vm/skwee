# skwee
skwee: a url shortener with platform detection.

## Getting Started
- Download and install [Docker](https://docs.docker.com/engine/installation/) & [docker-compose](https://docs.docker.com/compose/install/)
- For this project, there is just one container that sets up and runs the Django app
   - The container is named "mservices" to represent the microservices for this URL shortener app
- To run the Django Docker container, do:
   - `docker-compose up`

- That's it for setup! This command should install all dependencies then start the server.

## Testing
- Throughout development I used Google's Postman REST client and Django Unit tests to check functionality
- The Unit tests are run by default in the `docker-compose` file
   - To run the tests for yourself, open a separate docker terminal after running `docker-compose up`
   - In the separate terminal, do `docker exec -it mservices bash`
   - Once inside of the microservices container, do `python manage.py test`

- NOTE: Docker for Windows/Mac will run on a different IP than Docker Toolbox
   - Docker for Windows/Mac : 0.0.0.0:8000
   - Docker Toolbox : 192.168.99.100:8000 (my dev env)
      - Tried to programmatically use try/except on unit tests to detect and account for this.

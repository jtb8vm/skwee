# skwee
skwee: a url shortener with platform detection.

## Getting Started
- download Docker, docker-compose (TODO: links)
- set up the MySQL DB container:
   - `docker pull mysql:5.7.14`
   - `docker run --name skwee_mysql -d -e MYSQL\_ROOT\_PASSWORD='$kw33sKWee' -v db:/var/lib/mysql  mysql:5.7.14`
   - `docker run -it --name mysql-cmdline --link mysql:db mysql:5.7.14 bash`

- run the Django Docker container:
   - `docker compose up`

# GossipBook-api
> Django API endpoitns for Gossip Book Mobile app

### Setting up 

- Clone the repository to your local machine
- [Install Docker](https://docs.docker.com/get-docker/)
- [Install docker-compose](https://docs.docker.com/compose/install/)
- Create a ```.env.dev``` file in the root directory of the project and add env variables as per ```.env.sample``` file
- Create a ```.env.prod``` file in the root directory and repeat the process above
- Create a ```.env.prod.db, .env.dev.db``` files as well required by postgresl and add database environment variables
- Run ```docker-compose -f docker-compose.dev.yml build``` or ```docker-compose build``` to build development, production docker images respectively


### Technologies used

- Docker
- Python3.8
- Django
- PostgreSQL
- Django channels
- Redis


### Available API Endpoints



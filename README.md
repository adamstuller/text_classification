# text_classification

Simple API for bachelors thesis. 

API is created to classify short text into categories. 

To run the project you need installed git, docker and docker-compose

Once you installed dependencies, clone repository:

`
git clone https://github.com/AdamStuller/text_classification.git
`

Aftewars, if you want to run project for development pusposes, run:

`
docker-compose -f docker-compose.dev.yml up 
`

For production: 

`
docker-compose -f docker-compose.prod.yml up 
`


`docker exec -t your-db-container pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql`
`cat your_dump.sql | docker exec -i your-db-container psql -U postgres`
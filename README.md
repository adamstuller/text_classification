# text_classification

Simple API for bachelors thesis. 

API is created to classify short text into categories. 

To run the project you need installed git, docker and docker-compose

Once you installed dependencies, clone repository:

`
git clone https://github.com/AdamStuller/text_classification.git
`

Note that you need SENDGRID_API_KEY environmental variable to run docker-compose properly.
Hence, if you want to run project for development purposes, run:

`
SENDGRID_API_KEY=your_sendgrid_api_key docker-compose -f docker-compose.dev.yml up 
`

For production: 

`
SENDGRID_API_KEY=your_sendgrid_api_key docker-compose -f docker-compose.prod.yml up 
`


`docker exec -t postgres_development pg_dumpall -c -U postgres_development > backups/dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql`

`cat dump_09-04-2020_22_02_11.sql | docker exec -i postgres_development psql -U postgres_development  -d text_classification_development`
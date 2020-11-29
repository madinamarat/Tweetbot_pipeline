# Tweetbot pipeline
🐳   a dockerized pipeline using ETL job. 

This pipeline includes Docker containers having the following fucntionality:
* collecting tweets via the twitter API on a given hashtag 
* storing tweets in a MongoDB
* an ETL job that transforms collected tweets and stores metadata into a Postgres database
* a sentiment analysis using Vader module
* a Slackbot which posts tweets to a specific Slack channel
* A Metabase dashboard visualizing the geodata of the tweets with sentiments, showing the average sentiment score about the given hashtag

### Tools: 
* Docker 
* MongoDB
* PostgreSQL
* API
* Slackbot
* Metabase

### Further improvement:
- to deploy to Airflow


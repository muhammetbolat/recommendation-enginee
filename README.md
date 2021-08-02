# AI Recommendation Enginee

This is a product recommendation engine microservices project.

## Getting Started
Project has 2 micro-service which are used for training and prediction, and postgresql.

### Steps
1. Install docker on your machine

2. Load events.json and meta.json files for training under the data folder.

3. Clone the repository from Github

```bash
git clone https://github.com/muhammetbolat/recommendation-enginee.git
```

4. move to main working directory

```bash
cd recommendation-enginee/
```

5. run docker-compose build 
```bash
docker-compose build
```

6. run docker-compose up
```bash
docker-compose up
```

7. Check logs on terminal. You will 3 application.
- postgresql_1: to keep log, meta-data, events, scores, useful views and so on ...
- ai-training-microservice_1: working on http://0.0.0.0:7101/ you can connect on browser. You don't need any 3rd part application for Rest-API. 

![Alt text](/Users/tcmbolat/Desktop/training.png?raw=true "Title")




### Notes
Port is changeable from configs in models

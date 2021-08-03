# AI Recommendation Enginee

This is a product recommendation engine microservices project.

## Getting Started
Project have 2 micro-service which are used for training and prediction, and a postgresql. To create tables and view, I use open-source migration project which is name ALEMBIC. It automatically creates tables and views.

## Dataset
Events.json: events data of user's cart products.
Meta.json: metada of products.

## Design
Recommendation enginee has 3 micro-services. 
![header image](https://github.com/muhammetbolat/recommendation-enginee/blob/main/documents/design.jpg)

## Entity Relationship Diagram
Pre-processed data and scores are stored in DB. Application logs are stored as well.
![header image](https://github.com/muhammetbolat/recommendation-enginee/blob/main/documents/Entity_Relationship_Diagram.jpg)

### Steps
1. Install docker on your machine

2. Clone the repository from Github

```bash
git clone https://github.com/muhammetbolat/recommendation-enginee.git
```

3. move to main directory

```bash
cd recommendation-enginee/
```

4.  run docker-compose build and wait a little time.
```bash
docker-compose build
```

5. run docker-compose up
```bash
docker-compose up
```

6. Check logs on terminal. You will 3 application.
- postgresql_1: to keep log, meta-data, events, scores, useful views and so on ...
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=123456
    POSTGRES_DB=hb
    LOCALHOST:5432

- ai-training-microservice_1: working on http://0.0.0.0:7101/ you can connect on browser. You don't need any 3rd part application for Rest-API.
  For training, you should wait around 3 minutes. You can also connect to DB to see logs, data and scores. 

  [GET] /api/recommender/training -> This method is endpoint of recommender training service

  Check logs and wait until training is finished...
  API Response will be: (it takes around 4 minutes)
    ```json
     {
      "IsSuccess": true,
      "Message": "Training succesfully is ended",
      "Result": "Success"
    }
    ```
  You can also check logs on terminal or "ai_recommendation".log table.

  ```bash
    ai-training-microservice_1    | INFO:werkzeug:192.168.112.1 - - [02/Aug/2021 09:54:07] "GET /swagger.json HTTP/1.1" 200 -
    ai-training-microservice_1    | INFO:root:2021-08-02 09:54:12.202 - INFO - Recommender training is started.
    ai-training-microservice_1    | INFO:root:2021-08-02 09:54:12.464 - INFO - 10236 # of meta data is read from the source.

    ...

    ai-training-microservice_1    | INFO:root:2021-08-02 09:58:05.382 - INFO - 10235 # of content score data is mapped to object.
    ai-training-microservice_1    | INFO:root:2021-08-02 09:58:35.318 - INFO - 10235 # of content scores are saved/updated in DB.
    ai-training-microservice_1    | INFO:root:2021-08-02 09:58:35.629 - INFO - Content based recommender training is finished.
    ai-training-microservice_1    | INFO:root:2021-08-02 09:58:35.661 - INFO - Recommender training is finished. You can use API :)
  ```



- ai-prediction-microservice_1: to finish training step, you can send products on http://0.0.0.0:9101/

  [POST] /api/recommender/prediction -> This method is endpoint of recommender prediction service
    Post request body: 

    ```json
      {
        "products": [
          "HBV00000O2SCL", "HBV00000PQJWD", "HBV00000PLGGB"
        ]
      }
    ```

    Response body:
    ```json
      {
        "IsSuccess": true,
        "Message": "recommender succesfully finished.",
        "Result": [
          "HBV00000NVZBI",
          "HBV00000PQJVR",
          "HBV00000NVZBW",
          "HBV00000O3C6Z",
          "HBV00000O2SDB",
          "HBV00000O2SC9",
          "HBV00000O2SCZ",
          "HBV00000NVZBQ",
          "HBV00000O2SES",
          "HBV00000P7VSV"
        ]
      }
    ```
  

### Notes
Port is changeable from configs in models

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
          "HBV00000A5LWZ", "HBV00000APN7J", "HBV00000QS9LY"
        ]
      }
    ```

    Response body:
    ```json
      {
        "IsSuccess": true,
        "Message": "recommender succesfully finished.",
        "Result": [
          "HBV00000NH2GZ",
          "HBV00000NH2GV",
          "HBV00000NH2H1",
          "HBV00000QS9LY",
          "HBV00000PVQBG",
          "HBV00000APN7L",
          "HBV00000QS9LW",
          "HBV00000A5AUV",
          "HBV00000SP74O",
          "ZYBICN9286411"
        ]
      }
    ```
    If you want to see more detailed result, you can use detailprediction controller.
    [POST] /api/recommender/detailprediction -> This method is endpoint of recommender prediction service with more detail.
     Post request body: 

    ```json
      {
        "products": [
          "HBV00000A5LWZ", "HBV00000APN7J", "HBV00000QS9LY"
        ]
      }
    ```

    Response body:

    ```json

    {
      "IsSuccess": true,
      "Message": "recommender succesfully finished.",
      "Result": [
        {
          "productId": "HBV00000NH2GZ",
          "similarity_score": 0.8819171036881968,
          "cart_count_score": 0.8076721360605379,
          "last_carted_day_score": 0.5257731958762887,
          "final_score": 0.7384541452083412,
          "brand": "Carrefour",
          "numberOfCart": 2156,
          "passedDay": 46,
          "category": "Su",
          "subcategory": "Su",
          "name": "Carrefour Su 5 lt"
        },
        {
          "productId": "HBV00000NH2GV",
          "similarity_score": 0.8819171036881968,
          "cart_count_score": 0.780448169688676,
          "last_carted_day_score": 0.5257731958762887,
          "final_score": 0.7293794897510538,
          "brand": "Carrefour",
          "numberOfCart": 1825,
          "passedDay": 46,
          "category": "Su",
          "subcategory": "Su",
          "name": "Carrefour Su 0,5 lt"
        },
        {
          "productId": "HBV00000NH2H1",
          "similarity_score": 0.8819171036881968,
          "cart_count_score": 0.7649697857535249,
          "last_carted_day_score": 0.5257731958762887,
          "final_score": 0.7242200284393369,
          "brand": "Carrefour",
          "numberOfCart": 1671,
          "passedDay": 46,
          "category": "Su",
          "subcategory": "Su",
          "name": "Carrefour Su 1,5 lt"
        },
        {
          "productId": "HBV00000QS9LY",
          "similarity_score": 1,
          "cart_count_score": 0.526121469448034,
          "last_carted_day_score": 0.5257731958762887,
          "final_score": 0.6839648884414409,
          "brand": "Carrefour",
          "numberOfCart": 570,
          "passedDay": 46,
          "category": "Su",
          "subcategory": "Su",
          "name": "Carrefour Discount Su 10 lt"
        },
        {
          "productId": "HBV00000PVQBG",
          "similarity_score": 0.722501018689747,
          "cart_count_score": 0.6060606060606061,
          "last_carted_day_score": 0.5471698113207547,
          "final_score": 0.6252438120237026,
          "brand": "Garnier",
          "numberOfCart": 20,
          "passedDay": 48,
          "category": "Sağlık ve Kozmetik",
          "subcategory": "El, Yüz ve Vücut Bakımı",
          "name": "Kağıt Yüz Maskesi Taze Karışım Hyaluronik Asit"
        },
        {
          "productId": "HBV00000APN7L",
          "similarity_score": 0.9459459459459456,
          "cart_count_score": 0.35,
          "last_carted_day_score": 0.5523809523809524,
          "final_score": 0.616108966108966,
          "brand": "Garnier",
          "numberOfCart": 7,
          "passedDay": 47,
          "category": "Sağlık ve Kozmetik",
          "subcategory": "El, Yüz ve Vücut Bakımı",
          "name": "Garnier Skin Naturals Kömürlü Kağıt Yüz Maskesi Siyah Çay"
        },
        {
          "productId": "HBV00000QS9LW",
          "similarity_score": 1,
          "cart_count_score": 0.3239399525941533,
          "last_carted_day_score": 0.5204081632653061,
          "final_score": 0.6147827052864865,
          "brand": "Carrefour",
          "numberOfCart": 246,
          "passedDay": 47,
          "category": "Su",
          "subcategory": "Su",
          "name": "Carrefour Discount Su 0,33 lt"
        },
        {
          "productId": "HBV00000A5AUV",
          "similarity_score": 0.7086463144289912,
          "cart_count_score": 0.5517241379310345,
          "last_carted_day_score": 0.5576923076923077,
          "final_score": 0.6060209200174445,
          "brand": "Garnier",
          "numberOfCart": 16,
          "passedDay": 46,
          "category": "Sağlık ve Kozmetik",
          "subcategory": "El, Yüz ve Vücut Bakımı",
          "name": "GARNIER SKIN NATURALS ARINDIRICI MATCHA ÇAY MASKE 8ML"
        },
        {
          "productId": "HBV00000SP74O",
          "similarity_score": 0.6904757466825007,
          "cart_count_score": 0.5666666666666667,
          "last_carted_day_score": 0.5576923076923077,
          "final_score": 0.604944907013825,
          "brand": "Garnier",
          "numberOfCart": 17,
          "passedDay": 46,
          "category": "Sağlık ve Kozmetik",
          "subcategory": "El, Yüz ve Vücut Bakımı",
          "name": "Saf Temiz Kömürlü 3İn1 150 ml"
        },
        {
          "productId": "ZYBICN9286411",
          "similarity_score": 0.77898083770452,
          "cart_count_score": 0.42543859649122795,
          "last_carted_day_score": 0.53,
          "final_score": 0.5781398113985826,
          "brand": "Pınar",
          "numberOfCart": 97,
          "passedDay": 47,
          "category": "Kahvaltılık ve Süt",
          "subcategory": "Süt",
          "name": "Pınar Süt 200 Ml"
        }
      ]
    }

    ```


### Notes
Port is changeable from configs in models

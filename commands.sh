#consumer1:
curl -X GET http://127.0.0.1:5050/health_check

#consumer2:
curl -X POST  http://127.0.0.1:5050/insert_record/PES1UG20CS408/Shreyas/G

#consumer 3:
curl -X GET http://127.0.0.1:5050/delete_record/PES1UG20CS408


#consumer 4:
curl -X GET http://localhost:5050/read_database


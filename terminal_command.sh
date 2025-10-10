 
 
# starting the server
 docker-compose up 

# listing all folders
 curl http://localhost:8000/folders | jq

# get a folder by id
 curl http://localhost:8000/folders/1 | jq

# create a folder 
curl -X POST http://localhost:8000/folders -H "Content-Type: application/json" -d '{ "title": "fourth_folder" }' | jq

# update a folder eg title
 curl -X PUT http://localhost:8000/folders/1 -H "Content-Type: application/json" -d '{ "title": "fourth_folder" }' | jq

# delete a folder
 curl -X DELETE http://localhost:8000/folders/1 -H "Content-Type: application/json" -d '{ "title": "fourth_folder" }' | jq

# add items into a folder
curl -X POST http://localhost:8000/folders/1/items -H "Content-Type: application/json" -d '{ "title": "first_item" }' | jq

# get all items in a folder
 curl http://localhost:8000/folders/1/items | jq

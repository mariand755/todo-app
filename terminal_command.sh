 
 
# starting the server
 docker-compose up -d 

# create a folder 
curl -X POST http://localhost:8000/folders -H "Content-Type: application/json" -d '{ "title": "first_folder" }' | jq

# listing all folders
 curl http://localhost:8000/folders | jq

# get a folder by id
 curl http://localhost:8000/folders/1 | jq

# update a folder eg title
 curl -X PUT http://localhost:8000/folders/1 -H "Content-Type: application/json" -d '{ "title": "fourth_folder" }' | jq

# delete a folder
 curl -X DELETE http://localhost:8000/folders/1 -H "Content-Type: application/json" -d '{ "title": "fourth_folder" }' | jq

# add item into a folder
curl -X POST http://localhost:8000/folders/1/items -H "Content-Type: application/json" -d '{ "title": "first_item" }' | jq

# get all items in a folder
 curl http://localhost:8000/folders/1/items | jq

# get a specific item in a folder
 curl http://localhost:8000/folders/1/items/1 | jq
 
# update an item in a folder
 curl -X PUT http://localhost:8000/folders/1/items/1 -H "Content-Type: application/json" -d '{ "title": "updated_item" }' | jq

# delete an item in a folder
curl -X DELETE http://localhost:8000/folders/1/items/1 | jq

# stopping the server
 docker-compose down
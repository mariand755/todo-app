const apiURL= 'http://localhost:8000';

async function makeAPICall(http_method, api_path, payload=null){
    const url = `${apiURL}${api_path}`
    const method = http_method.toUpperCase()
    if (method == 'GET'){
        try { 
            const result = await fetch(url)
            return result
        } catch(ex){
            console.log(ex)
            return null
        }
    }
    try { 
        const result = await fetch(url, {
            method: method, 
            body: payload,
            headers: {
                'Content-Type': 'text/javascript'
            }
        })
        return result
    } catch(ex){
        console.log(ex)
        return null
    }
}
const add_folder = '.add-folder'
const folder_list_id = "#folder-list"
const folder_list = document.querySelector(folder_list_id);
const create_folder_item = (json) => {
    const new_folder_item = document.createElement("li")
    new_folder_item.id = `folder_id_${json.id}`
    new_folder_item.classList.add("folder-item")
    const folder_item_contents = document.createElement("span")
    folder_item_contents.classList.add("folder-name")
    folder_item_contents.textContent = json.title
    new_folder_item.appendChild(folder_item_contents)
    const add_folder_elem = document.querySelector(add_folder)
    folder_list.insertBefore(new_folder_item, add_folder_elem)
}
    

(async () => {
	const apiResult = await makeAPICall("GET","/folders");
	console.log(apiResult);
    const responseBody = await apiResult.json();
    console.log(responseBody);   
    for(const item of responseBody){
        create_folder_item(item)
    }  
    }
)();


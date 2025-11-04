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

const item_list_id  = "#todo-list"   
const item_list = document.querySelector(item_list_id);

const create_folder_item = (json) => {
    const new_folder_item = document.createElement("li")
    new_folder_item.id = `folder_id_${json.id}`
    new_folder_item.classList.add("folder-item")
    const folder_item_contents = document.createElement("span")
    folder_item_contents.classList.add("folder-name")
    folder_item_contents.textContent = json.title
    new_folder_item.appendChild(folder_item_contents)

    const show_folder_items = async () => {
        const apiItemResult = await makeAPICall("GET",`/folders/${json.id}/items/`);
        const list_of_items = await apiItemResult.json();
        const folder_item_str = create_folder_item_list(list_of_items);
        item_list.innerHTML = folder_item_str
    }
    new_folder_item.addEventListener("click", show_folder_items )
    const add_folder_elem = document.querySelector(add_folder)
    folder_list.insertBefore(new_folder_item, add_folder_elem)
}

const create_folder_item_list = (jsonArray) => {
    let htmlstr = ""
    for(const item of jsonArray){
        const folder_item_html = `
        <li class="todo-item">
            <input type="checkbox">
            <span class="todo-text">${item.title}</span>
            <button class="delete-btn">Delete</button>
        </li>
        `
        htmlstr += folder_item_html
    }
    return htmlstr
}

(async () => {
	const apiResult = await makeAPICall("GET","/folders");
	console.log(apiResult);
    const list_of_folders = await apiResult.json();
    console.log(list_of_folders);   
    for(const item of list_of_folders){
        create_folder_item(item)
    }
    const folder = list_of_folders[0]  
    const apiItemResult = await makeAPICall("GET",`/folders/${folder.id}/items/`);
    console.log(apiItemResult);
    const list_of_items = await apiItemResult.json();
    console.log(list_of_items);
    const folder_item_str = create_folder_item_list(list_of_items);
    item_list.innerHTML = folder_item_str
    }
)();


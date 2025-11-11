import { makeAPICall } from "./api.js";

const add_folder = '.add-folder'
const folder_list_id = "#folder-list"
const folder_list = document.querySelector(folder_list_id);

const current_folder_title_id = "#current-folder-title"
const current_folder_title = document.querySelector(current_folder_title_id);

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
        // getting folder items
        const apiItemResult = await makeAPICall("GET",`/folders/${json.id}/items/`);
        const list_of_items = await apiItemResult.json();
        const folder_item_str = create_folder_item_list(list_of_items);
        item_list.innerHTML = folder_item_str

        // set active folder
        const folder_list_items = document.querySelectorAll(".folder-item")
        for (const item of folder_list_items){
            item.classList.remove("active")
        }
        new_folder_item.classList.add("active")
        
        // update folder title
        current_folder_title.innerHTML = json.title
    }
    new_folder_item.addEventListener("click", show_folder_items )
    const add_folder_elem = document.querySelector(add_folder)
    folder_list.insertBefore(new_folder_item, add_folder_elem)
}
const input_new_folder_title = async () => {
    const new_folder_input = document.querySelector("#new-folder-input")
    const title = new_folder_input.value
    const apiResult = await makeAPICall("POST","/folders", {
        title
    });
    const apiResultJson = await apiResult.json()
    create_folder_item(apiResultJson)
    new_folder_input.value = ""
}
const enter_new_folder_tiltle_option = (event) => {
    // Check if the key pressed is the Enter key
    if (event.key === 'Enter') {
        input_new_folder_title()
    }
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
    //const folder = list_of_folders[0]  
    //const apiItemResult = await makeAPICall("GET",`/folders/${folder.id}/items/`);
    //console.log(apiItemResult);
    //const list_of_items = await apiItemResult.json();
    //console.log(list_of_items);
    //const folder_item_str = create_folder_item_list(list_of_items);
    //item_list.innerHTML = folder_item_str
    //current_folder_title.innerHTML = folder.title
    const add_folder_btn = document.querySelector("#add-folder-btn")
    add_folder_btn.addEventListener("click", input_new_folder_title)
    const new_folder_input = document.querySelector("#new-folder-input")
    new_folder_input.addEventListener("keyup",enter_new_folder_tiltle_option)
    }
)();


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

(async () => {
	const apiResult = await makeAPICall("GET","/folders");
	console.log(apiResult);
    const responseBody = await apiResult.json();
    console.log(responseBody);     
    }
)();

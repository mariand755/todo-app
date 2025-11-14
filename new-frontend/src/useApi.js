const apiURL= 'http://localhost:8000';

export async function makeAPICall(http_method, api_path, payload=null){
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
            body: JSON.stringify(payload),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        return result
    } catch(ex){
        console.log(ex)
        return null
    }
}
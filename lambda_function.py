import json
import urllib.request


def makeHTTPRequest(url) -> str:
    html_content = None
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8')
    except Exception as e:
        raise Exception(e)
    return html_content


def parseHTML(html: str) -> str:
    start_tag = '<title>'
    end_tag = '</title>'
    start_index = html.find(start_tag)
    if start_index != -1:
        start_index += len(start_tag)                   # jump to index after start_tag's ">"
        end_index = html.find(end_tag, start_index)     # find index of end_tag's "<"
        if end_index != -1:
            return html[start_index:end_index].strip()  # slice the title from between the indices
    return None
    
    
responseFactory = {
    "200": lambda title: {
            'statusCode': 200,
            'body': json.dumps(title)
        },
    "500": lambda title: {
            'statusCode': 500,
            'body': json.dumps(title)
        },
}

def lambda_handler(event, context):
    response = None
    statusCode = 200
    try:
        action = event.get("httpMethod")
        resource = event.get("resource")
        pathParameters = event.get("pathParameters")
        queryStringParameters = event.get("queryStringParameters")
        body = event.get("body")
        
        parsedBody = None
        if body:
            parsedBody = json.loads(body)
        
        print("========", parsedBody)
        
        url = None
        if parsedBody:
            url = parsedBody.get('url')
            
        html = None
        if url:
            print(url)
            html = makeHTTPRequest(url)
    
        title = None
        if html:
            title = parseHTML(html)
    except Exception as e:
        statusCode = 500
    
    getResponse = responseFactory.get(str(statusCode))
    
    return getResponse(title)

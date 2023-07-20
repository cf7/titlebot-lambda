import json
import urllib.request
import os

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
            'body': json.dumps(title),
            'headers': {
                'Access-Control-Allow-Origin': os.environ['ALLOWED_ORIGINS'],
                'Content-Type': 'application/json'
            }
        },
    "500": lambda title: {
            'statusCode': 500,
            'body': json.dumps(title),
            'headers': {
                'Access-Control-Allow-Origin': os.environ['ALLOWED_ORIGINS'],
                'Content-Type': 'application/json'
            }
        },
}

def lambda_handler(event, context):
    response = None
    statusCode = 200
    title = None
        # for later
        # action = event.get("httpMethod")
        # resource = event.get("resource")
        # pathParameters = event.get("pathParameters")
        # body = event.get("body")

    queryStringParameters = event.get("queryStringParameters")
    
    print("queryStringParameters: ", queryStringParameters)
    print("url: ", queryStringParameters.get("url"))
    
    url = None
    
    if queryStringParameters:
        url = queryStringParameters.get("url")
        
    try:
        html = None
        if url:
            html = makeHTTPRequest(url)
    
        if html:
            title = parseHTML(html)
    except Exception as e:
        statusCode = 500
        
    if title is None:
        statusCode = 500
        
    getResponse = responseFactory.get(str(statusCode))
    
    print(getResponse(title))
    
    return getResponse(title)

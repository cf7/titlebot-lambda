import json
import urllib.request

from Response import Response

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

"""
## Beautiful Soup Implementation ##
from bs4 import BeautifulSoup

def parseHTML(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title')
    print(title) # Prints the tag
    print(title.string) # Prints the tag string content
    return title.string
"""

responseFactory = {
    "200": lambda title: Response(200, json.dumps(title)),
    "500": lambda title: Response(500, json.dumps(title))
}

def lambda_handler(event, context):
    statusCode = 200
    url = None
    title = None

    queryStringParameters = event.get("queryStringParameters")
    
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
    
    return getResponse(title).toDict()

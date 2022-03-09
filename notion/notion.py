import json
import requests

def retrieve_db():
    headers = {'Authorization':'Bearer secret_bu46LyZxKyjcdZuLRKeYDoHsYPYIoCgx301wsb5BKuf', 'Notion-Version':'2021-08-16', "Content-Type": "application/json"}
    # notion_page = requests.get('https://api.notion.com/v1/pages/2fbf24dccb7441f49df98518b7329def', headers=headers)

    data = {"children": [{"object": "block","type": "heading_2","heading_2": {"text": [{ "type": "text", "text": { "content": "Lacinato kale" } }]}},{"object": "block","type": "paragraph","paragraph": {"text": [{"type": "text","text": {"content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.","link": { "url": "https://en.wikipedia.org/wiki/Lacinato_kale" }}}]}}]}
    
    # notion_page = requests.patch('https://api.notion.com/v1/pages/2fbf24dccb7441f49df98518b7329def',data=json.dumps(data), headers=headers)

    notion_page = requests.patch('https://api.notion.com/v1/blocks/eecd7238c2234cb180af8da308a00c7b',data=json.dumps(data), headers=headers)
    # eecd7238c2234cb180af8da308a00c7b

    print(notion_page.json())


if __name__ == "__main__":
    retrieve_db()
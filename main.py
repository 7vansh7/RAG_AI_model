import json
import os
from llamaapi import LlamaAPI

# Initialize the llamaapi with your api_token
llama = LlamaAPI(os.environ.get('KEY'))

# Define your API request
api_request_json = {
    "messages": [
        {"role": "assistant", "content": ""},
    ],
    # "functions": [
    #     {
    #         "name": "get_current_weather",
    #         "description": "Get the current weather in a given location",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "location": {
    #                     "type": "string",
    #                     "description": "The city and state, e.g. San Francisco, CA",
    #                 },
    #                 "days": {
    #                     "type": "number",
    #                     "description": "for how many days ahead you wants the forecast",
    #                 },
    #                 "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
    #             },
    #         },
    #         "required": ["location", "days"],
    #     }
    # ],
    # "stream": False,
    # "function_call": "get_current_weather",
}
while True:
    
    content = input('\033[32m\033[4mGive your prompt\033[0m\033[0m: ')
    if content == 'exit':
        print('Bye👋')
        break
    api_request_json["messages"][0]['content'] = content
    response = llama.run(api_request_json)
    res = response.json()['choices'][0]['message']['content']
    print(res)

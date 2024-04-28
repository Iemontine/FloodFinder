import openai
import json
from web import research_coordinates
from earth import get_disaster_warnings

from flask import Flask, request, jsonify
from flask_cors import CORS

msgs = []
def handle_function_call(completion):
	global msgs
	# handle function calling
	response_message = completion.choices[0].message
	tool_calls = response_message.tool_calls
	tool_msgs = msgs.copy()
	if tool_calls:
		available_functions = {
			"research_coordinates": research_coordinates,
			"get_disaster_warnings": get_disaster_warnings,
		}
		# extend conversation with assistant's reply
		tool_msgs.append(response_message)
		# Send the info for each function call and function response to the model
		for tool_call in tool_calls:
			function_name = tool_call.function.name
			function_to_call = available_functions[function_name]
			function_args = json.loads(tool_call.function.arguments)
			if function_name == "research_coordinates":
				function_response = function_to_call(
					location=function_args.get("location")
				)
			else: # function_name == "get_disaster_warnings":
				function_response = function_to_call(
					coordinates=function_args.get("coordinates")
				)
			tool_msgs.append( # Extend conversation with function response
			{
				"tool_call_id": tool_call.id,
				"role": "tool",
				"name": function_name,
				"content": function_response,
			})
			print(f'{function_name} --> {function_response}')
		completion = openai.chat.completions.create(model="gpt-4-turbo", messages=tool_msgs)
		print(f"Tokens Used To Function Call: {str(completion.usage.total_tokens)}")
	return completion.choices[-1].message.content
tools = [
	{
		"type": "function",
		"function": {
			"name": "get_disaster_warnings",
			"description": "Returns general disaster warnings of a city using its coordinates.",
			"parameters": {
				"type": "object",
				"properties": {
					"coordinates": {"type": "string", "description": "The coordinates, e.g. X longitude, Y latitude", },
				},
				"required": ["coordinates"],
			},
		},
	},
	{
		"type": "function",
		"function": {
			"name": "research_coordinates",
			"description": "Searches the web for a city's coordinates.",
			"parameters": {
				"type": "object",
				"properties": {
					"location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA", },
				},
				"required": ["location"],
			},
		},
	},
]

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests

@app.route('/getWeather', methods=['POST'])
def get_weather():
	global msgs
	data = request.json
	location =str(data.get('location', 'Not provided'))
	print(location)
	msgs = [
		{"role": "system", "content": "Pass coordinates in the VERY SPECIFIC FORMAT: [longitude value] longitude, [latitude value] latitude. You are able to get the disaster warnings of given cities. Return 'Failure' if anything goes wrong, or if the user does not prompt a specific location. Give a EXTREMELY brief recommendation on what the user should do given the disaster warnings, if any. Ensure your final response is less than 500 characters long, responding in a single paragraph format."}, 
		{"role": "user", "content": f"Get the coordinates of {location}"}, 
	]
	completion = openai.chat.completions.create(model="gpt-4-turbo", messages=msgs, tools=tools, tool_choice="auto")
	function_response = handle_function_call(completion)
	response = completion.choices[0].message.content if not function_response else function_response
	msgs.append({"role": "assistant", "content": response})
	msgs.append({"role": "user", "content": f"Now get the disaster warnings in {location} using these coordinates."})
	completion = openai.chat.completions.create(model="gpt-4-turbo", messages=msgs, tools=tools, tool_choice="auto")
	function_response = handle_function_call(completion)
	response = completion.choices[0].message.content if not function_response else function_response

	return response

# app.run(debug=True)

location = "Sacramento CA"
msgs = [
	{"role": "system", "content": "Pass coordinates in the VERY SPECIFIC FORMAT: [longitude value] longitude, [latitude value] latitude. You are able to get the disaster warnings of given cities. Return 'Failure' if anything goes wrong, or if the user does not prompt a specific location. Give a EXTREMELY brief recommendation on what the user should do given the disaster warnings, if any. Ensure your final response is less than 500 characters long, responding in a single paragraph format."}, 
	{"role": "user", "content": f"Get the coordinates of {location}"}, 
]
completion = openai.chat.completions.create(model="gpt-4-turbo", messages=msgs, tools=tools, tool_choice="auto")
function_response = handle_function_call(completion)
response = completion.choices[0].message.content if not function_response else function_response
msgs.append({"role": "assistant", "content": response})
msgs.append({"role": "user", "content": f"Now get the disaster warnings in {location} using these coordinates."})
completion = openai.chat.completions.create(model="gpt-4-turbo", messages=msgs, tools=tools, tool_choice="auto")
function_response = handle_function_call(completion)
response = completion.choices[0].message.content if not function_response else function_response
print("response")
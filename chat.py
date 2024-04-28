import openai
import json

def handle_function_call(completion):
	# handle function calling
	response_message = completion.choices[0].message
	tool_calls = response_message.tool_calls
	tool_msgs = msgs.copy()
	if tool_calls:
		# Step 3: call the function
		available_functions = {
			"search_google": search_google,
			"search_earth_engine": search_earth_engine,
		}
		# extend conversation with assistant's reply
		tool_msgs.append(response_message)
		# Step 4: send the info for each function call and function response to the model
		for tool_call in tool_calls:
			function_name = tool_call.function.name
			function_to_call = available_functions[function_name]
			function_args = json.loads(tool_call.function.arguments)
			if function_name == "search_google":
				function_response = function_to_call(
					location=function_args.get("location")
				)
			else: # function_name == "search_earth_engine":
				function_response = function_to_call(
					coordinates=function_args.get("coordinates")
				)
			# Extend conversation with function response
			tool_msgs.append(
				{
					"tool_call_id": tool_call.id,
					"role": "tool",
					"name": function_name,
					"content": function_response,
				}
			)
			print(function_name)
		completion = openai.chat.completions.create(model="gpt-4-turbo-preview", messages=tool_msgs)
		print(f"Tokens Used To Function Call: {str(completion.usage.total_tokens)}")

		return completion.choices[-1].message.content
def search_google(location):
	#TODO: add search loop (limited to 10 searches from google)
	return "37.7749° N, 122.4194° W"
def search_earth_engine(coordinates):
	return "Success"

tools = [
	{
		"type": "function",
		"function": {
			"name": "search_google",
			"description": "Use to ensure your assumption of the coordinates of a city's coordinates is correct.",
			"parameters": {
				"type": "object",
				"properties": {
					"location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA", },
				},
				"required": ["location"],
			},
		},
	},
	{
		"type": "function",
		"function": {
			"name": "search_earth_engine",
			"description": "Returns flood data on given coordinates.",
			"parameters": {
				"type": "object",
				"properties": {
					"coordinates": {"type": "string", "description": "The coordinates of a city, e.g. AAAA.aaaa° N, BBBB.bbbb° W", },
				},
				"required": ["coordinates"],
			},
		},
	},
]
msgs = [
	{"role": "system", "content": "You must ensure your assumption of a city's coordinates is correct. After obtaining coordinates, you must perform the Earth Search function on those coordinates."}, 
	{"role": "user", "content": "Get the flood data of the city of San Francisco."}, 
]
completion = openai.chat.completions.create(model="gpt-4-turbo-preview", messages=msgs, tools=tools, tool_choice="auto")
print(f"Tokens Used To Respond: {str(completion.usage.total_tokens)}")
function_response = handle_function_call(completion)
response = completion.choices[0].message.content if not function_response else function_response

print(response)
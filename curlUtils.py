import json
import curlify
import requests
from Utils.apiUtils import is_encoded
import urllib.parse



class SplitCurl():
	def __init__(self,curl):
		self.curl = curl
		self.curl_dict = {"method":"","host":"","url":"","params":{},"headers":{},"payload":{}}
		self.curl_host = self.curl_dict["host"]
		self.curl_url = self.curl_dict["url"]
		self.curl_params = self.curl_dict["params"]
		self.curl_headers = self.curl_dict["headers"]
		self.curl_payload = self.curl_dict["payload"]

	def process_uri(self,component):
		param_indexes = [index for index, char in enumerate(component) if char == "?" or char == "&"]
			# print(param_indexes) # comment
		params_count = len(param_indexes)
		# print(f"params count: {params_count}")
		for i in range(params_count):
			if(i+1)<params_count:
				temp_split = component[param_indexes[i]+1:param_indexes[i+1]].split("=")
				# print(f"if:\t temp_split:{temp_split} \n")
				self.curl_dict['params'][temp_split[0]] = temp_split[1]
			else:
				temp_split = component[param_indexes[i]+1:len(component)].split("=")
				# print(f"else:\t temp_split:{temp_split} \n")
				self.curl_dict['params'][temp_split[0]] = temp_split[1][:-2]
		# print(f"SplitCurl.process_uri executed :params count also returned: {params_count}")
		self.curl_params = self.curl_dict["params"]
		return params_count
		
	def split_modified(self):
		str1 = self.curl.split('--')
		# print(str1)
		data_flag = False
		request_flag = False
		for component in str1:
			if "request" in component:
				request_flag = True
			if "data-raw" in component or "data" in component:
				print("\n is 'POST','PATCH', 'PUT' \n")
				data_flag = True	
		for component in str1:
			#params
			if not request_flag:
				if "location" in component:
					params_count = self.process_uri(component)
					#host and url
					uri = component.split(" ")[1]
					http_index = uri.find("http")
					com_index = uri.find(".com", http_index)
					self.curl_dict["host"] = uri[http_index:com_index + 4]
					if params_count == 0:
						self.curl_dict["url"] = uri[com_index + 4:-1]
					else:
						self.curl_dict["url"] = uri[com_index + 4:uri.find("?")]
			elif request_flag and "request" in component:
				#host and url
				params_count = self.process_uri(component)
				component_split = component.split(" ")
				if data_flag:
					self.curl_dict["method"] = component_split[1]
					print(f"first update if  {component_split[1]}")
				uri = component_split[2].split("'")[1]
				# print(uri)
				http_index = uri.find("http")
				com_index = uri.find(".com", http_index)
				self.curl_dict["host"] = uri[http_index:com_index + 4]
				if params_count == 0:
					self.curl_dict["url"] = uri[com_index + 4:]
				else:
					self.curl_dict["url"] = uri[com_index + 4:uri.find("?")]

			#headers compilation
			if "header" in component:
				rand = component.split("'")[1]
				rand2 = rand.split(": ")
				self.curl_dict["headers"][rand2[0]] = rand2[1] 

			#payload compilation
			if "data-raw" in component or "data" in component:
				temp1= component.split("'")[1]
				try:
					self.curl_dict["payload"] = json.loads(temp1)
				except Exception as e:
					print(e)
					print("--data field is empty")
			#method
   			
		print(f"self.curl_dict['method'] = {self.curl_dict['method']}\n")
		print(f"data_flag = {data_flag}\n")
		print(f"len(self.curl_dict['payload']) {len(self.curl_dict['payload'])}")
		if data_flag and len(self.curl_dict["payload"]) != 0 and self.curl_dict["method"] == "" :
			self.curl_dict["method"] = "POST"
			print(f"final method conditions POST  {self.curl_dict['method']}")
		elif self.curl_dict["method"] == "" :
			self.curl_dict["method"] = "GET"
			print(f"final method conditions GET  {self.curl_dict['method']}")
		print(f"curl_dict created : {self.curl_dict}")	

class ToCurl:
	def __init__(self,curl_dict:dict):
		self.curl_dict = curl_dict
		
	def dict_to_curl(self):
		if self.curl_dict["method"] in ["POST","PUT","PATCH"]:
			payload_json = json.dumps(self.curl_dict["payload"])
		else:
			payload_json = self.curl_dict["payload"]
		# print("???????????????????????????????????????????????????????????????????????")
		# print(f"\nToCurl function self.curl_dict['params']: {self.curl_dict['params']}\n")
		# print("???????????????????????????????????????????????????????????????????????")
		
		self.curl_dict["params"] = {key: urllib.parse.unquote(val) if is_encoded(val) else val for key, val in self.curl_dict["params"].items()}

		request = requests.Request( method=self.curl_dict["method"],url=self.curl_dict["host"] + self.curl_dict["url"],
            headers=self.curl_dict["headers"],params=self.curl_dict["params"],data=payload_json)
		prepared_request = request.prepare()
		curl_command = curlify.to_curl(prepared_request)

		return curl_command


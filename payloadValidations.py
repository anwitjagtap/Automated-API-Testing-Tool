import random
import copy
import json 


class FlattenPayload:
    def __init__(self,payload_dict = {},payload_list = []) -> None:
        self.payload_if_dict = payload_dict
        self.payload_id_list = payload_list
        self.raw_fields_dict = {}
        self.final_fields_dict = {}

    def recursively_make_cases_in_dict(self,body={},items_list=[],items_list_name= "")->dict:
        dict_of_fields = {}
        if items_list!=[]:
            sequence_in_list = -1
            for item in items_list:
                sequence_in_list+=1
                if type(item) == dict:
                    returned_dict = self.recursively_make_cases_in_dict(body=item)
                    for index,value in returned_dict.items():
                        dict_of_fields[items_list_name+"["+str(sequence_in_list)+"]"+"{}"+index] = value
    #             if type(item) == list:
    #                 if any(isinstance(obj,dict) for obj in item):
    #                     returned_list = recursively_make_cases_in_dict(items_list=,items_list_name=item)
    #                     for i in range(len(returned_list)):
    #                         list_of_fields.append(returned_list[i])
                if type(item) in [int, str, bool,float]:
                    dict_of_fields[items_list_name+"['" + item + "']"] = type(item)
            return dict_of_fields
        if body != {}:
            for key,val in body.items():
                if type(val) == dict:
                    returned_dict = self.recursively_make_cases_in_dict(body=val)
                    dict_of_fields["['"+key+"']"]= type(val)
                    for index,value in returned_dict.items():
                        dict_of_fields["['"+key+"']"+index] = value
                if type(val) == list:
                    dict_of_fields["['"+key+"']"]= type(val)
                    if any(isinstance(item,dict) for item in val):
                        returned_dict = self.recursively_make_cases_in_dict(items_list=val,items_list_name="['"+key+"']")
                        for index,value in returned_dict.items():
                            dict_of_fields[index] = value
                if type(val) in [int, str, bool,float]:
                    dict_of_fields["['"+key+"']"] = type(val)
            return dict_of_fields
    
    def make_valid_dict_keys(self,rearrange:dict)-> dict:
        new_dict = {}
        for key, value in rearrange.items():
            modified_key = key
            count = key.count("{}")
            while count:
                start = modified_key.find("{}")
                index = start + 2
                while index < len(modified_key) and (modified_key[index] != "[" and modified_key[index] != "{"):
                    index += 1
                modified_key = modified_key[:start] + "['" + modified_key[start+2:index] + "']" + modified_key[index:]
                count -= 1
            modified_key = modified_key.replace("['']", "")
            new_dict[modified_key] = value
        return new_dict
    
    def get_final_flattened_dict(self):
        self.raw_fields_dict = self.recursively_make_cases_in_dict(body = self.payload_if_dict, items_list = self.payload_id_list)
        self.final_fields_dict = self.make_valid_dict_keys(self.raw_fields_dict)
        return self.final_fields_dict


class ChangingPayloadAsNeeded:
    def __init__(self,curl_dict:dict,fields_dict:dict,operations_needed=[])->None:
        # self.operations_list = ["headers","headers_tokens_check","data_validation",
        #                    "response_headers_present","missing_fields"]
        self.fields_dict = fields_dict
        self.operations_needed = operations_needed
        self.curl = copy.deepcopy(curl_dict)

        # print(json.dumps(self.curl,sort_keys=True,indent=4,separators=(',', ': ')))
        # print(self.fields_dict)
        
    def basic_validation_changes(self,field:str):
#         print("basic_validation_changes:{}",field)
        if field == str:
            string_input = ["sjzwe73","12214352"]
            return random.choice(string_input)
        if field == int:
            int_input = [ -1,""]
            return random.choice(int_input)
        if field == float:
            float_input = [-11022,"32.43"]
            return random.choice(float_input)
        if field == dict:
            dict_input = {}
            return dict_input
        if field == list:
            list_input = []
            return list_input
        if field == bool:
            bool_input = [True,False]
            return random.choice(bool_input)
        
    def generate_payload(self,field_to_change:str,field_to_replace="",operation="replace"):
    # def generate_payload(self,field_to_change:str,field_type)://if needed to generate payloads only using different payloads are needed
        # new_payload = copy.deepcopy(self.curl_payload)
        # print(f"field_to_change:{field_to_change}")
        # print(f"field_type:{field_type}")
        flattened_fields_list = [int(x) if x.isdigit() else x.strip("[]'") for x in field_to_change.split("][")]
        print(f"fields_dict: {self.fields_dict}\n")
        print(f"flattened_fields_list: {flattened_fields_list}\n")
        current_dict = self.curl["payload"]
        print(f"curl_dict in ChangingPayloadAsNeeded : {self.curl} \n")
        
        # current_dict[flattened_fields_list[-1]] = self.basic_validation_changes(field_type)//if needed to generate payloads only using different payloads are needed
        if operation == "replace":
            for component in flattened_fields_list[:-1]:
                current_dict = current_dict[component]
                print(f"current : {current_dict}, component: {component} \n")
            current_dict[flattened_fields_list[-1]] = field_to_replace
        elif operation == "pop":
            for component in flattened_fields_list[:-1]:
                current_dict = current_dict[component]
                print(f"current : {current_dict}, component: {component} \n")
            current_dict.pop(flattened_fields_list[-1])
        return self.curl["payload"]
        
    # def data_validation(self):
        
    #     for key,val in self.fields_dict.items():
    #         # print(key)
    #         report.append(self.generate_payload(key,val))

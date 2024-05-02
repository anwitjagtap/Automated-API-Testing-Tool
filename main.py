from Utils.curlUtils import *
from Utils.sheetUtils import *
from Utils.emailUtils import *
import Utils.globalVar as gv
from Report.report import Make_Test_Cases
from Validations.payloadValidations import FlattenPayload,ChangingPayloadAsNeeded
from apis import allApis



def run_all_for_curl(curl:str,report:list,api_name)->list:
    testcase_object = Make_Test_Cases(curl,report,api_name)
    testcase_object.get_basic_sanity()
    if len(testcase_object.curl_dict["headers"]):
        testcase_object.headers_test_cases()
    if len(testcase_object.curl_dict["params"]):
        testcase_object.params_test_cases()
    if len(testcase_object.curl_dict["payload"]):
        testcase_object.payload_test_cases()

    return testcase_object.report

def generate_report():
    
    # gv.initGlobalVars()
    # gv.initUserMeta()

    module_apis = vars(allApis)
    new_sheet_created = False
    sheet_id  = "1nA9JHDqSEbkifDl6gQu-5r1OnuWaAAivJjnUtu7fzRg"
    for api_name, api_value in module_apis.items():
        if isinstance(api_value, str) and "curl" in api_value:
            # print(f"Variable name: {api_name}, cURL command: {api_value}")
            print(f"{api_value}")
            
            report = []
            print(f"\n{api_name}:{api_value}\n")
            final_report = run_all_for_curl(api_value,report,api_name)
            
            api_df = pd.DataFrame(final_report)
            sheet_object = AccessGoogleSheets(sheet_id=sheet_id, sheet_name="HERO BANNER",wk_name = api_name,df=api_df)
            print(f"{sheet_object.sheet_id} , {sheet_object.sheet_name}, {sheet_object.wk_name}, {sheet_object.df}")
            if new_sheet_created == False:
                sheet_object.df_to_sheet()
                sheet_id = sheet_object.sheet_id
                new_sheet_created =True
                print("new sheet created")
            else:
                sheet_object.create_worksheet(worksheet_name = api_name)
                print("new spreadsheet updated")
    print(f"sheet_id : {sheet_id}")

if __name__ == "__main__":
    generate_report()
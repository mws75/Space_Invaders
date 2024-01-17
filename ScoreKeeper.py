import json
from pandas import json_normalize
import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))    
    return os.path.join(base_path, relative_path)
json_file_path = resource_path("json/scores.json")

class Score_Keeper:
    def __init__(self) -> None:
        pass

    def write_to_score_card(self, user_score):
        json_user_score = {"score": user_score}

        with open(json_file_path, "r+") as file:
            file_data = json.load(file)
            file_data["scores"].append(json_user_score)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def get_top_score(self):
        top_score = 0
        
        with open(json_file_path, "r") as file: 
            file_data = json.load(file)
            
            df = json_normalize(file_data['scores'])

            df = df.sort_values(['score'])            
            df_last_record = df.tail(1)
            top_score = df_last_record.iloc[0]['score']
        return top_score

            
        
def main(): 
    sk = Score_Keeper()
    top_score = sk.get_top_score()
    print(top_score)        

main() 
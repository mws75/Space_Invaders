import json
from pandas.io.json import json_normalize

class Score_Keeper:
    def __init__(self) -> None:
        pass

    def WriteToScoreCard(self, user_score):
        json_user_score = {"score": user_score}

        with open("scores.json", "r+") as file:
            file_data = json.load(file)
            file_data["scores"].append(json_user_score)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def Get_Top_Score(self):
        top_score = 0
        
        with open("scores.json", "r") as file: 
            file_data = json.load(file)
            
            df = json_normalize(file_data['scores'])

            df = df.sort_values(['score'])
            print(df)
        return top_score

            
        
def main(): 
    sk = Score_Keeper()
    top_score = sk.Get_Top_Score()
    print(top_score)        

main() 
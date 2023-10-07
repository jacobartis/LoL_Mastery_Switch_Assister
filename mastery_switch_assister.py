import requests
import itertools

api_key = ""
champ_data = {}

#Class to hold summoner data
class Summoner:
    id = itertools.count()

    def __new__(cls,name:str,champ_data:dict,api_key:str):
        if cls.is_valid(name,api_key):
            return super(Summoner, cls).__new__(cls)
        else:
            print("Invalid summoner name or api key")
            return None

    def __init__(self,name:str,champ_data:dict,api_key:str) -> None:
        self.name = name
        self.set_puuid(api_key)
        
        self.set_mastery(champ_data,api_key)
        self.id = next(self.id)
    
    #Checks the summoner is valid
    def is_valid(name,api_key) ->bool:
        req = "https://euw1.api.riotgames.com"+"/lol/summoner/v4/summoners/by-name/"+name+"?api_key="+api_key
        res = requests.get(req).json()
        return "status" not in res.keys()
    
    def set_puuid(self,api_key):
        req = "https://euw1.api.riotgames.com"+"/lol/summoner/v4/summoners/by-name/"+self.name+"?api_key="+api_key
        res = requests.get(req).json()
        self.puuid = res["puuid"]
    
    #Creates a dictionary with mastery points as keys and champ names as values
    def set_mastery(self,champ_data:dict,api_key:str) -> None:
        res = requests.get("https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/"+self.puuid+"?api_key="+api_key)
        self.mastery = {}
        for x in res.json():
            points = x["championPoints"]
            id = x["championId"]
            self.mastery[points] = champ_data[str(id)]
    
    #Returns a list of champs of the given mastery value
    def get_champs_over_value(self,value:int) -> list:
        champ_pool = []
        for mastery in self.mastery.keys():
            if int(mastery)>=value:
                champ_pool.append(self.mastery[mastery])
        return champ_pool

#Class for managing a champ pools
class Champ_Pool:
    id = itertools.count()
    mastery: int = 0
    pool = []
    enabled_summoners = []
    all_summoners = []

    #Returns the current list of avalible champs with no duplicates
    def get_pool(self) -> list:
        self.refresh_pool()
        no_dupe_pool = []
        for champ in self.pool:
            if champ not in no_dupe_pool:
                no_dupe_pool.append(champ)
        return no_dupe_pool

    def get_pool_as(self,summoner:Summoner) -> list:
        champ_pool = self.get_pool()
        summoner_champs = summoner.get_champs_over_value(self.mastery)
        for champ in summoner_champs:
            if champ not in champ_pool:
                continue
            champ_pool.remove(champ)
        return champ_pool

    def to_json(self) -> dict:
        summoners = []
        disabled = []
        for summoner in self.all_summoners:
            summoners.append(summoner.name)
        for summoner in self.all_summoners:
            if summoner not in self.enabled_summoners:
                disabled.append(summoner.name)
        json = {
            "summoners":summoners,
            "disabled":disabled
        }
        return json

    def __init__(self) -> None:
        self.id = next(self.id)

    def __str__(self) -> str:
        return str(self.get_pool())

    #Changes the min mastery thresh hold for the champ pool 
    def set_mastery(self,new_mastery:int) -> None:
        self.mastery = new_mastery
        self.refresh_pool()

    #Updates the champ pool with current active summoners
    def refresh_pool(self):
        self.pool.clear()
        for summoner in self.enabled_summoners:
            self.pool.extend(summoner.get_champs_over_value(self.mastery))
    
    #Enables all decativated summoners
    #Allows for easy resetting after a game
    def enable_all_summoners(self) -> None:
        self.enabled_summoners = self.all_summoners
        self.refresh_pool()

    #Enables a group disabled summoners, alowing their champions to being displayed
    def enable_summoners(self,summoners:list[Summoner]) -> None:
        for summoner in summoners:
            if not isinstance(summoner,Summoner):
                continue
            for sum in self.enabled_summoners:
                if sum.puuid != summoner.puuid:
                    continue
                if sum in self.all_summoners:
                    continue
                self.enabled_summoners.append(sum)
        self.refresh_pool()

    #Adds summoners to the pool
    def add_summoners(self,summoners) -> None:
        for summoner in summoners:
            if not isinstance(summoner,Summoner):
                continue
            if summoner not in self.enabled_summoners:
                self.enabled_summoners.append(summoner)
            if summoner not in self.all_summoners:
                self.all_summoners.append(summoner)

    #Removes summoners champions from being displayed
    def disable_summoners(self,summoners:list[Summoner]) -> None:
        for summoner in summoners:
            if not isinstance(summoner,Summoner):
                continue
            for sum in self.enabled_summoners:
                if sum.puuid != summoner.puuid:
                    continue
                self.enabled_summoners.remove(sum)
        self.refresh_pool()

    #Completely removes summoners from the pool
    def remove_summoners(self,summoners:list[Summoner]) -> None:
        for summoner in summoners:
            if not isinstance(summoner,Summoner):
                continue
            for sum in self.enabled_summoners:
                if sum.puuid != summoner.puuid:
                    continue
                self.enabled_summoners.remove(sum)
                self.all_summoners.remove(sum)
        self.refresh_pool()
    
    #Clears all summoners
    def clear_summoners(self) -> None:
        self.enabled_summoners.clear()
        self.all_summoners.clear()
        self.refresh_pool()


#Returns champ data
def get_champ_data() -> dict:
    #Only calls api if champ data is empty
    if not champ_data.keys():
        champs_raw = requests.get("http://ddragon.leagueoflegends.com/cdn/13.19.1/data/en_US/champion.json").json()["data"]
        for k in champs_raw.keys():
            champ_data[champs_raw[k]["key"]] = champs_raw[k]["name"]
    return champ_data

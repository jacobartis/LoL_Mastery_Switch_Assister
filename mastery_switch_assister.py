import requests
import itertools

api_key = ""
champ_data = {}

#Class to hold summoner data
class Summoner:

    def __new__(cls,name:str,champ_data:dict,api_key:str):
        if cls.is_valid(name.lower(),api_key):
            return super(Summoner, cls).__new__(cls)
        else:
            print("Invalid summoner name or api key")
            return None

    def __init__(self,name:str,champ_data:dict,api_key:str) -> None:
        self.name = name.lower()
        self.set_puuid(api_key)
        self.set_mastery(champ_data,api_key)
    
    def __str__(self) -> str:
        return "Name: "+self.name+" ID: "+self.puuid

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
        res = requests.get("https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/"+self.puuid+"?api_key="+api_key).json()
        self.mastery = {}

        #Request doesn't return champs with 0 mastery
        #Takes copy of champ list to calculate 0 mastery champs
        champs = champ_data.copy()

        #Sets mastery for all played champs
        for x in res:
            points = x["championPoints"]
            id = x["championId"]
            self.mastery[champs[str(id)]] = points
            del champs[str(id)]
        
        #Adds champs with 0 mastery
        for champ in champs:
             self.mastery[champs[champ]] = 0
    
    #Returns a list of champs of the given mastery value
    def get_champs_over_value(self,value:int) -> list:
        champ_pool = []
        for champ in self.mastery.keys():
            if self.mastery[champ]>=value:
                champ_pool.append(champ)
        return champ_pool

    #Returns a list of champs under the given mastery value
    def get_champs_under_value(self,value:int) -> list:
        champ_pool = []
        for champ in self.mastery.keys():
            if self.mastery[champ]<=value:
                champ_pool.append(champ)
        return champ_pool

    def get_champ_mastery(self,champ_name:str) -> int:

        if "&" not in champ_name and "'" not in champ_name and " " not in champ_name:
            champ_name = champ_name.capitalize()
        
        if champ_name in self.mastery.keys():
            return self.mastery[champ_name]
        raise Exception("Input ",champ_name," is not a valid champ name.")
        return  None

    #Checks if the given object holds the same data
    def same_as(self,obj) -> bool:
        return str(self) == str(obj)

#Class for managing a champ pools
class Champ_Pool:
    id = itertools.count()
    mastery: int = 0
    pool = []
    under_pool = []
    enabled_summoners = []
    all_summoners = []

    #Returns the current list of avalible champs with no duplicates
    def get_pool(self, under=False) -> list:
        self.refresh_pool()
        no_dupe_pool = []
        pool = []
        if under:
            pool = self.under_pool
        else:
            pool = self.pool
        
        for champ in pool:
            if champ in no_dupe_pool:
                continue
            no_dupe_pool.append(champ)
        return no_dupe_pool

    #Returns the current champ pool minus the given summoners champs
    def get_pool_as(self,summoners:list[Summoner], under=False) -> list:
        champ_pool = self.get_pool(under)

        for summoner in summoners:
            summoner_champs = summoner.get_champs_over_value(self.mastery)
            for champ in summoner_champs:
                if champ not in champ_pool:
                    continue
                champ_pool.remove(champ)
        return champ_pool

    def __init__(self) -> None:
        self.id = next(self.id)
    
    #Returns the champ pool data as a dict
    def as_dict(self) -> dict:
        summoners = []
        disabled = []
        for summoner in self.all_summoners:
            summoners.append(summoner.name)
        for summoner in self.all_summoners:
            if summoner not in self.enabled_summoners:
                disabled.append(summoner.name)
        data = {
            "summoners":summoners,
            "disabled":disabled,
            "mastery":self.mastery
        }
        return data

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
        
        self.under_pool.clear()
        for summoner in self.enabled_summoners:
            self.under_pool.extend(summoner.get_champs_under_value(self.mastery))


    #Enables all decativated summoners
    #Allows for easy resetting after a game
    def enable_all_summoners(self) -> None:
        self.enabled_summoners = self.all_summoners
        self.refresh_pool()

    #Enables a group disabled summoners, alowing their champions to being displayed
    def enable_summoners(self,summoners:list[Summoner]) -> None:
        for summoner in summoners:

            #Checks each summoner is a valid summoner and is in the champ pool
            if not isinstance(summoner,Summoner):
                raise Exception(str(summoner)+" is not a valid summoner object.")
            if not get_summoner_in(summoner,self.all_summoners):
                raise Exception(summoner.name+" isn't included in the champ pool. \n Current summoners: "+"\n".join(self.all_summoners))
            
            #Enables summoner if disabled
            if not get_summoner_in(summoner,self.enabled_summoners):
                self.enabled_summoners.append(summoner)
        
        self.refresh_pool()

    #Adds summoners to the pool
    def add_summoners(self,summoners) -> None:
        for summoner in summoners:
            
            #Checks summoner is valid and not in the champ pool already
            if not isinstance(summoner,Summoner):
                raise Exception(str(summoner)+" is not a valid summoner object.")
            if get_summoner_in(summoner,self.all_summoners):
                raise Exception(summoner.name+" is already in the pool.")
            
            self.enabled_summoners.append(summoner)
            self.all_summoners.append(summoner)

    #Removes summoners champions from being displayed
    def disable_summoners(self,summoners:list[Summoner]) -> None:
        for summoner in summoners:

            #Checks summoner is valid and should be disabled
            if not isinstance(summoner,Summoner):
                raise Exception(str(summoner)+" is not a valid summoner object.")
            if not get_summoner_in(summoner,self.all_summoners):
                raise Exception(summoner.name+" isn't included in the champ pool. \n Current summoners: "+"\n".join(self.all_summoners))
            if not get_summoner_in(summoner,self.enabled_summoners):
                raise Exception(summoner.name+" is already disabled.")
            
            self.enabled_summoners.remove(get_summoner_in(summoner,self.enabled_summoners))
        self.refresh_pool()

    #Completely removes summoners from the pool
    def remove_summoners(self,summoners:list[Summoner]) -> None:
        for summoner in summoners:

            #Checks summoner is valid and in the current pool
            if not isinstance(summoner,Summoner):
                raise Exception(str(summoner)+" is not a valid summoner object.")
            if not get_summoner_in(summoner,self.all_summoners):
                raise Exception(summoner.name+" isn't included in the champ pool. \n Current summoners: "+"\n".join(self.all_summoners))
            
            #Removes summoner from the pool
            if get_summoner_in(summoner,self.enabled_summoners):
                self.enabled_summoners.remove(get_summoner_in(summoner,self.enabled_summoners))
            self.all_summoners.remove(get_summoner_in(summoner,self.all_summoners))

        self.refresh_pool()

    #Clears all summoners
    def clear_summoners(self) -> None:
        self.enabled_summoners.clear()
        self.all_summoners.clear()
        self.refresh_pool()
    

#Returns an pre-existing summoner obj from a list with the same data as the given summoner (if one exists)
def get_summoner_in(summoner:Summoner,list:list[Summoner]) -> Summoner:
    for obj in list:
        if obj.same_as(summoner):
            return obj
    return None

#Returns the given champ icon
def get_champ_icons(champs:list):
    images = []
    for champ in champs:
        champ_name = get_champ_id(champ)
        images.append(requests.get("http://ddragon.leagueoflegends.com/cdn/13.19.1/img/champion/"+champ_name+".png").content)
    return images

#Returns champ data
def get_champ_data() -> dict:
    #Only calls api if champ data is empty
    if not champ_data.keys():
        champs_raw = requests.get("http://ddragon.leagueoflegends.com/cdn/13.19.1/data/en_US/champion.json").json()["data"]
        for k in champs_raw.keys():
            champ_data[champs_raw[k]["key"]] = champs_raw[k]["name"]
    return champ_data

def get_champ_id(champ_name) -> str:
    champs_raw = requests.get("http://ddragon.leagueoflegends.com/cdn/13.19.1/data/en_US/champion.json").json()["data"]
    for key in champs_raw.keys():
        if champs_raw[key]["name"] == champ_name:
            return champs_raw[key]["id"]
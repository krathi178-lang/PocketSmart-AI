from pydantic import BaseModel,Field,field_validator
class Register(BaseModel):
    name:str=Field(min_length=2,max_length=80); email:str; password:str=Field(min_length=6,max_length=100)
class Login(BaseModel): email:str; password:str
class Home(BaseModel):
    budget:float=Field(gt=0); rooms:list[str]=Field(min_length=1); items:dict[str,int]={}; style:str='Modern'; priorities:str='value for money'
    @field_validator('rooms')
    @classmethod
    def rooms_clean(cls,v): return [x.strip() for x in v if x.strip()][:10]
class Party(BaseModel):
    budget:float=Field(gt=0); guests:int=Field(gt=0); event_type:str='Birthday'; venue:str='Home'; food_preference:str='Mixed'; decoration_style:str='Elegant'

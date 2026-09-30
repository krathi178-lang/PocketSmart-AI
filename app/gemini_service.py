import json
from google import genai
from google.genai import types
from .config import GEMINI_API_KEY,GEMINI_MODEL
from .catalog import catalog
class GeminiService:
    def __init__(self): self.client=genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
    def generate(self,kind,data,image=None,mime=None):
        cat=catalog(kind)
        if not self.client:return self.fallback(kind,data,cat,bool(image))
        prompt=f'''You are PocketSmart AI, a budget-aware recommendation assistant. Planner={kind}. User input={json.dumps(data)}. Available demo catalog={json.dumps(cat)}. Stay within budget. Do not claim live availability. Return ONLY JSON with keys summary, budget_allocation, recommendations, tips. Each recommendation must contain name, category, estimated_price, platform, reason, link. Use catalog links where possible.'''
        parts=[prompt]
        if image: parts.append(types.Part.from_bytes(data=image,mime_type=mime or 'image/jpeg'))
        try:
            r=self.client.models.generate_content(model=GEMINI_MODEL,contents=parts,config=types.GenerateContentConfig(temperature=.4,response_mime_type='application/json'))
            out=json.loads(r.text or '{}'); out.setdefault('summary','Plan generated.'); out.setdefault('budget_allocation',{}); out.setdefault('recommendations',[]); out.setdefault('tips',[])
            allowed={x['name']:x['link'] for x in cat}
            for x in out['recommendations']:
                x['estimated_price']=float(x.get('estimated_price',0) or 0); x['link']=allowed.get(x.get('name'),x.get('link','#'))
            return out
        except Exception:return self.fallback(kind,data,cat,bool(image))
    def fallback(self,kind,data,cat,image=False):
        b=float(data['budget'])
        if kind=='home': alloc={'furniture':b*.45,'lighting':b*.15,'decor':b*.2,'fans':b*.1,'reserve':b*.1}; summary=f"A {data.get('style','Modern')} home starter plan for ₹{b:,.0f}."; tips=['Buy essentials first.','Keep 10% as contingency.','Compare final prices before checkout.']; chosen=cat[:4]
        elif kind=='party': alloc={'food':b*.5,'venue':b*.2,'decoration':b*.2,'reserve':b*.1}; summary=f"A {data.get('event_type','party')} plan for {data.get('guests',0)} guests and ₹{b:,.0f}."; tips=['Confirm per-guest pricing.','Keep a small emergency buffer.','Match decor to venue size.']; chosen=cat[:4]
        else: alloc={'necklace':b*.4,'earrings':b*.25,'bracelet':b*.15,'reserve':b*.2}; summary=f"A {data.get('occasion','special occasion')} jewelry plan for ₹{b:,.0f}."; tips=['Match metal tone to the outfit.','Use one statement piece with simpler accents.']; chosen=cat[:4]
        rec=[]; remain=b
        for x in chosen:
            p=min(x['price'],remain)
            if p<=0:continue
            rec.append({'name':x['name'],'category':x['category'],'estimated_price':p,'platform':x['platform'],'reason':'Budget-conscious starter option.','link':x['link']}); remain-=p
        return {'summary':summary,'budget_allocation':{k:round(v,2) for k,v in alloc.items()},'recommendations':rec,'tips':tips,'image_analysis':'Image supplied for visual matching.' if image else None}
service=GeminiService()

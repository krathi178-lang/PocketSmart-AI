from urllib.parse import quote_plus
BASE={'Amazon':'https://www.amazon.in/s?k=','Flipkart':'https://www.flipkart.com/search?q=','IKEA':'https://www.ikea.com/in/en/search/?q=','Swiggy':'https://www.swiggy.com/search?query=','Zomato':'https://www.zomato.com/search?q=','OYO':'https://www.oyorooms.com/search?location='}
CAT={
'home':[('LED Ceiling Light','lighting',1299,'Amazon'),('Modern Ceiling Fan','fan',2499,'Flipkart'),('Compact Study Table','furniture',4999,'IKEA'),('Accent Wall Art','decor',999,'Amazon'),('Two-Seater Sofa','furniture',14999,'IKEA'),('Dining Table 4-Seater','furniture',11999,'IKEA')],
'party':[('Veg Party Catering','food',350,'Swiggy'),('Mixed Party Catering','food',450,'Zomato'),('Birthday Decoration Package','decoration',4500,'Amazon'),('LED Party Decoration Kit','decoration',1999,'Flipkart'),('Budget Event Venue','venue',8000,'OYO'),('Premium Event Venue','venue',15000,'OYO')],
'jewelry':[('Minimal Gold-Plated Jhumka','earrings',899,'Amazon'),('Silver-Tone Hoop Earrings','earrings',699,'Flipkart'),('Pearl Necklace Set','necklace',1499,'Amazon'),('Emerald-Style Pendant','necklace',1899,'Flipkart'),('Statement Bridal Necklace','necklace',3999,'Amazon'),('Delicate Bracelet','bracelet',799,'Flipkart')]}
def catalog(kind):
    return [{'name':n,'category':c,'price':p,'platform':pl,'link':BASE[pl]+quote_plus(n)} for n,c,p,pl in CAT[kind]]

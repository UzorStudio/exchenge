import pymongo
from bson import ObjectId
from datetime import datetime
from datetime import timedelta


class Base():
    def __init__(self,classterMongo):
        self.classterMongo = classterMongo
        self.classter = pymongo.MongoClient(self.classterMongo)


########################### OraculCoin

    def postListing(self,listings,type):
        db = self.classter["OraculCoin"]
        Listings = db["Listings"]




        if Listings.find_one({"coinName":{"full":listings["coinName"]["full"] ,"tiker":listings["coinName"]["tiker"]}}) is None:
            listings["post"] = False
            listings["type"] = type
            post = listings
            Listings.insert_one(post)
        else:
            print("is in base")

    def getListByTiker(self,tiker):
        db = self.classter["OraculCoin"]
        Listings = db["Listings"]
        return Listings.find_one({"coinName":{"tiker":tiker}})

    def FindNoPost(self):
        db = self.classter["OraculCoin"]
        Listings = db["Listings"]
        lst = Listings.find({"post": False})
        lists = []
        for l in lst:
            lists.append(l)
            Listings.update_one({"_id": l["_id"]},{"$set":{"post": True}})
        return lists


######################## TeleBot

    def regUser(self, usrId):
        db = self.classter["OraculCoin"]
        User = db["User"]
        da = datetime.timestamp(datetime.today())

        post = {"usrId": usrId, "balance":0, "dateReg":da, "paidto":"", "payment":False,"admin": False}
        User.insert_one(post)

    def getuser(self, usrId):
        db = self.classter["OraculCoin"]
        User = db["User"]
        return User.find_one({"usrId": usrId})

    def getAdmin(self):
        db = self.classter["OraculCoin"]
        User = db["User"]
        return User.find({"admin": True})

    def getAllUsr(self):
        db = self.classter["OraculCoin"]
        User = db["User"]
        return User.find({})

    def Pay(self,usrId):
        db = self.classter["OraculCoin"]
        User = db["User"]

        User.update_one({"usrId":usrId},{"$set":{"paidto":datetime.today()+timedelta(days=30)}})

    def PayPromo(self,usrId,promokod):
        db = self.classter["OraculCoin"]
        User = db["User"]
        Promo = db["Promo"]
        if Promo.find_one({"codName":promokod}) and usrId not in Promo.find_one({"codName":promokod})["activator"]:
            User.update_one({"usrId":usrId},{"$set":{"paidto":datetime.today()+timedelta(days=5)}})
            Promo.find_one({"codName":promokod},{"$set":{"count":Promo.find_one({"codName":promokod})["count"]-1}})
            return True
        else:
            return False

    def getAllPaymentUsr(self):
        db = self.classter["OraculCoin"]
        User = db["User"]

        usr = User.find({})
        for u in usr:
            try:
                print(f"{datetime.fromtimestamp(u['paidto'])} {datetime.today()}")
                if datetime.fromtimestamp(u["paidto"]) >= datetime.today():
                    User.update_one({"_id":u["_id"]},{"$set":{"payment":False}})
            except:
                pass


        return User.find({"payment":True})


    ############# Some PromoCod

    def regPromoCod(self,count,codName):
        db = self.classter["OraculCoin"]
        Promo = db["Promo"]
        post = {"count":count,
                "codName":codName,
                "activator":[]}
        Promo.insert_one(post)

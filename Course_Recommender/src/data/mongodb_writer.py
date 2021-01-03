from pymongo import MongoClient
def mongodb_writer(coursetype,level,rating,hours,prices):
    print(coursetype,level,rating,hours,prices)
    cluster=MongoClient("mongodb+srv://Kartik_Rana:MongoDB08@cluster0.pe5z8.mongodb.net/Course_Data?retryWrites=true&w=majority")
    db = cluster["Course_Data"]
    collection = db["Coursera_Data"]
    for i in range(len(level)):
        if(collection.find_one({"_id":i})):
            collection.update_one({"_id":i},{"$set":{"Course Name":coursetype[i],"Level":level[i],"Rating":rating[i],"Time":hours[i]+" hours","Price":prices[i]+" per month after trial period ends"}})
        else:
            doc={"_id":i,"Course Name":coursetype[i],"Level":level[i],"Rating":rating[i],"Time":hours[i]+" hours","Price":prices[i]+" per month after trial period ends"}
            collection.insert_one(doc)
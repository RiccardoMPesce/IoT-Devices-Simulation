print("Creating collections and user/password")

db = db.getSiblingDB("conf");

db.createCollection("devices");
db.createCollection("measures");


print("Done creating collections and user/password")

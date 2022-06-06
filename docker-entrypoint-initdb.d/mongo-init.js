print("Creating collections and user/password")

db = db.getSiblingDB("conf");

db.createUser(
  {
    user: "admin",
    pwd: "ds&bd2021-2022",
    roles: [{ role: "readWrite", db: "conf" }],
  },
);

db.createCollection("devices");
db.createCollection("measures");


print("Done creating collections and user/password")

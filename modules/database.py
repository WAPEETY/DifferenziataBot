from pony.orm import Database, Required, Optional

db = Database("sqlite", "../differenziatabot.db", create_db=True)

class User(db.Entity):
    chatId = Required(int)
    status = Required(str, default="normal")
    area_raccolta = Optional(str)
    tipo_raccolta = Optional(str)

db.generate_mapping(create_tables=True)
import sqlite3

#Data of Games

games = [
        "Fifa 2023",
        "Fallout 3",
        "The Last of Us",
        "Grand Theft Auto IV", 
        "Grand Theft Auto V", 
        "Batman: Arkham City", 
        "LittleBigPlanet", 
        "Red Dead Redemption",
        "Fortnite",
        "Portal 2",
        "BioShock Infinite",
        "Call of Duty: Modern Wafare 2",
        "Call of Duty 4: Modern Warfare",
        "Mass Effect 2", 
        "Street Fighter IV",
        "Metal Gear Solid 4: Guns of the Patriots",
        "Rock Band",
        "Mass Effect 3"
    ]


games = sorted(games)

connection = sqlite3.connect("games.db")

cursor = connection.cursor()
cursor.execute("create table games (id integer primary key autoincrement, name text)")

cursor.execute("create table users (username text not null, password text not null)")

for i in range(len(games)):
    cursor.execute("insert into games (name) values (?)", [games[i]])
    print("added", games[i])


connection.commit()
connection.close()
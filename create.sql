CREATE TABLE IF NOT EXISTS "Houses" (
	"id"	INTEGER,
	"street"	TEXT NOT NULL,
	"house_number"	INTEGER NOT NULL,
	"area"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Users" (
	"id"	INTEGER UNIQUE NOT NULL,
	"name"	TEXT NOT NULL,
	"phone"	TEXT NOT NULL,
	"house_id"	INTEGER,
	"flat"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Events" (
    "id"    INTEGER UNIQUE,
    "type"  TEXT NOT NULL, -- can be "emergency", "scheduled work", "unscheduled work", "ads"
    "description"   TEXT,
    "start" DATETIME NOT NULL,
    "end"   DATETIME NOT NULL,
    "house_id"  INTEGER,
    "area"  TEXT
    "target"    TEXT NOT NULL, -- can be "house", "area", "all"
	PRIMARY KEY("id" AUTOINCREMENT)
)
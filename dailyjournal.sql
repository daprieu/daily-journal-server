CREATE TABLE `Moods` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `mood` TEXT NOT NULL
);

CREATE TABLE `Entries` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`date`	TEXT NOT NULL,
	`concept`	TEXT NOT NULL,
    `entry`	TEXT NOT NULL,
    `mood_id` INTEGER,
	FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)
);

INSERT INTO `Moods` VALUES (null, "Joyful");
INSERT INTO `Moods` VALUES (null, "Happy");
INSERT INTO `Moods` VALUES (null, "Relaxed");
INSERT INTO `Moods` VALUES (null, "Confused");
INSERT INTO `Moods` VALUES (null, "Sad");
INSERT INTO `Moods` VALUES (null, "Anxious");
INSERT INTO `Moods` VALUES (null, "Angry");

INSERT INTO `Entries` VALUES (null, "2021-04-15", "SQL", "bad python", 7);
INSERT INTO `Entries` VALUES (null, "2021-04-15", "SQL", "bad python", 7);

SELECT
	e.id,
	e.date,
	e.concept,
	e.entry,
	e.mood_id,
	m.mood mood
FROM Entries e
LEFT JOIN Moods m
	ON m.id = e.mood_id

CREATE TABLE `Tag` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL
);

CREATE TABLE `Entry_Tag` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id` INTEGER NOT NULL,
	`tag_id` INTEGER NOT NULL,
	FOREIGN KEY(`entry_id`) REFERENCES `Entries`(`id`),
	FOREIGN KEY(`tag_id`) REFERENCES `Tag`(`id`)
);

INSERT INTO `Tag` VALUES (null, 'tag?');
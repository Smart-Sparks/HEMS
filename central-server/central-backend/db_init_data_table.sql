
CREATE TABLE IF NOT EXISTS 'data' (
	homeid INTEGER NOT NULL,
	time DATETIME NOT NULL,
    irms DOUBLE NOT NULL,
    pwr DOUBLE NOT NULL,
    pf DOUBLE NOT NULL,
    energy DOUBLE NOT NULL,
	FOREIGN KEY (homeid)
		REFERENCES 'homes' (homeid)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);
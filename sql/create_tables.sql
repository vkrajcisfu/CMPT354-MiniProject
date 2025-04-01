CREATE TABLE IF NOT EXISTS User (
	uid INTEGER PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
	phone_num VARCHAR(15) NOT NULL
);
CREATE TABLE IF NOT EXISTS Item (
	iid INTEGER PRIMARY KEY,
	title VARCHAR(100) NOT NULL,
	item_type VARCHAR(50) NOT NULL,
	status VARCHAR(50) NOT NULL,
	added_date DATE NOT NULL,
	quantity INT NOT NULL
);
CREATE TABLE IF NOT EXISTS Record (
	rid INTEGER,
	uid INT NOT NULL,
	iid INT NOT NULL,
	borrow_date DATE NOT NULL,
	return_date DATE NOT NULL,
	fine_amount INT NOT NULL,
	PRIMARY KEY (rid, uid, iid),
	FOREIGN KEY (uid) REFERENCES User(uid),
	FOREIGN KEY (iid) REFERENCES Item(iid)
);
CREATE TABLE IF NOT EXISTS Event (
	eid INTEGER PRIMARY KEY,
	event_name VARCHAR(100) NOT NULL,
	event_type VARCHAR(50) NOT NULL,
	audience VARCHAR(100) NOT NULL,
	date DATE NOT NULL,
	room VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS Personnel (
	pid INTEGER PRIMARY KEY,
	occupation VARCHAR(100) NOT NULL,
	name VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
	phone_number VARCHAR(15) NOT NULL
);
CREATE TABLE IF NOT EXISTS RegisterFor (
	uid INT NOT NULL,
	eid INT NOT NULL,
	register_date DATE NOT NULL,
	PRIMARY KEY (uid, eid),
	FOREIGN KEY (uid) REFERENCES User(uid),
	FOREIGN KEY (eid) REFERENCES Event(eid)
);
CREATE TABLE IF NOT EXISTS Volunteer (
	vid INTEGER PRIMARY KEY, -- cant auto increment a composite primary key (vid, uid)
	uid INT NOT NULL UNIQUE, -- so have to declare uid unique to maintain functionality
	total_hours INT NOT NULL, -- as if primary key is (vid, uid)
	start_date DATE NOT NULL,
	FOREIGN KEY (uid) REFERENCES User(uid)
);
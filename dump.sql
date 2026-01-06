PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(120) NOT NULL, 
	role VARCHAR(20) NOT NULL, 
	phone VARCHAR(15), 
	department VARCHAR(100), 
	created_at DATETIME, 
	is_active BOOLEAN, 
	email_verified BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);
INSERT INTO user VALUES(1,'admin','admin@roadmaintenance.com','pbkdf2:sha256:600000$60VablB5KrnbrtDm$077dd73a53c39a44b46107e8ce9bab092b13addc9ce5431a3293ff6dc1ed4f03','authority',NULL,'Municipal Corporation','2025-09-07 02:13:01.014573',1,0);
INSERT INTO user VALUES(2,'Aditya','6kw4n58z1p@zudpck.com','pbkdf2:sha256:600000$1nP8NNVYBpjVUVFP$3ac66fe4918b0e79fe93165a5067cff03709202e21a64294779bda776044a681','citizen','8317023767',NULL,'2025-09-07 02:28:12.734363',1,1);
INSERT INTO user VALUES(3,'AnshikaSingh','aditya463615@gmail.com','pbkdf2:sha256:600000$ylkoCedL8uUtvmnB$08840be58916436959049abcb742ebd576d8e4a3efb5e66d840a21f5c5fa9238','citizen','8317023767',NULL,'2025-09-07 05:35:07.255046',1,1);
INSERT INTO user VALUES(4,'Sakshi gond','sakshigond6234@gmail.com','pbkdf2:sha256:600000$Sk9iJiIDotRHrhpM$47071efe9231858d0c99c0053d6c8885eedc23709f51a10ed7a06cc87be5e3a8','citizen','8787046827',NULL,'2025-09-07 06:37:36.212488',1,1);
INSERT INTO user VALUES(5,'Anshika singh','anshikasinghclg@gmail.com','pbkdf2:sha256:600000$2lV7FMGDjr25k1ef$97517906971559a2d48098b9b1129ff48f9108f7d57376ce63b87d24d2fc6699','citizen','9838215444',NULL,'2025-09-07 14:35:20.406591',1,1);
INSERT INTO user VALUES(6,'Shristy','shristysingh941@gmail.com','pbkdf2:sha256:600000$IkX4hEPbuTeg48RD$aab5c5181e7dc6e0ff1f8ace1d6599b83f6a553d478ed4063fff55ab2c2f5997','authority','9838215444','xyz','2025-09-07 14:54:14.413381',1,1);
INSERT INTO user VALUES(7,'Rahul','hwd6mt0bb2@osxofulk.com','pbkdf2:sha256:600000$vR0THD27OcdefpqA$66bfd50195297bb07d7128be35eb4c84d4fbe65c0084616535f3c1cba7e8e2a9','authority','8317023767','xyz','2025-09-07 14:55:21.712257',1,1);
INSERT INTO user VALUES(8,'Anshika','anshika1gh@gmail.com','pbkdf2:sha256:600000$GXNdKHFocCCIzjG8$9c97efe00faccb83b4054f72c94456b146e6dae8a32eda21be2ba2b2ea5244ef','citizen','9838215444',NULL,'2025-09-07 15:02:03.278954',1,1);
INSERT INTO user VALUES(9,'Rohan','ulgu1wwnid@cmhvzylmfc.com','pbkdf2:sha256:600000$dZHT4ASZUYzwgm1x$591e326fbea8240d582f87e7d83c0b47b3879c04c877b2f7cd09a6871983b5d4','citizen','999999999999999',NULL,'2025-09-08 13:29:23.249288',1,1);
INSERT INTO user VALUES(10,'Satish Dhiwar','dhiwarsatish009@gmail.com','pbkdf2:sha256:600000$BGtyM05r48vfEE47$b6d12ec57ebfb60d956cc6a4c49a04ce06cab8aa753d5ae85c97c4af5c48ec79','citizen','7869061859',NULL,'2025-09-09 06:34:49.582836',1,1);
CREATE TABLE analytics (
	id INTEGER NOT NULL, 
	metric_name VARCHAR(100) NOT NULL, 
	metric_value FLOAT NOT NULL, 
	date_recorded DATE, 
	category VARCHAR(50), 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE TABLE otp_verification (
	id INTEGER NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	otp_code VARCHAR(6) NOT NULL, 
	purpose VARCHAR(50) NOT NULL, 
	expires_at DATETIME NOT NULL, 
	is_used BOOLEAN, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
INSERT INTO otp_verification VALUES(1,'6kw4n58z1p@zudpck.com','941660','registration','2025-09-07 02:37:31.886748',1,'2025-09-07 02:27:31.889414');
INSERT INTO otp_verification VALUES(2,'38i3q1obdf@osxofulk.com','559000','registration','2025-09-07 02:49:28.792107',0,'2025-09-07 02:39:28.792107');
INSERT INTO otp_verification VALUES(3,'6kw4n58z1p@zudpck.com','333400','password_reset','2025-09-07 02:58:19.317913',0,'2025-09-07 02:48:19.320610');
INSERT INTO otp_verification VALUES(4,'aditya463615@gmail.com','393937','registration','2025-09-07 05:43:30.905502',1,'2025-09-07 05:33:30.908448');
INSERT INTO otp_verification VALUES(5,'aditya463615@gmail.com','155611','password_reset','2025-09-07 06:04:47.305007',0,'2025-09-07 05:54:47.305007');
INSERT INTO otp_verification VALUES(6,'saskhigond6234@gmail.com','962686','registration','2025-09-07 06:45:13.977786',0,'2025-09-07 06:35:13.983917');
INSERT INTO otp_verification VALUES(7,'sakshigond6234@gmail.com','297003','registration','2025-09-07 06:46:43.620633',1,'2025-09-07 06:36:43.621672');
INSERT INTO otp_verification VALUES(8,'anshikasinghclg@gmail.com','079185','registration','2025-09-07 14:44:24.377041',1,'2025-09-07 14:34:24.377041');
INSERT INTO otp_verification VALUES(9,'anshikasinghclg@gmail.com','526422','password_reset','2025-09-07 14:45:58.873843',1,'2025-09-07 14:35:58.873843');
INSERT INTO otp_verification VALUES(10,'shristysingh941@gmail.com','545677','registration','2025-09-07 15:03:55.126562',1,'2025-09-07 14:53:55.131189');
INSERT INTO otp_verification VALUES(11,'hwd6mt0bb2@osxofulk.com','326002','registration','2025-09-07 15:04:28.782371',1,'2025-09-07 14:54:28.783372');
INSERT INTO otp_verification VALUES(12,'anshika1gh@gmail.com','300346','registration','2025-09-07 15:11:27.472762',1,'2025-09-07 15:01:27.473275');
INSERT INTO otp_verification VALUES(13,'ulgu1wwnid@cmhvzylmfc.com','994781','registration','2025-09-08 13:38:40.325954',1,'2025-09-08 13:28:40.336474');
INSERT INTO otp_verification VALUES(14,'anshikasinghclg@gmail.com','627511','password_reset','2025-09-08 13:54:45.034749',1,'2025-09-08 13:44:45.037373');
INSERT INTO otp_verification VALUES(15,'dhiwarsatish009@gmail.com','652472','registration','2025-09-09 06:44:18.972097',1,'2025-09-09 06:34:18.972097');
CREATE TABLE report (
	id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	description TEXT NOT NULL, 
	category VARCHAR(50) NOT NULL, 
	severity VARCHAR(20) NOT NULL, 
	latitude FLOAT NOT NULL, 
	longitude FLOAT NOT NULL, 
	address VARCHAR(300), 
	photo_path VARCHAR(200), 
	status VARCHAR(20), 
	user_id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO report VALUES(1,'Drainage Problem','There is some drainage issue near the main highway ','drainage','medium',28.6311798423645456,77.2169581517009362,'Outer Circle, Connaught Place, Chanakya Puri Tehsil, New Delhi, Delhi, 110001, India','static/uploads\6b2e76a0-9c1d-4eda-92f1-8c3c02a3ded6_Commercial-Drain-Cleaning-Maintain-Drains-1024x768.jpeg','verified',3,'2025-09-07 05:41:11.631198','2025-09-07 20:03:40.561485');
INSERT INTO report VALUES(2,'fuse off, broken and  fully damage of  street light','fuse off, broken and  fully damage of  street light','lighting','low',26.4499229999999982,80.3318735999999944,'NH34, Kidwai Nagar, Kanpur, Kanpur Nagar, Uttar Pradesh, 208003, India','static/uploads\c9a7e85a-39df-43ea-95fb-ba7b5b6d970b_boken_steet_light.jpg','in_progress',4,'2025-09-07 06:49:37.636459','2025-09-07 07:01:24.108662');
INSERT INTO report VALUES(3,'road cracked','cracked road in my area.','crack','medium',26.726979,83.430176000000003,'Gorakhpur, Uttar Pradesh, 273001, India',NULL,'in_progress',8,'2025-09-07 15:09:54.115774','2025-09-07 15:24:39.203868');
INSERT INTO report VALUES(4,'big hole on road','all road fully damage','pothole','medium',26.7273746730769232,83.430726384615383,'Gorakhpur, Uttar Pradesh, 273001, India','static/uploads\b0e58530-0335-42cf-9bb4-95f636cb66cf_image.jpeg','in_progress',8,'2025-09-07 15:16:09.758572','2025-09-07 19:37:42.547762');
INSERT INTO report VALUES(5,'example','example','pothole','medium',26.7297699791742857,83.4311633813344713,'NH727BB, Air Force Area, Gorakhpur, Uttar Pradesh, 273001, India',NULL,'completed',3,'2025-09-07 18:47:05.175004','2025-09-07 19:48:57.309524');
INSERT INTO report VALUES(6,'example','example','pothole','medium',26.729865800085772,83.430876140578178,'NH727BB, Air Force Area, Gorakhpur, Uttar Pradesh, 273001, India',NULL,'reported',3,'2025-09-07 18:49:22.944552','2025-09-07 18:49:22.944552');
INSERT INTO report VALUES(7,'new drainage issue','there is a need of proper drainage system, each time it rains, the entire road is blocked by the rain water ','drainage','medium',26.7267840782841865,83.4325389387257843,'Gorakhpur, Uttar Pradesh, 273001, India','static/uploads\5b323d62-8a2b-445a-ae52-aa5ce638a164_images.jpeg','reported',9,'2025-09-08 13:46:02.355636','2025-09-08 13:46:02.355636');
INSERT INTO report VALUES(8,'sdjhbhb','hjbjhbhj','pothole','medium',28.6314096053125304,77.2166609048148018,'Indian Coffee House, Baba Kharak Singh Marg, Palika Niketan, Connaught Place, Chanakya Puri Tehsil, New Delhi, Delhi, 110001, India',NULL,'rejected',3,'2025-09-08 17:25:16.093813','2025-09-08 17:28:52.220201');
INSERT INTO report VALUES(9,'cjhbjhvjhJK','JBKJBKJ','pothole','medium',28.6314623409626918,77.2169346532908349,'Radial Road 2, Connaught Place, Chanakya Puri Tehsil, New Delhi, Delhi, 110001, India',NULL,'rejected',3,'2025-09-08 17:27:21.772856','2025-09-08 17:28:19.152292');
INSERT INTO report VALUES(10,'new issue ','new issue ','pothole','medium',26.4077312000000006,81.9724288000000029,'Sultanpur, Uttar Pradesh, 228121, India',NULL,'reported',3,'2025-09-08 23:15:46.043833','2025-09-08 23:15:46.043833');
INSERT INTO report VALUES(11,'Road Accident ','road accident happen in DDU university chowk ','pothole','high',26.7486226072389925,83.3807800867627122,'Gorakhpur, Uttar Pradesh, 273001, India','static/uploads\82799b2c-cdf4-437c-88d0-11e84878acc3_20231101061459_Accident_image_1.jpg','reported',10,'2025-09-09 06:39:35.729229','2025-09-09 06:39:35.729229');
CREATE TABLE maintenance_ticket (
	id INTEGER NOT NULL, 
	ticket_number VARCHAR(20) NOT NULL, 
	report_id INTEGER NOT NULL, 
	assigned_to_id INTEGER, 
	priority VARCHAR(20), 
	estimated_cost FLOAT, 
	estimated_completion DATETIME, 
	actual_completion DATETIME, 
	work_description TEXT, 
	materials_used TEXT, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (ticket_number), 
	FOREIGN KEY(report_id) REFERENCES report (id), 
	FOREIGN KEY(assigned_to_id) REFERENCES user (id)
);
INSERT INTO maintenance_ticket VALUES(1,'TKT-20250907-392D19B4',1,7,'medium',64864648.0,'2026-04-08 00:00:00.000000','2025-09-07 15:29:00.180322','ougyyv','guyv','2025-09-07 05:41:11.686535','2025-09-07 20:03:18.261188');
INSERT INTO maintenance_ticket VALUES(2,'TKT-20250907-BAEDBB33',2,NULL,'high',120000.0,'2025-08-09 00:00:00.000000',NULL,'test data','test data','2025-09-07 06:49:37.681883','2025-09-07 18:42:01.379922');
INSERT INTO maintenance_ticket VALUES(3,'TKT-20250907-7C6D787E',3,NULL,'medium',NULL,NULL,NULL,NULL,NULL,'2025-09-07 15:09:54.164834','2025-09-07 15:09:54.164834');
INSERT INTO maintenance_ticket VALUES(4,'TKT-20250907-E2CF968A',4,NULL,'medium',NULL,NULL,'2025-09-07 19:34:28.001363',NULL,NULL,'2025-09-07 15:16:09.797723','2025-09-07 19:34:28.003867');
INSERT INTO maintenance_ticket VALUES(5,'TKT-20250908-3C7AB0CE',6,7,'medium',1360000.0,'2025-09-08 00:00:00.000000',NULL,'Do your job on time ','use whatever you want to use ','2025-09-07 18:49:23.368982','2025-09-07 20:01:49.451349');
INSERT INTO maintenance_ticket VALUES(6,'TKT-20250908-E4136F75',7,NULL,'medium',NULL,NULL,NULL,NULL,NULL,'2025-09-08 13:46:02.741080','2025-09-08 13:46:02.741080');
INSERT INTO maintenance_ticket VALUES(7,'TKT-20250908-792966F3',8,NULL,'medium',NULL,NULL,NULL,NULL,NULL,'2025-09-08 17:25:16.267310','2025-09-08 17:25:16.267310');
INSERT INTO maintenance_ticket VALUES(8,'TKT-20250908-D0F4B32A',9,NULL,'medium',NULL,NULL,NULL,NULL,NULL,'2025-09-08 17:27:21.922872','2025-09-08 17:27:21.922872');
INSERT INTO maintenance_ticket VALUES(9,'TKT-20250909-842DCFCE',10,NULL,'medium',NULL,NULL,NULL,NULL,NULL,'2025-09-08 23:15:46.209788','2025-09-08 23:15:46.209788');
INSERT INTO maintenance_ticket VALUES(10,'TKT-20250909-274833F0',11,NULL,'high',NULL,NULL,NULL,NULL,NULL,'2025-09-09 06:39:35.890280','2025-09-09 06:39:35.890280');
CREATE TABLE status_update (
	id INTEGER NOT NULL, 
	report_id INTEGER NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	comment TEXT, 
	updated_by_id INTEGER NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(report_id) REFERENCES report (id), 
	FOREIGN KEY(updated_by_id) REFERENCES user (id)
);
INSERT INTO status_update VALUES(1,1,'verified','your report has been verified by the authority',1,'2025-09-07 05:44:41.901745');
INSERT INTO status_update VALUES(2,1,'verified','your report has been verified by the authority',1,'2025-09-07 05:44:46.363670');
INSERT INTO status_update VALUES(3,2,'verified',replace('Your problem is verified and will soon be actioned to work...\nThank you for your support and cooperation.','\n',char(10)),1,'2025-09-07 06:55:37.202450');
INSERT INTO status_update VALUES(4,2,'verified',replace('Your problem is verified and will soon be actioned to work...\nThank you for your support and cooperation.','\n',char(10)),1,'2025-09-07 06:55:45.909491');
INSERT INTO status_update VALUES(5,2,'in_progress','Thanks for reporting this issue, your issue is in progress now.☺️',1,'2025-09-07 06:58:21.332354');
INSERT INTO status_update VALUES(6,2,'in_progress','Thanks for reporting this issue, your issue is in progress now.☺️',1,'2025-09-07 06:58:30.243779');
INSERT INTO status_update VALUES(7,2,'in_progress','Bulk update to in_progress',1,'2025-09-07 07:01:16.744025');
INSERT INTO status_update VALUES(8,1,'in_progress','Bulk update to in_progress',1,'2025-09-07 07:01:16.807015');
INSERT INTO status_update VALUES(9,2,'in_progress','Bulk update to in_progress',1,'2025-09-07 07:01:24.118567');
INSERT INTO status_update VALUES(10,1,'in_progress','Bulk update to in_progress',1,'2025-09-07 07:01:24.184700');
INSERT INTO status_update VALUES(11,4,'verified','we are looking into it',6,'2025-09-07 15:21:46.798601');
INSERT INTO status_update VALUES(12,4,'in_progress','',6,'2025-09-07 15:23:06.702988');
INSERT INTO status_update VALUES(13,3,'verified','',6,'2025-09-07 15:24:20.076871');
INSERT INTO status_update VALUES(14,3,'in_progress','',6,'2025-09-07 15:24:34.953313');
INSERT INTO status_update VALUES(15,3,'in_progress','',6,'2025-09-07 15:24:39.217858');
INSERT INTO status_update VALUES(16,1,'in_progress','',6,'2025-09-07 15:28:44.236618');
INSERT INTO status_update VALUES(17,1,'completed','',6,'2025-09-07 15:29:00.180322');
INSERT INTO status_update VALUES(18,4,'completed','Your report is completed, thank you for the cooperation with us.',1,'2025-09-07 19:34:27.980540');
INSERT INTO status_update VALUES(19,4,'in_progress','',1,'2025-09-07 19:37:42.556795');
INSERT INTO status_update VALUES(20,5,'verified','',1,'2025-09-07 19:38:24.251366');
INSERT INTO status_update VALUES(21,5,'in_progress','',1,'2025-09-07 19:40:54.941235');
INSERT INTO status_update VALUES(22,5,'completed','',1,'2025-09-07 19:48:57.326740');
INSERT INTO status_update VALUES(23,1,'verified','',1,'2025-09-07 20:03:40.582213');
INSERT INTO status_update VALUES(24,9,'rejected','no proper information of the issue ',1,'2025-09-08 17:28:19.158998');
INSERT INTO status_update VALUES(25,8,'rejected','no proper information of the issue',1,'2025-09-08 17:28:52.225702');
CREATE TABLE vote (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	report_id INTEGER NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	CONSTRAINT unique_user_report_vote UNIQUE (user_id, report_id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(report_id) REFERENCES report (id)
);
INSERT INTO vote VALUES(1,3,1,'2025-09-07 19:16:16.461894');
INSERT INTO vote VALUES(2,9,1,'2025-09-08 16:22:50.946196');
INSERT INTO vote VALUES(3,3,10,'2025-09-08 23:16:10.348710');
CREATE TABLE citizen_points (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	points INTEGER, 
	reports_submitted INTEGER, 
	votes_cast INTEGER, 
	reports_verified INTEGER, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO citizen_points VALUES(1,3,54,4,5,2,'2025-09-08 23:16:10.438687');
INSERT INTO citizen_points VALUES(2,9,12,1,1,0,'2025-09-08 16:22:51.027851');
INSERT INTO citizen_points VALUES(3,10,10,1,0,0,'2025-09-09 06:39:35.828770');
COMMIT;

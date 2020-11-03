#DROP DATABASE IF EXISTS `hems`;
CREATE DATABASE IF NOT EXISTS hems;
USE hems;
CREATE TABLE IF NOT EXISTS `hems`.`devices`(
    id INT NOT NULL auto_increment, #Device ID
    name VARCHAR(50),               #Device Name
    last_update DATETIME,           #Last Time Device was touched
    plug BOOL,                      #true if the device is a plug, false if the device is a tempsensor
    status BOOL,                    #Whether device is online or not
    PRIMARY KEY (id)                #Index on Device ID
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS `hems`.`energy`(
    id INT NOT NULL,                #Device ID
    time DATETIME NOT NULL,                  #Time of submission
    irms DOUBLE NOT NULL,                    #RMS current for datapoint
    pwr DOUBLE NOT NULL,                     #power for datapoint
    pf DOUBLE NOT NULL,                      #powerfactor for datapoint
    energy DOUBLE NOT NULL,                  #energy for datapoint
    #primary key(time),
    CONSTRAINT fk_id FOREIGN KEY (id) 
        REFERENCES hems.`devices`(id)
        ON DELETE CASCADE
        ON UPDATE RESTRICT
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS `hems`.`temperature`(
    id INT NOT NULL,
    time DATETIME NOT NULL,
    temperature DOUBLE NOT NULL
    #primary key(time)
#    CONSTRAINT fk_id FOREIGN KEY (id)
#        REFERENCES hems.`devices`(id)
#        ON DELETE CASCADE
#        ON UPDATE RESTRICT
) ENGINE=InnoDB;

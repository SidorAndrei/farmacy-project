DROP TABLE IF EXISTS farmacy.users;
DROP TABLE IF EXISTS farmacy.recipe_content;
DROP TABLE IF EXISTS farmacy.recipes;
DROP TABLE IF EXISTS farmacy.employees;
DROP TABLE IF EXISTS farmacy.clients;
DROP TABLE IF EXISTS farmacy.sales;
DROP TABLE IF EXISTS farmacy.medicines;
DROP TABLE IF EXISTS farmacy.providers;


CREATE TABLE IF NOT EXISTS `farmacy`.`clients` (
  `id_client` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(25) NULL DEFAULT NULL,
  `Adress` VARCHAR(45) NULL DEFAULT NULL,
  `CNP` VARCHAR(13) NULL DEFAULT NULL,
  `code_client` INT NOT NULL,
  `gender` VARCHAR(10) NULL DEFAULT NULL,
  PRIMARY KEY (`id_client`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `farmacy`.`employees` (
  `ID_employee` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NULL DEFAULT NULL,
  `CNP` VARCHAR(13) NULL DEFAULT NULL,
  PRIMARY KEY (`ID_employee`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;



CREATE TABLE IF NOT EXISTS `farmacy`.`providers` (
  `ID_provider` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NULL DEFAULT NULL,
  `Adress` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`ID_provider`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `farmacy`.`medicines` (
  `ID_medicine` INT NOT NULL AUTO_INCREMENT,
  `Code` INT NULL DEFAULT NULL,
  `Name` VARCHAR(45) NULL DEFAULT NULL,
  `Activity_area` VARCHAR(45) NULL DEFAULT NULL,
  `Production_date` DATE NULL DEFAULT NULL,
  `Expiration_date` DATE NULL DEFAULT NULL,
  `Price` FLOAT NOT NULL,
  `ID_provider` INT NOT NULL,
  `Stock` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID_medicine`),
  INDEX `ID_medicine_idx` (`ID_provider` ASC) VISIBLE,
  INDEX `ID_provider_idx` (`ID_provider` ASC) VISIBLE,
  CONSTRAINT `ID_provider`
    FOREIGN KEY (`ID_provider`)
    REFERENCES `farmacy`.`providers` (`ID_provider`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `farmacy`.`recipes`
(
    ID_recipes        int auto_increment
        primary key,
    Code              int  null,
    ID_client         int  null,
    Expiration_date   date null,
    Prescription_date date null,
    ID_employee       int  null,
    constraint FK_client
        foreign key (ID_client) references clients (id_client),
    constraint FK_employee
        foreign key (ID_employee) references employees (ID_employee)
);

create index FK_employee_idx
    on recipes (ID_employee);

create index ID_recipes_idx
    on recipes (ID_client);


CREATE TABLE IF NOT EXISTS `farmacy`.`recipe_content`
(
    ID_recipes  int null,
    ID_medicine int null,
    quantity int null,
    constraint recipe_content_medicines_ID_medicine_fk
        foreign key (ID_medicine) references medicines (ID_medicine),
    constraint recipe_content_recipes_ID_recipes_fk
        foreign key (ID_recipes) references recipes (ID_recipes)
);



CREATE TABLE IF NOT EXISTS `farmacy`.`sales` (
  `ID_medicine` INT NOT NULL AUTO_INCREMENT,
  `Percent` FLOAT NULL DEFAULT NULL,
  `Start_date` DATE NULL DEFAULT NULL,
  `Finish_date` DATE NULL DEFAULT NULL,
  INDEX `ID_medicine_idx` (`ID_medicine` ASC) VISIBLE,
  CONSTRAINT `ID_medicine`
    FOREIGN KEY (`ID_medicine`)
    REFERENCES `farmacy`.`medicines` (`ID_medicine`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `farmacy`.`users` (
  `ID_user` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL DEFAULT NULL,
  `password` VARCHAR(150) NULL DEFAULT NULL,
  INDEX `ID_users_idx` (`ID_user` ASC) VISIBLE
  )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO farmacy.providers(Name, Adress)
VALUES ('PHARMAFARM','Mures'),
       ('FARMEXIM SA','Bucuresti'),
       ('FILDAS TRADING SRL', 'Mures'),
       ('FARMEXPERT DCI','Bucuresti'),
       ('MEDIPLUS EXIM','Cluj'),
       ('DELTAFARM S.R.L.','Suceava'),
       ('MEDICO-MED','Iasi'),
       ('MEDIPLUS EXIM S.R.L.','Constanta'),
       ('EUROPHARM HOLDING S.R.L.','Dolj'),
       ('TRANSMEDICA TRADING S.R.L.','Bucuresti');

INSERT INTO farmacy.medicines(Code, Name, Activity_area, Production_date, Expiration_date, Price, ID_provider, Stock)
VALUES (135415,'Herbion','Raceala si Gripa','2020-12-20','2023-12-12',15.5,1,25),
       (264732,'OROcalmin','Raceala si Gripa','2020-01-30','2023-12-27',65,2,100),
       (768945,'Nurofen','Raceala si Gripa','2020-12-12','2023-02-12',60,7,250),
       (724253,'Beres CalciviD','Vitamine si Minerale','2020-12-12','2023-03-20',12,5,125),
       (234162,'Magne B6','Vitamine si Minerale','2021-10-12','2024-10-12',13,3,225),
       (145632,'Agartha','Diabet','2021-12-12','2023-12-12',5.5,1,215),
       (895674,'Abasaglar','Diabet','2021-12-12','2023-01-01',6.5,3,25),
       (234532,'Cutaden','Preparate Deramatologice','2020-12-13','2023-12-12',1.5,1,235),
       (125623,'Aciclovir','Preparate Dermatologice','2020-12-12','2023-12-12',23.5,3,15),
       (123453,'Algocalmin','Sistem Nervos','2020-12-27','2023-11-23',34.5,3,105),
       (123412,'Algozone','Sistem Nervos','2021-01-23','2023-10-12',65.7,4,25),
       (130978,'Betahistina','Oftalmologie si ORL','2021-01-25','2024-10-17',5.53,6,17),
       (109234,'Calgel','Oftalmologie si ORL','2021-12-12','2023-12-12',7.5,9,259),
       (178234,'Pulsoximetru','Aparatura Medicala','2020-12-12','2023-12-10',8.5,10,275),
       (129023,'Aparat pentru aerosoli','Aparatura Medicala','2021-12-12','2024-12-12',5.5,8,125);

INSERT INTO farmacy.employees(Name, CNP)
VALUES ('Sidor Andrei',5789356271823),
       ('Sergiu Pert',5564829356172),
       ('Georgescu Maria',666735624120),
       ('Barbu Victor',1642459876453),
       ('Barbu Mariana',2787654361422),
       ('Popescu Alina',2786541326273),
       ('Dumitru Ana',2745263092345);

INSERT INTO farmacy.clients(Name, Adress, CNP, code_client, gender)
VALUES ('Catana Adrian','Bucuresti',    1267832415233,453234,'Masculin'),
       ('Cojocaru Nicoleta','Slatina',  2345617283945,874532,'Feminin'),
       ('Iancu Madalina','Sibiu',       2456738456342,5467342,'Feminin'),
       ('Avram Andreea','Cluj',         6743524537283,675433,'Feminin'),
       ('Dumitrascu Robert','Bucuresti',1674532142354,876468,'Masculin'),
       ('Bolocan Monica','Cluj',        1645234132435,764531,'Feminin');

INSERT INTO farmacy.sales(ID_medicine, Percent, Start_date, Finish_date)
VALUES (1,20.8,'2022-01-02','2022-02-01'),
       (2,30.2,'2022-01-23','2022-03-12'),
       (4,50,'2022-02-02','2022-04-02'),
       (7,42.3,'2022-01-09','2022-05-01'),
       (9,41.5,'2022-03-03','2022-05-05'),
       (10,54.3,'2022-03-04','2022-04-04');

INSERT INTO farmacy.recipes(Code, ID_client, Expiration_date, Prescription_date, ID_employee)
VALUES (345234,1,'2022-02-01','2022-01-01',1),
       (364823,2,'2022-02-03','2022-01-23',1),
       (784563,3,'2022-02-23','2022-01-26',2),
       (543562,4,'2022-02-19','2022-01-25',2),
       (098635,5,'2022-03-10','2022-01-12',6);

INSERT INTO farmacy.recipe_content(ID_recipes, ID_medicine, quantity)
VALUES (1,1,4),
       (1,2,5),
       (1,3,7),
       (2,4,8),
       (2,5,10),
       (2,6,10),
       (3,7,2),
       (3,8,3),
       (4,9,2),
       (4,10,1),
       (5,11,5),
       (5,12,4);


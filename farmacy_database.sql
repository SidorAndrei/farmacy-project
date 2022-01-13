CREATE TABLE IF NOT EXISTS `farmacy`.`clients` (
  `id_client` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(25) NULL DEFAULT NULL,
  `Adress` VARCHAR(45) NULL DEFAULT NULL,
  `CNP` INT NULL DEFAULT NULL,
  `code_client` INT NOT NULL,
  `gender` VARCHAR(10) NULL DEFAULT NULL,
  PRIMARY KEY (`id_client`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `farmacy`.`employees` (
  `ID_employee` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NULL DEFAULT NULL,
  `CNP` INT NULL DEFAULT NULL,
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

CREATE TABLE IF NOT EXISTS `farmacy`.`recipes` (
  `ID_recipes` INT NOT NULL AUTO_INCREMENT,
  `Code` INT NULL DEFAULT NULL,
  `ID_medicine` INT NULL DEFAULT NULL,
  `ID_client` INT NULL DEFAULT NULL,
  `Expiration_date` DATE NULL DEFAULT NULL,
  `Prescription_date` DATE NULL DEFAULT NULL,
  `ID_employee` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID_recipes`),
  INDEX `ID_recipes_idx` (`ID_client` ASC) VISIBLE,
  INDEX `FK_employee_idx` (`ID_employee` ASC) VISIBLE,
  INDEX `FK_medicine_idx` (`ID_medicine` ASC) VISIBLE,
  CONSTRAINT `FK_client`
    FOREIGN KEY (`ID_client`)
    REFERENCES `farmacy`.`clients` (`id_client`),
  CONSTRAINT `FK_employee`
    FOREIGN KEY (`ID_employee`)
    REFERENCES `farmacy`.`employees` (`ID_employee`),
  CONSTRAINT `FK_medicine`
    FOREIGN KEY (`ID_medicine`)
    REFERENCES `farmacy`.`medicines` (`ID_medicine`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;



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


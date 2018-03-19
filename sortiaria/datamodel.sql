-- MySQL Script generated by MySQL Workbench
-- mar. 30 janv. 2018 09:14:08 CET
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema sortiaria
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `sortiara` ;

-- -----------------------------------------------------
-- Schema sortiaria
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sortiaria` DEFAULT CHARACTER SET utf8 ;
USE `sortiaria` ;

-- -----------------------------------------------------
-- Table `sortiaria`.`mot`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sortiaria`.`mot` ;

CREATE TABLE IF NOT EXISTS `sortiaria`.`mot` (
  `mot_id` INT NOT NULL AUTO_INCREMENT COMMENT '	',
  `mot_terme` TINYTEXT NOT NULL,
  `mot_def` TEXT NOT NULL,
  `mot_commentaire` TEXT NOT NULL,
  PRIMARY KEY (`mot_terme`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sortiaria`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sortiaria`.`user` ;

CREATE TABLE IF NOT EXISTS `sortiaria`.`user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `user_nom` TINYTEXT NOT NULL,
  `user_login` VARCHAR(45) NOT NULL,
  `user_email` TINYTEXT NOT NULL,
  `user_password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_login_UNIQUE` (`user_login` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sortiara`.`auteur`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sortiaria`.`auteur` ;

CREATE TABLE IF NOT EXISTS `sortiaria`.`auteur` (
  `auteur_id` INT NOT NULL AUTO_INCREMENT,
  `auteur_user_id` INT NOT NULL,
  `auteur_mot_id` INT NOT NULL,
  `auteur_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`auteur_id`),
  INDEX `fk_auteur_1_idx` (`auteur_mot_id` ASC),
  INDEX `fk_auteur_2_idx` (`auteur_user_id` ASC),
  CONSTRAINT `fk_auteur_1`
    FOREIGN KEY (`auteur_mot_id`)
    REFERENCES `sortiaria`.`mot` (`mot_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_auteur_2`
    FOREIGN KEY (`auteur_user_id`)
    REFERENCES `sortiaria`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sortiaria`.`commentaire`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sortiaria`.`commentaire` ;

CREATE TABLE IF NOT EXISTS `sortiaria`.`commentaire` (
  `commentaire_id` INT NOT NULL AUTO_INCREMENT,
  `commentaire_titre` TINYTEXT NOT NULL,
  `commentaire_source` TEXT NOT NULL,
  `commentaire_texte` TEXT NOT NULL,
  PRIMARY KEY (`commentaire_id`),
  INDEX `fk_commentaire_1_idx` (`commentaire_mot_id` ASC),
  CONSTRAINT `fk_commentaire_1`
    FOREIGN KEY (`commentaire_mot_id`)
    REFERENCES `sortiaria`.`mot` (`mot_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE = '';
GRANT USAGE ON *.* TO sortiaria_user;
 DROP USER sortiaria_user;
SET SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE USER 'sortiara_user' IDENTIFIED BY 'password';

GRANT ALL ON `sortiaria`.* TO 'sortiaria_user';
GRANT SELECT ON TABLE `sortiaria`.* TO 'sortiaria_user';
GRANT SELECT, INSERT, TRIGGER ON TABLE `sortiaria`.* TO 'sortiaria_user';
GRANT SELECT, INSERT, TRIGGER, UPDATE, DELETE ON TABLE `sortiaria`.* TO 'sortiaria_user';
GRANT EXECUTE ON ROUTINE `sortiaria`.* TO 'sortiaria_user';

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `sortiaria`.`mot`
-- -----------------------------------------------------
START TRANSACTION;
USE `sortiaria`;
INSERT INTO `sortiaria`.`mot` (`mot_id`, `mot_terme`, `mot_def`) VALUES (1, 'Alchimiste', 'Celui qui s’occupait d’alchimie.');

COMMIT;


-- -----------------------------------------------------
-- Data for table `sortiaria`.`user`
-- -----------------------------------------------------
START TRANSACTION;
USE `sortiaria`;
INSERT INTO `sortiaria`.`user` (`user_id`, `user_nom`, `user_login`, `user_email`, `user_password`) VALUES (1, 'Administrator', 'admin', 'admin@supersite.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

COMMIT;

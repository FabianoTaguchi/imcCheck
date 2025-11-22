-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: imccheck
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activities`
--

DROP TABLE IF EXISTS `activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `tipo` varchar(100) NOT NULL,
  `data_atividade` date NOT NULL,
  `duracao_min` int NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_activity_user_date` (`user_id`,`data_atividade`),
  CONSTRAINT `fk_activity_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activities`
--

LOCK TABLES `activities` WRITE;
/*!40000 ALTER TABLE `activities` DISABLE KEYS */;
INSERT INTO `activities` VALUES (1,1,'Caminhada','2025-11-15',30,'2025-11-15 21:27:09'),(2,2,'Corrida','2022-11-17',30,'2025-11-20 04:10:41'),(3,2,'Corrida','2022-11-18',60,'2025-11-20 04:11:19'),(4,1,'Caminhada','2025-11-20',50,'2025-11-22 22:52:15');
/*!40000 ALTER TABLE `activities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goals`
--

DROP TABLE IF EXISTS `goals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `data_objetivo` date NOT NULL,
  `peso_meta` decimal(5,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_goals_user` (`user_id`),
  CONSTRAINT `fk_goals_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goals`
--

LOCK TABLES `goals` WRITE;
/*!40000 ALTER TABLE `goals` DISABLE KEYS */;
INSERT INTO `goals` VALUES (1,1,'2025-12-31',95.00,'2025-11-15 21:24:29'),(3,2,'2025-12-31',90.00,'2025-11-20 04:06:38');
/*!40000 ALTER TABLE `goals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome_completo` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `telefone` varchar(40) DEFAULT NULL,
  `login` varchar(80) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `data_nascimento` date DEFAULT NULL,
  `peso` decimal(5,2) DEFAULT NULL,
  `altura` decimal(3,2) DEFAULT NULL,
  `sexo` enum('masculino','feminino') DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Teste','teste@gmail.com','066999846363','teste','teste123','2000-01-01',100.00,1.89,'masculino','2025-11-15 17:23:23'),(2,'Natanael','natanael@gmail.com','66999998585','natanael','123456','2000-01-01',100.00,1.90,'masculino','2025-11-20 00:05:46');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weight_records`
--

DROP TABLE IF EXISTS `weight_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weight_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `data_registro` date NOT NULL,
  `peso` decimal(5,2) NOT NULL,
  `imc` decimal(5,2) DEFAULT NULL,
  `classificacao` varchar(40) DEFAULT NULL,
  `grau_obesidade` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ativo` enum('sim','não') NOT NULL DEFAULT 'sim',
  PRIMARY KEY (`id`),
  KEY `idx_weight_user_date` (`user_id`,`data_registro`),
  CONSTRAINT `fk_weight_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weight_records`
--

LOCK TABLES `weight_records` WRITE;
/*!40000 ALTER TABLE `weight_records` DISABLE KEYS */;
INSERT INTO `weight_records` VALUES (1,1,'2025-11-14',110.00,30.79,'Obesidade','I','2025-11-15 21:24:44','não'),(2,1,'2025-11-15',109.00,30.51,'Obesidade','I','2025-11-15 21:24:50','não'),(3,2,'2025-11-17',101.00,27.98,'Sobrepeso',NULL,'2025-11-20 04:07:02','sim'),(4,2,'2025-11-18',125.00,34.63,'Obesidade','I','2025-11-20 04:08:05','sim'),(5,2,'2025-11-19',89.00,24.65,'Peso normal',NULL,'2025-11-20 04:08:46','sim'),(6,2,'2022-11-20',91.00,25.21,'Sobrepeso',NULL,'2025-11-20 04:09:05','sim'),(7,1,'2025-11-22',107.00,29.95,'Sobrepeso',NULL,'2025-11-22 22:30:54','não'),(8,1,'2025-11-14',100.00,27.99,'Sobrepeso',NULL,'2025-11-22 22:52:28','sim'),(9,1,'2025-11-15',108.00,30.23,'Obesidade','I','2025-11-22 22:52:39','sim'),(10,1,'2025-11-22',89.00,24.92,'Peso normal',NULL,'2025-11-22 22:52:55','sim');
/*!40000 ALTER TABLE `weight_records` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-22 14:57:02

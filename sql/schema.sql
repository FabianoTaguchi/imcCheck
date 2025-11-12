CREATE DATABASE imccheck;
USE imccheck;

-- Usuários
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome_completo VARCHAR(150) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  telefone VARCHAR(40),
  login VARCHAR(80) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL, -- armazenar hash no backend
  data_nascimento DATE,
  peso DECIMAL(5,2), -- kg
  altura DECIMAL(3,2), -- metros
  sexo ENUM('masculino','feminino') DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Metas (uma meta ativa por usuário). Para simplicidade: 1 meta por usuário.
CREATE TABLE IF NOT EXISTS goals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  data_objetivo DATE NOT NULL,
  peso_meta DECIMAL(5,2) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_goals_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT uq_goals_user UNIQUE (user_id)
);

-- Registros de peso (histórico)
CREATE TABLE IF NOT EXISTS weight_records (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  data_registro DATE NOT NULL,
  peso DECIMAL(5,2) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_weight_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_weight_user_date (user_id, data_registro)
);

-- Atividades físicas
CREATE TABLE IF NOT EXISTS activities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  tipo VARCHAR(100) NOT NULL,
  data_atividade DATE NOT NULL,
  duracao_min INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_activity_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_activity_user_date (user_id, data_atividade)
);

-- Exemplos de views (opcional): comparação simples meta x último registro
-- CREATE VIEW v_user_last_weight AS
-- SELECT w.user_id, MAX(w.data_registro) AS ultima_data,
--        SUBSTRING_INDEX(GROUP_CONCAT(w.peso ORDER BY w.data_registro DESC), ',', 1) AS ultimo_peso
-- FROM weight_records w
-- GROUP BY w.user_id;
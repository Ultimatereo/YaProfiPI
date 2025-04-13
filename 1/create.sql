-- 1. Создание таблиц

CREATE TABLE Participant (
    participant_id INT PRIMARY KEY,
    name           VARCHAR(100),
    email          VARCHAR(100),
    password       VARCHAR(100)
);

CREATE TABLE Venue (
    venue_id   INT PRIMARY KEY,
    name       VARCHAR(150),
    location   VARCHAR(200),
    capacity   INT
);

CREATE TABLE Event (
    event_id   INT PRIMARY KEY,
    title      VARCHAR(200),
    date       DATE,
    time       TIME,
    description TEXT,
    venue_id   INT,
    FOREIGN KEY (venue_id) REFERENCES Venue(venue_id)
);

CREATE TABLE Registration (
    participant_id   INT,
    event_id         INT,
    registration_date DATETIME,
    PRIMARY KEY (participant_id, event_id),
    FOREIGN KEY (participant_id) REFERENCES Participant(participant_id),
    FOREIGN KEY (event_id) REFERENCES Event(event_id)
);

-- 2. Вставка демонстрационных данных

-- Добавляем участников
INSERT INTO Participant (participant_id, name, email, password) VALUES
(1, 'Иван Иванов', 'ivan@example.com', 'pass123'),
(2, 'Петр Петров', 'petr@example.com', 'pass456');

-- Добавляем площадки
INSERT INTO Venue (venue_id, name, location, capacity) VALUES
(1, 'Зал A', 'Бизнес-центр, 3-й этаж', 100),
(2, 'Сцена 1', 'Центральный парк', 50);

-- Добавляем мероприятия
INSERT INTO Event (event_id, title, date, time, description, venue_id) VALUES
(1, 'Конференция по ИИ', '2025-05-12', '10:00:00', 'Конференция по искусственному интеллекту', 1),
(2, 'Музыкальный фестиваль', '2025-06-25', '18:00:00', 'Летний музыкальный фестиваль', 2);

-- Добавляем регистрации участников на мероприятия
-- Участник 1 и 2 регистрируются на событие 1, участник 1 также на событие 2
INSERT INTO Registration (participant_id, event_id, registration_date) VALUES
(1, 1, '2025-05-01 09:00:00'),
(2, 1, '2025-05-02 10:30:00'),
(1, 2, '2025-06-01 12:00:00');

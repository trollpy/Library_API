DROP DATABASE IF EXISTS library_management;
CREATE DATABASE library_management;
USE library_management;

-- Create MEMBERS table
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255),
    date_of_birth DATE,
    membership_date DATE NOT NULL,
    membership_status ENUM('Active', 'Expired', 'Suspended') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create BOOKS table
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    publication_year YEAR,
    publisher VARCHAR(100),
    language VARCHAR(50) DEFAULT 'English',
    page_count INT,
    description TEXT,
    available_copies INT NOT NULL DEFAULT 0,
    total_copies INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create AUTHORS table
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE,
    nationality VARCHAR(50),
    biography TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create CATEGORIES table
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    parent_category_id INT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id) ON DELETE SET NULL
);

-- Create STAFF table
CREATE TABLE staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    role ENUM('Librarian', 'Assistant', 'Admin', 'Manager') NOT NULL,
    hire_date DATE NOT NULL,
    salary DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create BOOK_AUTHORS junction table (M:M relationship)
CREATE TABLE book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create BOOK_CATEGORIES junction table (M:M relationship)
CREATE TABLE book_categories (
    book_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (book_id, category_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create LOANS table
CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    staff_id INT NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    status ENUM('Borrowed', 'Returned', 'Overdue', 'Lost') NOT NULL DEFAULT 'Borrowed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
);

-- Create FINES table
CREATE TABLE fines (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    fine_date DATE NOT NULL,
    payment_date DATE,
    status ENUM('Pending', 'Paid', 'Waived') NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id) ON DELETE CASCADE
);

-- Create RESERVATIONS table
CREATE TABLE reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    status ENUM('Active', 'Fulfilled', 'Expired', 'Cancelled') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Create EVENTS table
CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    location VARCHAR(100),
    max_attendees INT,
    organizer_staff_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_staff_id) REFERENCES staff(staff_id) ON DELETE SET NULL
);

-- Create EVENT_ATTENDEES junction table (M:M relationship)
CREATE TABLE event_attendees (
    event_id INT NOT NULL,
    member_id INT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attendance_status ENUM('Registered', 'Attended', 'No-show') DEFAULT 'Registered',
    PRIMARY KEY (event_id, member_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Create index for commonly searched fields
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_isbn ON books(isbn);
CREATE INDEX idx_members_name ON members(last_name, first_name);
CREATE INDEX idx_loans_status ON loans(status);
CREATE INDEX idx_loans_dates ON loans(loan_date, due_date, return_date);


-- sample data for the library management system



-- MEMBERS data (South African)
INSERT INTO members (first_name, last_name, email, phone_number, address, date_of_birth, membership_date, membership_status) VALUES
('Thabo', 'Mbeki', 'thabo.mbeki@email.co.za', '0821234567', '15 Vilakazi St, Orlando West, Soweto', '1975-06-18', '2023-01-15', 'Active'),
('Nomsa', 'Dlamini', 'nomsa.d@email.co.za', '0832345678', '42 Long St, Cape Town City Centre', '1990-11-22', '2024-02-20', 'Active'),
('Sipho', 'Nkosi', 'sipho.nkosi@email.com', '0713456789', '7 Umhlanga Rocks Dr, Umhlanga, Durban', '1988-03-05', '2023-11-10', 'Active'),
('Lerato', 'Moloi', 'lerato.m@email.co.za', '0844567890', '23 Nelson Mandela Ave, Sandton', '1995-09-30', '2024-03-01', 'Active'),
('Jacob', 'Zuma', 'jacob.z@email.co.za', '0725678901', '1 Nkandla Rd, Nkandla, KZN', '1960-04-12', '2022-05-18', 'Suspended'),
('Precious', 'Khumalo', 'precious.k@email.co.za', '0816789012', '56 Commissioner St, Johannesburg CBD', '1992-07-25', '2023-08-22', 'Active'),
('Mandla', 'Botha', 'mandla.b@email.co.za', '0767890123', '34 Beach Rd, Strand, Cape Town', '1985-12-08', '2024-01-05', 'Active'),
('Nandi', 'Ngcobo', 'nandi.n@email.co.za', '0798901234', '89 Church St, Pietermaritzburg', '1978-02-14', '2023-06-30', 'Expired');

-- BOOKS data (South African literature)
INSERT INTO books (isbn, title, publication_year, publisher, language, page_count, description, available_copies, total_copies) VALUES
('9781770090287', 'Cry, the Beloved Country', 1948, 'Jonathan Ball Publishers', 'English', 256, 'Classic South African novel by Alan Paton', 5, 7),
('9780143185590', 'Disgrace', 1999, 'Penguin South Africa', 'English', 220, 'Nobel Prize-winning novel by J.M. Coetzee', 3, 5),
('9781431400842', 'The Whale Caller', 2005, 'Jacana Media', 'English', 192, 'Magical realism by Zakes Mda', 2, 3),
('9781770103147', 'Born a Crime', 2016, 'Pan Macmillan SA', 'English', 304, 'Trevor Noah''s memoir of growing up in apartheid SA', 4, 6),
('9780143027081', 'Ways of Dying', 1995, 'Penguin South Africa', 'English', 208, 'Zakes Mda''s debut novel', 1, 2),
('9781868427589', 'The Long Walk to Freedom', 1994, 'Ballantine Books', 'English', 656, 'Nelson Mandela''s autobiography', 6, 8),
('9781776093605', 'The Reactive', 2014, 'Umuzi', 'English', 176, 'Debut novel by Masande Ntshanga', 2, 3),
('9781415200585', 'Mhudi', 1930, 'Ad Donker', 'English', 224, 'First novel in English by a black South African', 1, 2),
('9781776092257', 'The Yearning', 2016, 'Pan Macmillan SA', 'English', 320, 'Mohale Mashigo''s debut novel', 3, 4),
('9780620480084', 'The Theory of Flight', 2018, 'Penguin Random House SA', 'English', 288, 'Siphiwe Gloria Ndlovu''s debut novel', 2, 3);

-- AUTHORS data (South African)
INSERT INTO authors (first_name, last_name, birth_date, nationality, biography) VALUES
('Alan', 'Paton', '1903-01-11', 'South African', 'Author of Cry, the Beloved Country and activist against apartheid'),
('J.M.', 'Coetzee', '1940-02-09', 'South African', 'Nobel Prize-winning author known for Disgrace and other works'),
('Zakes', 'Mda', '1948-10-06', 'South African', 'Novelist, poet and playwright known for his post-apartheid literature'),
('Trevor', 'Noah', '1984-02-20', 'South African', 'Comedian and author of Born a Crime'),
('Nelson', 'Mandela', '1918-07-18', 'South African', 'Anti-apartheid revolutionary and former President of South Africa'),
('Masande', 'Ntshanga', '1986-01-01', 'South African', 'Award-winning author of The Reactive'),
('Sol', 'Plaatje', '1876-10-09', 'South African', 'Writer, journalist and political activist'),
('Mohale', 'Mashigo', '1981-01-01', 'South African', 'Author and musician known for The Yearning'),
('Siphiwe Gloria', 'Ndlovu', '1973-01-01', 'South African', 'Author and academic known for The Theory of Flight');

-- CATEGORIES data
INSERT INTO categories (name, parent_category_id, description) VALUES
('Fiction', NULL, 'Imaginative narrative works'),
('Non-Fiction', NULL, 'Factual narrative works'),
('South African Literature', 1, 'Fiction by South African authors'),
('Autobiography', 2, 'Self-written life stories'),
('History', 2, 'Works about historical events'),
('African Literature', 1, 'Literature from African authors'),
('Politics', 2, 'Works about political systems and theories'),
('Post-Apartheid', 3, 'Literature about post-apartheid South Africa');

-- STAFF data (South African)
INSERT INTO staff (first_name, last_name, email, phone_number, role, hire_date, salary) VALUES
('Nomsa', 'Khumalo', 'nomsa.k@library.co.za', '0821122334', 'Manager', '2018-06-15', 45000.00),
('Sipho', 'Dlamini', 'sipho.d@library.co.za', '0832233445', 'Librarian', '2020-02-10', 32000.00),
('Lindiwe', 'Mokoena', 'lindiwe.m@library.co.za', '0713344556', 'Librarian', '2021-08-22', 30000.00),
('Tumi', 'Van der Merwe', 'tumi.v@library.co.za', '0724455667', 'Assistant', '2022-01-05', 25000.00),
('Jacob', 'Smith', 'jacob.s@library.co.za', '0845566778', 'Admin', '2019-11-18', 28000.00),
('Puleng', 'Ndlovu', 'puleng.n@library.co.za', '0796677889', 'Librarian', '2023-03-30', 31000.00);

-- BOOK_AUTHORS data
INSERT INTO book_authors (book_id, author_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 3), 
(6, 5), (7, 6), (8, 7), (9, 8), (10, 9);

-- BOOK_CATEGORIES data
INSERT INTO book_categories (book_id, category_id) VALUES
(1, 3), (1, 6), (2, 3), (2, 8), (3, 3), 
(3, 6), (4, 4), (4, 8), (5, 3), (5, 6),
(6, 4), (6, 5), (6, 7), (7, 3), (7, 8),
(8, 3), (8, 6), (9, 3), (9, 8), (10, 3), (10, 8);

-- LOANS data
INSERT INTO loans (book_id, member_id, staff_id, loan_date, due_date, return_date, status) VALUES
(1, 1, 2, '2024-01-10', '2024-02-10', '2024-02-08', 'Returned'),
(4, 2, 3, '2024-02-15', '2024-03-15', NULL, 'Borrowed'),
(6, 3, 2, '2024-03-01', '2024-04-01', '2024-04-05', 'Overdue'),
(2, 4, 3, '2024-03-10', '2024-04-10', NULL, 'Borrowed'),
(8, 5, 4, '2024-01-20', '2024-02-20', '2024-03-15', 'Overdue'),
(3, 6, 6, '2024-03-25', '2024-04-25', NULL, 'Borrowed'),
(5, 7, 2, '2024-02-05', '2024-03-05', '2024-03-01', 'Returned'),
(7, 1, 3, '2024-04-01', '2024-05-01', NULL, 'Borrowed'),
(9, 2, 6, '2024-03-18', '2024-04-18', NULL, 'Borrowed'),
(10, 3, 2, '2024-02-28', '2024-03-28', '2024-03-30', 'Overdue');

-- FINES data (in ZAR)
INSERT INTO fines (loan_id, amount, fine_date, payment_date, status) VALUES
(3, 80.00, '2024-04-02', NULL, 'Pending'),
(5, 500.00, '2024-02-21', '2024-03-10', 'Paid'),
(10, 40.00, '2024-03-29', NULL, 'Pending');

-- RESERVATIONS data
INSERT INTO reservations (book_id, member_id, reservation_date, expiry_date, status) VALUES
(1, 7, '2024-04-05', '2024-04-12', 'Fulfilled'),
(6, 4, '2024-04-10', '2024-04-17', 'Active'),
(4, 5, '2024-03-20', '2024-03-27', 'Expired');

-- EVENTS data (South African library events)
INSERT INTO events (title, description, event_date, start_time, end_time, location, max_attendees, organizer_staff_id) VALUES
('Freedom Day Reading', 'Celebrate Freedom Day with readings from South African literature', '2024-04-27', '14:00:00', '16:00:00', 'Main Reading Room', 50, 1),
('Youth Day Book Club', 'Discussion of contemporary South African YA literature', '2024-06-16', '15:30:00', '17:00:00', 'Community Hall', 30, 2),
('Heritage Day Storytelling', 'Traditional storytelling in multiple South African languages', '2024-09-24', '10:00:00', '12:00:00', 'Children''s Section', 40, 3),
('Author Talk: Zakes Mda', 'Discussion with renowned South African author Zakes Mda', '2024-05-15', '18:00:00', '20:00:00', 'Auditorium', 100, 1);

-- EVENT_ATTENDEES data
INSERT INTO event_attendees (event_id, member_id, attendance_status) VALUES
(1, 1, 'Attended'),
(1, 3, 'Attended'),
(1, 6, 'No-show'),
(2, 2, 'Registered'),
(2, 4, 'Registered'),
(4, 1, 'Registered'),
(4, 7, 'Registered');
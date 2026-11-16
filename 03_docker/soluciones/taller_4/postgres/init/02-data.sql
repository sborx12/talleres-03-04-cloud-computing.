
-- Estudiantes
INSERT INTO academia.students (name, email) VALUES
('Ana', 'ana@example.com'),
('Luis', 'luis@example.com'),
('Marta', 'marta@example.com');

-- Profesores
INSERT INTO academia.teachers (name, email) VALUES
('Carlos', 'carlos@example.com'),
('Laura', 'laura@example.com');

-- Cursos asociados a profesores
INSERT INTO academia.courses (name, credits, teacher_id) VALUES
('Cloud Computing', 3, 1),
('Internet of Things', 4, 2);

-- Inscripciones de estudiantes a cursos
INSERT INTO academia.enrollments (student_id, course_id) VALUES
(1, 1),
(2, 1),
(3, 2);

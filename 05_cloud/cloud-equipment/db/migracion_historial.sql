
-- Crear tabla para registrar el historial de asignaciones
-- No elimina las tablas ni los datos existentes

CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    equipment_id INTEGER NOT NULL REFERENCES equipment(id),
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Crear índice para consultar rápidamente
-- las asignaciones de cada equipo

CREATE INDEX IF NOT EXISTS idx_assignments_equipment
ON assignments(equipment_id);

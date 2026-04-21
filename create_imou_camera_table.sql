CREATE USER imou WITH PASSWORD '123456@';
CREATE DATABASE imou_camera;
GRANT ALL PRIVILEGES ON DATABASE imou_camera TO imou;
ALTER DATABASE imou_camera OWNER TO imou;
GRANT ALL ON SCHEMA public TO imou;

create table imou_camera_log (
    id SERIAL PRIMARY KEY,
    alarm_id VARCHAR(255) NOT NULL,
    dname VARCHAR(255) NOT NULL,
    msg_type VARCHAR(255) NOT NULL,
    thumb_url VARCHAR(255),
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
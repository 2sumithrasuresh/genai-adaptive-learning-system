import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "adaptive_engine")
    )

def init_db():
    # First connect without a database to create it if needed
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "")
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS adaptive_engine")
    cursor.execute("USE adaptive_engine")

    # students table — exactly as per plan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id VARCHAR(100) NOT NULL,
            topic VARCHAR(200) NOT NULL,
            mastery_score FLOAT DEFAULT 0.0,
            attempts INT DEFAULT 0,
            correct_count INT DEFAULT 0,
            wrong_count INT DEFAULT 0,
            last_mistake_type VARCHAR(50) DEFAULT '',
            difficulty_level INT DEFAULT 1,
            PRIMARY KEY (id, topic)
        )
    """)

    # sessions table — exactly as per plan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id VARCHAR(100) PRIMARY KEY,
            student_id VARCHAR(100) NOT NULL,
            topic VARCHAR(200) NOT NULL,
            timestamp DATETIME NOT NULL
        )
    """)

    # attempt_logs table — exactly as per plan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attempt_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(100) NOT NULL,
            question TEXT NOT NULL,
            expected_answer TEXT NOT NULL,
            student_answer TEXT NOT NULL,
            correctness VARCHAR(20) NOT NULL,
            score FLOAT NOT NULL,
            mistake_type VARCHAR(50) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
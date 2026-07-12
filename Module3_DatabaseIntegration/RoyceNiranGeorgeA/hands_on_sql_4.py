import time
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'college_db'
}

def run_performance_test():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query_count_n1 = 0
    start_time_n1 = time.time()

    cursor.execute("SELECT * FROM enrollments;")
    enrollments = cursor.fetchall()
    query_count_n1 += 1

    for row in enrollments:
        cursor.execute("SELECT first_name, last_name FROM students WHERE student_id = %s;", (row['student_id'],))
        student = cursor.fetchone()
        query_count_n1 += 1

    end_time_n1 = time.time()
    time_taken_n1 = end_time_n1 - start_time_n1
    print(f"Total Queries Executed: {query_count_n1}")
    print(f"Time Taken: {time_taken_n1:.6f} seconds\n")


    query_count_join = 0
    start_time_join = time.time()

    join_query = """
        SELECT e.*, s.first_name, s.last_name 
        FROM enrollments e 
        JOIN students s ON e.student_id = s.student_id;
    """
    cursor.execute(join_query)
    optimized_results = cursor.fetchall()
    query_count_join += 1

    end_time_join = time.time()
    time_taken_join = end_time_join - start_time_join
    print(f"Total Queries Executed: {query_count_join}")
    print(f"Time Taken: {time_taken_join:.6f} seconds\n")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_performance_test()
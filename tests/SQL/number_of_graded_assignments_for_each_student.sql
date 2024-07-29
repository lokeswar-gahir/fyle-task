-- database: ../../core/store.sqlite3
-- Write query to get number of graded assignments for each student:
select count(*) as grade_count from assignments WHERE state = "GRADED" GROUP BY student_id order BY grade_count ASC;
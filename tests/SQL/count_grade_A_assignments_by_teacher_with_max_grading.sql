-- database: ../../core/store.sqlite3
-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

select count(*) from assignments where teacher_id = (select teacher_id from (select teacher_id, max(count) as maximum from (SELECT teacher_id, count(*) as count FROM assignments GROUP BY teacher_id))) AND grade='A';
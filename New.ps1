Generate a SQL query based on the user-provided natural language instructions. The prompt should:

Identify the operation type (e.g., SELECT, INSERT, UPDATE, DELETE).
Extract key elements such as table name, columns, conditions, sorting, or grouping from the input text.
Handle ambiguities by making logical assumptions where necessary and provide comments in the query to explain assumptions.
Format the SQL query clearly and ensure proper syntax.
Include support for:

Data retrieval (SELECT queries with filtering, ordering, and grouping).
Data manipulation (INSERT, UPDATE, DELETE).
Basic and complex conditions.

Example Input:
"Generate a SQL query to retrieve data from the 'Employees' table. Select the 'Name' and 'Salary' columns where the 'Department' column equals 'Sales' and the 'Salary' column is greater than 50000. Order the results by 'Salary' in descending order."

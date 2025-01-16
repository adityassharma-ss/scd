import re
from graphviz import Digraph

def extract_tasks(description):
    tasks = []
    task_pattern = r"([A-Za-z0-9\s]+(?:task|action|step)[A-Za-z0-9\s]*)"
    matches = re.findall(task_pattern, description)
    tasks = [match.strip() for match in matches]
    return tasks

def extract_dependencies(description):
    dependencies = []
    dependency_pattern = r"(Task\s+\d+)\s+depends\s+on\s+(Task\s+\d+)"
    matches = re.findall(dependency_pattern, description)
    dependencies = [(match[0], match[1]) for match in matches]
    return dependencies

def generate_flow_diagram(tasks, dependencies):
    dot = Digraph(format='png')
    for task in tasks:
        dot.node(task)
    for dep in dependencies:
        dot.edge(dep[0], dep[1])
    diagram_path = '/tmp/flow_diagram'
    dot.render(diagram_path)
    return f"{diagram_path}.png"

def process_jira_description(description):
    tasks = extract_tasks(description)
    dependencies = extract_dependencies(description)
    diagram_path = generate_flow_diagram(tasks, dependencies)
    return diagram_path

description = """
Task 1: Initiate user login process.
Task 2: Validate user credentials.
Task 3: Create user session after validation.
Task 4: Display user dashboard.
Task 5: Logout user.
Task 3 depends on Task 2.
Task 4 depends on Task 3.
Task 5 depends on Task 4.
"""

diagram_path = process_jira_description(description)
print(f"Flow diagram generated at: {diagram_path}")

class SemanticAnalyzer:
    def __init__(self, symbol_table, error_handler):
        self.symbol_table = symbol_table
        self.error_handler = error_handler

    def analyze(self):
        tasks = self.symbol_table.tasks

        for task_name, details in tasks.items():
            for req in details['requires']:
                if not self.symbol_table.task_exists(req):
                    self.error_handler.report_error("Semantic", "Unknown", f"Task '{task_name}' requires '{req}', but '{req}' does not exist!")
                    return False

        visited = set()
        recursion_stack = set()

        def dfs(current_task):
            if current_task in recursion_stack:
                self.error_handler.report_error("Semantic", "Unknown", f"Infinite Loop! Circular dependency detected involving '{current_task}'.")
                return True
            
            if current_task in visited:
                return False

            visited.add(current_task)
            recursion_stack.add(current_task)

            for req in tasks[current_task]['requires']:
                if dfs(req):
                    return True

            recursion_stack.remove(current_task)
            return False

        for task_name in tasks:
            if dfs(task_name):
                return False 

        return True
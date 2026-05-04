class IRGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.graph = {}

    def generate(self):
        tasks = self.symbol_table.tasks

        for task_name, details in tasks.items():
            self.graph[task_name] = {
                "duration": details["duration"],
                "predecessors": details["requires"], 
                "successors": [],                     
                "assigned": details["assigned"]
            }

        for task_name, details in tasks.items():
            for req in details["requires"]:
                self.graph[req]["successors"].append(task_name)

        return self.graph
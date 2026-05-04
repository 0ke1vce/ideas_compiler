class SymbolTable:
    def __init__(self):
        self.tasks = {}

    def add_task(self, name, duration, requires=None, assigned="Unassigned"):
        if name in self.tasks:
            return False 
        
        if requires is None:
            requires = []

        self.tasks[name] = {
            "duration": duration,
            "requires": requires,
            "assigned": assigned
        }
        return True

    def get_task(self, name):
        return self.tasks.get(name)

    def task_exists(self, name):
        return name in self.tasks

    def print_table(self):
        print("\n--- Current Symbol Table ---")
        for task_name, details in self.tasks.items():
            print(f"Task: {task_name} | Duration: {details['duration']} | Requires: {details['requires']} | Assigned: {details['assigned']}")
        print("----------------------------\n")
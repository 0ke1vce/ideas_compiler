class Optimizer:
    def __init__(self, graph):
        self.graph = graph
        self.schedule = {}
        self.total_duration = 0

    def optimize(self):
        unresolved_tasks = set(self.graph.keys())
        resource_calendar = {} 

        # --- FORWARD PASS (Find Earliest Start Days) ---
        while unresolved_tasks:
            progress_made = False
            for task_name in list(unresolved_tasks):
                preds = self.graph[task_name]["predecessors"]
                assignee = self.graph[task_name]["assigned"]
                
                can_schedule = all(p in self.schedule for p in preds)
                if can_schedule:
                    if not preds:
                        actual_start = 1
                    else:
                        actual_start = max(self.schedule[p]["end_day"] for p in preds) + 1
                        
                    duration = self.graph[task_name]["duration"]
                    
                    if assignee != "Unassigned":
                        if assignee not in resource_calendar:
                            resource_calendar[assignee] = set()
                        while any(day in resource_calendar[assignee] for day in range(actual_start, actual_start + duration)):
                            actual_start += 1
                        for day in range(actual_start, actual_start + duration):
                            resource_calendar[assignee].add(day)
                    
                    end_day = actual_start + duration - 1
                    
                    self.schedule[task_name] = {
                        "start_day": actual_start,
                        "end_day": end_day,
                        "duration": duration,
                        "assigned": assignee
                    }
                    
                    if end_day > self.total_duration:
                        self.total_duration = end_day
                        
                    unresolved_tasks.remove(task_name)
                    progress_made = True
            
            if not progress_made:
                print("Error: Optimizer stuck!")
                break

        # --- BACKWARD PASS (Find Critical Path & Slack) ---
        # 1. Initialize latest possible dates based on total project duration
        for task in self.schedule:
            self.schedule[task]["late_finish"] = self.total_duration
            self.schedule[task]["late_start"] = self.total_duration - self.schedule[task]["duration"] + 1

        # 2. Work backwards from successors to predecessors
        changed = True
        while changed:
            changed = False
            for task_name, times in self.schedule.items():
                successors = self.graph[task_name]["successors"]
                if successors:
                    # A task's Late Finish is dictated by the Late Start of whatever relies on it
                    min_lf = min(self.schedule[succ]["late_start"] - 1 for succ in successors if succ in self.schedule)
                    if min_lf < times["late_finish"]:
                        times["late_finish"] = min_lf
                        times["late_start"] = times["late_finish"] - times["duration"] + 1
                        changed = True

        # 3. Calculate Slack (Late Start - Early Start)
        for task_name, times in self.schedule.items():
            slack = times["late_start"] - times["start_day"]
            times["slack_days"] = slack
            times["is_critical"] = (slack == 0) # If slack is 0, it's a bottleneck!

        return self.schedule
import json

class CodeGenerator:
    def __init__(self, schedule, total_duration):
        self.schedule = schedule
        self.total_duration = total_duration

    def generate_json(self, output_filename="project_schedule.json"):
        output_data = {
            "compiler_status": "Success",
            "total_project_days": self.total_duration,
            "tasks": []
        }

        for task_name, times in self.schedule.items():
            task_data = {
                "task_name": task_name,
                "start_day": times["start_day"],
                "end_day": times["end_day"],
                "duration": times["duration"],
                "assigned": times["assigned"],
                "is_critical": times["is_critical"],
                "slack_days": times["slack_days"]
            }
            output_data["tasks"].append(task_data)

        output_data["tasks"].sort(key=lambda x: x["start_day"])

        with open(output_filename, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)

        return output_filename
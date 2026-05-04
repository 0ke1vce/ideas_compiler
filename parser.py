class Parser:
    def __init__(self, tokens, symbol_table, error_handler):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.error_handler = error_handler
        self.current_pos = 0
        self.ast = [] 

    def get_current_token(self):
        if self.current_pos < len(self.tokens):
            return self.tokens[self.current_pos]
        return None

    def advance(self):
        self.current_pos += 1

    def match(self, expected_type):
        token = self.get_current_token()
        if token and token['type'] == expected_type:
            self.advance()
            return token
        else:
            actual_type = token['type'] if token else "END OF FILE"
            line = token['line'] if token else "Unknown"
            self.error_handler.report_error("Syntax", line, f"Expected {expected_type}, but got {actual_type}")
            return None

    def parse(self):
        while self.current_pos < len(self.tokens):
            token = self.get_current_token()
            if token['type'] == 'KEYWORD' and token['value'] == 'TASK':
                self.parse_task()
            else:
                self.error_handler.report_error("Syntax", token['line'], f"Unexpected word: {token['value']}")
                self.advance() 
        return self.ast

    def parse_task(self):
        self.advance() 
        
        name_token = self.match('IDENT')
        if not name_token: return
        task_name = name_token['value']

        duration_kw = self.get_current_token()
        if duration_kw and duration_kw['value'] == 'DURATION':
            self.advance()
        else:
            self.error_handler.report_error("Syntax", name_token['line'], "Expected 'DURATION' after task name")
            return

        duration_token = self.match('NUMBER')
        if not duration_token: return
        task_duration = int(duration_token['value'])

        requires_list = []
        assigned_person = "Unassigned"

        while True:
            next_token = self.get_current_token()
            if not next_token or (next_token['type'] == 'KEYWORD' and next_token['value'] == 'TASK'):
                break

            if next_token['value'] == 'REQUIRES':
                self.advance() 
                while True:
                    dep_token = self.match('IDENT')
                    if dep_token:
                        requires_list.append(dep_token['value'])
                    
                    check_comma = self.get_current_token()
                    if check_comma and check_comma['type'] == 'COMMA':
                        self.advance() 
                    else:
                        break 

            elif next_token['value'] == 'ASSIGNED':
                self.advance() 
                person_token = self.match('IDENT')
                if person_token:
                    assigned_person = person_token['value']
            
            else:
                break

        success = self.symbol_table.add_task(task_name, task_duration, requires_list, assigned_person)
        if not success:
            self.error_handler.report_error("Semantic", name_token['line'], f"Task '{task_name}' is defined twice!")
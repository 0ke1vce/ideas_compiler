import re

TOKEN_SPECIFICATION = [
    ('KEYWORD',  r'\b(TASK|DURATION|REQUIRES|ASSIGNED)\b'), 
    ('NUMBER',   r'\d+'),                          
    ('IDENT',    r'[a-zA-Z_]\w*'),                 
    ('COMMA',    r','),                            
    ('NEWLINE',  r'\n'),                           
    ('SKIP',     r'[ \t]+'),                       
    ('MISMATCH', r'.'),                            
]

class Lexer:
    def __init__(self, error_handler):
        self.error_handler = error_handler
        self.regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)

    def tokenize(self, source_code):
        tokens = []
        line_number = 1

        for match in re.finditer(self.regex, source_code):
            kind = match.lastgroup
            value = match.group()

            if kind == 'NEWLINE':
                line_number += 1
            elif kind == 'SKIP':
                pass 
            elif kind == 'MISMATCH':
                self.error_handler.report_error("Lexical", line_number, f"Unexpected character '{value}'")
            else:
                tokens.append({'type': kind, 'value': value, 'line': line_number})

        return tokens
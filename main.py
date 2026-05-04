import os
from error_handler import ErrorHandler
from symbol_table import SymbolTable
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from ir_gen import IRGenerator
from optimizer import Optimizer
from codegen import CodeGenerator # <-- NEW IMPORT

def compile_ideas(file_path):
    print("\n=== IDEAS Compiler Started ===")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: Could not find '{file_path}'")
        return

    with open(file_path, 'r') as file:
        source_code = file.read()

    error_handler = ErrorHandler()
    symbol_table = SymbolTable()
    
    # Phase 1
    lexer = Lexer(error_handler)
    tokens = lexer.tokenize(source_code)
    if error_handler.has_error: return

    # Phase 2
    parser = Parser(tokens, symbol_table, error_handler)
    parser.parse()
    if error_handler.has_error: return
        
    # Phase 3
    semantic = SemanticAnalyzer(symbol_table, error_handler)
    if not semantic.analyze() or error_handler.has_error: return

    # Phase 4
    ir_gen = IRGenerator(symbol_table)
    graph_blueprint = ir_gen.generate()
    
    # Phase 5
    optimizer = Optimizer(graph_blueprint)
    schedule = optimizer.optimize()

    # --- PHASE 6: CODE GENERATION ---
    print("\n[Phase 6] Code Generation: Creating final JSON output...")
    codegen = CodeGenerator(schedule, optimizer.total_duration)
    output_file = codegen.generate_json()
    
    print(f"\n🎉 COMPILATION SUCCESSFUL! 🎉")
    print(f"Your compiled project plan has been saved to: {output_file}")
    print("==============================\n")

if __name__ == "__main__":
    target_file = "examples/test_script.txt"
    compile_ideas(target_file)
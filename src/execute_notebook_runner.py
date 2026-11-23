#!/usr/bin/env python3
"""
Exécuteur Réel de Notebook avec Capture d'Outputs
GCI World 2026 September - Final Assignment
"""
import sys
import os
import json
import io
import contextlib
import base64
from IPython.core.interactiveshell import InteractiveShell

NOTEBOOK_PATH = "/Users/baptistebedeaux/gci_final_assignment/notebooks/BaptisteBdx.ipynb"

def execute_notebook():
    print("="*60)
    print("EXÉCUTION RÉELLE CELLULE PAR CELLULE DU NOTEBOOK")
    print("="*60)
    
    with open(NOTEBOOK_PATH, "r") as f:
        nb = json.load(f)
        
    shell = InteractiveShell.instance()
    
    # Changer le répertoire courant pour correspondre au notebook
    os.chdir("/Users/baptistebedeaux/gci_final_assignment/notebooks")
    
    execution_count = 1
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] == "code":
            code = "".join(cell["source"])
            print(f"\n--- Exécution de la cellule de code {execution_count} (index {i}) ---")
            print(f"Extrait : {code[:120].strip()}...")
            
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                result = shell.run_cell(code)
                
            stdout_text = stdout_capture.getvalue()
            stderr_text = stderr_capture.getvalue()
            
            cell["execution_count"] = execution_count
            outputs = []
            
            if stdout_text:
                outputs.append({
                    "output_type": "stream",
                    "name": "stdout",
                    "text": [line + "\n" for line in stdout_text.rstrip("\n").split("\n")]
                })
                print("STDOUT :", stdout_text[:200].replace("\n", " "))
                
            if stderr_text:
                outputs.append({
                    "output_type": "stream",
                    "name": "stderr",
                    "text": [line + "\n" for line in stderr_text.rstrip("\n").split("\n")]
                })
                print("STDERR :", stderr_text[:200].replace("\n", " "))
                
            if result.result is not None:
                res_repr = repr(result.result)
                outputs.append({
                    "output_type": "execute_result",
                    "execution_count": execution_count,
                    "data": {
                        "text/plain": [line + "\n" for line in res_repr.rstrip("\n").split("\n")]
                    },
                    "metadata": {}
                })
                print("RESULT :", res_repr[:200].replace("\n", " "))
                
            cell["outputs"] = outputs
            execution_count += 1
            
    with open(NOTEBOOK_PATH, "w") as f:
        json.dump(nb, f, indent=2)
        
    print("\n" + "="*60)
    print("NOTEBOOK INTÉGRALEMENT EXÉCUTÉ ET SAUVEGARDÉ !")
    print(f"Fichier : {NOTEBOOK_PATH}")
    print("="*60)

if __name__ == "__main__":
    execute_notebook()

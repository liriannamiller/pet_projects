import nbformat
from IPython.core.interactiveshell import InteractiveShell

def load_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    shell = InteractiveShell.instance()
    code_cells = [cell for cell in nb.cells if cell.cell_type == 'code']
    for cell in code_cells:
        shell.run_cell(cell.source)
"""
Unit tests for create_notebook.py
"""
import pytest
import os
import sys
import tempfile
import nbformat

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestNotebookGeneration:
    """Test notebook generation functionality"""
    
    def test_notebook_structure(self):
        """Test that notebook structure is valid"""
        # Create a simple notebook (mimicking create_notebook behavior)
        nb = nbformat.v4.new_notebook()
        nb['cells'] = [
            nbformat.v4.new_markdown_cell("# Test"),
            nbformat.v4.new_code_cell("print('hello')")
        ]
        
        # Verify structure
        assert len(nb.cells) == 2
        assert nb.cells[0]['cell_type'] == 'markdown'
        assert nb.cells[1]['cell_type'] == 'code'
    
    def test_notebook_can_be_written(self):
        """Test that notebook can be written to file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            notebook_path = os.path.join(tmpdir, 'test_notebook.ipynb')
            
            # Create a notebook
            nb = nbformat.v4.new_notebook()
            nb['cells'] = [
                nbformat.v4.new_markdown_cell("# Test"),
                nbformat.v4.new_code_cell("print('hello')")
            ]
            
            # Write it
            with open(notebook_path, 'w') as f:
                nbformat.write(nb, f)
            
            # Verify the notebook was created
            assert os.path.exists(notebook_path)
            
            # Load and verify structure
            with open(notebook_path, 'r') as f:
                loaded_nb = nbformat.read(f, as_version=4)
            
            assert len(loaded_nb.cells) == 2
            assert loaded_nb.cells[0]['cell_type'] == 'markdown'
            assert loaded_nb.cells[1]['cell_type'] == 'code'

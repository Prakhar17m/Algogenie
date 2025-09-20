import streamlit as st
import json
from datetime import datetime
from pathlib import Path

class SolutionEditor:
    def __init__(self, solutions_dir="solutions"):
        self.solutions_dir = Path(solutions_dir)
        self.solutions_dir.mkdir(exist_ok=True)
    
    def render_editor(self, solution_data=None):
        """Render the solution editor"""
        st.markdown("### ✏️ Solution Editor")
        
        if solution_data is None:
            st.info("No solution selected for editing")
            return
        
        # Problem editing
        st.markdown("#### 📝 Problem Description")
        problem = st.text_area(
            "Problem:",
            value=solution_data['problem'],
            height=100,
            key="edit_problem"
        )
        
        # Code editing
        st.markdown("#### 💻 Code")
        code = st.text_area(
            "Python Code:",
            value=solution_data['code'],
            height=400,
            key="edit_code"
        )
        
        # Explanation editing
        st.markdown("#### 📖 Explanation")
        explanation = st.text_area(
            "Explanation:",
            value=solution_data.get('explanation', ''),
            height=150,
            key="edit_explanation"
        )
        
        # Test cases
        st.markdown("#### 🧪 Test Cases")
        test_cases = st.text_area(
            "Test Cases (one per line):",
            value="\n".join(solution_data.get('test_results', [])),
            height=100,
            key="edit_test_cases"
        )
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save Changes", type="primary"):
                self.save_solution({
                    'id': solution_data['id'],
                    'timestamp': solution_data['timestamp'],
                    'problem': problem,
                    'code': code,
                    'explanation': explanation,
                    'test_results': [tc.strip() for tc in test_cases.split('\n') if tc.strip()]
                })
                st.success("Solution saved!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset"):
                st.rerun()
        
        with col3:
            if st.button("▶️ Run Code"):
                self.run_code(code)
        
        with col4:
            if st.button("📤 Export"):
                self.export_solution({
                    'id': solution_data['id'],
                    'timestamp': solution_data['timestamp'],
                    'problem': problem,
                    'code': code,
                    'explanation': explanation,
                    'test_results': [tc.strip() for tc in test_cases.split('\n') if tc.strip()]
                })
    
    def save_solution(self, solution_data):
        """Save solution to file"""
        try:
            # Update timestamp if content changed
            solution_data['last_modified'] = datetime.now().isoformat()
            
            # Save JSON
            json_file = self.solutions_dir / f"{solution_data['id']}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(solution_data, f, indent=2, ensure_ascii=False)
            
            # Save Python file
            py_file = self.solutions_dir / f"{solution_data['id']}.py"
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(solution_data['code'])
            
            return True
        except Exception as e:
            st.error(f"Error saving solution: {e}")
            return False
    
    def run_code(self, code):
        """Run the code and show results"""
        try:
            st.markdown("#### 🏃‍♂️ Code Execution Results")
            
            # Create a temporary file and run it
            import tempfile
            import subprocess
            import sys
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    st.success("✅ Code executed successfully!")
                    if result.stdout:
                        st.code(result.stdout, language='text')
                else:
                    st.error("❌ Code execution failed!")
                    if result.stderr:
                        st.code(result.stderr, language='text')
                
            finally:
                import os
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            st.error("⏰ Code execution timed out!")
        except Exception as e:
            st.error(f"Error running code: {e}")
    
    def export_solution(self, solution_data):
        """Export solution in different formats"""
        try:
            # Create export directory
            export_dir = self.solutions_dir / "exports"
            export_dir.mkdir(exist_ok=True)
            
            # Export as Python file with documentation
            py_file = export_dir / f"{solution_data['id']}_export.py"
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(f'"""\n')
                f.write(f"Problem: {solution_data['problem']}\n")
                f.write(f"Created: {solution_data['timestamp']}\n")
                f.write(f"Last Modified: {solution_data.get('last_modified', 'N/A')}\n")
                f.write(f"\nExplanation:\n{solution_data['explanation']}\n")
                f.write(f'"""\n\n')
                f.write(solution_data['code'])
            
            # Export as Markdown
            md_file = export_dir / f"{solution_data['id']}_export.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(f"# {solution_data['problem']}\n\n")
                f.write(f"**Created:** {solution_data['timestamp']}\n")
                f.write(f"**Last Modified:** {solution_data.get('last_modified', 'N/A')}\n\n")
                f.write(f"## Explanation\n\n{solution_data['explanation']}\n\n")
                f.write(f"## Code\n\n```python\n{solution_data['code']}\n```\n\n")
                if solution_data.get('test_results'):
                    f.write(f"## Test Cases\n\n")
                    for i, test in enumerate(solution_data['test_results'], 1):
                        f.write(f"{i}. {test}\n")
            
            st.success(f"Solution exported to: {export_dir}")
            
        except Exception as e:
            st.error(f"Error exporting solution: {e}")

def render_solution_editor():
    """Render the solution editor component"""
    editor = SolutionEditor()
    
    if 'editing_solution' in st.session_state:
        editor.render_editor(st.session_state.editing_solution)
    else:
        st.info("Select a solution to edit from the file browser")

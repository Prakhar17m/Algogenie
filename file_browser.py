import streamlit as st
import os
import json
from pathlib import Path
from datetime import datetime
import subprocess
import platform

class SolutionBrowser:
    def __init__(self, solutions_dir="solutions"):
        self.solutions_dir = Path(solutions_dir)
        self.solutions_dir.mkdir(exist_ok=True)
    
    def get_solutions(self):
        """Get all saved solutions"""
        solutions = []
        for solution_file in self.solutions_dir.glob("*.json"):
            try:
                with open(solution_file, 'r', encoding='utf-8') as f:
                    solution_data = json.load(f)
                    solutions.append(solution_data)
            except Exception as e:
                st.error(f"Error loading {solution_file}: {e}")
        
        return sorted(solutions, key=lambda x: x['timestamp'], reverse=True)
    
    def open_file_explorer(self):
        """Open file explorer to solutions directory"""
        try:
            if platform.system() == "Windows":
                os.startfile(str(self.solutions_dir.absolute()))
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(self.solutions_dir.absolute())])
            else:  # Linux
                subprocess.run(["xdg-open", str(self.solutions_dir.absolute())])
        except Exception as e:
            st.error(f"Could not open file explorer: {e}")
    
    def delete_solution(self, solution_id):
        """Delete a solution"""
        try:
            json_file = self.solutions_dir / f"{solution_id}.json"
            py_file = self.solutions_dir / f"{solution_id}.py"
            
            if json_file.exists():
                json_file.unlink()
            if py_file.exists():
                py_file.unlink()
            
            return True
        except Exception as e:
            st.error(f"Error deleting solution: {e}")
            return False
    
    def export_solution(self, solution_data, format="zip"):
        """Export solution in different formats"""
        try:
            if format == "zip":
                import zipfile
                zip_path = self.solutions_dir / f"{solution_data['id']}.zip"
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    zipf.writestr("solution.py", solution_data['code'])
                    zipf.writestr("solution.json", json.dumps(solution_data, indent=2))
                    zipf.writestr("README.md", f"# {solution_data['problem']}\n\n{solution_data['explanation']}")
                return zip_path
            elif format == "py":
                py_path = self.solutions_dir / f"{solution_data['id']}_export.py"
                with open(py_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {solution_data['problem']}\n")
                    f.write(f"# Generated on: {solution_data['timestamp']}\n\n")
                    f.write(solution_data['code'])
                return py_path
        except Exception as e:
            st.error(f"Error exporting solution: {e}")
            return None

def render_file_browser():
    """Render the file browser component"""
    browser = SolutionBrowser()
    solutions = browser.get_solutions()
    
    st.markdown("### 📁 Solution Browser")
    
    if not solutions:
        st.info("No solutions found. Solve some problems first!")
        return
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search solutions:", placeholder="Enter problem description...")
    with col2:
        sort_by = st.selectbox("Sort by:", ["Newest", "Oldest", "Problem"])
    
    # Filter solutions
    filtered_solutions = solutions
    if search_term:
        filtered_solutions = [s for s in solutions if search_term.lower() in s['problem'].lower()]
    
    # Sort solutions
    if sort_by == "Newest":
        filtered_solutions = sorted(filtered_solutions, key=lambda x: x['timestamp'], reverse=True)
    elif sort_by == "Oldest":
        filtered_solutions = sorted(filtered_solutions, key=lambda x: x['timestamp'])
    elif sort_by == "Problem":
        filtered_solutions = sorted(filtered_solutions, key=lambda x: x['problem'])
    
    # Display solutions
    for i, solution in enumerate(filtered_solutions):
        with st.expander(f"📄 {solution['problem'][:60]}{'...' if len(solution['problem']) > 60 else ''}", expanded=False):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**Created:** {solution['timestamp'][:19]}")
                st.write(f"**Problem:** {solution['problem']}")
                
                if solution.get('test_results'):
                    st.write(f"**Test Results:** {len(solution['test_results'])} tests")
            
            with col2:
                if st.button("👁️ View", key=f"view_{solution['id']}"):
                    st.session_state.current_solution = solution
                    st.rerun()
                
                if st.button("📝 Edit", key=f"edit_{solution['id']}"):
                    st.session_state.editing_solution = solution
                    st.rerun()
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{solution['id']}"):
                    if browser.delete_solution(solution['id']):
                        st.success("Solution deleted!")
                        st.rerun()
                
                if st.button("📦 Export", key=f"export_{solution['id']}"):
                    zip_path = browser.export_solution(solution)
                    if zip_path:
                        st.success(f"Exported to: {zip_path}")
    
    # Quick actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📁 Open Folder", use_container_width=True):
            browser.open_file_explorer()
    
    with col2:
        if st.button("📊 Statistics", use_container_width=True):
            show_statistics(solutions)
    
    with col3:
        if st.button("🧹 Clear All", use_container_width=True):
            if st.session_state.get('confirm_clear_all', False):
                for solution in solutions:
                    browser.delete_solution(solution['id'])
                st.success("All solutions cleared!")
                st.session_state.confirm_clear_all = False
                st.rerun()
            else:
                st.session_state.confirm_clear_all = True
                st.warning("Click again to confirm deletion of all solutions")

def show_statistics(solutions):
    """Show solution statistics"""
    if not solutions:
        st.info("No solutions to analyze")
        return
    
    st.markdown("### 📊 Solution Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Solutions", len(solutions))
    
    with col2:
        recent_count = len([s for s in solutions if 
                          (datetime.now() - datetime.fromisoformat(s['timestamp'])).days <= 7])
        st.metric("This Week", recent_count)
    
    with col3:
        avg_code_length = sum(len(s['code'].split('\n')) for s in solutions) / len(solutions)
        st.metric("Avg Code Lines", f"{avg_code_length:.1f}")
    
    with col4:
        unique_problems = len(set(s['problem'] for s in solutions))
        st.metric("Unique Problems", unique_problems)
    
    # Problem categories
    st.markdown("#### 🏷️ Problem Categories")
    categories = {}
    for solution in solutions:
        problem = solution['problem'].lower()
        if 'sort' in problem or 'merge' in problem or 'quick' in problem:
            categories['Sorting'] = categories.get('Sorting', 0) + 1
        elif 'search' in problem or 'binary' in problem:
            categories['Searching'] = categories.get('Searching', 0) + 1
        elif 'tree' in problem or 'binary tree' in problem:
            categories['Trees'] = categories.get('Trees', 0) + 1
        elif 'graph' in problem or 'bfs' in problem or 'dfs' in problem:
            categories['Graphs'] = categories.get('Graphs', 0) + 1
        elif 'dynamic' in problem or 'dp' in problem:
            categories['Dynamic Programming'] = categories.get('Dynamic Programming', 0) + 1
        else:
            categories['Other'] = categories.get('Other', 0) + 1
    
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        st.write(f"**{category}:** {count} solutions")

document.addEventListener('DOMContentLoaded', function() {
    // We look for the editor inside our specific wrapper
    const codingEnv = document.querySelector('.coding-environment');
    
    if (codingEnv) {
        const editor = document.getElementById('editor');

        // 1. Enable Tab Indentation (4 spaces)
        editor.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.selectionStart;
                const end = this.selectionEnd;

                // Insert 4 spaces
                this.value = this.value.substring(0, start) + "    " + this.value.substring(end);

                // Put caret in right position
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });

        // 2. Form Validation
        const form = document.getElementById('code-submission-form');
        form.addEventListener('submit', function(e) {
            const code = editor.value.trim();
            if (code === "") {
                alert("The editor is empty. Please write your Python solution!");
                e.preventDefault();
            }
        });

        // 3. Auto-scroll terminal to bottom if output exists
        const terminal = document.querySelector('.terminal');
        if (terminal) {
            terminal.scrollTop = terminal.scrollHeight;
        }
    }
});
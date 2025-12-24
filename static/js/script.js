document.addEventListener('DOMContentLoaded', function() {
    const editor = document.getElementById('editor');

    // 1. Enable Tab indentation in the textarea
    if (editor) {
        editor.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.selectionStart;
                const end = this.selectionEnd;

                // Set textarea value to: text before caret + tab + text after caret
                this.value = this.value.substring(0, start) +
                    "    " + this.value.substring(end);

                // Put caret in right position
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });
    }

    // 2. Simple confirmation before final submission
    const runBtn = document.querySelector('.run-btn');
    if (runBtn) {
        runBtn.addEventListener('click', function(e) {
            if (editor && editor.value.trim() === "") {
                alert("Please write some code before submitting!");
                e.preventDefault();
            }
        });
    }
});

// 3. Optional: Clear the console output after 10 seconds
const terminal = document.querySelector('.terminal');
if (terminal) {
    setTimeout(() => {
        console.log("Terminal ready for next execution.");
    }, 10000);
}
const themeToggle = document.getElementById("themeToggle");

// Restore the previous theme when possible.
try {
    if (localStorage.getItem("hospital-theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
} catch (error) {
    // The website still works if storage is unavailable.
}

function updateThemeButton() {
    if (!themeToggle) return;

    themeToggle.textContent =
        document.body.classList.contains("dark-mode")
            ? "☀ Light Mode"
            : "🌙 Dark Mode";
}

updateThemeButton();

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");

        try {
            localStorage.setItem(
                "hospital-theme",
                document.body.classList.contains("dark-mode")
                    ? "dark"
                    : "light"
            );
        } catch (error) {
            // Theme still changes for the current page.
        }

        updateThemeButton();
    });
}
// Handles night mode toggle
export function setupNightMode(nightModeToggle) {
  nightModeToggle.addEventListener('change', function () {
    document.body.classList.toggle('night-mode', this.checked)
  })
}

// Hamburger menu dropdown toggle logic
export function setupMenuDropdown() {
  const hamburgerMenu = document.getElementById('hamburger-menu')
  const menuDropdown = document.getElementById('menu-dropdown')
  if (!hamburgerMenu || !menuDropdown) return

  hamburgerMenu.addEventListener('click', () => {
    menuDropdown.classList.toggle('active')
  })

  // Optional: Hide dropdown when clicking outside
  document.addEventListener('click', e => {
    if (!hamburgerMenu.contains(e.target) && !menuDropdown.contains(e.target)) {
      menuDropdown.classList.remove('active')
    }
  })

  // Hide Optimal Fingering container by default
  window.addEventListener('DOMContentLoaded', () => {
    const containers = document.querySelectorAll('.container')
    containers.forEach(container => {
      const h2 = container.querySelector('h2')
      if (h2 && h2.textContent.includes('Optimal Fingering from MIDI File')) {
        container.style.display = 'none'
      }
    })
  })

  // Show/hide containers based on menu selection
  const menuItems = menuDropdown.querySelectorAll('.menu-item')
  const containers = document.querySelectorAll('.container')
  menuItems.forEach(item => {
    item.addEventListener('click', () => {
      menuDropdown.classList.remove('active')
      const view = item.getAttribute('data-view')
      containers.forEach(container => {
        // Match by heading text
        const h2 = container.querySelector('h2')
        if (!h2) return
        if (
          (view === 'neck' && h2.textContent.includes('Instrument Neck Visualizer')) ||
          (view === 'optimal' && h2.textContent.includes('Optimal Fingering from MIDI File'))
        ) {
          container.style.display = ''
        } else {
          container.style.display = 'none'
        }
      })
    })
  })
}

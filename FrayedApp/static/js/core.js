//Header Hamburger Profile, and Cart Open and Close
const hamOpen = document.getElementById("hamburgerOpen");
const hamClose = document.getElementById("hamburgerClose");
const hamMenucontainer = document.getElementById('hamburgerMenuContainer');
const hamMenuOverlay = document.getElementById('hamburgerMenuOverlay');
const profileBtn = document.getElementById("profileBtn");
const cartBtn = document.getElementById("cartBtn");
const profileDropdown = document.getElementById("profileDropdown");

hamOpen.addEventListener("click", () => {
  hamMenucontainer.style.display = "flex";
  hamMenuOverlay.style.display = "block";

  hamOpen.classList.add("hamburgerActive");
  hamClose.classList.add("hamburgerCloseActive");
});

hamClose.addEventListener("click", () => {
  hamMenucontainer.style.display = "none";
  hamMenuOverlay.style.display = "none";

  hamOpen.classList.remove("hamburgerActive");
  hamClose.classList.remove("hamburgerCloseActive");
});

hamMenuOverlay.addEventListener("click", () => {
  hamMenucontainer.style.display = "none";
  hamMenuOverlay.style.display = "none";

  hamOpen.classList.remove("hamburgerActive");
  hamClose.classList.remove("hamburgerCloseActive");
});

profileBtn.addEventListener("click", () => {
  profileDropdown.classList.toggle("profileDropdownActive");
});

//Mobile Footer Accordian Buttons
const infoBtn = document.getElementById("footerInformationBtn");
const supportBtn = document.getElementById("footerSupportBtn");
const socialsBtn = document.getElementById("footerSocialsBtn");
//accordian menu toggles
const InformationMenu = document.getElementById('');
const SupportMenu = document.getElementById('');
const SocialsMenu = document.getElementById('');

infoBtn.addEventListener("click", () => {
  infoBtn.classList.toggle("footerInfoActive");
});
supportBtn.addEventListener("click", () => {
  supportBtn.classList.toggle("footerSupportActive");
});
socialsBtn.addEventListener("click", () => {
  socialsBtn.classList.toggle("footerSocialsActive");
});

//TOPBAR
document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("saleCountdownContainer");
  if (!container) return;

  const startDate = new Date(container.dataset.startDate);
  const endDate = new Date(container.dataset.endDate);
  const statusEl = document.getElementById("saleStatus");
  const timerEl = document.getElementById("saleTimer");

  function updateCountdown() {
    const now = new Date();

    if (now < startDate) {
      // before sale
      statusEl.textContent = "Sale starts in:";
      const diff = startDate - now;
      timerEl.textContent = formatTime(diff);
    } else if (now >= startDate && now <= endDate) {
      // current sale
      statusEl.textContent = "Sale ends in:";
      const diff = endDate - now;
      timerEl.textContent = formatTime(diff);
    } else {
      // after sale
      statusEl.textContent = "Sale has ended";
      timerEl.textContent = "";
      clearInterval(interval);
    }
  }

  function formatTime(ms) {
    if (ms <= 0) return "0d 0h 0m 0s";

    const totalSeconds = Math.floor(ms / 1000);
    const days = Math.floor(totalSeconds / (3600 * 24));
    const hours = Math.floor((totalSeconds % (3600 * 24)) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    // add some zeros before single digits
    const pad = (n) => String(n).padStart(2, "0");
    return `${days}d ${pad(hours)}h ${pad(minutes)}m ${pad(seconds)}s`;
  }

  updateCountdown();
  const interval = setInterval(updateCountdown, 1000);
});


const socialsContainer = document.getElementById("socialsContainer");
const socialsText = [
  '<a href="https://discord.gg/vzDV2ddt2V" target="_blank">Join Our Discord</a>',
  '<a href="https://www.tiktok.com/@frayyed.com" target="_blank">Follow Our Tiktok</a>',
  '<a href="https://www.instagram.com" target="_blank">Follow Our Instagram</a>',
];
let current = 0;
function switchSocialsText() {
  socialsContainer.style.opacity = 0;

  setTimeout(() => {
    current = (current + 1) % socialsText.length
    socialsContainer.innerHTML = socialsText[current];
    socialsContainer.style.opacity = 1;
  }, 500);
}
setInterval(switchSocialsText, 5000);
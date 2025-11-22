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
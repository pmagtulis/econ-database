// mobile menu

const burgerIcon = document.querySelector("#burger");
const navbarMenu = document.querySelector("#navbarSupportedContent");

burgerIcon.addEventListener("click", () => {
  navbarMenu.classList.toggle("is-active");
});

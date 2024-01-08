import 'bootstrap';
import "@fontsource/jetbrains-mono";
import '../css/style.scss';
import {registerSidebarHandler, registerLogoutButtons} from './utils';


document.addEventListener("DOMContentLoaded", () => {
  registerSidebarHandler();
  registerLogoutButtons();
});
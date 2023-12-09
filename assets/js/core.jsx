import '../css/core.css';
import $ from "jquery/dist/jquery.slim";


let sidebarState = localStorage.getItem('sbstate')

function logout(url, csrfToken) {
  window.localStorage.clear();
  const form = document.createElement('form');
  form.action = url;
  form.method = 'post';
  const csrfInput = document.createElement('input');
  csrfInput.type = 'hidden';
  csrfInput.name = 'csrfmiddlewaretoken';
  csrfInput.value = csrfToken;
  form.appendChild(csrfInput);
  document.body.appendChild(form);
  form.submit();
}

function saveStateSidebar() {

}

$(document).ready(function () {
  console.log("dom ready");
  let state = localStorage.getItem('sbstate') ? localStorage.setItem('sbstate', 'show') : 'show';

  const nav_term_btn = document.getElementById('nav-term-btn');
  nav_term_btn.on('click', function (e) {

  })
});
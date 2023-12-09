import '../css/core.css';
import $ from "jquery/dist/jquery.slim";

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


function sidebarStateHandler() {
  let sbshow = localStorage.getItem('sb.show');
  let hasshow = $("#sidebar").hasClass('show')
  // Check if 'sbshow' is not set
  if (sbshow === null) {
    // Set 'sbshow' based on the class of #sidebar
    localStorage.setItem('sb.show', hasshow);
  }
  // Check the value of sbshow and update #sidebar accordingly
  if ((sbshow === 'true') && !hasshow) {
    $('#sidebar').addClass('show');
  } else if ((sbshow === 'false') && sbshow) {
    $('#sidebar').removeClass('show');
  }
  // When sidebar button is clicked
  $("#nav-sb-btn").on('click', function (e) {
    let prevSbState = JSON.parse(localStorage.getItem('sb.show'));
    // noinspection JSCheckFunctionSignatures
    localStorage.setItem('sb.show', !prevSbState)
  })
}

function termElemStateHandler() {
  let termshow = localStorage.getItem('term.show');
  let thasshow = $("#terminal-container").hasClass('show')
  // Check if 'sbshow' is not set
  if (termshow === null) {
    // Set 'sbshow' based on the class of #sidebar
    localStorage.setItem('term.show', thasshow);
  }
  // Check the value of sbshow and update #sidebar accordingly
  if ((termshow === 'true') && !thasshow) {
    $('#terminal-container').addClass('show');
  } else if ((termshow === 'false') && termshow) {
    $('#terminal-container').removeClass('show');
  }
  // When sidebar button is clicked
  $("#nav-term-btn").on('click', function (e) {
    let prevTermState = JSON.parse(localStorage.getItem('term.show'));
    // noinspection JSCheckFunctionSignatures
    localStorage.setItem('term.show', !prevTermState)
  })
}

$(document).ready(function() {
  sidebarStateHandler();
  termElemStateHandler();
});
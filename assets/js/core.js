import Cookies from "js-cookie";
import $ from "jquery";

$(".logout-func-btn").click(function () {
  localStorage.clear();
  const form = document.createElement('form');
  form.action = 'accounts/logout/';
  form.method = 'post';
  const csrfInput = document.createElement('input');
  csrfInput.type = 'hidden';
  csrfInput.name = 'csrfmiddlewaretoken';
  csrfInput.value = Cookies.get('csrftoken');
  form.appendChild(csrfInput);
  document.body.appendChild(form);
  form.submit();
});

async function sidebarStateHandler() {
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
  $("#nav-sb-btn").on('click', function () {
    let prevSbState = JSON.parse(localStorage.getItem('sb.show'));
    // noinspection JSCheckFunctionSignatures
    localStorage.setItem('sb.show', !prevSbState)
  })
}

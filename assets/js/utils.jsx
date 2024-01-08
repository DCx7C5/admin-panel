import Cookies from "js-cookie";


export function getLocalStorage(value, def=null) {
  let item= localStorage.getItem(value);
  if ((item === null) && def !== null ) {
    item = def
    localStorage.setItem(value, item)
  }
  return item
}


export function getCookie(name) {
    const dc = document.cookie;
    const prefix = name + "=";
    let begin = dc.indexOf("; " + prefix);
    if (begin === -1) {
      begin = dc.indexOf(prefix);
      if (begin !== 0) return null;
    } else {
      begin += 2;
      var end = document.cookie.indexOf(";", begin);
      if (end === -1) {
        end = dc.length;
      }
    }
    return decodeURI(dc.substring(begin + prefix.length, end));
}


export function registerLogoutButtons() {
  const elems = document.getElementsByClassName('logout-func-btn');
  for (const elem of elems) {
    elem.addEventListener('click', async () => {
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
    })
  }
}

export function registerSidebarHandler() {
  const btn = document.getElementById('nav-sb-btn');
  const sb = document.getElementById('sidebar-wrapper');
  let hasshow = sb.classList.contains('show');
  let sbshow = localStorage.getItem('sb.show');
  if (sbshow === null) {
    localStorage.setItem('sb.show', hasshow.toString());
  }
  if ((sbshow === 'true') && !hasshow) {
    sb.classList.add('show');
  } else if ((sbshow === 'false') && hasshow) {
    sb.classList.remove('show');
  }
  btn.addEventListener('click', function () {
    let prevSbState = JSON.parse(localStorage.getItem('sb.show'));
    localStorage.setItem('sb.show', !prevSbState)
  })
}

export function setLocalStorageDefaults(dict) {
  for (const [key, value] of Object.entries(dict)) {
    const item = localStorage.getItem(key)
    item === null && localStorage.setItem(key, JSON.stringify(value))
  }
}


export const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

function decline_challenge(elem, sent_user_id, base_url) {
  const csrftoken = getCookie("csrftoken");
  const f_body = {
    sent_user_id: sent_user_id,
  };
  let response = fetch(`${base_url}/decline-challenge-api`, {
    method: "POST",
    headers: {
      // Добавляем необходимые заголовки
      "Content-type": "application/json; charset=UTF-8",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(f_body), // Тело запроса в JSON-формате
  })
    .then((response) => {
      if (response.ok) {
        elem.parentElement.parentElement.parentElement.parentElement.remove();
      } else {
        throw new Error("Bad Status");
      }
    })
    .catch((error) => {
      let exist = document.querySelector(".message");
      if (exist) {
        exist.remove();
      }
      let el = document.createElement("div");
      if (typeof el.innerText !== "undefined") {
        // IE8-
        el.innerText = "что-то пошло не так";
      } else {
        // Нормальные браузеры
        el.createTextNode("что-то пошло не так");
      }
      el.classList.add("message");
      el.classList.add("activated-mes");
      el.classList.add("red-mes");
      el.style.display = "block";
      let sp = document.createElement("span");
      sp.innerText = "×";
      sp.setAttribute("class", "closebtn");
      sp.setAttribute("onclick", "close_message()");
      el.append(sp);
      document.body.append(el);
    });
}
function decline_my_challenge(elem, recieved_user_id) {
  const csrftoken = getCookie("csrftoken");
  const f_body = {
    recieved_user_id: recieved_user_id,
  };
  let response = fetch("http://127.0.0.1:8000/decline-my-challenge-api", {
    method: "POST",
    headers: {
      // Добавляем необходимые заголовки
      "Content-type": "application/json; charset=UTF-8",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(f_body), // Тело запроса в JSON-формате
    mode: "same-origin",
  })
    .then((response) => {
      if (response.ok) {
        elem.parentElement.parentElement.parentElement.parentElement.remove();
      } else {
        throw new Error("Bad Status");
      }
    })
    .catch((error) => {
      let exist = document.querySelector(".message");
      if (exist) {
        exist.remove();
      }
      let el = document.createElement("div");
      if (typeof el.innerText !== "undefined") {
        // IE8-
        el.innerText = "что-то пошло не так";
      } else {
        // Нормальные браузеры
        el.createTextNode("что-то пошло не так");
      }
      el.classList.add("message");
      el.classList.add("activated-mes");
      el.classList.add("red-mes");
      el.style.display = "block";
      let sp = document.createElement("span");
      sp.innerText = "×";
      sp.setAttribute("class", "closebtn");
      sp.setAttribute("onclick", "close_message()");
      el.append(sp);
      document.body.append(el);
    });
}

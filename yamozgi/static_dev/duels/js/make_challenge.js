function challenge(from, to) {
  let to_user = to;
  let from_user = from;
  const csrftoken = getCookie("csrftoken");
  const f_body = {
    to_user: to_user,
    from_user: from_user,
  };
  let response = fetch("http://127.0.0.1:8000/challenge-api", {
    method: "POST",
    headers: {
      // Добавляем необходимые заголовки
      "Content-type": "application/json; charset=UTF-8",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(f_body), // Тело запроса в JSON-формате
    mode: "same-origin",
  })
    .then((response) => response.json())
    .then((data) => {
      let message = data["messages"];
      let exist = document.querySelector('.message')
      if (exist){
        exist.remove()
      }
      let el = document.createElement("div");
      if (typeof el.innerText !== "undefined") {
        // IE8-
        el.innerText = message;
      } else {
        // Нормальные браузеры
        el.createTextNode(message);

      }
      el.classList.add('message')
      el.classList.add('activated-mes')
      el.style.display = 'block';
      let sp = document.createElement('span')
      sp.innerText = '×'
      sp.setAttribute('class' , 'closebtn')
      sp.setAttribute('onclick', 'close_message()')
      el.append(sp)
      document.body.append(el)
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

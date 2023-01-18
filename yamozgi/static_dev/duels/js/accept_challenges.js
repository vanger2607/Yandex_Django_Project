function accept_challenge(
  elem,
  sent_user_login,
  sent_user_id,
  sent_user_avatar,
  base_url
) {
  const csrftoken = getCookie("csrftoken");
  const f_body = {
    sent_user_id: sent_user_id,
  };
  let response = fetch(`${base_url}/accept-challenge-api`, {
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
        return response.json();
      } else {
        throw new Error("Bad Status");
      }
    })
    .then((data) => {
      //elem.parentElement.parentElement.parentElement.parentElement.remove();
      const currents_battle_body = document
        .querySelector(".current-battles__battle-container")
        .lastElementChild.querySelectorAll(".current-battles__column");
      console.log(currents_battle_body.length);
      new_elem = document.createElement("div");
      new_elem.className = "current-battles__column";
      console.log(new_elem);
      new_item = document.createElement("div");
      new_item.className = "current-battles__item battle-item";
      console.log(new_item);
      new_pic = document.createElement("div");
      new_pic.className = "battle-item__pic";

      if (sent_user_avatar == "/media/null") {
        new_img = document.createElement("div");
        new_img.className = "battle-none-photo";
      } else {
        new_img = document.createElement("img");
        new_img.className = "battle-item__photo";
        new_img.setAttribute("src", sent_user_avatar);
      }
      console.log(new_img);
      new_item_info = document.createElement("div");
      new_item_info.className = "battle-item__info battle-info";
      new_item_title = document.createElement("div");
      new_item_title.className = "battle-info__title";
      if (typeof new_item_title.innerText !== "undefined") {
        // IE8-
        new_item_title.innerText = sent_user_login;
      } else {
        // Нормальные браузеры
        new_item_title.textContent = sent_user_login;
      }
      console.log(new_item_title);
      new_item_text = document.createElement("div");
      new_item_text.className = "battle-info__text";
      if (typeof new_item_text.innerText !== "undefined") {
        // IE8-
        new_item_text.innerText = "Раунд 0";
      } else {
        // Нормальные браузеры
        new_item_text.textContent = "Раунд 0";
      }
      console.log(new_item_text);
      new_item_button = document.createElement("div");
      new_item_button.className = "battle-info__button";
      const battle_url = data["battle_url"];

      console.log(battle_url);
      new_item_a = document.createElement("a");
      new_item_a.setAttribute("href", battle_url);
      new_item_a.setAttribute("class", "battle-button mini-button");
      if (typeof new_item_text.innerText !== "undefined") {
        // IE8-
        new_item_a.innerText = "перейти";
      } else {
        // Нормальные браузеры
        new_item_a.textContent = "перейти";
      }
      new_item_button.appendChild(new_item_a);
      new_item_info.appendChild(new_item_title);
      new_item_info.appendChild(new_item_text);
      new_item_info.appendChild(new_item_button);
      new_pic.appendChild(new_img);
      new_item.appendChild(new_pic);
      new_item.appendChild(new_item_info);
      new_column = document.createElement("div");
      new_column.className = "current-battles__column";
      new_column.appendChild(new_item);
      if (currents_battle_body.length < 3) {
        document
          .querySelector(".current-battles__battle-container")
          .lastElementChild.appendChild(new_column);
      } else {
        new_row = document.createElement("div");
        new_row.className = "current-battles__body";
        new_row.appendChild(new_column);
        document
          .querySelector(".current-battles__battle-container")
          .appendChild(new_row);
      }
      elem.parentElement.parentElement.parentElement.parentElement.remove();
      let exist = document.querySelector(".message");
      if (exist) {
        exist.remove();
      }
      let el = document.createElement("div");
      if (typeof el.innerText !== "undefined") {
        // IE8-
        el.innerText = "Вызов принят, и появился в текущах играх";
      } else {
        // Нормальные браузеры
        el.createTextNode("Вызов принят, и появился в текущах играх");
      }
      el.classList.add("message");
      el.classList.add("activated-mes");
      el.style.display = "block";
      let sp = document.createElement("span");
      sp.innerText = "×";
      sp.setAttribute("class", "closebtn");
      sp.setAttribute("onclick", "close_message()");
      el.append(sp);
      document.body.append(el);
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

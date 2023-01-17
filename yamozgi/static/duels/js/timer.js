function timer(base_url, question_id, round_id, pos, battle, round_now) {
  const lineSpecial = document.body.querySelector(".line__special");
  let widthBlock = lineSpecial.clientWidth;
  if (widthBlock !== 0) {
    setInterval(function () {
      lineSpecial.style.width = [(widthBlock -= 2)] + "px";
    }, 165);
    setTimeout(function () {
      clearInterval,
      end_get_answer(base_url, question_id, round_id, pos, battle, round_now);
    }, widthBlock * 82.5);
  }
}
function end_get_answer(base_url, question_id, round_id, pos, battle, round_now) {
  const csrftoken = getCookie('csrftoken');
  const check = {
    question_id: question_id,
    round_id: round_id,
    question_now: pos,
    battle_now: battle,
    round_now: round_now
  };
  let response = fetch(`${base_url}/question_api_endtime`,{
            method: 'POST',
            headers: {
              // Добавляем необходимые заголовки
              'Content-type': 'application/json; charset=UTF-8',
              'X-CSRFToken': csrftoken},
              body: JSON.stringify(check), // Тело запроса в JSON-формате
            })
            .then((response) => {if (response.ok) {return response.json()}
                        else{
      throw new Error("Bad Status");}})
    .then((data) => {
      window.location.replace(data["question_url"]);
    })
    .catch((error) => {
      let exist = document.querySelector('.message')
      if (exist){
        exist.remove()
      }
      let el = document.createElement("div");
      if (typeof el.innerText !== "undefined") {
        // IE8-
        el.innerText = "что-то пошло не так";
      } else {
        // Нормальные браузеры
        el.createTextNode("что-то пошло не так");

      }
      el.classList.add('message')
      el.classList.add('activated-mes')
      el.classList.add('red-mes')
      el.style.display = 'block';
      let sp = document.createElement('span')
      sp.innerText = '×'
      sp.setAttribute('class' , 'closebtn')
      sp.setAttribute('onclick', 'close_message()')
      el.append(sp)
      document.body.append(el)
    });
}

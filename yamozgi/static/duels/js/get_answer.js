

function is_right(el, question_id, player_choice, round_id, pos,battle, round_now, base_url) {
        
    const csrftoken = getCookie('csrftoken');
            answer = el.textContent;
            const check ={
                userr_answer: answer,
                question_id: question_id,
                player_choice: player_choice,
                round_id: round_id,
                question_now: pos,
                battle_now: battle,
                round_now: round_now
              };
            let response = fetch(`${base_url}/question-api`,{
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
    });}

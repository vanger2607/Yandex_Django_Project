

function is_right(el, question_id) {
        
    const csrftoken = getCookie('csrftoken');
            answer = el.textContent;
            alert(question_id);
            const check ={
                userr_answer: answer,
                question_id: question_id,
              };
            let  body1 = JSON.stringify(check);
            alert(body1);
            let response = fetch('http://127.0.0.1:8000/challenge-api',{
            method: 'POST',
            headers: {
              // Добавляем необходимые заголовки
              'Content-type': 'application/json; charset=UTF-8',
              'X-CSRFToken': csrftoken},
              body: JSON.stringify(check), // Тело запроса в JSON-формате
            mode: 'same-origin'
            },)
            if (response.ok) { // если HTTP-статус в диапазоне 200-299
                // получаем тело ответа (см. про этот метод ниже)
                alert('верно')
              } else {
                alert("Ошибка HTTP: " + response.status);
              }
          }

document.getElementById('findRandomBattle').addEventListener('click', function() {
  const button = this;
  const loading = document.getElementById('loadingSpinner');
  button.disabled = true;  // Блокируем кнопку во время поиска
  loading.style.display = 'block';  // Показываем спиннер

  // Шаг 1: AJAX-запрос на find_battle для добавления в Redis
  fetch(`/battles/find_battle`, {  
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')  
    },
    body: JSON.stringify({})  
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'searching') {
      // Шаг 2: Запускаем polling для проверки матча
      const pollInterval = setInterval(() => {
        fetch('/battles/check_match')  // GET-запрос на статус
          .then(res => res.json())
          .then(matchData => {
            if (matchData.matched) {
              clearInterval(pollInterval);  // Останавливаем polling
              loading.style.display = 'none';
              button.disabled = false;
              window.location.href = `/battles/${matchData.battle_id}`;  // Redirect с ID битвы
            }
          })
          .catch(error => {
            console.error('Polling error:', error);
            clearInterval(pollInterval);
            loading.style.display = 'none';
            button.disabled = false;
            alert('Ошибка поиска. Попробуйте снова.');
          });
      }, 5000);  // Проверяем каждые 5 секунд
    }
  })
  .catch(error => {
    console.error('Find battle error:', error);
    loading.style.display = 'none';
    button.disabled = false;
    alert('Ошибка запуска поиска.');
  });
});


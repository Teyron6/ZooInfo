// search.js (For the search result page)
document.addEventListener('DOMContentLoaded', function() {
  const urlParams = new URLSearchParams(window.location.search);
  const query = urlParams.get('query');

  if (query) {
      // Здесь вы можете использовать значение query для поиска информации о животном
      // и заполнения страницы результатами
      fetchAnimalData(query);
  }
});

function fetchAnimalData(animalName) {
  // Пример данных (замените на реальный запрос к вашему источнику данных)
  const animals = {
      "лев": {
          name: "Лев",
          description: "Лев — вид хищных млекопитающих, один из пяти представителей рода пантер, относящегося к подсемейству больших кошек в составе семейства кошачьих."
      },
      "тигр": {
          name: "Тигр",
          description: "Тигр — вид хищных млекопитающих семейства кошачьих, один из пяти представителей рода пантера, который относится к подсемейству больших кошек."
      },
      "жираф": {
          name: "Жираф",
          description: "Жираф — вид африканских млекопитающих из отряда парнокопытных, семейства жирафовых. Самое высокое наземное животное планеты."
      }
  };

  const animal = animals[animalName.toLowerCase()];
  if (animal) {
      document.getElementById('animal-name').textContent = animal.name;
      document.getElementById('animal-description').textContent = animal.description;
  } else {
      document.getElementById('animal-name').textContent = "Не найдено";
      document.getElementById('animal-description').textContent = "Информация о животном не найдена.";
  }
}
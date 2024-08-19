function resizeImage(width) {
  const images = document.querySelectorAll('.img-resize');

  images.forEach((img) => {
    img.style.width = width + 'px';
  });

  // не всегда срабатывается вовремя при прокрутке рейнджа, поэтому сделано c setTimeout.
  // логика для того, чтобы отображать картинку по центру если она меньше центрального блока,
  // и отображать ее полностью, если она больше.
  // без этой логики левая часть картинки обрезается
  setTimeout(() => {
    const contentCenter = document.querySelector('.content-center');
    const contentCenterWidth = contentCenter.offsetWidth;
    const contentCenterImages = document.querySelectorAll(
      '.content-center > div'
    );
    const maxImageWidth = Math.max(
      ...Array.from(contentCenterImages).map((el) => el.offsetWidth)
    );
    if (contentCenterWidth < maxImageWidth) {
      contentCenter.classList.add('alignStart');
      contentCenter.classList.remove('alignCenter');
    } else {
      contentCenter.classList.add('alignCenter');
      contentCenter.classList.remove('alignStart');
    }
  }, 100);
}

// Переменные для состояния чекбоксов
let checkboxes = localStorage.getItem('checkboxes')
  ? formatStorageCheckboxes(localStorage.getItem('checkboxes'))
  : Array.from({ length: 30 }, () => [false, false]);

function formatStorageCheckboxes(checkboxes) {
  const copiedCheckboxes = JSON.parse(JSON.stringify(checkboxes));
  const arr = copiedCheckboxes.split(',');
  const resultArr = [];
  for (let i = 0; i < arr.length; i += 2) {
    resultArr.push([
      arr[i].toLowerCase() === 'true',
      arr[i + 1].toLowerCase() === 'true',
    ]);
  }

  return resultArr;
}

// задаем стили кнопок и состояния чекбоксов
function initializeCheckboxes() {
  checkboxes.forEach((checkbox, index) => {
    const checkbox1 = document.getElementById(`checkbox${index + 1}_1`);
    checkbox1.checked = checkbox[0];
    const checkbox2 = document.getElementById(`checkbox${index + 1}_2`);
    checkbox2.checked = checkbox[1];
    updateCheckboxes(checkbox1, index);
    updateCheckboxes(checkbox2, index);

    // дополнительно навешиваем стили кнопки лайк, т.к. в предыдущей функции
    // они стираются классом button-inactive
    if (checkbox1.checked) {
      updateParticipantButtonStyles(index + 1, 'button-like');
    }
    updateCountLeft();
  });
}

function handleCheckboxChange(checkbox) {
  const index = parseInt(checkbox.id.match(/\d+/)[0]) - 1;

  updateCheckboxes(checkbox, index);
  updateCount();
  updateCountLeft();
}

function updateCheckboxes(checkbox, index) {
  const isLikeButton = checkbox.id.endsWith('1');
  const isChecked = checkbox.checked;
  const likeCheckbox = document.querySelector(
    `#${checkbox.id.slice(0, checkbox.id.length - 2)}_1`
  );
  const dislikeCheckbox = document.querySelector(
    `#${checkbox.id.slice(0, checkbox.id.length - 2)}_2`
  );
  const likeLabel = document.querySelector(
    `label[for="${checkbox.id.slice(0, checkbox.id.length - 2)}_1"]`
  );
  const dislikeLabel = document.querySelector(
    `label[for="${checkbox.id.slice(0, checkbox.id.length - 2)}_2"]`
  );

  // логика для того, чтобы убрать чек лайка, если поставлен дислайк, и наоборот
  if (isLikeButton && isChecked) {
    likeLabel.classList.add('checked');
    dislikeLabel.classList.remove('checked_red');
    dislikeCheckbox.checked = false;
    checkboxes[index][0] = true;
    checkboxes[index][1] = false;
    // изменяем стили соответсвующей кнопки
    updateParticipantButtonStyles(index + 1, 'button-like');
  }
  if (isLikeButton && !isChecked) {
    likeLabel.classList.remove('checked');
    checkboxes[index][0] = false;
    updateParticipantButtonStyles(index + 1, 'button-inactive');
  }
  if (!isLikeButton && isChecked) {
    dislikeLabel.classList.add('checked_red');
    likeLabel.classList.remove('checked');
    likeCheckbox.checked = false;
    checkboxes[index][0] = false;
    checkboxes[index][1] = true;
    updateParticipantButtonStyles(index + 1, 'button-dislike');
  }
  if (!isLikeButton && !isChecked) {
    dislikeLabel.classList.remove('checked_red');
    checkboxes[index][1] = false;
    updateParticipantButtonStyles(index + 1, 'button-inactive');
  }

  localStorage.setItem('checkboxes', checkboxes);
}

function updateParticipantButtonStyles(index, className) {
  const classList = ['button-inactive', 'button-like', 'button-dislike'];
  const participantButton = document.querySelector(`#participant${index}`);
  participantButton.classList.add(className);
  const classesToRemove = classList.filter((cl) => cl !== className);
  classesToRemove.forEach((cl) => {
    participantButton.classList.remove(cl);
  });
}

function updateCount() {
  let count = countTrue(checkboxes);
  document.getElementById('count').innerText = `${count}/15`;
  updateButtonState();
}

function updateButtonState() {
  const button = document.getElementById('btn-end-vote');
  let count = document.getElementById('count').innerText;
  let remainCount = document.getElementById('span-left').innerText;
  if (count === '15/15' && remainCount === '0') {
    button.disabled = false; // Активируем кнопку
    button.title = ''; // Убираем подсказку, когда кнопка активна
  } else {
    button.disabled = true; // Деактивируем кнопку
    button.title = 'Необходимо 15 положительных и 15 отрицательных голосов'; // Устанавливаем подсказку
  }
}

// логика для кнопки завершения голосования
document.getElementById('btn-end-vote').addEventListener('click', function (e) {
  let count = document.getElementById('count').innerText;
  if (count !== '15/15' || e.target.textContent === 'Оценка завершена') {
    return;
  }
  e.target.textContent = 'Оценка завершена'; // Изменяем текст при отправке ответов
  e.target.disabled = true;
  e.target.style.opacity = '0.5'; // Изменяем текст при отправке ответов

  // модалка
  const successModal = document.querySelector('.success-modal');
  const endVoteClose = document.querySelector('.success-modal-close');

  successModal.classList.add('success-modal-opened');

  endVoteClose.onclick = function () {
    successModal.classList.remove('success-modal-opened');
  };

  window.onclick = function (event) {
    if (event.target == successModal) {
      successModal.classList.remove('success-modal-opened');
    }
  };
});

// логика для скрытия и открытия левой панели
const contentRight = document.querySelector('.content-right');
const contentRightButton = document.querySelector('.content-right-toggle');
const contentRightTriangle = document.querySelector(
  '.content-right-triangle-right'
);
const contentLeftInside = document.querySelectorAll('.content-left-inside');
const contentCenter = document.querySelector('.content-center');
contentRightButton.addEventListener('click', () => {
  contentRight.classList.toggle('content-right-invisible');
  contentCenter.classList.toggle('content-center-extended');

  if (Array.from(contentRight.classList).includes('content-right-invisible')) {
    contentRightTriangle.classList.add('content-right-triangle-left');
    contentRightTriangle.classList.remove('content-right-triangle-right');
  } else {
    contentRightTriangle.classList.add('content-right-triangle-right');
    contentRightTriangle.classList.remove('content-right-triangle-left');
  }
});

// Функция для подсчета количества true
function countTrue(checkboxes) {
  let count = 0;
  checkboxes.forEach((pair) => {
    if (pair[0] === true) {
      count++;
    }
  });
  return count;
}

function updateCountLeft() {
  let countLeft = countAll(checkboxes);
  document.getElementById('span-left').innerText = `${30 - countLeft}`;
  updateButtonState();
}

function countAll(checkboxes) {
  let count = 0;
  checkboxes.forEach((pair) => {
    if (pair[0] === true || pair[1] === true) {
      count++;
    }
  });
  return count;
}

function showContent(buttonId) {
  let num = buttonId.replace(/[^0-9]/g, '');
  document.querySelectorAll('.content-section').forEach((section) => {
    section.style.display = 'none';
  });
  document.getElementById(`content${num}`).style.display = 'block';
  document.getElementById('participant-image').src = part_images[buttonId];
  document.getElementById('part-name').textContent = participants[num - 1];
}

function highlightButton(buttonId) {
  const buttons = document.querySelectorAll('button[id^="participant"]');
  buttons.forEach((button) => {
    if (button.id === buttonId) {
      button.classList.add('participantButton-highlighted');
    } else {
      button.classList.remove('participantButton-highlighted');
    }
  });
}

function showParticipantInformation(participant) {
  const chosenParticipant = participantsInfo[participant];
  const participantName = document.querySelector('.participant-name');
  const participantInformation = document.querySelector(
    '.participant-information'
  );

  participantName.textContent = participant;
  participantInformation.textContent = chosenParticipant['information'];
}

const participants = [
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
  'participant',
];

const participantsInfo = {
  participant: {
    information: 'position',
  },
};

function createMenuItems() {
  let sidebar = document.getElementById('left-sidebar');
  participants.forEach(function (participant, index) {
    let newItem = document.createElement('div');
    newItem.className = 'menu-item';

    let newButton = document.createElement('button');
    newButton.className = 'btn btn-light btn-custom button-inactive';
    newButton.textContent = participant;
    newButton.id = 'participant' + (index + 1);
    newButton.onclick = function () {
      highlightButton(newButton.id);
      showParticipantInformation(participant);
      showContent(newButton.id);
    };
    newItem.appendChild(newButton);

    //   <!-- Создание блока с сердцем -->
    let newForm = document.createElement('div');
    newForm.className = 'form-check';
    // newButton.appendChild(newForm);
    newItem.appendChild(newForm);

    let newInput = document.createElement('input');
    newInput.className = 'form-check-input';
    newInput.type = 'checkbox';
    newInput.id = 'checkbox' + (index + 1) + '_1';
    newInput.onchange = function () {
      handleCheckboxChange(newInput);
    };
    newForm.appendChild(newInput);

    let newLabel = document.createElement('label');
    newLabel.className = 'form-check-label';
    newLabel.htmlFor = 'checkbox' + (index + 1) + '_1';
    newForm.appendChild(newLabel);

    let newI = document.createElement('i');
    newI.className = 'fas fa-heart';
    newLabel.appendChild(newI);

    // <!-- Создание блока с крестом -->
    let newForm2 = document.createElement('div');
    newForm2.className = 'form-check';
    // newButton.appendChild(newForm2);
    newItem.appendChild(newForm2);

    let newInput2 = document.createElement('input');
    newInput2.className = 'form-check-input';
    newInput2.type = 'checkbox';
    newInput2.id = 'checkbox' + (index + 1) + '_2';
    newInput2.onchange = function () {
      handleCheckboxChange(newInput2);
    };
    newForm2.appendChild(newInput2);

    let newLabel2 = document.createElement('label');
    newLabel2.className = 'form-check-label form-check-label-dislike';
    newLabel2.htmlFor = 'checkbox' + (index + 1) + '_2';
    newForm2.appendChild(newLabel2);

    let newI2 = document.createElement('i');
    newI2.className = 'fas fa-times-circle';
    newLabel2.appendChild(newI2);

    sidebar.appendChild(newItem);

    // задаем источники картинок в зависимости от имени участника
    const participantImage = document.querySelector(
      `#content${index + 1} > img`
    );
    participantImage.src = 'test.jpg';
    participantImage.style.width = '1000px';
  });
}

// скрытие и показ слайдера увеличения документа
const documentRangeTriangle = document.querySelector(
  '.document-range-triangle-down'
);
const formRange = document.querySelector('.form-range');
documentRangeTriangle.addEventListener('click', () => {
  formRange.classList.toggle('form-range-invisible');
  if (
    Array.from(documentRangeTriangle.classList).includes(
      'document-range-triangle-down'
    )
  ) {
    documentRangeTriangle.classList.remove('document-range-triangle-down');
    documentRangeTriangle.classList.add('document-range-triangle-up');
    contentCenter.style.height = '95%';
  } else {
    documentRangeTriangle.classList.remove('document-range-triangle-up');
    documentRangeTriangle.classList.add('document-range-triangle-down');
    contentCenter.style.height = '90%';
  }
});

///////////////////

createMenuItems();

document.addEventListener('DOMContentLoaded', (event) => {
  initializeCheckboxes(); // Устанавливаем состояние чекбоксов при загрузке страницы
  updateCount(); // Устанавливаем счетчик
  showContent('content0'); // Показываем инструкцию по умолчанию
});

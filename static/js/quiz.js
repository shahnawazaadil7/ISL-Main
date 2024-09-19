const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
const handSigns = {
  'A': 'images/A.jpg',
  'B': 'images/B.jpg',
  'C': 'images/C.jpg',
  'D': 'images/D.jpg',
  'E': 'images/E.jpg',
  'F': 'images/F.jpg',
  'G': 'images/G.jpg',
  'H': 'images/H.jpg',
  'I': 'images/I.jpg',
  'J': 'images/J.jpg',
  'K': 'images/K.jpg',
  'L': 'images/L.jpg',
  'M': 'images/M.jpg',
  'N': 'images/N.jpg',
  'O': 'images/O.jpg',
  'P': 'images/P.jpg',
  'Q': 'images/Q.jpg',
  'R': 'images/R.jpg',
  'S': 'images/S.jpg',
  'T': 'images/T.jpg',
  'U': 'images/U.jpg',
  'V': 'images/V.jpg',
  'W': 'images/W.jpg',
  'X': 'images/X.jpg',
  'Y': 'images/Y.jpg',
  'Z': 'images/Z.jpg'
};

let currentQuizLevel = 1;

function showSection(section) {
    document.getElementById('quizzes-section').style.display = 'none';
    if (section === 'quizzes') {
        document.getElementById('quizzes-section').style.display = 'block';
        generateQuizLevels();
    }
}

function generateQuizLevels() {
    const quizLevelsContainer = document.getElementById('quiz-levels');
    quizLevelsContainer.innerHTML = '';
    alphabet.forEach((letter, index) => {
        quizLevelsContainer.innerHTML += `<button onclick="startQuiz(${index + 1})">Level ${index + 1} (${letter})</button>`;
    });
}

function startQuiz(level) {
    currentQuizLevel = level;
    document.getElementById('quiz-content').style.display = 'block';
    const letter = alphabet[level - 1];
    const handSignImage = handSigns[letter];
    
    document.getElementById('quiz-question').innerHTML = `<img src="${handSignImage}" alt="Hand sign for ${letter}">`;
    
    const options = generateOptions(letter);
    document.getElementById('quiz-options').innerHTML = options.map(option => `<button onclick="checkAnswer('${option}', '${letter}')">${option}</button>`).join('');
    
    document.getElementById('next-level').style.display = 'none';
    document.getElementById('message').style.display = 'none';
}

function generateOptions(correctLetter) {
    const options = [correctLetter];
    while (options.length < 4) {
        const randomLetter = alphabet[Math.floor(Math.random() * alphabet.length)];
        if (!options.includes(randomLetter)) {
            options.push(randomLetter);
        }
    }
    return options.sort(() => Math.random() - 0.5);
}

function checkAnswer(selectedLetter, correctLetter) {
    const messageDiv = document.getElementById('message');
    if (selectedLetter === correctLetter) {
        messageDiv.textContent = 'Correct!';
        messageDiv.style.color = '#32cd32'; // Green
    } else {
        messageDiv.textContent = 'Wrong!';
        messageDiv.style.color = '#ff4500'; // Red
    }
    messageDiv.style.display = 'block';
    if (currentQuizLevel < 26) {
        document.getElementById('next-level').style.display = 'block';
    } else {
        messageDiv.textContent = 'Congratulations! You have completed all levels.';
        messageDiv.style.color = '#1e90ff'; // Blue
    }
}

function goToNextLevel() {
    startQuiz(currentQuizLevel + 1);
}
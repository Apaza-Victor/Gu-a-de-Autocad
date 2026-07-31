/* =========================================================
   AutoCAD Guía — quiz.js
   Autoevaluación por nivel: opciones clickeables, feedback
   inmediato, puntuación y botón para reintentar.
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {
  initQuiz();
});

function initQuiz(){
  document.querySelectorAll('.quiz[data-quiz]').forEach(quiz => {
    const questions = quiz.querySelectorAll('.quiz-q');
    if (!questions.length) return;

    const scoreEl = document.createElement('p');
    scoreEl.className = 'quiz-score';
    quiz.appendChild(scoreEl);

    const resetBtn = document.createElement('button');
    resetBtn.className = 'quiz-reset';
    resetBtn.type = 'button';
    resetBtn.innerHTML = '<i class="bi bi-arrow-counterclockwise"></i> Reintentar';
    quiz.appendChild(resetBtn);

    let answered = 0;
    let correct = 0;

    function updateScore(){
      scoreEl.textContent = 'Puntuación: ' + correct + ' de ' + answered +
        ' · ' + (answered ? Math.round((correct / answered) * 100) : 0) + '%';
    }
    updateScore();

    questions.forEach(q => {
      const answerKey = q.getAttribute('data-answer') || 'A';
      const feedbackEl = q.querySelector('.quiz-feedback');
      const opts = q.querySelectorAll('.quiz-opt');
      const letters = ['A', 'B', 'C', 'D'];

      opts.forEach(opt => {
        opt.addEventListener('click', () => {
          if (opt.disabled) return;
          const key = opt.getAttribute('data-key') || letters[Array.prototype.indexOf.call(opts, opt)];
          const isCorrect = key === answerKey;

          opts.forEach(o => {
            o.disabled = true;
            o.classList.remove('correct', 'wrong');
            const oKey = o.getAttribute('data-key') || letters[Array.prototype.indexOf.call(opts, o)];
            if (oKey === answerKey) o.classList.add('correct');
            else if (o === opt) o.classList.add('wrong');
          });

          answered++;
          if (isCorrect) correct++;

          if (feedbackEl) {
            feedbackEl.classList.add('show', isCorrect ? 'ok' : 'bad');
          }
          updateScore();
        });
      });
    });

    resetBtn.addEventListener('click', () => {
      answered = 0;
      correct = 0;
      questions.forEach(q => {
        q.querySelectorAll('.quiz-opt').forEach(o => {
          o.disabled = false;
          o.classList.remove('correct', 'wrong');
        });
        const f = q.querySelector('.quiz-feedback');
        if (f) f.classList.remove('show', 'ok', 'bad');
      });
      updateScore();
    });
  });
}

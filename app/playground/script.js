// script.js
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    const openModalBtn = document.getElementById('openModalBtn');
    const closeModalBtn = document.querySelector('.close-btn');
    const submitBtn = document.getElementById('submitBtn');
    const numberInput = document.getElementById('numberInput');
    const message = document.getElementById('message');

    openModalBtn.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    closeModalBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        resetModal();
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
            resetModal();
        }
    });

    submitBtn.addEventListener('click', () => {
        const value = numberInput.value;
        if (value === '') {
            displayMessage('Please enter a number.', 'error');
        } else if (isNaN(value)) {
            displayMessage('Invalid input. Please enter a valid number.', 'error');
        } else {
            displayMessage(`You entered: ${value}`, 'info');
        }
    });

    function displayMessage(msg, type) {
        message.textContent = msg;
        message.className = `message ${type}`;
        message.style.display = 'block';
    }

    function resetModal() {
        numberInput.value = '';
        message.style.display = 'none';
    }
});

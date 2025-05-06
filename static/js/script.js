
const dealBtn = document.getElementById('deal-btn')
const hitBtn = document.getElementById('hit-btn')
const standBtn = document.getElementById('stand-btn')
const doubleBtn = document.getElementById('double-btn')
const splitBtn = document.getElementById('split-btn')

dealBtn.addEventListener('click', () => handleAction('deal'));
hitBtn.addEventListener('click', () => handleAction('hit'));
standBtn.addEventListener('click', () => handleAction('stand'));
doubleBtn.addEventListener('click', () => handleAction('double'));
splitBtn.addEventListener('click', () => handleAction('split'));

hitBtn.disabled = true;
standBtn.disabled = true;
doubleBtn.disabled = true;
splitBtn.disabled = true;


async function handleAction(action) {
    try {
        const response = await fetch(`/action`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action }) 
        });
        const gameState = await response.json();
        updateGame(gameState);
    } catch (error) {
        console.error('Error:', error);
    }
}

function updateGame(gameState) {
    const dealerCardsDiv = document.getElementById('dealer-cards');
    const playerCardsDiv = document.getElementById('player-cards');
    const outputDiv = document.getElementById('output-text');

    if (gameState.status === 'playerTurn') {
        outputDiv.textContent = ''
        dealBtn.disabled = true;
        hitBtn.disabled = false;
        standBtn.disabled = false;
        if (gameState.firstMove) {
            doubleBtn.disabled = false;
            if (gameState.canSplit) {
                splitBtn.disabled = false;
            }
        }} else {
            outputDiv.textContent = gameState.output;
            dealBtn.disabled = false;
            hitBtn.disabled = true;
            standBtn.disabled = true;
            doubleBtn.disabled = true;
            splitBtn.disabled = true;
        }


    // Clear hands
    dealerCardsDiv.innerHTML = '';
    playerCardsDiv.innerHTML = '';

    //update player cards
    gameState.playerHand.forEach(card => {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        cardDiv.textContent = card
        // hides dealers second card until the round is over
        playerCardsDiv.appendChild(cardDiv);
    });

    //update dealer cards
    gameState.dealerHand.forEach((card, index) => {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        if (gameState.dealerHand.length > 1 && index === 1 && gameState.status === 'playerTurn') {
            cardDiv.textContent = '';
        } else {
            cardDiv.textContent = card;
        }
        
        dealerCardsDiv.appendChild(cardDiv);
    });

}

// Function to fetch game state from the back-end
async function fetchGameState() {
    try {
        const response = await fetch('/get-state'); // Fetch game state from back-end
        const gameState = await response.json();
        updateGame(gameState); // Call a function to render the game state
    } catch (error) {
        console.error('Error fetching game state:', error);
    }
}

// Call fetchGameState when the page loads
window.addEventListener('DOMContentLoaded', fetchGameState);
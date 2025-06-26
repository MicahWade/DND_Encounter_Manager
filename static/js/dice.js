function closeDice() {
    const mainDiceRollMenu = document.getElementById('mainDiceRoll');
    mainDiceRollMenu.classList.add('hidden');
    popup.classList.remove('show');
}
function openDice() {
    const mainDiceRollMenu = document.getElementById('mainDiceRoll');
    mainDiceRollMenu.classList.remove('hidden');
    popup.classList.add('show');
}
function rollDice(amount, dice, modifier){
    total = 0;
    for(let i = 0; i < amount; i++){
        roll = Math.floor(Math.random() * dice) + 1
        total += roll
    }
    modifierText = (modifier > 0 ? "+"+modifier : modifier)
    const DiceInfo = document.getElementById('DiceInfo');
    if(amount == 1 && dice == 20){
        DiceInfo.innerHTML = `Dice Rolled D20 ${modifierText}`
    } 
    else{
        DiceInfo.innerHTML = `Dice Rolled ${amount}D${dice} ${modifierText}`
    }
    const DicerollText = document.getElementById('DiceRoll');
    DicerollText.innerHTML = total;
    openDice()
    return total;
}
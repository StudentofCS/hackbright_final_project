"use strict";

document.querySelector('#equipment_search_btn').addEventListener('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {
        min_level: document.querySelector('input[name="min_level"]').value 
    };

    alert('${formInputs.min_level}');
});
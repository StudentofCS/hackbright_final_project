"use strict";

document.querySelector('#equipment_search_form').addEventListener('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {

        equipment_name: document.querySelector(
            'input[name="equipment_name"]').value,
        min_level: document.querySelector('input[name="min_level"]').value,
        max_level: document.querySelector('input[name="max_level"]').value,
        min_hp: document.querySelector('input[name="min_hp"]').value,
        max_hp: document.querySelector('input[name="max_hp"]').value,
        min_ap: document.querySelector('input[name="min_ap"]').value,
        max_ap: document.querySelector('input[name="max_ap"]').value,
        min_mp: document.querySelector('input[name="min_mp"]').value,
        max_mp: document.querySelector('input[name="max_mp"]').value,
        min_wp: document.querySelector('input[name="min_wp"]').value,
        max_wp: document.querySelector('input[name="max_wp"]').value,
        min_elemental_mastery: document.querySelector(
            'input[name="min_elemental_mastery"]').value,
        max_elemental_mastery: document.querySelector(
            'input[name="max_elemental_mastery"]').value,
        min_elemental_res: document.querySelector('input[name="min_elemental_res"]').value,
        max_elemental_res: document.querySelector('input[name="max_elemental_res"]').value,
        mastery_element: document.querySelectorAll('input[name="min_level"]').value,
        res_element: document.querySelectorAll('input[name="max_level"]').value,
        min_crit_hit: document.querySelector('input[name="min_crit_hit"]').value,
        max_crit_hit: document.querySelector('input[name="max_crit_hit"]').value,
        min_block: document.querySelector('input[name="min_block"]').value,
        max_block: document.querySelector('input[name="max_block"]').value,
        min_initiative: document.querySelector('input[name="min_initiative"]').value,
        max_initiative: document.querySelector('input[name="max_initiative"]').value,
        min_spell_range: document.querySelector('input[name="min_spell_range"]').value,
        max_spell_range: document.querySelector('input[name="max_spell_range"]').value,
        min_dodge: document.querySelector('input[name="min_dodge"]').value,
        max_dodge: document.querySelector('input[name="max_dodge"]').value,
        min_lock: document.querySelector('input[name="min_lock"]').value,
        max_lock: document.querySelector('input[name="max_lock"]').value,
        min_wisdom: document.querySelector('input[name="min_wisdom"]').value,
        max_wisdom: document.querySelector('input[name="max_wisdom"]').value,
        min_prospecting: document.querySelector('input[name="min_prospecting"]').value,
        max_prospecting: document.querySelector('input[name="max_prospecting"]').value,
        min_control: document.querySelector('input[name="min_control"]').value,
        max_control: document.querySelector('input[name="max_control"]').value,
        min_force_of_will: document.querySelector('input[name="min_force_of_will"]').value,
        max_force_of_will: document.querySelector('input[name="max_force_of_will"]').value,
        min_crit_mastery: document.querySelector('input[name="min_crit_mastery"]').value,
        max_crit_mastery: document.querySelector('input[name="max_crit_mastery"]').value,
        min_crit_res: document.querySelector('input[name="min_crit_res"]').value,
        max_crit_res: document.querySelector('input[name="max_crit_res"]').value,
        min_rear_mastery: document.querySelector('input[name="min_rear_mastery"]').value,
        max_rear_mastery: document.querySelector('input[name="max_rear_mastery"]').value,
        min_rear_res: document.querySelector('input[name="min_rear_res"]').value,
        max_rear_res: document.querySelector('input[name="max_rear_res"]').value,
        min_melee_mastery: document.querySelector('input[name="min_melee_mastery"]').value,
        max_melee_mastery: document.querySelector('input[name="max_melee_mastery"]').value,
        min_armor_given: document.querySelector('input[name="min_armor_given"]').value,
        max_armor_given: document.querySelector('input[name="max_armor_given"]').value,
        min_distance_mastery: document.querySelector('input[name="min_distance_mastery"]').value,
        max_distance_mastery: document.querySelector('input[name="max_distance_mastery"]').value,
        min_armor_received: document.querySelector('input[name="min_armor_received"]').value,
        max_armor_received: document.querySelector('input[name="max_armor_received"]').value,
        min_healing_mastery: document.querySelector('input[name="min_healing_mastery"]').value,
        max_healing_mastery: document.querySelector('input[name="max_healing_mastery"]').value,
        min_berserk_mastery: document.querySelector('input[name="min_berserk_mastery"]').value,
        max_berserk_mastery: document.querySelector('input[name="max_berserk_mastery"]').value,
    };

    fetch('/api/equip_search', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {

            if (responseJson !== null) {
                alert('got it');
                // const search_tab = document.querySelector(
                //     '#equipment_tab_col');
                // const results_div = 
                //     '<div class="row row-col-4 border g-4 mb-3 pt-3" id="equipment_results_row">';
                // // search_tab.insertAdjacentHTML('beforeend', results_div)

                const results_row = document.querySelector(
                    '#equipment_results_row');
                results_row.setAttribute('style', 'display:block;')
                results_row.innerHTML = ''

                const results_qty = '<div class="col-12">' +
                                `<h5 class="text-end">Results: ${responseJson.length}</h5>` +
                                '</div>';
                results_row.insertAdjacentHTML('afterbegin', results_qty)
                

                for (const equip of responseJson) {
                    console.log(equip['id'])
                    
                    const card = 
                        '<div class="col-3">' +
                            `<div class="card h-100" id="${equip['id']}">` +
                                '<div class="card card-header">' +
                                    // <!-- equipment name -->
                                    `<span style="dispaly:inline-block;text-overflow:ellipsis;">ID: ${equip.id}</span>` +
                                    `<span style="dispaly:inline-block;text-overflow:ellipsis;">Type: ${equip.equip_type} Level: ${equip.level}</span>` +
                                '</div>' +
                                '<div class="card card-body">' +
                                    // <!-- equipment stats -->
                                '</div>' +
                            '</div>' +
                        '</div>';

                    results_row.insertAdjacentHTML('beforeend', card)
                }
            }
            

        });

});
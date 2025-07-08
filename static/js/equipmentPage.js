"use strict";

// import { debounce} from 'lodash';

if (window.location.pathname.startsWith('/build/')) {
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
                    const equips = responseJson[0]
                    const names = responseJson[1]
                    // alert('got it');

                    const search_tab = document.querySelector(
                        '#equipment_tab_col');
                    // const results_div = 
                    //     '<div class="row row-col-4 border g-4 mb-3 pt-3" id="equipment_results_row">';
                    // // search_tab.insertAdjacentHTML('beforeend', results_div)

                    // const results_row = document.querySelector(
                    //     '#equipment_results_row');
                    // results_row.setAttribute('style', 'display:block;')
                    // results_row.innerHTML = ''
                    const results_row_query = document.querySelector(
                        '#equipment_results_row'
                    );

                    if (results_row_query) {
                        search_tab.removeChild(results_row_query)
                    }

                    const results_row = document.createElement('div');
                    results_row.classList.add('row', 'row-col-4',
                        'border', 'g-4', 'mb-3', 'pt-3', 'rounded-4'
                    )
                    results_row.setAttribute('id', 'equipment_results_row')


                    // const results_qty = '<div class="col-12">' +
                    //                 `<h5 class="text-end">Results: ${equips.length}</h5>` +
                    //                 '</div>';

                    const results_qty = document.createElement('div');
                    results_qty.classList.add('col-12')
                    const results_header = document.createElement('h5');
                    results_header.classList.add('text-end')
                    results_header.innerHTML = `Results: ${equips.length}`;
                    results_qty.insertAdjacentElement('beforeend', results_header)
                    results_row.insertAdjacentElement('afterbegin', results_qty)
                    search_tab.insertAdjacentElement('beforeend', results_row)
                    
                    for (const equip of equips) {
                        // console.log(equip);
                        
                        // const card = 
                        //     '<div class="col-4">' +
                        //         `<div class="card h-100" id="card${equip.id}">` +
                        //             '<div class="card card-header">' +
                        //                 // <!-- equipment name -->
                        //                 `<span style="dispaly:inline-block;text-overflow:ellipsis;">${names[equip.id].en}</span>` +
                        //                 `<span style="dispaly:inline-block;text-overflow:ellipsis;">Type: ${equip.equip_type_id} Level: ${equip.level}</span>` +
                        //             '</div>' +
                        //             '<div class="card card-body">' +
                        //                 // <!-- equipment stats -->
                        //             '</div>' +
                        //         '</div>' +
                        //     '</div>';
                        // results_row.insertAdjacentHTML('beforeend', card)

                        const equip_dict = document.createElement('input');
                        equip_dict.setAttribute('id', `${equip.id}`)
                        equip_dict.setAttribute('value', equip)
                        equip_dict.setAttribute('type', 'hidden')
                        const col_div = document.createElement('div');
                        col_div.classList.add('col-md-4','card_col')
                        results_row.insertAdjacentElement('beforeend', col_div)
                        const card_div = document.createElement('div');
                        card_div.classList.add('card', 'h-100', 'equip-card')
                        card_div.setAttribute('id', `card${equip.id}`)
                        col_div.insertAdjacentElement('beforeend', card_div)
                        card_div.insertAdjacentElement('beforeend', equip_dict)
                        const card_header = document.createElement('div');
                        card_header.classList.add('card', 'card-header')
                        card_header.innerHTML = 
                        `<span style="dispaly:inline-block;text-overflow:ellipsis;">${names[equip.id].en}</span>` +
                        `<span style="dispaly:inline-block;text-overflow:ellipsis;">Type: ${equip.equip_type_id} Level: ${equip.level}</span>`;
                        card_div.insertAdjacentElement('beforeend', card_header)
                        const card_body = document.createElement('div');
                        card_body.classList.add('card', 'card-body')
                        card_div.insertAdjacentElement('beforeend', card_body)



                        

                        // const card_body = document.querySelector(
                        //         `#card${equip.id}`
                        //     ).querySelector('.card-body')

                        for (const stat of Object.keys(equip)) {
                            
                            if (equip[stat] !== null && !(stat in ['id', 'equip_type_id', 'level']) ) {
                                card_body.insertAdjacentHTML('beforeend', `<span style="dispaly:inline-block;text-overflow:ellipsis;">${equip[stat]} ${stat}</span>`)
                            }
                        }

                        
                        const add_equip_button = document.createElement('button');
                        add_equip_button.classList.add('btn', 'btn-sm', 
                            'btn-primary', 'ms-auto', 'add_equip')
                        add_equip_button.setAttribute('style', 
                            'bottom: 0; right: 0; position:absolute;')
                        add_equip_button.setAttribute('id', `add_${equip.id}`)
                        add_equip_button.innerHTML = 'Add';
                        add_equip_button.setAttribute('type', 'button')
                        card_body.insertAdjacentElement('beforeend', add_equip_button)
                        add_equip_button.addEventListener('click', add_equip)
                    }
                }
                

            });

    });
}


function update_build_totals(build_totals) {
    
    const main_stats = JSON.parse(document.getElementsByName(
        'main_stats_order')[0].value);
    for (const stat of main_stats) {
        const stat_name = 'total_' + stat;
        const element = document.querySelector(`#${stat_name}`);
        const updated_value = element.innerHTML.replace(
            /\d+/, `${build_totals[stat]}`);
        element.innerHTML = updated_value;
    }

    const elemental_stats = JSON.parse(document.getElementsByName(
        'elemental_stats_order')[0].value);
    for (const stat of elemental_stats) {
        const stat_name = 'total_' + stat;
        const element = document.querySelector(`#${stat_name}`);
        if (stat_name.endsWith('_res')) {
            const updated_value = element.innerHTML.replace(
                /\d+/, `${build_totals[stat]}`);
            const percentage = `(${build_totals[stat + '_percent']}%)`
            element.innerHTML = updated_value + '&nbsp' + percentage;
        }
        else {
            const updated_value = element.innerHTML.replace(
                /\d+/, `${build_totals[stat]}`);
            element.innerHTML = updated_value;
        }
    }

    const battle_stats = JSON.parse(document.getElementsByName(
        'battle_stat_order')[0].value);
    for (const stat of battle_stats) {
        const stat_name = 'total_' + stat;
        const element = document.querySelector(`#${stat_name}`);
        const updated_value = element.innerHTML.replace(
            /\d+/, `${build_totals[stat]}`);
        element.innerHTML = updated_value;
    }

    const secondary_stats = JSON.parse(document.getElementsByName(
        'secondary_stat_order')[0].value);
    for (const stat of secondary_stats) {
        const stat_name = 'total_' + stat;
        const element = document.querySelector(`#${stat_name}`);
        const updated_value = element.innerHTML.replace(
            /\d+/, `${build_totals[stat]}`);
        element.innerHTML = updated_value;
    }
}


function add_equip(evt) {
    evt.preventDefault();

    const equip_id = this.id.slice(4);
    const formInputs = {
        equip_id: equip_id,
        // equip: document.getElementById(`${equip_id}`).value,
        // build: document.getElementsByName('build_dict')[0].value,
        build_id: document.getElementsByName('build_id')[0].value

    };
    
    fetch('/api/add_equip', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {
            
            if (responseJson.equip_set.length !== 0) {
                // console.log(responseJson.equip_set)

                const set = responseJson.equip_set;
                const equip_order = JSON.parse(
                    document.getElementsByName(
                    'equip_order')[0].value);

                for (const equip of equip_order) {
                    // console.log(equip)
                    const slot = document.querySelector(`#${equip}_slot`);

                    if (set[equip] !== null) {
                        slot.innerHTML = `${equip}: ${set[equip]['id']}`
                    }
                }
            }
            if (responseJson.stat_totals.length != 0) {
                const build_totals = responseJson.stat_totals
                update_build_totals(build_totals);
            }

            });
}

// const add_equip_buttons = document.querySelectorAll('.add_equip');

// for (let i = 0; i < add_equip_buttons.length; i++) {
//     add_equip_buttons[i].addEventListener('click', (evt) => {
//         evt.preventDefault();


//         alert('add pressed')
//         const equip_id = add_equip_buttons[i].id.slice(4);
//         const formInputs = {
//             equip: document.getElementById(`#${equip_id}`).value,
//             build: document.getElementsByName('build_dict')[0].value,

//         };
        
//         fetch('/api/add_equip', {
//             method: 'POST',
//             body: JSON.stringify(formInputs),
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//         })
//             .then((response) => response.json())
//             .then((responseJson) => {
//                 alert('hello')
//                 });

//         });
// }


function activate_tab(evt) {
    evt.preventDefault();

    const tab_classes = ['characteristics_tab', 'equipment_tab',
        'spells_tab', 'runes_tab', 'auto_tab'];
    const equipment_section = document.querySelector('#equipment_slots_row');

    // DIDN'T WORK :(
    // Add sticky to equipment section if in equipment tab
    // if (this.classList.contains('equipment_tab')) {
    //     equipment_section.classList.add('sticky-sm-top')    
    // }
    // else {
    //     equipment_section.classList.remove('sticky-sm-top')
    // }
    
    for (const tab of tabs) {
        tab.classList.remove('active')
        tab.removeAttribute('aria-current')
    }

    for (const tab_class of tab_classes) {
            if (this.classList.contains(tab_class)) {
                document.querySelector(
                    `.tab_section.${tab_class}`).setAttribute(
                        'style', 'display:block;')
            } 
            else {
                document.querySelector(
                    `.tab_section.${tab_class}`).setAttribute(
                        'style', 'display:none;')
            }
        }

    this.classList.add('active')
    this.setAttribute('aria-current', 'page')
}


const tabs = document.querySelectorAll('.tab');
const tab_sections = document.querySelectorAll('.tab_section');

if (window.location.pathname.startsWith('/build/')) {
    for (const tab of tabs) {
        tab.addEventListener('click', activate_tab)
    }
}


function set_characteristics_max_and_totals(char_caps, characteristic) {

    const intelligence_order = JSON.parse(
        document.getElementsByName('intelligence_order')[0].value);
    const strength_order = JSON.parse(
        document.getElementsByName('strength_order')[0].value);
    const agility_order = JSON.parse(
        document.getElementsByName('agility_order')[0].value);
    const fortune_order = JSON.parse(
        document.getElementsByName('fortune_order')[0].value);
    const major_order = JSON.parse(
        document.getElementsByName('major_order')[0].value);
    const characteristic_sections = [intelligence_order[0],
        strength_order[0], agility_order[0], fortune_order[0],
        major_order[0]];
    const all_characteristics = intelligence_order.concat(
        strength_order, agility_order, fortune_order,
        major_order);
    const char_multipliers = JSON.parse(
        document.getElementsByName('char_multipliers')[0].value);

    for (const stat of all_characteristics) {

        if (characteristic_sections.includes(stat)) {
            const points = stat + '_points';
            const max_points = stat + '_max_points';
            const section_points = document.querySelector(
                `#${points}`);
            const section_max_points = document.querySelector(
                `#${max_points}`);

            section_points.innerHTML = characteristic[stat];
            section_max_points.innerHTML = char_caps[stat];
        }
        else {
            const point_stats = stat + '_point_stats';
            const char_total_stats = document.querySelector(
                `#${point_stats}`);
            const points_input = stat + '_points_input';
            const char_points_input = document.querySelector(
                `#${points_input}`);
            const section = char_points_input.dataset.group;

            
            const current_points = characteristic[stat];
            const section_points = characteristic[section];
            const section_cap = char_caps[section];
            const available_section_points = section_cap - section_points + 
                                                current_points;
            let points_cap = char_caps[stat];
            if (points_cap === -1 || points_cap > available_section_points) {
                points_cap = available_section_points
            }
            
            char_points_input.value = current_points;
            
            const two_multipliers = ['lock_dodge', 'mp',
                'spell_range', 'control'];
            const percentage_multipliers = ['hp_percentage',
                'heals_received', 'armor', 'crit_hit',
                'block', 'dmg_inflicted'];
            
            // Get total stats for characteristics with two stats
            if (two_multipliers.includes(stat)) {
                if (stat === 'lock_dodge') {
                    char_total_stats.innerHTML = '&nbsp' +
                        `(${current_points * char_multipliers[stat]['lock']}` +
                        '/' +
                        `${current_points * char_multipliers[stat]['dodge']})`;
                }
                else {
                    char_total_stats.innerHTML = '&nbsp' +
                        `(${current_points * char_multipliers[stat][stat]}` +
                        '/' +
                        `${current_points * char_multipliers[stat]['elemental_mastery']})`;
                }
            }
            // Add % for characteristics that are percentages
            else if (percentage_multipliers.includes(stat)) {
                char_total_stats.innerHTML = '&nbsp' +
                    `(${current_points * char_multipliers[stat]}%)`;    
            }
            // Else calculate total characteristic stats normally
            else {
                char_total_stats.innerHTML = '&nbsp' +
                    `(${current_points * char_multipliers[stat]})`;
            }
            
            char_points_input.setAttribute('max', `${points_cap}`)   
        }
    }
}


if (window.location.pathname.startsWith('/build/')) {

    const characteristic_inputs = document.querySelectorAll('.points_input')

    for (const element of characteristic_inputs) {
        element.addEventListener('input', update_characteristic)
    }
}


function update_characteristic(evt) {
    
    const char_name = this.id.slice(0,-13)
    const formInputs = {
        characteristic : char_name,
        points : this.value,
        build_id : document.getElementsByName('build_id')[0].value,
        section: this.dataset.group
    };

    fetch('/api/update_characteristic', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {
            
            const char_caps = responseJson.char_cap;
            const characteristic = responseJson.characteristic;
            const stat_totals = responseJson.stat_totals;

            if (char_caps.length !== 0 && characteristic.length !== 0) {
                set_characteristics_max_and_totals(char_caps, characteristic)
            }
            if (stat_totals.length != 0) {
                update_build_totals(stat_totals);
            }

        });
}


if (window.location.pathname.startsWith('/build/')) {
    const level_input = document.getElementsByName(
        'level')[0]
    
    level_input.addEventListener('input', update_level)
}


function update_level(evt){

    const formInputs = {
        build_id : document.getElementsByName('build_id')[0].value,
        level : this.value
    };

    fetch('/api/update_level', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type' : 'application/json',
        },
    })

        .then((response) => response.json())
        .then((responseJson) => {
            const char_caps = responseJson.char_cap;
            const characteristic = responseJson.characteristic;
            const stat_totals = responseJson.stat_totals;

            if (char_caps.length !== 0 && characteristic.length !== 0) {
                set_characteristics_max_and_totals(char_caps, characteristic)
            }
            if (stat_totals.length != 0) {
                update_build_totals(stat_totals)
            }
        });
}


// Event listener for turning checkboxes into radio-style buttons 
// and updating value
if (window.location.pathname.startsWith('/build/')) {

    // Add event listeners to main role inputs
    const main_role_inputs = document.querySelector(
        '#main_role_col').querySelectorAll('input');
    for (const input of main_role_inputs) {
        input.addEventListener('input', update_and_radio_input)
    }

    // Add event listeners to content type inputs
    const content_type_inputs = document.querySelector(
        '#content_type_col').querySelectorAll('input');
    for (const input of content_type_inputs) {
        input.addEventListener('input', update_and_radio_input)
    }
    
}


function update_and_radio_input(evt) {

    make_radio_input(this)
    update_role_and_content(this)
}


function make_radio_input(element) {
    
    const group = element.name;
    const checkboxes = document.getElementsByName(group);

    for (const checkbox of checkboxes) {
        if (checkbox !== element && checkbox.checked) {
            checkbox.checked = false;
        }
    }
}


function update_role_and_content(element) {

    let element_value = element.value;
    // If element was unchecked, send value as null to clear role/content
    if (!element.checked) {
        element_value = null;
    }

    const formInputs = {
        build_id : document.getElementsByName('build_id')[0].value,
        type: element.name,
        value : element_value
    };

    fetch('/api/update_role_and_content', {
        method : 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type' : 'application/json',
        }
    })
        .then((response) => {
            if (response.status === 204) {
                console.log('Update successful.')
            }
        })

}


function update_name(evt) {

    const formInputs = {
        build_id : document.getElementsByName('build_id')[0].value,
        build_name : this.value
    };

    fetch('/api/update_build_name', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => {
            if (response.status === 204) {
                console.log('Update successful.')
            }
        })
}

if (window.location.pathname.startsWith('/build/')) {
    const build_name_input = document.querySelector('#build_name')

    build_name_input.addEventListener('change', update_name)
}


function update_class(evt) {
    
    const formInputs = {
        build_id : document.getElementsByName('build_id')[0].value,
        class_id : this.id.slice(16)
    };

    fetch('/api/update_class', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJson) => {
            const build = responseJson.build;
            const char_class = responseJson.char_class
            const stat_totals = responseJson.stat_totals;

            if (build.length !== 0) {
                update_build_info(build, char_class)
                update_build_totals(stat_totals)
            }

        });
}


if (window.location.pathname.startsWith('/build/')) {
    const class_dropdown_buttons = document.querySelectorAll(
        '.class_dropdown')
    
    for (const button of class_dropdown_buttons) {
        button.addEventListener('click', update_class)
    }
}


function update_selected_elements(evt) {

    const formInputs = {
        build_id : document.getElementsByName('build_id')[0].value,
        position : this.dataset.position,
        element_id : this.dataset.elementId
    };

    fetch('/api/update_selected_elements', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJson) => {
            const build = responseJson.build;
            const char_class = responseJson.char_class
            const stat_totals = responseJson.stat_totals;

            if (build.length !== 0) {
                update_build_info(build, char_class)
                update_build_totals(stat_totals)
            }

        });
}


function update_build_info(build, char_class) {
    
    // Update the character class element
    const char_class_element = document.querySelector(
        '#char_class_dropdown');
    if (Object.keys(char_class).length != 0) {
        char_class_element.innerHTML = char_class.name;
    }
    
    // Update the selected elements button
    const selected_elements = document.querySelector(
        '#selected_elements_col');
    
    const positions_dict = {};
    for (const element of build.selected_elements) {
    
        positions_dict[element.position] = element.element.name;
    }
    
    for (let i = 0; i < 8; i++) {
        const btn =
        selected_elements.querySelector(
            '#dropdown_position_' + `${i.toString()}`);

        if (i < 4) {
            const position_element = positions_dict[i];
            btn.innerHTML = position_element.slice(0,-8);
        }
        else {
            const position_element = positions_dict[i];
            btn.innerHTML = position_element.slice(0,-4);
        }
    }

    // Update role
    if (build.main_role) {

        const main_role = document.querySelector('#main_role_col');
        const active_mr = main_role.querySelector(
            'input[value=' + `"${build.main_role}"` + ']');
        active_mr.checked = true;
        
    }


    // Update content type
    if (build.content_type) {

        const content_type = document.querySelector('#content_type_col');
        const active_ct = content_type.querySelector(
            'input[value=' + `"${build.content_type}"` + ']');
        active_ct.checked = true;
    }
}


if (window.location.pathname.startsWith('/build/')) {
    const selected_elements = document.querySelector(
        '#selected_elements_col').querySelectorAll('.dropdown-item')

    for (const element of selected_elements) {
        element.addEventListener('click', update_selected_elements)
    }
}


if (window.location.pathname.startsWith('/build/')) {

    const formInputs = {
        build_id : document.getElementsByName('build_id')[0].value
    };

    fetch('/api/initialize_build_info', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJson) => {
            const build = responseJson.build;
            const char_class = responseJson.char_class;
            const stat_totals = responseJson.stat_totals;
            const char_cap = responseJson.char_cap;

            if (build.length !== 0) {
                update_build_info(build, char_class)
            }
            if (stat_totals.length !== 0) {
                update_build_totals(stat_totals)
            }
            if (char_cap.length !== 0 && build.characteristic.length !== 0) {
                set_characteristics_max_and_totals(char_cap, build.characteristic)
            }
        });
}


if (window.location.pathname == ('/')) {

    const search_button = document.querySelector('#homepage_submit_button')

    search_button.addEventListener('click', update_search_results)
}


function update_search_results(evt) {
    evt.preventDefault();




    const formInputs = {
        build_name: document.querySelector(
            'input[name="build_name"]').value,
        character_class_ids : Array.from(document.querySelectorAll(
            'input[name="character_class_id"]')).map(element => {
                if (element.checked) {
                    return element.value
                }
            }).filter(element => typeof element !== 'undefined'),
        character_class_ids : Array.from(document.querySelectorAll(
            'input[name="character_class_id"]')),
        character_class_ids : Array.from(document.querySelectorAll(
            'input[name="character_class_id"]')),
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
}
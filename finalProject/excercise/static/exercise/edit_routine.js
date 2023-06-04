function update_etiquette(exerciseId, routineExercisePossition, routineId, routineExerciseId) {
    // Front component
    var input = document.querySelector('#input_' + exerciseId + '_' + routineExercisePossition);
    if (input) {
        // ETIQUETTE
        var etq = document.querySelector('.etiqueta_' + exerciseId + '_' + routineExercisePossition);
        if (etq) {
            // etiquette value 
            etq.innerHTML = input.value;
        }
    }

    // API Ret component
    console.log('Updatting exerciseRoutine');

    var url = 'http://127.0.0.1:8000/api_update_repetition/' + routineExerciseId;
    const csrftoken = getCookie('csrftoken');

    /* Get the values to build up an routineExercise */
    var repetitions_s = document.getElementById('input_' + exerciseId + '_' + routineExercisePossition);
    var new_repetittions = repetitions_s.value;

    fetch(url,
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({
                'position': routineExercisePossition,
                'repetitions': new_repetittions,
                'routine_id': routineId,
                'excercise_id': exerciseId
            })
        }
    );
    
    console.log('exerciseRoutine updated successfully');
}

function api_build_list(routine_id) {
    var testContainer = document.getElementById('test_container');
    var firstContainer = document.getElementById('firstContainer');

    var url = 'http://127.0.0.1:8000/api_list/' + routine_id;
    const csrftoken = getCookie('csrftoken');

    testContainer.innerHTML = '';

    fetch(url)
    .then((resp) => resp.json())
    .then(
        function(data){
            /*console.log('Data: ', data)*/
            const myObj = JSON.parse(data);
            for(let i = 0; i < myObj.auxiliars.length; i++) {
                let obj = myObj.auxiliars[i];
                /*console.log('Object video: ', obj['Exercise']['id_link_video']);*/
                var item = `
                    <div class="row">
                        <div class="col-sm exercise_image_container"
                            style="background: url(https://img.youtube.com/vi/${obj['Exercise']['id_link_video']}/hqdefault.jpg) no-repeat center; background-size: cover;">
                            <div class="part-1">
                                <a href="{% url 'exercise' ${obj['Exercise']['id']} %}"></a>
                            </div>
                        </div>
                        <div class="col-sm">
                            <a class="product-title"
                                href="{% url 'exercise' ${obj['Exercise']['id']} %}">${obj['Exercise']['name']}</a>
                        </div>
                        <div class="col-sm">
                            <div class="inputDiv">
                                # Repetitions:
                                <div class="etiqueta_${obj['Exercise']['id']}_${obj['RoutineExcercise']['position']}">
                                    ${obj['RoutineExcercise']['repetitions']}</div>
                                <input type="range" value="${obj['RoutineExcercise']['repetitions']}" min="1" max="10"
                                    autocomplete="off"
                                    id="input_${obj['Exercise']['id']}_${obj['RoutineExcercise']['position']}"
                                    oninput="update_etiquette('${obj['Exercise']['id']}', '${obj['RoutineExcercise']['position']}', '${routine_id}', '${obj['RoutineExcercise']['id']}')">
                            </div>
                        </div>
                        <div class="col-sm">
                            <select class="form-control" id="slc_position_${obj['Exercise']['id']}_${obj['RoutineExcercise']['position']}" name="slc_position" 
                            oninput="api_rest_update_possition('${obj['Exercise']['id']}', '${obj['RoutineExcercise']['position']}', '${routine_id}' , '${obj['RoutineExcercise']['id']}')">
                            `    
                            for(let j = 0; j < myObj.auxiliars.length; j++) {
                                let obj2 = myObj.auxiliars[j];
                                if(obj2 == obj){
                                    item += `<option selected>${obj2['RoutineExcercise']['position']}</option>`    
                                }else{
                                    item += `<option>${obj2['RoutineExcercise']['position']}</option>`
                                }
                            }
                        item += 
                            `
                            </select>
                        </div>
                        <div class="col-sm">
                            <i class="fa fa-trash" aria-hidden="true" 
                            onclick="api_rest_delete_possition('${obj['RoutineExcercise']['id']}', '${routine_id}')"></i>
                        </div>
                    </div>
                    `
                
                testContainer.innerHTML += item
            }
            firstContainer.style.display = "none";
        }
    )
    ;
    
    console.log('Listed successfully');
}

function api_rest_update_possition(exerciseId, routineExercisePossition, routineId, routineExerciseId) {

    console.log('Updatting exerciseRoutine');

    var url = 'http://127.0.0.1:8000/api_update_position/' + routineExerciseId;
    const csrftoken = getCookie('csrftoken');

    /* Get the values to build up an routineExercise */
    var position_s = document.getElementById('slc_position_' + exerciseId + '_' + routineExercisePossition);
    var new_possition = position_s.options[position_s.selectedIndex].text;

    fetch(url,
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({
                'old_position': routineExercisePossition,
                'new_position': new_possition
            })
        }
    ).then(function(response)
    {
        api_build_list(routineId)
    });
    
    console.log('exerciseRoutine updated successfully');
}

function api_rest_delete_possition(routineExerciseId, routineId) {

    console.log('Deleting exerciseRoutine');

    var url = 'http://127.0.0.1:8000/api_delete/' + routineExerciseId;
    const csrftoken = getCookie('csrftoken');

    fetch(url,
        {
            method: 'DELETE',
            headers: {
                'Content-type': 'application/json',
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({
                
            })
        }
    ).then(function(response)
    {
        api_build_list(routineId)
    });
    
    console.log('exerciseRoutine deleted successfully');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
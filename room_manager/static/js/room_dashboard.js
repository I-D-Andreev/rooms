var NUM_FAILURES = 0;
const MAX_FAILURES = 5;
const UPDATE_INTERVAL = 10000; // 10 seconds

$(document).ready(function(){
    setInterval(updateSchedule, UPDATE_INTERVAL);
});

function updateSchedule() {
    console.log("Update schedule");

    $.ajax({
        cache: false,
        url: `/get-room-schedule/${ROOM_PROFILE_ID}`,
        success: function(data){
            NUM_FAILURES = 0;
            loadData(data);
        },
        error: function(err){
            increaseNumFailures();
            console.log(err);
        }
    });
}

function loadData(data) {
    if (data.meetings.length == 0){
        increaseNumFailures();
        return;
    }
    roomOccupied(data.is_room_free);
    
    let meetingsHolder = $("#meeting_holder");

    // remove child elements
    meetingsHolder.empty();

    for(let i=0; i<data.meetings.length; i++){
        let element = createMeetingElement(data.meetings[i].start_time,
             data.meetings[i].end_time, data.meetings[i].name, data.meetings[i].background_colour);
        meetingsHolder.append(element);
    }
}

function increaseNumFailures() {
    NUM_FAILURES++;
    if (NUM_FAILURES >= MAX_FAILURES) {
        NUM_FAILURES = 0;
        location.reload();
    }
}

function createMeetingElement(start_time, end_time, name, background_colour){
    let element = `
    <div class="list-group-item border-secondary ${background_colour}">
        <span class="float-left w-25">${start_time} - ${end_time}</span>
        <span class="ml-4">${name}</span>                      
    </div>
    `;
    return element;
}

function roomOccupied(isFree) {
    let roomOccupiedHolder = $("#room_occupied_holder");
    roomOccupiedHolder.empty();
    
    let element = isFree? roomFreeElement() : roomBusyElement();
    roomOccupiedHolder.append(element);
}

function roomFreeElement(){
    return roomOccupiedElement("Free", "text-green");
}

function roomBusyElement(){
    return roomOccupiedElement("Busy", "text-danger");
}

function roomOccupiedElement(text, textColour){
    return `
        <div class="h1 w-100 ${textColour}">${text}</div>
    `;
}
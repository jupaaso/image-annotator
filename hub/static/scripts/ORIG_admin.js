//"use strict";

const DEBUG = true;
const MASONJSON = "application/vnd.mason+json";
const PLAINJSON = "application/json";

function renderError(jqxhr) {
    let msg = jqxhr.responseJSON["@error"]["@message"];
    $("div.notification").html("<p class='error'>" + msg + "</p>");
}

function renderMsg(msg) {
    $("div.notification").html("<p class='msg'>" + msg + "</p>");
}

function getResource(href, renderer) {
    $.ajax({
        url: href,
        success: renderer,
        error: renderError
    });
}

function sendData(href, method, item, postProcessor) {
    $.ajax({
        url: href,
        type: method,
        data: JSON.stringify(item),
        contentType: PLAINJSON,
        processData: false,
        success: postProcessor,
        error: renderError
    });
}

// define link for ImageContent

function ImageContentRow(item) {
    let link = "<a href='" +
                item["@controls"].self.href +
                "' onClick='followLink(event, this, renderMatches)'>update</a>" +
                " | <a href='" +
                item["@controls"].self.href +
                "' onClick='deleteResource(event, this)'>delete</a>";

    return "<tr><td>" + item.team1 +
            "</td><td>" + item.team2 +
            "</td><td>" + item.date +
            "</td><td>" + item.team1_points +
            "</td><td>" + item.team2_points +
            "</td><td>" + link + "</td></tr>";
}

function appendImageContentRow(body) {
    $(".resulttable tbody").append(ImageContentRow(body));
}

function getSubmittedImageContent(data, status, jqxhr) {
    renderMsg("Successful");
    let href = jqxhr.getResponseHeader("Location");
    if (href) {
        getResource(href, appendImageContentRow);
    }
}

function followLink(event, a, renderer) {
    event.preventDefault();
    getResource($(a).attr("href"), renderer);
}

// define submit for ImageContent

function submitImageContent(event) {
    event.preventDefault();

    let data = {};
    let form = $("div.form form");
    data.team1 = $("input[name='team1']").val();
    data.team2 = $("input[name='team2']").val();
    data.date = $("input[name='date']").val();
    data.team1_points = parseInt($("input[name='team1_points']").val());
    data.team2_points = parseInt($("input[name='team2_points']").val());
    sendData(form.attr("action"), form.attr("method"), data, getSubmittedSensor);
}

// define delete function
function deleteResource(event, a) {
    event.preventDefault();
    let resource = $(a);
    $.ajax({
        url:resource.attr("href"),
        type:"DELETE",
        success: function(){
            renderMsg("Delete Succesful");
        },
        error:renderError
    });
}

// define update function
function updateResource(event, a) {
    event.preventDefault();
    let resource = $(a);
    $.ajax({
        url:resource.attr("href"),
        type:"PUT",
        success: function(){
            renderMsg("Update Succesful");
        },
        error:renderError
    });
}

// define render for ImageContent
function renderSensorForm(ctrl) {
    let form = $("<form>");
    let team1 = ctrl.schema.properties.team1;
    let team2 = ctrl.schema.properties.team2;
    let date = ctrl.schema.properties.date;
    let team1_points = ctrl.schema.properties.team1_points;
    let team2_points = ctrl.schema.properties.team2_points;
    form.attr("action", ctrl.href);
    form.attr("method", ctrl.method);
    form.submit(submitSensor);
    form.append("<label>" + team1.description + "</label>");
    form.append("<input type='text' name='team1'>");
    form.append("<label>" + team2.description + "</label>");
    form.append("<input type='text' name='team2'>");
    form.append("<label>" + date.description + "</label>");
    form.append("<input type='text' name='date'>");
    form.append("<label>" + team1_points.description + "</label>");
    form.append("<input type='number' name='team1_points'>");
    form.append("<label>" + team2_points.description + "</label>");
    form.append("<input type='number' name='team2_points'>");
    ctrl.schema.required.forEach(function (property) {
        $("input[name='" + property + "']").attr("required", true);
    });
    form.append("<input type='submit' name='submit' value='Submit'>");
    $("div.form").html(form);
}

// new code below
function renderSensor(body) {
    $("div.navigation").html(
        "<a href='" +
        body["@controls"].collection.href +
        "' onClick='followLink(event, this, renderSensors)'>collection</a>" + 
        " | <a href='" +
        body["@controls"]["senhub:measurements-first"].href +
        "' onClick='followLink(event, this, renderMeasurements)'>measurements</a>"
    ); 
    $(".resulttable thead").empty();
    $(".resulttable tbody").empty();
    renderSensorForm(body["@controls"].edit);
    $("input[name='name']").val(body.name);
    $("input[name='model']").val(body.model);
    $("form input[type='submit']").before(
        "<label>Location</label>" +
        "<input type='text' name='location' value='" +
        body.location + "' readonly>"
    );
}
/* //new code below
function renderMeasurements(body) {
    $("div.tablecontrols").empty();
    if (body["@controls"].prev) {
        $(".tablecontrols").append ("<a href='" +
        body["@controls"].prev.href +
        "' onClick='followLink(event, this, renderMeasurements)'>Prev</a>");
    }
    if (body["@controls"].next) {
        $(".tablecontrols").append (" | <a href='" +
        body["@controls"].next.href +
        "' onClick='followLink(event, this, renderMeasurements)'>Next</a>");
    }
    $(".resulttable thead").html(
        "<tr><th>Time</th><th>Value</th></tr>"
    );
    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        let measurement = "<tr><td>" + item.time +
            "</td><td>" + item.value + "</td></tr>";
        tbody.append(measurement);
    });
}
*/
function renderSensors(body) {
    $("div.navigation").empty();
    $("div.tablecontrols").empty();
    $(".resulttable thead").html(
        "<tr><th>team1</th><th>team2</th><th>date</th><th>team1_points</th><th>team2_points</th></tr>"
    );
    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        tbody.append(sensorRow(item));
    });
    renderSensorForm(body["@controls"]["kyykka:add-match"]);
}
//edit funkkari
function renderMatches(body) {
    $("div.navigation").html(
        "<a href='" +
        body["@controls"].collection.href +
        "' onClick='followLink(event, this, renderSensors)'>Previous page</a>"
    );
    $("div.tablecontrols").empty();
    //$(".resulttable thead").html(
        //"<tr><th>team1</th><th>team2</th><th>date</th><th>team1_points</th><th>team2_points</th></tr>"
    //);
    let tbody = $(".resulttable tbody");
    tbody.empty();

    function edit_matches() {
    renderSensorForm(body["@controls"]["edit"]);
    $("input[name='team1']").val(body.team1);
    $("input[name='team2']").val(body.team2);
    $("input[name='date']").val(body.date);
    $("input[name='team1_points']").val(body.team1_points);
    $("input[name='team2_points']").val(body.team2_points);
    }
    $("button[name='Update']").click(edit_matches());
}

$(document).ready(function () {
    getResource("http://localhost:5000/api/images/", renderSensors);
});
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

// define item print outs for ImageContent metadata 
function ImageContentRow(item) {
    let link = "<img src='" +
                item.location + "'" + 
                "style='width:82px; height:86px'" + 
                "alt='" + item.name + "'>";                                

    return "<tr><td>" + item.name +
            "</td><td>" + item.publish_date +            
            "</td><td>" + item.is_private +            
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
// NOT changed yet
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
function renderImageForm(ctrl) {
    let form = $("<form>");
    let name = ctrl.schema.properties.name;
    let model = ctrl.schema.properties.location;
    form.attr("action", ctrl.href);
    form.attr("method", ctrl.method);
    form.submit(submitImageContent);
    form.append("<label>" + name.description + "</label>");
    form.append("<input type='text' name='name'>");
    form.append("<label>" + location.description + "</label>");
    form.append("<input type='text' name='model'>");
    ctrl.schema.required.forEach(function (property) {
        $("input[name='" + property + "']").attr("required", true);
    });
    form.append("<input type='submit' name='submit' value='Submit'>");
    $("div.form").html(form);
}

function renderUserLogin(ctrl) {
    let form = $("<form>");
    let name = ctrl.schema.properties.name;
    let model = ctrl.schema.properties.model;
    form.attr("action", ctrl.href);
    form.attr("method", ctrl.method);
    form.submit(submitSensor);
    form.append("<label>" + name.description + "</label>");
    form.append("<input type='text' name='name'>");
    form.append("<label>" + model.description + "</label>");
    form.append("<input type='text' name='model'>");
    ctrl.schema.required.forEach(function (property) {
        $("input[name='" + property + "']").attr("required", true);
    });
    form.append("<input type='submit' name='submit' value='Submit'>");
    $("div.form").html(form);
}

function renderStartup(body) {
    $("div.navigation").empty();
    $("div.tablecontrols").empty();
    $(".resulttable thead").html(
        "<tr><th>Name</th><th>Model</th><th>Location</th><th>Actions</th></tr>"
    );
    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        tbody.append(sensorRow(item));
    });
    renderSensorForm(body["@controls"]["senhub:add-sensor"]);
}

/* function to render uploaded image data and metadata */
function renderUploaded(body) {
    $("div.navigation").empty();
    $(".resulttable thead").html(
        "<tr><th>Filename</th><th>Publish date</th><th>Privacy class</th><th>Image</th></tr>"
    );
    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        tbody.append(ImageContentRow(item));
    });
    renderImageForm(body["@controls"]["annometa:add-image"]);    
}

/* local host for render uploaded */
$(document).ready(function () {
    getResource("http://localhost:5000/api/images/", renderUserLogin);
});

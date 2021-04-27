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


// define item print outs for User data 
function UserItemRow(item) {
    let link = "<a href='" +
                item["@controls"].self.href +
                "' onClick='followLink(event, this, renderSelection)'>Login</a>";

    return "<tr><td>" + item.user_name +            
            "</td><td>" + link + "</td></tr>";
}


// define item print outs for ImageContent metadata 
function ImageContentRow(item) {    
    let imageLink  = "<a href='" +
    item["@controls"].self.href +    
    "' onClick='followLink(event, this, renderImageAnnotation)'>Edit</a>";
    
    return createItemTable(item, imageLink);
}

// define item print outs for ImageContent metadata 
function PhotoContentRow(item) {    
    let imageLink  = "<a href='" +
    item["@controls"].self.href +    
    "' onClick='followLink(event, this, renderPhotoAnnotation)'>Edit</a>";
    
    return createItemTable(item, imageLink);
}

// create table item for image or photo
function createItemTable(item, imageLink) {
    let link = "<img src='" +
                item.location + "'" + 
                "style='width:82px; height:86px'" + 
                "alt='" + item.name + "'>";

    return "<tr><td>" + item.name +
            "</td><td>" + item.publish_date +            
            "</td><td>" + item.is_private +            
            "</td><td>" + link + 
            "</td><td>" + imageLink + "</td></tr>";
}

// render device selection 
// and back to start / user selection
function renderSelection(body) {
    // add empty navigation object
    // $("div.navigation").empty();
    // link to imagecollection / photocollection resource
    // click handlers
    $("div.navigation").html(
        "<a href='" +
        "' onClick='getImageCollection(event)'> Images </a>" +
        "<span class='linkbar'> | </span>" +
        "<a href='" +
        "' onClick='getPhotoCollection(event)'> Photos </a>" +
        "<span class='linkbar'> | </span>" +
        "<a href='" +
        "' onClick='getResource(event)'> Back to User Selection </a>"
    );
    $(".resulttable thead").empty();
    $(".resulttable tbody").empty();
}

// REQUIRED for image/photo list update, when a new is added
function appendImageContentRow(body) {
    $(".resulttable tbody").append(ImageContentRow(body));
}

// REQUIRED for image/photo list update, when a new is added
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

function getImageCollection(event) {
    event.preventDefault();
    getResource("http://localhost:5000/api/images/", renderImages);
}

function getPhotoCollection(event) {
    event.preventDefault();
    getResource("http://localhost:5000/api/photos/", renderPhotos);
}


////////////////////////////////
// define submit for ImageContent
// NOT created yet
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

// REQUIRED, not used yet
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

// REQUIRED, not used yet
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

// REQUIRED, maybe for adding a new image and photo
// define render for ImageContent
// NOT created yet
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

// define render for User Login page
// NOT created yet
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


// define render for start page
// database populated and users are already in database
function renderStartup(body) {
    $("div.navigation").empty();
    $(".resulttable thead").html(
        "<tr><th>User name</th></tr>"
    );
    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        tbody.append(UserItemRow(item));
    });    
}

/////////////////////////////////////
// REQUIRED, same funcitonality as with renderImageAnnotation, but with photos
function renderPhotoAnnotation(body) {            
    $("div.navigation").empty();  
}


/* function to render uploaded photo data and metadata */
function renderPhotos(body) {    
    $("div.navigation").html(
        "<a href='" +
        "' onClick='followLink(event, this, renderSelection)'>Back</a>"         
    );
    $(".resulttable thead").html(
        "<tr><th>Filename</th><th>Publish date</th><th>Privacy class</th><th>Photo</th></tr>"
    );
    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        tbody.append(ImageContentRow(item));
        console.log(item);
    });
    $('img').each(function() {
        var currentImage = $(this);
        currentImage.wrap("<a target='_blank' href='" + currentImage.attr("src") + "'</a>");
    });
    renderImageForm(body["@controls"]["annometa:add-photo"]);
}


function renderImageAnnotation(item) {
    
    // clear the view before rendering
    $(".imagecontent").empty();
    $(".imagemetatable tbody").empty();
    $(".imagemetatable thead").empty();
    $(".resulttable thead").empty();
    $(".resulttable tbody").empty();
    $(".form").empty();


    $("div.navigation").html(
        "<a href='" +
        "' onClick='getImageCollection(event)'> Back to Images </a>"
    );
    let link = "<img src='" +
    item.location + "'" +     
    "alt='" + item.name + "'>";
    
    let imagemeta = "<tr><td>" + item.name +
    "</td><td>" + item.publish_date + "</td></tr>";

    let imagecontent = $(".imagecontent");
    imagecontent.append(link);        
    $(".imagemetatable thead").html(
        "<tr><th>Filename</th><th>Publish date</th></tr>"
    );
    let ibody = $(".imagemetatable tbody");           
    ibody.append(imagemeta);
    
    if (item["@controls"].hasOwnProperty("imageannotation"))
    {
        getResource(item["@controls"].imageannotation.href, function(annotationItem) {
            $(".annotationtable thead").html(
                "<tr><th>Meme class</th><th>HS_class</th></tr>"
            );
            let annotations = "<tr><td>" + annotationItem.meme_class +
            "</td><td>" + annotationItem.HS_class + "</td></tr>";

            let abody = $(".annotationtable tbody");           
            abody.append(annotations);
        });
    }
    else {
        console.log("No annotations - implement add ")
    }    
}

/* function to render uploaded image data and metadata */
function renderImages(body) {    
    $("div.navigation").html(
        "<a href='" +
        "' onClick='followLink(event, this, renderSelection)'>Back</a>"         
    );
    $(".resulttable thead").html(
        "<tr><th>Filename</th><th>Publish date</th><th>Privacy class</th><th>Image</th></tr>"
    );
    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        tbody.append(ImageContentRow(item));
    });
    $('img').each(function() {
        var currentImage = $(this);
        currentImage.wrap("<a target='_blank' href='" + currentImage.attr("src") + "'</a>");
    });
    renderImageForm(body["@controls"]["annometa:add-image"]);
}


/* local host for render uploaded */
$(document).ready(function () {
    getResource("http://localhost:5000/api/users/", renderStartup);
});

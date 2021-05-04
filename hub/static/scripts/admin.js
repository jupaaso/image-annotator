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
    console.log(href);
    console.log(method);
    console.log(item);
    console.log(JSON.stringify(item));
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
    
    console.log(body);
    // MUUTOS
    sessionStorage.setItem("CurrentUser", body.user_name);
    // clear the view before rendering
    $("div.navigation").empty();
    $(".resulttable thead").empty();
    $(".resulttable tbody").empty();

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
    //$(".resulttable thead").empty();
    //$(".resulttable tbody").empty();
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

function backToImageCollection() {
    renderMsg("Delete Successful");
    $('#testform').hide(); 
    hideButtons();
    getResource("http://localhost:5000/api/images/", renderImages);
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
function deleteResource(href, callback) {    
    //let resource = $(a);
    $.ajax({
        //url:resource.attr("href"),
        url:href,
        type:"DELETE",
        success: callback,        
        error: renderError
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

     // clear the view before rendering
     $("div.navigation").empty();
     $(".resulttable thead").empty();
     $(".resulttable tbody").empty();

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
        "' onClick='followLink(event, this, renderSelection)'>Back to User Selection</a>"         
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

function createheaderForFormRow(valueString) {
    return "<div class='col-md-2 col-form-label'><label>'" +
                valueString + "</label></div>"
}

function createSpanForFormRow(valueString) {
    return "<div class='col-md-5'><span>'" +
                valueString + "</span></div>"
}

 

function appendToForm(form, rowHeader, rowValue) {
    //let annotationForm =  $(".annotationform");
    let rowElement = "<div class='row'>" + rowHeader + rowValue + "</div>";
    form.append(rowElement);
}

function getSubmittedAnnotation(data, status, xhr) {
    renderMsg("Submit of annotation was successful");
    let href = xhr.getResponseHeader("Location");
    console.log(href);
    if (href) {
        getResource(href, populateImageAnnotationForm);
    }
}

// define checkbox values to json format
function isChecked(checkbox) {
    if (checkbox.is(":checked"))
    {        
        return true;
    }
    else {        
        return false;
    }
}

function submitImageAnnotationContent(event) {
    event.preventDefault();
    let data = {};
    let form = $(".annotationMetaForm");
    
    data.image_id = parseInt(($('input[id="imageId"]', '#testform').val()));
    data.user_id = parseInt(($('input[id="userId"]', '#testform').val()));
    data.meme_class = isChecked($("#meme_class"));
    data.HS_class = isChecked($("#HS_class"));
    data.text_class = isChecked($("#text_class"));    
    data.polarity_classA = parseInt(($('input[name=inlineRadioOptions]:checked', '#testform').val()));
    //data.polarity_classB = $("#polarity_classB").val();
    data.polarity_classB = parseInt(($('input[name=rangeInputclassB]', '#testform').val()));
    //data.HS_strength = $("#HS_strength").val();
    data.HS_strength = parseInt(($('input[name=rangeInputclassHS]', '#testform').val()));
    data.HS_category = $("#HS_category").val();
    data.text_text = $("#text_text").val();
    data.text_language = $("#text_language").val();
    
    sendData(form.attr("action"), form.attr("method"), data, getSubmittedAnnotation);
}


function populateEmptyImageAnnotationForm(imageItem) {
    //$('.annotationMetaForm').show(); // Show annotation form
    $("#testform").show();

    // enable fields
    //$("#annotationMetaFormId").find('*').attr('disabled', false);
    $("#testform").find('*').attr('disabled', false);
    
    $("#text_class").prop("checked", false);
    enableTextFields();

    // set current user and image id's
    $("#annotatorName").attr("value", sessionStorage.getItem("CurrentUser"));
    $("#imageId").attr("value", imageItem.id);
    $("#userId").attr("value", imageItem.user_id);

    // get imageannotation collection to get the control, method and encoding
    getResource(imageItem["@controls"].imageannotations.href, function(annotationCollection) {
        console.log(annotationCollection);
        ctrl = annotationCollection["@controls"]["annometa:add-imageannotation"];                
        $("#annotationMetaFormId").attr("action", ctrl.href);
        $("#annotationMetaFormId").attr("method", ctrl.method);
        console.log($("#annotationMetaFormId").attr("method"));
        console.log($("#annotationMetaFormId").attr("action"));
    });
    $("#addAnnotationBtnId").show();
    $("#addAnnotationBtnId").on( "click", function(event) {        
        submitImageAnnotationContent(event);
      });      
}


function updatePolarityClassB(val) {
    document.getElementById('valuePolarity_classB').value=val; 
}


function updateHSStrength(val) {
    document.getElementById('valueHS_strength').value=val; 
}


function enableTextFields() {    
  let checkBox = document.getElementById("text_class");  
  if (checkBox.checked == true){    
    $("#text_language").prop( "disabled", false );
    $("#text_text").prop( "disabled", false );
  } else {
    $("#text_language").prop( "disabled", true );    
    $("#text_text").prop( "disabled", true );
  } 
}


function populateImageAnnotationForm(annotationItem, annotationExists) {
    // clear the view before rendering
    //$("div.navigation").empty();
    // api/imageannotations/<id>/
    getResource(annotationItem["@controls"].annotator.href, function(annotatorItem) {
        $("#annotatorName").attr("value", annotatorItem.user_name);
        $("#imageId").attr("value", annotationItem.image_id);
        $("#userId").attr("value", annotationItem.user_id);
        $("#annotationId").attr("value", annotationItem.id);    
    });

    // tässä on lista itemeistä, joiden nimillä annotaatio taulu kootaan
    let requiredItems = annotationItem["@controls"]["edit"]["schema"]["required"];    
    console.log(requiredItems);

    //let annotationForm =  $(".annotationform");

    $.each(requiredItems, function(index, item) {
        if (annotationItem.hasOwnProperty(item)) 
        {
            let value = annotationItem[item];
            console.log(item);
            console.log(value);
            switch (item) {
                case "meme_class":
                    if (value === true) {
                        $("#meme_class").prop("checked", true);
                    }
                    else {
                        $("#meme_class").prop("checked", false);
                    }
                    break;
                case "HS_class":
                    if (value === true) {
                        $("#HS_class").prop("checked", true);
                    }
                    else {
                        $("#HS_class").prop("checked", false);
                    }                 
                    break;
                case "text_class":
                    if (value === true) {
                        $("#Text_class").prop("checked", true);
                        enableTextFields();
                    }
                    else {
                        $("#Text_class").prop("checked", false);
                        enableTextFields();
                    }
                    break;
                case "polarity_classA":
                    if (value < 0) {
                        $("#Polarity_classA_Negative").prop("checked", true);
                    }
                    if (value == 0) {
                        $("#Polarity_classA_Neutral").prop("checked", true);
                    }
                    if (value > 0) {
                        $("#Polarity_classA_Positive").prop("checked", true);
                    }
                    break;

                case "polarity_classB":
                    $("#Polarity_classB").attr("value", value);
                    updatePolarityClassB(value);
                    break;
                case "HS_strength":
                    $("#HS_strength").attr("value", value);
                    updateHSStrength(value);
                    break;

                case "HS_category":
                    $("#HS_category").attr("value", value);                                    
                    break;
                case "text_text":
                    $("#text_text").attr("value", value);                
                    break;
                case "text_language":
                    $("#text_language").attr("value", value);                
                    break;                
                default:
                    break;
            }
            //$('.annotationMetaForm').show(); // Show annotation form
            $("#testform").show();
            $("#testform").find('*').attr('disabled', true);
            showButtons();
            $("#addAnnotationBtnId").prop("disabled", true);            
        }
        
        //    renderImageAnnotation(body["@controls"]["annometa:add-imageannotation"]);        
    });

    // create PUT - edit here for annotation that already exists
    // edit - put not implemented yet - coming here soon
    $("#editAnnotationBtnId").on( "click", function(event) {
        event.preventDefault();
        console.log("Annotation edit not implemented yet")
      });     
    
    $("#deleteAnnotationBtnId").on( "click", function(event) {
        event.preventDefault();
        let deleteCtrl = annotationItem["@controls"]["annometa:delete"];
        $("#annotationMetaFormId").attr("action", deleteCtrl.href);
        $("#annotationMetaFormId").attr("method", deleteCtrl.method);
        console.log("Delete of imageannotation was succesful " + deleteCtrl.href);
        deleteResource(deleteCtrl.href, backToImageCollection);
      });                
}

function hideButtons() {
    $("#addAnnotationBtnId").hide();
    $("#editAnnotationBtnId").hide();
    $("#deleteAnnotationBtnId").hide();
}

function showButtons() {
    $("#addAnnotationBtnId").show();
    $("#editAnnotationBtnId").show();
    $("#editAnnotationBtnId").prop("disabled", false);
    $("#deleteAnnotationBtnId").show();
    $("#deleteAnnotationBtnId").prop("disabled", false);
}

// item includes image as api/images/<id>/
function renderImageAnnotation(item) {
    
    // clear the view before rendering
    $("div.navigation").empty();
    $(".imagemetatable tbody").empty();
    $(".imagemetatable thead").empty();
    $(".resulttable thead").empty();
    $(".resulttable tbody").empty();
    $(".imagemetaform").empty();
    $(".form").empty();
    
    // MUUTOS
    $("div.navigation").html(
        "<a href='" +
        "' onClick=' $('.annotationMetaForm').hide(); hideButtons(); getImageCollection(event)'> Back to Images </a>"
    );
    
    /* let imagemeta = "<tr><td>" + item.name + "</td><td>" + item.publish_date + "</td></tr>"; */
    
    let requiredItems = item["@controls"]["annometa:edit"]["schema"]["required"];
    
    let imageIdName = Object.keys(item.id);
    console.log(imageIdName);
    let userIdName = Object.keys(item.user_id);
    console.log(userIdName);
    
    $.each(requiredItems, function(index, imageItem) {
        if (item.hasOwnProperty(imageItem)) 
        {
            let value = item[imageItem];
            let rowHeader = createheaderForFormRow(imageItem);
            let rowValue = createSpanForFormRow(value);

            appendToForm($(".imagemetaform"), rowHeader, rowValue);                        
        }        
    });

    let imagecontent = $(".imagecontent");
    let link = "<img src='" + item.location + "'" + "alt='" + item.name + "'>";
    imagecontent.append(link);            
    
    // annotaatio vastauksena jos sellainen on
    if (item["@controls"].hasOwnProperty("imageannotation"))
    {
        // api/imageannotations/<id>/
        getResource(item["@controls"].imageannotation.href, function(annotationItem) {
            populateImageAnnotationForm(annotationItem, true);
        });
    }
    else {
        // create and define POST - add here for new annotation
        populateEmptyImageAnnotationForm(item);
    }    
}


/* function to render uploaded image data and metadata */
function renderImages(body) {

    // clear the view before rendering
    $("div.navigation").empty();
    $(".resulttable thead").empty();
    $(".resulttable tbody").empty();
    $(".imagemetatable tbody").empty();
    $(".imagemetatable thead").empty();
    $(".imagecontent").empty();
    $(".annotationform").empty();
    $(".imagemetaform").empty();
    
    // define navigation
    $("div.navigation").html(
        "<a href='" +
        "' onClick='followLink(event, this, renderSelection)'>Back to Resource Selection</a>"         
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
    // MUUTOS
    sessionStorage.clear();
    //$('.annotationMetaForm').hide(); // Hide annotation form
    $("#testform").toggle();       
    getResource("http://localhost:5000/api/users/", renderStartup);
});

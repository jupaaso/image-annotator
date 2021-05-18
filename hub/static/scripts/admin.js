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

function showLoginAlert(xhr) {
    let msg = xhr.responseJSON["@error"]["@message"];
    alert(msg);    
}

function showAddUserAlert(xhr) {
    let msg = xhr.responseJSON["@error"]["@message"];
    alert(msg);    
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

function sendAddUserData(href, method, item, postProcessor) {
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
        error: showAddUserAlert
    });
}

function sendLoginData(href, method, item, postProcessor) {
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
        error: showLoginAlert
    });
}

function sendImageData(href, method, formData, postProcessor) {
    console.log(href);
    console.log(method);  
    console.log(formData);
    $.ajax({
        url: href,
        type: method,
        data: formData,
        contentType: false,
        processData: false,
        success: postProcessor,
        error: renderError
    });
}

function followLink(event, a, renderer) {
    event.preventDefault();
    getResource($(a).attr("href"), renderer);
}

function backToImageCollection() {
    renderMsg("Delete/Update was successful");    
    $('#testform').each(function(){
        this.reset();
    });    
    $('#testform').hide(); 
    hideAnnoFormButtons();
    getResource("http://localhost:5000/api/images/", renderImages);
}

function getImageCollection(event) {
    event.preventDefault();
    // TESTI TESTI $('.annotationMetaForm').hide();
    $('.imageAnnotationForm').hide();
    //$('#AnnoFormButtons').hide();
    getResource("http://localhost:5000/api/images/", renderImages);
}

function getPhotoCollection(event) {
    event.preventDefault();
    getResource("http://localhost:5000/api/photos/", renderPhotos);
}

// define delete of resource
function deleteResource(href, callback) {    
    $.ajax({
        url:href,
        type:"DELETE",
        success: callback,
        error: renderError
    });
}

// define delete of image resource
function deleteImageResource(href) {    
    $.ajax({
        url:href,
        type:"DELETE",
        success: renderMsg("Image deleted."),        
        error: renderError
    });
}

// define update-edit-put of resource
function updateResource(href, callback) {
    $.ajax({
        url:href,
        type:"PUT",
        success: callback,
        // success: function(){ renderMsg("Update Succesful"); },
        error:renderError
    });
}

// -------------------------------------------------------------------------------------
// LOGIN USER and ADD USER page

/*  // define item print outs for User data 
function UserItemRow(item) {
    let link = "<a href='" +
                item["@controls"].self.href +
                "' onClick='followLink(event, this, renderSelection)'>Login</a>";

    return "<tr><td>" + item.user_name + "</td><td>" + link + "</td></tr>";
} */

// define render for start page / user login page
// database populated and users are already in database
// user item - api/users/<user>

function renderLoginResponse(data, status, xhr) {
    if (xhr.status === 200) {
        console.log("User login OK")
        let href = xhr.getResponseHeader("Location");
        if (href) {
            console.log(href);
            $("#userFormId").hide();
            getResource(href, renderSelection);            
        }
    }
    else {
        console.log(xhr.status)
        console.log("User login failed")
        alert("User login failed - invalid user name or password");
    }
}

function renderAddUserResponse(data, status, xhr) {
    if (xhr.status === 201) {
        console.log("New user was created successfully")
        let href = xhr.getResponseHeader("Location");
        if (href) {
            console.log(href);
            $("#userFormId").hide();
            getResource(href, renderSelection);            
        }
    }
    else {
        console.log(xhr.status)
        console.log("Add of user failed")
        alert("Add of user failed - invalid user name or password");
    }
}

function renderStartup(body) {
    // clear and define the view before rendering
    $("div.navigation").empty();
    $(".resulttable thead").empty();
    $(".resulttable tbody").empty();

    $("#userFormId").show();
    showUserFormButtons();
    $("#editUserBtnId").hide();
    $("#deleteUserBtnId").hide();
    $("#imageListBtnId").hide();
    $("#photoListBtnId").hide();
    $("#userAccountBtnId").hide();

    $("#user_name").attr('disabled', false);

    /*
    $(".resulttable thead").html("<tr><th>User name</th></tr>");
    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        tbody.append(UserItemRow(item));
    });
    */

    let data = {};
    let form = $("#userFormId");
    
    // define login POST for user that already exists
    $("#loginUserBtnId").on( "click", function(event) {
        event.preventDefault();
        event.stopPropagation();
        //console.log("User login not implemented yet");
        if ($("#user_name").val() !== '') {
            data.user_name = $("#user_name").val();
        }
        else {
            alert("Please enter user name")
        }
        if ($("#user_password").val() !== '') {
            data.user_password = $("#user_password").val();
        }
        else {
            alert("Please enter password")
        }
        if ($("#user_name").val() !== '' && $("#user_password").val() !== '') {
            console.log($("#user_name").val() + " " + $("#user_password").val())

            loginCtrl = body["@controls"]["annometa:login"];
            sendLoginData(loginCtrl.href, loginCtrl.method, data, renderLoginResponse);
        }       
    });

    // define add POST for new user
    $("#addUserBtnId").on("click", function(event) {        
        event.preventDefault();
        //console.log("Add user with post not implemented yet");
        if ($("#user_name").val() !== '') {
            data.user_name = $("#user_name").val();
        }
        else {
            alert("Please enter user name")
        }
        if ($("#user_password").val() !== '') {
            data.user_password = $("#user_password").val();
        }
        else {
            alert("Please enter password")
        }
        if ($("#user_name").val() !== '' && $("#user_password").val() !== '') {
            addUserCtrl = body["@controls"]["annometa:add-user"];
            sendAddUserData(addUserCtrl.href, addUserCtrl.method, data, renderAddUserResponse);
        }            
    }); 
}

function hideUserFormButtons() {
    $("#addUserBtnId").hide();
    $("#editUserBtnId").hide();
    $("#deleteUserBtnId").hide();
    $("#loginUserBtnId").hide();
    $("#imageListBtnId").hide();
    $("#photoListBtnId").hide();
    $("#userAccountBtnId").hide();
}

function showUserFormButtons() {
    $("#addUserBtnId").show();
    $("#editUserBtnId").show();
    $("#deleteUserBtnId").show();
    $("#loginUserBtnId").show();
    $("#imageListBtnId").show();
    $("#photoListBtnId").show();
    $("#userAccountBtnId").show();
}

// USER ACCOUNT page -------------------------------------------------------------
// can be used to delete user or change password

function renderUserData(body) {
    // show html form
    $("#userFormId").show();
    // show/hide buttons
    $("#deleteUserBtnId").show();
    $("#editUserBtnId").show();
    $("#addUserBtnId").hide();
    $("#loginUserBtnId").hide();
    $("#imageListBtnId").hide();
    $("#photoListBtnId").hide();
    $("#userAccountBtnId").hide();
    $("#user_name").attr("value", body.user_name);
    $("#user_name").attr('disabled', true);
    $("#user_password").attr("value", body.user_password);

    let data = {};

    // define delete for user that already exists
    $("#deleteUserBtnId").on( "click", function(event) {
        event.preventDefault();
        //console.log("User delete not implemented yet");
        if ($("#user_password").val() !== '') {
            data.user_password = $("#user_password").val();
            data.user_name = $("#user_name").val();
            let deleteUserCtrl = body["@controls"]["annometa:delete"];
            console.log()
            deleteResource(deleteUserCtrl.href, renderStartup);
        }
        else {
            alert("Password cannot be empty")
        }
    });

    // define put-edit for user that already exists
    $("#editUserBtnId").on( "click", function(event) {
        event.preventDefault();
        //console.log("User edit not implemented yet");
        if ($("#user_password").val() !== '') {
            data.user_password = $("#user_password").val();
            data.user_name = $("#user_name").val();             
            let editCtrl = body["@controls"]["edit"];            
            console.log()
            sendData(editCtrl.href, editCtrl.method, data, function() {
                $("#userFormId").hide();
                getResource(body["@controls"]["self"]["href"], renderSelection);
            });
        }
        else {
            alert("Password cannot be empty")
        }
    });
}

// DEVICE SELECTION page -------------------------------------------------------------

// render device / user account selection
function renderSelection(body) {
    console.log(body);
    // define logged in current user
    sessionStorage.setItem("CurrentUser", body.user_name);
    // define html form for device selection buttons
    let form = $("#selectionFormId");
    // show UI blocks
    document.getElementById("leftSidebar").style.display = "block";
    document.getElementById("rightSidebar").style.display = "block";
    // clear the view before rendering
    $("div.navigation").empty();
    // show buttons
    showUserFormButtons();
    $("#imageListBtnId").show();
    $("#photoListBtnId").show();
    $("#userAccountBtnId").show();
    // hide buttons and tables
    $("#addUserBtnId").hide();
    $("#editUserBtnId").hide();
    $("#deleteUserBtnId").hide();
    $("#loginUserBtnId").hide();
    $(".resulttable thead").empty();
    $(".resulttable tbody").empty();
    //$("#uploadFileBtnId").hide();
    $("#userFormId").hide();

    $("#imageListBtnId").on( "click", function(event) {
        event.preventDefault();
        getResource("http://localhost:5000/api/images/", renderImages);
    });

    $("#photoListBtnId").on( "click", function(event) {
        event.preventDefault();
        getResource("http://localhost:5000/api/photos/", renderPhotos);
    });

    $("#userAccountBtnId").on( "click", function(event) {
        event.preventDefault();
        getResource(body["@controls"]["self"]["href"], renderUserData);
    });

    /*
    // click handlers and link to imagecollection / photocollection resource
    $("div.navigation").html(
        "<a href='" +
        "' onClick='getImageCollection(event)'> Images </a>" +
        "<span class='linkbar'> | </span>" +
        "<a href='" +
        "' onClick='getPhotoCollection(event)'> Photos </a>" +
        "<span class='linkbar'> | </span>" +
        "<a href='" +
        body["@controls"].self.href +
        "' onClick='followLink(event, this, renderUserData)'>" + body.user_name + "</a>"
    );
    */
}

// IMAGES / PHOTOS TABLE page ---------------------------------------------------------------

// define table items for image or photo
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

// define item print outs for Image Content metadata 
function ImageContentRow(item) {    
    let imageLink  = "<a href='" +
    item["@controls"].self.href +    
    "' onClick='followLink(event, this, renderImagesTable)'> Modify Annotation </a>" +
    "<a href='" +
    item["@controls"].self.href + 
    "' onClick='followLink(event, this, deleteImageContent)'> Delete Image </a>";
    return createItemTable(item, imageLink);
}

// define item print outs for Photo Content metadata 
function PhotoContentRow(item) {    
    let imageLink  = "<a href='" +
    item["@controls"].self.href +    
    "' onClick='followLink(event, this, renderPhotosTable)'> Modify Annotation </a>" +
    "<a href='" +
    item["@controls"].self.href + 
    "' onClick='followLink(event, this, deletePhotoContent)'> Delete Photo </a>"
    return createItemTable(item, imageLink);
}

// define delete for image on list/table
function deleteImageContent(imageItem) {
    let deleteCtrl = imageItem["@controls"]["annometa:delete"];
    deleteImageResource(deleteCtrl.href);
    getResource("http://localhost:5000/api/images/", renderImages);
}

// define delete for photo on list/table - not created yet

// REQUIRED for image/photo list update, when a new is added
function appendImageContentRow(body) {
    $(".resulttable tbody").append(ImageContentRow(body));
}

// REQUIRED for image/photo list update, when a new is added
function getSubmittedImageContent(data, status, jqxhr) {
    renderMsg("Image/Photo update was successful");
    //let href = jqxhr.getResponseHeader("Location");
    //if (href) {
    //    getResource(href, getImageCollection);
   // }
   getResource("http://localhost:5000/api/images/", renderImages);
}

// UPLOAD or CANCEL new IMAGES / PHOTOS on file list
// file select window for image files
function handleFileSelectImages (e) {
    var files = e.target.files;
    if (files.length < 1) {
        alert('Select a file...');
        return;
    }
    // -------------------------------------
    //$("#uploadFileBtnId").attr('disabled', true);
    $("#fileElem").attr('disabled', true);
    $("div.fileElem").empty();
    $("#fileList").empty();

    var file = files[0];
    fileList.innerHTML = "";
    const list = document.createElement("ul");
    fileList.appendChild(list);

    const li = document.createElement("li");
    list.appendChild(li);

    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    img.height = 60;
    img.onload = function() {
    URL.revokeObjectURL(this.src);
    }
    li.appendChild(img);
    const info = document.createElement("span");
    info.innerHTML = file.name + ": " + file.size + " bytes";
    li.appendChild(info);

    $("#cancelUploadBtn").show();
    $("#uploadBtn").show();

    $("#cancelUploadBtn").on("click", function(event) {        
        event.preventDefault();
        // ----------------
        $("div.fileList").empty();
        $("div.fileElem").empty();
        //$("#uploadFileBtnId").attr('disabled', false);
        $("#cancelUploadBtn").hide();
        $("#uploadBtn").hide();
        $("#fileElem").val(null);
        $("#fileElem").attr('disabled', false);
    });

    $("#uploadBtn").on("click", function(event) {        
        event.preventDefault();
        $("div.fileList").empty();
        //$("#uploadFileBtnId").attr('disabled', false);
        $("#cancelUploadBtn").hide();
        $("#uploadBtn").hide();

        const fd = new FormData();
        fd.append('image', file);
        let data = {};
        data.user_name = sessionStorage.getItem("CurrentUser");
        // file select for images: "is_private" = false
        data.is_private = false;
        fd.append('request', JSON.stringify(data));
        file = undefined;
        $("#fileElem").val(null);
        // --------------
        $("div.fileElem").empty();
        $("#fileElem").attr('disabled', false);
        sendImageData($("#imageUploadFormId").attr("action"), $("#imageUploadFormId").attr("method"), fd, getSubmittedImageContent);
    }); 
}

// for adding a new image and photo - define render for ImageContent
function renderImageForm(ctrl) {
    $("imageUploadFormId").toggle();
    //$("#uploadFileBtnId").show();
    $("#imageUploadFormId").attr("action", ctrl.href);
    $("#imageUploadFormId").attr("method", ctrl.method);
    $(function () {
        //$('#uploadFileBtnId').click(function(e) {
        //    $('#fileElem').click();
        //});
        //$('#fileElem').change(handleFileSelectImages);
        // TÄSSÄ BUGI - cancel kuva filet jäävat muistiin listaksi ----------------------------
        const inputElement = document.getElementById("fileElem");
        inputElement.addEventListener("change", handleFileSelectImages, false);
    });
}

/* function to render uploaded photo data and metadata */
function renderPhotos(body) {    
    $("div.navigation").html(
        "<a href='" +
        "' onClick='followLink(event, this, renderSelection)'>Back to Device Selection</a>"         
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

// item includes image as api/images/<id>/

function renderImagesTable(item) {
    // clear the view before rendering
    $("div.navigation").empty();
    $(".imagemetatable tbody").empty();
    $(".imagemetatable thead").empty();
    $(".resulttable thead").empty();
    $(".resulttable tbody").empty();
    $(".imagemetaform").empty();
    // TESTI TESTI $(".imageListForm").empty();
    $(".imageListForm").hide();
    //$("#uploadFileBtnId").hide();

    $("div.navigation").html(
        "<a href='" +
        "' onClick='getImageCollection(event)'> Back to Images </a>"
    );
    // $('.annotationMetaForm').hide(); $('#AnnoFormButtons').hide();

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
    // provides annotation as response if there is one
    if (item["@controls"].hasOwnProperty("imageannotation"))
    {
        // api/imageannotations/<id>/
        getResource(item["@controls"].imageannotation.href, function(annotationItem) {
            populateImageAnnotationForm(annotationItem, true);
        });
    }
    else {
        // create and define POST-add for new annotation
        populateEmptyImageAnnotationForm(item);
    }    
}

// MUUTOS ALKAA  -------------------------------------------------------

function backToDeviceSelection(event) {
    event.preventDefault();

    hideAnnoFormButtons();
    // TESTI; POISTA ??? $(".annotationMetaForm").empty();
    // VANHA; POISTA $(".annotationform").empty();
    //$(".imagemetaform").empty();
    //$("#testform").empty();

    let currentUser = sessionStorage.getItem("CurrentUser");        
    getResource("http://localhost:5000/api/users/" + currentUser, function(userData) {
        renderSelection(userData);
    });
}
// MUUTOS Päättyy-------------------------------------------------

// function to render uploaded image data and metadata
function renderImages(body) {
    // clear the view before rendering    
    document.getElementById("leftSidebar").style.display = "none";
    document.getElementById("rightSidebar").style.display = "none";    
    $("div.navigation").empty();
    $(".resulttable thead").empty();
    $(".resulttable tbody").empty();
    $(".imagemetatable tbody").empty();
    $(".imagemetatable thead").empty();
    $(".imagecontent").empty();
    // VANHA; POISTA  $(".annotationform").empty();
    hideAnnoFormButtons();
    $("#imageListFormId").show();

    //$(".imagemetaform").empty();
    //$(".annotationMetaForm").empty();
    //$("#testform").empty();
    
    // define navigation
    // MUUTOS alkaa----------------------------------------------------
    
    $("div.navigation").html(
        "<a href='" +        
        "' onClick='backToDeviceSelection(event)'>Device Selection</a>"         
    );

    // Muutos päättyy    --------------------------------------------------

    $(".resulttable thead").html(
        "<tr><th>Filename</th><th>Publish date</th><th>Privacy class</th><th>Image</th></tr>"
    );

    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        tbody.append(ImageContentRow(item));
    });
    // create 'image-in-new-window-tab'
    $('img').each(function() {
        var currentImage = $(this);
        currentImage.wrap("<a target='_blank' href='" + currentImage.attr("src") + "'</a>");
    });
    // add image files from folder here
    renderImageForm(body["@controls"]["annometa:add-image"]);
}

/////////////////////////////////////// ---------------------------------------------------------------------------------

// REQUIRED, same funcitonality as with renderImagesTable, but with photos
function renderPhotosTable(body) {            
    $("div.navigation").empty();  
}

/////////////////////////////////////// ---------------------------------------------------------------------------------

// helper functions for image annotation -----------------------------------

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
    renderMsg("Submit of new annotation was successful");
    let href = xhr.getResponseHeader("Location");
    console.log(href);
    if (href) {
        getResource(href, populateImageAnnotationForm);
    }
}

function getEditedAnnotation(data, status, xhr) {
    renderMsg("EDIT of annotation was successful");
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

function hideAnnoFormButtons() {
    $("#addAnnotationBtnId").hide();
    $("#editAnnotationBtnId").hide();
    $("#deleteAnnotationBtnId").hide();
}

function showAnnoFormButtons() {
    $("#addAnnotationBtnId").show();
    $("#editAnnotationBtnId").show();
    $("#editAnnotationBtnId").prop("disabled", false);
    $("#deleteAnnotationBtnId").show();
    $("#deleteAnnotationBtnId").prop("disabled", false);
}

// EDIT - PUT for image annotation --------------------------------------------------------------

function putImageAnnotationContent(event) {
    event.preventDefault();
    let data = {};
    let form = $(".annotationMetaForm");

    data.id = parseInt(($('input[id="annotationId"]', '#testform').val()));
    data.image_id = parseInt(($('input[id="imageId"]', '#testform').val()));
    data.user_id = parseInt(($('input[id="userId"]', '#testform').val()));
    data.meme_class = isChecked($("#meme_class"));
    data.HS_class = isChecked($("#HS_class"));
    data.text_class = isChecked($("#text_class"));    
    data.polarity_classA = parseInt(($('input[name=inlineRadioOptions]:checked', '#testform').val()));
    data.polarity_classB = parseInt(($('input[name=rangeInputclassB]', '#testform').val()));
    data.HS_strength = parseInt(($('input[name=rangeInputclassHS]', '#testform').val()));
    data.HS_category = $("#HS_category").val();
    data.text_text = $("#text_text").val();
    data.text_language = $("#text_language").val();

    sendData(form.attr("action"), form.attr("method"), data, getEditedAnnotation);
}

function editImageAnnotationContent(event) {
    event.preventDefault();
    $("#testform").find('*').attr('disabled', false);
    hideAnnoFormButtons();
    $("#editAnnotationBtnId").show();
    $("#editAnnotationBtnId").on( "click", function(event) {        
        putImageAnnotationContent(event);
    }); 
}

// ADD - POST for image annotation --------------------------------------------------------------

function submitImageAnnotationContent(event) {
    event.preventDefault();
    let data = {};
    let form = $(".annotationMetaForm");
    
    // post tarvitsee image_id ja user_id
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
    $("div.notification").empty();
    // set current user and image id's
    $("#annotatorName").attr("value", sessionStorage.getItem("CurrentUser"));
    $("#imageId").attr("value", imageItem.id);
    $("#userId").attr("value", imageItem.user_id);
    $("#annotationId").attr("value", $("#annotationId").attr("placeholder"));

    // clear text fields if not already empty
    $("#HS_category").val('');
    $("#text_language").val('');
    $("#text_text").val('');

    // enable fields
    $("#testform").find('*').attr('disabled', false);
    $("#text_class").prop("checked", false);
    enableTextFields();

    // get imageannotation collection to get the control, method and encoding
    getResource(imageItem["@controls"].imageannotations.href, function(annotationCollection) {
        console.log(annotationCollection);
        ctrl = annotationCollection["@controls"]["annometa:add-imageannotation"];                
        $("#annotationMetaFormId").attr("action", ctrl.href);
        $("#annotationMetaFormId").attr("method", ctrl.method);
        console.log($("#annotationMetaFormId").attr("method"));
        console.log($("#annotationMetaFormId").attr("action"));
    });
    $("#testform").show();
    $("#addAnnotationBtnId").show();
    $("#addAnnotationBtnId").on( "click", function(event) {        
        submitImageAnnotationContent(event);
      });      
}

// helpers for population of annotation table ------------------------------------------

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

// -------------------------------------------------------------------------------------

function populateImageAnnotationForm(annotationItem, annotationExists) {
    // api/imageannotations/<id>/
    getResource(annotationItem["@controls"].annotator.href, function(annotatorItem) {
        $("#annotatorName").attr("value", annotatorItem.user_name);
        $("#imageId").attr("value", annotationItem.image_id);
        $("#userId").attr("value", annotationItem.user_id);
        $("#annotationId").attr("value", annotationItem.id);    
    });
    // list of items to define annotation table
    let requiredItems = annotationItem["@controls"]["edit"]["schema"]["required"];    
    console.log(requiredItems);

    // ----------------------------------------------
    //let annotationForm =  $(".annotationform");
    $(".imageAnnotationForm").show();
    $("#testform").show();

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
            // Show annotation form - $('.imageAnnoMetaForm').show();
            // define add-post button for new annotation
            //$(".imageAnnotationForm").show();
            //$("#testform").show();
            
            $("#testform").find('*').attr('disabled', true);
            showAnnoFormButtons();
            $("#addAnnotationBtnId").prop("disabled", true);            
        }      
    });

    // define put-edit for annotation that already exists
    $("#editAnnotationBtnId").on( "click", function(event) {
        event.preventDefault();
        //console.log("Annotation edit not implemented yet")
        let editCtrl = annotationItem["@controls"]["edit"];
        $("#annotationMetaFormId").attr("action", editCtrl.href);
        $("#annotationMetaFormId").attr("method", editCtrl.method);
        console.log("EDIT of imageannotation was succesful " + editCtrl.href);
        editImageAnnotationContent(event);
      });

    // define delete for annotation that already exists
    $("#deleteAnnotationBtnId").on( "click", function(event) {
        event.preventDefault();
        let deleteCtrl = annotationItem["@controls"]["annometa:delete"];
        $("#annotationMetaFormId").attr("action", deleteCtrl.href);
        $("#annotationMetaFormId").attr("method", deleteCtrl.method);
        console.log("Delete of imageannotation was succesful " + deleteCtrl.href);
        deleteResource(deleteCtrl.href, backToImageCollection);
      });                
}


// ---------------------------------------------------------------------------
// render local host upload as start page / home page

$(document).ready(function () {
    // MUUTOS
    sessionStorage.clear();
    //$('.annotationMetaForm').hide(); // Hide annotation form
    $("#testform").toggle();    
    getResource("http://localhost:5000/api/users/", renderStartup);
});

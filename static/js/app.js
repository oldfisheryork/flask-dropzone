// dropzone.js initialization 
$(function() {
    // Define the drop zone area
    var myDropzone = new Dropzone(document.querySelector('.fileUploadArea'), { 
        url: "/uploadajax", // Set the url
        method: "POST", // can be changed to "put" if necessary
        maxFilesize: 200, // in MB
        uploadMultiple: true, // This option will also trigger additional events (like processingmultiple).
        headers: {
            "My-Awesome-Header": "header value"
        },

        previewTemplate : '<div style="display:none"></div>', // build-in but in our requirement no need to display
        createImageThumbnails: false, // no need to display the image
        parallelUploads: 20,
        autoQueue: true, // Make sure the files aren't queued until manually added

        clickable: false,// files can only be uploaded via drag and drop, no through clicking the area

        autoProcessQueue: true, // When set to false you have to call myDropzone.processQueue() yourself in order to upload the dropped files. 
        forceFallback: false,

        // initializaiton 
        init: function() {
            this.on("complete", function (file) {
                if (this.getUploadingFiles().length === 0 && this.getQueuedFiles().length === 0) {
                    readFiles("upload");
                }
            });
            console.log("init");
        },

        accept: function(file, done) {
            console.log("accept");
            done();
        },

        fallback: function() {
            console.log("fallback");
        }
    });

    // processing added files 
    myDropzone.on("addedfile", function(file) {
        myDropzone.enqueueFile(file);
        myDropzone.processQueue();
    });
});

// read the files in the uploads folder and then display 
function readFiles(path) {
   // empty the table every time before upload new file
    $("#fileTable tr").remove();
    // add one more row for the new uploaded file
    $.ajax({
        url:'filenameajax',
        type:'get',
        cache:false,
        success: function(data) {    
            if (data.result.length != 0 ) {
                // for every file in the folder, add one more row
                $.each(data.result, function(index, value){
                    addRowForTable('fileTable', value)
                });
            }
        }
    })
}

// add one more row to the page
function addRowForTable(tableID, filename) {
    var table = document.getElementById(tableID);
    var rowCount = table.rows.length;
    var row = table.insertRow(rowCount);
    // update the table 
    row.innerHTML = row.innerHTML+"<tr><td class='highlight'><div class='success'></div><a>"+filename+"</a></td>"
                    + "<td><a href= '/uploads/"+filename+"' download ><i class='icon-edit'></i> Download </a></td></tr>";
}
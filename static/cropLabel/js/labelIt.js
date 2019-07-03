var images = []

//-----------
$.each(crop_data.cropdata, function(i) {
  init_crop_data = crop_data.cropdata[i].split('.').slice(0, -1).join('.')
        images.push(init_crop_data)
      });

var labels = crop_data.labels;

if (images === undefined || images.length == 0) alert('images undefined');
var image_format = '.' + images[0].split('.')[1];


var images_path = 'images/'
if (crop_data.imagesPath != undefined) {
  images_path = crop_data.imagesPath;
}

if (crop_data.selected != undefined) {
  images_index = crop_data.selected;
}
//---

var image_index = 0;
var image_tracker = image_path = images[image_index];

var captured = null;
var capturedList = [];
var selected_index = 0;
var copiedSelection = null;



//todo reload color map and existing captures
const labelColorMap = new Map();
for (var key in crop_data.labelColors) {
  labelColorMap.set(key, crop_data.labelColors[key]);
}

const capturedMap = new Map();
capturedMap.set(initial_image, crop_data.existingCaptures);

//set original image size
var trueWidth = 0;
var trueHeight = 0;

var image = new Image();
image.src = images_path + image_path;



function getImageRealSize() {
    trueWidth = image.naturalWidth;
    trueHeight = image.naturalHeight;
    //show real size
    $("#twd").val(trueWidth);
    $("#thd").val(trueHeight);
}

function getPlugins() {
  $.each(crop_data.plugins, function(plg) {
        $("#selMo").append($("<option />").val(this.id).text(this.name));
  });
}

function initialImagesAndPlugginLoad() {
    getImageRealSize();
    getPlugins();
}

image.onload = initialImagesAndPlugginLoad

  jQuery(function($){

    // Create variables (in this scope) to hold the API and image size
    var jcrop_api,
        boundx,
        boundy;

        grabInfo();

    $('#target').Jcrop({
      onChange: updatePreview,
      onSelect: updatePreview,
      onRelease:  clearCoords,
      boxWidth: 800,
      boxHeight: 400
      //aspectRatio: xsize / ysize //this is to keep squared shape
    }, function(){
      // Use the API to get the real image size
      var bounds = this.getBounds();
      boundx = bounds[0];
      boundy = bounds[1];

      // Store the API in the jcrop_api variable
      jcrop_api = this;

      // Move the preview into the jcrop container for css positioning
      $preview.appendTo(jcrop_api.ui.holder);
    });

    $('#bnext').on('click', function(e) {
      changeImage('next');
      updatePreview(e);
      if (copiedSelection != null) {
        jcrop_api.setSelect(copiedSelection);
      }
      return false;
    });

    $('#bback').on('click', function(e) {
      changeImage('back');
      updatePreview(e);
      if (copiedSelection != null) {
        jcrop_api.setSelect(copiedSelection);
      }
      return false;
    });

    $("#close").on('click',function() {
      $("#myModal").css("display", "none");
      $("#" + captured['divId']).remove();
      captured = null;
    });

    $("#newlabel").on("change paste", function() {
      var label_selected = $(this).val(); 
      addToLabelList(label_selected);
      closeModal(label_selected);
    });

    $("#selectlabels").on("change select keypress", function() {
      label_selected = $(this).val(); 
      closeModal(label_selected);
    });

    $('#capture').on('click', function(e) {
        captured = {
          img: $('#img_name').val(),
          cx: $('#x1').val(),
          cy: $('#y1').val(),
          cw: $('#w').val(),
          ch: $('#h').val(),
          twd: $('#twd').val(),
          thd: $('#thd').val(),
          divBorderColor: getRandomColor()
        };

        if (!validCapture(captured)) {
            return false;
        }

        //call fuction to show label selection and on true proceed to draw 
        refreshLabelList();

        //disable select element, only added if the label list is not empty      
        if (labels === undefined || labels.length == 0) {
          $("#selectlabels").prop("disabled", true );
        } else { //-------------------------- 
          $("#selectlabels").prop("disabled", false );
        }

        openLabelSelectWindow();

        drawCapturedArea(captured);

        toggleEditSelectionButtons(false);
      return false;
    });

    $('#coords').on('change','input',function(e){
      alert("this feature should be deleted?")
      var x1 = $('#x1').val(),
          x2 = $('#x2').val(),
          y1 = $('#y1').val(),
          y2 = $('#y2').val();
          alert([x1,y1,x2,y2]);
      jcrop_api.setSelect([x1,y1,x2,y2]);
    });


    $('#enext').on('click', function(e) {
      selected_index++;
      if (selected_index >= capturedList.length) {
        selected_index = 0;
      }
      var capturr = capturedList[selected_index];
      jcrop_api.setSelect(getSelect(capturr));
      resetInputs(capturr);
      // copy selection
      copiedSelection = getSelect(capturr);
      return false;
    });

    $('#eback').on('click', function(e) {
      selected_index--;
      if (selected_index < 0) {
        selected_index = capturedList.length - 1;
      }
      var capturr = capturedList[selected_index];
      jcrop_api.setSelect(getSelect(capturr));
      resetInputs(capturr);
      // copy selection
      copiedSelection = getSelect(capturr);
      return false;
    });

    $('#edel').on('click', function(e) {
      //delete
      capt = capturedList[selected_index];
      image_name = capt.img;

      // filter out the selected one
      capList = capturedList.filter(c => c.divId != capt.divId);
      delList = capturedList.filter(c => c.divId == capt.divId);
      
      capturedMap.set(image_name, capList);
      capturedList = capList;
      console.log(capturedMap);
      selected_index=0;

      //request saved the new captured (without the deleted item
      if (delList.length > 0) {
        //delete specific capture
        deleteSelected({project_folder: project_folder, image_name: image_name, label:delList[0]})
        refreshAfterChanged(capturedList, e);
      }
      return false;
    });

    function refreshAfterChanged(capturedList, e) {
        //repaint new state
        changeImage('remain');
        updatePreview(e);

        if (capturedList === undefined || capturedList.length == 0) {
            toggleEditSelectionButtons(true);
        }
    }

//    $('#ecpy').on('click', function(e) {
//      var capturr = capturedList[selected_index];
//      copiedSelection = getSelect(capturr);
//    });

    $("#gen").on('click', function(e) {
         var value = $("#selMo").val();
         getGenerate({projectName: project_name, model:value})
    });

    function validCapture(tured) {
        return tured.cx > 0 && tured.cy > 0 && tured.ch > 0 && tured.cw > 0;
    }

    function getSelect(captur) {
      temp = [
        parseInt(captur.cx),
        parseInt(captur.cy),
        parseInt(captur.cx) + parseInt(captur.cw),
        parseInt(captur.cy) + parseInt(captur.ch)
      ];
      return temp;
    }

    function resetInputs(cap) {
      $("#label_name").val(cap['label']);
      $("#color_name").val(cap['divBorderColor']);
      $("#edel").prop("disabled", false );
    }

    function toggleEditSelectionButtons(enable) {
       $("#eback").prop("disabled", enable );
       $("#enext").prop("disabled", enable );
       $("#edel").prop("disabled", enable );
       $("#ecpy").prop("disabled", enable );
    }

    function openLabelSelectWindow() {
      $("#myModal").css("display", "block");
    }

    function drawCapturedArea(captured) {

        console.log(captured);
        target = document.getElementById('target');
        $("#target-canvas").css({width: target.style.width, height: target.style.height, position:'absolute'});

        canvasId ="x"+Math.round( captured.cx)+"y"+Math.round( captured.cy);
        canvas = document.createElement("div");
        canvas.id= canvasId;
        identifier = "#"+canvasId

        $("#target-canvas").append(canvas);

        if (typeof captured.drawBox == 'undefined') {
            captured.drawBox = jcrop_api.tellScaled();
        }

        $(identifier).css({
          top: Math.round( captured.drawBox.y) +'px',
          left: Math.round( captured.drawBox.x) +'px',
          width: Math.round( captured.drawBox.w),
          height: Math.round( captured.drawBox.h),
          zIndex:88,
          border:"1px solid",
          position:'absolute',
          borderColor: captured.divBorderColor});

        captured['divId'] = canvasId;
    }

    function grabInfo() {
      // Grab some information about the preview pane
      $preview = $('#preview-pane'),
      $pcnt = $('#preview-pane .preview-container'),
      $pimg = $('#preview-pane .preview-container img'),

      xsize = $pcnt.width(),
      ysize = $pcnt.height();
    }

    function updatePreview(c) {
       //console.log(c);
      if (parseInt(c.w) > 0) {

        $preview.css({
          width: c.w + 'px',
          height: c.h + 'px',
        });

        $pcnt.css({
          width: c.w + 'px',
          height: c.h + 'px',
        });

        xsize = $pcnt.width(),
        ysize = $pcnt.height();

        var rx = xsize / c.w;
        var ry = ysize / c.h;

        bounds = jcrop_api.getBounds();
        boundx = bounds[0];
        boundy = bounds[1];

        //change pcnt to reflect the selected area
        var drawW = Math.round(rx * boundx);
        var drawH = Math.round(ry * boundy);
        var drawX = Math.round(rx * c.x);
        var drawY = Math.round(ry * c.y);

        $pimg.css({
          width: drawW + 'px',
          height: drawH + 'px',
          marginLeft: '-' + drawX + 'px',
          marginTop: '-' + drawY + 'px'
        });
      }

      showCoords(c)
    };

    function showCoords(c) {
        $('#x1').val(c.x);
        $('#y1').val(c.y);
        $('#x2').val(c.x2);
        $('#y2').val(c.y2);
        $('#w').val(c.w);
        $('#h').val(c.h);
        $('#img_name').val(images[image_index]);
    };

    function clearCoords(){
      $('#coords input').val('');
      $("#edel").prop("disabled", true );
    };

    function changeImage(direction){
      $("#target-canvas").empty();
      if (direction == 'next') {
        if (image_index < images.length - 1) {
          image_index =  image_index + 1;
        }
      } 

      if (direction == 'back') {
        if (image_index > 0) {
          image_index =  image_index - 1;
        }
      }

      image_tracker=images[image_index];
      
      image_path = images_path + images[image_index];
      jcrop_api.setImage(image_path);
      jcrop_api.setOptions({ bgOpacity: .6 });

      $('#img_name').val(image_tracker);

      $("target").attr("src", image_path);
      $("target").css({width: '100%', height: '100%'});

      //update preview box
      $pimg.attr("src", image_path);

      //get image real size
      image.src = image_path;
      getImageRealSize();

      //bring de already captured
      getCaptured({projectName: project_name, imageName: image_tracker}, repaintCaptures);
    }

    //
    function repaintCaptures(photoName) {
      capturedObject = capturedMap.get(photoName);
      if (capturedObject != null) {

        capturedList = capturedObjectToList(capturedObject);
        toggleEditSelectionButtons(false);

        $.each(capturedList, function(cap) {
          drawCapturedArea(capturedList[cap])
        });
      }
    }

    function getRandomColor() {
      var letters = '0123456789ABCDEF';
      var color = '#';
      for (var i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }

    function refreshLabelList() {

      $("#selectlabels").empty();

      var i =0
      $.each(labels, function() {
        $("#selectlabels").append($("<option/>").val(labels[i]).text(labels[i]));
        i++;
      });
    }

    function addToLabelList(label) {
      if (!labels.includes(label)) {
        labels.push(label);
        //console.log(labels);
      }
    }

    function closeModal(label_selected) {
      $("#myModal").css("display", "none");
      captured['label'] = label_selected;
      alert(captured['label'])

      colorForLabel = labelColorMap.get(label_selected);
      if (colorForLabel == null) {
        labelColorMap.set(label_selected, captured['divBorderColor']);
      } else {
        captured['divBorderColor'] = colorForLabel;
        $('#'+captured['divId']).css({borderColor: captured.divBorderColor});
      }
      //save captured
      storeToMap(captured['img'], captured);
    }

    // store in a map
    function storeToMap(pictureName, captured) {
      //get list of picture data given the picture's name
      var pictureNameList = capturedMap.get(pictureName);
      if (pictureNameList == null) {
        pictureNameList = [];
      } 

      capturedIndex = findSameCaptured(pictureNameList, captured['divId']);
      if (capturedIndex > -1) {
        pictureNameList[capturedIndex] = captured;
      } else {
        pictureNameList.push(captured);
      }
      
      capturedList = pictureNameList; //set current captured list

      //update map
      capturedMap.set(pictureName, pictureNameList);
      console.log(capturedMap);

      // post to back end
      postUpdate({
        project_folder: project_folder,
        image_name: pictureName,
        image_label_list: pictureNameList,
        label_list: labels,
        label_color_map: strMapToObj(labelColorMap)});
    }

//     // store in a map
//    function storeToMapAfterDel(pictureName, callback) {
//      //get list of picture data given the picture's name
//      var pictureNameList = capturedMap.get(pictureName);
//      if (pictureNameList == null) {
//        pictureNameList = [];
//      }
//
//      capturedList = pictureNameList; //set current captured list
//
//      //update map
//      console.log(capturedMap);
//
//      // post to back end
//      postUpdate({
//        project_folder: project_folder,
//        image_name: pictureName,
//        image_label_list: pictureNameList,
//        label_list: labels,
//        label_color_map: strMapToObj(labelColorMap)});
//
//      // retrieve the latest
//      callback(arguments[2], arguments[3])
//    }

    // find previous with same selection
    function findSameCaptured(capturedList, capturedDiv) {
      for (var i = 0; i < capturedList.length; i++) {
        cptrd = capturedList[i];
        if (cptrd['divId'] == capturedDiv) {
          return i;
        }
      }

      return -1;
    }


    //todo server side interactions
    function deleteSelected(requestData) {
        console.log(requestData);
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        console.log(csrftoken);

        $.ajax({
            url: 'http://localhost:8000/deleteSelected/',
            type: 'post',
            data: JSON.stringify(requestData),
            headers: {
                "X-CSRFToken": csrftoken
            },
            contentType: 'application/json',
            dataType: 'json',
            success: function (response) {
                console.info(response);
            },
            error: function(response) {
                alert('Error: ' + response.responseText);
            }
        });

        return false;
    }

    //todo server side interactions
    function postUpdate(requestData) {
        console.log(requestData);
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        console.log(csrftoken);

        $.ajax({
            url: 'http://localhost:8000/crop/',
            type: 'post',
            data: JSON.stringify(requestData),
            headers: {
                "X-CSRFToken": csrftoken
            },
            contentType: 'application/json',
            dataType: 'json',
            success: function (response) {
                console.info(response);
            },
            error: function(response) {
                alert('Error: ' + response.responseText);
            }
        });

        return false;
    }


    function getCaptured(requestData, repaintCaptures) {
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
                url: `http://localhost:8000/retrieveCaptured/`,
                type: 'post',
                data: JSON.stringify(requestData),
                headers: {
                    "X-CSRFToken": csrftoken
                },
                contentType: 'application/json',
                dataType: 'json',

                success: function(response){
                        captured = response['captured'];
                        console.log(captured);

                        //convert it to list
                        var captureL = capturedObjectToList(captured);

                        capturedMap.set(requestData['imageName'], captureL);
                        repaintCaptures(requestData['imageName'])
                 },
                 error: function(response) {
                    alert(`woops! ${requestData}` +response); //or whatever
                 }
        });

        return false;
    }

    function getGenerate(requestData) {
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
                url: `http://localhost:8000/process/`,
                type: 'post',
                data: JSON.stringify(requestData),
                headers: {
                    "X-CSRFToken": csrftoken
                },
                contentType: 'application/json',
                dataType: 'json',

                success: function(response){
                        console.log(response);
                 },
                 error: function(response) {
                    alert(`woops! ${requestData}` +response.status); //or whatever
                 }
        });
    }

    //convert string map to object
    function strMapToObj(strMap) {
        let obj = Object.create(null);
        for (let [k,v] of strMap) {
            // We don’t escape the key '__proto__'
            // which can cause problems on older engines
            obj[k] = v;
        }
        return obj;
    }

    //conver captured map to a list
    function capturedObjectToList(capturedObject) {
        var list = [];
        for (var key in capturedObject) {
            list.push(capturedObject[key]);
        }
        return list;
    }

    $(window).bind("load", function() {
        refreshLabelList();
        repaintCaptures(image_tracker);
    });
  });


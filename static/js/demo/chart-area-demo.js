// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
// Render FITACF browser chart
function parse(url, div) {
    var opt = {
      mode: "vega-lite",
      renderer: "svg",
      actions: {export: true, source: false, editor: false}
    };
    vegaEmbed("#"+div, url).then(function(result) {
        // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
      }).catch(console.error);
}
// Render Histogram scatter plot
function parsehistsctr(url, div) {
    var opt = {
      mode: "vega-lite",
      renderer: "svg",
      actions: {export: true, source: false, editor: false}
    };
    vegaEmbed("#"+div, url).then(function(result) {
        // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
      }).catch(console.error);
}
// parse("/fitbaseplot", "fitbasevis")


// jquery code to reset all the empty forms 
// once the page reloads
$( '.form-control' ).val("");

// jquery code to toggle between button options
$(".dropdown-menu li a").click(function(){
    $(this).parents(".btn-group").find('.selection').text($(this).text());
    $(this).parents(".btn-group").find('.selection').val($(this).text());

  });



// jquery code to be executed after clicking the plot button
$('#plotButton').on('click', function (e) {
    // get the parameters in the selected boxes
    var ftypeVal = $("#ftypeList").parents(".btn-group").find('.selection').text()
    var pltTypeVal = $("#pltPrmList").parents(".btn-group").find('.selection').text()
    var dateVal = $("#dateForm").val()
    var startTimeVal = $("#startTimeForm").val()
    var endTimeVal = $("#endTimeForm").val()
    var radVal = $("#radForm").val()
    // create a json of these vals
    inpJson = {
        "ftypeVal" : ftypeVal,
        "pltTypeVal" : pltTypeVal,
        "dateVal" : dateVal,
        "startTimeVal" : startTimeVal,
        "endTimeVal" : endTimeVal,
        "radVal" : radVal
    }
    // send (ajax) the data to flask
    // get the json back and populate the
    // corresponding div
    $.ajax({
      type: "POST",
      contentType: "application/json;charset=utf-8",
      url: "/updatebaseplot",
      traditional: "true",
      data: JSON.stringify(inpJson),
      dataType: "json",  
      success: function(data) {
         parse(data, "fitbasevis"); 
      }
      });
})


// jquery code to be executed after clicking the plot button
$('#plotHistButton').on('click', function (e) {
    // get the parameters in the selected boxes
    var ftypeVal = $("#ftypeList").parents(".btn-group").find('.selection').text()
    var pltTypeVal = $("#pltPrmList").parents(".btn-group").find('.selection').text()
    var cmprTypeVal = $("#cmprPrmList").parents(".btn-group").find('.selection').text()
    var dateVal = $("#dateForm").val()
    var startTimeVal = $("#startTimeForm").val()
    var endTimeVal = $("#endTimeForm").val()
    var radVal = $("#radForm").val()
    // create a json of these vals
    inpJson = {
        "ftypeVal" : ftypeVal,
        "pltTypeVal" : pltTypeVal,
        "cmprTypeVal" : cmprTypeVal,
        "dateVal" : dateVal,
        "startTimeVal" : startTimeVal,
        "endTimeVal" : endTimeVal,
        "radVal" : radVal
    }
    // send (ajax) the data to flask
    // get the json back and populate the
    // corresponding div
    $.ajax({
      type: "POST",
      contentType: "application/json;charset=utf-8",
      url: "/updthistcmprplot",
      traditional: "true",
      data: JSON.stringify(inpJson),
      dataType: "json",  
      success: function(data) {
         parsehistsctr(data, "histsctrvis"); 
      }
      });
})

// jquery loading function
var $loading = $('#fitbasevis').hide();
$(document)
  .ajaxStart(function () {
    $loading.hide();
  })
  .ajaxStop(function () {
    $loading.show();
  });
var $loadingHist = $('#histsctrvis').hide();
$(document)
  .ajaxStart(function () {
    $loadingHist.hide();
  })
  .ajaxStop(function () {
    $loadingHist.show();
  });
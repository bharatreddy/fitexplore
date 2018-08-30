// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
// Render Charts 
function parse(url, div) {
var opt = {
  mode: "vega-lite",
  renderer: "svg",
  actions: {export: true, source: false, editor: false}
};
// vegaEmbed("#"+div, url, opt, function(error, result) {
//   // console.log(error)
//   // result.view is the Vega View, url is the original Vega-Lite specification
//   vegaTooltip.vegaLite(result.view, url);
// });
vegaEmbed("#"+div, url).then(function(result) {
    // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
  }).catch(console.error);
}
parse("/fitbaseplot", "fitbasevis")
// parse("/data/waterfall", "waterfall")
// parse("/data/line", "line");
// parse("/data/multiline", "multiline");
// parse("/data/stocks", "stocks");
// parse("/data/scatter", "scatter");


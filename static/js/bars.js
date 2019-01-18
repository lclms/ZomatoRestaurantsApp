'use strict';
// with strict mode, you can not, for example, use undeclared variables

//****************************************************
// 		the profile of the hosts
//****************************************************

// Note: visualization will be put in the div with id=hosts_id

// see https://bl.ocks.org/d3noob/bdf28027e0ce70bd132edc64f1dd7ea4
// plus tooltip

var margin = {top: 30, right: 30, bottom: 40, left: 40},
    width = 700 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;
    
// set the dimensions and add the graph canvas to the body of the webpage
var svg = d3.select("#hosts_id").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// set the ranges
var x = d3.scaleBand()
          .range([0, width])
          .padding(0.3);
          
var y = d3.scaleLinear()
          .range([height, 0]);

var formatDecimalComma = d3.format(",.2f"),
    formatMoney = function(d) { return formatDecimalComma(d) + "€"; };

// add the tooltip area to the webpage
var tooltip = d3.select("body").append("div").attr("class", "tooltip").style("opacity", 0);

// load data and set visualization

// data fields are (all numeric): host_id|num_listings|average_price|
// we want to see the top hosts in terms of number of listings 
// they have advertised

    function drawHostsProfile(data) {
    // change string (from csv) into number format
    // but use host_id as string
    if(data)
    {
    console.log(data);
    
        data.forEach(function(d) {
            d.country = d.country;
            d.num_restaurants_by_country = + d.num_restaurants_by_country;
            
        });
    

   // scale the range of the data in the domains
  x.domain(data.map(function(d) { return d.country; }));
  y.domain([0, d3.max(data, function(d) { return d.num_restaurants_by_country; })]);

  // append the rectangles for the bar chart
  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.country); })
      .attr("width", x.bandwidth())
      .attr("y", function(d) { return y(d.num_restaurants_by_country); })
      .attr("height", function(d) { return height - y(d.num_restaurants_by_country); })
      .style("fill", "steelblue")
      .on("mouseover", function (d) {
            tooltip.transition()
                .duration(100)
                .style("opacity", .9);
            tooltip.html("" + d.num_restaurants_by_country)
                .style("left", (d3.event.pageX + 5) + "px")
                .style("top", (d3.event.pageY - 50) + "px");
        })
        .on("mouseout", function (d) {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
        });

  // add the x Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
      .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-30)");

  // add the y Axis
  svg.append("g")
      .call(d3.axisLeft(y));
  
}};



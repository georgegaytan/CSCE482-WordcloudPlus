//Simple animated example of d3-cloud - https://github.com/jasondavies/d3-cloud
//Based on https://github.com/jasondavies/d3-cloud/blob/master/examples/simple.html

//Global dictionary, follows {"word" : "color"} format
//i.e. {"cuba" : "rgb(78.55%, 0%, 21.45%)"}
var word_color = {}

//Appropriately sets color based on source%
function color_filler(site1_percentage, site2_percentage){
    var color = "";

    //iterates through all words, distributes % of red/blue
    for (i in site1_percentage){
        //this format is used to 'fill' svg objects
        color = "rgb(" + site1_percentage[i] + "%,0%," + site2_percentage[i] + "%)";
        word_color[i] = color;
    }
    //console.log(word_color);
}

// Encapsulate the word cloud functionality
function wordCloud(selector) {

    //var fill = d3.scale.category20();
	//Construct the word cloud's SVG element
	var svg = d3.select(selector).append("svg")
		.attr("width", 1000)
		.attr("height", 1000)
		.append("g")
		.attr("transform", "translate(500,500)");
	
    //Draw the word cloud
    function draw(words) {
		
        var cloud = svg.selectAll("g text")
                        .data(words, function(d) { return d.text; })
		
        //Entering words
        cloud.enter()
            .append("text")
            .style("font-family", "Impact")
            //fills svg with color based on param tied to word 'd.text'
			.style("fill", function(d, i){return word_color[d.text];})
			.style("fill-opacity", 1)
            .attr("text-anchor", "middle")
            .attr('font-size', 1)
            .text(function(d) { return d.text; })
			//.style("font-size", function(d) { return d.size + "px"; })
			//.attr("transform", function(d) {
			//	console.log(d.text + ": " + d.x);
            //    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
			//})
		
        //Entering and existing words
        cloud.transition()
                .duration(600)
                .style("font-size", function(d) { return d.size; })
				.attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
				})
		
        //Exiting words
        cloud.exit()
            .transition()
                .duration(200)
                .style('fill-opacity', 1e-6)
                .attr('font-size', 1)
                .remove();
		
    }


    //Use the module pattern to encapsulate the visualisation code. We'll
    // expose only the parts that need to be public.
    return {

        //Recompute the word cloud for a new set of words. This method will
        // asycnhronously call draw when the layout has been computed.
        //The outside world will need to call this function, so make it part
        // of the wordCloud return value.
        update: function(words) {
            d3.layout.cloud().size([1000, 1000])
				.font("Impact")
                .fontSize(function(d) { return d.size; })
				.text(function (d) { return d.text; })
				.x(function (d) { return d.x; })
				.y(function (d) { return d.y; })
				.padding(1)
                .words(words)
                .on("end", draw)
                .start();
        }
    }
}

//This method tells the word cloud to redraw with a new set of words.
//In reality the new words would probably come from a server request,
// user input or some other source.
function showNewWords(vis, words, site1_percentage, site2_percentage) {

    //alert(site1_percentage);
	
    //applies percentages to word_color dict
    color_filler(site1_percentage, site2_percentage);
	
    //runs update with given 'words' set on vis aka myWordCloud
	var previous_positions;
    vis.update(words);

	setTimeout(function() { showNewWords(vis, words)}, 5000)
}

//Simple animated example of d3-cloud - https://github.com/jasondavies/d3-cloud
//Based on https://github.com/jasondavies/d3-cloud/blob/master/examples/simple.html

//Global dictionary, follows {"word" : "color"} format
//i.e. {"cuba" : "rgb(78.55%, 0%, 21.45%)"}
var word_color = {}
var source1_percentage = {}
var source2_percentage = {}

//Appropriately sets color based on source%
function color_filler(site1_percentage, site2_percentage){
    var color = "";

    //iterates through all words, distributes % of red/blue
    for (i in site1_percentage){
        //this format is used to 'fill' svg objects
        color = "rgb(" + site1_percentage[i] + "%,0%," + site2_percentage[i] + "%)";
        word_color[i] = color;
    }
    // console.log(word_color);
}

function word_source_position(site1_percentage, site2_percentage) {
    for (i in site1_percentage) {
        source1_percentage[i] = site1_percentage[i];
    }

    for (i in site2_percentage) {
        source2_percentage[i] = site2_percentage[i]
    }
    // console.log(location_percentage);
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
            .attr("text-anchor", "middle")
            .attr('font-size', 1)
            .text(function(d) { return d.text; });

        //Entering and existing words
        cloud
            .transition()
                .duration(600)
                .style("font-size", function(d) { return d.size + "px"; })
                .attr("transform", function(d) {
                    if (source1_percentage[d.text] > source2_percentage[d.text]) {
                        return "translate(" + [source1_percentage[d.text] * 3, d.y] + ")rotate(" + d.rotate + ")";
                    }
                    else {
                        return "translate(" + [-source2_percentage[d.text] * 3, d.y] + ")rotate(" + d.rotate + ")";
                    }
                })
                .style("fill-opacity", 1);

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
                .words(words)
                .padding(5)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { return d.size; })
                .on("end", draw)
                .start();
        }
    }

}

//Some sample data - http://en.wikiquote.org/wiki/Opening_lines
/*
var words = [
    "You don't know about me without you have read a book called The Adventures of Tom Sawyer but that ain't no matter.",
    "The boy with fair hair lowered himself down the last few feet of rock and began to pick his way toward the lagoon.",
    "When Mr. Bilbo Baggins of Bag End announced that he would shortly be celebrating his eleventy-first birthday with a party of special magnificence, there was much talk and excitement in Hobbiton.",
    "It was inevitable: the scent of bitter almonds always reminded him of the fate of unrequited love."
]
*/
//Prepare one of the sample sentences by removing punctuation,
// creating an array of words and computing a random size attribute.
//function getWords(i) {
function getWords(words) {
    //return words[i]
    return words
			.replace(/[!\.,:;\?]/g, '')
            .split(' ')
            .map(function(d) {
                return {text: d, size: 10 + Math.random() * 60};
            })
}

//This method tells the word cloud to redraw with a new set of words.
//In reality the new words would probably come from a server request,
// user input or some other source.
function showNewWords(vis, words, site1_percentage, site2_percentage) {
    //i = i || 0;
    //vis.update(getWords(i ++ % words.length));
	//vis.update(getWords(words));
    //alert(site1_percentage);

    //applies percentages to word_color dict
    color_filler(site1_percentage, site2_percentage);

    word_source_position(site1_percentage, site2_percentage);

    //runs update with given 'words' set on vis aka myWordCloud
    vis.update(words);

	//setTimeout(function() { showNewWords(vis, words)}, 5000)
}

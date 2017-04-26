//Simple animated example of d3-cloud - https://github.com/jasondavies/d3-cloud
//Based on https://github.com/jasondavies/d3-cloud/blob/master/examples/simple.html

//Global dictionary, follows {"word" : "color"} format
//i.e. {"cuba" : "rgb(78.55%, 0%, 21.45%)"}
var timeslot_word_color = {}
var placed_words_text = []
var placed_words = []
var global_instance = 1;
var previous_instance = 1;

//Appropriately sets color based on source%
function color_filler(current_year, current_year_freq){
    var color = "";
    var r = {};
    //If area1/2/3 exist, assign them to dictionary r/b/g
    //YES THESE ARE NOT RGB, THEY ARE RBG. So Area1v2 can be RvB
    if (current_year_freq[0] != ""){
        r = {current_year_freq[0]};
    }
    if (current_year_freq[1] != ""){
        var b = {current_year_freq[1]};
    }
    if (current_year_freq[2] != ""){
        var g = {current_year_freq[2]};
    }

    if (typeof b !== 'undefined' && typeof g !== 'undefined') {
        //iterates through all words, distributes % of red/blue/green
        for (var word in r){
            //this format is used to 'fill' svg objects
            color = "rgb(" + r[word] + "%," + g[word] + "%," + b[word] + "%)";
            timeslot_word_color[current_year][word] = color;
        }
    } else if (typeof b !== 'undefined') {
        //iterates through all words, distributes % of red/blue/green
        for (var word in r){
            //this format is used to 'fill' svg objects
            color = "rgb(" + r[word] + "%,0%," + b[word] + "%)";
            timeslot_word_color[current_year][word] = color;
        }   
    } else if (typeof g !== 'undefined') {
        //iterates through all words, distributes % of red/blue/green
        for (var word in r){
            //this format is used to 'fill' svg objects
            color = "rgb(" + r[word] + "%," + g[word] + "%,0%)";
            timeslot_word_color[current_year][word] = color;
        }   
    } else {
        //iterates through all words, distributes % of red/blue/green
        for (var word in r){
            //this format is used to 'fill' svg objects
            color = "rgb(" + r[word] + "%,0%,0%)";
            timeslot_word_color[current_year][word] = color;
        }      
    }

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

    function draw(words) {
        var cloud = svg.selectAll("g text")
                        .data(words, function(d) { return d.text; })

        //Entering words
        cloud.enter()
            .append("text")
            .style("font-family", "Impact")
            .style("fill-opacity", 1)
            .attr("text-anchor", "middle")
            .attr('font-size', 1)
            .text(function(d) { return d.text; })

        //Entering and existing words
        cloud.transition()
            .duration(900)
            //fills svg with color based on param tied to word 'd.text'
            .style("fill", function(d, i){ 
                if (global_instance == 1){return timeslot_word_color[current_year][d.text];}
                else if (global_instance == 2){return timeslot_word_color[current_year][d.text];}
                else {return area3_word_color[d.text];}
            })
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
    
    function placed(word){
        placed_words_text.push(word.text);
        placed_words.push(word);
    }

    //Use the module pattern to encapsulate the visualisation code. We'll
    // expose only the parts that need to be public.
    return {
        //Recompute the word cloud for a new set of words. This method will
        // asycnhronously call draw when the layout has been computed.
        //The outside world will need to call this function, so make it part
        // of the wordCloud return value.
        update: function(current_year, words, current_year_freq) {
            d3.layout.cloud().size([1000, 1000])
                .font("Impact")
                .fontSize(function(d) { return d.size; })
                .text(function (d) { return d.text; })
                .x(function (d) { return d.x; })
                .y(function (d) { return d.y; })
                .rotate(function (d){
                    if (d.rotate != null) {return d.rotate;}
                    else {return ~~(Math.random() * 2) * 90;}
                })
                .padding(1)
                .words(words)
                .on("word", placed)
                .on("end", draw)        
                .start(current_year_freq[0], current_year_freq[1]);
        }
    }
}

//This method tells the word cloud to redraw with a new set of words.
//In reality the new words would probably come from a server request,
// user input or some other source.

function showNewWords(current_year, vis, all_words, current_year_freq) {
    if (previous_instance = current_year-1){
        for (var word = all_words.length-1; word >= 0; --word){
            var index = placed_words_text.indexOf(words[word].text);
            if (index != -1){
                all_words[word].x = placed_words[index].x;
                all_words[word].y = placed_words[index].y;
                all_words[word].rotate = placed_words[index].rotate;
            }
        }
    }
        
    placed_words_text = [];
    placed_words = [];
    previous_instance = current_year;
    global_instance = current_year;
        
    //applies percentages to word_color dict, instance = year
    color_filler(current_year, current_year_freq);

    //runs update with given 'words' set on vis aka myWordCloud
    vis.update(current_year, all_words, current_year_freq);
    
    for (var word = all_words.length-1; word >= 0; --word){
        if (placed_words_text.indexOf(all_words[word].text) == -1){
            all_words.splice(word, 1);
        }
    }
}


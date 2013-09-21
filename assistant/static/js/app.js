var tagselect = function() {
    var input = $('.tags input[name="tags"]');
    var tags = $('.tags ul > li');
    var widget = $('.tags ul');
    
    var tag_on_click = function(index, event) {
	var val = input.val();
	var element = $(this);
	var selected = element.attr('selected');
	if (selected) {
	    element.attr('selected', false);
	    var selected_tags = val.split(',');
	    var current_tag_index = selected_tags.indexOf(element.text());
	    selected_tags.splice(current_tag_index, 1);
	    input.val(selected_tags.join(','));
	} else {
	    element.attr('selected', true);
	    if (val) {
		input.val(val + ',' + element.text());
	    } else {
		input.val(element.text());
	    }
	}
    }

    tags.map(function(index, element) {
	var element = $(element);
	element.click(tag_on_click);
    })

    var newtag = $('<li class="add-tag"><span class="glyphicon glyphicon-edit"></span> New tag</li>');
    var newtag_on_click = function() {
	$(this).remove()
	var newinput = $('<li><form><input type="text"/><input type="submit" value="Add"/><form></li>');
	newinput.submit(function(event) {
	    var tag = $('input[type="text"]', newinput).val();
	    newinput.remove();
	    tag = $('<li>' + tag + '</li>');
	    tag.click(tag_on_click);
	    widget.append(tag);
	    tag_on_click.call(tag);
	    widget.append(newtag);
	    newtag.click(newtag_on_click);
	});
	widget.append(newinput);
    };
    newtag.click(newtag_on_click);
    widget.append(newtag);
}

tagselect();  // Parameters are harcoded

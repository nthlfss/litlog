<script>

function view_books()
{
	$.getJSON('https://www.googleapis.com/books/v1/volumes?q=food+allergies&maxResults=5', function(data) {
	  var items = [];
	
	  $.each(data, function(key, val) {
	    items.push('<li id="' + key + '">' + val + '</li>');
	  });
	
	  $('<ul/>', {
	    'class': 'my-new-list',
	    html: items.join('')
	  }).appendTo('body');
	});
}

function view_books2()
{
	$.ajax({
	  url: "https://www.googleapis.com/books/v1/volumes?q=food+allergies&maxResults=5",
	  dataType: "json",
	  success: function(){
  	}
});
}
</script>
<button onclick="view_books();">Click</button>
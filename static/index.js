
var selectedWord = null;



/*---------- Key Handling ----------*/

$('#search-input').keypress(function(e) {
    if(e.which == 13){

        var input = $(this).val();
        console.log(input);
        
        fetch("https://cors-anywhere.herokuapp.com/https://api.datamuse.com/sug?s=" + input)
            .then(response => response.json())
            .then(data => populateSearchResults(data));

    }
});

/*---------- On Click Events ----------*/

$('.quote-word').on('click', function(e){
    clearSelectedWord();
    $(this).addClass('selected');
    selectedWord = $(this).html();
});


/*---------- Helper Functions -----------*/

function clearSelectedWord(){
    $('.quote-word').each(function(){
        $(this).removeClass('selected');
    });
}

function populateSearchResults(data){

    $('#search-results').html(' ');

    for(i = 0; i < data.length; i++){
        $('#search-results').append('<li>' + data[i].word + '</li>')
    }
}
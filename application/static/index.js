
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

$(document).ready(function(){
    
    //Clicking one of our selectable words in the quote
    $('.quote-word').on('click', function(e){
        clearSelectedQuoteWord();
        $(this).addClass('selected-quote-word');
        selectedWord = $(this)

        $('#quote').addClass('slide-up');
        $('#word-selector').addClass('visible');

        $.ajax({
            type : 'POST',
            url : '/top-choices',
            data : JSON.stringify(selectedWord.data()),
            contentType: 'application/json; charset=utf-8',
            success: function(result){
                $('#top-words-list').html('');

                for(var choice in result){
                    console.log(result[choice].word);
                    //TO DO: These need to be sorted by number of votes
                    $('#top-words-list').append('<li>' + result[choice].word + '<span>' + result[choice].votes + '</span></li>');
                }
            }
        });
    });

    $('#save-button').on('click', function(e){

        $.ajax({
            type : 'POST',
            url : '/save',
            data : JSON.stringify(getSelectedWords()),
            contentType: 'application/json; charset=utf-8',
            success: function(result){
                console.log(result);
            }
        });
    });
});


function addWordChoiceClickEvent(){
    $('.word-choice').on('click', function(e){
        clearSelectedWordChoice();
        $(this).addClass('selected-word-choice');

        selectedWord.html($(this).html());
    });
}


/*---------- Miscellaneous Functions -----------*/

function populateSearchResults(data){

    $('#search-results').html(' ');

    for(i = 0; i < data.length; i++){
        $('#search-results').append('<li class="word-choice">' + data[i].word + '</li>')
    }
    addWordChoiceClickEvent();
}

function getSelectedWords(){

    var selectedWords = [];

    $('.quote-word').each(function(){
        selectedWords.push($(this).html());
    });

    return selectedWords;
}

function clearSelectedQuoteWord(){
    $('.quote-word').each(function(){
        $(this).removeClass('selected-quote-word');
    });
}

function clearSelectedWordChoice(){
    $('.word-choice').each(function(){
        $(this).removeClass('selected-word-choice');
    });
}
